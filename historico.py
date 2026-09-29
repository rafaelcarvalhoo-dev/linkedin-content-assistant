# ROBÔ LINKEDIN CONTEÚDO V1 — histórico e Prompt Visual V2.
# Registros antigos são lidos sem migração ou remoção de campos.

import json
import os
from datetime import datetime, timedelta

PASTA_DADOS = "dados"
ARQUIVO_HISTORICO = os.path.join(PASTA_DADOS, "historico_posts.json")

# Os status antigos continuam participando da proteção contra repetição.
STATUS_QUE_BLOQUEIAM_TEMA = [
    "gerado", "pendente", "aprovado", "agendado", "publicado",
]


def garantir_estrutura():

    os.makedirs(
        PASTA_DADOS,
        exist_ok=True
    )

    if not os.path.exists(
        ARQUIVO_HISTORICO
    ):

        with open(
            ARQUIVO_HISTORICO,
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                [],
                arquivo,
                ensure_ascii=False,
                indent=4
            )


def carregar_historico():

    garantir_estrutura()

    try:

        with open(
            ARQUIVO_HISTORICO,
            "r",
            encoding="utf-8"
        ) as arquivo:

            dados = json.load(
                arquivo
            )

            if isinstance(
                dados,
                list
            ):
                return dados

            return []

    except (
        json.JSONDecodeError,
        FileNotFoundError
    ):

        return []


def salvar_historico(
    historico
):

    garantir_estrutura()

    with open(
        ARQUIVO_HISTORICO,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            historico,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def gerar_id_registro():

    return datetime.now().strftime(
        "%Y%m%d%H%M%S%f"
    )


def registrar_post(
    tema,
    post,
    status="gerado",
    arquivo=None
):

    historico = carregar_historico()

    registro = {
        "id": gerar_id_registro(),
        "data": datetime.now().isoformat(
            timespec="seconds"
        ),
        "categoria": tema["categoria"],
        "tema": tema["tema"],
        "nivel": tema["nivel"],
        "tipo": tema["tipo"],
        "status": status,
        "arquivo": arquivo,
        "post": post,
    }

    historico.append(
        registro
    )

    salvar_historico(
        historico
    )

    return registro


def listar_posts_por_status(
    status
):

    historico = carregar_historico()

    status = status.lower()

    registros = []

    for registro in historico:

        if (
            registro.get(
                "status",
                ""
            ).lower()
            == status
        ):

            registros.append(
                registro
            )

    return registros


def buscar_registro_por_id(
    id_registro
):

    historico = carregar_historico()

    for registro in historico:

        if (
            registro.get("id")
            == id_registro
        ):

            return registro

    return None


# Consulta de compatibilidade ainda utilizada pelo main.py atual.


def tema_tem_pendente(
    tema
):

    pendentes = listar_posts_por_status(
        "pendente"
    )

    for registro in pendentes:

        if (
            registro.get("tema")
            == tema
        ):

            return True

    return False


def tema_usado_recentemente(
    tema,
    dias_anti_repeticao
):

    historico = carregar_historico()

    limite_data = (
        datetime.now()
        - timedelta(
            days=dias_anti_repeticao
        )
    )

    for registro in historico:

        if (
            registro.get("tema")
            != tema
        ):
            continue

        status = registro.get(
            "status",
            ""
        ).lower()

        if (
            status
            not in STATUS_QUE_BLOQUEIAM_TEMA
        ):
            continue

        data_texto = (
            registro.get(
                "data_atualizacao"
            )
            or registro.get(
                "data"
            )
        )

        if not data_texto:
            continue

        try:

            data_registro = (
                datetime.fromisoformat(
                    data_texto
                )
            )

        except ValueError:

            continue

        if (
            data_registro
            >= limite_data
        ):

            return True

    return False


def salvar_briefing_imagem(
    id_registro,
    briefing
):
    """
    Salva o briefing visual dentro
    do registro da postagem.
    """

    historico = carregar_historico()

    for registro in historico:

        if (
            registro.get("id")
            != id_registro
        ):
            continue

        registro[
            "briefing_imagem"
        ] = briefing

        registro[
            "data_atualizacao"
        ] = datetime.now().isoformat(
            timespec="seconds"
        )

        salvar_historico(
            historico
        )

        return True

    return False
