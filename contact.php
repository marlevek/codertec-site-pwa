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
$sendStage = 'dependencies';
try {
    foreach (['PHPMailer/src/PHPMailer.php', 'PHPMailer/src/SMTP.php', 'PHPMailer/src/Exception.php', 'config/email.php'] as $requiredFile) {
        if (!is_readable(__DIR__ . '/' . $requiredFile)) {
            error_log('[CoderTec contact] Missing or unreadable file: ' . $requiredFile);
            contact_fail(500, 'send', $lang);
        }
    }
    require __DIR__ . '/PHPMailer/src/PHPMailer.php';
    require __DIR__ . '/PHPMailer/src/SMTP.php';
    require __DIR__ . '/PHPMailer/src/Exception.php';
    $sendStage = 'configuration';
    $emailConfig = require __DIR__ . '/config/email.php';
    foreach (['host', 'username', 'password', 'encryption', 'port'] as $configKey) {
        if (!is_array($emailConfig) || !isset($emailConfig[$configKey]) || !is_scalar($emailConfig[$configKey])) {
            error_log('[CoderTec contact] Missing or invalid configuration key: ' . $configKey);
            contact_fail(500, 'send', $lang);
        }
    }
    $sendStage = 'message_setup';
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
    $sendStage = 'smtp_send';
    if (!$mail->send()) throw new RuntimeException('SMTP send returned false');
    $redirects = ['pt'=>'/pt/obrigado.html', 'en'=>'/en/thank-you.html', 'es'=>'/es/gracias.html'];
    header('Location: ' . $redirects[$lang], true, 303);
    exit;
} catch (Throwable $e) {
    // Log only fixed diagnostic labels, never raw exceptions, credentials or message data.
    $reason = 'unclassified';
    foreach (['authenticate'=>'authentication', 'connect'=>'connection', 'certificate'=>'tls_certificate', 'instantiate mail'=>'mail_transport', 'recipient'=>'recipient_rejected', 'data not accepted'=>'message_rejected'] as $fragment => $label) {
        if (stripos($e->getMessage(), $fragment) !== false) {
            $reason = $label;
            break;
        }
    }
    error_log('[CoderTec contact] Send failed; stage=' . $sendStage . '; reason=' . $reason);
    contact_fail(500, 'send', $lang);
}
