import zipfile
import os
import hashlib
import re
import requests

#task 1
directory_to_extract_to = 'C:\\Users\\HOME\\Desktop\\python'
arch_file = 'C:\\Users\\HOME\\Desktop\\python\\tiff-4.2.0_lab1.zip'

test_zip = zipfile.ZipFile(arch_file)
test_zip.extractall(directory_to_extract_to)
test_zip.close()

#task 2.1
txt_files = []
for r, d, f in os.walk(directory_to_extract_to):
    for file in f:
        if file.endswith(".txt"):
            txt_files.append(r + '\\' + file)
            print(os.path.join(r, file))


#task 2.2
for file in txt_files:
    target_file_data = open(file, 'rb').read()
    result = hashlib.md5(target_file_data).hexdigest()
    print(result)

#task 3
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = ''
target_file_data = ''

files_arr = []
for r, d, f in os.walk(directory_to_extract_to):
    for file in f:
        files_arr.append(os.path.join(r, file))
for file in files_arr:
    file_data = open(file, 'rb').read()
    result = hashlib.md5(file_data).hexdigest()
    if result == target_hash:
        target_file = os.path.join(file)
        target_file_data = file_data
        break

print("Абсолютный путь файла: " + target_file)
print("Содержимое файла: ")
print(target_file_data)


