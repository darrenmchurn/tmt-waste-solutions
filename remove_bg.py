"""
Remove the navy background from the TMT logo PNG using flood-fill from
the image corners. Only pixels *connected* to the edge background are
removed — interior navy outlines on the letters are left intact.
"""
from PIL import Image
import math
from collections import deque

INPUT     = r"C:\Users\dchur\Downloads\C4DA6F4A-F800-49F7-9BF7-97DEF6F6D9B1.PNG"
OUTPUT    = r"C:\tmtwebsite\assets\images\tmt-logo-nobg.png"
TOLERANCE = 60   # Euclidean RGB distance — background pixels within this
                 # distance of the seed colour are considered background

img = Image.open(INPUT).convert("RGBA")
pixels = img.load()
w, h = img.size

def color_dist(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1[:3], c2[:3])))

# Seed colour: sample the top-left corner pixel
seed_color = pixels[0, 0][:3]
print(f"Seed colour: rgb{seed_color}")

# BFS flood-fill from all four corners
visited = [[False] * h for _ in range(w)]
queue = deque()

corner_seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
for sx, sy in corner_seeds:
    if not visited[sx][sy]:
        if color_dist(pixels[sx, sy], seed_color) < TOLERANCE:
            queue.append((sx, sy))
            visited[sx][sy] = True

removed = 0
while queue:
    x, y = queue.popleft()
    r, g, b, a = pixels[x, y]
    pixels[x, y] = (r, g, b, 0)   # make transparent
    removed += 1

    for nx, ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
        if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny]:
            nr, ng, nb, na = pixels[nx, ny]
            if color_dist((nr, ng, nb), seed_color) < TOLERANCE:
                visited[nx][ny] = True
                queue.append((nx, ny))

print(f"Made {removed} pixels transparent ({removed/(w*h)*100:.1f}% of image).")
img.save(OUTPUT)
print(f"Saved: {OUTPUT}")
