<?php
require 'PHPMailer/src/PHPMailer.php';
require 'PHPMailer/src/SMTP.php';
require 'PHPMailer/src/Exception.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nome = htmlspecialchars($_POST['nome']);
    $email = htmlspecialchars($_POST['email']);
    $mensagem = htmlspecialchars($_POST['mensagem']);


    $mail = new PHPMailer(true);


    try {
        $mail->CharSet = 'UTF-8';
        $mail->isSMTP();
        $mail->Host       = 'mail.codertec.com.br'; // HostGator
        $mail->SMTPAuth   = true;
        $mail->Username   = 'marcelo@codertec.com.br';
        $mail->Password   = '#coder1972';  // coloque entre aspas
        $mail->SMTPSecure = 'tsl';
        $mail->Port       = 587;

        $mail->setFrom('marcelo@codertec.com.br', 'CoderTec');
        $mail->addAddress('marcelo@codertec.com.br');
        $mail->addReplyTo($email);

        $mail->isHTML(true);
        $mail->Subject = 'Novo Contato pelo Site - CoderTec';
        $mail->Body    = "<h2>Contato via Website</h2>
                          <p><strong>Nome:</strong> $nome</p>
                          <p><strong>Email:</strong> $email</p>
                          <p><strong>Mensagem:</strong> $mensagem</p>";

        $mail->send();
        header("Location: obrigado.html");
        exit();
    } catch (Exception $e) {
        echo "Erro ao enviar: {$mail->ErrorInfo}";
    }
}














































