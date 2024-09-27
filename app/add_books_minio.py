import os
from minio import Minio

current_path = os.getcwd()
minio_client = Minio(
        "localhost:9000",
        access_key="71yeZzM1n5GX8q6Ts8HU",
        secret_key="Dw1g2b7zzbrbhyZ4ibf88xua09a3S309CrVB6tC9",
        secure=False
        )


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

for file in all_files:
    object_name = f"books/{file.replace('/home/beehyv/Documents/hackathon/ai_learning_backend/app/data/subject/', '')}".lower()
    minio_client.fput_object("ailearning", object_name, file, content_type="application/pdf")
