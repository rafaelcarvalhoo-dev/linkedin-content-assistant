# ==========================================
# ROBÔ LINKEDIN CONTEÚDO V1
# GERADOR DE POSTAGENS
# ==========================================

import re

from perfil_profissional import (
    TECNOLOGIAS_PRINCIPAIS,
    TECNOLOGIAS_EM_ESTUDO,
)


# ============================================================
# NORMALIZAÇÃO DE CATEGORIAS
# ============================================================

def normalizar_categoria(categoria):

    mapa = {
        "SQL SERVER": "SQL Server",
        "PYTHON": "Python",
        "C# / .NET": ".NET",
        "AUTOMAÇÃO": "Automação",
        "DADOS": "Dados",
        "AWS / CLOUD": "AWS",
        "IA": "IA",
    }

    return mapa.get(
        categoria,
        categoria,
    )


# ============================================================
# UTILITÁRIOS
# ============================================================

def limpar_texto(texto):

    if not texto:
        return ""

    texto = str(texto).strip()

    texto = re.sub(
        r"\s+",
        " ",
        texto,
    )

    return texto


def normalizar_comparacao(texto):

    return limpar_texto(
        texto
    ).lower()


def textos_semelhantes(
    texto_1,
    texto_2,
):

    texto_1 = normalizar_comparacao(
        texto_1
    )

    texto_2 = normalizar_comparacao(
        texto_2
    )

    if not texto_1 or not texto_2:
        return False

    if texto_1 == texto_2:
        return True

    if (
        texto_1 in texto_2
        or texto_2 in texto_1
    ):
        return True

    return False


# ============================================================
# CONTEXTO PROFISSIONAL
# ============================================================

def identificar_contexto_profissional(
    categoria
):

    categoria_normalizada = normalizar_categoria(
        categoria
    )

    tecnologias_principais = [
        str(tecnologia).lower()
        for tecnologia
        in TECNOLOGIAS_PRINCIPAIS
    ]

    tecnologias_estudo = [
        str(tecnologia).lower()
        for tecnologia
        in TECNOLOGIAS_EM_ESTUDO
    ]

    categoria_lower = (
        categoria_normalizada.lower()
    )

    if categoria_lower in tecnologias_principais:

        return "experiencia"

    if categoria_lower in tecnologias_estudo:

        return "estudo"

    # Compatibilidades adicionais.

    if (
        categoria_normalizada == ".NET"
        and any(
            item in tecnologias_principais
            for item in [
                ".net",
                "c#",
                "csharp",
            ]
        )
    ):

        return "experiencia"

    if (
        categoria_normalizada == ".NET"
        and any(
            item in tecnologias_estudo
            for item in [
                ".net",
                "c#",
                "csharp",
            ]
        )
    ):

        return "estudo"

    return "interesse"


# ============================================================
# ABERTURA - POSTS TRADICIONAIS
# ============================================================

def gerar_abertura(
    tema,
    contexto
):

    categoria = normalizar_categoria(
        tema.get(
            "categoria",
            "Tecnologia",
        )
    )

    assunto = tema.get(
        "tema",
        "",
    )

    tipo = tema.get(
        "tipo",
        "",
    )

    if tipo == "aprendizado":

        return (
            f"Tenho estudado mais sobre "
            f"{categoria} e um ponto que "
            f"vale compartilhar é:"
        )

    if tipo == "dica_tecnica":

        return (
            f"Uma prática simples em "
            f"{categoria} pode fazer bastante "
            f"diferença no dia a dia:"
        )

    if tipo == "experiencia":

        return (
            f"Trabalhando com {categoria}, "
            f"um ponto que considero importante é:"
        )

    if contexto == "estudo":

        return (
            f"Nos meus estudos de {categoria}, "
            f"esse assunto apareceu como um "
            f"ponto interessante:"
        )

    return (
        f"Um assunto interessante relacionado "
        f"a {categoria}:"
    )


# ============================================================
# PONTOS - POSTS TRADICIONAIS
# ============================================================

def gerar_lista_pontos(
    pontos
):

    if not pontos:
        return ""

    linhas = []

    for ponto in pontos:

        ponto = limpar_texto(
            ponto
        )

        if not ponto:
            continue

        linhas.append(
            f"• {ponto}"
        )

    return "\n".join(
        linhas
    )


