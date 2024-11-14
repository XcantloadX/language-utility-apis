<?php
require_once dirname(__FILE__).'/../../../backends/moji.php';
require_once dirname(__FILE__).'/../../common.php';

header('Content-Type: application/json; charset=utf-8');
$__registers = $GLOBALS['__registers'];

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $backend = isset($_GET['backend']) ? $_GET['backend'] : null;
    $word = isset($_GET['word']) ? $_GET['word'] : null;
    $lang = isset($_GET['lang']) ? $_GET['lang'] : 'en';
    $redirect = isset($_GET['redirect']) ? $_GET['redirect'] : false;

    if (!$backend || !$word || !$lang) {
        echo JSONResponse::fail(-1, 'Missing required parameters')->json();
        exit;
    }

    if (!isset($__registers['word_pronounce'][$backend])) {
        echo JSONResponse::fail(-2, 'Backend not found')->json();
        exit;
    }

    $function = $__registers['word_pronounce'][$backend];

    try {
        $result = $function($lang, $word, $_GET);
        echo JSONResponse::success($result)->json();
    } catch (Exception $e) {
        echo JSONResponse::fail(1, $e->getMessage())->json();
    }
} else {
    echo JSONResponse::fail(-3, 'Method not allowed')->json();
}
