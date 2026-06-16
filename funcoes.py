from scraper import obter_titulo
import json
from urllib.parse import urlparse


def obter_link():
    url = input("Cole o link do produto: ")
    titulo = obter_titulo(url)

    if titulo is None:
        print("Não foi possível obter o produto.")
        return None, None

    return url, titulo

def carregar_sites_categorias():

    try:

        with open(
            "sites_categorias.json",
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)

    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def salvar_site_categoria(
    dominio,
    categoria
):

    sites = carregar_sites_categorias()

    sites[dominio] = categoria

    with open(
        "sites_categorias.json",
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            sites,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def obter_dominio(url):

    dominio = urlparse(url).netloc

    dominio = dominio.replace(
        "www.",
        ""
    )

    return dominio


def categorizar_produto(url):

    url = url.lower()

    dominio = obter_dominio(url)

    sites = carregar_sites_categorias()

    if dominio in sites:
        return sites[dominio]

    if "nike" in url or "adidas" in url or "centauro" in url or "netshoes" in url:
        return "Vestuário"

    elif "kabum" in url or "pichau" in url or "terabyteshop" in url:
        return "Tecnologia"

    elif "redragon" in url or "logitech" in url or "razer" in url:
        return "Tecnologia"

    elif "mercadolivre" in url or "amazon" in url or "enjoei" in url or "olx" in url or "shopee" in url:
        return "Marketplace"

    elif "pioner" in url or "cobrecar" in url or "mercadocar" in url:
        return "Automovel"

    elif "wella" in url or "loreal" in url or "natura" in url:
        return "Beleza"

    elif "livraria cultura" in url or "saraiva" in url:
        return "Livros"

    else:
        return "Outros"
    

def salvar_produto(produto):
    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            produtos = json.load(arquivo)

    except FileNotFoundError:
            produtos = []

    produtos.append(produto)

    with open("dados.json", "w", encoding="utf-8") as arquivo:
        json.dump(produtos, arquivo, ensure_ascii=False, indent=4)

    print("Produto salvo com sucesso!")


def listar_por_categoria():
    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            produtos = json.load(arquivo)

    except FileNotFoundError:
        print("Nenhum produto encontrado.")
        return

    categorias = {}

    for produto in produtos:
        categoria = produto["categoria"]

        if categoria not in categorias:
            categorias[categoria] = []

        categorias[categoria].append(produto)

    lista_categorias = list(categorias.keys())

    for i, categoria in enumerate(lista_categorias, start=1):
        print(f"{i} - {categoria}")

    escolha = int(input("Escolha uma categoria: "))

    categoria_escolhida = lista_categorias[escolha - 1]

    for produto in categorias[categoria_escolhida]:
        print(f" - {produto['nome']} (Frete: R${produto['frete']:.2f})")


def ver_total_por_categoria():
    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            produtos = json.load(arquivo)

    except FileNotFoundError:
        print("Nenhum produto encontrado.")
        return

    categorias = {}

    for produto in produtos:
        categoria = produto["categoria"]

        if categoria not in categorias:
            categorias[categoria] = []

        categorias[categoria].append(produto)

    lista_categorias = list(categorias.keys())

    for i, categoria in enumerate(lista_categorias, start=1):
        print(f"{i} - {categoria}")

    escolha = int(input("Escolha uma categoria: "))

    categoria_escolhida = lista_categorias[escolha - 1]

    total_produtos = 0
    total_fretes = 0

    print(f"\nCategoria: {categoria_escolhida}")
    print("-" * 50)

    for produto in categorias[categoria_escolhida]:

        preco = produto["preco"] if produto["preco"] is not None else 0
        frete = produto["frete"]

        print(f"Produto: {produto['nome']}")
        print(f"Preço: R${preco:.2f}")
        print(f"Frete: R${frete:.2f}")
        print("-" * 50)

        total_produtos += preco
        total_fretes += frete

    print("\nRESUMO")
    print("-" * 50)
    print(f"Total dos produtos: R${total_produtos:.2f}")
    print(f"Total dos produtos com frete: R${total_produtos + total_fretes:.2f}")


def remover_produto_por_categoria():
    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            produtos = json.load(arquivo)

    except FileNotFoundError:
        print("Nenhum produto encontrado.")
        return

    categorias = {}

    for produto in produtos:
        categoria = produto["categoria"]

        if categoria not in categorias:
            categorias[categoria] = []

        categorias[categoria].append(produto)

    lista_categorias = list(categorias.keys())

    print("*" * 50)

    for i, categoria in enumerate(lista_categorias, start=1):
        print(f"{i} - {categoria}")

    escolha = int(input("Escolha uma categoria: "))

    if escolha < 1 or escolha > len(lista_categorias):
        print("Categoria inválida.")
        return

    categoria_escolhida = lista_categorias[escolha - 1]

    produtos_categoria = categorias[categoria_escolhida]

    print("*" * 50)
    print(f"Categoria: {categoria_escolhida}")
    print("*" * 50)

    for i, produto in enumerate(produtos_categoria, start=1):

        preco = produto["preco"] if produto["preco"] is not None else 0

        print(
            f"{i} - {produto['nome']} "
            f"(Preço: R${preco:.2f} | "
            f"Frete: R${produto['frete']:.2f})"
        )

    print("*" * 50)

    escolha_produto = int(input("Escolha um produto para remover: "))

    if escolha_produto < 1 or escolha_produto > len(produtos_categoria):
        print("Produto inválido.")
        return

    produto_remover = produtos_categoria[escolha_produto - 1]

    produtos.remove(produto_remover)

    with open("dados.json", "w", encoding="utf-8") as arquivo:
        json.dump(
            produtos,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    print("*" * 50)
    print(f"Produto '{produto_remover['nome']}' removido com sucesso!")
    print("*" * 50)

def gerar_relatorio():
    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            produtos = json.load(arquivo)

    except FileNotFoundError:
        print("Nenhum produto encontrado.")
        return

    categorias = {}
    produtos_sem_preco = []

    total_produtos = 0
    total_fretes = 0
    quantidade_produtos = 0

    for produto in produtos:

        if produto["preco"] is None:
            produtos_sem_preco.append(produto["nome"])
            continue

        categoria = produto["categoria"]

        if categoria not in categorias:
            categorias[categoria] = {
                "quantidade": 0,
                "total": 0
            }

        categorias[categoria]["quantidade"] += 1
        categorias[categoria]["total"] += (
            produto["preco"] +
            produto["frete"]
        )

        total_produtos += produto["preco"]
        total_fretes += produto["frete"]
        quantidade_produtos += 1

    with open("relatorio.txt", "w", encoding="utf-8") as relatorio:

        relatorio.write("*" * 50 + "\n")
        relatorio.write("RELATÓRIO GERAL\n")
        relatorio.write("*" * 50 + "\n\n")

        relatorio.write(
            f"Total de produtos com preço identificado: "
            f"{quantidade_produtos}\n\n"
        )

        for categoria, dados in categorias.items():

            relatorio.write(f"Categoria: {categoria}\n")
            relatorio.write(
                f"Quantidade: {dados['quantidade']}\n"
            )
            relatorio.write(
                f"Total: R${dados['total']:.2f}\n"
            )
            relatorio.write("-" * 30 + "\n")

        relatorio.write("\n")
        relatorio.write("*" * 50 + "\n")
        relatorio.write(
            f"Total produtos: R${total_produtos:.2f}\n"
        )
        relatorio.write(
            f"Total fretes: R${total_fretes:.2f}\n"
        )
        relatorio.write(
            f"Total geral: R${total_produtos + total_fretes:.2f}\n"
        )
        relatorio.write("*" * 50 + "\n\n")

        if produtos_sem_preco:

            relatorio.write("*" * 50 + "\n")
            relatorio.write("PRODUTOS SEM PREÇO IDENTIFICADO\n")
            relatorio.write("*" * 50 + "\n")

            for produto in produtos_sem_preco:
                relatorio.write(f"- {produto}\n")

    print("Relatório gerado com sucesso!")


def carregar_categorias():

    try:

        with open(
            "categorias.json",
            "r",
            encoding="utf-8"
        ) as arquivo:

            categorias = json.load(arquivo)

            if not categorias:

                categorias = [
                    "Tecnologia",
                    "Marketplace",
                    "Vestuário"
                ]

                with open(
                    "categorias.json",
                    "w",
                    encoding="utf-8"
                ) as arq:

                    json.dump(
                        categorias,
                        arq,
                        ensure_ascii=False,
                        indent=4
                    )

            return categorias

    except (FileNotFoundError, json.JSONDecodeError):

        categorias = [
            "Tecnologia",
            "Marketplace",
            "Vestuário"
        ]

        with open(
            "categorias.json",
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                categorias,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

        return categorias
    

def adicionar_categoria(nome_categoria):

    categorias = carregar_categorias()

    if nome_categoria not in categorias:

        categorias.append(nome_categoria)

        with open("categorias.json", "w", encoding="utf-8") as arquivo:
            json.dump(
                categorias,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

