<?php
// Shared by every contact endpoint. No SMTP dependencies here.
function contact_error($key, $lang) {
    $messages = [
        'pt' => ['method'=>'Use POST para enviar o formulário.', 'invalid'=>'Informe nome (1–120 caracteres), e-mail válido (até 254 bytes) e mensagem (1–5000 caracteres), somente como texto.', 'spam'=>'Mensagem bloqueada pela proteção contra spam.', 'limit'=>'Limite de cinco envios em quinze minutos atingido. Tente novamente mais tarde.', 'storage'=>'Formulário temporariamente indispon?vel. Tente novamente mais tarde.', 'send'=>'Não foi possível enviar a mensagem. Tente novamente mais tarde.'],
        'en' => ['method'=>'Use POST to submit the form.', 'invalid'=>'Enter a name (1–120 characters), valid email (up to 254 bytes), and message (1–5000 characters), as text only.', 'spam'=>'Message blocked by spam protection.', 'limit'=>'The limit of five submissions in fifteen minutes has been reached. Please try again later.', 'storage'=>'Form temporarily unavailable. Please try again later.', 'send'=>'Unable to send the message. Please try again later.'],
        'es' => ['method'=>'Utilice POST para enviar el formulario.', 'invalid'=>'Introduzca nombre (1–120 caracteres), correo válido (hasta 254 bytes) y mensaje (1–5000 caracteres), solo como texto.', 'spam'=>'Mensaje bloqueado por la protección contra spam.', 'limit'=>'Se alcanzó el límite de cinco envíos en quince minutos. Inténtelo m?s tarde.', 'storage'=>'Formulario temporalmente no disponible. Inténtelo m?s tarde.', 'send'=>'No se pudo enviar el mensaje. Inténtelo m?s tarde.']
    ];
    return $messages[$lang][$key];
}
function contact_validate($post, $fields) {
    foreach (array_merge(array_values($fields), ['website', 'lang']) as $field) {
        if (isset($post[$field]) && !is_string($post[$field])) return ['error'=>'invalid'];
        if (array_key_exists($field, $post) && $post[$field] === null) return ['error'=>'invalid'];
    }
    if (($post['website'] ?? '') !== '') return ['error'=>'spam'];
    if (isset($post['lang']) && !in_array($post['lang'], ['pt','en','es'], true)) return ['error'=>'invalid'];
    $data = [];
    foreach ($fields as $key => $field) {
        $value = trim($post[$field] ?? '');
        $max = $key === 'nome' ? 120 : ($key === 'email' ? 254 : 5000);
        if ($value === '' || strlen($value) > $max * 4 || !preg_match('//u', $value)
            || preg_match('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/', $value)
            || preg_match_all('/./us', $value) > $max) return ['error'=>'invalid'];
        if ($key !== 'mensagem' && preg_match('/[\r\n]/', $value)) return ['error'=>'invalid'];
        $data[$key] = $value;
    }
    if (strlen($data['email']) > 254 || !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) return ['error'=>'invalid'];
    $text = implode(' ', $data);
    // Exact malicious domain (including subdomains), not unrelated domains containing its name.
    if (preg_match('/(?<![a-z0-9_-])(?:[a-z0-9_-]+\.)*clickto\.cc(?![a-z0-9_-]|\.[a-z0-9_-])/i', $text)
        || preg_match('/your\s+\$25,000\s+promo\s+code\s+is\s+your\s+treasure/i', $text)) return ['error'=>'spam'];
    return $data;
}
function contact_storage_dir() {
    // Optional server environment setting; never read proxy/client headers for this path.
    $configured = getenv('CODERTEC_CONTACT_STORAGE');
    $public = realpath($_SERVER['DOCUMENT_ROOT'] ?? '') ?: __DIR__;
    $dir = $configured ?: dirname($public) . '/.codertec-contact-private';
    if (!is_dir($dir) && !@mkdir($dir, 0700, true) && !is_dir($dir)) throw new RuntimeException('storage');
    $real = realpath($dir);
    foreach ([$public, __DIR__] as $root) {
        $root = rtrim(str_replace('\\', '/', realpath($root)), '/') . '/';
        $candidate = rtrim(str_replace('\\', '/', $real), '/') . '/';
        if (stripos($candidate, $root) === 0) throw new RuntimeException('storage');
    }
    return $real;
}
function contact_rate_limit($dir, $ip, $now = null) {
    if (!filter_var($ip, FILTER_VALIDATE_IP)) throw new RuntimeException('storage');
    $now = $now ?? time();
    $file = @fopen($dir . '/rate-limit.json', 'c+');
    if (!$file) throw new RuntimeException('storage');
    @chmod($dir . '/rate-limit.json', 0600);
    try {
        if (!flock($file, LOCK_EX)) throw new RuntimeException('storage');
        $raw = stream_get_contents($file);
        $records = $raw === '' ? [] : json_decode($raw, true);
        if (!is_array($records)) throw new RuntimeException('storage');
        foreach ($records as $key => $times) {
            if (!is_array($times)) throw new RuntimeException('storage');
            $records[$key] = array_values(array_filter($times, function ($t) use ($now) { return is_int($t) && $t > $now - 900; }));
            if (!$records[$key]) unset($records[$key]);
        }
        $key = hash('sha256', inet_pton($ip));
        $times = $records[$key] ?? [];
        $retry = count($times) >= 5 ? max(1, min($times) + 900 - $now) : 0;
        if (!$retry) { $times[] = $now; $records[$key] = $times; }
        $json = json_encode($records);
        rewind($file);
        if (!ftruncate($file, 0) || fwrite($file, $json) !== strlen($json) || !fflush($file)) throw new RuntimeException('storage');
        return $retry;
    } finally {
        flock($file, LOCK_UN);
        fclose($file);
    }
}
function contact_body($data) {
    $safe = array_map(function ($value) { return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }, $data);
    return '<h2>Contato via Website</h2><p><strong>Nome:</strong> ' . $safe['nome'] . '</p><p><strong>Email:</strong> ' . $safe['email'] . '</p><p><strong>Mensagem:</strong><br>' . nl2br($safe['mensagem']) . '</p>';
}
