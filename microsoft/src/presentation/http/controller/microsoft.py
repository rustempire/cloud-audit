import os
import tempfile
from contextlib import asynccontextmanager
from typing import Optional, Tuple

from fastapi import APIRouter, File, Request, UploadFile
from src.application.service.microsoft import (
    extension_allowed,
    get_file_extension,
    get_loader,
)
from src.presentation.http.error import HttpException

router = APIRouter()


async def validate_file_upload(file: Optional[UploadFile]) -> Tuple[bytes, str]:
    """验证上传的文件"""
    if not file:
        raise HttpException(
            status_code=400, error="Bad Request", message="没有上传文件"
        )

    if not file.filename:
        raise HttpException(
            status_code=400, error="Bad Request", message="没有文件名称"
        )

    extension = get_file_extension(file.filename)

    if not extension_allowed(extension):
        raise HttpException(
            status_code=400,
            error="Bad Request",
            message=f"不支持的文件格式: {extension}",
        )

    filebody = await file.read()

    if not filebody:
        raise HttpException(
            status_code=400, error="Bad Request", message="文件没有内容"
        )

    return filebody, extension


async def validate_file_stream(request: Request, filename: str) -> Tuple[bytes, str]:
    """验证文件流"""
    if not filename:
        raise HttpException(
            status_code=400, error="Bad Request", message="没有文件名称"
        )

    extension = get_file_extension(filename)

    if not extension_allowed(extension):
        raise HttpException(
            status_code=400,
            error="Bad Request",
            message=f"不支持的文件格式: {extension}",
        )

    filebody = await request.body()

    if not filebody:
        raise HttpException(
            status_code=400, error="Bad Request", message="文件没有内容"
        )

    return filebody, extension


@asynccontextmanager
async def create_temp_file(filebody: bytes, extension: str):
    """创建临时文件的上下文管理器"""
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
            temp_file.write(filebody)
            temp_file.flush()
            yield temp_file.name
    except Exception as e:
        raise HttpException(
            status_code=500,
            error="Internal Server Error",
            message=f"创建临时文件失败: {str(e)}",
        )
    finally:
        if temp_file and os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
            except Exception:
                pass


async def extract_content(filepath: str, extension: str) -> str:
    """提取文件内容"""

    loader_class = get_loader(extension)

    if not loader_class:
        raise HttpException(
            status_code=400,
            error="Bad Request",
            message=f"不支持的文件格式: {extension}",
        )

    try:
        if extension == ".json":
            loader = loader_class(filepath, jq_schema=".", text_content=False)
        elif extension == ".csv":
            loader = loader_class(filepath, encoding="utf-8")
        else:
            loader = loader_class(filepath)

        documents = loader.load()
        return "".join([doc.page_content for doc in documents])

    except Exception as e:
        raise HttpException(
            status_code=500,
            error="Internal Server Error",
            message=f"文件内容提取失败: {str(e)}",
        )


@router.post("/microsoft/extract/fileupload")
async def extract_from_fileupload(file: Optional[UploadFile] = File(None)):
    """接收上传的文件并提取内容"""
    file_body, extension = await validate_file_upload(file)

    async with create_temp_file(file_body, extension) as temp_file_path:
        try:
            content = await extract_content(temp_file_path, extension)

            return {
                "code": 200,
                "error": "",
                "message": "读取文件成功",
                "data": content,
            }

        except HttpException:
            raise
        except Exception as e:
            raise HttpException(
                status_code=500,
                error="Internal Server Error",
                message=f"文件处理失败: {str(e)}",
            )


@router.post("/microsoft/extract/filestream")
async def extract_from_filestream(request: Request, filename: str):
    """接收文件流并提取内容"""
    file_body, extension = await validate_file_stream(request, filename)

    async with create_temp_file(file_body, extension) as temp_file_path:
        try:
            content = await extract_content(temp_file_path, extension)

            return {
                "code": 200,
                "error": "",
                "message": "读取文件成功",
                "data": content,
            }

        except HttpException:
            raise
        except Exception as e:
            raise HttpException(
                status_code=500,
                error="Internal Server Error",
                message=f"文件处理失败: {str(e)}",
            )
