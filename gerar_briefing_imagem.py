# ==========================================
# ROBÔ LINKEDIN CONTEÚDO V1
# BRIEFING VISUAL V2
# ==========================================

import re


# --------------------------------------------------
# IDENTIDADE VISUAL
# --------------------------------------------------

IDENTIDADE_CATEGORIAS = {
    "SQL Server": {
        "titulo": "SQL SERVER",
        "familia": "dados",
        "elementos": [
            "banco de dados",
            "editor de consultas SQL",
            "servidor de banco de dados",
            "estrutura de tabelas e dados",
        ],
    },

    "Python": {
        "titulo": "PYTHON",
        "familia": "desenvolvimento",
        "elementos": [
            "código Python",
            "ambiente de desenvolvimento",
            "terminal",
            "automação",
        ],
    },

    "AWS": {
        "titulo": "AWS",
        "familia": "cloud",
        "elementos": [
            "infraestrutura em nuvem",
            "arquitetura cloud",
            "serviços AWS",
            "ambiente tecnológico",
        ],
    },

    "AWS / CLOUD": {
        "titulo": "AWS / CLOUD",
        "familia": "cloud",
        "elementos": [
            "infraestrutura em nuvem",
            "arquitetura cloud",
            "serviços AWS",
            "ambiente tecnológico",
        ],
    },

    "C#": {
        "titulo": "C#",
        "familia": "desenvolvimento",
        "elementos": [
            "código C#",
            "IDE profissional",
            "desenvolvimento backend",
            "arquitetura de software",
        ],
    },

    ".NET": {
        "titulo": ".NET",
        "familia": "desenvolvimento",
        "elementos": [
            "código C#",
            "aplicação .NET",
            "backend",
            "arquitetura de software",
        ],
    },

    "C# / .NET": {
        "titulo": "C# / .NET",
        "familia": "desenvolvimento",
        "elementos": [
            "código C#",
            "aplicação .NET",
            "IDE profissional",
            "arquitetura de software",
        ],
    },

    "Dados": {
        "titulo": "DADOS",
        "familia": "dados",
        "elementos": [
            "dados estruturados",
            "pipeline de dados",
            "banco de dados",
            "validação de informações",
        ],
    },

    "DADOS": {
        "titulo": "DADOS",
        "familia": "dados",
        "elementos": [
            "dados estruturados",
            "pipeline de dados",
            "banco de dados",
            "validação de informações",
        ],
    },

    "Cloud": {
        "titulo": "CLOUD",
        "familia": "cloud",
        "elementos": [
            "infraestrutura em nuvem",
            "servidores",
            "arquitetura cloud",
            "serviços distribuídos",
        ],
    },

    "Automação": {
        "titulo": "AUTOMAÇÃO",
        "familia": "automacao",
        "elementos": [
            "fluxo automatizado",
            "código",
            "processos conectados",
            "ambiente de desenvolvimento",
        ],
    },

    "AUTOMAÇÃO": {
        "titulo": "AUTOMAÇÃO",
        "familia": "automacao",
        "elementos": [
            "fluxo automatizado",
            "código",
            "processos conectados",
            "ambiente de desenvolvimento",
        ],
    },

    "IA": {
        "titulo": "INTELIGÊNCIA ARTIFICIAL",
        "familia": "ia",
        "elementos": [
            "inteligência artificial",
            "fluxos inteligentes",
            "dados",
            "ambiente tecnológico",
        ],
    },
}


IDENTIDADE_PADRAO = {
    "titulo": "TECNOLOGIA",
    "familia": "tecnologia",
    "elementos": [
        "programação",
        "tecnologia",
        "código",
        "ambiente profissional",
    ],
}


# --------------------------------------------------
# REGRAS DE ASSUNTO
# --------------------------------------------------