# ============================================================
# COMENTÁRIO FINAL - POSTS TRADICIONAIS
# ============================================================

def gerar_comentario_final(
    tema,
    contexto
):

    categoria = normalizar_categoria(
        tema.get(
            "categoria",
            "Tecnologia",
        )
    )

    tipo = tema.get(
        "tipo",
        "",
    )

    if tipo == "aprendizado":

        return (
            "Tenho buscado evoluir nesse assunto "
            "e entender cada vez mais como aplicar "
            "esses conceitos na prática."
        )

    if tipo == "dica_tecnica":

        return (
            "São detalhes simples, mas que ajudam "
            "a deixar o código e o processo mais "
            "seguros e organizados."
        )

    if contexto == "estudo":

        return (
            f"Continuo aprofundando meus estudos "
            f"em {categoria} e colocando esses "
            f"conceitos em prática."
        )

    return (
        "Esse tipo de conhecimento acaba fazendo "
        "diferença principalmente quando precisamos "
        "pensar em manutenção, qualidade e evolução "
        "das soluções."
    )


# ============================================================
# HASHTAGS
# ============================================================

def gerar_hashtags(
    categoria,
    tipo,
):

    categoria = normalizar_categoria(
        categoria
    )

    hashtags_por_categoria = {

        "SQL Server": [
            "#SQLServer",
            "#SQL",
            "#BancoDeDados",
            "#Dados",
        ],

        "Python": [
            "#Python",
            "#Automacao",
            "#Desenvolvimento",
            "#Tecnologia",
        ],

        "C#": [
            "#CSharp",
            "#DotNet",
            "#Desenvolvimento",
            "#Programacao",
        ],

        ".NET": [
            "#DotNet",
            "#CSharp",
            "#AspNetCore",
            "#Desenvolvimento",
        ],

        "AWS": [
            "#AWS",
            "#Cloud",
            "#CloudComputing",
            "#Tecnologia",
        ],

        "Cloud": [
            "#Cloud",
            "#CloudComputing",
            "#Tecnologia",
            "#Infraestrutura",
        ],

        "Automação": [
            "#Automacao",
            "#Python",
            "#Tecnologia",
            "#Produtividade",
        ],

        "Dados": [
            "#Dados",
            "#Data",
            "#BancoDeDados",
            "#Tecnologia",
        ],

        "IA": [
            "#InteligenciaArtificial",
            "#IA",
            "#Tecnologia",
            "#Inovacao",
        ],

        "Carreira": [
            "#Carreira",
            "#Tecnologia",
            "#DesenvolvimentoProfissional",
        ],
    }

    hashtags = hashtags_por_categoria.get(
        categoria,
        [
            "#Tecnologia",
            "#Desenvolvimento",
        ],
    )

    if tipo == "assunto_atual":

        if "#TechNews" not in hashtags:

            hashtags.append(
                "#TechNews"
            )

    return " ".join(
        hashtags
    )


# ============================================================
# FONTE DE ASSUNTO ATUAL
# ============================================================

def gerar_fonte_assunto_atual(
    tema
):

    fonte = limpar_texto(
        tema.get(
            "fonte",
            "",
        )
    )

    url = limpar_texto(
        tema.get(
            "url_fonte",
            "",
        )
    )

    if not fonte and not url:
        return ""

    linhas = []

    if fonte:

        linhas.append(
            f"🔎 Fonte: {fonte}"
        )

    if url:

        linhas.append(
            url
        )

    return "\n".join(
        linhas
    )


# ============================================================
# MOTOR EDITORIAL - ASSUNTOS ATUAIS
# PASSO 17.10.3
# ============================================================

