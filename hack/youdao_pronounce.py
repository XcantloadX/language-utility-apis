import json
import requests
from copy import copy
from hashlib import md5
from itertools import chain
from urllib.parse import urlencode

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
KEY = "qCG2vdP92hOXDcKa"

def calc_sign(queries: dict[str, str], key: str):
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
    "mysticTime": 1730300850404, # ===> 时间戳
    "yduuid": "abcdefg",
    "le": "jp", # ===> 语言
    "phonetic": "",
    "rate": 4, # 未知
    "word": "千", # ===> 单词
    "type": "1",
    "id": "",
}

sign, point_param = calc_sign(queries, KEY)
queries["sign"] = sign
queries["pointParam"] = point_param

url = "https://dict.youdao.com/pronounce/base?" + urlencode(queries)

payload = {}
headers = {
    "Pragma": "no-cache",
    "Range": "bytes=0-",
    #    'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=279651111.96915686; OUTFOX_SEARCH_USER_ID=-1279201491@111.22.178.112; _ga=GA1.2.1027360333.1705307473; JSESSIONID=abcL6UCFB9Kxx9Yh4hu1y; NTES_SESS=k.imjvBtR6IFNIM_N7NbbgxT_nFc29.w3r6jvJnFbML.ybvYyrnuZzDsrrHClt06z3WbQhYuHCiiV1rEN.zD0qC5t16kNvmn6pOEWztGSzfPbI6gWxOxEdQ1aHhsFsRx_4z_aKpeIMwY2.Htf_P8BOZcEAgO.W0Qat12ksH266desxBhhdaUvM3v_varELW3hUDc_s3tCA18z; S_INFO=1716985346|0|3&80##|xcantloadx; P_INFO=xcantloadx@163.com|1716985346|0|youdaonote|11&99|hun&1714357338&music#hun&null#10#0#0|&0||xcantloadx@163.com; YG_COSPREAD_SESSIONID="3||1716985346274@v2|u0hOsqrxIVUfRHTLnLkERJZhHU5kf6B0z5kL6LRHquRpyPMzWkMpLR6S6LYA6LpFRgzh4kY6LUG0TK0LzYO4Py0YMP4YWkfeZ0"; _uetsid=95bfbad095f611ef9f43d5bd91cb4f8b; _uetvid=95bfe3c095f611efb106addc46ac26c2; DICT_DOCTRANS_SESSION_ID=ZWI2NzcyOTUtNmM5My00MDcxLTlkMWYtYjY2NTRjYmEwOGZj',
    "User-Agent": UA,
}

response = requests.request("GET", url, headers=headers, data=payload)
print(response.status_code)

with open("output.mp3", "wb") as f:
    f.write(response.content)
