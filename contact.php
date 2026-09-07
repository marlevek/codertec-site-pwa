<?php
use PHPMailer\PHPMailer\PHPMailer;
require_once __DIR__ . '/contact-protection.php';
$lang = $contactLanguage ?? (is_string($_POST['lang'] ?? null) && in_array($_POST['lang'], ['pt','en','es'], true) ? $_POST['lang'] : 'pt');
$fields = $contactFields ?? ['nome'=>'nome', 'email'=>'email', 'mensagem'=>'mensagem'];
header('Cache-Control: no-store');
function contact_fail($status, $key, $lang) {
    http_response_code($status);
    header('Content-Type: text/plain; charset=UTF-8');
    exit(contact_error($key, $lang));
}
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    contact_fail(405, 'method', $lang);
}
$data = contact_validate($_POST, $fields);
if (isset($data['error'])) contact_fail($data['error'] === 'spam' ? 422 : 400, $data['error'], $lang);
try {
    $retry = contact_rate_limit(contact_storage_dir(), $_SERVER['REMOTE_ADDR'] ?? '');
} catch (Throwable $e) {
    contact_fail(503, 'storage', $lang);
}
if ($retry) {
    header('Retry-After: ' . $retry);
    contact_fail(429, 'limit', $lang);
}
// All checks complete before loading SMTP or credentials.
try {
    require __DIR__ . '/PHPMailer/src/PHPMailer.php';
    require __DIR__ . '/PHPMailer/src/SMTP.php';
    require __DIR__ . '/PHPMailer/src/Exception.php';
    $emailConfig = require __DIR__ . '/config/email.php';
    $nome = $data['nome'];
    $email = $data['email'];
    $mail = new PHPMailer(true);
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
    $mail->Body = contact_body($data);
    $mail->send();
    $redirects = ['pt'=>'/pt/obrigado.html', 'en'=>'/en/thank-you.html', 'es'=>'/es/gracias.html'];
    header('Location: ' . $redirects[$lang], true, 303);
    exit;
} catch (Throwable $e) {
    contact_fail(500, 'send', $lang);
}
