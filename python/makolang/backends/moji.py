import json
from typing import NamedTuple, Optional

import requests

from .common import UA, HTTPRequest, random_uuid, UpstreamAPIError

UNION_API = "https://api.mojidict.com/parse/functions/union-api"
TTS_API = "https://api.mojidict.com/parse/functions/tts-fetch"

SEARCH_FUNCTION_NAME = "search-all"
SEARCH_QUESTION_FUNCTION_NAME = "mojitest-examV2-searchQuestion-v2"
DECONJUGATE_FUNCTION_NAME = "deconjugateWithKeyWord" # 动词变形还原

class MojiWordSearchResult(NamedTuple):
    target_id: str
    title: str
    summary: str
    """单词概要。"""
    summary_b: Optional[str]
    """
    单词概要。
    
    此字段与 `summary` 的区别在于，当单词为动词时，
    `summary` 用一段、五段、サ变、カ变表示动词类型，
    `summary_b` 用一类、二类、三类表示动词类型。
    """

class MojiWordDefinition(NamedTuple):
    pass

def search(word: str) -> list[MojiWordSearchResult]:
    """
    搜索单词。

    :param word: 单词
    :return: 单词信息
    """
    payload = {
        "functions": [
            {
                "name": SEARCH_FUNCTION_NAME,
                "params": {
                    "text": word,
                    # 106 语法、102 单词、103 未知
                    "types": [102, 106, 103]
                }
            }
        ],
        "_ClientVersion": "js3.4.1",
        "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
        "g_os": "PCWeb",
        "g_ver": "v4.8.9.20241014",
        "_InstallationId": random_uuid(),
    }

    headers = {
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'User-Agent': UA,
        'content-type': 'text/plain'
    }

    response = requests.request(
        "POST",
        UNION_API,
        headers=headers,
        data=json.dumps(payload)
    )
    
    ret = response.json()
    if ret['result']['code'] != 200:
        UpstreamAPIError(ret['code'], None, response.text)
    
    # result.results["search-all"].result.word.searchResult
    results = []
    for result in ret['result']['results']['search-all']['result']['word']['searchResult']:
        results.append(MojiWordSearchResult(
            result['targetId'],
            result['title'],
            result['excerpt'],
            result.get('excerptB', None)
        ))
    return results

def pronounce(target_id: str) -> HTTPRequest:
    """
    获取单词发音。
    
    :param target_id: 单词 ID。由 `search` 函数返回。
    :return: 发音音频 URL
    """
    payload = {
        "tarId": target_id,
        "tarType": 102,
        "voiceId": "f002", # TODO: 查看此字段的含义
        "_ClientVersion": "js3.4.1", 
        "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
        "g_os": "PCWeb",
        "g_ver": "v4.8.9.20241014",
        "_InstallationId": random_uuid()
    }

    headers = {
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'User-Agent': UA,
        'content-type': 'text/plain'
    }
    
    response = requests.request(
        "POST",
        TTS_API,
        headers=headers,
        data=json.dumps(payload)
    )
    ret = response.json()
    if ret['result']['code'] != 200:
        UpstreamAPIError(ret['code'], None, response.text)

    return HTTPRequest(
        method="GET",
        url=ret['result']['result']['url'],
        headers={
            "User-Agent": UA,
        },
        payload=None
    )


__exports = [
    MojiWordSearchResult,
    MojiWordDefinition,
    search,
    pronounce
]

if __name__ == "__main__":
    from pprint import pprint as print
    from makolang.utility import play_sound
    results = (search("見る"))
    result = results[0]
    tts = pronounce(result.target_id)
    print(tts)
    # tts.save("pronounce.mp3")
    play_sound(tts)