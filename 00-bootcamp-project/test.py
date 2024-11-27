import os

folder_path = "data"

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, file_name)):
        print(file_name)