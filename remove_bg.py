"""
Remove the navy background from the TMT logo PNG and save as transparent PNG.
Background colour: approx #0d1b2e — we use a Euclidean distance tolerance
to catch all background shades without clipping into the logo colours.
"""
from PIL import Image
import math

INPUT  = r"C:\Users\dchur\Downloads\C4DA6F4A-F800-49F7-9BF7-97DEF6F6D9B1.PNG"
OUTPUT = r"C:\tmtwebsite\assets\images\tmt-logo-nobg.png"
TOLERANCE = 55          # adjust 40-70 if needed

# Target background colour (navy)
BG = (13, 27, 46)       # #0d1b2e

img = Image.open(INPUT).convert("RGBA")
pixels = img.load()
w, h = img.size

removed = 0
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        dist = math.sqrt((r - BG[0])**2 + (g - BG[1])**2 + (b - BG[2])**2)
        if dist < TOLERANCE:
            pixels[x, y] = (r, g, b, 0)   # fully transparent
            removed += 1

print(f"Made {removed} pixels transparent ({removed/(w*h)*100:.1f}% of image).")
img.save(OUTPUT)
print(f"Saved: {OUTPUT}")
