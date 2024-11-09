<?php
require_once dirname(__FILE__).'/../../../backends/moji.php';

header('Content-Type: application/json');
header('Cache-Control: public, max-age=2592000');
header('Access-Control-Allow-Origin: *');

$action = isset($_GET['action']) ? $_GET['action'] : null;

if ($action === 'search') {
    $word = isset($_GET['word']) ? $_GET['word'] : null;
    if ($word) {
        try {
            $results = search($word);
            echo json_encode(array('status' => 'success', 'data' => $results));
        } catch (Exception $e) {
            echo json_encode(array('status' => 'error', 'message' => $e->getMessage()));
        }
    } else {
        echo json_encode(array('status' => 'error', 'message' => 'Missing parameter: word'));
    }
} elseif ($action === 'pronounce') {
    // TODO: 加入一个 API 可以直接请求发音，不需要先查词获得单词 ID 再请求发音
    $target_id = isset($_GET['target_id']) ? $_GET['target_id'] : null;
    $redirect = isset($_GET['redirect']) ? $_GET['redirect'] : null;
    if ($target_id) {
        try {
            $request = pronounce($target_id);
            if ($redirect) {
                header('Location: '.$request->url);
                exit;
            }
            echo json_encode(array('status' => 'success', 'data' => $request));
        } catch (Exception $e) {
            echo json_encode(array('status' => 'error', 'message' => $e->getMessage()));
        }
    } else {
        echo json_encode(array('status' => 'error', 'message' => 'Missing parameter: target_id'));
    }
} 
elseif ($action === 'pronounce_ex') {
    $kanji = isset($_GET['kanji']) ? $_GET['kanji'] : null;
    $katakana = isset($_GET['katakana']) ? $_GET['katakana'] : null;
    $redirect = isset($_GET['redirect']) ? $_GET['redirect'] : null;
    $allow_fallback = isset($_GET['allow_fallback']) ? $_GET['allow_fallback'] : null;
    // TODO: 允许$katakana可选
    // search($kanji) -> 找到第一个发音为 $katakana 的单词 -> pronounce($target_id)
    if ($kanji && $katakana) {
        try {
            $results = search($kanji);
            $target_id = null;
            foreach ($results as $result) {
                // 勉強 | べんきょう ⓪
                // $kanji | $katakana $tone
                $title = $result->title;
                $parts = explode('|', $title);
                // var_dump($parts);
                if (count($parts) == 2) {
                    $reading_part = trim($parts[1]);
                    $reading = trim(explode(' ', $reading_part)[0]);
                    // var_dump($reading);
                    if ($reading === $katakana) {
                        $target_id = $result->target_id;
                        break;
                    }
                }
            }
            if (!$target_id && $allow_fallback) {
                $target_id = $results[0]->target_id;
            }
            if ($target_id) {
                $request = pronounce($target_id);
                if ($redirect) {
                    header('Location: '.$request->url);
                    exit;
                }
                echo json_encode(array('status' => 'success', 'data' => $request));
            } else {
                echo json_encode(array('status' => 'error', 'message' => 'No matching word found'));
            }
        } catch (Exception $e) {
            echo json_encode(array('status' => 'error', 'message' => $e->getMessage()));
        }
    } else {
        echo json_encode(array('status' => 'error', 'message' => 'Missing parameter: kanji or katakana'));
    }
}
else {
    echo json_encode(array('status' => 'error', 'message' => 'Invalid action'));
}

?>