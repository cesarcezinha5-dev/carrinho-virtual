import funcoes
import scraper


def menu():
    print("\nSeja bem-vindo ao seu carrinho virtual!")
    print("1 - Adicionar item")
    print("2 - Listar produtos por categoria")
    print("3 - Ver total por categoria")
    print("4 - Remover produto por categoria")
    print("5 - Gerar relatório")
    print("6 - Sair")


if __name__ == "__main__":

    while True:

        menu()

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":

            url, titulo = funcoes.obter_link()

            if not url:
                print("Não foi possível obter o produto.")
                continue

            if not titulo:

                print("Título não encontrado automaticamente.")

                titulo = input(
                    "Digite o nome do produto: "
                ).strip()

            categoria = funcoes.categorizar_produto(url)

            if categoria == "Outros":

                print("Categoria não identificada.")
                print("*" * 50)

                categorias = funcoes.carregar_categorias()

                print("Categorias existentes:")
                print()

                for i, cat in enumerate(
                    categorias,
                    start=1
                ):
                    print(f"{i} - {cat}")

                print("0 - Criar nova categoria")
                print()

                escolha = input(
                    "Escolha uma opção: "
                ).strip()

                if escolha == "0":

                    categoria = input(
                        "Digite o nome da nova categoria: "
                    ).strip().title()

                    funcoes.adicionar_categoria(
                        categoria
                    )

                    print(
                        f"Categoria '{categoria}' criada com sucesso!"
                    )

                else:

                    try:

                        categoria = categorias[
                            int(escolha) - 1
                        ]

                    except (
                        ValueError,
                        IndexError
                    ):

                        print(
                            "Opção inválida."
                        )

                        continue

                dominio = funcoes.obter_dominio(url)

                funcoes.salvar_site_categoria(
                    dominio,
                    categoria
                )

            print("*" * 50)

            preco = scraper.obter_preco(url)

            print(
                f"Produto encontrado: {titulo}"
            )

            if preco is not None:

                print(
                    f"Preço encontrado: R${preco:.2f}"
                )

            else:

                print(
                    "Preço não encontrado automaticamente."
                )

                try:

                    preco = float(
                        input(
                            "Digite o preço do produto: "
                        ).replace(",", ".")
                    )

                except ValueError:

                    print(
                        "Preço inválido."
                    )

                    continue

            print(
                f"Categoria identificada: {categoria}"
            )

            try:

                frete = float(
                    input(
                        "Digite o valor do frete: "
                    ).replace(",", ".")
                )

            except ValueError:

                print(
                    "Frete inválido."
                )

                continue

            produto = {
                "nome": titulo,
                "link": url,
                "categoria": categoria,
                "preco": preco,
                "frete": frete
            }

            funcoes.salvar_produto(
                produto
            )

            print("*" * 50)
            print(
                "Produto salvo com sucesso!"
            )
            print("*" * 50)

        elif opcao == "2":

            funcoes.listar_por_categoria()

        elif opcao == "3":

            funcoes.ver_total_por_categoria()

        elif opcao == "4":

            funcoes.remover_produto_por_categoria()

        elif opcao == "5":

            funcoes.gerar_relatorio()

        elif opcao == "6":

            print(
                "Saindo do programa. Até mais!"
            )

            break

        else:

            print(
                "Opção inválida. Por favor, escolha uma opção válida."
            )