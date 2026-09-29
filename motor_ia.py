import json
import os

from openai import OpenAI


# ============================================================
# CONFIGURAÇÕES DO MOTOR DE IA
# ============================================================

MODELO_IA = "gpt-5.6-luna"

MAX_OUTPUT_TOKENS = 900


# ============================================================
# CLIENTE OPENAI
# ============================================================

def obter_cliente():
    """
    Cria o cliente da OpenAI utilizando a variável de ambiente
    OPENAI_API_KEY.

    A chave nunca deve ficar escrita diretamente no código.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY não encontrada nas variáveis de ambiente."
        )

    return OpenAI(api_key=api_key)


# ============================================================
# PROMPT EDITORIAL
# ============================================================

def montar_prompt_editorial(
    titulo_original,
    resumo_original,
    categoria,
    fonte,
    url_fonte="",
):
    """
    Monta o conteúdo enviado para a IA.

    REGRA PRINCIPAL:
    A IA deve trabalhar somente com as informações fornecidas
    pela fonte selecionada.
    """

    titulo_original = (titulo_original or "").strip()
    resumo_original = (resumo_original or "").strip()
    categoria = (categoria or "Tecnologia").strip()
    fonte = (fonte or "Fonte não informada").strip()
    url_fonte = (url_fonte or "").strip()

    return f"""
Você é o motor editorial de um projeto que cria conteúdo
profissional para LinkedIn em português do Brasil.

Sua tarefa é transformar uma notícia ou atualização técnica
em material editorial claro, profissional e natural.

IMPORTANTE:

- Utilize SOMENTE as informações fornecidas abaixo.
- NÃO invente funcionalidades, números, datas ou fatos.
- NÃO complemente o conteúdo com conhecimento externo.
- NÃO diga que algo aconteceu se isso não estiver explícito.
- Preserve nomes técnicos como C#, ASP.NET Core, SQL Server,
  Python, AWS, .NET, APIs e nomes de produtos.
- Escreva em português brasileiro natural.
- Evite linguagem publicitária exagerada.
- Evite clickbait.
- Não traduza nomes oficiais de tecnologias.
- O conteúdo deve ser útil para profissionais e estudantes
  de tecnologia.
- Caso as informações fornecidas sejam insuficientes para
  afirmar algum detalhe, seja conservador.

DADOS DA FONTE

Categoria:
{categoria}

Título original:
{titulo_original}

Resumo/conteúdo fornecido pela fonte:
{resumo_original}

Fonte:
{fonte}

URL:
{url_fonte}

Gere exatamente:

1. Um tema/título para LinkedIn em português.
2. Um resumo editorial curto em português.
3. Exatamente 3 pontos técnicos relevantes.
4. Uma conclusão curta indicando por que vale acompanhar
   esse assunto.

