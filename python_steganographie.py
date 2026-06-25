from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from Crypto.Cipher import AES
import hashlib
window = tk.Tk()
window.title("Steganographie")
window.geometry("800x600")
label_original = tk.Label(window)
label_original.pack()
label_output = tk.Label(window)
label_output.pack()
def choose_file():
    global img, width, height, total_pixels, path
    path = filedialog.askopenfilename(filetypes=[("Images", "*.png")])
    img = Image.open(path)
    width, height = img.size
    total_pixels = width * height
    photo = ImageTk.PhotoImage(img)
    label_original.config(image=photo)
    label_original.image = photo 
def hide():
    key = hashlib.sha256(password.get().encode()).digest()
    cipher = AES.new(key, AES.MODE_EAX)
    text = eingabe.get()
    ciphertext, tag = cipher.encrypt_and_digest(text.encode())
    binary = "".join(format(byte, "08b") for byte in ciphertext)
    global nonce, ciphertext_length
    nonce = cipher.nonce
    ciphertext_length = len(ciphertext)
    length_binary = format(ciphertext_length, "032b")
    full_binary = length_binary + binary
    pixels = img.load()
    for i in range(len(full_binary)):
        x = i % width
        y = i // width
        r, g, b = pixels[x, y]
        new_r = (r & ~1) | int(full_binary[i])
        pixels[x, y] = (new_r, g, b)
    img.save("output.png")
    output_img = Image.open("output.png")
    photo = ImageTk.PhotoImage(output_img)
    label_output.config(image=photo)
    label_output.image = photo 
    window.clipboard_clear()
    window.clipboard_append(nonce.hex())
    window.update()
    messagebox.showinfo("Done", f"Message hidden!\nNonce (kopiert): {nonce.hex()}")
def reveal():
    key = hashlib.sha256(password.get().encode()).digest()
    cipher2 = AES.new(key, AES.MODE_EAX, nonce = bytes.fromhex(nonce_entry.get()))
    img = Image.open("output.png")
    pixels = img.load()
    message = ""
    bits = ""
    length_bits = ""
    for i in range(32):
        x = i % width
        y = i // width
        r, g, b = pixels[x, y]
        length_bits += str(r & 1)
    ciphertext_length = int(length_bits, 2)
    for i in range(32, 32+ciphertext_length * 8):
        x = i % width
        y = i // width
        r, g, b = pixels[x, y]
        bits += str(r & 1)
        if len(bits) == 8:
            char = chr(int(bits, 2))
            bits = ""
            message += char
    ciphertext_bytes = bytes([ord(c) for c in message])
    decrypted = cipher2.decrypt(ciphertext_bytes)
    messagebox.showinfo("Done", decrypted.decode())
tk.Label(window, text="Nachricht:").pack()    
eingabe = tk.Entry(window)
eingabe.pack()
tk.Label(window, text="Passwort:").pack()
password = tk.Entry(window)
password.pack()
tk.Label(window, text="Nonce:").pack()
nonce_entry = tk.Entry(window)
nonce_entry.pack()
button = tk.Button(window, text="Verstecken", command=hide)
button.pack()
button = tk.Button(window, text="Die versteckte Botschaft finden", command=reveal)
button.pack()
button = tk.Button(window, text="Bild auswählen", command=choose_file)
button.pack()
window.mainloop()