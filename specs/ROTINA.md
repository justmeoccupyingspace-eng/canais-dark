# ROTINA DIÁRIA DOS CANAIS (executada por tarefa agendada, sessão nova a cada dia)

Dono: Kauan. Regra dele: "A ÚNICA IMPORTÂNCIA É RESULTADO". Responder sempre em PT-BR, direto, com links clicáveis; dólar/euro sempre convertido em R$ (~R$ 5,65/US$).

## 0. Preparar
- Repo: `gh repo clone justmeoccupyingspace-eng/canais-dark /home/claude/canais-dark` (ou `git pull --rebase`). Commits terminam com as linhas de atribuição pedidas pelo sistema. Push: `GIT_TERMINAL_PROMPT=0 timeout 120 git push origin HEAD:main`.
- DINHEIRO PRIMEIRO: ler specs/DINHEIRO.md (frente única que paga; tem prioridade sobre volume dos canais quando faltar cota ou tempo).
- Ler: topo de specs/PLANO.md (v5.1 / v5) e as 10 primeiras linhas de specs/long/QUEUE.md (log, mais novo em cima).
- Se o QUEUE já tem uma linha com a data de hoje e "manhã" → a produção de hoje já foi feita: só faça a parte 1 (números) e pare.
- Cotas (renovam 08:00Z): Gemini TTS 10/dia por modelo (B usa gemini-3.1-flash-tts-preview: 1–2 req/Short; A Short usa gemini-3.8-flash-tts: 1 req; longo A usa 3.8: 7 req, um por ato). YouTube: ~6 envios/dia no total dos 2 canais.

## 1. Números (sempre)
- `gh api -X POST repos/justmeoccupyingspace-eng/canais-dark/actions/workflows/ytchan.yml/dispatches -f ref=main -f 'inputs[ch]=A' -f 'inputs[mode]=list'` (e ch=B). Ler o log do run (views por vídeo, inscritos). Analytics (retenção, tráfego): ytstats.yml → branch `stats`, arquivo yt.json (atraso de ~2–3 dias).
- Regras: Short ou longo > 10 mil → 3 variações do mesmo molde em 48 h. Formato com 10 vídeos ou 7 dias e mediana < 1 mil → trocar o formato.

## 2. Produção do dia (agendar sempre com 2–3 dias de folga; conferir no ytchan list o último agendado de cada fila)
- REGRAS ATUAIS: PLANO v5 no topo de specs/PLANO.md (manda sobre o resto deste arquivo).
- B "E Se no Mapa" (PT): 3 Shorts/dia, 15:00Z, 19:00Z e 22:00Z, máx. 140 palavras (≈50 s). Molde que funciona: pedaço do Brasil × vizinho/rival, ou estado vira país, com fato real "quase aconteceu" + 1 curiosidade surpresa + pergunta no fim. Gerador: acrescentar save(N, ...) em specs/ese_pt.py (copiar a estrutura dos últimos), `python3 specs/ese_pt.py`. Selo "SÓ IMAGINAÇÃO" vem do spec.
- A "Chartbound" (EN): 3 Shorts/dia 14:00Z, 17:00Z e 20:00Z (v5.1, 22/11) em specs/map_en.py — fato real "Why/How" no mapa (fronteira/enclave/compra de território), ≤130 palavras. E 1 LONGO/dia 23:00Z (PLANO v5.2: molde "X Was N% Richer Than Poland", copiar specs/long/a-L34.py; longo só se julga com 48 h).
- Cota de envio: 6/dia = longo A 1 + Shorts A 2 + Shorts B 3 (Short A das 20:00Z só se sobrar). Agendar o mais cedo possível (buraco de hoje/amanhã primeiro), nunca empurrar para depois.
- FATOS: todo número/data/nome checado na web (WebSearch/WebFetch) ou no JSON do FMI ANTES de escrever. Nada inventado. Se não confirmar, tira.
- PRÉVIA obrigatória antes de enviar: gerar es.json sintético (165 ppm) e quadros: `CHROME_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell node scripts/eserender.mjs <es.json> stills <prefixo> t1,t2,... 0.4` e `... thumb <saida.jpg>`; olhar os quadros (Read) e corrigir sobreposição, bandeira errada, câmera no vazio.
- Enviar Short: `gh api -X POST .../actions/workflows/ese.yml/dispatches -f ref=main -f 'inputs[spec]=specs/ese/b-pt-NNN.json' -f 'inputs[upload]=B'` (A: a-en-NNN, upload=A). A data/hora vem do spec.
- Antes de enviar um longo: conferir que todo `at` (keys/labels/react/items/stats) aparece literalmente na narração do shot (o prep falha com 'frase não encontrada').
- Enviar longo A: longo.yml com inputs spec=specs/long/a-LNN.py, mode=full, upload=A, at=<ISO 23:00Z>, model=gemini-3.1-flash-tts-preview (21/11: o 3.8 lê ~25 s das instruções em voz alta e estragou atos; o 3.1 saiu limpo). Disparar o LONGO ANTES dos Shorts do B (os Shorts do B também tentam o 3.1 primeiro e caem para o 3.8 quando acaba). Se um ato sair fora (wpm fora de 110–195 ou align < 0,85), reescrever só esse ato e rodar de novo com tts_cache_run=<run anterior> (só esse ato gasta cota).
- Conferir em cada run: linha `notice]{...wpm...}` (Short: 150–195 ppm) e `enviado: <ID> agendado para ...`.

## 3. Fechar
- TOM DO RELATÓRIO (ordem do Kauan, 21/11): BRUTO e honesto, todo dia. Sem suavizar, sem "ainda é cedo" como desculpa, sem elogio. Abrir com o veredito (está funcionando ou não, com o número), depois o que fracassou e por quê, o que foi CORTADO hoje, o que muda amanhã, e os erros do próprio Claude. Nunca repetir algo que não deu resultado só por inércia: todo dia tem que ter uma melhoria concreta no ar.
- Linha nova no topo de specs/long/QUEUE.md: data/hora, números (views por vídeo novo, inscritos A e B), o que foi agendado (IDs e datas), problemas. Commit + push.
- Mensagem final curta ao Kauan (PT-BR): só números + links (youtube.com/shorts/ID ou youtu.be/ID) + o que foi agendado e qualquer coisa feita sem ele saber.

## Regras fixas (do Kauan)
- Chrome: SÓ o deviceId 361e56b8-093e-4ba6-9bb0-12616394e3fc. NUNCA o 8aef3209.
- Nunca digitar senha, código, dados de pagamento, Pix, CPF/CNPJ; nunca mexer em chave de API/cobrança.
- Nunca apagar vídeo: no máximo deixar privado (só duplicata substituída). Vídeo do canal tem que estar público ou agendado.
- Avisar o Kauan de tudo que for feito sem ele saber. Mudança de configuração de conta só com "sim" dele (pendente: bio do TikTok @vale_opreco).
- Não mexer na tarefa agendada do LinkedIn.
