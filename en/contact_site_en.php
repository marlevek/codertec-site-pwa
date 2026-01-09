<?php
require '../PHPMailer/src/PHPMailer.php';
require '../PHPMailer/src/SMTP.php';
require '../PHPMailer/src/Exception.php';

$emailConfig = require '../config/email.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $name    = htmlspecialchars($_POST['name'] ?? '');
    $email   = htmlspecialchars($_POST['email'] ?? '');
    $message = htmlspecialchars($_POST['message'] ?? '');

    $mail = new PHPMailer(true);

    try {
        $mail->CharSet = 'UTF-8';
        $mail->isSMTP();
        $mail->Host       = $emailConfig['host'];
        $mail->SMTPAuth   = true;
        $mail->Username   = $emailConfig['username'];
        $mail->Password   = $emailConfig['password'];
        $mail->SMTPSecure = $emailConfig['encryption']; // ssl
        $mail->Port       = $emailConfig['port'];       // 465

        $mail->setFrom($emailConfig['username'], 'CoderTec');
        $mail->addAddress('marcelo@codertec.com.br');
        $mail->addReplyTo($email);

        $mail->isHTML(true);
        $mail->Subject = 'New Contact from Website - CoderTec';
        $mail->Body = "
            <h2>Website Contact</h2>
            <p><strong>Name:</strong> {$name}</p>
            <p><strong>Email:</strong> {$email}</p>
            <p><strong>Message:</strong><br>{$message}</p>
        ";

        $mail->send();

        header("Location: /en/thank-you.html");
        exit();

    } catch (Exception $e) {
        echo "Error sending message: {$mail->ErrorInfo}";
    }
}
