import json
from copy import copy
from hashlib import md5
from urllib.parse import urlencode
import time

from .common import HTTPRequest

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
KEY = "qCG2vdP92hOXDcKa"

def _calc_sign(queries: dict[str, str], key: str):
    queries = copy(queries)
    queries = { k: v for k, v in queries.items() if v != '' }
    names = sorted(queries.keys()) + ["key"]
    queries['key'] = key
    
    params = map(
        lambda x: f"{x}={queries[x]}",
        names
    )

    params = '&'.join(params)
    sign = md5(params.encode()).hexdigest()
    point_param = ','.join(names)
    return (sign, point_param)

def pronounce(language: str, word: str) -> HTTPRequest:
    """
    获取单词发音。
    
    :param word: 单词
    :param language: 语言
    :return: 发音音频 URL
    """
    queries = {
        "product": "webfanyi",
        "appVersion": 1,
        "client": "web",
        "mid": 1,
        "vendor": "web",
        "screen": 1,
        "model": 1,
        "imei": 1,
        "network": "wifi",
        "keyfrom": "webfanyi",
        "keyid": "voiceFanyiWeb",
        "mysticTime": int(time.time() * 1000), # ===> 时间戳
        "yduuid": "abcdefg",
        "le": language, # ===> 语言
        "phonetic": "",
        "rate": 4, # 未知
        "word": word, # ===> 单词
        "type": "1",
        "id": "",
    }

    sign, point_param = _calc_sign(queries, KEY)
    queries["sign"] = sign
    queries["pointParam"] = point_param

    payload = {}
    headers = {
        "Pragma": "no-cache",
        "Range": "bytes=0-",
        "User-Agent": UA,
    }

    url = "https://dict.youdao.com/pronounce/base?" + urlencode(queries)
    
    return HTTPRequest(url, "GET", headers, payload)
