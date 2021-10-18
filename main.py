import zipfile
import os
import hashlib
import re
import requests

# task 1
directory_to_extract_to = 'C:\\Users\\HOME\\Desktop\\python'
arch_file = 'C:\\Users\\HOME\\Desktop\\python\\tiff-4.2.0_lab1.zip'

test_zip = zipfile.ZipFile(arch_file)
test_zip.extractall(directory_to_extract_to)
test_zip.close()

# task 2.1
txt_files = []
for r, d, f in os.walk(directory_to_extract_to):
    for file in f:
        if file.endswith(".txt"):
            txt_files.append(r + '\\' + file)

# task 2.2
for file in txt_files:
    target_file_data = open(file, 'rb').read()
    result = hashlib.md5(target_file_data).hexdigest()

# task 3
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

print(target_file)
print(target_file_data)

# task 4
r = requests.get(target_file_data)
result_dct = {}

counter = 0
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)

headers = []

for line in lines:
    if counter == 0:
        headers = re.sub(r'<.*?>', ';', line)
        headers = re.findall('[А-Яа-я-ё]+\s?', headers)
        counter += 1
        headers[3] = headers[3] + headers[4]
        del headers[4]
        continue
    temp = re.sub('<.*?>', ';', line)
    temp = re.sub('\(.*?\)', '', temp)
    temp = re.sub(';+', ';', temp)
    temp = re.sub('^;', '', temp)
    temp = re.sub(';$', '', temp)
    temp = re.sub('\*', ' ', temp)

    tmp_split = re.split(';', temp)
    if (len(tmp_split) == 6):
        tmp_split.remove('📝  ')
    country_name = tmp_split[0]
    country_name = re.sub('[🇦-🇿]', '', country_name)
    country_name = re.sub('🛳', '', country_name)
    country_name = re.sub(r'^\s+', '', country_name)

    col1_val = re.sub(u'\xa0', '', tmp_split[1])
    col2_val = re.sub(u'\xa0', '', tmp_split[2])
    col3_val = re.sub(u'\xa0', '', tmp_split[3])
    col4_val = re.sub(u'\xa0', '', tmp_split[4])
    if (col4_val == '_'):
        col4_val = -1

    result_dct[country_name] = {}
    result_dct[country_name][headers[0]] = int(col1_val)
    result_dct[country_name][headers[1]] = int(col2_val)
    result_dct[country_name][headers[2]] = int(col3_val)
    result_dct[country_name][headers[3]] = int(col4_val)

# task 5
output = open(directory_to_extract_to + "\\data.csv", 'w')
string_headers = "Страна;" + ';'.join(headers)
output.write(string_headers + '\n')

for key in result_dct.keys():
    output.write(str(key) + ';')
    for i in range(0, 4):
        string_to_write = str(result_dct[key][headers[i]]) + ';'
        output.write(string_to_write)
    output.write('\n')

output.close()

# task 6
target_country = input("Введите название страны: ")
try:
    string = str(result_dct[target_country])
    print(string)
except KeyError:
    print("Страны с указанным именем не существует")
