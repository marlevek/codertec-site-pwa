"""Offline integration tests: temporary site, fake PHPMailer, no SMTP connection."""
from pathlib import Path
import tempfile, shutil, subprocess, os, socket, time, json, urllib.request, urllib.parse, urllib.error
ROOT = Path(__file__).resolve().parents[1]
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args): return None
with tempfile.TemporaryDirectory(prefix='codertec-contact-test-') as tmp:
    base = Path(tmp); public = base/'public'; public.mkdir()
    for name in ['contact.php','contact-protection.php','en/contact_site_en.php','es/contacto_site_es.php']:
        dest=public/name; dest.parent.mkdir(exist_ok=True); shutil.copy2(ROOT/name,dest)
    mock=public/'PHPMailer/src'; mock.mkdir(parents=True)
    (mock/'PHPMailer.php').write_text('''<?php
namespace PHPMailer\\PHPMailer;
#[\\AllowDynamicProperties]
class PHPMailer {
 function __construct($x) {} function isSMTP() {} function setFrom(...$x) {}
 function addAddress(...$x) {} function addReplyTo(...$x) {} function isHTML(...$x) {}
 function send() { file_put_contents(getenv('MOCK_LOG'), $this->Body . "\\n", FILE_APPEND); return true; }
}
''')
    for name in ['SMTP.php','Exception.php']: (mock/name).write_text('<?php')
    (public/'config').mkdir()
    (public/'config/email.php').write_text("<?php return ['host'=>'invalid.test','username'=>'test','password'=>'fake','encryption'=>'ssl','port'=>465];")
    store=base/'private'; store.mkdir(); log=base/'sent.log'
    env={**os.environ,'CODERTEC_CONTACT_STORAGE':str(store),'MOCK_LOG':str(log)}
    with socket.socket() as sock: sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]
    server=subprocess.Popen(['php','-S',f'127.0.0.1:{port}','-t',str(public)],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    opener=urllib.request.build_opener(NoRedirect)
    good={'nome':'Ana <Silva>','email':'ana@example.com','mensagem':'Quero uma promoção para meu site https://example.com?a=1&b=2','website':'','lang':'pt'}
    def request(data, path='/contact.php', expected=400):
        req=urllib.request.Request(f'http://127.0.0.1:{port}'+path, data=urllib.parse.urlencode(data).encode() if data is not None else None,headers={'X-Forwarded-For':'198.51.100.99'})
        try: response=opener.open(req)
        except urllib.error.HTTPError as error: response=error
        body=response.read().decode()
        assert response.code==expected,(response.code,expected,body)
        return response,body
    try:
        for _ in range(50):
            try:
                with socket.create_connection(('127.0.0.1',port),timeout=.1): break
            except OSError: time.sleep(.1)
        request(None,expected=405)
        for patch in [{'mensagem':'YOUR $25,000 PROMO CODE IS YOUR TREASURE'}, {'mensagem':'Veja https://m.clickto.cc/test'}, {'website':'bot'}, {'email':'bad'}, {'nome':''}, {'mensagem':'x'*5001}, {'nome':'x'*121}, {'nome':'x\r\nBcc: victim@example.com'}]:
            request({**good,**patch},expected=422 if 'website' in patch or patch.get('mensagem','').startswith(('YOUR','Veja')) else 400)
        for field in ['nome','email','mensagem','website','lang']:
            data=good.copy(); del data[field]; data[field+'[]']='x'; request(data)
        assert not log.exists(), 'Rejected requests reached SMTP mock'
        response,_=request(good,expected=303); assert response.headers['Location']=='/pt/obrigado.html'
        assert '&lt;Silva&gt;' in log.read_text() and '&amp;' in log.read_text()
        request({**good,'mensagem':'https://clickto.cc.example.org promoção'},expected=303)
        request({'name':'Ana','email':'ana@example.com','message':'Hello'},'/en/contact_site_en.php',303)
        response,_=request({'nombre':'Ana','correo':'ana@example.com','mensaje':'Hola'},'/es/contacto_site_es.php',303)
        assert response.headers['Location']=='/es/gracias.html'
        request(good,expected=303)
        for path,data,word in [('/contact.php',good,'Limite'),('/en/contact_site_en.php',{'name':'Ana','email':'ana@example.com','message':'Hello'},'limit'),('/es/contacto_site_es.php',{'nombre':'Ana','correo':'ana@example.com','mensaje':'Hola'},'límite')]:
            response,body=request(data,path,429); assert word in body and int(response.headers['Retry-After'])>0
        assert len(log.read_text().splitlines())==5
        rate=store/'rate-limit.json'; records=json.loads(rate.read_text()); records={k:[int(time.time())-900]*5 for k in records}; records['expired-other-ip']=[int(time.time())-901]; rate.write_text(json.dumps(records))
        request(good,expected=303)
        records=json.loads(rate.read_text()); assert 'expired-other-ip' not in records and sum(map(len,records.values()))==1
        for path,data,word in [('/en/contact_site_en.php',{'name[]':'x','email':'bad','message':'Hello'},'Enter'),('/es/contacto_site_es.php',{'nombre':'Ana','correo':'bad','mensaje':'Hola'},'Introduzca')]:
            _,body=request(data,path,400); assert word in body
        # Parallel processes contend on the same file: exactly five may proceed.
        rate.write_text('{}')
        runner=base/'rate.php'; runner.write_text("<?php require $argv[1]; echo contact_rate_limit($argv[2], '127.0.0.1', 10000);")
        workers=[subprocess.Popen(['php',str(runner),str(public/'contact-protection.php'),str(store)],stdout=subprocess.PIPE) for _ in range(12)]
        results=[w.communicate()[0].decode() for w in workers]
        assert results.count('0')==5 and results.count('900')==7,results
        # Storage inside the web root must fail closed before SMTP.
        check=base/'storage.php'; check.write_text("<?php require $argv[1]; $_SERVER['DOCUMENT_ROOT']=$argv[2]; putenv('CODERTEC_CONTACT_STORAGE=' . $argv[2]); try {contact_storage_dir(); exit(1);} catch (RuntimeException $e) {exit(0);}")
        subprocess.run(['php',str(check),str(public/'contact-protection.php'),str(public)],check=True)
        print('PASS: legitimate message, HTML escaping, specific spam, honeypot, invalid email, required/oversized/array fields, legacy routes, languages, HTTP status/redirects, shared rate limit, expiration/cleanup, concurrency, private storage. No real email sent.')
    finally:
        server.terminate(); server.wait(timeout=5)
