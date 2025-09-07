import os
import math
import shutil
import zipfile
import chardet

import fitz


def float2int(num_list):
    return [math.floor(x) for x in num_list]


def copy_file(src_file, dst_file):
    """
    :param src_file: 具体文件目录全路径
    :param dst_file: 保存文件的上层目录
    :return: 保存的文件目录全路径
    """
    filename = os.path.split(src_file)[-1]
    dst_file = os.path.join(dst_file, filename)
    shutil.copyfile(src_file, dst_file)
    return dst_file


def pdf2img(name, save_path, suffix):
    os.makedirs(save_path, exist_ok=True)
    doc = fitz.open(name)
    dir_name = os.path.splitext(os.path.split(name)[1])[0]
    os.makedirs(save_path, exist_ok=True)
    page = doc[0]
    trans = fitz.Matrix(2.0, 2.0).prerotate(int(0))
    pm = page.get_pixmap(matrix=trans, alpha=False)
    pic_pwd = os.path.join(save_path, "{}.{}".format(dir_name, suffix))
    pm.save(pic_pwd)
    return pic_pwd


def write_txt(path, texts, mode="w", filename=None):
    with open(path, mode=mode, encoding="utf-8") as f:
        if filename:
            f.write(filename + "\n")
        for t in texts:
            if isinstance(t, dict):
                t = str(t)[1:-1]
            f.write(t)
            f.write("\n")


def pdf2img_multipage(name, file_temporary, suffix="png"):
    doc = fitz.open(name)
    pdf_name = os.path.splitext(os.path.split(name)[1])[0]
    pdf_path = os.path.join(file_temporary, pdf_name)
    if os.path.exists(pdf_path):
        shutil.rmtree(pdf_path)
    os.makedirs(pdf_path)
    temp = 0
    for pg in range(doc.page_count):
        page = doc[pg]
        temp += 1
        rotate = int(0)
        zoom_x = 2.0
        zoom_y = 2.0
        trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        page = str(temp)
        if len(page) == 1:
            page = "0{}".format(page)
        pic_name = "{}_{}.{}".format(pdf_name, page, suffix)
        pic_pwd = os.path.join(pdf_path, pic_name)
        pm.save(pic_pwd)
    return pdf_path


def unzip(filepath, unzip_path):
    """
    :param filepath: 待解压的目录
    :param unzip_path: 解压的目录
    :return: 所有解压后的文件目录
    """
    file_path = []
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    unzip_path = os.path.join(unzip_path, f"{base_name}_{os.urandom(4).hex()}")
    zip_file = zipfile.ZipFile(filepath)
    for names in zip_file.namelist():
        if "__MACOSX" in names:
            continue
        if chardet.detect(names.encode("cp437")).get("encoding") == "utf-8":
            name = names.encode("cp437").decode("utf-8")
        else:
            name = names.encode("cp437").decode("gbk")
        zip_file.extract(names, unzip_path)
        file = os.path.join(unzip_path, name.lower())
        os.makedirs(os.path.dirname(file), exist_ok=True)
        os.rename(os.path.join(unzip_path, names), file)
        file_path.append(file)
    zip_file.close()
    return file_path


def get_upload_file(file_list, unzip_path):
    filepath_list = []
    zip_path_list = []
    for filepath in file_list:
        if zipfile.is_zipfile(filepath):
            unzip_list = unzip(filepath, unzip_path)
            filepath_list.extend(unzip_list)
            zip_path_list.append(
                {
                    os.path.basename(filepath): [
                        zp.split(unzip_path)[1] for zp in unzip_list
                    ]
                }
            )
        else:
            filepath_list.append(filepath)
    return filepath_list, zip_path_list


def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def delete_file(file_list):
    if file_list:
        for f in file_list:
            os.remove(f)
