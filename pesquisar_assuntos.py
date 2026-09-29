from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
import re

import feedparser


DIAS_MAXIMOS_ASSUNTO = 45
LIMITE_RESULTADOS = 15


# ============================================================
# FONTES RSS
# ============================================================

FONTES_RSS = [
    {
        "nome": "AWS News Blog",
        "url": "https://aws.amazon.com/about-aws/whats-new/recent/feed/",
    },
    {
        "nome": "Microsoft .NET Blog",
        "url": "https://devblogs.microsoft.com/dotnet/feed/",
    },
    {
        "nome": "Python Insider",
        "url": "https://blog.python.org/rss.xml",
    },
    {
        "nome": "Microsoft SQL Server Blog",
        "url": "https://www.microsoft.com/en-us/sql-server/blog/feed/",
    },
]


# ============================================================
# PALAVRAS IMPORTANTES
# ============================================================

PALAVRAS_PRIORIDADE_ALTA = [
    "sql server",
    "python",
    "selenium",
    "automation",
    "automação",
    "automacao",
    ".net",
    "dotnet",
    "asp.net",
    "c#",
    "csharp",
    "aws",
    "amazon web services",
    "database",
    "banco de dados",
    "data engineering",
    "engenharia de dados",
]


PALAVRAS_COMPLEMENTARES = [
    "sql",
    "api",
    "rest api",
    "cloud",
    "nuvem",
    "dados",
    "data",
    "devops",
    "azure",
    "machine learning",
    "artificial intelligence",
    "inteligência artificial",
    "inteligencia artificial",
    "agentic ai",
    "ai agent",
    "agente de ia",
    "agentes de ia",
    "performance",
    "migration",
    "migração",
    "modernization",
    "modernização",
    "modernizacao",
    "security",
    "segurança",
    "seguranca",
]


PALAVRAS_CONTEUDO_PROFISSIONAL = [
    "developer",
    "desenvolvedor",
    "development",
    "desenvolvimento",
    "productivity",
    "produtividade",
    "performance",
    "best practices",
    "boas práticas",
    "boas praticas",
    "release",
    "preview",
    "new features",
    "novos recursos",
    "modernization",
    "modernização",
    "migration",
    "migração",
    "architecture",
    "arquitetura",
    "automation",
    "automação",
    "database",
    "sql",
    "python",
    ".net",
    "c#",
]


# ============================================================
# ASSUNTOS DE BAIXA PRIORIDADE
# ============================================================

PALAVRAS_BAIXA_PRIORIDADE = [
    "advertising",
    "advertisement",
    "ads demand",
    "media live",
    "medialive",
    "mediatailor",
    "broadcast",
    "live video",
    "watermarking",
    "forensic watermarking",
    "transit gateway peering",
    "network monitor",
    "contact center",
    "gaming",
    "game",
    "govcloud",
]


# ============================================================
# CATEGORIAS
# ============================================================

CATEGORIAS = {
    "SQL SERVER": [
        "sql server",
        "microsoft sql",
        "t-sql",
        "tsql",
        "sql database",
    ],

    "PYTHON": [
        "python",
        "django",
        "fastapi",
        "pandas",
        "pytest",
    ],

    "C# / .NET": [
        "c#",
        "csharp",
        ".net",
        "dotnet",
        "asp.net",
        "aspnet",
    ],

    "AUTOMAÇÃO": [
        "selenium",
        "automation",
        "automação",
        "automacao",
        "robot",
        "bot",
        "web automation",
        "process automation",
    ],

    "DADOS": [
        "data engineering",
        "engenharia de dados",
        "data engineer",
        "data pipeline",
        "pipeline de dados",
        "etl",
        "data quality",
        "qualidade de dados",
        "database",
        "banco de dados",
        "analytics",
    ],

    "IA": [
        "artificial intelligence",
        "inteligência artificial",
        "inteligencia artificial",
        "machine learning",
        "generative ai",
        "genai",
        "agentic ai",
        "ai agent",
        "ai agents",
        "agente de ia",
        "agentes de ia",
        "mcp",
    ],

    "AWS / CLOUD": [
        "aws",
        "amazon web services",
        "amazon rds",
        "amazon ec2",
        "aws lambda",
        "amazon s3",
        "cloud",
        "nuvem",
    ],
}


