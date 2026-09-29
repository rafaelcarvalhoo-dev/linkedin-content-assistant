\# LinkedIn Content Assistant



\*\*Python + OpenAI + RSS + Content Intelligence\*\*



Assistente de conteúdo executado no terminal para transformar assuntos de fontes oficiais em rascunhos de publicações para o LinkedIn. Combina pesquisa via RSS, ranking de relevância, seleção humana, geração editorial com OpenAI e histórico local para apoiar uma rotina de produção de conteúdo.



A V1 mantém a decisão editorial com o usuário: o sistema prepara o texto e o Prompt Visual V2; a revisão, a geração da imagem em ferramenta externa e a publicação no LinkedIn são manuais.



\## Funcionalidades



\- Pesquisa de assuntos atuais nos feeds RSS das fontes oficiais configuradas.

\- Filtragem de assuntos, classificação por categoria e remoção de duplicatas na pesquisa.

\- Ranking com relevância técnica, afinidade com o perfil e pontuação final.

\- Exibição de título, fonte, data e link de origem para apoiar a seleção manual.

\- Geração de tema, resumo, pontos editoriais e conclusão com OpenAI.

\- Composição do post com estrutura editorial, referência à fonte e hashtags.

\- Continuidade com a camada editorial local quando o motor de IA está indisponível.

\- Salvamento dos textos em `posts/gerados/` e registro no histórico local.

\- Controle anti-repetição com janela configurada de \*\*30 dias\*\*.

\- Criação do \*\*Prompt Visual V2\*\*, associado à publicação para uso manual no ChatGPT.

\- Consulta de publicações geradas, prompts visuais, assuntos atuais e histórico pelo terminal.



\## Arquitetura e fluxo



```text

RSS / fontes oficiais

&#x20;       |

&#x20;       v

Coleta, filtros e ranking de relevância

&#x20;       |

&#x20;       v

Seleção manual do assunto e confirmação da geração

&#x20;       |

&#x20;       v

OpenAI: elaboração editorial

(camada editorial local em caso de indisponibilidade)

&#x20;       |

&#x20;       v

Verificação anti-repetição no histórico — 30 dias

&#x20;       |

&#x20;       v

Composição do post para LinkedIn

&#x20;       |

&#x20;       v

Salvamento em posts/gerados/ e registro no histórico

&#x20;       |

&#x20;       v

Prompt Visual V2 associado ao registro

&#x20;       |

&#x20;       v

Revisão humana → geração manual da imagem → publicação manual

```



O histórico é consultado antes de salvar uma nova publicação e atualizado após a geração. A checagem de repetição ocorre depois da etapa editorial com IA; portanto, um tema bloqueado ainda pode ter consumido uma chamada à API.



O status interno `gerado` indica que o conteúdo foi criado localmente. Ele não confirma uma publicação no LinkedIn.



\## Estrutura do projeto



Os nove módulos ativos da V1 têm as seguintes responsabilidades:



| Módulo | Responsabilidade |

| --- | --- |

| `main.py` | Ponto de entrada, menu interativo e coordenação do fluxo de pesquisa, geração, registro e consulta. |

| `config.py` | Configurações gerais, incluindo a janela anti-repetição e o modo de depuração. |

| `perfil\_profissional.py` | Configuração do perfil usada na afinidade dos assuntos e na personalização editorial. |

| `pesquisar\_assuntos.py` | Coleta RSS, tratamento dos conteúdos, filtros, categorias, pontuação, ranking e preparação editorial local. |

| `motor\_ia.py` | Integração com OpenAI para gerar o conteúdo editorial e retornar metadados da geração. |

| `gerar\_post.py` | Montagem e formatação do texto final para LinkedIn. |

| `fila\_posts.py` | Preparação das pastas, nomes dos arquivos e salvamento das publicações geradas. |

| `historico.py` | Persistência e consulta do histórico, controle de repetição e associação do briefing visual. |

| `gerar\_briefing\_imagem.py` | Construção do briefing e do Prompt Visual V2 com orientações de composição e identidade visual. |



