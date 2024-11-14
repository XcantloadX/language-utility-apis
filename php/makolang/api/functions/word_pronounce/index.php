<?php
require_once dirname(__FILE__).'/../../../backends/moji.php';
require_once dirname(__FILE__).'/../../../backends/youdao.php';
require_once dirname(__FILE__).'/../../common.php';

header('Content-Type: application/json; charset=utf-8');
header('Content-Type: application/json');
header('Cache-Control: public, max-age=2592000');
header('Access-Control-Allow-Origin: *');

$__registers = $GLOBALS['__registers'];

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $backendParam = isset($_GET['backend']) ? $_GET['backend'] : null;
    $word = isset($_GET['word']) ? $_GET['word'] : null;
    $lang = isset($_GET['lang']) ? $_GET['lang'] : 'en';
    $redirect = isset($_GET['redirect']) ? $_GET['redirect'] : false;

    if (!$word || !$lang) {
        echo JSONResponse::fail(-1, 'Missing required parameters')->json();
        exit;
    }

    $backends = $backendParam ? explode(',', $backendParam) : array_keys($__registers['word_pronounce']);
    $failMessages = array();
    foreach ($backends as $backend) {
        if (!isset($__registers['word_pronounce'][$backend])) {
            continue;
        }

        $function = $__registers['word_pronounce'][$backend];

        try {
            $result = $function($lang, $word, $_GET);
            $failMessages[$backend] = null;
            if ($redirect) {
                header('HTTP/1.1 301 Moved Permanently'); // 302 可能不会被缓存
                header('Location: '.$result->url);
                exit;
            }
            echo JSONResponse::success([
                'backend' => $backend,
                'lang' => $lang,
                'word' => $word,
                'result' => $result,
                'trials' => $failMessages,
            ])->json();
            exit;
        } catch (Exception $e) {
            $failMessages[$backend] = $e->getMessage();
        }
    }

    echo JSONResponse::fail(-2, 'No backend succeeded', ['trials' => $failMessages])->json();
} else {
    echo JSONResponse::fail(-3, 'Method not allowed')->json();
}