# ============================================================
# AFINIDADE BASE POR CATEGORIA
# ============================================================

AFINIDADE_CATEGORIA = {
    "SQL SERVER": 100,
    "PYTHON": 100,
    "C# / .NET": 95,
    "AUTOMAÇÃO": 95,
    "DADOS": 90,
    "AWS / CLOUD": 80,
    "IA": 75,
    "OUTROS": 45,
}


# ============================================================
# FUNÇÕES DE TEXTO
# ============================================================

def normalizar_texto(texto):
    if not texto:
        return ""

    texto = str(texto).lower().strip()

    # Remove HTML.
    texto = re.sub(r"<[^>]+>", " ", texto)

    # Remove espaços duplicados.
    texto = re.sub(r"\s+", " ", texto)

    return texto


def palavra_presente(palavra, texto):
    palavra = normalizar_texto(palavra)

    if not palavra:
        return False

    return palavra in texto


# ============================================================
# DATA
# ============================================================

def converter_data_publicacao(data_publicacao):
    if not data_publicacao:
        return None

    try:
        data = parsedate_to_datetime(data_publicacao)

        if data.tzinfo is None:
            data = data.replace(
                tzinfo=timezone.utc
            )

        return data.astimezone(
            timezone.utc
        )

    except Exception:
        return None


def calcular_dias_desde_publicacao(
    data_publicacao
):
    data = converter_data_publicacao(
        data_publicacao
    )

    if not data:
        return None

    agora = datetime.now(
        timezone.utc
    )

    diferenca = agora - data

    return diferenca.days


def assunto_e_atual(
    data_publicacao
):
    dias = calcular_dias_desde_publicacao(
        data_publicacao
    )

    # Caso a fonte não tenha data,
    # não descartamos automaticamente.
    if dias is None:
        return True

    # Pequena proteção para diferença
    # de horário entre fontes.
    if dias < 0:
        return True

    return (
        dias
        <= DIAS_MAXIMOS_ASSUNTO
    )


# ============================================================
# RELEVÂNCIA TÉCNICA
# ============================================================

def calcular_relevancia(
    titulo,
    descricao,
    data_publicacao=None,
):
    titulo_normalizado = normalizar_texto(
        titulo
    )

    descricao_normalizada = normalizar_texto(
        descricao
    )

    texto_completo = (
        titulo_normalizado
        + " "
        + descricao_normalizada
    )

    pontuacao = 0

    # --------------------------------------------------------
    # Palavras fortes no título.
    # --------------------------------------------------------

    for palavra in PALAVRAS_PRIORIDADE_ALTA:
        if palavra_presente(
            palavra,
            titulo_normalizado,
        ):
            pontuacao += 18

    # --------------------------------------------------------
    # Complementares no título.
    # --------------------------------------------------------

    for palavra in PALAVRAS_COMPLEMENTARES:
        if palavra_presente(
            palavra,
            titulo_normalizado,
        ):
            pontuacao += 8

    # --------------------------------------------------------
    # Palavras fortes na descrição.
    # --------------------------------------------------------

    for palavra in PALAVRAS_PRIORIDADE_ALTA:
        if palavra_presente(
            palavra,
            descricao_normalizada,
        ):
            pontuacao += 7

    # --------------------------------------------------------
    # Complementares na descrição.
    # --------------------------------------------------------

    for palavra in PALAVRAS_COMPLEMENTARES:
        if palavra_presente(
            palavra,
            descricao_normalizada,
        ):
            pontuacao += 3

    # --------------------------------------------------------
    # Potencial para publicação profissional.
    # --------------------------------------------------------

    for palavra in PALAVRAS_CONTEUDO_PROFISSIONAL:
        if palavra_presente(
            palavra,
            texto_completo,
        ):
            pontuacao += 3

    # --------------------------------------------------------
    # Penalidades.
    # --------------------------------------------------------

    for palavra in PALAVRAS_BAIXA_PRIORIDADE:
        if palavra_presente(
            palavra,
            texto_completo,
        ):
            pontuacao -= 25

    # --------------------------------------------------------
    # Bônus de atualidade.
    # --------------------------------------------------------

    dias = calcular_dias_desde_publicacao(
        data_publicacao
    )

    if dias is not None:

        if dias <= 3:
            pontuacao += 15

        elif dias <= 7:
            pontuacao += 12

        elif dias <= 15:
            pontuacao += 8

        elif dias <= 30:
            pontuacao += 4

    # --------------------------------------------------------
    # Limites.
    # --------------------------------------------------------

    if pontuacao < 0:
        pontuacao = 0

    if pontuacao > 100:
        pontuacao = 100

    return pontuacao


