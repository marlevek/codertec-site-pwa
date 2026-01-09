<?php
require '../PHPMailer/src/PHPMailer.php';
require '../PHPMailer/src/SMTP.php';
require '../PHPMailer/src/Exception.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = htmlspecialchars($_POST['nombre']);
    $correo = htmlspecialchars($_POST['correo']);
    $mensaje = htmlspecialchars($_POST['mensaje']);

    $mail = new PHPMailer(true);

    try {
        $mail->CharSet = 'UTF-8';
        $mail->isSMTP();
        $mail->Host       = 'mail.codertec.com.br';
        $mail->SMTPAuth   = true;
        $mail->Username   = 'marcelo@codertec.com.br';
        $mail->Password   = '#coder1972';
        $mail->SMTPSecure = 'tls';
        $mail->Port       = 587;

        $mail->setFrom('marcelo@codertec.com.br', 'CoderTec');
        $mail->addAddress('marcelo@codertec.com.br');
        $mail->addReplyTo($correo);

        $mail->isHTML(true);
        $mail->Subject = 'Nuevo Contacto desde el Sitio Web - CoderTec';
        $mail->Body    = "<h2>Contacto vía Website</h2>
                          <p><strong>Nombre:</strong> $nombre</p>
                          <p><strong>Email:</strong> $correo</p>
                          <p><strong>Mensaje:</strong> $mensaje</p>";

        $mail->send();
        header("Location: gracias.html");
        exit();
    } catch (Exception $e) {
        echo "Error al enviar: {$mail->ErrorInfo}";
    }
}
?>
