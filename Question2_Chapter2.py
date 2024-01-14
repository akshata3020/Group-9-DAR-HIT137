from PIL import Image
import numpy as np
import time
import os
import sys
print(os.getcwd())
# Get the full path of the current file
file_path = os.path.realpath(__file__)

# Extract the directory path
directory_path = os.path.dirname(file_path)

file_path = directory_path + '/chapter1.jpg'

# Question 2 Chapter 2

s = '56aAww1984sktr235270aYmn145ss785fsq31D0'

# declare variables
number_string = ""
letter_string = ""
ASCII_number = []
ASCII_letter = []

# split characters and numbers
for char in s:
    if char.isalpha():
        letter_string += char
    else:
        number_string += char

# ASCII values of the uppercase letters
for char in letter_string:
    if char.isupper(): # only appending uppercase letters
        ASCII_letter.append(ord(char))

#ASCII values of the even numbers
for char in number_string:
    if int(char) % 2 == 0: # only appening even numbers
        ASCII_number.append(ord(char))

print(ASCII_letter)
print(ASCII_number) 