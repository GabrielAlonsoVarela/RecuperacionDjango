<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre = $_POST['nombre'];
    $apellidos = $_POST['apellidos'];
    $nickname = $_POST['nickname'];
    $contraseña = $_POST['contraseña'];
    $email = $_POST['email'];

    $data = json_encode(array(
        'nickname' => $nickname,
        'nombre' => $nombre,
        'apellidos' => $apellidos,
        'contraseña' => $contraseña,
        'email' => $email,
    ));

    $ch = curl_init('http://localhost:8000/register/');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

    $response = curl_exec($ch);
    curl_close($ch);

    $result = json_decode($response, true);
    if ($result) {
        echo 'Registration successful';
    } else {
        echo 'Registration failed';
    }
}
?>

<form method="post" action="">
    <label for="nickname">Nickname:</label>
    <input type="text" id="nickname" name="nickname" required>
    <label for="nombre">Nombre:</label>
    <input type="text" id="nombre" name="nombre" required>
    <label for="apellidos">Apellidos:</label>
    <input type="text" id="apellidos" name="apellidos" required>
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required>
    <label for="contraseña">Contraseña:</label>
    <input type="password" id="contraseña" name="contraseña" required>
    <button type="submit">Registro</button>
</form>