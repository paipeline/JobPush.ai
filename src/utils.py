import os

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_to_file(content, file_path):
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(content)
    print(f"Content saved to {file_path}")
