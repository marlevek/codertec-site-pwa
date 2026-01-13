<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require __DIR__ . '/PHPMailer/src/PHPMailer.php';
require __DIR__ . '/PHPMailer/src/SMTP.php';
require __DIR__ . '/PHPMailer/src/Exception.php';

// Carrega config de email
$emailConfig = require __DIR__ . '/config/email.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit;
}

// Dados do formulário
$nome     = htmlspecialchars($_POST['nome'] ?? '');
$email    = htmlspecialchars($_POST['email'] ?? '');
$mensagem = htmlspecialchars($_POST['mensagem'] ?? '');
$lang     = $_POST['lang'] ?? 'pt';

if (!$email || !$mensagem) {
    http_response_code(400);
    exit('Dados inválidos');
}

$mail = new PHPMailer(true);

try {
    $mail->CharSet = 'UTF-8';
    $mail->isSMTP();
    $mail->Host       = $emailConfig['host'];
    $mail->SMTPAuth   = true;
    $mail->Username   = $emailConfig['username'];
    $mail->Password   = $emailConfig['password'];
    $mail->SMTPSecure = $emailConfig['encryption'];
    $mail->Port       = $emailConfig['port'];

    $mail->setFrom('marcelo@codertec.com.br', 'CoderTec');
    $mail->addAddress('marcelo@codertec.com.br');
    $mail->addReplyTo($email, $nome);

    $mail->isHTML(true);
    $mail->Subject = 'Novo contato pelo site - CoderTec';
    $mail->Body = "
        <h2>Contato via Website</h2>
        <p><strong>Nome:</strong> {$nome}</p>
        <p><strong>Email:</strong> {$email}</p>
        <p><strong>Mensagem:</strong><br>{$mensagem}</p>
    ";

    $mail->send();

    // Redirecionamento por idioma
    switch ($lang) {
        case 'en':
            $redirect = '/en/thank-you.html';
            break;
        case 'es':
            $redirect = '/es/gracias.html';
            break;
        default:
            $redirect = '/obrigado.html';
    }

    header("Location: {$redirect}");
    exit;

} catch (Exception $e) {
    http_response_code(500);
    echo "Erro ao enviar mensagem.";
}
