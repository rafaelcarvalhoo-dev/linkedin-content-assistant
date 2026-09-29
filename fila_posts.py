# ROBÔ LINKEDIN CONTEÚDO V1 — salvamento de publicações geradas.
# As pastas e os arquivos de publicações antigas permanecem intactos.

import os
import re
from datetime import datetime

PASTA_POSTS = "posts"
PASTA_GERADOS = os.path.join(PASTA_POSTS, "gerados")


def garantir_estrutura_posts():
    """Garante somente a pasta utilizada para novas publicações da V1."""
    os.makedirs(PASTA_GERADOS, exist_ok=True)


def limpar_nome_arquivo(texto):
    """
    Remove caracteres inválidos para nomes
    de arquivo no Windows.
    """

    texto = texto.strip()

    texto = re.sub(
        r'[<>:"/\\|?*]',
        "",
        texto
    )

    texto = re.sub(
        r"\s+",
        "_",
        texto
    )

    return texto[:80]


def gerar_nome_arquivo(tema):
    """
    Cria um nome único para o arquivo.
    """

    agora = datetime.now()

    data_hora = agora.strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    categoria = limpar_nome_arquivo(
        tema["categoria"]
    )

    assunto = limpar_nome_arquivo(
        tema["tema"]
    )

    return (
        f"{data_hora}_"
        f"{categoria}_"
        f"{assunto}.txt"
    )


def salvar_post_gerado(
    tema,
    post
):
    """
    Salva uma nova postagem gerada pelo fluxo V1 final.

    Os arquivos antigos em posts/pendentes permanecem intactos
    para preservar compatibilidade com o histórico existente.
    """

    garantir_estrutura_posts()

    nome_arquivo = gerar_nome_arquivo(
        tema
    )

    caminho = os.path.join(
        PASTA_GERADOS,
        nome_arquivo
    )

    conteudo = f"""
STATUS: GERADO

CATEGORIA: {tema["categoria"]}
TEMA: {tema["tema"]}
NIVEL: {tema["nivel"]}
TIPO: {tema["tipo"]}

============================================================
POSTAGEM
============================================================

{post}
""".strip()

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(
            conteudo
        )

    return caminho
