import os
from typing import Callable, List

from common.utils.util import allowed_file, delete_file
from configs.ocrConfig import ALLOWED_EXTENSIONS, OUTPUT_PATH, UPLOAD_PATH
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from views.ocrView import generalView, invoiceView

router = APIRouter()


async def handle_upload(files: List[UploadFile]) -> List[str]:
    filelist = []
    for file in files:
        if allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = os.path.join(UPLOAD_PATH, file.filename)
            with open(filename, "wb") as buffer:
                buffer.write(await file.read())
            filelist.append(filename)
        else:
            delete_file(filelist)
            raise HTTPException(
                status_code=422,
                detail=f"文件格式不符合要求，只允许上传 {ALLOWED_EXTENSIONS} 格式文件",
            )

    return filelist


def create_endpoint(func: Callable):
    async def endpoint(file: List[UploadFile] = File(...)):
        try:
            check_data, download, _, zip_file = func(await handle_upload(file))
            return {
                "status": 200,
                "data": {
                    "checkData": check_data,
                    "download": download,
                    "zip_file": zip_file,
                },
            }
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})

    return endpoint


@router.get("/ocr/download/{filename}")
async def download(filename: str):
    filepath = os.path.join(OUTPUT_PATH, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="文件未找到")

    return FileResponse(
        filepath, filename=filename, media_type="application/octet-stream"
    )


router.post("/ocr/general")(create_endpoint(generalView))
router.post("/ocr/invoice")(create_endpoint(invoiceView))
