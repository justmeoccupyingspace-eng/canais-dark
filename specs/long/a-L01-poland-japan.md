# a-L01 — "Poland Just Passed Japan. Nobody Noticed."
Piloto de vídeo longo do Chartbound (canal A). 16:9, 1920x1080, 30 fps, alvo 8:30–9:30 (mid-rolls exigem 8:00+).
Roteiro escrito por Fable 5.1 em 26/10/2026. Implementação (engine L1) fica para Opus/Sonnet.

## Por que este tema
- Fato novo e verificável: IMF WEO out/2026 projeta PIB per capita PPP 2026 de Polônia US$ 60.051 vs Japão US$ 59.712 (primeira vez na história). Espanha US$ 60.106 — Polônia passa em 2027.
- Arco completo em dados que a pipeline já puxa (World Bank) + IMF datamapper (puxar em Actions).
- Twist no 3º ato (fecundidade polonesa 1,14 < Japão 1,15) é original — não está nos vídeos que cobrem o tema.
- Evergreen por ~2 anos; replicável como série ("X just passed Y").

## Dados (puxar no render; nunca digitar na mão)
| chave | fonte | uso |
|---|---|---|
| ppp POL/JPN/ESP/PRT/DEU 1990–2024 | WB NY.GDP.PCAP.PP.CD | gráfico principal (linhas) |
| ppp 2025–2027 | IMF datamapper PPPPC (`https://www.imf.org/external/datamapper/api/v1/PPPPC`) | prolonga as linhas; ano do cruzamento |
| nominal POL/JPN 1990–2024 | WB NY.GDP.PCAP.CD | ato 3 (iene) |
| TFR POL/JPN/KOR 1990–2024 | WB SP.DYN.TFRT.IN | ato 4 (twist) |
| desemprego POL 1990–2024 | WB SL.UEM.TOTL.ZS | ato 2 (20% → <3%) |
| inflação POL 1989–1992 | WB FP.CPI.TOTL.ZG | ato 1 (~586% em 1990) |
| crescimento real, todos os países da UE, 2009 | WB NY.GDP.MKTP.KD.ZG | mapa "ilha verde" (verde = cresceu, vermelho = encolheu) |
| crescimento real POL 1990–2024 | idem | "28 anos sem recessão" (1992–2019) |
| população POL 1990–2024 | WB SP.POP.TOTL | ato 4 |
| horas trabalhadas 2025 | OECD (POL 1.776, JPN 1.598) — constante no spec, citar | ato 4 |

Valores de referência (WB, para conferir o que o render puxar): PPP 1990 POL 6.185 / JPN 20.331 (30%); 2024 POL 51.263 / JPN 54.156 (95%). Nominal JPN 2012 49.627 → 2024 33.797; POL 2024 25.104. TFR 2024 POL 1,14 / JPN 1,15 / KOR 0,75.

A verificar antes de gravar (fatos fora da API): Polônia maior beneficiária líquida de fundos da UE (ordem de grandeza > €100 bi líquidos desde 2004); ~1/4 das exportações vai para a Alemanha (~28% em 2023); ~2 milhões emigraram após 2004; złoty caiu ~30% vs euro em 2008–09; único país da UE a crescer em 2009 (+2,8%).

## Voz e direção de narração
- Modelo: Gemini 3.8 Flash TTS (free tier) — voz **Charon**. Fallback: `en-US-Chirp3-HD-Charon` (GCP_TTS_KEY) → Edge `en-US-AndrewMultilingualNeural`.
- Style prompt (prefixo): *"You are the narrator of a data documentary. Warm, curious, unhurried, a little dry humor. Short sentences. Pause briefly before every number that matters. Never sound like an advertisement."*
- Tags inline no roteiro: `[pause]` (≈0,4 s), `[beat]` (≈0,8 s), `[low]` voz mais baixa/íntima, `[up]` energia.
- Timing de palavras: faster-whisper (já instalado em produce.yml; ver audit.py) alinhando o áudio ao texto → cues para gráfico, mascote e texto cinético.
- Métricas de "vida" (gate antes do render): desvio-padrão de F0 ≥ 2,5 semitons; 145–170 wpm; nenhuma frase > 24 palavras; ≥ 1 pausa > 0,5 s a cada 20 s.

## Música e som
- Trilha: 3 faixas CC-BY de Kevin MacLeod (incompetech.com, mp3 direto, curl no Actions; crédito na descrição):
  - abertura/tensão: "Cipher" ou "Eastminster"; corpo: "Thinking Music"/"Lightless Dawn"; fechamento: "Heartbreaking".
  - alternativa sem atribuição: YouTube Audio Library via Chrome do Kauan (precisa autorizar o download).
- Ducking: −9 dB sob a voz (ataque 80 ms, release 400 ms). Volume base −22 LUFS trilha / −16 LUFS voz / mix −14 LUFS.
- Riser (fx.py novo: `riser`, 2,5 s) antes de cada revelação; `hit` suave no cruzamento; `tick` do contador de anos; `click` nas trocas de card. Nada de pop infantil no longo.