REGRAS_ASSUNTOS = [
    {
        "nome": "testes_unitarios",
        "palavras": [
            "teste unitário",
            "testes unitários",
            "unit test",
            "unit tests",
            "testing",
        ],
        "composicao": "DEV_WORKSPACE",
        "conceito": (
            "ambiente profissional de desenvolvimento mostrando "
            "código sendo validado por testes automatizados"
        ),
        "elementos": [
            "notebook ou monitor exibindo código",
            "código C# ou código relacionado ao tema",
            "painel de testes com indicadores de sucesso",
            "checkmarks representando testes aprovados",
            "fluxo visual entre desenvolvimento e validação",
        ],
        "tags": [
            "unit testing",
            "quality assurance",
            "software development",
            "automated tests",
        ],
    },

    {
        "nome": "selenium",
        "palavras": [
            "selenium",
            "automação web",
            "automacao web",
            "browser automation",
        ],
        "composicao": "AUTOMATION_FLOW",
        "conceito": (
            "automação de navegador executada por código "
            "em um ambiente profissional de desenvolvimento"
        ),
        "elementos": [
            "navegador moderno",
            "código Python",
            "fluxo automatizado",
            "terminal de desenvolvimento",
            "elementos indicando execução automática",
        ],
        "tags": [
            "selenium",
            "python automation",
            "browser automation",
            "workflow",
        ],
    },

    {
        "nome": "api",
        "palavras": [
            "api",
            "apis",
            "rest",
            "endpoint",
            "endpoints",
        ],
        "composicao": "SYSTEM_ARCHITECTURE",
        "conceito": (
            "arquitetura moderna de software mostrando "
            "comunicação entre aplicação, API e serviços"
        ),
        "elementos": [
            "aplicação",
            "API central",
            "requisições e respostas",
            "serviços conectados",
            "código backend",
        ],
        "tags": [
            "REST API",
            "backend",
            "software architecture",
            "integration",
        ],
    },

    {
        "nome": "sql_join",
        "palavras": [
            "inner join",
            "left join",
            "right join",
            "full join",
            "join",
        ],
        "composicao": "DATA_SYSTEM",
        "conceito": (
            "consulta SQL conectando conjuntos de dados "
            "e demonstrando relacionamento entre tabelas"
        ),
        "elementos": [
            "editor SQL",
            "duas ou mais tabelas relacionadas",
            "query SQL",
            "linhas conectando dados",
            "resultado de consulta",
        ],
        "tags": [
            "SQL Server",
            "SQL query",
            "database",
            "data relationship",
        ],
    },

    {
        "nome": "banco_dados",
        "palavras": [
            "sql server",
            "database",
            "banco de dados",
            "query",
            "tabela temporária",
            "tabelas temporárias",
            "delete",
        ],
        "composicao": "DATA_SYSTEM",
        "conceito": (
            "ambiente profissional de banco de dados "
            "com consultas e estruturas de dados"
        ),
        "elementos": [
            "servidor de banco de dados",
            "editor SQL",
            "tabelas estruturadas",
            "query em execução",
            "dados organizados",
        ],
        "tags": [
            "SQL Server",
            "database",
            "T-SQL",
            "data",
        ],
    },

    {
        "nome": "aws_s3",
        "palavras": [
            "amazon s3",
            "aws s3",
            " s3 ",
        ],
        "composicao": "CLOUD_ARCHITECTURE",
        "conceito": (
            "armazenamento de objetos em nuvem conectado "
            "a aplicações e serviços"
        ),
        "elementos": [
            "cloud computing",
            "armazenamento de objetos",
            "arquivos digitais",
            "aplicação conectada à nuvem",
            "infraestrutura AWS",
        ],
        "tags": [
            "AWS",
            "Amazon S3",
            "cloud storage",
            "cloud computing",
        ],
    },

    {
        "nome": "cloud",
        "palavras": [
            "aws",
            "cloud",
            "nuvem",
            "lambda",
            "ec2",
            "rds",
        ],
        "composicao": "CLOUD_ARCHITECTURE",
        "conceito": (
            "arquitetura tecnológica em nuvem conectando "
            "aplicações, serviços e infraestrutura"
        ),
        "elementos": [
            "infraestrutura cloud",
            "serviços conectados",
            "aplicação",
            "servidores",
            "fluxo de dados",
        ],
        "tags": [
            "cloud computing",
            "AWS",
            "cloud architecture",
            "infrastructure",
        ],
    },

    {
        "nome": "inteligencia_artificial",
        "palavras": [
            "inteligência artificial",
            "inteligencia artificial",
            "generative ai",
            "genai",
            "agentic ai",
            "agente de ia",
            "agentes de ia",
            "machine learning",
        ],
        "composicao": "AI_SYSTEM",
        "conceito": (
            "sistema inteligente processando informações "
            "e interagindo com aplicações e dados"
        ),
        "elementos": [
            "fluxo de inteligência artificial",
            "dados",
            "aplicações conectadas",
            "processamento inteligente",
            "interface tecnológica",
        ],
        "tags": [
            "artificial intelligence",
            "AI",
            "data",
            "automation",
        ],
    },
]


# --------------------------------------------------
# FUNÇÕES AUXILIARES
# --------------------------------------------------

