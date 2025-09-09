from PIL import Image, ImageDraw, ImageFont
import math
import colorsys

# 16 Grayscale colors
grayscale = [
    "#000000", "#111111", "#222222", "#333333", "#444444", "#555555",
    "#666666", "#777777", "#888888", "#999999", "#AAAAAA", "#BBBBBB",
    "#CCCCCC", "#DDDDDD", "#EEEEEE", "#FFFFFF"
]

# Define schemes with fixed 6 hues and varying sat/val levels
schemes = [
    {'name': 'distinct8', 'num_hues': 6, 'num_sat': 1, 'num_val': 2},
    {'name': 'distinct27', 'num_hues': 6, 'num_sat': 2, 'num_val': 3},
    {'name': 'distinct64', 'num_hues': 6, 'num_sat': 3, 'num_val': 4},
    {'name': 'distinct125', 'num_hues': 6, 'num_sat': 4, 'num_val': 5}
]

# Function to generate distinct colors in HSV grid with varying lightness (value)
def generate_distinct_colors(num_hues, num_sat, num_val):
    colors = []
    # Fixed 6 hues for pure colors: red, yellow, green, cyan, blue, magenta
    hues = [i / 6.0 for i in range(6)]  # 0, 1/6, 2/6, 3/6, 4/6, 5/6

    # Saturation levels: ensure max is 1.0
    if num_sat > 1:
        sat_steps = [0.4 + (i / (num_sat - 1)) * 0.6 for i in range(num_sat)]
    else:
        sat_steps = [1.0]  # Full saturation for pure colors

    # Value levels: ensure max is 1.0
    if num_val > 1:
        val_steps = [0.4 + (i / (num_val - 1)) * 0.6 for i in range(num_val)]
    else:
        val_steps = [1.0]

    for h in hues:
        for s in sat_steps:
            for v in val_steps:
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                hex_color = f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}"
                colors.append(hex_color)

    return list(set(colors))  # Remove any duplicates

# Function to generate PNG for a scheme
def generate_png(scheme_name, num_hues, num_sat, num_val):
    colors = generate_distinct_colors(num_hues, num_sat, num_val)
    all_colors = list(set(grayscale + colors))

    # Sort by HSV for gradual hue changes
    def hsv_key(color):
        r, g, b = int(color[1:3], 16)/255, int(color[3:5], 16)/255, int(color[5:7], 16)/255
        return colorsys.rgb_to_hsv(r, g, b)
    all_colors.sort(key=hsv_key)

    n = len(all_colors)

    # Fixed image size
    img_width = 1920
    img_height = 1080

    # Allocate space: bottom row ~10% of height
    bottom_height = img_height // 10
    main_height = img_height - bottom_height

    # Optimal grid for main colors
    aspect = img_width / main_height
    sqrt_n = math.sqrt(n)
    cols = math.ceil(sqrt_n * math.sqrt(aspect))
    rows = math.ceil(n / cols)
    rect_width = img_width // cols
    rect_height = main_height // rows

    img = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(img)

    # Draw main grid with serpentine order for smoother transitions
    font_size = min(20, rect_height // 3)
    font = ImageFont.truetype("arial.ttf", font_size)  # Adjust path

    for i, color in enumerate(all_colors):
        row = i // cols
        col = i % cols
        if row % 2 == 1:  # Reverse direction for odd rows
            col = cols - 1 - col
        x = col * rect_width
        y = row * rect_height
        draw.rectangle((x, y, x + rect_width, y + rect_height), fill=color)
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        luminance = r*0.299 + g*0.587 + b*0.114
        text_color = 'black' if luminance > 186 else 'white'
        text = color.upper()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = x + (rect_width - text_width) // 2
        text_y = y + (rect_height - text_height) // 2
        draw.text((text_x, text_y), text, fill=text_color, font=font)

    # Draw extra grayscale row at bottom
    cols_bottom = 16
    rect_width_bottom = img_width // cols_bottom
    rect_height_bottom = bottom_height
    font_size_bottom = min(20, rect_height_bottom // 3)
    font_bottom = ImageFont.truetype("arial.ttf", font_size_bottom)  # Adjust path

    for i, color in enumerate(grayscale):
        x = i * rect_width_bottom
        y = main_height
        draw.rectangle((x, y, x + rect_width_bottom, y + rect_height_bottom), fill=color)
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        luminance = r*0.299 + g*0.587 + b*0.114
        text_color = 'black' if luminance > 186 else 'white'
        text = color.upper()
        bbox = draw.textbbox((0, 0), text, font=font_bottom)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = x + (rect_width_bottom - text_width) // 2
        text_y = y + (rect_height_bottom - text_height) // 2
        draw.text((text_x, text_y), text, fill=text_color, font=font_bottom)

    img.save(f'{scheme_name}.png')

# Generate PNGs
for scheme in schemes:
    print("Generating PNG for {}".format(scheme['name']))
    generate_png(scheme['name'], scheme['num_hues'], scheme['num_sat'], scheme['num_val'])
