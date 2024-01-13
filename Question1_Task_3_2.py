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
from transformers import AutoTokenizer, AutoModel
from collections import Counter
import tensorflow as tf
import collections
import csv

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf

# Get the full path of the current file
file_path = os.path.realpath(__file__)

# Extract the directory path
directory_path = os.path.dirname(file_path)
def count_unique_tokens(text, max_length=512):
    """
    Count unique tokens in the given text using the AutoTokenizer from the Transformers library.
    Handles extremely long texts by tokenizing and processing in smaller segments.

    :param text: Text to be tokenized and analyzed.
    :param max_length: Maximum length of tokens for each segment.
    :return: A dictionary with the top 30 tokens and their counts.
    """
    # Initialize the tokenizer
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    # Split the text into words
    words = text.split()

    # Initialize variables for segment processing
    start = 0
    end = 0
    token_counts = collections.Counter()

    # Process the text in segments
    while start < len(words):
        # Prepare a segment
        segment = " ".join(words[start:end])

        # Tokenize the segment
        tokenized_segment = tokenizer.tokenize(segment)

        # Check if the tokenized segment is within the max_length or if we reached the end of the words
        if len(tokenized_segment) <= max_length or end == len(words):
            token_counts.update(tokenized_segment)
            start = end
            end += 1
        else:
            end -= 1

    # Get the top 30 tokens
    top_30_tokens = dict(token_counts.most_common(30))

    return top_30_tokens


top_30_token ={}
update_dict_1 = {}

file_path = directory_path + '/text'+'.txt'
with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
top_30_token = count_unique_tokens(text)
for key, value in top_30_token.items():
    print(key, ":", value)
with open(directory_path + '/Top30Tokens.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(('token', 'occurrences'))
    for key, value in top_30_token.items():
       writer.writerow([key, value])