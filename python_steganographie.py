from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
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
    text = eingabe.get() + "\0"
    binary = "".join(format(ord(char), "08b") for char in text)
    pixels = img.load()
    for i in range(len(binary)):
        x = i % width
        y = i // width
        r, g, b = pixels[x, y]
        new_r = (r & ~1) | int(binary[i])
        pixels[x, y] = (new_r, g, b)
    img.save("output.png")
    output_img = Image.open("output.png")
    photo = ImageTk.PhotoImage(output_img)
    label_output.config(image=photo)
    label_output.image = photo 
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
button = tk.Button(window, text="Bild auswählen", command=choose_file)
button.pack()
window.mainloop()