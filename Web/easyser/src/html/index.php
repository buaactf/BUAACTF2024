<?php
highlight_file(__FILE__);

class Alice {
    public $name;
    public $age;
    function __construct($name, $age) {
        $this->name = $name;
        $this->age = $age;
    }

    function __wakeup() {
        $this->name = "Alice";
        $this->age = 18;
    }

    function __destruct() {
        echo "Bye, {$this->name}!\n";
    }
}

class Blob {
    public $data = "Hello, world!";
    public $alice;
    function __construct($data) {
        $this->data = $data;
        $this->alice = new Alice("Alice", 18);
    }

    function __toString() {
        return $this->alice->data;
    }

    function __destruct() {
        echo "Bye, Blob!\n";
    }
}

class User {
    public $file;

    function __construct($file) {
        $this->file = $file;
    }

    function __get($name) {
        include $this->file;
    }

    function __destruct() {
        echo "Bye, User!\n";
    }
}

if (isset($_POST["your_answer"])) {
    $answer = base64_decode($_POST["your_answer"]);
    unserialize($answer);
}