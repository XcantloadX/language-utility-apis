<?php
class WordNotFoundException extends Exception {
    public function __construct($word, Exception $previous = null) {
        parent::__construct("Word not found: $word", 0, $previous);
    }
}

class UnSupportedLanguageException extends Exception {
    public function __construct($lang, Exception $previous = null) {
        parent::__construct("Unsupported language: $lang", 0, $previous);
    }
}