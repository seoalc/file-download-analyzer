import requests
import zipfile
from pathlib import Path
from collections import Counter
import time

def get_file_names():
    url = "http://91.199.149.128:18001/api/files/names"  # Replace with the actual API endpoint
    response = requests.get(url, timeout=10)

    response.raise_for_status()
    
    data = response.json()
    
    return data['file_names']

def download_files(chunk, index):
    url = f"http://91.199.149.128:18001/api/files/download"

    while True:

        response = requests.post(
            url,
            json={
                "file_names": chunk
            },
            timeout=10
        )

        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 1))
            print(f"Rate limit. Waiting {retry_after} seconds...")
            time.sleep(retry_after)
            continue

        response.raise_for_status()
        break

    response.raise_for_status()

    archive_path = f"downloads/archive_{index}.zip"

    with open(archive_path, "wb") as file:
        file.write(response.content)

    with zipfile.ZipFile(archive_path, "r") as zip_file:
        zip_file.extractall(f"downloads/extracted")

def mark_downloaded(file_names):
    url = f"http://91.199.149.128:18001/api/files/downloaded"
    response = requests.post(
        url,
        json={
            "file_names": file_names
        },
        timeout=10
    )

    response.raise_for_status()

def read_downloaded_files():
    folder_path = Path(f"downloads/extracted")

    file_statistics = []

    for file in folder_path.iterdir():
        if file.is_file():
            print(file.name)

            content = file.read_text(encoding='utf-8')
            counter = Counter(content)
            file_statistics.append(
                {
                    "file_name": file.name
                }
            )
    return {
        "files": file_statistics
    }

def calculate_statistics(selected_files):
    folder_path = Path(f"downloads/extracted")
    
    total_counter = Counter()
    file_statistics = []

    for file in folder_path.iterdir():
        if file.is_file():
            print(file.name)

            content = file.read_text(encoding='utf-8')
            counter = Counter(content)
            file_statistics.append(
                {
                    "file_name": file.name,
                    "statistics": dict(counter)
                }
            )
            total_counter.update(counter)
    return {
        "files": file_statistics,
        "total": dict(total_counter)
    }

def download_all_files():
    files = get_file_names()
    for index in range(0, len(files), 3):
        chunk = files[index : index + 3]
        download_files(chunk, index)
        mark_downloaded(chunk)
    read_downloaded_files()