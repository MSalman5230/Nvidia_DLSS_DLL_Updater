# Nvidia_DLSS_DLL_Updater

Game Developers/Studio often do not update nvidia DLSS dll, However Nvidia constantly updates DLSS dll for better Image Quality/Stability
This program downs newest DLLs from TechPowerUp.com 
DLSS:https://www.techpowerup.com/download/nvidia-dlss-dll/
DLSS Frame Generation: https://www.techpowerup.com/download/nvidia-dlss-3-frame-generation-dll/

Then finds all the **nvngx_dlss.dll** and **nvngx_dlssg.dl** in your local game path provided in config.txt
# Running the program
Download the latest build from release and extract
In **config.txt** change the config according to your need
```bash
# TechPowerUp Dont Change if you dont know
TPU_DOWNLOAD_SERVER_ID=14 # SERVER_ID is the server location of TechPowerUp, 15=SG,14=NL,5=UK,3=USA-2
DLSS_URL=https://www.techpowerup.com/download/nvidia-dlss-dll/
DLSS_FG_URL=https://www.techpowerup.com/download/nvidia-dlss-3-frame-generation-dll/

# User Setup
GAME_PATH=E:\Games # Change to your Game Library
DLSS_ZIP_NAME=nvngx_dlss_3.5.0.zip # if want to download from link Techpowerup leave it blank or remove it
DLSS_FG_ZIP_NAME=nvngx_dlssg_3.5.0.zip # if want to download from link Techpowerup leave it blank or remove it
```