# ============================================================
# DETECÇÃO DE CATEGORIA
# ============================================================

def contar_palavras_categoria(
    categoria,
    titulo,
    descricao,
):
    titulo_normalizado = normalizar_texto(
        titulo
    )

    descricao_normalizada = normalizar_texto(
        descricao
    )

    pontuacao = 0

    for palavra in CATEGORIAS.get(
        categoria,
        [],
    ):
        if palavra_presente(
            palavra,
            titulo_normalizado,
        ):
            # Palavra no título tem mais peso.
            pontuacao += 3

        elif palavra_presente(
            palavra,
            descricao_normalizada,
        ):
            pontuacao += 1

    return pontuacao


def detectar_categoria(
    titulo,
    descricao,
    fonte="",
):
    titulo_normalizado = normalizar_texto(
        titulo
    )

    descricao_normalizada = normalizar_texto(
        descricao
    )

    fonte_normalizada = normalizar_texto(
        fonte
    )

    ordem_prioridade = [
        "SQL SERVER",
        "PYTHON",
        "C# / .NET",
        "AUTOMAÇÃO",
        "DADOS",
        "IA",
        "AWS / CLOUD",
    ]

    # ========================================================
    # 1. PRIMEIRO: analisar somente o título
    # ========================================================

    pontuacoes_titulo = {}

    for categoria in ordem_prioridade:

        pontuacao = 0

        for palavra in CATEGORIAS.get(
            categoria,
            [],
        ):
            if palavra_presente(
                palavra,
                titulo_normalizado,
            ):
                pontuacao += 10

        pontuacoes_titulo[
            categoria
        ] = pontuacao

    maior_categoria = "OUTROS"
    maior_pontuacao = 0

    for categoria in ordem_prioridade:

        pontuacao = pontuacoes_titulo.get(
            categoria,
            0,
        )

        if pontuacao > maior_pontuacao:
            maior_pontuacao = pontuacao
            maior_categoria = categoria

    # Se encontrou categoria clara no título,
    # usamos ela imediatamente.
    if maior_pontuacao > 0:
        return maior_categoria

    # ========================================================
    # 2. FALLBACK POR FONTE
    # ========================================================

    # Se veio diretamente da AWS e nenhuma tecnologia
    # mais específica apareceu no título, classificamos
    # como AWS / CLOUD.
    if "aws" in fonte_normalizada:
        return "AWS / CLOUD"

    # Fonte oficial .NET.
    if ".net" in fonte_normalizada:
        return "C# / .NET"

    # Fonte oficial Python.
    if "python" in fonte_normalizada:
        return "PYTHON"

    # Fonte SQL Server.
    if "sql server" in fonte_normalizada:
        return "SQL SERVER"

    # ========================================================
    # 3. ÚLTIMO RECURSO: descrição
    # ========================================================

    pontuacoes_descricao = {}

    for categoria in ordem_prioridade:

        pontuacao = 0

        for palavra in CATEGORIAS.get(
            categoria,
            [],
        ):
            if palavra_presente(
                palavra,
                descricao_normalizada,
            ):
                pontuacao += 1

        pontuacoes_descricao[
            categoria
        ] = pontuacao

    maior_categoria = "OUTROS"
    maior_pontuacao = 0

    for categoria in ordem_prioridade:

        pontuacao = pontuacoes_descricao.get(
            categoria,
            0,
        )

        if pontuacao > maior_pontuacao:
            maior_pontuacao = pontuacao
            maior_categoria = categoria

    return maior_categoria


