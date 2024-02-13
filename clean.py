import os
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

def get_file_extensions(folder_path):
    file_extensions = defaultdict(list)
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_name, extension = os.path.splitext(file)
            file_extensions[extension].append(os.path.join(root, file))
    return file_extensions

def move_file(file_path, destination_folder):
    try:
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(destination_folder, file_name)
        os.replace(file_path, destination_path)
        print(f"Moved {file_path} to {destination_path}")
    except Exception as e:
        print(f"Failed to move {file_path}: {e}")

def sort_files_by_extension(folder_path, destination_folder):
    file_extensions = get_file_extensions(folder_path)
    with ThreadPoolExecutor() as executor:
        for extension, files in file_extensions.items():
            extension_folder = os.path.join(destination_folder, extension[1:].lower())
            if not os.path.exists(extension_folder):
                os.makedirs(extension_folder)
            for file_path in files:
                executor.submit(move_file, file_path, extension_folder)

if __name__ == "__main__":
    source_folder = "C:\projects\goit\Hw3web\Hw3Web\Chlam"  # Замініть на ваш шлях до папки "Хлам"
    destination_folder = "C:\projects\goit\Hw3web\Hw3Web\Sorted"  # Замініть на ваш шлях до папки, куди будуть переміщені файли
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    print("Початок сортування файлів...")
    sort_files_by_extension(source_folder, destination_folder)
    print("Сортування завершено.")
