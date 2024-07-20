import os
import py7zr
from . import logger


def extract_7z_file(file_path, extract_folder):
    file_name = os.path.basename(file_path)
    logger.info(f"正在提取 {file_name}")

    with py7zr.SevenZipFile(file_path, mode='r') as z:
        z.extractall(path=extract_folder)

    logger.info(f"提取完成 删除 {file_name}")
    os.remove(file_path)
