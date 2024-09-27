import os
from minio import Minio
from motor.motor_asyncio import AsyncIOMotorClient

current_path = os.getcwd()

client = AsyncIOMotorClient("mongodb://localhost:27017")

db = client["ailearning"]



print("Current working directory:", current_path)

def get_all_files(folder_path):
    file_paths = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            file_paths.append(file_path)

    
    return file_paths

folder_path = f'{current_path}/app/data/subject/'
all_files = get_all_files(folder_path)
data = {}
for file in all_files:
    object_name = f"books/{file.replace('/home/beehyv/Documents/hackathon/ai_learning_backend/app/data/subject/', '')}".lower()
    ls = file.replace('/home/beehyv/Documents/hackathon/ai_learning_backend/app/data/subject/', '').split('/')
    if len(ls) == 3:
        subject, book, topic = ls
        subject = subject.lower()
        book = book.lower()
        if subject not in data:
            data[subject] = {}
        if book not in data[subject]:
            data[subject][book] = {}
        
        # Assign object name to the corresponding path in the dictionary
        topic = topic.replace('.pdf', '')
        data[subject][book][topic] = object_name

async def add_data_to_mongo(data):

    subjects_id = []

    for subject, books in data.items():
        books_id = []
        for book, topics in books.items():
            topics_id = []
            for topic, object_name in topics.items():
                data = {
                    'name': topic,
                    'description': f'{subject}/{book}',
                    'book_location': object_name,
                }
                result = await db["topic"].insert_one(data)
                topics_id.append(str(result.inserted_id))
            
            data = {
                'name': book,
                'topics': topics_id,
            }
            result = await db['book'].insert_one(data)
            books_id.append(str(result.inserted_id))
        data = {
            'name': subject,
            'books': books_id,
        }
        result = await db['subject'].insert_one(data)
        subjects_id.append(str(result.inserted_id))

    data = {
        'name': "X",
        'subjects': subjects_id,
    }
    result = await db["className"].insert_one(data)

import asyncio
asyncio.run(add_data_to_mongo(data))
