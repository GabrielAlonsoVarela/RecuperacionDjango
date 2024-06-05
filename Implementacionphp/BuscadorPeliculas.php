<?php
    $search = $_POST['search'];
    $limit = $_POST['limit'];
    $page = $_POST['page'];
    
    $baseurl = "http://localhost:8000/peliculas/";

    $parametros = http_build_query(array(
        'search' => $search,
        'page' => $page,
        'limit' => $limit
    ));

    $url = $baseurl . '?' . $parametros;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_URL, $url);

    $response = curl_exec($ch);
    if (curl_errno($ch)) {
        echo 'Error en cURL: ' . curl_error($ch);
    } else {
        $result = json_decode($response, true);
        echo '<h2>Películas encontradas:</h2>';
                echo '<table border="1">';
                echo '<tr>';
                echo '<th>Título</th>';
                echo '<th>Portada</th>';
                echo '<th>Categoria</th>';
                echo '</tr>';

                foreach ($result['peliculas'] as $pelicula) {
                    echo '<tr>';
                    echo '<td>' . htmlspecialchars($pelicula['nombre']) . '</td>';      
                    echo '<td><img style="height:300px; width:200px;" src="' . htmlspecialchars($pelicula['imagen']) . '" /></td>';
                    echo '<td>' . htmlspecialchars($pelicula['categoria']) . '</td>';
                    echo '</tr>';
                }

                echo '</table>';
        }
    curl_close($ch);

    
?>

<form method="post" action="">
    <label for="search">Buscar:</label>
    <input type="text" id="search" name="search" value=''>
    <label for="limit">Limite:</label>
    <input type="number" id="limit" name="limit" value='5'>
    <label for="page">Pagina:</label>
    <input type="number" id="page" name="page" value='1'>
    <button type="submit">Buscar</button>
</form>