# ============================================================
# AFINIDADE COM PERFIL
# ============================================================

def calcular_afinidade_perfil(
    titulo,
    descricao,
    categoria,
):
    texto = normalizar_texto(
        f"{titulo} {descricao}"
    )

    afinidade = AFINIDADE_CATEGORIA.get(
        categoria,
        45,
    )

    # --------------------------------------------------------
    # Combinações especialmente fortes.
    # --------------------------------------------------------

    if palavra_presente(
        "sql server",
        texto,
    ):
        afinidade += 10

    if palavra_presente(
        "python",
        texto,
    ):
        afinidade += 10

    if (
        palavra_presente(
            ".net",
            texto,
        )
        or palavra_presente(
            "dotnet",
            texto,
        )
        or palavra_presente(
            "c#",
            texto,
        )
    ):
        afinidade += 10

    if (
        palavra_presente(
            "selenium",
            texto,
        )
        or palavra_presente(
            "automation",
            texto,
        )
        or palavra_presente(
            "automação",
            texto,
        )
    ):
        afinidade += 10

    if (
        palavra_presente(
            "data engineering",
            texto,
        )
        or palavra_presente(
            "engenharia de dados",
            texto,
        )
        or palavra_presente(
            "data quality",
            texto,
        )
    ):
        afinidade += 8

    # --------------------------------------------------------
    # Combinações interessantes.
    # --------------------------------------------------------

    if (
        palavra_presente(
            "aws",
            texto,
        )
        and (
            palavra_presente(
                ".net",
                texto,
            )
            or palavra_presente(
                "dotnet",
                texto,
            )
            or palavra_presente(
                "sql server",
                texto,
            )
            or palavra_presente(
                "python",
                texto,
            )
        )
    ):
        afinidade += 10

    # --------------------------------------------------------
    # AWS genérico não deve receber afinidade máxima.
    # --------------------------------------------------------

    if categoria == "AWS / CLOUD":

        tecnologias_fortes = [
            "sql server",
            "python",
            ".net",
            "dotnet",
            "c#",
            "selenium",
            "automation",
            "data engineering",
        ]

        encontrou_tecnologia_forte = any(
            palavra_presente(
                palavra,
                texto,
            )
            for palavra
            in tecnologias_fortes
        )

        if not encontrou_tecnologia_forte:
            afinidade -= 15

    # --------------------------------------------------------
    # Baixa prioridade reduz afinidade também.
    # --------------------------------------------------------

    for palavra in PALAVRAS_BAIXA_PRIORIDADE:
        if palavra_presente(
            palavra,
            texto,
        ):
            afinidade -= 10

    if afinidade < 0:
        afinidade = 0

    if afinidade > 100:
        afinidade = 100

    return afinidade


# ============================================================
# PONTUAÇÃO FINAL
# ============================================================

def calcular_pontuacao_final(
    relevancia_tecnica,
    afinidade_perfil,
):
    # 70% = qualidade/relevância da notícia
    # 30% = compatibilidade com o perfil.

    pontuacao = (
        relevancia_tecnica * 0.70
        + afinidade_perfil * 0.30
    )

    pontuacao = round(
        pontuacao
    )

    if pontuacao < 0:
        pontuacao = 0

    if pontuacao > 100:
        pontuacao = 100

    return pontuacao


