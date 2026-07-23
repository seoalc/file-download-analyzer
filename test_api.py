import requests
import zipfile
from pathlib import Path
from collections import Counter

def get_file_names():
    url = "http://91.199.149.128:18001/api/files/names"  # Replace with the actual API endpoint
    response = requests.get(url, timeout=10)

    response.raise_for_status()

    print(f"Status Code: {response.status_code}")
    
    data = response.json()
    
    return data['file_names']

def download_files(chunk, index):
    url = f"http://91.199.149.128:18001/api/files/download"
    response = requests.post(
        url,
        json={
            "file_names": chunk
        },
        timeout=10
    )

    response.raise_for_status()

    archive_path = f"downloads/archive_{index}.zip"

    with open(archive_path, "wb") as file:
        file.write(response.content)

    with zipfile.ZipFile(archive_path, "r") as zip_file:
        # print(dir(zip_file))
        print(zip_file.namelist())
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
            # for index in range(10):
            #     digit_count = content.count(str(index))
            #     print(f"{index}: {digit_count}")



files = get_file_names()

for index in range(0, len(files), 3):
    chunk = files[index : index + 3]
    download_files(chunk, index)
    # mark_downloaded(chunk)
read_downloaded_files()
