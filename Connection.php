#Comprobar la conección con mariaDB
<?php
$con = new mysqli('localhost', 'arletteg', '123456', 'Proyecto_Ganaderia');

if ($con) {
    echo"Conexión exitosa";
} else {
    die(mysqli_error($con));
}
return $con;
?>