def classificar_relevancia(
    pontuacao
):
    if pontuacao >= 80:
        return "PRIORIDADE"

    if pontuacao >= 65:
        return "MUITO RELEVANTE"

    if pontuacao >= 45:
        return "RELEVANTE"

    if pontuacao >= 30:
        return "POSSÍVEL"

    return "DESCARTAR"


# ============================================================
# RSS
# ============================================================

def buscar_feed(
    fonte
):
    print()

    print(
        f"🔎 Consultando: "
        f"{fonte['nome']}"
    )

    try:
        feed = feedparser.parse(
            fonte["url"]
        )

        if getattr(
            feed,
            "bozo",
            False,
        ):
            print(
                "⚠️ A fonte retornou "
                "um aviso ao ser lida."
            )

        entradas = getattr(
            feed,
            "entries",
            [],
        )

        print(
            f"✅ Itens encontrados: "
            f"{len(entradas)}"
        )

        assuntos = []

        # Até 30 notícias por fonte.
        for entrada in entradas[:30]:

            titulo = entrada.get(
                "title",
                "",
            )

            descricao = (
                entrada.get(
                    "summary",
                    "",
                )
                or entrada.get(
                    "description",
                    "",
                )
            )

            link = entrada.get(
                "link",
                "",
            )

            data_publicacao = (
                entrada.get(
                    "published",
                    "",
                )
                or entrada.get(
                    "updated",
                    "",
                )
            )

            assuntos.append(
                {
                    "titulo": titulo,
                    "descricao": descricao,
                    "fonte": fonte["nome"],
                    "url": link,
                    "data_publicacao": (
                        data_publicacao
                    ),
                }
            )

        return assuntos

    except Exception as erro:

        print(
            f"❌ Erro ao consultar "
            f"{fonte['nome']}: "
            f"{erro}"
        )

        return []


def buscar_assuntos_na_internet():
    todos_assuntos = []

    for fonte in FONTES_RSS:

        assuntos = buscar_feed(
            fonte
        )

        todos_assuntos.extend(
            assuntos
        )

    return todos_assuntos


# ============================================================
# CAMADA EDITORIAL
# ============================================================

def limpar_texto_editorial(texto):
    """
    Limpa HTML e espaços sem transformar
    todo o conteúdo em letras minúsculas.

    Diferente de normalizar_texto(), esta função
    serve para produzir texto que poderá aparecer
    posteriormente em uma postagem.
    """

    if not texto:
        return ""

    texto = str(texto)

    texto = unescape(
        texto
    )

    texto = re.sub(
        r"<[^>]+>",
        " ",
        texto,
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto,
    )

    return texto.strip()


def remover_boilerplate_rss(texto):
    """
    Remove alguns textos genéricos normalmente
    adicionados automaticamente por feeds RSS.
    """

    if not texto:
        return ""

    padroes = [
        r"\bRead more\b.*$",
        r"\bContinue reading\b.*$",
        r"\bThe post\b.*$",
        r"\bappeared first on\b.*$",
        r"\bSaiba mais\b.*$",
        r"\bLeia mais\b.*$",
    ]

    resultado = texto

    for padrao in padroes:
        resultado = re.sub(
            padrao,
            "",
            resultado,
            flags=re.IGNORECASE,
        )

    resultado = re.sub(
        r"\s+",
        " ",
        resultado,
    )

    return resultado.strip()


def limitar_texto(
    texto,
    limite=300,
):
    """
    Limita um texto sem cortar de forma
    muito agressiva quando ele é usado
    apenas como resumo editorial.
    """

    if not texto:
        return ""

    texto = texto.strip()

    if len(texto) <= limite:
        return texto

    texto_cortado = texto[:limite]

    ultima_posicao = texto_cortado.rfind(
        " "
    )

    if ultima_posicao > 0:
        texto_cortado = texto_cortado[:ultima_posicao]

    return texto_cortado.strip() + "..."


