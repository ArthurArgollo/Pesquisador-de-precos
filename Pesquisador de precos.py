import requests
from bs4 import BeautifulSoup


def buscar_precos_mercado_livre(produto):
    termo_busca = produto.replace(' ', '-')
    url = f'https://lista.mercadolivre.com.br/{termo_busca}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36'
    }

    print(f"Buscando por '{produto}' em: {url}\n")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Pega todos os elementos com a classe do título com link
    itens = soup.select('a.poly-component__title')

    if not itens:
        print("Nenhum produto encontrado com a nova estrutura.")
        return

    palavras_chave = produto.lower().split()
    contador = 0

    for item in itens:
        titulo = item.get_text(strip=True)
        link = item.get('href')

        # Achar o bloco pai para tentar puxar o preço
        parent = item.find_parent('li')
        preco_tag = parent.select_one('span.andes-money-amount__fraction') if parent else None

        if preco_tag:
            preco = preco_tag.get_text(strip=True).replace('.', '')

            if all(p in titulo.lower() for p in palavras_chave):
                contador += 1
                print(f"Produto: {titulo}")
                print(f"Preço: R$ {preco}")
                print(f"Link: {link}\n")

    if contador == 0:
        print(f"Nenhum resultado relevante encontrado para '{produto}'.")
    else:
        print(f"--- Fim da busca. {contador} resultados relevantes exibidos. ---")

# Teste
produto = input("Escreva o nome do produto:")
buscar_precos_mercado_livre(produto)