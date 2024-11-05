<?php

define('UA', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36');

/**
 * 生成随机 UUID。
 * 
 * @return string UUID
 */
function random_uuid() {
    return sprintf(
        '%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
        mt_rand(0, 0xffff), mt_rand(0, 0xffff),
        mt_rand(0, 0xffff),
        mt_rand(0, 0x0fff) | 0x4000,
        mt_rand(0, 0x3fff) | 0x8000,
        mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff)
    );
}

class HTTPRequest implements \JsonSerializable {
    public $url;
    public $method;
    public $headers;
    public $payload;

    /**
     * HTTPRequest constructor.
     * 
     * @param string $url
     * @param string $method
     * @param array|null $headers
     * @param array|null $payload
     */
    public function __construct($url, $method, $headers = null, $payload = null) {
        $this->url = $url;
        $this->method = $method;
        $this->headers = $headers;
        $this->payload = $payload;
    }

    /**
     * 发送 HTTP 请求。
     * 
     * @return string
     */
    public function request() {
        $options = array(
            'http' => array(
                'method' => $this->method,
                'header' => $this->formatHeaders($this->headers),
                'content' => $this->payload ? json_encode($this->payload) : null,
            )
        );
        $context = stream_context_create($options);
        return file_get_contents($this->url, false, $context);
    }

    /**
     * 保存 HTTP 响应内容到文件。
     * 
     * @param string $path
     */
    public function save($path) {
        file_put_contents($path, $this->request());
    }

    /**
     * 格式化 HTTP 头。
     * 
     * @param array|null $headers
     * @return string
     */
    private function formatHeaders($headers) {
        if (!$headers) {
            return '';
        }
        $formatted = '';
        foreach ($headers as $key => $value) {
            $formatted .= "$key: $value\r\n";
        }
        return $formatted;
    }

    /** @disregard  */
    public function jsonSerialize()
    {
        return get_object_vars($this);
    }
}

class UpstreamAPIError extends Exception {
    public $code;
    public $message;
    public $response;

    /**
     * UpstreamAPIError constructor.
     * 
     * @param string $code
     * @param string|null $message
     * @param string|null $response
     */
    public function __construct($code, $message = null, $response = null) {
        $this->code = $code;
        $this->message = $message;
        $this->response = $response;
        parent::__construct("Upstream API error: $code $message");
    }
}

// 导出类和函数
$__exports = array(
    'HTTPRequest',
    'UpstreamAPIError',
    'random_uuid'
);
?>