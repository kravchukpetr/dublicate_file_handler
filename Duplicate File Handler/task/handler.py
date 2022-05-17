import os
import sys
import hashlib

def get_file_hash(file):
    md5 = hashlib.md5()
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    hash_str = md5.hexdigest()
    return hash_str

try:
    root_folder = sys.argv[1]
except:
    print('Directory is not specified')
    exit()
file_format = input("Enter file format:")
while True:
    print('Size sorting options:')
    print('1. Descending')
    print('2. Ascending')
    order = input()
    if order == '1' or order == '2':
        order = int(order)
        break
    else:
        print("Wrong option")
listOfFiles = []
dictOfFiles = {}
sorted_dict2 ={}
for (dirpath, dirnames, filenames) in os.walk(root_folder):
    listOfFiles += [{os.path.join(dirpath, file): os.path.getsize(os.path.join(dirpath, file))} for file in filenames if ('.' + file_format in file or file_format == "")]
for file in listOfFiles:
    dictOfFiles[list(file.keys())[0]] = list(file.values())[0]
sorted_tuples = sorted(dictOfFiles.items(), key=lambda item: (1 if order == 2 else -1) * item[1])
sorted_dict = {k: [v, get_file_hash(k)] for k, v in sorted_tuples}
for k, v in sorted_tuples:
    if (v, get_file_hash(k)) not in sorted_dict2.keys():
        sorted_dict2[(v, get_file_hash(k))] = []
    sorted_dict2[(v, get_file_hash(k))].append(k)

prev_value = 0
for key, value in sorted_dict.items():
    if value[0] != prev_value:
        print(value[0], 'bytes')
        prev_value = value[0]
    print(key)
while True:
    is_check = input('Check for duplicates?')
    if is_check == 'yes' or is_check == 'no':
        break
dubl_files = []
if is_check == 'yes':
    number_of_dubl_files = 1
    prev_value = 0
    for key, value in sorted_dict2.items():
        if len(value) > 1:
            if key[0] != prev_value:
                print(key[0], 'bytes')
                prev_value = key[0]
            print('Hash:', key[1])
            for file in value:
                print(str(number_of_dubl_files) + '.', file)
                dubl_files.append({'file': file, 'file_number': number_of_dubl_files, 'file_size': key[0]})
                number_of_dubl_files += 1
while True:
    is_delete = input('Delete files?')
    if is_delete == 'yes' or is_delete == 'no':
        break
if is_delete == 'yes':
    while True:
        try:
            list_to_delete = list(str(input('Enter file numbers to delete:')).replace(' ', ''))
            if len(list_to_delete) > 0:
                if any([int(file_num) > number_of_dubl_files for file_num in list_to_delete]):
                    print('Wrong format')
                else:
                    break
            else:
                print('Wrong format')
        except:
            print('Wrong format')
    feed_up_space = 0
    if len(list_to_delete) > 0:
        for file in dubl_files:
            if file['file_number'] in list(map(int, list_to_delete)):
                os.remove(file['file'])
                feed_up_space += file['file_size']
        print('Total freed up space: {0} bytes'.format(feed_up_space))

