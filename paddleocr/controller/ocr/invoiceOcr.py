import os

import cv2
from common.crop.get_box import invoice_module_box
from common.invoice.get_invoice_info import Invoice
from common.ocr.ocr import OCRPredict
from common.utils.util import copy_file
from configs.ocrConfig import ERROR_PATH
from controller.ocr.utils import get_table_content

OCR = OCRPredict(use_angle_cls=False, lang="ch")


def invoiceOcr(filepath):
    filename = os.path.basename(filepath)
    img = cv2.imread(filepath)
    box_dict, buyer_ap_im, seller_ap_img = invoice_module_box(img)
    if box_dict is None:
        copy_file(filepath, ERROR_PATH)
        return {"文件名": filename, "error": "边界检测失败"}
    result = OCR.ocr(img, cls=False)
    buyer_ap = OCR.ocr(buyer_ap_im, cls=False)
    seller_ap = OCR.ocr(seller_ap_img, cls=False)
    content_point = get_table_content(result, ty="i")
    invoice = Invoice(content_point, box_dict, filename)
    invoice.check_address_and_phone(buyer_ap, seller_ap)
    return invoice.res
