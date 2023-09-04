import requests
import shutil
import os
import time
from bs4 import BeautifulSoup

url="https://www.techpowerup.com/download/nvidia-dlss-dll/"
source_code = requests.get(url).text
soup = BeautifulSoup(source_code, "lxml")
#elements = soup.find_all(True, {"class": "versions"})
#elements = soup.find(False, {"class": "version"})

# Find the <form> element
form = soup.find("form", {"class": "download-version-form"})

# Find the <input> element within the <form> by name
input_element = form.find("input", {"name": "id"})

# Get the value attribute of the <input> element
value = input_element["value"]

print(value)