<!DOCTYPE html>
<style>
    img {
        width: 100%;
        height: 100%;
        object-flit: cover;
    }
</style>
<html>
<head>
    <title>Image Service</title>
</head>
<body>
<?php
function downloadImage($quote) {
    $ch = curl_init($quote->url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Accept: */*",
        "Accept-Encoding: gzip",
        "X-From-Author: ".$quote->author
    ]);
    $image = curl_exec($ch);
    curl_close($ch);
    $encodeImage = base64_encode($image);
    return "data:image/png;base64,{$encodeImage}";
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $json = json_decode(file_get_contents('php://input'));
    if (strtolower(substr($json->url, 0, 7)) != 'http://' && strtolower(substr($json->url, 0, 8)) != 'https://') {
        http_response_code(400);
        echo 'url must start with http or https';
        exit(1);
    }
    $image = downloadImage($json);
    echo "<h2>Here is a random image for you:</h2>";
    echo "<img src='{$image}' />";
}

if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    $tmp = '{"url": "http://localhost/static/1.jpg","author": "admin"}';
    $image = downloadImage(json_decode($tmp));
    echo "<h2>Here is a awesome image for you:</h2>";
    echo "<img src='{$image}' height='50' width='50' /> <!-- /www.zip-->";
}
?>
</body>
</html>
