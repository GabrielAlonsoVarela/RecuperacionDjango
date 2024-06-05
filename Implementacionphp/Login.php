<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nickname = $_POST['nickname'];
    $contraseña = $_POST['contraseña'];


    $data = json_encode(array(
        'nickname' => $nickname,
        'contraseña' => $contraseña,
    ));

    $ch = curl_init('http://localhost:8000/login/');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

    $response = curl_exec($ch);
    curl_close($ch);

    $result = json_decode($response, true);
    if ($result) {
        echo 'Login successful';
    } else {
        echo 'Login failed';
    }
}
?>

<form method="post" action="">
    <label for="nickname">Nickname:</label>
    <input type="text" id="nickname" name="nickname" required>
    <label for="contraseña">Contraseña:</label>
    <input type="password" id="contraseña" name="contraseña" required>
    <button type="submit">Login</button>
</form>