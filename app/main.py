import signal
import sys
import os
import time

import requests
from tabulate import tabulate
from datetime import datetime
from loguru import logger

from core.api import DOMAIN, get_token, list_dir, get_base_path
from core.download import download_file
from core.decompress import extract_7z_file
from core.config import load_config, save_config, prompt_for_csgo_dir
from core.detect import detect_csgo_path

logger.remove()  # Remove the default logger
logger.add(sys.stderr, format="{time:HH:mm:ss} | {level} | {message}", colorize=True, level="INFO")

def format_size(size):
    """格式化文件大小，根据大小自动使用MB或GB"""
    if size >= 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"
    else:
        return f"{size / (1024 * 1024):.2f} MB"

def format_datetime(dt_str):
    """格式化日期时间字符串"""
    dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    return f"{dt.year}年{dt.month}月{dt.day}日 {dt.hour:02d}:{dt.minute:02d}"

def display_menu(file_info):
    headers = ["编号", "文件名", "大小", "修改日期"]
    table = []
    for i, info in enumerate(file_info):
        file_name = info['name'].rsplit('.', 1)[0]
        size = format_size(info['size'])
        modified = format_datetime(info['modified'])
        table.append([i + 1, file_name, size, modified])
    logger.info("\n" + tabulate(table, headers=headers, tablefmt="grid"))
    time.sleep(0.02)

def signal_handler(sig, frame):
    logger.info('\n退出')
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    logger.info("加载配置文件...")
    config = load_config()

    if not config or "csgo_dir" not in config:
        logger.info("检测CSGO路径...")
        csgo_path = detect_csgo_path()
        if csgo_path:
            csgo_dir = os.path.dirname(csgo_path)
            config = {"csgo_dir": csgo_dir}
            save_config(config)
        else:
            config = prompt_for_csgo_dir()

    csgo_dir = config['csgo_dir']

    logger.info("获取资源列表...")
    token = get_token()
    if not token:
        return

    base_path = get_base_path(token)
    if not base_path:
        return

    dir_list = list_dir(token)
    if dir_list['code'] != 200:
        logger.error("获取目录列表失败")
        return

    file_info = dir_list['data']['content']
    urls = [f"https://{DOMAIN}/d{base_path}/资源包/{item['name']}" for item in file_info]

    while True:
        display_menu(file_info)
        choice = input("请选择 (输入编号以选择资源，输入 'q' 退出程序，选择多个用空格隔开): ")

        if choice.lower() == 'q':
            logger.info("程序已退出。")
            break

        selected_urls = []
        try:
            indices = list(map(int, choice.split()))
            for index in indices:
                if 1 <= index <= len(urls):
                    selected_urls.append(urls[index - 1])
                else:
                    logger.error(f"无效的选项: {index}")
        except ValueError:
            logger.error("请输入有效的数字。")
            continue

        for url in selected_urls:
            file_name = url.split('/')[-1]
            logger.info(f"正在下载 {file_name}")
            try:
                file_path = download_file(url, csgo_dir)
                logger.info(f"下载完成 {file_name}")
                extract_7z_file(file_path, csgo_dir)
                logger.info(f"提取完成 {file_name}")
            except requests.exceptions.RequestException as e:
                logger.error(f"下载失败 {url}: {e}")
            except Exception as e:
                logger.error(f"发生错误: {e}")


if __name__ == "__main__":
    main()
