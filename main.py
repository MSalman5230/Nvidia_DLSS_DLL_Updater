import requests
import shutil
import os
import time
from bs4 import BeautifulSoup
import zipfile
from dotenv import load_dotenv
import datetime
import re

load_dotenv()
game_paths_list = os.environ.get("GAME_PATH")
game_paths_list = [path.strip() for path in game_paths_list.split(",")]
game_paths_list = [path for path in game_paths_list if path]
# print(game_paths_list)
TPU_DOWNLOAD_SERVER_ID = 14
urls = {"DLSS": "https://www.techpowerup.com/download/nvidia-dlss-dll/", "DLSS_FG": "https://www.techpowerup.com/download/nvidia-dlss-3-frame-generation-dll/"}


def is_empty_or_whitespace(input_string):
    if input_string is None:
        return True
    return re.match(r"^\s*$", input_string) is not None


def get_file_id(url):
    try:
        response = requests.get(url).text
        soup = BeautifulSoup(response, "lxml")

        dll = soup.find("div", {"class": "version"})
        file_name = dll.find("div", {"class": "filename"})
        file_name = file_name.text
        id = dll.find("input", {"name": "id"})
        id = id["value"]
        return id, file_name
    except Exception as e:
        print(f"Failed to scrape {url}:{e}")
        exit()


def check_if_zip_exists(file_name):
    if os.path.exists(file_name):
        # print(f"The file at '{file_name}' exists.")
        return True

    # print(f"The file at '{file_name}' does not exist.")
    return False


def download_dll_zip(url, id, file_name):
    payload = {"server_id": TPU_DOWNLOAD_SERVER_ID, "id": id}
    print(f"Downloading {file_name} ......")
    response = requests.request("POST", url, data=payload)
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
            print(f"{file_name} successfully downloaded")
            return file_name

    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        exit()


def extract_zip_file(zip_file_name):
    try:
        print(f"Extracting {zip_file_name}")
        # Open the specified zip file
        with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
            # Extract all the contents to the root location (current working directory)
            zip_ref.extractall("")

        print(f"Successfully extracted '{zip_file_name}' to root location")
    except zipfile.BadZipFile as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def check_DLL_exists_in_root(DLSS_FG_Game_exists):
    if not os.path.exists("nvngx_dlss.dll"):
        print("nvngx_dlss.dll not found in root location \nexiting..")
        exit()
    if DLSS_FG_Game_exists and not os.path.exists("nvngx_dlssg.dll"):
        print("nvngx_dlssg.dll not found in root location \nexiting..")
        exit()


def find_dll_files(game_paths_list):
    dll_files = []
    DLSS_FG_Game = False
    for directory in game_paths_list:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename in ["nvngx_dlss.dll", "nvngx_dlssg.dll"]:
                    file_path = os.path.join(root, filename)
                    dll_files.append(file_path)
                    if filename == "nvngx_dlssg.dll":
                        DLSS_FG_Game = True

    return dll_files, DLSS_FG_Game


def copy_new_dll(file_path):
    directory, filename = os.path.split(file_path)
    try:
        # directory_path = os.path.dirname(directory)
        # directory, filename = os.path.split(file_path)
        # Move the file from the source to the destination
        shutil.copy(filename, directory)
        print(f"Copied {filename} to {directory}")
    except Exception as e:
        print(f"Failed to copy {filename} to {directory} :{e}")


def rename_old_DLLs(dll_files_paths):
    # Get the current date and time
    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Iterate through the file paths and rename the files in place
    for file_path in dll_files_paths:
        try:
            if os.path.exists(file_path):
                directory, filename = os.path.split(file_path)
                base_filename, extension = os.path.splitext(filename)
                # new_filename = f"{base_filename}_Backup_{current_date}{extension}"
                new_filename = f"{filename}_Backup_{current_date}"
                new_file_path = os.path.join(directory, new_filename)
                # Rename the file in place
                os.rename(file_path, new_file_path)
                print(f"Renamed '{filename}' to '{new_filename}' in place")
                copy_new_dll(file_path)
            else:
                print(f"File '{file_path}' does not exist")
        except Exception as e:
            print(f"Failed to rename {file_path}:{e}")


if __name__ == "__main__":
    # Find All the DLLs in game path
    print(f"Finding path for nvngx_dlssg.dll and nvngx_dlss.dll in {game_paths_list}")
    dll_files_paths, DLSS_FG_Game_exists = find_dll_files(game_paths_list)
    if len(dll_files_paths) == 0:
        print("No Games found with nvngx_dlssg.dll or nvngx_dlss.dll \n Exiting..")
        exit()

    print(f"Found {dll_files_paths}")

    # print(f"Check if DLL Zip location provided")
    # Check if DLL Download is needed
    DLSS_ZIP_Location = os.environ.get("DLSS_ZIP")
    DLSS_FG_ZIP_Location = os.environ.get("DLSS_FG_ZIP")
    # print(" --------",DLSS_ZIP_Location,"-----",type(DLSS_ZIP_Location))
    # Download DLSS zip if not present

    if not check_if_zip_exists(DLSS_ZIP_Location) and is_empty_or_whitespace(DLSS_ZIP_Location):
        url = urls["DLSS"]
        id, file_name = get_file_id(url)
        DLSS_ZIP_Location = download_dll_zip(url, id, file_name)

    # Download DLSS Frame Gen zip if not present
    if not check_if_zip_exists(DLSS_FG_ZIP_Location) and is_empty_or_whitespace(DLSS_FG_ZIP_Location):
        if DLSS_FG_Game_exists:
            url = urls["DLSS_FG"]
            id, file_name = get_file_id(url)
            DLSS_FG_ZIP_Location = download_dll_zip(url, id, file_name)
        else:
            print("Skipping download of Frame Generation DLL as there is no game with Frame Generation")

    # Extract Downloaded File
    extract_zip_file(DLSS_ZIP_Location)

    if DLSS_FG_Game_exists:
        extract_zip_file(DLSS_FG_ZIP_Location)

    # check if the extraction was in correct
    check_DLL_exists_in_root(DLSS_FG_Game_exists)
    # Create Back of Old DLLs and Copy New
    rename_old_DLLs(dll_files_paths)

    print("Done")

    pass
