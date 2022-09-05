#!/usr/bin/env python3

"""Load an image from wikimedia and calculate its average and dominant color.
Display them on colored boxes in the upper left corner.
"""

from urllib.request import urlopen
from PIL import Image, ImageDraw, ImageFont
import numpy as np


# some const
IMG_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/L%C3%A1pices_de_colores_01.jpg/1024px-L%C3%A1pices_de_colores_01.jpg'
TTF_URL = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Regular.ttf?raw=true'
BOX_LEN = 200
BOX_HGH = 50

# open image and convert as RGB numpy array
web_pil_img = Image.open(urlopen(IMG_URL))
web_pil_img = web_pil_img.convert('RGB')
# web_pil_img.thumbnail([1280, 720])
web_arr_img = np.array(web_pil_img)

# compute average color of image
avg_r, avg_g, avg_b = map(round, np.mean(web_arr_img, axis=(0, 1)))
dom_r, dom_g, dom_b = web_pil_img.resize((1, 1), resample=0).getpixel((0, 0))

# format and print RGB color string
avg_col_str = f'#{avg_r:02X}{avg_g:02X}{avg_b:02X}'
dom_col_str = f'#{dom_r:02X}{dom_g:02X}{dom_b:02X}'
print(f'RGB mean is {avg_col_str}')
print(f'RGB dominant is {dom_col_str}')

# load a TTF font and compute txt position
font = ImageFont.truetype(urlopen(TTF_URL), size=20)

# add colors box on top corner of the web image
# mean color box
avg_box_str = f'average {avg_col_str}'
avg_col_pil_img = Image.new('RGB', (BOX_LEN, BOX_HGH), (avg_r, avg_g, avg_b))
font_len, font_hgh = font.getsize(avg_box_str)
txt_pos = ((BOX_LEN-font_len)/2, (BOX_HGH-font_hgh)/2)
ImageDraw.Draw(avg_col_pil_img).text(txt_pos, avg_box_str, font=font, fill=(255, 255, 255))
web_pil_img.paste(avg_col_pil_img)
# dominant color box
dom_box_str = f'dominant {dom_col_str}'
dom_col_pil_img = Image.new('RGB', (BOX_LEN, BOX_HGH), (dom_r, dom_g, dom_b))
font_len, font_hgh = font.getsize(dom_box_str)
txt_pos = ((BOX_LEN-font_len)/2, (BOX_HGH-font_hgh)/2)
ImageDraw.Draw(dom_col_pil_img).text(txt_pos, dom_box_str, font=font, fill=(255, 255, 255))
web_pil_img.paste(dom_col_pil_img, (0, BOX_HGH))

# show-it
web_pil_img.show()
