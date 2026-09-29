# ==========================================
# ROBÔ LINKEDIN CONTEÚDO V1 FINAL
# Fluxo: pesquisa -> IA -> post -> prompt visual -> publicação manual
# ==========================================

from config import DIAS_ANTI_REPETICAO, MODO_DEBUG
from perfil_profissional import NOME
from gerar_post import gerar_post
from motor_ia import gerar_editorial_com_ia
from historico import (
    carregar_historico,
    registrar_post,
    tema_tem_pendente,
    tema_usado_recentemente,
    salvar_briefing_imagem,
)
from fila_posts import (
    garantir_estrutura_posts,
    salvar_post_gerado,
)
from gerar_briefing_imagem import gerar_briefing_imagem
from pesquisar_assuntos import pesquisar_assuntos, exibir_assuntos


def exibir_cabecalho():
    print()
    print("=" * 60)
    print("🤖 ROBÔ LINKEDIN CONTEÚDO - V1 FINAL")
    print("=" * 60)
    print(f"Usuário: {NOME}")
    print(f"Anti-repetição: {DIAS_ANTI_REPETICAO} dias")
    print("Fluxo: pesquisar → gerar post → gerar prompt visual → publicar manualmente")
    print("=" * 60)


def exibir_menu():
    print()
    print("1 - 🚀 Criar nova publicação")
    print("2 - 📚 Ver publicações geradas")
    print("3 - 🎨 Ver prompt da imagem")
    print("4 - 📰 Ver assuntos atuais")
    print("5 - 📊 Ver histórico")
    print("0 - Sair")
    print()


def selecionar_registro(registros):
    if not registros:
        return None

    escolha = input("Digite o número da postagem: ").strip()

    if not escolha.isdigit():
        print()
        print("❌ Opção inválida.")
        return None

    indice = int(escolha)

    if indice < 1 or indice > len(registros):
        print()
        print("❌ Postagem não encontrada.")
        return None

    return registros[indice - 1]


def exibir_historico():
    historico = carregar_historico()

    print()
    print("=" * 60)
    print("HISTÓRICO DE POSTAGENS")
    print("=" * 60)

    if not historico:
        print()
        print("Nenhum registro encontrado.")
        return

    for indice, registro in enumerate(reversed(historico), start=1):
        status = str(registro.get("status", "desconhecido")).upper()

        print()
        print(f"[{indice}] {status}")
        print(f"Categoria: {registro.get('categoria')}")
        print(f"Tema: {registro.get('tema')}")
        print(f"Data criação: {registro.get('data')}")
        print(f"ID: {registro.get('id', 'registro antigo')}")

    print()
    print(f"Total de registros: {len(historico)}")


def ver_prompt_imagem():
    print()
    print("=" * 60)
    print("PROMPT DA IMAGEM PARA O CHATGPT")
    print("=" * 60)

    historico = carregar_historico()
    registros = []

    # Mantemos leitura dos status antigos para compatibilidade
    # com o histórico já existente, sem reativar o fluxo legado.
    status_compativeis = {
        "gerado",
        "pendente",
        "aprovado",
        "agendado",
        "publicado",
    }

    for registro in historico:
        status_post = str(registro.get("status", "")).lower()
        briefing = registro.get("briefing_imagem")

        if status_post not in status_compativeis:
            continue

        if not isinstance(briefing, dict):
            continue

        prompt = briefing.get("prompt_chatgpt") or briefing.get("prompt")

        if prompt:
            registros.append(registro)

    if not registros:
        print()
        print("📭 Nenhuma postagem possui prompt visual disponível.")
        print()
        print("Gere primeiro uma publicação pela opção 1.")
        return

    print()
    print("Selecione a postagem cujo prompt você deseja visualizar.")
    print()

    for indice, registro in enumerate(registros, start=1):
        print(f"[{indice}] {registro.get('categoria')}")
        print(f"Tema: {registro.get('tema')}")
        print(f"Post: {str(registro.get('status', '')).upper()}")
        print()

    registro = selecionar_registro(registros)

    if registro is None:
        return

    briefing = registro.get("briefing_imagem", {})
    prompt = briefing.get("prompt_chatgpt") or briefing.get("prompt")

    if not prompt:
        print()
        print("❌ O briefing desta postagem não possui um prompt válido.")
        return

    print()
    print("=" * 60)
    print("🤖 PROMPT PARA O CHATGPT")
    print("=" * 60)
    print()
    print(prompt)
    print()
    print("=" * 60)
    print()
    print("📋 Copie o conteúdo acima e envie para o ChatGPT gerar a imagem.")


