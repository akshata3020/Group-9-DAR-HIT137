def decrypt(encrypted_text, key):
    decrypted_text = ""
    for char in encrypted_text:
        if char.isalpha():  # 检查字符是否为字母
            shifted = ord(char) - key
            if char.islower():
                if shifted < ord('a'):
                    shifted += 26
                elif shifted > ord('z'):
                    shifted -= 26
            elif char.isupper():
                if shifted < ord('A'):
                    shifted += 26
                elif shifted > ord('Z'):
                    shifted -= 26
            decrypted_text += chr(shifted)
        else:
            decrypted_text += char
    return decrypted_text

# 使用密钥13来解密文本
with open('encrypted_text.txt', 'r') as file:
    encrypted_text = file.read()
decrypted_text = decrypt(encrypted_text, 13)
print(decrypted_text)