```text

.

├── main.py

├── config.py

├── perfil\_profissional.py

├── pesquisar\_assuntos.py

├── motor\_ia.py

├── gerar\_post.py

├── fila\_posts.py

├── historico.py

├── gerar\_briefing\_imagem.py

├── requirements.txt

├── .env.example

├── .gitignore

└── README.md

```



Durante o uso, `posts/gerados/` armazena os textos e `dados/` mantém os dados e o histórico local. Esses conteúdos não fazem parte do repositório público. A estrutura acima não inclui arquivos pessoais, exemplos reais de posts nem registros do histórico.



\## Tecnologias e ambiente de referência



| Tecnologia | Versão informada no ambiente do projeto | Uso |

| --- | --- | --- |

| Python | 3.14.2 | Execução da aplicação |

| `openai` | 3.14.0 | Integração com a API OpenAI |

| `feedparser` | 6.0.14 | Leitura de feeds RSS |



As versões das dependências diretas estão fixadas no `requirements.txt`:



```text

openai==3.14.0

feedparser==6.0.14

```



O projeto também utiliza recursos da biblioteca padrão do Python para arquivos, JSON, datas e tratamento de texto. As versões acima descrevem o ambiente informado para a V1; outras combinações não estão validadas neste documento.



\## Instalação no Windows / PowerShell



\### 1. Preparar o ambiente



Instale o Python 3.14.2 com acesso pelo terminal e obtenha os arquivos do projeto por download ou clonagem do repositório. Abra o PowerShell na pasta que contém `main.py` e `requirements.txt`.



Confirme a versão:



```powershell

python --version

```



É necessário acesso à internet para consultar os feeds e usar a API, além de uma chave OpenAI com acesso ao modelo configurado no projeto.



\### 2. Criar e ativar o ambiente virtual



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



Se o PowerShell bloquear a ativação por política de execução, permita scripts apenas na sessão atual e tente novamente:



```powershell

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

.\\.venv\\Scripts\\Activate.ps1

```



Em um computador gerenciado, respeite as políticas da organização. A presença de `(.venv)` no início do prompt indica que o ambiente está ativo.



\### 3. Instalar as dependências



Com o ambiente virtual ativo:



```powershell

pip install -r requirements.txt

```



\### 4. Configurar `OPENAI\_API\_KEY`



A aplicação utiliza a variável de ambiente `OPENAI\_API\_KEY`. Para disponibilizá-la apenas na sessão atual sem escrever a chave literalmente no comando nem exibi-la na tela:



```powershell

$chaveOpenAI = Read-Host "Informe sua chave OpenAI" -AsSecureString

$env:OPENAI\_API\_KEY = \[System.Net.NetworkCredential]::new('', $chaveOpenAI).Password

Remove-Variable chaveOpenAI

```



Execute a aplicação nessa mesma janela. Ao abrir uma nova sessão, configure a variável novamente. Como alternativa, cadastre `OPENAI\_API\_KEY` nas variáveis de ambiente do usuário no Windows e abra um novo PowerShell.



O `.env.example` documenta somente o nome da variável com um valor fictício:



```dotenv

OPENAI\_API\_KEY=sua\_chave\_openai\_aqui

```



Esse arquivo é um modelo público. A V1 usa a variável de ambiente e não inclui carregamento automático de `.env`; copiar ou renomear o modelo não substitui a configuração acima.



\### 5. Executar



Na raiz do projeto, com o ambiente virtual ativo:



```powershell

python main.py

```



Para sair do ambiente virtual ao terminar:



```powershell

deactivate

```



\## Como usar



| Opção | Ação |

| --- | --- |

| `1` | Criar nova publicação: pesquisar, selecionar um assunto e confirmar a geração. |

| `2` | Consultar as publicações geradas, exibindo até os 20 registros mais recentes. |

| `3` | Selecionar uma publicação e visualizar seu prompt de imagem. |

| `4` | Consultar os assuntos atuais sem iniciar a geração do post. |