## Linguagem visual (engine L1, 16:9)
- Câmera global: deriva lenta contínua (0,3%/s) + push-in de 4% nas revelações + corte seco no beat da música. Nunca 3 s sem movimento (gate: energia de frame-diff > 0 em toda janela de 3 s).
- Fundo: gradiente profundo do canal + grão + vinheta + partículas lentas (profundidade).
- Componentes: `Map` (world-atlas + d3-geo, zoom Europa→Polônia; coropleto 2009), `Lines` (POL/JPN/ESP desenhando no tempo da fala, ticker de ano, ponto de cruzamento com burst), `Nominal` (duas linhas, iene), `Stat` (contador grande), `Cards` (3 catches), `Photo` (Wikimedia Commons PD/CC, Ken Burns, crédito no canto), `Host` (mascote PiP 22% da altura, canto inferior direito; tela cheia nas viradas de ato), `Chapter` (lower third).
- Mascote: lip-sync pelo envelope (já existe); reações cued por palavra: `nod` no número-chave, `lean` (inclina pra frente) na pergunta, `shock` no twist, `point` para o gráfico, `think` no "why?". Idle com respiração + peso trocando de perna. Poses novas a implementar: `lean`, `point`, `nod`.
- Texto cinético: só os números e as frases-âncora (≤ 6 palavras), entrando por palavra com spring; nunca legenda corrida.
- Thumbnail: bandeiras 🇵🇱 🇯🇵 com linha cruzando, mascote de queixo caído apontando, texto "PASSED JAPAN?!" — gerar via still do Remotion (composição `Thumb`).

## Render
- `remotion render` em matriz de 6 jobs (`--frames a-b`) + job de concat (ffmpeg). Pré-render: TTS → whisper → data → timeline JSON (um só arquivo, cada job lê o mesmo).
- Upload: publishAt sexta 31/10 16:00Z (não — esperar aprovação do Kauan ao piloto; deixar `at` vazio).
- Descrição: fontes (WB indicadores, IMF WEO out/2026, OECD), créditos de música (CC BY 4.0) e fotos, "Narration is AI-generated". Marcar "conteúdo alterado/sintético" no upload.

---

## ROTEIRO (narração em inglês; [colchetes] = direção)

### 0. COLD OPEN (0:00–0:50) — música: Cipher, baixa; mapa Europa, grão
[Map: Europa escura, Polônia acende] In 1990, the average person in Poland produced about six thousand dollars of value a year. [pause] The average person in Japan? [beat] Twenty thousand.
[Photo: fila em loja, 1989–90] Poland was coming out of forty years of communism. Inflation was heading for six hundred percent. Shops had queues, but not much on the shelves. [pause] Japan was the second-largest economy on Earth.
[Lines: as duas linhas aparecem só no ponto 1990] Thirty-six years later, the IMF put out a forecast that almost nobody read. [riser] In 2026, for the first time ever, [hit; linhas correm até 2026 e se cruzam] the average Pole out-produces the average Japanese.
[Host tela cheia, shock → sorriso] Nobody threw a party. Most people didn't notice. [low] And the number that explains how it happened… is the same number that could undo it. [up] Let's go through the chart.
[Chapter: "1 · The hole"]

### 1. THE HOLE (0:50–2:20) — música: corpo, tensa; Lines começa a desenhar
[Lines: 1990, destaque "30%"] Here's where the line starts. Thirty percent. That's Poland's income as a share of Japan's, in 1990.
[Photo: Balcerowicz / Sejm 1989, PD se houver; senão Stat "Jan 1, 1990"] And honestly, thirty was generous. Because on January first, 1990, Poland did something economists still argue about. It ripped the bandage off. [pause] Price controls: gone. Subsidies to state factories: gone. The currency: let it float, let it fall. They called it shock therapy. [beat] The shock part was real.
[Stat: inflação 1990, contador sobe até ~586%] Prices rose almost six hundred percent in a single year. Output fell. Unemployment went from zero — because communism didn't admit it existed — to double digits.
[Lines: ticker 1990→1995, linha POL faz o vale e sobe] But watch the line. By 1992, Poland was growing again. [Host nod] And here is the stat that actually matters: [kinetic: "28 years. No recession."] from 1992 to 2019, Poland's economy grew every single year. Twenty-eight years. [pause] No other country in the European Union can say that.
[Host lean] So how do you go from bread lines to no recessions? Three things. And the first one has a date.
[Chapter: "2 · The climb"]