def gerar_abertura_assunto_atual(
    tema
):

    categoria_original = tema.get(
        "categoria",
        "Tecnologia",
    )

    categoria = normalizar_categoria(
        categoria_original
    )

    aberturas = {

        ".NET": (
            "Uma atualização recente do "
            "ecossistema .NET chamou minha atenção."
        ),

        "SQL Server": (
            "Uma novidade recente envolvendo "
            "SQL Server merece atenção."
        ),

        "Python": (
            "Uma atualização recente no ecossistema "
            "Python trouxe um ponto interessante "
            "para acompanhar."
        ),

        "AWS": (
            "A AWS trouxe uma atualização recente "
            "que vale acompanhar."
        ),

        "Automação": (
            "Uma novidade relacionada a automação "
            "me chamou a atenção recentemente."
        ),

        "Dados": (
            "Uma atualização recente na área de "
            "dados trouxe um assunto interessante."
        ),

        "IA": (
            "Entre as novidades recentes em "
            "Inteligência Artificial, uma chamou "
            "minha atenção."
        ),
    }

    return aberturas.get(
        categoria,
        (
            "Uma atualização recente no mundo "
            "da tecnologia chamou minha atenção."
        ),
    )


def gerar_titulo_assunto_atual(
    tema
):

    tema_linkedin = limpar_texto(
        tema.get(
            "tema_linkedin",
            "",
        )
    )

    if tema_linkedin:

        return tema_linkedin

    return limpar_texto(
        tema.get(
            "tema",
            "",
        )
    )


def gerar_introducao_editorial(
    tema
):

    categoria = normalizar_categoria(
        tema.get(
            "categoria",
            "Tecnologia",
        )
    )

    resumo = limpar_texto(
        tema.get(
            "resumo_editorial",
            "",
        )
    )

    # Se o conteúdo veio do Motor de IA, o resumo já foi
    # produzido em português e validado a partir da fonte.
    # Nesse caso, usamos o resumo da IA diretamente.
    if tema.get("gerado_com_ia") and resumo:
        return resumo

    # No fallback local, não usamos automaticamente o resumo
    # porque ele pode vir em inglês pelo RSS.
    # Em vez disso, introduzimos o assunto de forma neutra.

    introducoes = {

        ".NET": (
            "O assunto envolve recursos do "
            "ecossistema C# e ASP.NET Core e mostra "
            "como a plataforma continua evoluindo "
            "em diferentes cenários de desenvolvimento."
        ),

        "SQL Server": (
            "A atualização está ligada ao ecossistema "
            "SQL Server e pode ser relevante para quem "
            "trabalha com bancos de dados Microsoft."
        ),

        "Python": (
            "A novidade faz parte do ecossistema "
            "Python e pode trazer reflexos para "
            "desenvolvimento e automação."
        ),

        "AWS": (
            "O anúncio faz parte da evolução dos "
            "serviços AWS e pode abrir novas "
            "possibilidades para aplicações em nuvem."
        ),

        "Automação": (
            "O assunto está relacionado à evolução "
            "de ferramentas e práticas de automação."
        ),

        "Dados": (
            "A atualização está relacionada ao "
            "ecossistema de dados e pode trazer "
            "novas possibilidades para projetos "
            "e arquiteturas."
        ),

        "IA": (
            "A novidade faz parte da rápida evolução "
            "das ferramentas de Inteligência Artificial "
            "e merece ser acompanhada."
        ),
    }

    return introducoes.get(
        categoria,
        (
            "O assunto faz parte das atualizações "
            "recentes do mercado de tecnologia e "
            "vale acompanhar sua evolução."
        ),
    )


def ponto_esta_em_ingles(
    texto
):

    if not texto:
        return False

    texto_lower = texto.lower()

    indicadores_ingles = [
        " learn ",
        " how ",
        " with ",
        " across ",
        " now ",
        " supports ",
        " support ",
        " available ",
        " using ",
        " use ",
        " new ",
        " for ",
        " from ",
        " and ",
        " work ",
        " generates ",
        " modernization ",
    ]

    texto_teste = (
        " "
        + texto_lower
        + " "
    )

    quantidade = 0

    for indicador in indicadores_ingles:

        if indicador in texto_teste:
            quantidade += 1

    return quantidade >= 2


