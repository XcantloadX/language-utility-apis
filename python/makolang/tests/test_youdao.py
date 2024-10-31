import json
import time
import unittest
from test import support

import requests

from makolang.backends import youdao

class YoudaoPronounceTest(unittest.TestCase):

    def test_sign_calc(self):
        case1 = ({"a": "1", "b": "2"}, "key")
        case2 = ({'product': 'webfanyi', 'appVersion': 1, 'client': 'web', 'mid': 1, 'vendor': 'web', 'screen': 1, 'model': 1, 'imei': 1, 'network': 'wifi', 'keyfrom': 'webfanyi', 'keyid': 'voiceFanyiWeb', 'mysticTime': 1730300850404, 'yduuid': 'abcdefg', 'le': 'jp', 'phonetic': '', 'rate': 4, 'word': '千', 'type': '1', 'id': ''}, 'qCG2vdP92hOXDcKa')
        case3 = ({}, '')
        result1 = ('735a0bafc42420a9b223ce31415e043a', 'a,b,key')
        result2 = ('5a200127ec01072461b9683239707db6', 'appVersion,client,imei,keyfrom,keyid,le,mid,model,mysticTime,network,product,rate,screen,type,vendor,word,yduuid,key')
        result3 = ('08e27903afd3b3888f0974f33b255a0f', 'key')
        self.assertEqual(youdao._calc_sign(*case1), result1)
        self.assertEqual(youdao._calc_sign(*case2), result2)
        self.assertEqual(youdao._calc_sign(*case3), result3)
        
    def test_api(self):
        cases = [
            ('en', 'test', 12717),
            ('en', '1234', 35040),
            ('zh', '有道翻译', 19200),
            ('ja', 'こんにちは', 18720),
        ]
        for case in cases:
            lang, word, length = case
            url, _, headers, _ = youdao.pronounce(lang, word)
            res = requests.get(url, headers=headers)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(res.content), length)
            time.sleep(0.2)

if __name__ == '__main__':
    support.run_unittest(YoudaoPronounceTest)