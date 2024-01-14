import spacy
import os
import re
import csv
import sys
import zipfile
from transformers import AutoTokenizer
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer
from collections import Counter
import sys
from transformers import AutoTokenizer, AutoModel
from collections import Counter
import collections
import csv

# Get the full path of the current file
file_path = os.path.realpath(__file__)

# Extract the directory path
directory_path = os.path.dirname(file_path)

file_path = directory_path + '/text.txt'
def split_file(file_path, chunk_size_mb=2):
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

def remove_nonwords(s):
    return [word for word in s if word.isalpha()]

def extract(doc, diseases_list, drugs_list):
    for ent in doc.ents:
        # Check if ent is a Span object and has a text attribute
        if isinstance(ent, spacy.tokens.Span) and hasattr(ent, 'label_'):
            if ent.label_ == "DISEASE" and ent.text not in diseases_list:
                diseases_list.append(ent.text)
            elif ent.label_ == "CHEMICAL" and ent.text not in drugs_list:
                drugs_list.append(ent.text)

# Load the model
model = spacy.load("en_ner_bc5cdr_md")
diseases = []
drugs = []

for i in range(2):
    i = i + 1
    file_path = directory_path + '/text' +'_part_'+str(i)+'.txt'
    print(file_path)
    with open(file_path, 'r') as file:
        text = file.read().lower().strip()
        model.max_length = len(text) + 100
        doc = model(text)
    extract(doc, diseases, drugs)
    if os.path.exists(directory_path + '/text' +'_part_'+str(i)+'.txt'):
        os.remove(directory_path + '/text' +'_part_'+str(i)+'.txt')
print("This is the entities detected by model en_ner_bc5cdr_md \n")

print(f"Extracted {len(diseases)} diseases: {diseases}")

with open(directory_path+ '/text_bc5cdr.txt', 'w') as fp:
    fp.write("Total Extracted diseases:" + str(len(diseases)))
    fp.write("diseases extracted \n \n")
    for item in diseases:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')
print(f"Extracted {len(drugs)} drugs: {drugs}")

with open(directory_path+'/text_bc5cdr.txt', 'w') as fp:
    fp.write("Total Extracted drug:" + str(len(drugs)))
    for item in drugs:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')
