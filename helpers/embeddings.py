from transformers import AutoTokenizer, AutoModel
import torch
from courses.models import Course

def generate_embedding(text):
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L12-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L12-v2")
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings

def store_embeddings():
    courses = Course.objects.all()
    for course in courses:
        text = f"{course.title} {course.description}"
        embedding = generate_embedding(text)
        course.embedding = embedding
        course.save()
