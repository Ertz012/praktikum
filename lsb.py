from PIL import Image
import numpy as np

# 1. Bild laden und in ein Numpy-Array konvertieren
img = Image.open("input.png")
data = np.array(img)

# 2. Text in eine Liste von Bits umwandeln
secret_text = "Hi"
# TIPP für den Studenten: Schau dir bin(ord(char)) an und sorge dafür, 
# dass jedes Zeichen exakt 8 Bits lang ist (mit führenden Nullen).
bits = [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1] # Als Beispiel

# 3. Schleife über die Bits und Einbettung in den Rot-Kanal
# Wir nutzen der Einfachheit halber die erste Zeile (y=0) und die ersten X Spalten (x)
for i in range(len(bits)):
    current_value = data[0, i, 0] # Zeile 0, Spalte i, Kanal 0 (Rot)
    
    # Bit-Manipulation: Das LSB auf 0 setzen, dann das gewünschte Bit addieren
    # Hier muss der Student kurz über Bitwise-Operatoren nachdenken (& 0xFE)
    new_value = (current_value & 0xFE) | bits[i]
    
    data[0, i, 0] = new_value

# 4. Zurück in ein Bild verwandeln und abspeichern (Wichtig: Als PNG, nicht JPEG!)
stego_img = Image.fromarray(data)
stego_img.save("stego.png")