def dividir_em_frases(texto):
    """
    Divide uma descrição em frases utilizáveis.

    Não cria informação nova.
    Apenas reorganiza o conteúdo que já veio
    da fonte original.
    """

    if not texto:
        return []

    texto = limpar_texto_editorial(
        texto
    )

    texto = remover_boilerplate_rss(
        texto
    )

    if not texto:
        return []

    frases = re.split(
        r"(?<=[.!?])\s+",
        texto,
    )

    frases_limpas = []

    for frase in frases:
        frase = frase.strip()

        if not frase:
            continue

        if len(frase) < 25:
            continue

        frase = limitar_texto(
            frase,
            limite=260,
        )

        frases_limpas.append(
            frase
        )

    return frases_limpas


def nome_categoria_editorial(
    categoria
):
    """
    Converte a categoria interna para um nome
    mais natural para apresentação.
    """

    mapa = {
        "SQL SERVER": "SQL Server",
        "PYTHON": "Python",
        "C# / .NET": "C# / .NET",
        "AUTOMAÇÃO": "Automação",
        "DADOS": "Dados",
        "IA": "Inteligência Artificial",
        "AWS / CLOUD": "AWS / Cloud",
        "OUTROS": "Tecnologia",
    }

    return mapa.get(
        categoria,
        categoria or "Tecnologia",
    )


def gerar_tema_linkedin(
    assunto
):
    """
    Cria um tema editorial sem tentar traduzir
    tecnicamente a manchete.

    O objetivo neste estágio é deixar claro
    qual é o foco da futura postagem sem
    inventar interpretações sobre a notícia.
    """

    titulo = limpar_texto_editorial(
        assunto.get(
            "titulo",
            "",
        )
    )

    categoria = nome_categoria_editorial(
        assunto.get(
            "categoria",
            "OUTROS",
        )
    )

    if not titulo:
        return (
            f"Atualizações recentes em "
            f"{categoria}"
        )

    titulo = limitar_texto(
        titulo,
        limite=150,
    )

    return (
        f"{categoria}: pontos para acompanhar "
        f"sobre \"{titulo}\""
    )


def gerar_resumo_editorial(
    assunto
):
    """
    Produz um pequeno resumo usando apenas
    informações existentes na descrição RSS.
    """

    descricao = assunto.get(
        "descricao",
        "",
    )

    frases = dividir_em_frases(
        descricao
    )

    if frases:
        return limitar_texto(
            frases[0],
            limite=320,
        )

    descricao = limpar_texto_editorial(
        descricao
    )

    descricao = remover_boilerplate_rss(
        descricao
    )

    return limitar_texto(
        descricao,
        limite=320,
    )


def gerar_pontos_editoriais(
    assunto
):
    """
    Prepara pontos que posteriormente poderão
    alimentar o gerador da postagem.

    Sempre que possível utiliza fatos presentes
    na própria descrição RSS.

    Caso o feed tenha pouca informação, usa
    somente orientações editoriais genéricas,
    sem inventar detalhes técnicos.
    """

    descricao = assunto.get(
        "descricao",
        "",
    )

    categoria = nome_categoria_editorial(
        assunto.get(
            "categoria",
            "OUTROS",
        )
    )

    frases = dividir_em_frases(
        descricao
    )

    pontos = []

    for frase in frases[:2]:
        frase = limitar_texto(
            frase,
            limite=230,
        )

        if frase and frase not in pontos:
            pontos.append(
                frase
            )

    if len(pontos) == 0:
        pontos.append(
            "Acompanhar o que foi anunciado "
            "pela fonte oficial."
        )

        pontos.append(
            f"Entender como a novidade se "
            f"relaciona com {categoria}."
        )

        pontos.append(
            "Avaliar possíveis impactos práticos "
            "antes de aplicar o recurso."
        )

    elif len(pontos) == 1:
        pontos.append(
            f"Entender como a novidade se "
            f"relaciona com {categoria}."
        )

        pontos.append(
            "Avaliar possíveis impactos práticos "
            "antes de aplicar o recurso."
        )

    else:
        pontos.append(
            "Avaliar onde essa atualização pode "
            "ter aplicação prática."
        )

    return pontos[:3]