| `5` | Consultar o histórico local. |

| `0` | Encerrar a aplicação. |



Na criação de uma publicação, confira a fonte e a pontuação do assunto antes de confirmar. Após a geração, revise o texto salvo em `posts/gerados/`. Se quiser uma imagem, copie o Prompt Visual V2 e utilize-o manualmente no ChatGPT. Revise o resultado e publique o conteúdo pelo próprio LinkedIn.



O Prompt Visual V2 é uma instrução textual para criação de imagem. O aplicativo não gera nem publica a imagem automaticamente. Se a criação do briefing falhar, o post já registrado permanece disponível.



\## Segurança e versionamento



O `.gitignore` mantém fora do versionamento:



| Grupo | Itens ignorados |

| --- | --- |

| Ambientes virtuais | `.venv/`, `venv/`, `env/` |

| Cache Python | `\_\_pycache\_\_/`, `\*.py\[cod]`, `\*$py.class` |

| Dados e histórico | `dados/` |

| Publicações geradas | `posts/` |

| Imagens locais | `imagens/`, `IMAGENS IA/` |

| Segredos e configuração local | `.env`, `.env.\*`, com exceção de `.env.example` |

| Configurações de editor | `.vscode/`, `.idea/` |

| Temporários | `\*.tmp`, `\*.log`, `\*.bak` |

| Arquivos do sistema | `.DS\_Store`, `Thumbs.db`, `desktop.ini` |



Mantenha a chave fora do código, do README, de capturas de tela e dos commits. O `.env.example` deve conter apenas o marcador fictício. Antes de publicar o repositório, confira os arquivos selecionados para commit e substitua configurações pessoais em `perfil\_profissional.py` por valores genéricos apropriados à distribuição.



O `.gitignore` não remove arquivos já rastreados nem apaga segredos do histórico do Git. Se uma chave for exposta, revogue-a e substitua-a.



A etapa de IA envia à API os dados usados na elaboração editorial. Não acrescente informações confidenciais ao conteúdo enviado. Posts, histórico e imagens devem permanecer locais; este README não distribui esses arquivos.



\## Escopo e limitações da V1



\- \*\*Aplicação local de terminal:\*\* o fluxo é interativo e voltado ao uso individual, sem interface web ou serviço em segundo plano.

\- \*\*Publicação manual:\*\* não há automação de login, integração de publicação com a API do LinkedIn ou agendamento automático no fluxo ativo.

\- \*\*Imagem externa:\*\* a V1 entrega o prompt visual; a geração e o uso da imagem são etapas manuais.

\- \*\*Dependência das fontes:\*\* disponibilidade, atualização e qualidade dos assuntos dependem dos feeds configurados. Um feed pode retornar conteúdo incompleto ou nenhum resultado relevante.

\- \*\*Ranking por regras:\*\* pontuações orientam a escolha editorial; não representam validação factual nem garantia de alcance ou engajamento.

\- \*\*Revisão humana necessária:\*\* o texto gerado pode conter imprecisões. Confira os fatos e a fonte antes de publicar.

\- \*\*API sujeita a disponibilidade e cobrança:\*\* a geração depende da chave, do acesso ao modelo e dos limites da conta. O fallback local mantém o fluxo, mas pode produzir conteúdo menos elaborado.

\- \*\*Anti-repetição local:\*\* a janela de 30 dias usa os registros e critérios de status do histórico. A comparação do tema é textual, sem garantia de detectar assuntos semanticamente iguais com títulos diferentes. Remover o histórico elimina essa referência.

\- \*\*Sem sincronização com o LinkedIn:\*\* os registros locais não comprovam que um post foi publicado. A compatibilidade de leitura com status antigos não reativa fluxos legados de aprovação ou agendamento.



\## Autoria



Desenvolvido por \*\*Rafael Carvalho\*\*.



Projeto de portfólio que reúne Python, integração com IA, consumo de RSS, organização modular e apoio à produção editorial com decisão humana.



