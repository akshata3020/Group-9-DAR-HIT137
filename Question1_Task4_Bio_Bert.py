
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import os
import re
import zipfile
from huggingface_hub import hf_hub_download
import sys
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

count = split_file(file_path, chunk_size_mb=20)


# Load pre-trained model and tokenizer for BioBERT
def extract_disease_and_drug(text, model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)
    # Use the pipeline to identify entities in the text
    ner_results = ner_pipeline(text)
    return ner_results

# Process the results
# (Here, you can filter and separate the 'diseases' and 'drugs' entities as needed)
# Filter results for diseases and drugs
disease = []
drug = []
for i in range(count):
    i = i + 1
    file_path = directory_path + '/text' +'_part_'+str(i)+'.txt'
    print(file_path)
    with open(file_path, 'r') as file:
        text = file.read().lower().strip()
    model_name = "ugaray96/biobert_ncbi_disease_ner"

    ner_result = extract_disease_and_drug(text, model_name)
    
#    disease = [result['word'] for result in ner_result if result["entity"] == "Disease"]
    for result in ner_result:
        if result["entity"] == "Disease":
            disease.append(result['word'])
    print(disease)
    model_name = "alvaroalon2/biobert_chemical_ner"

    ner_result = extract_disease_and_drug(text, model_name)

#    drug = [result['word'] for result in ner_result if result['entity'] == 'B-CHEMICAL']
    for result in ner_result:
        if result["entity"] == "B-CHEMICAL":
            drug.append(result['word'])
    print(drug)
    if os.path.exists(directory_path + '/text' +'_part_'+str(i)+'.txt'):
        os.remove(directory_path + '/text' +'_part_'+str(i)+'.txt')


with open(directory_path+ '/text_BioBert.txt', 'w') as fp:
    fp.write("Total Extracted diseases:" + str(len(disease)) +"\n")
    for item in disease:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')
    fp.write("\nTotal Extracted drug:" + str(len(drug)) +"\n")
    for item in drug:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')