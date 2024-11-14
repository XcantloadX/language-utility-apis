<?php
/**
 * Class JSONResponse
 * 
 * 该类表示一个包含状态码、消息和数据的 JSON 响应。
 * 提供将响应转换为数组或 JSON 格式的方法。
 * 
 * @property int $code 响应的状态码。
 * @property string $message 响应的消息。
 * @property mixed $data 响应的数据，可以是对象、数组或任何其他类型。
 */
class JSONResponse {
    private $code;
    private $message;
    private $data;

    /**
     * JSONResponse 构造函数。
     * 
     * @param int $code 响应的状态码。
     * @param string $message 响应的消息。
     * @param mixed $data 响应的数据。
     */
    public function __construct($code, $message, $data) {
        $this->code = $code;
        $this->message = $message;
        $this->data = $this->convertDataToArray($data);
    }

    /**
     * 如果给定数据是具有 toArray 方法的对象，则将其转换为数组，
     * 或者如果是数组，则递归转换元素。
     * 
     * @param mixed $data 要转换的数据。
     * @return mixed 转换后的数据。
     */
    private function convertDataToArray($data) {
        if (is_object($data) && method_exists($data, 'toArray')) {
            return $data->toArray();
        } elseif (is_array($data)) {
            return array_map([$this, 'toDict'], $data);
        }
        return $data;
    }

    /**
     * 创建一个状态码为 0 且消息为 'ok' 的成功 JSONResponse。
     * 
     * @param mixed $data 响应的数据。
     * @return JSONResponse 成功的 JSONResponse。
     */
    public static function success($data) {
        return new self(0, 'ok', $data);
    }

    /**
     * 创建一个具有给定状态码和消息的失败 JSONResponse。
     * 
     * @param int $code 响应的状态码。
     * @param string $message 响应的消息。
     * @return JSONResponse 失败的 JSONResponse。
     */
    public static function fail($code, $message) {
        return new self($code, $message, null);
    }

    /**
     * 将 JSONResponse 转换为数组。
     * 
     * @return array JSONResponse 的数组表示。
     */
    public function toArray() {
        return [
            'code' => $this->code,
            'message' => $this->message,
            'data' => $this->data
        ];
    }

    /**
     * 将 JSONResponse 转换为 JSON 字符串。
     * 
     * @return string JSONResponse 的 JSON 字符串表示。
     */
    public function json() {
        return json_encode($this->toArray());
    }
}
