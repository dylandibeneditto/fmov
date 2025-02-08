from PIL import Image, ImageDraw, ImageFont

def draw_text_with_background(text, font_path=None, font_size=20, text_color="white", 
                              bg_color="black", padding=10, output_size=(300, 150)):
    img = Image.new("RGBA", output_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]

    box_width = text_width + 2 * padding
    box_height = text_height + 2 * padding

    img_width, img_height = img.size
    box_x = (img_width - box_width) // 2
    box_y = (img_height - box_height) // 2
    text_x = box_x + padding
    text_y = box_y + padding

    draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], fill=bg_color)

    draw.text((text_x, text_y), text, font=font, fill=text_color)

    return img

img = draw_text_with_background("Hello, PIL!", font_path="./Inter-VariableFont_opsz,wght.ttf", font_size=30, bg_color="blue", text_color="white", padding=15)
img.show()
