from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.runnables import RunnableLambda, RunnableWithFallbacks
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field
from typing import Any
from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict
from typing import Annotated, Literal

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class SQLChatBot:
    def __init__(self, db_url: str, groq_model: str, groq_api_key: str):
        # Initialize SQLAlchemy engine and database
        self.engine = create_engine(db_url)
        self.db = SQLDatabase(self.engine)

        # Initialize GroQ LLM
        self.llm = ChatGroq(model=groq_model, api_key=groq_api_key)

        # Define SQL tool
        @tool
        def db_query_tool(query: str) -> str:
            """
            Execute a SQL query against the database and return the result.
            """
            result = self.db.run_no_throw(query)
            if not result:
                return "Error: Query failed. Please rewrite your query and try again."
            return result

        self.db_query_tool = db_query_tool

        # SQL query check prompt
        self.query_check_prompt = ChatPromptTemplate.from_messages([
            ("ai", """You are a SQL expert with a strong attention to detail.
                        Double check the SQLite query for common mistakes, including:
                        - Using NOT IN with NULL values
                        - Using UNION when UNION ALL should have been used
                        - Using BETWEEN for exclusive ranges
                        - Data type mismatch in predicates
                        - Properly quoting identifiers
                        - Using the correct number of arguments for functions
                        - Casting to the correct data type
                        - Using the proper columns for joins

                        If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

                        You will call the appropriate tool to execute the query after running this check."""), 
            ("placeholder", "{messages}")
        ])

        # Query generation prompt
        self.query_gen_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a SQL expert with a strong attention to detail.

Given an input question, output a syntactically correct SQLite query to run, then look at the results of the query and return the answer.

DO NOT call any tool besides SubmitFinalAnswer to submit the final answer.

When generating the query:

Output the SQL query that answers the input question without a tool call.

Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.

If you get an error while executing a query, rewrite the query and try again.

If you get an empty result set, you should try to rewrite the query to get a non-empty result set.
NEVER make stuff up if you don't have enough information to answer the query... just say you don't have enough information.

If you have enough information to answer the input question, simply invoke the appropriate tool to submit the final answer to the user.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database. Do not return any sql query except answer."""), 
            ("placeholder", "{messages}")
        ])

        # Workflow graph
        self.workflow = self._initialize_workflow()

    def create_tool_node_with_fallback(self, tools: list) -> RunnableWithFallbacks[Any, dict]:
        return ToolNode(tools).with_fallbacks([RunnableLambda(self.handle_tool_error)], exception_key="error")

    def handle_tool_error(self, state: dict) -> dict:
        error = state.get("error")
        tool_calls = state.get("messages", [])[-1].get("tool_calls", [])
        return {
            "messages": [
                ToolMessage(content=f"Error: {repr(error)}\nPlease fix your mistakes.", tool_call_id=tc["id"])
                for tc in tool_calls
            ]
        }

    def model_check_query(self, state: dict) -> dict:
        # Ensure that we invoke with valid messages
        messages = [AIMessage(content=str(state["messages"][-1]))]
        return {"messages": messages}

    def query_gen_node(self, state: dict) -> dict:
        message = self.query_gen_prompt.invoke(state)
        tool_messages = []
        if getattr(message, "tool_calls", None):
            for tc in message.tool_calls:
                if tc["name"] != "SubmitFinalAnswer":
                    tool_messages.append(
                        ToolMessage(
                            content=f"Error: The wrong tool was called: {tc['name']}. Please fix your mistakes. "
                                    f"Remember to only call SubmitFinalAnswer to submit the final answer. "
                                    f"Generated queries should be outputted WITHOUT a tool call.",
                            tool_call_id=tc["id"],
                        )
                    )
        return {"messages": [AIMessage(content=str(message))] + tool_messages}

    def should_continue(self, state: dict) -> str:
        messages = state["messages"]
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None):
            return END
        if last_message.content.startswith("Error:"):
            return "query_gen"
        else:
            return "correct_query"

    def _initialize_workflow(self) -> StateGraph:
        workflow = StateGraph(State)

        # Ensure we reference the method without calling it
        workflow.add_node("first_tool_call", self.first_tool_call)

        workflow.add_node("list_tables_tool", self.create_tool_node_with_fallback([self.db_query_tool]))
        workflow.add_node("get_schema_tool", self.create_tool_node_with_fallback([self.db_query_tool]))

        model_get_schema = self.llm.bind_tools([self.db_query_tool])
        workflow.add_node("model_get_schema", lambda state: {"messages": [model_get_schema.invoke(state["messages"])]})

        workflow.add_node("query_gen", self.query_gen_node)
        workflow.add_node("correct_query", self.model_check_query)
        workflow.add_node("execute_query", self.create_tool_node_with_fallback([self.db_query_tool]))
        
        workflow.add_edge(START, "first_tool_call")  # Start at the first tool call node
        workflow.add_edge("first_tool_call", "list_tables_tool")
        workflow.add_edge("list_tables_tool", "model_get_schema")
        workflow.add_edge("model_get_schema", "get_schema_tool")
        workflow.add_edge("get_schema_tool", "query_gen")
        workflow.add_conditional_edges("query_gen", self.should_continue, {
            END: END,
            "query_gen": "query_gen",
            "correct_query": "correct_query"
        })
        workflow.add_edge("correct_query", "execute_query")
        workflow.add_edge("execute_query", "query_gen")
        
        app = workflow.compile()
        return app

    def first_tool_call(self, state:State)->dict[str,list[AIMessage]]:
        return {"messages": [AIMessage(content="",tool_calls=[{"name":"sql_db_list_tables","args":{},"id":"tool_abcd123"}])]}


    def run_query(self, user_query: str) -> Any:
        query={"messages": [("user", user_query)]}
        return self.workflow.invoke(query, {"recursion_limit": 100})