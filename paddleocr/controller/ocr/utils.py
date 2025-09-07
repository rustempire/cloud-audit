import os
import shutil

from configs.ocrConfig import fileType, TEMPORARY_PATH
from common.utils.util import float2int, copy_file, pdf2img_multipage


def get_box_and_txt(coordinate):
    p_x = []
    p_y = []
    for x, y in coordinate:
        p_x.append(x)
        p_y.append(y)
    p_x = sorted(p_x)
    p_y = sorted(p_y)
    point_x = p_x[1] + (p_x[2] - p_x[1]) / 2
    point_y = p_y[1] + (p_y[2] - p_y[1]) / 2
    point = float2int((point_x, point_y))
    return point


def get_table_content(result, ty="g"):
    content_point = {}
    for i, rows in enumerate(result[0]):
        if ty == "g":
            ocr_txt = rows[1][0].replace(" ", "", -1)
        else:
            ocr_txt = rows[1][0].replace(" ", "", -1) + "卍{}".format(i)
        point = get_box_and_txt(rows[0])
        content_point[ocr_txt] = point
    return dict(sorted(content_point.items(), key=lambda x: (x[1][1], x[1][0])))


def get_all_file(file_path, inp):
    shutil.rmtree(inp)
    os.makedirs(inp)

    suffix = file_path.split(".")[-1].lower()

    if suffix in fileType["img"]:
        return copy_file(file_path, inp)
    if suffix == "pdf":
        return copy_file(file_path, inp)


def move_recursion_file(inp, suffix_list):
    for root, dirs, files in os.walk(inp):
        for file in files:
            suffix = file.split(".")[-1].lower()
            if suffix in suffix_list:
                shutil.move(os.path.join(root, file), os.path.join(inp, file))
    file_list = [os.path.join(inp, file) for file in os.listdir(inp)]
    for file in file_list:
        if os.path.isdir(file):
            shutil.rmtree(file)


def get_img_path(file_path):
    suffix = file_path.split(".")[-1].lower()
    if suffix in ["png", "jpg", "jpeg"]:
        return file_path
    if suffix == "pdf":
        return pdf2img_multipage(file_path, TEMPORARY_PATH, "png")

    return None