def preparar_conteudo_editorial(
    assunto
):
    """
    Centraliza a preparação editorial de uma
    notícia selecionada pelo robô.

    Não altera o título original e não cria
    fatos novos.
    """

    titulo_original = limpar_texto_editorial(
        assunto.get(
            "titulo",
            "",
        )
    )

    tema_linkedin = gerar_tema_linkedin(
        assunto
    )

    resumo_editorial = gerar_resumo_editorial(
        assunto
    )

    pontos_editoriais = gerar_pontos_editoriais(
        assunto
    )

    return {
        "titulo_original": titulo_original,
        "tema_linkedin": tema_linkedin,
        "resumo_editorial": resumo_editorial,
        "pontos_editoriais": pontos_editoriais,
    }


# ============================================================
# FILTRO + RANKING
# ============================================================

def filtrar_assuntos(
    assuntos
):
    assuntos_filtrados = []

    total_antigos = 0
    total_descartados = 0

    for assunto in assuntos:

        data_publicacao = assunto.get(
            "data_publicacao",
            "",
        )

        # ----------------------------------------------------
        # Filtro de atualidade.
        # ----------------------------------------------------

        if not assunto_e_atual(
            data_publicacao
        ):
            total_antigos += 1
            continue

        titulo = assunto.get(
            "titulo",
            "",
        )

        descricao = assunto.get(
            "descricao",
            "",
        )

        # ----------------------------------------------------
        # 1. Relevância técnica.
        # ----------------------------------------------------

        relevancia_tecnica = calcular_relevancia(
            titulo=titulo,
            descricao=descricao,
            data_publicacao=data_publicacao,
        )

        # ----------------------------------------------------
        # 2. Detectar categoria.
        # ----------------------------------------------------

        categoria = detectar_categoria(
            titulo=titulo,
            descricao=descricao,
            fonte=assunto.get(
                "fonte",
                "",
            ),
        )

        # ----------------------------------------------------
        # 3. Afinidade com perfil.
        # ----------------------------------------------------

        afinidade_perfil = calcular_afinidade_perfil(
            titulo=titulo,
            descricao=descricao,
            categoria=categoria,
        )

        # ----------------------------------------------------
        # 4. Pontuação final.
        # ----------------------------------------------------

        pontuacao_final = calcular_pontuacao_final(
            relevancia_tecnica=relevancia_tecnica,
            afinidade_perfil=afinidade_perfil,
        )

        classificacao = classificar_relevancia(
            pontuacao_final
        )

        if classificacao == "DESCARTAR":
            total_descartados += 1
            continue

        novo_assunto = assunto.copy()

        novo_assunto[
            "categoria"
        ] = categoria

        novo_assunto[
            "relevancia"
        ] = relevancia_tecnica

        novo_assunto[
            "relevancia_tecnica"
        ] = relevancia_tecnica

        novo_assunto[
            "afinidade_perfil"
        ] = afinidade_perfil

        novo_assunto[
            "pontuacao_final"
        ] = pontuacao_final

        novo_assunto[
            "classificacao"
        ] = classificacao

        novo_assunto[
            "dias_desde_publicacao"
        ] = calcular_dias_desde_publicacao(
            data_publicacao
        )

        # ----------------------------------------------------
        # 5. Preparar camada editorial.
        # ----------------------------------------------------

        conteudo_editorial = preparar_conteudo_editorial(
            novo_assunto
        )

        novo_assunto.update(
            conteudo_editorial
        )

        assuntos_filtrados.append(
            novo_assunto
        )

    # Agora o ranking usa a PONTUAÇÃO FINAL.
    assuntos_filtrados.sort(
        key=lambda item: item.get(
            "pontuacao_final",
            0,
        ),
        reverse=True,
    )

    print()

    print(
        f"🕒 Itens antigos descartados: "
        f"{total_antigos}"
    )

    print(
        f"🗑️ Itens com baixa relevância: "
        f"{total_descartados}"
    )

    return assuntos_filtrados


