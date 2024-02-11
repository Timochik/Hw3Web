import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict


def move_file(src, dest):
    shutil.move(src, dest)


def sort_files_by_extension(folder):
    file_extension_map = defaultdict(list)
    for root, _, files in os.walk(folder):
        for file in files:
            file_extension = os.path.splitext(file)[1]
            file_extension_map[file_extension].append(os.path.join(root, file))

    with ThreadPoolExecutor(max_workers=5) as executor:
        for ext, files in file_extension_map.items():
            extension_folder = os.path.join(folder, ext)
            os.makedirs(extension_folder, exist_ok=True)
            for file in files:
                executor.submit(move_file, file, extension_folder)


if __name__ == "__main__":
    folder_path = "Хлам"  # Ваша шлях до папки "Хлам"
    sort_files_by_extension(folder_path)
