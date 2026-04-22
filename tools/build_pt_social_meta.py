from __future__ import annotations

import html
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent.parent
STATIC_IMG_DIR = ROOT / "static" / "img"
LOGO_PATH = ROOT / "static" / "images" / "logo_codertec_atual.png"

SITE_URL = "https://codertec.com.br"
DEFAULT_IMAGE_PATH = "/static/img/default-og.jpg"
PLAN_IMAGE_PATH = "/static/img/og-planos-sites-v2.jpg"

DEFAULT_IMAGE_URL = f"{SITE_URL}{DEFAULT_IMAGE_PATH}"
PLAN_IMAGE_URL = f"{SITE_URL}{PLAN_IMAGE_PATH}"

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 630

TITLE_RE = re.compile(r"\s*<title>.*?</title>\s*", re.IGNORECASE | re.DOTALL)
DESCRIPTION_RE = re.compile(
    r"\s*<meta\s+name=\"description\"[^>]*>\s*",
    re.IGNORECASE | re.DOTALL,
)
CANONICAL_RE = re.compile(
    r"\s*<link\s+rel=\"canonical\"[^>]*>\s*",
    re.IGNORECASE | re.DOTALL,
)
SOCIAL_RE = re.compile(
    r"\s*<meta\s+(?:property|name)=\"(?:og:[^\"]+|twitter:[^\"]+)\"[^>]*>\s*",
    re.IGNORECASE | re.DOTALL,
)