def normalizar_texto(texto):
    texto = str(texto or "")
    texto = texto.strip()
    texto = re.sub(r"\s+", " ", texto)
    return texto


def deve_ter_imagem(registro):
    """
    Posts aprovados ou agendados podem
    receber briefing visual.
    """

    status = str(
        registro.get("status", "")
    ).lower()

    return status in [
        "aprovado",
        "agendado",
    ]


def criar_subtitulo(tema):
    """
    V2:
    Não corta mais o tema com "...".

    O tema completo fica disponível no briefing.
    O gerador de imagem/ChatGPT decide a melhor
    hierarquia visual.
    """

    return normalizar_texto(tema)


def obter_identidade(categoria):
    categoria = normalizar_texto(categoria)

    return IDENTIDADE_CATEGORIAS.get(
        categoria,
        IDENTIDADE_PADRAO,
    )


def detectar_assuntos(tema, categoria):
    """
    Detecta regras específicas usando categoria + tema.

    Pode retornar mais de uma regra.
    Isso permite, por exemplo:
    AWS + .NET + testes unitários.
    """

    texto = (
        f" {normalizar_texto(categoria)} "
        f"{normalizar_texto(tema)} "
    ).lower()

    encontrados = []

    for regra in REGRAS_ASSUNTOS:

        encontrou = any(
            palavra.lower() in texto
            for palavra in regra["palavras"]
        )

        if encontrou:
            encontrados.append(regra)

    return encontrados


def remover_duplicados(lista):
    resultado = []

    for item in lista:
        if item not in resultado:
            resultado.append(item)

    return resultado


def escolher_composicao(regras, familia):
    """
    Prioriza a primeira regra específica detectada.
    Caso não exista, escolhe pela família.
    """

    if regras:
        return regras[0]["composicao"]

    composicoes = {
        "dados": "DATA_SYSTEM",
        "desenvolvimento": "DEV_WORKSPACE",
        "cloud": "CLOUD_ARCHITECTURE",
        "automacao": "AUTOMATION_FLOW",
        "ia": "AI_SYSTEM",
        "tecnologia": "EDITORIAL_TECH",
    }

    return composicoes.get(
        familia,
        "EDITORIAL_TECH",
    )


def gerar_conceito_visual(
    categoria,
    tema,
    identidade,
    regras,
):
    if regras:

        conceitos = [
            regra["conceito"]
            for regra in regras[:2]
        ]

        return " integrado a ".join(conceitos)

    return (
        f"representação visual profissional sobre {tema}, "
        f"com foco em {categoria} e desenvolvimento "
        "de tecnologia em ambiente corporativo"
    )


def gerar_elementos_visuais(
    identidade,
    regras,
):
    elementos = []

    for regra in regras[:3]:
        elementos.extend(
            regra["elementos"]
        )

    elementos.extend(
        identidade["elementos"]
    )

    return remover_duplicados(
        elementos
    )[:10]


def gerar_tags_visuais(
    categoria,
    regras,
):
    tags = [categoria]

    for regra in regras[:3]:
        tags.extend(
            regra["tags"]
        )

    return remover_duplicados(
        tags
    )[:12]


def gerar_texto_destaque(
    categoria,
    tema,
    regras,
):
    """
    Texto curto opcional para aparecer na arte.

    Não usa automaticamente o tema inteiro como
    uma manchete gigantesca.
    """

    if regras:

        nome = regras[0]["nome"]

        textos = {
            "testes_unitarios": "TESTES UNITÁRIOS",
            "selenium": "AUTOMAÇÃO WEB",
            "api": "APIs & BACKEND",
            "sql_join": "SQL JOINS",
            "banco_dados": "SQL SERVER",
            "aws_s3": "AMAZON S3",
            "cloud": "CLOUD",
            "inteligencia_artificial": "IA",
        }

        if nome in textos:
            return textos[nome]

    identidade = obter_identidade(
        categoria
    )

    return identidade["titulo"]


# --------------------------------------------------
# GERAR PROMPT VISUAL V2
# --------------------------------------------------