Não inclua a URL dentro dos textos gerados.
Não crie hashtags.
Não mencione informações que não estejam presentes
nos dados fornecidos.
""".strip()


# ============================================================
# SCHEMA DA RESPOSTA
# ============================================================

SCHEMA_EDITORIAL = {
    "type": "object",
    "properties": {
        "tema_linkedin": {
            "type": "string"
        },
        "resumo_editorial": {
            "type": "string"
        },
        "pontos_editoriais": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "minItems": 3,
            "maxItems": 3
        },
        "conclusao_editorial": {
            "type": "string"
        }
    },
    "required": [
        "tema_linkedin",
        "resumo_editorial",
        "pontos_editoriais",
        "conclusao_editorial"
    ],
    "additionalProperties": False
}


# ============================================================
# MOTOR EDITORIAL
# ============================================================

def gerar_editorial_com_ia(
    titulo_original,
    resumo_original,
    categoria,
    fonte,
    url_fonte="",
):
    """
    Envia UM assunto selecionado para a OpenAI.

    Retorna um dicionário estruturado ou None em caso de erro.
    """

    try:
        cliente = obter_cliente()

        prompt = montar_prompt_editorial(
            titulo_original=titulo_original,
            resumo_original=resumo_original,
            categoria=categoria,
            fonte=fonte,
            url_fonte=url_fonte,
        )

        print()
        print("🤖 Enviando assunto selecionado para o Motor de IA...")
        print(f"Modelo: {MODELO_IA}")

        resposta = cliente.responses.create(
            model=MODELO_IA,

            reasoning={
                "effort": "none"
            },

            input=[
                {
                    "role": "developer",
                    "content": (
                        "Responda exclusivamente de acordo com "
                        "as informações fornecidas pelo usuário. "
                        "Não invente fatos."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

            text={
                "format": {
                    "type": "json_schema",
                    "name": "editorial_linkedin",
                    "strict": True,
                    "schema": SCHEMA_EDITORIAL,
                }
            },

            max_output_tokens=MAX_OUTPUT_TOKENS,

            store=False,
        )

        texto_resposta = resposta.output_text

        if not texto_resposta:
            print("❌ A IA não retornou conteúdo.")
            return None

        resultado = json.loads(texto_resposta)

        # ----------------------------------------------------
        # Validação mínima
        # ----------------------------------------------------

        campos_obrigatorios = [
            "tema_linkedin",
            "resumo_editorial",
            "pontos_editoriais",
            "conclusao_editorial",
        ]

        for campo in campos_obrigatorios:
            if campo not in resultado:
                raise ValueError(
                    f"Campo obrigatório ausente: {campo}"
                )

        pontos = resultado.get("pontos_editoriais", [])

        if not isinstance(pontos, list) or len(pontos) != 3:
            raise ValueError(
                "A IA não retornou exatamente 3 pontos editoriais."
            )

        # ----------------------------------------------------
        # Metadados locais
        # ----------------------------------------------------

        resultado["titulo_original"] = titulo_original
        resultado["categoria"] = categoria
        resultado["fonte"] = fonte
        resultado["url_fonte"] = url_fonte
        resultado["modelo_ia"] = MODELO_IA

        # ----------------------------------------------------
        # Uso de tokens
        # ----------------------------------------------------

        if resposta.usage:
            resultado["tokens_entrada"] = (
                resposta.usage.input_tokens or 0
            )

            resultado["tokens_saida"] = (
                resposta.usage.output_tokens or 0
            )

            resultado["tokens_total"] = (
                resposta.usage.total_tokens or 0
            )

        print("✅ Motor de IA executado com sucesso.")

        return resultado

    except Exception as erro:
        print()
        print("❌ ERRO NO MOTOR DE IA")
        print(f"Detalhes: {erro}")
        print()
        print(
            "O restante do robô poderá continuar utilizando "
            "o motor editorial local."
        )

        return None


# ============================================================
# EXIBIÇÃO DO RESULTADO
# ============================================================

def exibir_editorial(resultado):
    if not resultado:
        return

    print()
    print("=" * 70)
    print("RESULTADO DO MOTOR DE IA")
    print("=" * 70)

    print()
    print("📌 TEMA LINKEDIN")
    print(resultado["tema_linkedin"])

    print()
    print("📝 RESUMO")
    print(resultado["resumo_editorial"])

    print()
    print("🔹 PONTOS EDITORIAIS")

    for ponto in resultado["pontos_editoriais"]:
        print(f"• {ponto}")

    print()
    print("💬 CONCLUSÃO")
    print(resultado["conclusao_editorial"])

    print()
    print("🔎 FONTE")
    print(resultado["fonte"])

    if resultado.get("url_fonte"):
        print(resultado["url_fonte"])

    print()
    print("📊 CONSUMO DA CHAMADA")

    print(
        f"Entrada: {resultado.get('tokens_entrada', 0)} tokens"
    )

    print(
        f"Saída:   {resultado.get('tokens_saida', 0)} tokens"
    )

    print(
        f"Total:   {resultado.get('tokens_total', 0)} tokens"
    )

    print()
    print("=" * 70)


# ============================================================
# TESTE ISOLADO
# ============================================================

def executar_teste():
    """
    Faz UMA chamada real à API.

    Esse teste utiliza o assunto que já apareceu anteriormente
    durante os testes do Robô LinkedIn.
    """

    print()
    print("=" * 70)
    print("TESTE ISOLADO - MOTOR DE IA")
    print("=" * 70)

    resultado = gerar_editorial_com_ia(
        titulo_original=(
            "Use C# unions and closed hierarchies "
            "in ASP.NET Core"
        ),

        resumo_original=(
            "An update from the Microsoft .NET Blog about "
            "C# unions and closed hierarchies in ASP.NET Core."
        ),

        categoria="C# / .NET",

        fonte="Microsoft .NET Blog",

        url_fonte=(
            "https://devblogs.microsoft.com/dotnet/"
            "unions-and-closed-hierarchies-in-aspnetcore/"
        ),
    )

    if resultado:
        exibir_editorial(resultado)

    else:
        print()
        print("⚠️ O teste não foi concluído.")


# ============================================================
# EXECUÇÃO DIRETA
# ============================================================

if __name__ == "__main__":
    executar_teste()