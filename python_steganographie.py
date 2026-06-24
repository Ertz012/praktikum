from PIL import Image
text = "Hallo"
binary = " ".join(format(ord(char), "b") for char in text)
img = Image.open("HobbyTown_USA_Oshkosh_interior_under_construction_2002.png")
pixel_colour = img.getpixel((0, 0))
print(binary)
print(img)
print(format(pixel_colour[0], "b"))