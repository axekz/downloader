import os
import requests
from tqdm import tqdm
from . import logger


def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kilobyte

    file_name = local_filename.split(os.path.sep)[-1]
    t = tqdm(total=total_size, unit='B', unit_scale=True, desc=file_name, ncols=100)
    with open(local_filename, 'wb') as f:
        for data in response.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()

    if total_size != 0 and t.n != total_size:
        raise Exception("下载文件大小不匹配")

    return local_filename