def visualizar_assuntos_atuais():
    print()
    print("=" * 60)
    print("ASSUNTOS ATUAIS")
    print("=" * 60)
    print()
    print("🌐 Pesquisando assuntos atuais nas fontes configuradas...")

    assuntos = pesquisar_assuntos()

    if not assuntos:
        print()
        print("📭 Nenhum assunto relevante foi encontrado.")
        return

    exibir_assuntos(assuntos)

    print()
    print("ℹ️ Para criar um post, volte ao menu e use a opção 1.")


def pesquisar_assuntos_atuais():
    print()
    print("=" * 60)
    print("PESQUISAR ASSUNTOS ATUAIS")
    print("=" * 60)
    print()
    print("🌐 Pesquisando assuntos atuais nas fontes configuradas...")

    assuntos = pesquisar_assuntos()

    if not assuntos:
        print()
        print("📭 Nenhum assunto relevante foi encontrado.")
        return

    exibir_assuntos(assuntos)
    limite = min(len(assuntos), 15)

    print()
    print("=" * 60)
    print("SELECIONAR ASSUNTO")
    print("=" * 60)
    print()
    print("Escolha um assunto para visualizar os detalhes.")
    print("Digite 0 para voltar ao menu.")
    print()

    escolha = input("Digite o número do assunto: ").strip()

    if escolha == "0":
        print()
        print("ℹ️ Voltando ao menu.")
        return

    if not escolha.isdigit():
        print()
        print("❌ Opção inválida.")
        return

    indice = int(escolha)

    if indice < 1 or indice > limite:
        print()
        print("❌ Assunto não encontrado.")
        return

    assunto = assuntos[indice - 1]

    titulo_original = assunto.get("titulo_original") or assunto.get("titulo", "")
    categoria = assunto.get("categoria", "OUTROS")
    fonte = assunto.get("fonte", "Não informada")
    url_fonte = assunto.get("url", "")
    data_publicacao = assunto.get("data_publicacao", "")
    relevancia_tecnica = assunto.get("relevancia_tecnica", 0)
    afinidade_perfil = assunto.get("afinidade_perfil", 0)
    pontuacao_final = assunto.get("pontuacao_final", 0)
    classificacao = assunto.get("classificacao", "")

    tema_linkedin = assunto.get("tema_linkedin")
    resumo_editorial = assunto.get("resumo_editorial", "")
    pontos_editoriais = assunto.get("pontos_editoriais", [])
    conclusao_editorial = ""

    if not tema_linkedin:
        tema_linkedin = f"{categoria}: {titulo_original}"

    if not isinstance(pontos_editoriais, list):
        pontos_editoriais = []

    print()
    print("=" * 60)
    print("ASSUNTO SELECIONADO")
    print("=" * 60)
    print()
    print(f"📰 Título original: {titulo_original}")
    print()
    print(f"✍️ Tema atual: {tema_linkedin}")
    print(f"📂 Categoria: {categoria}")
    print(f"🌐 Fonte: {fonte}")

    if data_publicacao:
        print(f"📅 Publicado: {data_publicacao}")

    print(f"🔧 Relevância técnica: {relevancia_tecnica}%")
    print(f"🎯 Afinidade com perfil: {afinidade_perfil}%")
    print(f"⭐ Pontuação final: {pontuacao_final}%")
    print(f"🏆 Classificação: {classificacao}")

    if url_fonte:
        print()
        print(f"🔗 Fonte original: {url_fonte}")

    print()
    print("-" * 60)
    print()
    print("1 - Gerar postagem com IA")
    print("0 - Voltar ao menu")
    print()

    opcao = input("Escolha uma opção: ").strip()

    if opcao == "0":
        print()
        print("ℹ️ Operação cancelada.")
        return

    if opcao != "1":
        print()
        print("❌ Opção inválida.")
        return

    resumo_fonte = (
        assunto.get("descricao")
        or assunto.get("resumo")
        or resumo_editorial
        or ""
    )

    resultado_ia = gerar_editorial_com_ia(
        titulo_original=titulo_original,
        resumo_original=resumo_fonte,
        categoria=categoria,
        fonte=fonte,
        url_fonte=url_fonte,
    )

    usou_ia = False
    modelo_ia = ""
    tokens_entrada = 0
    tokens_saida = 0
    tokens_total = 0

    if resultado_ia:
        tema_linkedin = resultado_ia.get("tema_linkedin", tema_linkedin)
        resumo_editorial = resultado_ia.get("resumo_editorial", resumo_editorial)
        pontos_editoriais = resultado_ia.get("pontos_editoriais", pontos_editoriais)
        conclusao_editorial = resultado_ia.get("conclusao_editorial", "")
        modelo_ia = resultado_ia.get("modelo_ia", "")
        tokens_entrada = resultado_ia.get("tokens_entrada", 0)
        tokens_saida = resultado_ia.get("tokens_saida", 0)
        tokens_total = resultado_ia.get("tokens_total", 0)
        usou_ia = True

        print()
        print("=" * 60)
        print("🤖 CONTEÚDO EDITORIAL GERADO PELA IA")
        print("=" * 60)
        print()
        print(f"📌 Tema LinkedIn: {tema_linkedin}")
        print()
        print("📝 Resumo:")
        print(resumo_editorial)
        print()
        print("🔹 Pontos editoriais:")

        for numero, ponto in enumerate(pontos_editoriais, start=1):
            print(f"{numero}. {ponto}")

        if conclusao_editorial:
            print()
            print("💬 Conclusão:")
            print(conclusao_editorial)

        print()
        print(f"📊 Tokens utilizados: {tokens_total}")

    else:
        print()
        print("=" * 60)
        print("⚠️ MOTOR DE IA INDISPONÍVEL")
        print("=" * 60)
        print()
        print("O robô continuará utilizando a camada editorial local.")

    if tema_tem_pendente(tema_linkedin):
        print()
        print("⚠️ Já existe uma publicação registrada com este tema.")
        return

    if tema_usado_recentemente(
        tema=tema_linkedin,
        dias_anti_repeticao=DIAS_ANTI_REPETICAO,
    ):
        print()
        print("⚠️ Este tema foi utilizado recentemente.")
        print(f"🔒 Anti-repetição: {DIAS_ANTI_REPETICAO} dias.")
        return

    pontos = []

    if resumo_editorial:
        pontos.append(resumo_editorial)

    for ponto in pontos_editoriais:
        if ponto and ponto not in pontos:
            pontos.append(ponto)

    if conclusao_editorial and conclusao_editorial not in pontos:
        pontos.append(conclusao_editorial)

    if not pontos:
        pontos = [
            "Acompanhar o anúncio feito pela fonte oficial.",
            f"Entender como a novidade se relaciona com {categoria}.",
            "Avaliar possíveis aplicações práticas dessa atualização.",
        ]

    pontos = pontos[:5]

    tema = {
        "categoria": categoria,
        "tema": tema_linkedin,
        "nivel": "atualidade",
        "tipo": "assunto_atual",
        "pontos": pontos,
        "fonte": fonte,
        "url_fonte": url_fonte,
        "titulo_original": titulo_original,
        "tema_linkedin": tema_linkedin,
        "resumo_editorial": resumo_editorial,
        "pontos_editoriais": pontos_editoriais,
        "conclusao_editorial": conclusao_editorial,
        "data_publicacao_fonte": data_publicacao,
        "relevancia_tecnica": relevancia_tecnica,
        "afinidade_perfil": afinidade_perfil,
        "pontuacao_final": pontuacao_final,
        "classificacao_assunto": classificacao,
        "gerado_com_ia": usou_ia,
        "modelo_ia": modelo_ia,
        "tokens_entrada": tokens_entrada,
        "tokens_saida": tokens_saida,
        "tokens_total": tokens_total,
    }

    print()
    print("=" * 60)
    print("GERANDO POSTAGEM")
    print("=" * 60)

    post = gerar_post(tema)

    print()
    print("📝 POSTAGEM GERADA")
    print("-" * 60)
    print()
    print(post)
    print()
    print("-" * 60)

    caminho = salvar_post_gerado(
        tema=tema,
        post=post,
    )

    registro = registrar_post(
        tema=tema,
        post=post,
        status="gerado",
        arquivo=caminho,
    )

    print()
    print("=" * 60)
    print("✅ POSTAGEM CRIADA E REGISTRADA")
    print("=" * 60)
    print()
    print("📥 Status interno: GERADO")
    print(f"🆔 ID: {registro['id']}")
    print(f"📂 Categoria: {categoria}")
    print(f"✍️ Tema: {tema_linkedin}")
    print(f"🌐 Fonte: {fonte}")

    if usou_ia:
        print(f"🤖 IA: {modelo_ia}")
        print(f"📊 Tokens: {tokens_total}")
    else:
        print("🛡️ Motor editorial: LOCAL")

    if url_fonte:
        print(f"🔗 URL: {url_fonte}")

    print(f"📄 Arquivo: {caminho}")

    briefing = None

    try:
        briefing = gerar_briefing_imagem(registro)

        salvo_briefing = salvar_briefing_imagem(
            id_registro=registro["id"],
            briefing=briefing,
        )

        if not salvo_briefing:
            briefing = None

    except Exception as erro:
        print()
        print("⚠️ O post foi registrado, mas o prompt visual não pôde ser criado.")
        if MODO_DEBUG:
            print(f"Detalhes: {erro}")

    print()
    print("=" * 60)
    print("✅ PUBLICAÇÃO PRONTA")
    print("=" * 60)
    print()
    print("📝 POST LINKEDIN")
    print("-" * 60)
    print()
    print(post)
    print()

    if briefing:
        prompt_visual = (
            briefing.get("prompt_chatgpt")
            or briefing.get("prompt")
            or ""
        )

        print("-" * 60)
        print("🎨 PROMPT PARA GERAR A IMAGEM NO CHATGPT")
        print("-" * 60)
        print()
        print(prompt_visual)
        print()
        print("-" * 60)
        print("📋 Copie o prompt acima e envie para o ChatGPT gerar a imagem.")
    else:
        print("⚠️ Prompt visual indisponível para esta publicação.")

    print()
    print("💾 O post foi registrado no histórico para evitar repetição.")
    print("👤 A publicação no LinkedIn será feita manualmente por você.")


