import http.client
import json
from . import logger

DOMAIN = 'dl.axekz.com'


def get_token():
    conn = http.client.HTTPSConnection(DOMAIN)
    payload = json.dumps({
        "username": "downloader",
        "password": "12345678"
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/auth/login", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    if data['code'] == 200:
        return data['data']['token']
    else:
        logger.error("获取token失败")
        return None

def list_dir(token):
    conn = http.client.HTTPSConnection(DOMAIN)
    payload = json.dumps({
        "path": "资源包",
        "password": "",
        "page": 1,
        "per_page": 0,
        "refresh": False
    })
    headers = {
        'Authorization': token,
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/fs/list", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def get_base_path(token):
    conn = http.client.HTTPSConnection(DOMAIN)
    headers = {
        'Authorization': token,
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
    }
    conn.request("GET", "/api/me", '', headers)
    res = conn.getresponse()
    data = res.read()
    user_data = json.loads(data.decode("utf-8"))
    if user_data['code'] == 200:
        return user_data['data']['base_path']
    else:
        logger.error("获取base_path失败")
        return None