# ============================================================
# DUPLICADOS
# ============================================================

def remover_duplicados(
    assuntos
):
    assuntos_unicos = []

    titulos_vistos = set()

    for assunto in assuntos:

        titulo_normalizado = normalizar_texto(
            assunto.get(
                "titulo",
                "",
            )
        )

        if not titulo_normalizado:
            continue

        if titulo_normalizado in titulos_vistos:
            continue

        titulos_vistos.add(
            titulo_normalizado
        )

        assuntos_unicos.append(
            assunto
        )

    return assuntos_unicos


# ============================================================
# PESQUISA PRINCIPAL
# ============================================================

def pesquisar_assuntos():
    assuntos = buscar_assuntos_na_internet()

    assuntos = filtrar_assuntos(
        assuntos
    )

    assuntos = remover_duplicados(
        assuntos
    )

    return assuntos


# ============================================================
# EXIBIÇÃO
# ============================================================

def exibir_assuntos(
    assuntos
):
    print()

    print(
        "=" * 60
    )

    print(
        "ASSUNTOS ATUAIS DE TECNOLOGIA"
    )

    print(
        "=" * 60
    )

    if not assuntos:

        print()

        print(
            "📭 Nenhum assunto "
            "relevante encontrado."
        )

        return

    limite = min(
        len(assuntos),
        LIMITE_RESULTADOS,
    )

    for indice, assunto in enumerate(
        assuntos[:limite],
        start=1,
    ):
        print()

        print(
            f"[{indice}] "
            f"{assunto.get('titulo')}"
        )

        if assunto.get(
            "tema_linkedin"
        ):
            print(
                f"Tema LinkedIn: "
                f"{assunto.get('tema_linkedin')}"
            )

        print(
            f"Categoria: "
            f"{assunto.get('categoria', 'OUTROS')}"
        )

        print(
            f"Fonte: "
            f"{assunto.get('fonte', 'Não informada')}"
        )

        dias = assunto.get(
            "dias_desde_publicacao"
        )

        if dias is not None:

            if dias <= 0:
                texto_dias = "hoje"

            elif dias == 1:
                texto_dias = "há 1 dia"

            else:
                texto_dias = (
                    f"há {dias} dias"
                )

            print(
                f"Atualidade: "
                f"{texto_dias}"
            )

        if assunto.get(
            "data_publicacao"
        ):
            print(
                f"Publicado: "
                f"{assunto.get('data_publicacao')}"
            )

        print(
            f"Relevância técnica: "
            f"{assunto.get('relevancia_tecnica', 0)}%"
        )

        print(
            f"Afinidade com perfil: "
            f"{assunto.get('afinidade_perfil', 0)}%"
        )

        print(
            f"Pontuação final: "
            f"{assunto.get('pontuacao_final', 0)}%"
        )

        print(
            f"Classificação: "
            f"{assunto.get('classificacao')}"
        )

        if assunto.get(
            "url"
        ):
            print(
                f"Link: "
                f"{assunto.get('url')}"
            )

    print()

    print(
        f"Total de assuntos relevantes encontrados: "
        f"{len(assuntos)}"
    )

    if len(assuntos) > limite:

        print(
            f"Exibindo apenas os "
            f"{limite} mais relevantes."
        )


# ============================================================
# TESTE
# ============================================================

def executar_teste():
    print()

    print(
        "=" * 60
    )

    print(
        "ROBÔ LINKEDIN - "
        "PESQUISA DE ASSUNTOS ATUAIS"
    )

    print(
        "=" * 60
    )

    print()

    print(
        "Data da pesquisa:",
        datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        ),
    )

    print()

    print(
        "🌐 Iniciando pesquisa "
        "nas fontes configuradas..."
    )

    assuntos = pesquisar_assuntos()

    exibir_assuntos(
        assuntos
    )


if __name__ == "__main__":
    executar_teste()