def preparar_pontos_assunto_atual(
    tema
):

    categoria = normalizar_categoria(
        tema.get(
            "categoria",
            "Tecnologia",
        )
    )

    pontos_originais = tema.get(
        "pontos_editoriais",
        [],
    )

    if not isinstance(
        pontos_originais,
        list,
    ):

        pontos_originais = []

    pontos_validos = []

    for ponto in pontos_originais:

        ponto = limpar_texto(
            ponto
        )

        if not ponto:
            continue

        # Por enquanto não publicamos frases
        # claramente em inglês.
        if ponto_esta_em_ingles(
            ponto
        ):
            continue

        repetido = False

        for existente in pontos_validos:

            if textos_semelhantes(
                ponto,
                existente,
            ):

                repetido = True
                break

        if repetido:
            continue

        pontos_validos.append(
            ponto
        )

    pontos_categoria = {

        ".NET": [
            (
                "Entender como o recurso se integra "
                "ao ecossistema C# e ASP.NET Core."
            ),
            (
                "Avaliar os cenários em que a novidade "
                "pode simplificar a modelagem e o "
                "desenvolvimento de aplicações."
            ),
            (
                "Acompanhar como o recurso se comporta "
                "em APIs e aplicações .NET modernas."
            ),
        ],

        "SQL Server": [
            (
                "Entender quais cenários do SQL Server "
                "podem ser impactados pela atualização."
            ),
            (
                "Avaliar possíveis efeitos em "
                "performance, manutenção e segurança."
            ),
            (
                "Verificar a documentação oficial "
                "antes de aplicar a novidade em produção."
            ),
        ],

        "Python": [
            (
                "Entender quais mudanças chegam ao "
                "ecossistema Python."
            ),
            (
                "Avaliar como a novidade pode afetar "
                "projetos de desenvolvimento e automação."
            ),
            (
                "Testar o recurso em ambiente controlado "
                "antes de utilizá-lo em projetos reais."
            ),
        ],

        "AWS": [
            (
                "Entender qual problema o novo recurso "
                "ou atualização da AWS busca resolver."
            ),
            (
                "Avaliar onde ele pode fazer sentido "
                "dentro de uma arquitetura em nuvem."
            ),
            (
                "Analisar custo, integração e impacto "
                "antes de levar a novidade para produção."
            ),
        ],

        "Automação": [
            (
                "Entender como a novidade pode reduzir "
                "tarefas manuais."
            ),
            (
                "Avaliar ganhos de produtividade e "
                "confiabilidade no processo."
            ),
            (
                "Testar o recurso antes de incorporá-lo "
                "a uma automação existente."
            ),
        ],

        "Dados": [
            (
                "Entender onde a novidade se encaixa "
                "no fluxo de dados."
            ),
            (
                "Avaliar impactos em qualidade, "
                "processamento e manutenção."
            ),
            (
                "Identificar aplicações práticas antes "
                "de adotar o recurso."
            ),
        ],

        "IA": [
            (
                "Entender o que realmente mudou "
                "com a atualização."
            ),
            (
                "Avaliar aplicações práticas além "
                "do anúncio inicial."
            ),
            (
                "Considerar segurança, custo e "
                "qualidade antes da adoção."
            ),
        ],
    }

    pontos_fallback = pontos_categoria.get(
        categoria,
        [
            (
                "Entender o que mudou com "
                "a atualização."
            ),
            (
                "Avaliar onde a novidade pode "
                "ser aplicada na prática."
            ),
            (
                "Acompanhar a documentação oficial "
                "antes de utilizar o recurso."
            ),
        ],
    )

    for ponto in pontos_fallback:

        if len(pontos_validos) >= 3:
            break

        repetido = False

        for existente in pontos_validos:

            if textos_semelhantes(
                ponto,
                existente,
            ):

                repetido = True
                break

        if not repetido:

            pontos_validos.append(
                ponto
            )

    return pontos_validos[:3]


