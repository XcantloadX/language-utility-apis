<?php
require_once dirname(__FILE__).'/cache.class.php';

$cache = new Cache('./.cache');

/**
 * Reads entire file into a string
 * @link https://php.net/manual/en/function.file-get-contents.php
 * @param string $filename <p>
 * Name of the file to read.
 * </p>
 * @param bool $use_include_path [optional] <p>
 * Note: As of PHP 5 the FILE_USE_INCLUDE_PATH constant can be
 * used to trigger include path search.
 * </p>
 * @param resource $context [optional] <p>
 * A valid context resource created with
 * stream_context_create. If you don't need to use a
 * custom context, you can skip this parameter by null.
 * </p>
 * @param int $offset [optional] <p>
 * The offset where the reading starts.
 * </p>
 * @param int|null $length [optional] <p>
 * Maximum length of data read. The default is to read until end
 * of file is reached.
 * </p>
 * @return string|false The function returns the read data or false on failure.
 */
function cached_file_get_contents(
    $filename,
    $use_include_path = false,
    $context = null
) {
    global $cache;
    $request_body = stream_context_get_params($context)['options']['http']['content'];
    $key = 'file_get_contents-' . md5($filename . $request_body);
    if (!$cache->isCached($key)) {
        $data = file_get_contents($filename, $use_include_path, $context);
        $cache->store($key, $data);
    } else {
        $data = $cache->retrieve($key);
    }
    return $data;
}