def gerar_prompt_visual(
    categoria,
    tema,
    conceito_visual,
    composicao,
    elementos,
    texto_destaque,
    tags_visuais,
):
    elementos_texto = "; ".join(
        elementos
    )

    tags_texto = ", ".join(
        tags_visuais
    )

    prompt = f"""
Crie uma imagem quadrada premium para uma publicação profissional no LinkedIn.

TEMA DA PUBLICAÇÃO:
{tema}

CATEGORIA:
{categoria}

CONCEITO VISUAL:
{conceito_visual}

DIREÇÃO DE ARTE:
Criar uma composição visual tecnológica sofisticada e específica para este assunto.
A imagem não deve parecer um template genérico de rede social.
O assunto da publicação deve ser reconhecível pelos elementos visuais da cena.

COMPOSIÇÃO SUGERIDA:
{composicao}

ELEMENTOS VISUAIS IMPORTANTES:
{elementos_texto}

ESTILO:
Visual profissional, premium, moderno e tecnológico.
Composição editorial contemporânea.
Ambiente corporativo de tecnologia.
Boa profundidade visual.
Iluminação profissional.
Detalhes realistas e sofisticados.
Contraste elegante.
Design limpo, mas visualmente interessante.
A imagem deve parecer criada especificamente para esta publicação.

TEXTO NA IMAGEM:
Usar pouco texto.
Texto principal opcional: "{texto_destaque}".
Não colocar o texto completo da publicação na imagem.
Não cortar palavras.
Não usar reticências para esconder partes do título.
Não criar parágrafos longos dentro da arte.

IDENTIDADE:
Manter uma linguagem visual consistente com um perfil profissional de tecnologia,
programação, dados, automação, cloud e desenvolvimento de software.
A identidade pode ser consistente entre publicações, mas a composição,
o cenário e os elementos principais devem variar conforme o assunto.

EVITAR:
Template genérico.
Mesmo layout usado em todas as publicações.
Grandes blocos de texto.
Excesso de ícones soltos.
Visual infantil.
Poluição visual.
Elementos sem relação com o tema.
Texto ilegível.
Palavras cortadas.
Logotipos inventados ou deformados.
Interfaces com textos aleatórios sem sentido.

TAGS VISUAIS DE REFERÊNCIA:
{tags_texto}

FORMATO:
1080x1080, proporção 1:1, otimizada para o feed do LinkedIn.
""".strip()

    return prompt


# --------------------------------------------------
# GERAR BRIEFING COMPLETO
# --------------------------------------------------

def gerar_briefing_imagem(registro):
    """
    Gera o Briefing Visual V2.

    Mantém os campos da V1 para compatibilidade
    e adiciona campos novos para o fluxo manual
    de geração da imagem pelo ChatGPT.
    """

    categoria = normalizar_texto(
        registro.get(
            "categoria",
            "Tecnologia",
        )
    )

    tema = normalizar_texto(
        registro.get(
            "tema",
            "Conteúdo de tecnologia",
        )
    )

    identidade = obter_identidade(
        categoria
    )

    regras = detectar_assuntos(
        tema,
        categoria,
    )

    composicao = escolher_composicao(
        regras,
        identidade["familia"],
    )

    conceito_visual = gerar_conceito_visual(
        categoria,
        tema,
        identidade,
        regras,
    )

    elementos = gerar_elementos_visuais(
        identidade,
        regras,
    )

    tags_visuais = gerar_tags_visuais(
        categoria,
        regras,
    )

    texto_destaque = gerar_texto_destaque(
        categoria,
        tema,
        regras,
    )

    prompt = gerar_prompt_visual(
        categoria=categoria,
        tema=tema,
        conceito_visual=conceito_visual,
        composicao=composicao,
        elementos=elementos,
        texto_destaque=texto_destaque,
        tags_visuais=tags_visuais,
    )

    briefing = {
        # ----------------------------------
        # CAMPOS COMPATÍVEIS COM A V1
        # ----------------------------------

        "titulo": identidade["titulo"],

        "subtitulo": criar_subtitulo(
            tema
        ),

        "categoria": categoria,

        "tema": tema,

        "formato": "quadrado",

        "estilo": (
            "visual profissional, premium, moderno, "
            "tecnológico, sofisticado e específico "
            "para o assunto"
        ),

        "elementos": elementos,

        "prompt": prompt,

        # ----------------------------------
        # NOVOS CAMPOS DA V2
        # ----------------------------------

        "versao_briefing": "2.0",

        "familia_visual": identidade[
            "familia"
        ],

        "composicao": composicao,

        "conceito_visual": conceito_visual,

        "elementos_principais": elementos,

        "tags_visuais": tags_visuais,

        "texto_destaque": texto_destaque,

        "assuntos_detectados": [
            regra["nome"]
            for regra in regras
        ],

        # Campo explícito para facilitar
        # o uso manual com o ChatGPT.
        "prompt_chatgpt": prompt,
    }

    return briefing