def gerar_comentario_final_assunto_atual(
    tema
):

    # Quando a IA foi usada com sucesso, aproveitamos a
    # conclusão editorial gerada por ela. O texto fixo abaixo
    # permanece como fallback do motor local.
    conclusao_ia = limpar_texto(
        tema.get(
            "conclusao_editorial",
            "",
        )
    )

    if tema.get("gerado_com_ia") and conclusao_ia:
        return conclusao_ia

    categoria = normalizar_categoria(
        tema.get(
            "categoria",
            "Tecnologia",
        )
    )

    finais = {

        ".NET": (
            "Para quem trabalha ou estuda C# e .NET, "
            "acompanhar esse tipo de evolução ajuda "
            "a entender para onde o ecossistema está "
            "caminhando e quais recursos podem fazer "
            "sentido nos próximos projetos."
        ),

        "SQL Server": (
            "Para quem trabalha com SQL Server, "
            "acompanhar essas atualizações é importante "
            "para avaliar novas possibilidades sem "
            "perder de vista estabilidade e segurança."
        ),

        "Python": (
            "Para quem utiliza Python no desenvolvimento "
            "ou em automações, vale acompanhar essas "
            "mudanças e entender o que realmente pode "
            "ser aproveitado no dia a dia."
        ),

        "AWS": (
            "No ecossistema AWS, novos recursos aparecem "
            "com frequência. O mais importante é entender "
            "onde eles realmente agregam valor antes de "
            "adicioná-los a uma arquitetura."
        ),

        "Automação": (
            "Em automação, nem toda novidade precisa ser "
            "adotada imediatamente. Primeiro vale entender "
            "o ganho real e onde ela pode tornar o processo "
            "mais confiável."
        ),

        "Dados": (
            "Na área de dados, acompanhar as novidades é "
            "importante, mas sempre avaliando qualidade, "
            "manutenção e aplicação prática."
        ),

        "IA": (
            "Com a velocidade das novidades em IA, "
            "separar anúncio de aplicação prática se "
            "torna cada vez mais importante."
        ),
    }

    return finais.get(
        categoria,
        (
            "Acompanhar novas tecnologias é importante, "
            "mas entender onde elas realmente resolvem "
            "problemas continua sendo o principal."
        ),
    )


def gerar_post_assunto_atual(
    tema
):

    abertura = gerar_abertura_assunto_atual(
        tema
    )

    titulo = gerar_titulo_assunto_atual(
        tema
    )

    introducao = gerar_introducao_editorial(
        tema
    )

    pontos = preparar_pontos_assunto_atual(
        tema
    )

    lista_pontos = gerar_lista_pontos(
        pontos
    )

    fechamento = gerar_comentario_final_assunto_atual(
        tema
    )

    hashtags = gerar_hashtags(
        categoria=tema.get(
            "categoria",
            "Tecnologia",
        ),
        tipo="assunto_atual",
    )

    fonte = gerar_fonte_assunto_atual(
        tema
    )

    partes = [
        abertura,
        "",
        f"📌 {titulo}",
        "",
        introducao,
    ]

    if lista_pontos:

        partes.extend(
            [
                "",
                "Alguns pontos que vale acompanhar:",
                "",
                lista_pontos,
            ]
        )

    partes.extend(
        [
            "",
            fechamento,
            "",
            hashtags,
        ]
    )

    if fonte:

        partes.extend(
            [
                "",
                fonte,
            ]
        )

    return "\n".join(
        partes
    )


# ============================================================
# GERADOR PRINCIPAL
# ============================================================

def gerar_post(
    tema
):

    tipo = tema.get(
        "tipo",
        "",
    )

    # ========================================================
    # ASSUNTO ATUAL
    # ========================================================

    if tipo == "assunto_atual":

        return gerar_post_assunto_atual(
            tema
        )

    # ========================================================
    # POSTS NORMAIS
    # ========================================================

    categoria = tema.get(
        "categoria",
        "Tecnologia",
    )

    assunto = tema.get(
        "tema",
        "",
    )

    pontos = tema.get(
        "pontos",
        [],
    )

    contexto = identificar_contexto_profissional(
        categoria
    )

    abertura = gerar_abertura(
        tema=tema,
        contexto=contexto,
    )

    lista_pontos = gerar_lista_pontos(
        pontos
    )

    comentario_final = gerar_comentario_final(
        tema=tema,
        contexto=contexto,
    )

    hashtags = gerar_hashtags(
        categoria=categoria,
        tipo=tipo,
    )

    partes = [
        abertura,
        "",
        f"📌 {assunto}",
    ]

    if lista_pontos:

        partes.extend(
            [
                "",
                lista_pontos,
            ]
        )

    partes.extend(
        [
            "",
            comentario_final,
            "",
            hashtags,
        ]
    )

    return "\n".join(
        partes
    )