from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Kriptografi')
root.geometry('720x540')

def clear():
    input_text.delete(1.0, END)
    key_entry.delete(0, END)

def encMethodHandler():
    if (method_value.get() == 1):
        vc_encrypt()
    elif (method_value.get() == 2):
        messagebox.showwarning("Error", "Metode Playfair Cipher Sedang Dalam Pengerjaan")
        # pc_encrypt()
    else:
        # messagebox.showwarning("Method", "Enkripsi ini akan menggunakan Hill Cipher")
        hill_encrypt()


def decMethodHandler():
    if (method_value.get() == 1):
        vc_decrypt()
    elif (method_value.get() == 2):
        messagebox.showwarning("Error", "metode playfair cipher sedang dalam pengerjaan")
    else:
        messagebox.showwarning("Error", "Metode hill cipher sedang dalam pengerjaan")

#Vigenère Cipher

def vc_key_generator(text, key):
    key = list(key)
    if len(text) == len(key):
        return key
    else:
        for c in range(len(text) - len(key)):
            key.append(key[c % len(key)])
    return "".join(key)
    
def vc_encrypt():
    text = input_text.get(1.0, END)
    input_text.delete(1.0, END)
    input_key = key_entry.get()

    if len(input_key) >= 12:

        encrypted = []
        key = vc_key_generator(text, input_key)
        for i in range(len(text)):
            char = text[i]
            if char.isupper():
                encrypted_char = chr((ord(char) + ord(key[i]) - 2 * ord('A')) % 26 + ord('A'))
            elif char.islower():
                encrypted_char = chr((ord(char) + ord(key[i]) - 2 * ord('a')) % 26 + ord('a'))
            else:
                encrypted_char = char
            encrypted.append(encrypted_char)
        result = "".join(encrypted)
        input_text.insert(END, result)

    else:
        messagebox.showwarning("Invalid", "Kata kunci Kurang dari 12 karakter")


def vc_decrypt():
    text = input_text.get(1.0, END)
    input_text.delete(1.0, END)
    input_key = key_entry.get()

    if len(input_key) >= 12:
        decrypted = []
        key = vc_key_generator(text, input_key)
        for i in range(len(text)):
            char = text[i]
            if char.isupper():
                decrypted_char = chr((ord(char) - ord(key[i]) + 26) % 26 + ord('A'))
            elif char.islower():
                decrypted_char = chr((ord(char) - ord(key[i]) + 26) % 26 + ord('a'))
            else:
                decrypted_char = char
            decrypted.append(decrypted_char)
        result = "".join(decrypted)
        input_text.insert(END, result)
    else:
        messagebox.showwarning("Invalid", "Kata kunci Kurang dari 12 karakter")


# Playfair Cipher

# Hill cipher

import numpy as np

def get_matrix(key):
    key = key.replace(" ", "").upper()
    size = int(len(key)**0.5)
    matrix = []
    
    for i in range(size):
        row = []
        for j in range(size):
            row.append(ord(key[i * size + j]) - ord('A'))
        matrix.append(row)

    return np.array(matrix)



def hill_encrypt():
    plaintext = input_text.get(1.0, END)
    input_text.delete(1.0, END)
    key = key_entry.get()

    if len(key) >= 12:
        plaintext = plaintext.replace(" ", "").upper()
        n = int(len(key)**0.5)
        key_matrix = get_matrix(key)
        
        # Pad plaintext to be a multiple of n
        while len(plaintext) % n != 0:
            plaintext += 'X'  # Pad with 'X'

        ciphertext = ''
        for i in range(0, len(plaintext), n):
            block = np.array([ord(char) - ord('A') for char in plaintext[i:i + n]])
            encrypted_block = (key_matrix @ block) % 26
            ciphertext += ''.join(chr(num + ord('A')) for num in encrypted_block)

        result = ciphertext
        input_text.insert(END, result)
    else:
        messagebox.showwarning("Invalid", "Kata kunci Kurang dari 12 karakter")



enc_label = Label(root, text="Plain Text/Ciper Text", font=("Helvetica", 18))

enc_label.pack()

input_text = Text(root, width=57, height=10)
input_text.pack(pady=10)

key_label = Label(root, text="Enter the key... (min 12 char)", font=("Helvetica", 18))
key_label.pack()

key_entry = Entry(root, font=("Helvetica", 18), width=35)
key_entry.pack(pady=10)


rb_frame = Frame(root)
rb_frame.pack(pady=20)

method_value = IntVar()

vigenere = Radiobutton(rb_frame, text="Vigenere Cipher", font=("Helvetica", 18), value=1, variable=method_value)
vigenere.grid(row=0, column=0)

playFair = Radiobutton(rb_frame, text="Playfair Cipher", font=("Helvetica", 18), value=2, variable=method_value)
playFair.grid(row=0, column=1)

hill = Radiobutton(rb_frame, text="Hill Cipher", font=("Helvetica", 18), value=3, variable=method_value)
hill.grid(row=0, column=2)

my_frame = Frame(root)
my_frame.pack(pady=20)

enc_button = Button(my_frame, text="Encrypt", font=("Helvetica", 18), command=encMethodHandler)
enc_button.grid(row=0, column=0)

dec_button = Button(my_frame, text="Decrypt", font=("Helvetica", 18), command=decMethodHandler)
dec_button.grid(row=0, column=1, padx=20)

clear_button = Button(my_frame, text="Clear", font=("Helvetica", 18), command=clear)
clear_button.grid(row=0, column=2)


root.mainloop()