def ver_publicacoes_geradas():
    print()
    print("=" * 60)
    print("PUBLICAÇÕES GERADAS")
    print("=" * 60)

    historico = carregar_historico()

    if not historico:
        print()
        print("📭 Nenhuma publicação encontrada.")
        return

    registros = list(reversed(historico[-20:]))

    for indice, registro in enumerate(registros, start=1):
        print()
        print(f"[{indice}] {registro.get('categoria', 'Sem categoria')}")
        print(f"Tema: {registro.get('tema', 'Sem tema')}")
        print(f"Status interno: {str(registro.get('status', '')).upper()}")
        print(f"Data: {registro.get('data', 'não informada')}")
        print(f"ID: {registro.get('id', 'não informado')}")

    print()
    print("ℹ️ Exibindo até as 20 publicações mais recentes.")


def main():
    garantir_estrutura_posts()
    exibir_cabecalho()

    while True:
        exibir_menu()

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            pesquisar_assuntos_atuais()

        elif opcao == "2":
            ver_publicacoes_geradas()

        elif opcao == "3":
            ver_prompt_imagem()

        elif opcao == "4":
            visualizar_assuntos_atuais()

        elif opcao == "5":
            exibir_historico()

        elif opcao == "0":
            print()
            print("👋 Encerrando Robô LinkedIn Conteúdo.")
            print("Até a próxima!")
            break

        else:
            print()
            print("❌ Opção inválida.")


if __name__ == "__main__":
    main()
