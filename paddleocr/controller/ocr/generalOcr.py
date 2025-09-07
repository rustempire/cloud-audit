from common.ocr.ocr import OCRPredict
from controller.ocr.utils import get_table_content

OCR = OCRPredict(use_angle_cls=True)


def generalOcr(filepath):
    ocr_text = OCR.ocr(filepath, rec=True, det=True, cls=False)
    result = get_table_content(ocr_text)
    return list(result.keys())