PAGES = {
    "pt/index.html": {
        "url": f"{SITE_URL}/pt/",
        "title": "CoderTec | IA, Automação, Dashboards e SaaS para Empresas e Clínicas",
        "description": (
            "A CoderTec desenvolve soluções em inteligência artificial, automação, dashboards, "
            "ciência de dados, sistemas web e SaaS para empresas, clínicas e profissionais."
        ),
        "twitter_title": "IA, automação, dashboards e websites | CoderTec",
        "twitter_description": (
            "Soluções sob medida para empresas, clínicas e profissionais venderem mais e operarem melhor."
        ),
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para compartilhamento do site.",
    },
    "pt/obrigado.html": {
        "url": f"{SITE_URL}/pt/obrigado.html",
        "title": "Obrigado pelo contato | CoderTec",
        "description": "Recebemos sua mensagem. Em breve a CoderTec retorna para conversar sobre seu projeto.",
        "twitter_title": "Obrigado pelo contato | CoderTec",
        "twitter_description": "Recebemos sua mensagem e vamos responder em breve.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para compartilhamento do site.",
    },
    "pt/portfolio.html": {
        "url": f"{SITE_URL}/pt/portfolio.html",
        "title": "Portfólio de Soluções Digitais | CoderTec",
        "description": (
            "Conheça projetos e soluções desenvolvidos pela CoderTec em websites, automação, "
            "inteligência artificial, dashboards e produtos digitais."
        ),
        "twitter_title": "Portfólio de Soluções Digitais | CoderTec",
        "twitter_description": "Projetos reais em websites, automação, IA, dashboards e produtos digitais.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para compartilhamento do portfólio.",
    },
    "pt/sobre-mim.html": {
        "url": f"{SITE_URL}/pt/sobre-mim.html",
        "title": "Sobre Marcelo Zagonel Levek | CoderTec",
        "description": (
            "Conheça Marcelo Zagonel Levek, profissional da CoderTec com atuação em ciência de dados, "
            "desenvolvimento web, automação e inteligência artificial."
        ),
        "twitter_title": "Sobre Marcelo Zagonel Levek | CoderTec",
        "twitter_description": "Ciência de dados, desenvolvimento web, automação e inteligência artificial.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para compartilhamento da página sobre.",
    },
    "pt/automacao-empresarial-em-curitiba/index.html": {
        "url": f"{SITE_URL}/pt/automacao-empresarial-em-curitiba/",
        "title": "Automação Empresarial em Curitiba | CoderTec",
        "description": (
            "Automação de processos em Curitiba para eliminar tarefas repetitivas, reduzir erros "
            "e aumentar a produtividade com fluxos inteligentes."
        ),
        "twitter_title": "Automação Empresarial em Curitiba | CoderTec",
        "twitter_description": "Reduza tarefas manuais e ganhe produtividade com automações inteligentes.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para serviços de automação.",
    },
    "pt/demos/django/sites-institucionais/index.html": {
        "url": f"{SITE_URL}/pt/demos/django/sites-institucionais/",
        "title": "Demonstração de Site Institucional para Clínica | CoderTec",
        "description": (
            "Demonstração de site institucional para clínica odontológica com foco em apresentação "
            "profissional, confiança e agendamento."
        ),
        "twitter_title": "Demonstração de Site Institucional | CoderTec",
        "twitter_description": "Exemplo de site para clínica com foco em apresentação e agendamento.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para demonstrações de websites.",
    },
    "pt/inteligencia-artificial-em-curitiba/index.html": {
        "url": f"{SITE_URL}/pt/inteligencia-artificial-em-curitiba/",
        "title": "Inteligência Artificial em Curitiba | CoderTec",
        "description": (
            "Soluções de inteligência artificial em Curitiba com assistentes virtuais, automações, "
            "análise de dados e atendimento inteligente para empresas."
        ),
        "twitter_title": "Inteligência Artificial em Curitiba | CoderTec",
        "twitter_description": "Assistentes virtuais, automações e IA aplicada para empresas em Curitiba.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para serviços de inteligência artificial.",
    },
    "pt/site-que-trabalha/index.html": {
        "url": f"{SITE_URL}/pt/site-que-trabalha/",
        "title": "Planos de Sites | CoderTec",
        "description": (
            "Conheça os planos de sites da CoderTec: criação de sites profissionais com foco em "
            "credibilidade, WhatsApp, captação de contatos e estrutura pronta para evoluir com automação e IA."
        ),
        "twitter_title": "Planos de Sites | CoderTec",
        "twitter_description": "Sites profissionais com foco em credibilidade, WhatsApp, captação de contatos e evolução comercial.",
        "image": PLAN_IMAGE_URL,
        "image_alt": "Arte da CoderTec sobre planos de sites profissionais com WhatsApp, captação de contatos e apoio comercial.",
    },
    "pt/produtos/psicosense/index.html": {
        "url": f"{SITE_URL}/pt/produtos/psicosense/",
        "title": "Psicosense para Psicólogos e Clínicas | CoderTec",
        "description": (
            "Conheça o Psicosense, solução com IA e automação para psicólogos e clínicas "
            "organizarem atendimentos e ganharem eficiência."
        ),
        "twitter_title": "Psicosense para Psicólogos e Clínicas | CoderTec",
        "twitter_description": "IA e automação para organizar atendimentos e ganhar eficiência clínica.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para o produto Psicosense.",
    },
    "pt/servicos/automacao/index.html": {
        "url": f"{SITE_URL}/pt/servicos/automacao/",
        "title": "Automação de Processos para Empresas e Clínicas | CoderTec",
        "description": (
            "A CoderTec desenvolve automações para empresas, clínicas e profissionais "
            "reduzirem tarefas manuais, falhas e retrabalho."
        ),
        "twitter_title": "Automação de Processos | CoderTec",
        "twitter_description": "Reduza retrabalho e ganhe eficiência com automação sob medida.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para serviços de automação.",
    },
    "pt/servicos/ciencia-de-dados/index.html": {
        "url": f"{SITE_URL}/pt/servicos/ciencia-de-dados/",
        "title": "Ciência de Dados para Empresas e Clínicas | CoderTec",
        "description": (
            "A CoderTec desenvolve análises, insights e soluções em ciência de dados para empresas, "
            "clínicas e profissionais tomarem decisões com mais clareza."
        ),
        "twitter_title": "Ciência de Dados para Empresas e Clínicas | CoderTec",
        "twitter_description": "Análises, indicadores e insights para decisões mais claras.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para serviços de ciência de dados.",
    },
    "pt/servicos/dashboards/index.html": {
        "url": f"{SITE_URL}/pt/servicos/dashboards/",
        "title": "Dashboards Personalizados para Empresas e Clínicas | CoderTec",
        "description": (
            "A CoderTec desenvolve dashboards personalizados e indicadores para empresas, clínicas "
            "e profissionais acompanharem resultados com mais clareza e rapidez."
        ),
        "twitter_title": "Dashboards Personalizados | CoderTec",
        "twitter_description": "Indicadores visuais e dashboards sob medida para decisões mais rápidas.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para serviços de dashboards.",
    },
    "pt/servicos/desenvolvimento-web/index.html": {
        "url": f"{SITE_URL}/pt/servicos/desenvolvimento-web/",
        "title": "Desenvolvimento Web sob Medida | CoderTec",
        "description": (
            "A CoderTec desenvolve sites, landing pages, sistemas web e aplicações sob medida "
            "para empresas, clínicas e profissionais."
        ),
        "twitter_title": "Desenvolvimento Web sob Medida | CoderTec",
        "twitter_description": "Sites, landing pages e sistemas web sob medida para vender e operar melhor.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para desenvolvimento web.",
    },
    "pt/servicos/inteligencia-artificial/index.html": {
        "url": f"{SITE_URL}/pt/servicos/inteligencia-artificial/",
        "title": "Inteligência Artificial para Empresas e Clínicas | CoderTec",
        "description": (
            "A CoderTec desenvolve soluções com inteligência artificial para empresas, clínicas "
            "e profissionais automatizarem processos e ganharem eficiência."
        ),
        "twitter_title": "Inteligência Artificial para Empresas e Clínicas | CoderTec",
        "twitter_description": "IA aplicada para atendimento, automação e ganho de eficiência.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para inteligência artificial.",
    },
    "pt/solucoes/landing-dentista.html": {
        "url": f"{SITE_URL}/pt/solucoes/landing-dentista.html",
        "title": "Landing Page para Dentistas | CoderTec",
        "description": (
            "Demonstração de landing page para dentistas com atendimento 24h, WhatsApp "
            "e estrutura pensada para conversão."
        ),
        "twitter_title": "Landing Page para Dentistas | CoderTec",
        "twitter_description": "Exemplo de página para dentistas com foco em atendimento e conversão.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para landing pages.",
    },
    "pt/solucoes/agentes-ia/index.html": {
        "url": f"{SITE_URL}/pt/solucoes/agentes-ia/",
        "title": "Agentes de IA para Atendimento | CoderTec",
        "description": (
            "Atendente virtual com inteligência artificial para responder clientes, qualificar contatos "
            "e automatizar atendimentos 24 horas por dia."
        ),
        "twitter_title": "Agentes de IA para Atendimento | CoderTec",
        "twitter_description": "Atendimento inteligente 24h com IA para empresas e clínicas.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para agentes de inteligência artificial.",
    },
    "pt/solucoes/webapps/index.html": {
        "url": f"{SITE_URL}/pt/solucoes/webapps/",
        "title": "Web Apps para Clínicas e Consultórios | CoderTec",
        "description": (
            "Web apps e dashboards sob medida para clínicas, consultórios e empresas "
            "organizarem processos, dados e atendimento com mais clareza."
        ),
        "twitter_title": "Web Apps para Clínicas e Consultórios | CoderTec",
        "twitter_description": "Soluções web sob medida para organizar operação, dados e atendimento.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para web apps.",
    },
    "pt/solucoes/websites/clinica.html": {
        "url": f"{SITE_URL}/pt/solucoes/websites/clinica/",
        "title": "Website para Clínicas | CoderTec",
        "description": (
            "Exemplo de website profissional para clínicas com foco em credibilidade, "
            "organização do atendimento e geração de contatos."
        ),
        "twitter_title": "Website para Clínicas | CoderTec",
        "twitter_description": "Exemplo de site para clínicas com foco em confiança e contatos.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para websites de clínicas.",
    },
    "pt/solucoes/websites/dentista.html": {
        "url": f"{SITE_URL}/pt/solucoes/websites/dentista/",
        "title": "Website para Dentistas | CoderTec",
        "description": (
            "Exemplo de website profissional para dentistas com foco em autoridade, "
            "clareza na apresentação e geração de agendamentos."
        ),
        "twitter_title": "Website para Dentistas | CoderTec",
        "twitter_description": "Exemplo de site para dentistas com foco em autoridade e agendamentos.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para websites de dentistas.",
    },
    "pt/solucoes/websites/index.html": {
        "url": f"{SITE_URL}/pt/websites/",
        "title": "Websites Profissionais para Empresas e Clínicas | CoderTec",
        "description": (
            "Criação de websites profissionais com foco em credibilidade, SEO, WhatsApp "
            "e geração de contatos para empresas, clínicas e profissionais."
        ),
        "twitter_title": "Websites Profissionais | CoderTec",
        "twitter_description": "Sites profissionais com foco em autoridade, SEO e geração de contatos.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para websites profissionais.",
    },
    "pt/solucoes/websites/smartpmoc.html": {
        "url": f"{SITE_URL}/pt/solucoes/websites/smartpmoc.html",
        "title": "Website SmartPMOC | CoderTec",
        "description": (
            "Website com monitoramento inteligente SmartPMOC para comunicar solução, "
            "mostrar valor técnico e gerar novos contatos."
        ),
        "twitter_title": "Website SmartPMOC | CoderTec",
        "twitter_description": "Exemplo de website técnico com comunicação clara e foco comercial.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para websites técnicos.",
    },
    "pt/videos/automacao/exemplo_integracao_apis.html": {
        "url": f"{SITE_URL}/pt/videos/automacao/exemplo_integracao_apis.html",
        "title": "Exemplo de Integração com APIs | CoderTec",
        "description": (
            "Exemplo visual de integração com APIs para automatizar processos, conectar sistemas "
            "e reduzir tarefas manuais."
        ),
        "twitter_title": "Exemplo de Integração com APIs | CoderTec",
        "twitter_description": "Veja uma demonstração de integração de sistemas e automação com APIs.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para demonstrações de automação.",
    },
    "pt/videos/automacao/exemplo_relatorio_automacoes.html": {
        "url": f"{SITE_URL}/pt/videos/automacao/exemplo_relatorio_automacoes.html",
        "title": "Exemplo de Relatórios Automáticos | CoderTec",
        "description": (
            "Exemplo visual de relatórios automáticos para acompanhar indicadores, processos "
            "e resultados de automações."
        ),
        "twitter_title": "Exemplo de Relatórios Automáticos | CoderTec",
        "twitter_description": "Veja uma demonstração de relatórios automáticos e indicadores.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para relatórios automáticos.",
    },
    "pt/websites-em-curitiba/index.html": {
        "url": f"{SITE_URL}/pt/websites-em-curitiba/",
        "title": "Criação de Sites Profissionais em Curitiba | CoderTec",
        "description": (
            "Criação de websites profissionais em Curitiba para empresas, clínicas e consultórios "
            "com SEO local, WhatsApp e presença forte no Google."
        ),
        "twitter_title": "Sites Profissionais em Curitiba | CoderTec",
        "twitter_description": "Websites em Curitiba com foco em conversão, SEO local e WhatsApp.",
        "image": DEFAULT_IMAGE_URL,
        "image_alt": "Arte institucional da CoderTec em azul e amarelo para websites em Curitiba.",
    },
}


