<?php
require_once 'common.php';

function youdao_pronounce($lang, $word) {
    return new HTTPRequest(
        "http://dict.youdao.com/dictvoice?le=$lang&type=3&audio=".urlencode($word),
        'GET',
        array('User-Agent' => UA)
    );
}

register_backend('youdao', 'word_pronounce', function($lang, $word, $params) {
    if ($lang === 'ja')
        $lang = 'jap';
    return youdao_pronounce($lang, $word);
});