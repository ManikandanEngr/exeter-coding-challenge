import csv
import os
import psutil
from time import process_time

t1_start = process_time()

list_of_input_text = []
list_of_find_words = []
french_dictionary = {}
list_of_find_words_temp = []
word_count = {}
find_words_french = []

with open('find_words.txt', 'r') as find_words:
    for line in find_words:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        list_of_find_words_temp.append(line_list)
    list_of_find_words = [item for sublist in list_of_find_words_temp for item in sublist]

with open('french_dictionary.csv', mode='r') as input_file_french:
    reader = csv.reader(input_file_french)
    french_dictionary = {rows[0]: rows[1] for rows in reader}

with open('t8.shakespeare.txt', 'r') as input_file:
    with open('t8.shakespeare.translated.txt', 'w') as output_file:
        for line in input_file:
            temp_line = line
            line = line.replace(',', '')
            line = line.replace('.', '')
            line = line.replace('!', '')
            stripped_line = line.strip()
            line_list = stripped_line.split()
            list_of_input_text.append(line_list)
            for words in list_of_input_text:
                for word in words:
                    if word.lower() in list_of_find_words:
                        if word_count.get(word.lower()) is None:
                            temp_line = temp_line.replace(word, french_dictionary[word.lower()])
                            word_count[word.lower()] = 1
                        else:
                            temp_line = temp_line.replace(word, french_dictionary[word.lower()])
                            word_count[word.lower()] += 1
            output_file.write(temp_line)
            list_of_input_text = []


find_words_dict = list(word_count.keys())

find_words_count = list(word_count.values())

for item in find_words_dict:
    find_words_french.append(french_dictionary[item])

csv_rows = zip(find_words_dict, find_words_french, find_words_count)

with open('frequency.csv', "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['English Word', 'French Word', 'Frequency'])
    for row in csv_rows:
        writer.writerow(row)

t1_stop = process_time()

time_of_process = t1_stop - t1_start

with open('performance.txt', 'w') as per_file:
    seconds = time_of_process % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    time_of_process_minutes = time_of_process / 60
    per_file.writelines("Time of process: " + str(int(minutes)) + ' minutes ' + str(int(seconds)) + ' seconds' + '\n')
    per_file.writelines("Memory used: " + str(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2) + ' MB')
