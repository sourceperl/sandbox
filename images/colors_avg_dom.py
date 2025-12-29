#!/usr/bin/env python3

"""Load an image from wikimedia and calculate its average and dominant color.
Display them on colored boxes in the upper left corner.
"""

from urllib.request import Request, urlopen

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# some const
IMG_URL = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/L%C3%A1pices_de_colores_01.jpg/1024px-L%C3%A1pices_de_colores_01.jpg'
TTF_URL = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Regular.ttf?raw=true'
BOX_LEN = 200
BOX_HIGHT = 50

# open image and convert as RGB numpy array
web_pil_img = Image.open(urlopen(Request(IMG_URL, headers={'User-Agent': 'MyApp/1.0'})))
web_pil_img = web_pil_img.convert('RGB')
# web_pil_img.thumbnail([1280, 720])
web_arr_img = np.array(web_pil_img)

# compute average color of image
avg_r, avg_g, avg_b = [int(round(x)) for x in np.mean(web_arr_img, axis=(0, 1))]
dom_r, dom_g, dom_b = web_pil_img.resize((1, 1), resample=0).getpixel((0, 0))

# format and print RGB color string
avg_col_str = f'#{avg_r:02X}{avg_g:02X}{avg_b:02X}'
dom_col_str = f'#{dom_r:02X}{dom_g:02X}{dom_b:02X}'
print(f'RGB mean is {avg_col_str}')
print(f'RGB dominant is {dom_col_str}')

# load a TTF font and compute text position
font = ImageFont.truetype(urlopen(TTF_URL), size=20)

# add colors box on top corner of the web image
# create average color box
avg_box_str = f'average {avg_col_str}'
avg_col_pil_img = Image.new('RGB', (BOX_LEN, BOX_HIGHT), (avg_r, avg_g, avg_b))
draw_avg = ImageDraw.Draw(avg_col_pil_img)

# calculate text size using getbbox
bbox_avg = draw_avg.textbbox((0, 0), avg_box_str, font=font)
font_len = bbox_avg[2] - bbox_avg[0]  # Width
font_hgh = bbox_avg[3] - bbox_avg[1]  # Height
txt_pos_avg = ((BOX_LEN - font_len) / 2, (BOX_HIGHT - font_hgh) / 2)
draw_avg.text(txt_pos_avg, avg_box_str, font=font, fill=(255, 255, 255))

# paste average color box
web_pil_img.paste(avg_col_pil_img)

# create dominant color box
dom_box_str = f'dominant {dom_col_str}'
dom_col_pil_img = Image.new('RGB', (BOX_LEN, BOX_HIGHT), (dom_r, dom_g, dom_b))
draw_dom = ImageDraw.Draw(dom_col_pil_img)

# calculate text size using getbbox
bbox_dom = draw_dom.textbbox((0, 0), dom_box_str, font=font)
font_len_dom = bbox_dom[2] - bbox_dom[0]  # Width
font_hgh_dom = bbox_dom[3] - bbox_dom[1]  # Height
txt_pos_dom = ((BOX_LEN - font_len_dom) / 2, (BOX_HIGHT - font_hgh_dom) / 2)
draw_dom.text(txt_pos_dom, dom_box_str, font=font, fill=(255, 255, 255))

# paste dominant color box
web_pil_img.paste(dom_col_pil_img, (0, BOX_HIGHT))

# show-it
web_pil_img.show()
