import pandas as pd
import os
import re
import csv
import sys
import zipfile
from transformers import AutoTokenizer
from huggingface_hub import hf_hub_download
from transformers.models.bert.modeling_bert import BertLayer
from transformers import AutoTokenizer
from collections import Counter
import sys

file_path = os.path.realpath(__file__)

# Extract the directory path
directory_path = os.path.dirname(file_path)
with open(directory_path +'\\text.txt') as file:
    data = file.read().replace('\n',' ')
# Define a function named word_count that takes one argument, 'str'.
def word_count(str):
    # Create an empty dictionary named 'counts' to store word frequencies.
    counts = dict()
    
    # Split by regular expression the input string 'str' into a list of words using spaces as separators and store it in the 'words' list.
    words = re.sub(r"[^a-zA-Z]", " ", str).split()

    # Iterate through each word in the 'words' list.
    for word in words:
        # Check if the word is already in the 'counts' dictionary.
        if word in counts:
            # If the word is already in the dictionary, increment its frequency by 1.
            counts[word] += 1
        else:
            # If the word is not in the dictionary, add it to the dictionary with a frequency of 1.
            counts[word] = 1

    # Return the 'counts' dictionary, which contains word frequencies.
    return counts
sorted_list = sorted(word_count(data).items(), key = lambda x:x[1], reverse = True)
Print_List = []
count = 0
while (count < 31):
    Print_List.append(sorted_list[count])
    count = count + 1
for i in Print_List:
    print(i)
field_names = ['word', 'occurrences']
with open(directory_path +'\\Top30Words.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(('word', 'occurrences'))
    for row in Print_List:
        writer.writerow(row)