### 2. THE CLIMB (2:20–4:30) — música: sobe um degrau no 2004
[Map: UE 2004 — dez países acendem, Polônia por último] May first, 2004. Poland joins the European Union, and the slope of this chart changes.
[Cards 1/3: "Money"] One: money. Over the next twenty years, Poland becomes the biggest net recipient of EU funds in the whole bloc. Roads, rail, water, broadband. [kinetic: valor verificado] More than a hundred billion euros more than it paid in.
[Cards 2/3: "Factories"; Map: seta Berlim→Varsóvia] Two: factories. German companies needed somewhere to build parts: close, cheap, skilled. Warsaw is a six-hour drive from Berlin. Today, roughly a quarter of everything Poland exports goes to Germany.
[Cards 3/3: "People"; Map: pontos saindo para UK/IE e voltando] Three: people. Around two million Poles left to work in Britain and Ireland. They sent money home. And then — slowly — a lot of them came back, with skills and savings.
[Lines: ticker 2004→2008, POL acelera] Look at the slope after 2004. [Host point] That's not luck. That's a supply chain.
[Map coropleto 2009: UE toda vermelha, Polônia verde] And then 2008. The global financial crisis. In 2009, every single economy in the European Union shrank. [pause] Every one — [hit] except Poland. [Stat: +2.8%] It grew. The press called it "the green island." One green dot on a map of red.
[Host think] Why? Boring reasons — which are the best reasons. Banks that hadn't gone crazy. A currency, the złoty, that dropped about thirty percent and made Polish exports cheap at exactly the right moment. And a home market of thirty-eight million people buying Polish stuff.
[Stat: desemprego 20% → 2.9%, contador cai] Look at unemployment. 2002: twenty percent. One in five adults. 2024: under three. [beat] That's not a recovery. That's a different country.
[Chapter: "3 · The other line"]

### 3. THE OTHER LINE (4:30–5:45) — música: fria, mais vazia
[Lines: isola JPN, câmera push-in na linha quase plana] But a crossover has two lines. And the second one barely moved.
[Photo: Tóquio anos 90 / Nikkei] In 1990, Japan's bubble popped. Stocks, land, everything. What followed got a name: the Lost Decade. Then the second Lost Decade. [pause] In purchasing-power terms, Japan did grow — slowly. From twenty thousand to about fifty-four. [Lines: POL sobe ao lado] Poland went from six… to fifty-one.
[Nominal: duas linhas, JPN cai de 2012] And in plain dollars, it's worse. In 2012, the average Japanese income was almost fifty thousand dollars. In 2024? [beat] Thirty-four. [Host shock] That's not Japan getting poorer at home. That's the yen losing nearly half its value against the dollar.
[Host, tela cheia, sério] So part of this story is Poland running. [low] And part of it is Japan standing on an escalator going down.
[Chapter: "4 · The catch"]

### 4. THE CATCH (5:45–7:30) — música: para no twist
[Lines: cruzamento 2026, confete discreto] Okay. Poland passes Japan in 2026. [Host lean] Before you move to Warsaw: three catches.
[Cards: "1 · Per person ≠ per hour"; ícones de relógio] One. Per person is not per hour. Poles work about seventeen hundred and eighty hours a year. The Japanese, about sixteen hundred. [kinetic: "+4.5 weeks"] That's four and a half extra weeks of full-time work. Measured per hour, Japan is still ahead.
[Cards: "2 · Purchasing power ≠ pay"] Two. Purchasing power is not pay. These numbers are adjusted for the fact that a haircut in Kraków costs less than one in Osaka. In actual dollars, Poland's income is still about twenty-five thousand. Japan's, thirty-four.
[Cards: "3 · The number"; música cai; Stat gigante "1.14"] Three. And this is the one. [beat] Babies per woman. Poland, 2024: one point one four. [pause] Japan — the country the entire world uses as the example of a shrinking society — [beat] one point one five.
[Host shock → quieto] Poland now has fewer children per woman than Japan.
[Lines TFR: POL cruza abaixo de JPN; população POL começa a cair] Half of Poland's miracle was a big, young workforce with nowhere to go but up. That workforce is now getting older. The same math that shrank Japan is already running in Poland — [low] it just started thirty years later.
[Chapter: "5 · What's next"]

### 5. WHAT'S NEXT (7:30–8:45) — música: volta, resolvida
[Lines: gráfico completo 1990→2027, POL/JPN/ESP] So here's the whole chart, start to finish. Thirty percent of Japan… to a hundred. [pause] Spain is next: the IMF has the two basically tied this year, [kinetic: "$60,106 vs $60,051"] and Poland ahead next year. Germany? No. Germany is still thirty percent ahead, and the gap isn't closing fast.
[Host, tela cheia, think → lean] But the real question isn't who Poland passes next. It's whether a country can keep climbing after its people stop multiplying. [beat] Japan couldn't. Korea is trying. [pause] Poland is about to find out.
[Photo: Varsóvia hoje, skyline; Ken Burns lento] If you'd told someone standing in a Warsaw bread line in 1990 that their grandchildren would out-earn Tokyo… they'd have laughed. [beat] The chart didn't.
[End card: thumbnail do vídeo da Coreia + inscrever] If you want the Korea version of this story — the one with the scariest number on Earth — it's right here. [Host wave] I'm Chartbound. See you in the next one.

---
Contagem alvo: ~1.300 palavras faladas. Se o TTS fechar abaixo de 8:05, alongar o ato 2 com o beat "o que o dinheiro da UE construiu" (km de rodovia, dado verificado) — nunca com enrolação.
