import os

UPLOAD_PATH = "/workspace/upload/ocr"
IMAGE_TYPE = ["png", "jpg", "jpeg"]

fileType = {"img": IMAGE_TYPE, "pdf": ["pdf"], "zip": ["zip"]}

ALLOWED_EXTENSIONS = [t for types in fileType.values() for t in types]

OCR_MODEL = "/workspace/model/ocr/model_ocr"

# 文件保存目录
INPUT_PATH = "/workspace/data/input"
# 异常文件目录
ERROR_PATH = "/workspace/data/error"
# 文件输出目录
OUTPUT_PATH = "/workspace/data/output/ocr"
# 临时文件目录
TEMPORARY_PATH = "/workspace/data/temporary"


os.makedirs(UPLOAD_PATH, exist_ok=True)
os.makedirs(INPUT_PATH, exist_ok=True)
os.makedirs(ERROR_PATH, exist_ok=True)
os.makedirs(OUTPUT_PATH, exist_ok=True)
os.makedirs(TEMPORARY_PATH, exist_ok=True)

INVOICE_COLUMNS = [
    "文件名",
    "发票名称",
    "发票代码",
    "发票号码",
    "开票日期",
    "校验码",
    "购买方名称",
    "购买方纳税人识别号",
    "购买方地址、电话",
    "购买方开户行及账号",
    "货物或应税劳务、服务名称",
    "规格型号",
    "单位",
    "数量",
    "单价",
    "金额",
    "税率",
    "税额",
    "合计金额",
    "合计税额",
    "价税合计",
    "销售方名称",
    "销售方纳税人识别号",
    "销售方地址、电话",
    "销售方开户行及账号",
]
