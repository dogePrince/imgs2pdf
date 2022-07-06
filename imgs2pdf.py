# -*- coding: utf-8 -*-
# @author: dave.yao@outlook.com
# @time:   2022/07/06 12:05 AM

import os
import img2pdf
from PIL import Image
from io import BytesIO
import json
import sys

img_type = ["jpg", "png"]
info_template = {
    "path": None,
    "order": 0,
    "rotation": 0
}
config_file = "config.json"


def gen_imgs_info(base_dir):
    imgs_info = []
    for fname in os.listdir(base_dir):
        ext = fname.split('.')[-1]
        if not fname.endswith(".jpg"):
            continue
        path = os.path.join(base_dir, fname)
        if os.path.isdir(path):
            continue
        img_info = info_template.copy()
        img_info["path"] = path
        imgs_info.append(img_info)

    if len(imgs_info) == 0:
        return 1

    imgs_info.sort(key=lambda x: x["path"])
    with open(os.path.join(base_dir, config_file), 'w') as f:
        f.write(json.dumps(imgs_info))


def imgs_to_pdf(base_dir):
    with open(os.path.join(base_dir, config_file)) as info_file:
        imgs_info = json.loads(info_file.read())

    imgs_order = []
    for img_info in imgs_info:
        img = Image.open(img_info["path"])
        img = img.rotate(img_info["rotation"], expand=True)
        bytes_io = BytesIO()
        img.save(bytes_io, format("png"))
        imgs_order.append((img_info["order"], bytes_io.getvalue()))
    imgs_order.sort(key=lambda x: x[0])
    imgs = list(zip(*imgs_order))[1]

    dir_name = os.path.basename(base_dir)
    output_path = os.path.join(base_dir, f"{dir_name}.pdf")
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(imgs))


if __name__ == '__main__':
    config_path = os.path.join(sys.argv[1], config_file)
    if os.path.exists(config_path):
        imgs_to_pdf(sys.argv[1])
    else:
        exit(gen_imgs_info(sys.argv[1]))