def hex_to_rgb(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[index:index + 2], 16) for index in (0, 2, 4))


def blend(color_a: tuple[int, int, int], color_b: tuple[int, int, int], ratio: float) -> tuple[int, int, int]:
    return tuple(
        int(color_a[index] * (1 - ratio) + color_b[index] * ratio)
        for index in range(3)
    )


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates.extend(
            [
                Path("C:/Windows/Fonts/segoeuib.ttf"),
                Path("C:/Windows/Fonts/arialbd.ttf"),
                Path("C:/Windows/Fonts/calibrib.ttf"),
            ]
        )
    else:
        candidates.extend(
            [
                Path("C:/Windows/Fonts/segoeui.ttf"),
                Path("C:/Windows/Fonts/arial.ttf"),
                Path("C:/Windows/Fonts/calibri.ttf"),
            ]
        )

    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def wrap_text(text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    dummy = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(dummy)
    words = text.split()
    lines: list[str] = []
    current = ""

    for word in words:
        trial = word if not current else f"{current} {word}"
        trial_box = draw.textbbox((0, 0), trial, font=font)
        if trial_box[2] - trial_box[0] <= max_width:
            current = trial
            continue

        if current:
            lines.append(current)
        current = word

    if current:
        lines.append(current)

    return lines


def draw_gradient_background() -> Image.Image:
    base = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT))
    draw = ImageDraw.Draw(base)

    dark = hex_to_rgb("#0a2540")
    blue = hex_to_rgb("#3782cc")
    accent = hex_to_rgb("#ffc107")
    light = hex_to_rgb("#d9ecff")

    for y in range(CANVAS_HEIGHT):
        y_ratio = y / max(CANVAS_HEIGHT - 1, 1)
        row_base = blend(dark, blue, min(0.72, y_ratio * 0.78))
        for x in range(CANVAS_WIDTH):
            x_ratio = x / max(CANVAS_WIDTH - 1, 1)
            tone = blend(row_base, light, max(0.0, (x_ratio - 0.6) * 0.18))
            draw.point((x, y), fill=tone + (255,))

    overlay = Image.new("RGBA", (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.ellipse((780, -80, 1320, 420), fill=accent + (230,))
    overlay_draw.ellipse((820, 260, 1230, 720), fill=(255, 255, 255, 34))
    overlay_draw.rounded_rectangle((710, 70, 1140, 540), radius=52, fill=(255, 255, 255, 28))
    overlay_draw.rounded_rectangle((40, 460, 600, 595), radius=42, fill=(255, 255, 255, 20))
    overlay = overlay.filter(ImageFilter.GaussianBlur(2))

    return Image.alpha_composite(base, overlay)


def add_logo_card(canvas: Image.Image) -> None:
    if not LOGO_PATH.exists():
        return

    logo = Image.open(LOGO_PATH).convert("RGBA")
    ratio = 360 / logo.width
    logo = logo.resize((int(logo.width * ratio), int(logo.height * ratio)), Image.Resampling.LANCZOS)

    card = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle((760, 92, 1110, 232), radius=34, fill=(255, 255, 255, 248))
    draw.rounded_rectangle((780, 205, 940, 221), radius=8, fill=(10, 37, 64, 26))
    canvas.alpha_composite(card)

    logo_x = 790
    logo_y = 132
    canvas.alpha_composite(logo, (logo_x, logo_y))


def add_badge(draw: ImageDraw.ImageDraw, text: str) -> None:
    badge_font = load_font(26, bold=True)
    bbox = draw.textbbox((0, 0), text, font=badge_font)
    width = bbox[2] - bbox[0] + 46
    draw.rounded_rectangle((70, 60, 70 + width, 114), radius=22, fill=(255, 255, 255, 40))
    draw.text((93, 76), text, font=badge_font, fill=(255, 255, 255))


def draw_multiline(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    start_xy: tuple[int, int],
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int] | tuple[int, int, int, int],
    line_gap: int,
) -> int:
    x, y = start_xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y = bbox[3] + line_gap
    return y


def create_og_image(
    output_path: Path,
    headline: str,
    subtitle: str,
    supporting: str,
    badge: str,
) -> None:
    canvas = draw_gradient_background()
    draw = ImageDraw.Draw(canvas)

    add_logo_card(canvas)
    add_badge(draw, badge)

    title_font = load_font(64, bold=True)
    subtitle_font = load_font(34, bold=True)
    body_font = load_font(28)

    title_lines = wrap_text(headline, title_font, 610)
    next_y = draw_multiline(draw, title_lines, (70, 150), title_font, (255, 255, 255), 10)

    subtitle_box = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_box[2] - subtitle_box[0] + 44
    subtitle_y = next_y + 18
    draw.rounded_rectangle(
        (70, subtitle_y, 70 + subtitle_width, subtitle_y + 64),
        radius=22,
        fill=(255, 193, 7),
    )
    draw.text((92, subtitle_y + 13), subtitle, font=subtitle_font, fill=(10, 37, 64))

    body_lines = wrap_text(supporting, body_font, 610)
    draw_multiline(draw, body_lines, (70, subtitle_y + 92), body_font, (232, 242, 255), 8)

    canvas.convert("RGB").save(output_path, quality=92, subsampling=0)


def build_meta_block(meta: dict[str, str]) -> str:
    def esc(value: str) -> str:
        return html.escape(value, quote=True)

    return "\n".join(
        [
            f'    <title>{esc(meta["title"])}</title>',
            f'    <meta name="description" content="{esc(meta["description"])}">',
            f'    <link rel="canonical" href="{esc(meta["url"])}">',
            "",
            '    <meta property="og:locale" content="pt_BR">',
            '    <meta property="og:type" content="website">',
            '    <meta property="og:site_name" content="CoderTec">',
            f'    <meta property="og:title" content="{esc(meta["title"])}">',
            f'    <meta property="og:description" content="{esc(meta["description"])}">',
            f'    <meta property="og:url" content="{esc(meta["url"])}">',
            f'    <meta property="og:image" content="{esc(meta["image"])}">',
            f'    <meta property="og:image:secure_url" content="{esc(meta["image"])}">',
            '    <meta property="og:image:width" content="1200">',
            '    <meta property="og:image:height" content="630">',
            '    <meta property="og:image:type" content="image/jpeg">',
            f'    <meta property="og:image:alt" content="{esc(meta["image_alt"])}">',
            "",
            '    <meta name="twitter:card" content="summary_large_image">',
            f'    <meta name="twitter:title" content="{esc(meta["twitter_title"])}">',
            f'    <meta name="twitter:description" content="{esc(meta["twitter_description"])}">',
            f'    <meta name="twitter:image" content="{esc(meta["image"])}">',
            f'    <meta name="twitter:image:alt" content="{esc(meta["image_alt"])}">',
        ]
    )


def update_head(html_text: str, meta: dict[str, str]) -> str:
    head_match = re.search(r"(<head[^>]*>)(.*?)(</head>)", html_text, re.IGNORECASE | re.DOTALL)
    if not head_match:
        raise ValueError("Tag <head> não encontrada.")

    opening, head_inner, closing = head_match.groups()
    cleaned = TITLE_RE.sub("\n", head_inner, count=1)
    cleaned = DESCRIPTION_RE.sub("\n", cleaned, count=1)
    cleaned = CANONICAL_RE.sub("\n", cleaned, count=1)
    cleaned = SOCIAL_RE.sub("\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    anchor = None
    for pattern in [
        r"<meta\s+name=\"author\"[^>]*>",
        r"<meta\s+name=\"keywords\"[^>]*>",
        r"<meta\s+name=\"viewport\"[^>]*>",
        r"<meta\s+charset=\"[^\"]*\">",
    ]:
        matches = list(re.finditer(pattern, cleaned, re.IGNORECASE))
        if matches:
            anchor = matches[-1]
            break

    meta_block = "\n" + build_meta_block(meta) + "\n"

    if anchor:
        insert_at = anchor.end()
        cleaned = cleaned[:insert_at] + meta_block + cleaned[insert_at:]
    else:
        cleaned = meta_block + cleaned

    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).rstrip() + "\n"
    return html_text[:head_match.start()] + opening + cleaned + closing + html_text[head_match.end():]


def build_assets() -> None:
    STATIC_IMG_DIR.mkdir(parents=True, exist_ok=True)
    create_og_image(
        STATIC_IMG_DIR / "og-planos-sites-v2.jpg",
        "Planos de Sites que Trabalham",
        "WhatsApp, contatos e hospedagem",
        "Sites profissionais com foco em credibilidade, captação de contatos e evolução comercial.",
        "Compartilhe a CoderTec",
    )
    create_og_image(
        STATIC_IMG_DIR / "default-og.jpg",
        "Soluções Digitais sob Medida",
        "IA, automação, websites e dashboards",
        "Projetos para empresas, clínicas e profissionais crescerem com mais clareza e eficiência.",
        "CoderTec",
    )


def update_pages() -> None:
    for relative_path, meta in PAGES.items():
        file_path = ROOT / relative_path
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {relative_path}")

        original = file_path.read_text(encoding="utf-8")
        updated = update_head(original, meta)
        file_path.write_text(updated, encoding="utf-8", newline="\n")


def main() -> None:
    build_assets()
    update_pages()
    print(f"Imagens OG geradas em: {STATIC_IMG_DIR}")
    print(f"Metadados sociais atualizados em {len(PAGES)} páginas.")


if __name__ == "__main__":
    main()
