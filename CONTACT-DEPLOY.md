# Proteção do formulário de contato

## Arquivos para enviar à hospedagem

- contact.php
- contact-protection.php (novo, obrigatório)
- en/contact_site_en.php
- es/contacto_site_es.php
- pt/index.html
- en/index.html
- es/index.html
- service-worker.js

Envie os oito arquivos juntos, preservando suas pastas. Não é necessário enviar tests/ ou este documento. Não altere config/email.php nem as credenciais. A hospedagem deve manter o PHPMailer existente.

## Armazenamento privado

Por padrão, o PHP cria `.codertec-contact-private` no diretório pai de DOCUMENT_ROOT, com permissões 0700 e arquivo 0600. O usuário do PHP precisa poder criar/escrever nessa pasta. Ela não pode ser publicada por outro site, alias ou link simbólico do servidor.

Se a hospedagem restringir essa localização (permissões ou open_basedir), crie uma pasta privada acessível ao PHP fora de qualquer raiz pública e configure a variável de ambiente do servidor `CODERTEC_CONTACT_STORAGE` com seu caminho absoluto. Não coloque o armazenamento dentro de public_html/www. Uma configuração inacessível ou pública retorna HTTP 503 e não envia e-mail.

O limite é compartilhado pelos três endpoints: cinco submissões que passam pela validação por IP em uma janela móvel de 900 segundos. Uma tentativa que falhe no SMTP também consome uma posição. Rejeições na validação não consomem posições. Os registros expirados de todos os IPs são limpos em cada acesso ao limitador, sob LOCK_EX; o arquivo não deve ser removido por uma rotina externa enquanto estiver em uso. Somente REMOTE_ADDR é utilizado; X-Forwarded-For e demais cabeçalhos de proxy são ignorados. Em múltiplos servidores PHP, o armazenamento deve ser compartilhado com suporte adequado a flock.

## Validação e respostas

Nome: 1–120 caracteres; mensagem: 1–5000 caracteres; e-mail válido: até 254 bytes. Exige texto UTF-8, rejeita arrays e caracteres de controle. O honeypot website deve estar vazio. Bloqueia clickto.cc e seus subdomínios e a frase específica recebida, sem proibir links ou a palavra promoção em geral. Campos antigos em inglês e espanhol mantêm seus nomes originais.

HTTP: 400 dados inválidos; 422 spam; 405 método incorreto; 429 limite (com Retry-After); 503 armazenamento indisponível; 500 falha no envio; 303 sucesso. Respostas não são armazenadas em cache. Redirecionamento português: /pt/obrigado.html.

## Testes locais, sem envio real

Execute `python tests/contact_integration.py` com PHP disponível no PATH. O teste cria uma cópia temporária com PHPMailer falso e configuração fictícia, sem conexão SMTP e sem ler as credenciais reais. Verifica dados legítimos, escape HTML, spam, honeypot, e-mail inválido, obrigatoriedade, tamanho, arrays, idiomas, endpoints antigos, códigos HTTP, redirecionamento, limite compartilhado, expiração, limpeza, concorrência e recusa de armazenamento público.

Valide também `php -l` nos quatro arquivos PHP e `node --check service-worker.js`.

A cópia local não contém PHPMailer/src: a entrega real por SMTP não foi testada. Nenhum e-mail real foi enviado e nenhuma publicação foi feita.
