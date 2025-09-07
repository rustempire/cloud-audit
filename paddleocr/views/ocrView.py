import os
from uuid import uuid1, uuid5

import pandas as pd
from common.utils.util import (
    allowed_file,
    get_upload_file,
    pdf2img_multipage,
    write_txt,
)
from configs.ocrConfig import (
    ALLOWED_EXTENSIONS,
    INVOICE_COLUMNS,
    OUTPUT_PATH,
    TEMPORARY_PATH,
)
from controller.ocr.generalOcr import generalOcr
from controller.ocr.invoiceOcr import invoiceOcr
from controller.ocr.utils import get_img_path


def generalView(file_list):
    results = []
    rand = uuid5(namespace=uuid1(), name="".join(file_list))
    txt_name = "RecognitionInfo_{}.txt".format(rand).replace("-", "")
    txt_path = os.path.join(OUTPUT_PATH, txt_name)
    file_list, zip_path_list = get_upload_file(file_list, TEMPORARY_PATH)
    pdf_list = []
    errorMes = []
    for file in file_list:
        if not allowed_file(file, ALLOWED_EXTENSIONS):
            print("ERROR:通用识别\nfile:{}\nerror:{}".format(file, "文件格式不符"))
            errorMes.append("{}:{}".format(os.path.basename(file), "文件格式不符"))
            continue
        if file[-3:].lower() == "pdf":
            pdf_img_dir = pdf2img_multipage(file, TEMPORARY_PATH)
            for i in sorted(os.listdir(pdf_img_dir)):
                pdf2png_path = os.path.join(pdf_img_dir, i)
                pdf_list.append(pdf2png_path)
                file_list.append(pdf2png_path)
            continue
        try:
            result = generalOcr(file)
        except Exception as e:
            print("ERROR:通用识别\nfile:{}\nerror:{}".format(file, e))
            errorMes.append("{}:{}".format(os.path.basename(file), "通用识别异常"))
            continue

        if file in pdf_list:
            file = file.replace("png", "pdf")
        filename = os.path.basename(file)
        write_txt(txt_path, result, mode="a", filename=filename)
        results.append({"filename": filename, "data": result})
    return results, txt_name, errorMes, zip_path_list


def invoiceView(file_list):
    results = []
    errorMes = []
    rand = uuid5(namespace=uuid1(), name="".join(file_list))
    save_name = "checkExcel_{}.xlsx".format(rand).replace("-", "")
    save_path = os.path.join(OUTPUT_PATH, save_name)
    result_df = pd.DataFrame(columns=INVOICE_COLUMNS)
    file_list, zip_path_list = get_upload_file(file_list, TEMPORARY_PATH)
    pdf_list = []
    for file in file_list:
        if not allowed_file(file, ALLOWED_EXTENSIONS):
            print(
                "ERROR:电子增值税识别\nfile:{}\nerror:{}".format(file, "文件格式不符"),
                flush=True,
            )
            errorMes.append("{}:{}".format(os.path.basename(file), "文件格式不符"))
            continue
        f = get_img_path(file)
        if os.path.isdir(f):
            for i in os.listdir(f):
                pdf2png_path = os.path.join(f, i)
                pdf_list.append(os.path.basename(pdf2png_path))
                file_list.append(pdf2png_path)
            continue
        try:
            result = invoiceOcr(f)
        except Exception as e:
            print("ERROR:电子增值税识别\nfile:{}\nerror:{}".format(f, e), flush=True)
            errorMes.append("{}:{}".format(os.path.basename(f), "电子增值税识别异常"))
            continue
        if result["文件名"] in pdf_list:
            result["文件名"] = result["文件名"].replace("png", "pdf")
        if "error" in result:
            print("INFO: {} {}".format(f, result["error"]), flush=True)
            errorMes.append("{}:{}".format(result["文件名"], result["error"]))
        results.append(result)
        result_df = result_df._append(pd.DataFrame([result]))

    result_df.to_excel(save_path, index=False)
    return results, save_name, errorMes, zip_path_list
