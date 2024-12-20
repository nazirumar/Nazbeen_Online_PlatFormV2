from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get user_id from the URL
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f"notifications_{self.user_id}"

        # Add the user to the appropriate notification group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the notification group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive a message from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        # Broadcast the message to the WebSocket group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'broadcast_notification',
                'message': message,
            }
        )

    async def broadcast_notification(self, event):
        # Send message to WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
