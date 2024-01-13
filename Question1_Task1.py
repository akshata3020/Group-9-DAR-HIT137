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

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Get the full path of the current file
file_path = os.path.realpath(__file__)

# Extract the directory path
directory_path = os.path.dirname(file_path)

extract_to_path = directory_path
list_of_files = []

zip_folder_path = directory_path + '/Assignment2.zip'
with zipfile.ZipFile(zip_folder_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to_path)

def fn():       # 1.Get file names from directory
    file_list=os.listdir(directory_path)
    for i in file_list:
        if i.endswith('.csv'):
            list_of_files.append(i)
    return list_of_files
list_of_files= fn()
listOf = 'CSV1.csv'
with open(directory_path + "/text.txt",'a') as file:
    for j in list_of_files:
        df = pd.read_csv(directory_path +'/'+ j.replace('.csv','') +'.csv')
        for col in df.columns:
            if 'TEXT' in col:
                df = df[[col]]
                df.to_csv(directory_path + '/text.txt', index=False, mode = 'a')
with open(directory_path +"/text.txt") as file:
    data = file.read().replace('\n',' ')