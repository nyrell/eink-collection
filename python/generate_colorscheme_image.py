from PIL import Image, ImageDraw, ImageFont
import math

# List of colors (combine grayscale and 216 colors, remove duplicates)
grayscale = [
    "#000000", "#111111", "#222222", "#333333", "#444444", "#555555",
    "#666666", "#777777", "#888888", "#999999", "#AAAAAA", "#BBBBBB",
    "#CCCCCC", "#DDDDDD", "#EEEEEE", "#FFFFFF"
]

values = ['00', '33', '66', '99', 'CC', 'FF']
colors_216 = [f"#{r}{g}{b}" for r in values for g in values for b in values]

all_colors = list(set(grayscale + colors_216))
all_colors.sort()

# Settings

img_width=1920
img_height=1080
cols = 16
rows = math.ceil(len(all_colors) / cols)
rect_width = math.ceil(img_width / cols)
rect_height = math.ceil(img_height / rows)
# img_width = cols * rect_width
# img_height = rows * rect_height

img = Image.new('RGB', (img_width, img_height), color='white')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("arial.ttf", 20)  # Adjust path and size as needed

for i, color in enumerate(all_colors):
    x = (i % cols) * rect_width
    y = (i // cols) * rect_height
    draw.rectangle((x, y, x + rect_width, y + rect_height), fill=color)
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    text_color = 'black' if (r*0.299 + g*0.587 + b*0.114) > 186 else 'lightgray'
    draw.text((x + 10, y + 10), color.upper(), fill=text_color, font=font)

img.save('colorscheme.png')
