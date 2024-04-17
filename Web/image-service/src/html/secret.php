<?php
function isInternal() {
    return $_SERVER['REMOTE_ADDR'] == '127.0.0.1';
}

$admin = base64_decode($_COOKIE['admin']);

if (isInternal()) {
    if ($admin == 'true') {
        echo "Hello admin, here is your flag: " . getenv('GZCTF_FLAG');
    } else {
        echo "Hello guest, you are not admin";
    }
} else {
    echo "You are not internal";
}
