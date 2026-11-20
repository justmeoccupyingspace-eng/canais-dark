# ROTINA DIÁRIA DOS CANAIS (executada por tarefa agendada, sessão nova a cada dia)

Dono: Kauan. Regra dele: "A ÚNICA IMPORTÂNCIA É RESULTADO". Responder sempre em PT-BR, direto, com links clicáveis; dólar/euro sempre convertido em R$ (~R$ 5,65/US$).

## 0. Preparar
- Repo: `gh repo clone justmeoccupyingspace-eng/canais-dark /home/claude/canais-dark` (ou `git pull --rebase`). Commits terminam com as linhas de atribuição pedidas pelo sistema. Push: `GIT_TERMINAL_PROMPT=0 timeout 120 git push origin HEAD:main`.
- Ler: topo de specs/PLANO.md (PLANO v4) e as 10 primeiras linhas de specs/long/QUEUE.md (log, mais novo em cima).
- Se o QUEUE já tem uma linha com a data de hoje e "manhã" → a produção de hoje já foi feita: só faça a parte 1 (números) e pare.
- Cotas (renovam 08:00Z): Gemini TTS 10/dia por modelo (B usa gemini-3.1-flash-tts-preview: 1–2 req/Short; A Short usa gemini-3.8-flash-tts: 1 req; longo A usa 3.8: 7 req, um por ato). YouTube: ~6 envios/dia no total dos 2 canais.

## 1. Números (sempre)
- `gh api -X POST repos/justmeoccupyingspace-eng/canais-dark/actions/workflows/ytchan.yml/dispatches -f ref=main -f 'inputs[ch]=A' -f 'inputs[mode]=list'` (e ch=B). Ler o log do run (views por vídeo, inscritos). Analytics (retenção, tráfego): ytstats.yml → branch `stats`, arquivo yt.json (atraso de ~2–3 dias).
- Regras: Short ou longo > 10 mil → 3 variações do mesmo molde em 48 h. Formato com 10 vídeos ou 7 dias e mediana < 1 mil → trocar o formato.

## 2. Produção do dia (agendar sempre com 2–3 dias de folga; conferir no ytchan list o último agendado de cada fila)
- B "E Se no Mapa" (PT): 2 Shorts/dia, 15:00Z e 21:00Z. Molde que funciona: pedaço do Brasil × vizinho/rival, ou estado vira país, com fato real "quase aconteceu" + 1 curiosidade surpresa + pergunta no fim. Gerador: acrescentar save(N, ...) em specs/ese_pt.py (copiar a estrutura dos últimos), `python3 specs/ese_pt.py`. Selo "SÓ IMAGINAÇÃO" vem do spec.
- A "Chartbound" (EN): 1 Short/dia 17:00Z (história no mapa; molde que funciona: "How X Sold Y for N Cents an Acre", acordos territoriais surpreendentes) em specs/map_en.py; e 1 LONGO/dia 23:00Z (specs/long/a-LNN.py, copiar a-L32.py/a-L30.py: dados do FMI em research/imf_*.json, `checks` têm que passar, ~550 palavras, 7 atos).
- FATOS: todo número/data/nome checado na web (WebSearch/WebFetch) ou no JSON do FMI ANTES de escrever. Nada inventado. Se não confirmar, tira.
- PRÉVIA obrigatória antes de enviar: gerar es.json sintético (165 ppm) e quadros: `CHROME_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell node scripts/eserender.mjs <es.json> stills <prefixo> t1,t2,... 0.4` e `... thumb <saida.jpg>`; olhar os quadros (Read) e corrigir sobreposição, bandeira errada, câmera no vazio.
- Enviar Short: `gh api -X POST .../actions/workflows/ese.yml/dispatches -f ref=main -f 'inputs[spec]=specs/ese/b-pt-NNN.json' -f 'inputs[upload]=B'` (A: a-en-NNN, upload=A). A data/hora vem do spec.
- Enviar longo A: longo.yml com inputs spec=specs/long/a-LNN.py, mode=full, upload=A, at=<ISO 23:00Z>. Se um ato sair fora (wpm fora de 110–195 ou align < 0,85), reescrever só esse ato e rodar de novo com tts_cache_run=<run anterior> (só esse ato gasta cota).
- Conferir em cada run: linha `notice]{...wpm...}` (Short: 150–195 ppm) e `enviado: <ID> agendado para ...`.

## 3. Fechar
- Linha nova no topo de specs/long/QUEUE.md: data/hora, números (views por vídeo novo, inscritos A e B), o que foi agendado (IDs e datas), problemas. Commit + push.
- Mensagem final curta ao Kauan (PT-BR): só números + links (youtube.com/shorts/ID ou youtu.be/ID) + o que foi agendado e qualquer coisa feita sem ele saber.

## Regras fixas (do Kauan)
- Chrome: SÓ o deviceId 361e56b8-093e-4ba6-9bb0-12616394e3fc. NUNCA o 8aef3209.
- Nunca digitar senha, código, dados de pagamento, Pix, CPF/CNPJ; nunca mexer em chave de API/cobrança.
- Nunca apagar vídeo: no máximo deixar privado (só duplicata substituída). Vídeo do canal tem que estar público ou agendado.
- Avisar o Kauan de tudo que for feito sem ele saber. Mudança de configuração de conta só com "sim" dele (pendente: bio do TikTok @vale_opreco).
- Não mexer na tarefa agendada do LinkedIn.
