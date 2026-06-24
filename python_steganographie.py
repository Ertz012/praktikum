from PIL import Image
import tkinter as tk
from tkinter import messagebox
window = tk.Tk()
window.title("Steganographie")
window.geometry("500x300")
img = Image.open("HobbyTown_USA_Oshkosh_interior_under_construction_2002.png")
width, height = img.size
total_pixels = width * height
def hide():
    text = eingabe.get() + "\0"
    binary = "".join(format(ord(char), "08b") for char in text)
    img = Image.open("HobbyTown_USA_Oshkosh_interior_under_construction_2002.png")
    pixels = img.load()
    for i in range(len(binary)):
        x = i % width
        y = i // width
        r, g, b = pixels[x, y]
        new_r = (r & ~1) | int(binary[i])
        pixels[x, y] = (new_r, g, b)
    img.save("output.png")
    messagebox.showinfo("Done", "Message hidden in output.png")
def reveal():
    img = Image.open("output.png")
    pixels = img.load()
    message = ""
    bits = ""
    for i in range(total_pixels):
        x = i % width
        y = i // width
        r, g, b = pixels[x, y]
        bits += str(r & 1)
        if len(bits)==8:
            char=chr(int(bits, 2))
            bits=""
            if char == "\0":
                break
            else:
                message = message + char 
    messagebox.showinfo("Done", message)
        
eingabe = tk.Entry(window)
eingabe.pack()
button = tk.Button(window, text="Verstecken", command=hide)
button.pack()
button = tk.Button(window, text="Die versteckte Botschaft finden", command=reveal)
button.pack()
window.mainloop()