import requests
from bs4 import BeautifulSoup
import re


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive"
}


def obter_titulo(url):
    try:
        resposta = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        print(f"Status Título: {resposta.status_code}")

        if resposta.status_code != 200:
            return None

        soup = BeautifulSoup(
            resposta.text,
            "html.parser"
        )

        if soup.title:
            return soup.title.get_text(strip=True)

        h1 = soup.find("h1")

        if h1:
            return h1.get_text(strip=True)

        return None

    except Exception as erro:
        print(f"Erro ao obter título: {erro}")
        return None


def obter_preco(url):
    try:
        resposta = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        print(f"Status Preço: {resposta.status_code}")

        if resposta.status_code == 403:
            print("Site bloqueou a consulta.")
            return None

        if resposta.status_code != 200:
            return None

        html = resposta.text

        # =====================================
        # MÉTODO 1 - REDRAGON
        # =====================================

        preco = re.search(
            r"produto_preco\s*=\s*([\d.]+)",
            html
        )

        if preco:
            return float(preco.group(1))

        # =====================================
        # MÉTODO 2 - KABUM
        # =====================================

        preco = re.search(
            r'"discountPrice":([\d.]+)',
            html
        )

        if preco:
            return float(preco.group(1))

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # =====================================
        # MÉTODO 3 - MERCADO LIVRE
        # =====================================

        preco = re.search(
            r'"value":([\d.]+),"original_value"',
            html
        )

        if preco:
            return float(preco.group(1))

        # =====================================
        # MÉTODO 4 - META TAG PROPERTY
        # =====================================

        meta_preco = soup.find(
            "meta",
            attrs={"property": "product:price:amount"}
        )

        if meta_preco:

            valor = meta_preco["content"]

            valor = valor.replace("R$", "")
            valor = valor.replace(",", "")
            valor = valor.strip()

            return float(valor)

        # =====================================
        # MÉTODO 5 - META TAG NAME (PICHAU)
        # =====================================

        meta_preco = soup.find(
            "meta",
            attrs={"name": "product:price:amount"}
        )

        if meta_preco:

            valor = meta_preco["content"]

            valor = valor.replace("R$", "")
            valor = valor.replace(",", "")
            valor = valor.strip()

            return float(valor)

        # =====================================
        # MÉTODO 6 - JSON-LD
        # =====================================

        preco = re.search(
            r'"price":"?([\d.]+)"?',
            html
        )

        if preco:
            return float(preco.group(1))

        # =====================================
        # MÉTODO 7 - BUSCA GENÉRICA
        # =====================================

        palavras_chave = [
            "discountPrice",
            "priceWithDiscount",
            "finalPrice",
            "salePrice",
            "productPrice",
            "price",
            "priceAmount",
            "amount",
            "basePrice"
        ]

        for palavra in palavras_chave:

            preco = re.search(
                rf'"{palavra}":([\d.]+)',
                html
            )

            if preco:
                return float(preco.group(1))

        # =====================================
        # MÉTODO 8 - R$ NO HTML
        # =====================================

        preco = re.search(
            r'R\$\s*([\d.]+,\d{2})',
            html
        )

        if preco:

            valor = preco.group(1)

            valor = valor.replace(".", "")
            valor = valor.replace(",", ".")

            return float(valor)

        return None

    except Exception as erro:
        print(f"Erro ao obter preço: {erro}")
        return None