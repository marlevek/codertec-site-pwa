<?php
require_once __DIR__ . '/contact-protection.php';
header('Cache-Control: no-store');
header('Content-Type: application/json; charset=UTF-8');
header('X-Robots-Tag: noindex');
try {
    echo json_encode(['token' => contact_token_issue(contact_secret(contact_storage_dir()))]);
} catch (Throwable $e) {
    http_response_code(503);
    echo json_encode(['error' => 'storage']);
}
