<?php

require_once 'common.php';

define('UNION_API', 'https://api.mojidict.com/parse/functions/union-api');
define('TTS_API', 'https://api.mojidict.com/parse/functions/tts-fetch');

define('SEARCH_FUNCTION_NAME', 'search-all');
define('SEARCH_QUESTION_FUNCTION_NAME', 'mojitest-examV2-searchQuestion-v2');
define('DECONJUGATE_FUNCTION_NAME', 'deconjugateWithKeyWord'); // 动词变形还原

class MojiWordSearchResult {
    public $target_id;
    public $title;
    public $summary;
    public $summary_b;

    /**
     * MojiWordSearchResult constructor.
     * 
     * @param string $target_id
     * @param string $title
     * @param string $summary
     * @param string|null $summary_b
     */
    public function __construct($target_id, $title, $summary, $summary_b = null) {
        $this->target_id = $target_id;
        $this->title = $title;
        $this->summary = $summary;
        $this->summary_b = $summary_b;
    }
}

class MojiWordDefinition {
    // 定义类
}

/**
 * 搜索单词。
 * 
 * @param string $word 单词
 * @return array 单词信息
 */
function search($word) {
    $payload = array(
        "functions" => array(
            array(
                "name" => SEARCH_FUNCTION_NAME,
                "params" => array(
                    "text" => $word,
                    "types" => array(102, 106, 103)
                )
            )
        ),
        "_ClientVersion" => "js3.4.1",
        "_ApplicationId" => "E62VyFVLMiW7kvbtVq3p",
        "g_os" => "PCWeb",
        "g_ver" => "v4.8.9.20241014",
        "_InstallationId" => random_uuid(),
    );

    $headers = array(
        'pragma: no-cache',
        'priority: u=1, i',
        'User-Agent: ' . UA,
        'content-type: text/plain'
    );

    $options = array(
        'http' => array(
            'method' => 'POST',
            'header' => implode("\r\n", $headers),
            'content' => json_encode($payload)
        )
    );
    $context = stream_context_create($options);
    $response = file_get_contents(UNION_API, false, $context);
    $ret = json_decode($response, true);

    if ($ret['result']['code'] != 200) {
        throw new UpstreamAPIError($ret['code'], null, $response);
    }

    $results = array();
    foreach ($ret['result']['results']['search-all']['result']['word']['searchResult'] as $result) {
        $results[] = new MojiWordSearchResult(
            $result['targetId'],
            $result['title'],
            $result['excerpt'],
            isset($result['excerptB']) ? $result['excerptB'] : null
        );
    }
    return $results;
}

/**
 * 获取单词发音。
 * 
 * @param string $target_id 单词 ID。由 `search` 函数返回。
 * @return HTTPRequest 发音音频 URL
 */
function pronounce($target_id) {
    $payload = array(
        "tarId" => $target_id,
        "tarType" => 102,
        "voiceId" => "f002",
        "_ClientVersion" => "js3.4.1",
        "_ApplicationId" => "E62VyFVLMiW7kvbtVq3p",
        "g_os" => "PCWeb",
        "g_ver" => "v4.8.9.20241014",
        "_InstallationId" => random_uuid()
    );

    $headers = array(
        'pragma: no-cache',
        'priority: u=1, i',
        'User-Agent: ' . UA,
        'content-type: text/plain'
    );

    $options = array(
        'http' => array(
            'method' => 'POST',
            'header' => implode("\r\n", $headers),
            'content' => json_encode($payload)
        )
    );
    $context = stream_context_create($options);
    $response = file_get_contents(TTS_API, false, $context);
    $ret = json_decode($response, true);

    if ($ret['result']['code'] != 200) {
        throw new UpstreamAPIError($ret['code'], null, $response);
    }

    return new HTTPRequest(
        $ret['result']['result']['url'],
        'GET',
        array('User-Agent' => UA),
        null
    );
}

// 导出类和函数
$__exports = array(
    'MojiWordSearchResult',
    'MojiWordDefinition',
    'search',
    'pronounce'
);

if (basename(__FILE__) == basename($_SERVER['SCRIPT_FILENAME'])) {
    $results = search("見る");
    $result = $results[0];
    $tts = pronounce($result->target_id);
    var_dump($tts);
    // $tts->save("pronounce.mp3");
    // play_sound($tts);
}
?>