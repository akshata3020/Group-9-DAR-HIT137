import pandas as pd
import os
import csv
from transformers.models.bert.modeling_bert import BertLayer
from transformers import AutoTokenizer
import sys
from transformers import AutoTokenizer, AutoModel
from collections import Counter
import collections
import csv
def split_file(file_path, chunk_size_mb=20):
    chunk_size = chunk_size_mb * 1024 * 1024  # Convert MB to bytes
    file_number = 1

    with open(file_path, 'rb') as file:
        chunk = file.read(chunk_size)
        while chunk:
            with open(directory_path+'/text'+f"_part_{file_number}"+".txt", 'wb') as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = file.read(chunk_size)
# Usage
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf

# Get the full path of the current file
file_path = os.path.realpath(__file__)

# Extract the directory path
directory_path = os.path.dirname(file_path)

file_path = directory_path + '/text.txt'

# Split the text file into smaller files for faster process
def split_file(file_path, chunk_size_mb=20):
    chunk_size = chunk_size_mb * 1024 * 1024  # Convert MB to bytes
    file_number = 1
    with open(file_path, 'rb') as file:
        chunk = file.read(chunk_size)
        while chunk:
            with open(directory_path+'/text'+f"_part_{file_number}"+".txt", 'wb') as chunk_file:
                chunk_file.write(chunk)
            file_number += 1
            chunk = file.read(chunk_size)
    return file_number
count = split_file(file_path) - 1
# Count unique token
def count_unique_tokens(file_path):
    # Load a tokenizer
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    # Counter to hold token counts
    token_counts = collections.Counter()
    max_length = 512
    # Read the file and tokenize
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Process the line in chunks
            for i in range(0, len(line), max_length):
                chunk = line[i:i+max_length]
                tokens = tokenizer.tokenize(chunk)
                token_counts.update(tokens)

    # Get the top 30 most common tokens
    top_30_tokens = token_counts.most_common(30)

    return top_30_tokens


top_30_token ={}
update_dict_1 = {}
for i in range(count):
    i = i + 1
    file_path = directory_path + '/text' +'_part_'+str(i)+'.txt'
    print(file_path)
    update_dict_1.update(count_unique_tokens(file_path))
    for key, value in update_dict_1.items():
        if key in top_30_token:
            top_30_token[key] += value
        else:
            top_30_token[key] = value
    update_dict_1 = {}
    if os.path.exists(directory_path + '/text' +'_part_'+str(i)+'.txt'):
        os.remove(directory_path + '/text' +'_part_'+str(i)+'.txt')

sorted_dict = dict(sorted(top_30_token.items(), key=lambda item: item[1], reverse=True))

for key, value in sorted_dict.items():
    print(key, ":", value)
with open(directory_path + '/Top30Tokens.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(('token', 'occurrences'))
    for key, value in sorted_dict.items():
       writer.writerow([key, value])