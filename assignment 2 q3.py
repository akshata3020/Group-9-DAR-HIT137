# The code here decrypts the encrypted code saved in "encrypted_text.txt"
# Saves the decrypted code in "decrypted_code.txt"

def decrypt(text, key):
    """This function decrypts encrypted text using a key"""
    
    decrypted_text = "" # declare variables

    for char in text: # iterate through each character
        
        if char.isalpha(): # if character is a letter we implement decryption process
            shifted = ord(char) - key # reverse operation to encryption
            
            if char.islower(): # decrypt lowercase letters outside bounds
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26

            elif char.isupper(): # decrypt uppercase letters outside bounds
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            decrypted_text += chr(shifted)

        else: # if character is not a letter, it does not need to be decrypted
            decrypted_text += char

    return decrypted_text


total = 0 # total is equivalent to key

## THIS CODE IS FROM TASK SHEET
## _____________________________________
for i in range(5):
    for j in range(3):
        if i + j == 5:
            total += i + j
        else:
            total -= i - j

counter = 0
while counter < 5:
    if total < 13:
        total += 1
    elif total > 13:
        total -= 1
    else:
        counter += 2
## _____________________________________

with open("encrypted_text.txt", "r") as file:
    text = file.read() # single string containing encrypted text

decrypted_text = decrypt(text, total) # text decrypted

with open("decrypted_text.txt", "w") as file:
    file.write(decrypted_text) # saving decrypted text to new file
