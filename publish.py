# Publish web files to the Arduino data folder
import os
from os import listdir
from os.path import isfile, join
import subprocess

source_path = "C:\\Users\\delimas\\PycharmProjects\\python-webserver-part-2\\public"
dest_path = "C:\\Users\\delimas\\Documents\\Arduino\\ESP_Chart_Web_Server\\data"
gz_path = '"C:\\Program Files\\7-Zip\\7Z.exe"'

files = [f for f in listdir(source_path) if isfile(join(source_path, f))]

for file in files:
    source = join(source_path, file)
    dst = join(dest_path, file + '.gz')
    if os.path.isfile(dst):
        os.remove(dst)
    command = gz_path +  ' a -tgzip "' + dst + '" "' + source + '"'
    subprocess.call(command)
