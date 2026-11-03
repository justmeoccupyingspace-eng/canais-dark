# Fila de vídeos longos (1 por canal por dia)

Rotina diária (cota Gemini zera ~07:00Z até 1/nov; depois ~08:00Z):
1. ~07:10Z disparar `longo.yml` mode=full para o A (gemini-3.1-flash-tts-preview, Charon) e o B (gemini-3.8-flash-tts, Iapetus).
2. Revisar preview (sheet, gates, loudness, frames com texto; deixas tardias perto do fim do shot; gráfico parado; pílulas sobrepostas). Correção só de texto → `prep_run=<run>` (lpatch aplica sem gastar cota).
3. Publicar no MESMO dia do render (decisão do Kauan, 29/10): A às 18:00Z, B às 20:00Z (`upload=A|B`, `at=`). Thumbnail: automática pela API (canais verificados em 29/10); conferir a anotação "thumbnail aplicada" no job final.
4. Shorts = 4 cortes do longo do dia (sem cota TTS): `python scripts/mkclips.py specs/long/<x>.json <videoId> <run_final> <run_prep> auto:<publishAt do longo>` → `cortes.yml cfg=specs/clips/<x>.json` (só render) → revisar previews no branch `cortes-<run>` → `cortes.yml use_run=<run> upload=A|B`. Horários (decisão do Kauan 29/10: 2 cortes na noite do longo + 2 na manhã seguinte, antes do próximo longo; Brasília fixo = UTC−3):
   - A: longo 15:00 BRT (18:00Z) → cortes 19:00 e 22:00 BRT (22:00Z, 01:00Z) + 09:00 e 12:00 BRT do dia seguinte (12:00Z, 15:00Z).
   - B: longo 17:00 BRT (20:00Z) → cortes 20:00 e 23:00 BRT (23:00Z, 02:00Z) + 10:00 e 13:00 BRT do dia seguinte (13:00Z, 16:00Z).
   - Noite BRT = tarde/noite nos EUA (maior público); manhã BRT = noite em PH/ID/IN. Se o longo atrasar, mover cortes com `ytresched.yml` (ids, at, ch).

Limite: ≤10 pedidos/dia por modelo; cada ato ≤210 palavras = 1 pedido (roteiro de ~1.150 palavras ≈ 7–9 pedidos).

## Decisão 30/10 (pedido do Kauan: originalidade + RPM)
- Pesquisa (research/q1.json, q2.json → branches research-41079941354 e research-41080248419): "How It Ticks" tem 19 canais com o mesmo nome (12 criados em 2026); temas do B dominados por gigantes (GPS: Veritasium/minutephysics; 931 GB: ThioJoe 1,1 mi + Short 2,4 mi; 0,1+0,2: Fireship 8,8 mi; QR: Veritasium 9,7 mi). "Chartbound" é nome único.
- A (Chartbound): MANTÉM. Única tração real (Polônia 23 mil views, CTR 9,4%; Coreia 50% de retenção). Regras novas de pauta:
  1. Antes de roteirizar, rodar ytresearch com o tema: se existe vídeo ≥500 mil views nos últimos 2 anos, só entra com dado novo (publicado há ≤60 dias) ou número calculado por nós que ninguém mostrou.
  2. Título conferido contra os existentes (nada de "X Just Passed Y" igual aos clones).
  3. Prioridade a dados recém-lançados (Eurostat, World Bank, institutos nacionais) e a ângulos com número próprio.
- B (How It Ticks): PAUSADO a partir de 31/10 (nada de render novo; o canal fica, nada é apagado). B-L03 (GPS) cancelado. Esforço e cota concentrados no A até monetizar.

## Decisão 30/10 23:00 (Kauan)
- How It Ticks parado de vez até o Chartbound monetizar; depois disso, Claude decide se recria/reaproveita o slot com outro tema (autonomia total de administração).
- Chartbound recebe o esforço que ia para o B:
  1. Banco de pautas aprovadas no filtro de saturação (meta: ≥5 sempre prontas), cada uma com número próprio ou dado recém-lançado.
  2. Teste A/B nativo do Studio (3 miniaturas) em todo longo novo, a partir do A-L04.
  3. Cota TTS do modelo do B (gemini-3.8-flash-tts) passa a servir de reserva do A (refações sem perder o dia).
  4. 2º longo por dia só quando o banco tiver ≥3 pautas aprovadas; reavaliar semanalmente por views/hora nas primeiras 48 h.
- Exclusão: Claude deixa privado (reversível) e lista; apagar de vez é com o Kauan.

## Aprendizados de pauta
- Coreia (A-L02): 99 views em ~2,3 dias, CTR 2,4% apesar de 50% de retenção. Tema mais batido do nicho (Kurzgesagt 15,9 mi + dezenas de vídeos "Korea is dying"); título "Scariest Number" soa igual aos clones. Retenção boa não salva CTR baixo: o filtro de saturação (regra 1) vale também para tema "do momento". A Polônia funcionou por ser número novo (IMF out/26) que ninguém tinha mostrado.
- Retenção Polônia (Analytics até 28/10, 3,2 mil views; 95% Browse/início): 63% aos 30 s, 51% em 0:52, 31% em 1:30 e daí plano (29% no meio, 24% em 90%, 15% no fim); duração média 2:35 de 8:45. Maiores quedas: 0:21 (−12 pts, globo da abertura s01), 0:26 (−9, entrada do gráfico do FMI), 0:47 (−7, host sem dado s03), 1:03 e 1:19. Quem passa de 1:30 fica até o fim.
  → Regras: nada de globo nos primeiros 60 s; gráfico com o número-gancho já no 1º quadro; intro de host curta. Teste em 02/11: A-L08 com a intro dividida (lista + host de 2 frases) × A-L09 com host longo; comparar retenção aos 60 s quando o Analytics liberar (~3 dias).
- 31/10 21:31Z: Polônia 41,6 mil (+~500/h, 554 likes, 163 coment.); Coreia 286 em 2 dias; Irlanda 37 em 27 h; Letônia 1 em 3,5 h. Geo do canal (Analytics): PL 14,0 mil de ~18 mil views contadas → o A-L01 explodiu porque o público POLONÊS assistiu/compartilhou uma vitória do próprio país. Coreia/Irlanda/Letônia: tema negativo ou país pequeno, sem esse motor. Regra nova: priorizar "vitória de país grande e conectado" (Polônia, Turquia, Vietnã, Espanha, Filipinas, Indonésia, Nigéria, Egito); temas negativos (México, África do Sul) por último. A-L06 retitulado para o público polonês (q8: sem concorrente longo; maior é Short de 19 mil).
- 31/10 23:31Z: Polônia 42,7 mil (+510/h), Coreia 337 (+25/h, acelerou), Irlanda 47, Letônia 7 em 5,5 h (<30 → falhou; sem teste A/B: com tão poucas impressões o teste não conclui; causa é o tema, país pequeno). Saudi no ar 23:00Z (0 em 30 min). Chartbound 84 inscritos. TikTok: c-315 claro 40 views/3 curtidas em 3 h (escuros = 0; post do Kauan das 20:00 com 4 em 30 min) → visual claro destravou a distribuição.
- 01/11 18:16Z: Polônia 46,2 mil (~230/h), Coreia 417, Irlanda 106, Letônia 70 (subiu com os cortes), Saudi 7, A-L06 público (0 nos 1os min). Chartbound 89 inscritos.
- Depois que o A-L06 sair (01/11 18:00Z): trocar tela final + card do Poland (ainda +500 views/h) de Korea para o A-L06. Maior alavanca de tráfego para os novos.
- Shorts: os templated antigos (Etiópia 746, Egito ~790) superam os cortes do longo (5–135). Cortes não são o canal de descoberta; servem de vitrine para o longo.

## Telas finais / cards (estado 31/10 01:40Z; 01/11: A-L06 → Poland + inscrição; A-L07 → A-L06 + inscrição; Poland → A-L06 FEITO 18:20Z: elemento de vídeo ampliado cobrindo o 'UP NEXT Korea' renderizado; card 7:21 Korea → A-L06 'Poland passed Portugal too'; card Ireland 4:47 mantido)
- Poland (XGmxZPO8lx8): tela final → Korea + inscrição; cards: Korea 7:21, Ireland 4:47 ("Europe's richest? Not really").
- Korea (PP9J1_ZcpBo): tela final → Poland + inscrição.
- Ireland (EpQQtd0o78Q): tela final → Korea (bate com o "watch next 0.72" do outro) + inscrição; card Poland 5:30.
- B-L02 (_SgVH8bGG5k): tela final → B-L01 (bate com o "watch next 0.1+0.2") + inscrição.
- Regra: o vídeo da tela final tem que ser o mesmo do "WATCH NEXT" renderizado no outro; setar no Studio no dia da publicação.

## Calendário de render (linha de foco 01/11: 1 longo/dia; 2º só se as duas pautas tiverem nota ≥8 no filtro; voz 3.1 ≥1.115 palavras, 3.8 ≥1.270)
- 01/11: A-L06 (3.1, 18:00Z) + A-L07 (3.8, 23:00Z) — feito.
- 02/11: A-L09 Espanha×Japão (3.1, 18:00Z) + A-L08 Vietnã×Indonésia (3.8, 23:00Z) — já prontos e dentro do filtro; último dia com 2. Cortes: 2 por longo (A-L09 19:00/22:00 BRT, A-L08 +1d 10:00/13:00).
- 03/11: A-L14 Polônia/Croácia > Grécia (18:00Z), roteiro em 02/11. Sem 2º longo (Bulgária nota ~7: país pequeno).
- 04/11+: A-L17 Polônia > Espanha (conferir dado: Euronews 26/02/2026, Tusk; FMI/Eurostat PPP), depois o melhor do banco pelo filtro. Cota de voz que sobra → canal B (Nest Egg Atlas, 3.8); faixa polonesa só se ainda sobrar.
- Rebaixados (prontos, fora do filtro: tema negativo): A-L10 México, A-L11 África do Sul — só se T1 falhar em 15/11 ou para preencher buraco.
- Antes de cada render: validar deixas (todo 'at' existe na fala), teste visual grátis (engine=edge) e checagem de títulos de stats ≤34 caracteres, stats na ordem da fala, miniatura com line2 ≤10 caracteres (senão o mascote cobre).

## TikTok C (alerta 31/10)
- Template escuro (gabgen) zerou: MDC 29/10 19:30, negação 30/10 12:30, Pitágoras 30/10 19:30 = 0 views (MDC com 27 h). Antes: 107–219 por post. Template claro do Kauan segue com views (111, 34).
- Checagem 31/10 15:40 BRT: Excel 31/10 12:30 = 0 views após 3 h → 4º zero seguido do escuro (MDC 29/10 19:30, negação e Pitágoras 30/10, Excel 31/10). Os do Kauan (claro, 20:00) seguem com 112–116. Os dois têm o selo "Conteúdo promocional", então não é isso. Nenhum aviso em Notificações. Antes de 29/10 o escuro dava 107–748 → hipótese: a série escura (mesmo visual, mascote e música em todo post) caiu em filtro de conteúdo repetitivo.
- Preparado: paleta clara 'gabaritoclaro' no V3 (fundo rosa, texto escuro, mascote rosa, música diferente) e as 14 da semana 45 renderizadas em versão clara (specs/v3/c-3xx-*-claro.json, branches pv-<run>). Trocar os agendados = Kauan apaga os escuros; eu reagendo os claros no Chrome dele com o OK.
- 31/10 17:33 BRT: teste publicado AGORA — c-315 claro (colocação pronominal, mesma questão do escuro agendado 31/10 19:30). Ler views às 20:30 BRT (3 h). Já agendados claros: c-318 02/11 12:00, c-319 02/11 19:00. Pedido ao Kauan: apagar escuros (:30). Regra: claro em 12:00/19:00; escuro em 12:30/19:30; posts do Kauan em 19:00/20:00 sem fuso.
- 31/10 ~18:00: Kauan apagou TODOS os escuros agendados (e junto o claro c-319). 18:05–18:55 agendei 15 claros: c-316 01/11 12:00, c-317 01/11 17:30, c-318 02/11 12:00 (já estava), c-319 02/11 19:00, c-320…c-331 03–08/11 12:00/19:00. Todos com "Sua marca" e legenda do spec. c-315 claro: 4 views em 25 min, ainda 4 com 1h20.
- Fluxo de agendamento no Studio (Chrome): upload → find "file input (type=file)" → file_upload; legenda em (500,286); rolar 10 → "Exibir mais" (756,400) → divulgação (484,461) → Sua marca (278,503) → Programar (348,221); rolar ↑3 → data (500,497) → seta mês (551,258) → dia (grade nov: Dom x=298 … Sáb x=542; linha1 y=337, linha2 y=366); hora (343,497): colunas centradas em y=381, passo 26 px (clicar linha recentra); rolar ↓15 → Agendar (336,644).
- Decisão após o teste: c-315 claro >0 views (≥30) → agendar c-320…c-331 claros 03–08/11 12:00/19:00 (+ c-316 01/11 12:00, c-317 01/11 18:30 se o Kauan apagou os escuros desses dias). Claro também 0 → problema é da conta/série, não do visual: parar de agendar duplicatas e testar formato diferente (sem mascote/sem TTS, estilo do Kauan).
- Agendados c-318…c-331 (02–08/11, 12:30/19:30) são todos template escuro. Se 31/10 12:30 (Excel) e 19:30 (colocação) também ficarem em 0 após 3 h, o template está sendo filtrado → trocar visual/áudio antes de 02/11 (agendado no TikTok não edita, só apaga — apagar é do Kauan).

## TikTok C: funil para o WhatsApp (decisão do Kauan 01/11 16:53 — sem canal de histórias; foco em vender a apostila)
- Kauan NÃO quer o canal de histórias animadas (pesquisa em /home/claude/reports/Rota de retorno mais rápida.md). Seguir: TikTok → WhatsApp → apostila; YouTube segue o calendário (veredito do A-L06/A-L07 em 04/11).
- 01/11: comentário-CTA ("Quer a amostra grátis da apostila... Chama no WhatsApp da bio e manda AMOSTRA.") postado no c-315 e no c-316. Fixar comentário NÃO existe no TikTok web (só "Excluir"). Repetir em cada post claro publicado (nas checagens).
- Bio trocada para "1 questão do Escrevente TJSP por dia. Amostra grátis: WhatsApp 11 91729-1381" (o web mostrou erro, mas salvou; confirmado às 20:45 BRT).
- Semana 46 (próximo lote, c-332+): cena final com CTA de venda ("Amostra grátis da apostila: WhatsApp na bio", fala "Quer a amostra grátis? Chama no WhatsApp da bio.") em vez de só "Siga"; mais posts de edital/prazo ("faltam X dias para o fim das inscrições", 10/12), salário e circunscrição do interior (2ª–10ª RAJ), que trazem candidato novo.
- Instagram @gabaritododia (liberado pelo Kauan para concursos): 4 posts, 0 seguidores em 01/11. Plano: repostar os vídeos claros como Reels (1/dia) — Reels alcança não seguidores e o IG aceita link clicável do WhatsApp na bio sem mínimo de seguidores (TikTok exige 1.000).
- 01/11 20:45 BRT: CTA postado também no c-317. c-316 96 views, c-317 47 em ~3 h; post do Kauan 01/11 19:00 (Lei 9.099) 13. YouTube 23:42Z: A-L06 16 views em 5,7 h (Polônia teve 13 nas 1as 13 h), A-L07 público às 23:00Z, Letônia 103, Polônia 47,7 mil, 91 inscritos.
- 02/11 19:40 BRT: CTA postado no c-318 (salário, 82 views em 7 h) e no c-319 (concordância, 7 views em 50 min). Demais: c-315 97, c-316 111, c-317 94; posts do Kauan 114 e 129. Perfil 91 seguidores, 174 curtidas.
- 02/11: 1º Reel no IG @gabaritododia = c-316 MMC (out/ig/c-316-ig.mp4, recomprimido p/ <10 MB). Bio do IG já tem o número do WhatsApp em texto; link clicável SÓ pelo app (web: "Somente é possível editar os links no celular") → pedido ao Kauan: app → Editar perfil → Links → https://wa.me/5511917291381.
- YouTube 22:40Z: Chartbound 97 inscritos; Polônia 50,6 mil; A-L06 104 views em 29 h; A-L07 12 em 24 h; A-L09 7 em 4,7 h. Nest Egg Atlas: B-N01 1 view em 4 h (normal p/ canal recomeçado).
- Números 01/11 ~17h: c-315 claro 94 views/7 curtidas (24 h); c-316 claro 78 em 5 h; posts do Kauan 108–163. Perfil: 89 seguidores, 164 curtidas.

## Plano de correção do Chartbound (01/11 21:45, pedido do Kauan "como vai arrumar")
- Feito 01/11 21:50: comentário fixado no Poland (XGmxZPO8lx8) com link do A-L06 + "Which country should Poland pass next?". YouTube já sugere o A-L07 (Turkey = Greece) ao lado do Poland.
- Tema: só "vitória de país grande" com número novo. 02/11 Espanha×Japão + Vietnã×Indonésia (ok). 03/11: sai A-L10 México e A-L11 África do Sul; entra A-L14 Polônia/Croácia > Grécia (roteiro em 02/11) e A-L12 Bulgária se ficar pronto.
- Embalagem: teste A/B de 3 miniaturas no Studio em cada longo novo a partir do A-L06; meta de clique ≥5%.
- Retenção: número-gancho no 1º quadro, sem globo, intro curta (teste A-L08 × A-L09).
- Inscrito: pedido de inscrição amarrado à série + pergunta de próximo país; playlist "Who passed whom".
- Cortar: Shorts templated novos (risco "inauthentic content" na revisão do YPP); cortes do longo continuam.
- Se a veia polonesa confirmar (04/11): faixa de áudio em polonês nos vídeos da Polônia (cota grátis de voz).
- Gatilhos: 04/11 (≥5 mil em 72 h = veia confirmada); 15/11 (todos <1 mil → 3 longos/semana); 15/12 (<500 inscritos → regra antiga perdida, manutenção).

## Execução 02/11 (11:30Z)
- Teste A/B de miniatura ativo (3 versões: mascote atual × MAPA estilo Polônia × bandeiras sem mascote) em A-L06, A-L07, A-L08; A-L09 com mascote × duelo de linhas × bandeiras (criado antes do mapa). Variantes em src/long/L1.jsx (thumb.v = map | duel | flags); arquivos em out/thumbs/.
- A miniatura atual do Polônia × Japão é um MAPA (Polônia em vermelho), não o duelo de linhas do roteiro original → hipótese T2 = mapa.
- Telas finais: A-L09 → Polônia × Japão (elemento sobre o card WATCH NEXT) + card 7:05 "Poland passed Japan too"; A-L08 → A-L09 + card 6:50 "Spain passed Japan too".
- Playlist "Who Passed Whom" criada (PLRrtWo-xNj6Q, pública, 5 vídeos).
- Números 11:50Z: A-L06 60 views em 18 h, A-L07 5 views em 13 h (fraco; veredito 04/11).

## Execução 03/11 (09:00–09:40Z)
- A-L14 (knei7dcuF5M, 18:00Z): teste A/B mapa × duel × flags; tela final inscrição + A-L06 sobre o WATCH NEXT; card 7:40 → A-L06; playlist Who Passed Whom.
- Nest Egg Atlas: B-N01 tela final → B-N02 (vídeo específico; o Studio avisa "privado, será substituído" até 18:30Z); B-N02 tela final inscrição + B-N01 sobre o card (elemento 996,261 207×117 no preview = card do End em 140,250 820×462).
- ytstats 09:25Z: Chartbound 100 inscritos, 61,5 mil views; Polônia 51.586 (+~1 mil/dia); A-L06 126 views (~40 h); A-L07 101 (~34 h; era 12); A-L09 9 e A-L08 7 (~15 h e ~10 h). Nest Egg Atlas 6 inscritos: B-N01 2 views em 15 h, cortes 10 e 13.
- Leitura: nenhum longo novo do Chartbound perto de 5 mil → veredito 04/11 vai dar "não confirmado"; segue T1 até 15/11 (regra). B ainda sem distribuição (normal nas 1as 48 h de canal recomeçado).

## Linha de foco (01/11 22:30 BRT; doc "Canais Dark — Plano Operacional", seção "Linha de foco do Chartbound")
- Foco único: "quem está passando quem" — país em ascensão acaba de passar um mais rico/famoso, contado pelo lado de quem subiu. Série principal: Leste Europeu passando Sul/Oeste (Polônia primeiro). Controle: Turquia, Vietnã, Filipinas, Índia, Nigéria, Espanha.
- Filtro (0–2 cada, entra com ≥8/10): 1) país que sobe tem público grande que assiste em inglês; 2) orgulho, nunca derrota; 3) dado ≤60 dias ou cálculo nosso; 4) nenhum concorrente ≥500 mil views em 2 anos na mesma ultrapassagem; 5) rivalidade (o lado ultrapassado também comenta).
- Testes: T1 tema (6 longos no filtro; mediana 72 h ≥1.000 ou um ≥10 mil; base 113) · T2 miniatura A/B 3 versões (mapa × mascote; clique ≥5%) · T3 1º minuto (A-L08 intro curta × A-L09 longa; ≥70% aos 30 s; Polônia 63%) · T4 áudio polonês (se 04/11 confirmar; AVD da PL +20%) · T5 inscrição (CTA de série + "qual país a seguir?" + playlist; ≥3 inscritos/mil views; hoje 1,5).
- Cortes: 2 por longo (mkclips A = 19:00/22:00 BRT; os 2 primeiros clips do spec → pôr os de orgulho primeiro). Nenhum Short templated novo.
- Datas: 04/11 (≥5 mil em 72 h no A-L06 ou A-L07 → série confirmada, liga T4, volta o 2º longo só nessa série) · 15/11 (T1 falhou → família Ásia/África em ascensão) · 15/12 (<500 inscritos → manutenção, 3 longos/semana) · 31/01/2027 (1.000 inscritos + 4.000 h → inscrever no YPP antes de 01/02/2027).

## A · Chartbound
| id | tema | estado | publicação |
|---|---|---|---|
| A-L01 | Poland passed Japan | publicado | 27/10 |
| A-L02 | South Korea's scariest number | publicado (PP9J1_ZcpBo) | 29/10 18:40Z |
| A-L03 | Ireland is the richest country in Europe. It isn't. | agendado (EpQQtd0o78Q) · cortes 6z26Abz-OT4, ScvCTM6mp9s, uxy6Av-fHBw, MmF-8_Niq0I | 30/10 18:00Z |
| A-L04 | Latvia Lost 30% of Its People. There Was No War. | agendado (LinIPuj7wDI) · cortes 9NsLyIXALV4, xAsXXbTTBAY, APX7b0usW5M, ScuyYnuARNU | 31/10 18:00Z |
| A-L05 | Saudi Arabia Is No Richer Than in 1990 (Golfo) | agendado (s7VEEc8S61c, voz Charon no 3.8, 8:02) · cortes TZSIH-yJFQI, wdyKVv2WiXo | 31/10 23:00Z |
| A-L06 | Poland Just Passed Portugal. Again. (título trocado 31/10 para o público polonês; era "Portugal Was Richer…") | agendado (aaBU1S0wwpM, render 41284184197, 8:23) · cortes 2gl7fS3Ebm0, BMxSpCNgTYQ, Big4NErU6u0, Wc82qjCvjFk · tela final → Polônia | 01/11 18:00Z |
| A-L07 | Turkey Caught Up With Greece. Despite 50% Inflation. | agendado (dJbN7cO1Rnc, render 41286294903, 8:06; 1º render deu 7:59 → +34 palavras no ato 3, WATCH NEXT corrigido) · cortes A2 zfDCacC3I9I, wxEb-427bJg · tela final → A-L06 | 01/11 23:00Z |
| A-L08 | Vietnam Overtook Indonesia. With a Third of the People. | agendado (MHSYNptZ38s, render 41412455861, 8:16) · cortes qmU3o61jNz4 (03/11 13:00Z), 7AcmLT5r-30 (03/11 16:00Z) · WATCH NEXT → A-L09 (trocado da Coreia) · tela final/card no Studio pendente | 02/11 23:00Z |
| A-L09 | In 2012, Japan Was 74% Richer Than Spain. Now Spain Is Ahead. | agendado (l7uaR6BQYa4, render 41412443395, 8:27) · cortes yWOIBAXz5ro (22:00Z), k-9lf5rpo3E (03/11 01:00Z) · WATCH NEXT → Polônia · tela final/card no Studio pendente | 02/11 18:00Z |
| A-L10 | (REBAIXADO 01/11: tema negativo) Mexico Exports 4x More Than in 2000. Its Workers Produce Less. (21 países passaram; PIB por trabalhador −10%) | pronto: checks ok, 1.110 palavras, voz 3.1, teste visual ok · tela final → A-L07 | — |
| A-L11 | (REBAIXADO 01/11: tema negativo) South Africans Are Poorer Than in 2008. Here's Why. (Egito 2019, Indonésia 2023, Vietnã 2024 passaram em PPP; pico real em 2013) | pronto: checks ok, ~1.270 palavras, voz 3.8, teste visual ok · tela final → A-L08 | — |
| A-L12 | Bulgária: do mais pobre da UE ao euro (jan/26), 0,31→0,49 dos EUA desde 2010 | banco: filtro ok (q6; maior longo 78 mil) | |
| A-L13 | Albânia mais rica por pessoa que México (PPP 2024) e Brasil (nominal 2024) | banco: q7 ok (TLDR 115 mil; nada ≥500 mil) | |
| A-L14 | In 2008, Greece Was Twice as Rich as Poland. Now It's Behind. (Polônia 2024 e Croácia 2025 passaram em US$; 12 de 13 passaram em PPS; só a Bulgária atrás) | agendado (knei7dcuF5M, 8:34) · cortes 8S7VJNqcwqQ, PBtivTl3WIc · teste A/B miniatura mapa × duel × flags · tela final: inscrição + A-L06 sobre o card WATCH NEXT · card 7:40 → A-L06 ('Poland passed Portugal too') · playlist Who Passed Whom (03/11 09:20Z) | 03/11 18:00Z |
| A-L15 | Argentina passada por Costa Rica e Sérvia (PPP 2024); Sérvia também no nominal 2025 | banco: q7 ok (Econ 38 mil) | |
| A-L16 | República Dominicana: passou o México (PPP 2021), crescimento mais longo da América Latina | banco: q7 ok (nada ≥2 mil) | |
| A-L17 | Poland Is $55 Away From Passing Spain (FMI out/2026: 2026 ESP $60.106 × POL $60.051; POL passa em 2027; Tusk disse em fev/26 que já tinha passado — dado antigo) | roteiro 03/11: 1.146 palavras, 6 atos, voz 3.1 Charon, 80 checks ok (data runs 41612978719/41614082943), saturação ok (q11: maior longo em inglês 2,2 mil) · miniaturas out/thumbs/a17_{map,duel,flags}.jpg · WATCH NEXT → Polônia × Japão · teste visual edge 41614422835 | 04/11 18:00Z |
| ~~Rússia > Itália/Canadá~~ · ~~Singapura > Noruega~~ · ~~Geórgia~~ | fora: tema de guerra / Singapura saturada / busca ambígua | — | |
| ~~Germany~~ / ~~Iene~~ | reprovados no filtro | — | |

Ferramentas de pauta: `mine.yml` (sem input = garimpo de ultrapassagens/quem subiu/quem caiu no WDI; com `dump` = séries do WDI para explorar) → branch mine-<run>. O datamapper do IMF bloqueia os runners (403): para projeção do WEO, snapshot com fonte.

## B · Nest Egg Atlas (ex-How It Ticks) — decisão 01/11 22:40 BRT (Kauan: "volta a usar a cota no outro canal, muda o tema, público fixo, máximo RPM")
- Público fixo: americanos de 55 a 75 anos, perto de se aposentar ou aposentados. Tema: o dinheiro da aposentadoria em dados oficiais — "onde você está" (percentis por idade, renda, estado).
- RPM (estimativas de terceiros, US$/mil views): aposentadoria 12–18 médio (OutlierKit, jun/2026), finanças pessoais 8–20 (Peeksy, abr/2026); Q4 +30–60%. Polônia 0,60 vs EUA 5,11 na amostra de música da Dynamoi → o público do Chartbound paga ~8× menos.
- Evidência de que canal novo entra (q9/q10, research-41371308058 e -41371483680): Retiree Math (criado 09/10/26) 350 mil em "How Wealthy Are You Compared to Most Retirees?"; Income Over Wealth (fev/26) 402 mil "6 Wealth Tiers in Retirement (Where Do You Rank?)"; Dean Finance (640 inscritos) 167 mil; Uncle John Financial (dez/25) 184 mil "401(k) Balances by Age: Federal Reserve Survey Data"; Trevor Phibbs (13 mil inscritos) 2,4 mi "Social Security at 62 vs 70". Contra: formato "anúncio do IRS/limite do 401k" está morto (dezenas de canais IA com 0–100 views); vários canais IA criados em set–out/26 com <2 mil views → corrida do ouro, distribuição muito desigual.
- Nossa vantagem: dado oficial com gráfico de verdade + número calculado por nós (microdados do SCF 2025, publicado pelo Fed em 09/10/2026; SSA; BLS; Censo). Os concorrentes citam o resumo; nós mostramos o percentil exato por idade.
- Regra dura: nada de urgência falsa nem boato ("checks stopping", "born before 1967", "new bill gives $4,188"). Sempre "educational, not financial advice" na descrição. Sem mascote: visual limpo, texto grande, ritmo ~140 wpm.
- Filtro de pauta (0–2 cada, entra com ≥8/10): 1) é o dinheiro do espectador na aposentadoria; 2) ele se posiciona (onde estou?); 3) dado oficial recente + cálculo nosso; 4) prova de demanda: canal <50 mil inscritos com ≥100 mil views no ângulo nos últimos 12 meses; 5) vale por 6 meses ou mais.
- Cadência: 1 longo/dia a partir de 03/11, 15:00Z (12:00 BRT = 10:00 ET), na cota do modelo que o Chartbound não usar (Chartbound 3.1 / B 3.8); até 10 pedidos → pode ir a ~12 min. 2 cortes (17:00 e 21:00 BRT). Faixa polonesa do Chartbound só com sobra de cota.
- Lançamento (02/11): renomear canal e @ no Studio (nome e @ "Nest Egg Atlas"/@nesteggatlas, sem concorrente com esse nome no q10), descrição, banner e avatar novos; antes do 1º vídeo, deixar PRIVADOS os vídeos antigos de tecnologia (B-L01, B-L02 + cortes + Shorts) — reversível, Kauan avisado 01/11.
- Testes: B1 formato "onde você está" × "quantos têm X" (views 7 dias) · B2 miniatura número+barra de percentil × só texto (clique) · B3 duração 8 × 12 min (retenção e RPM depois do YPP) · B4 horário 15:00Z × 20:00Z.
- Datas: 15/11 (~12 longos: mediana <500 views em 7 dias e nenhum ≥5 mil → trocar formato) · 15/12 (ritmo de inscritos e horas para o YPP) · regra nova do YPP em 01/02/2027.

| id | tema | estado | publicação |
|---|---|---|---|
| B-N01 | Net Worth at 55, 65 and 75: The Fed's New Numbers (Where Do You Rank?) | agendado (OS94QbIKvWw, render 41477075491 gemini-2.5-flash-preview-tts/Algieba, 8:15) · cortes e7hQSkqSnnM (20:30Z), Ou6IdtVIiMI (03/11 00:00Z) · tela final: inscrição + vídeo específico B-N02 sobre o card COMING NEXT (03/11; fica 'melhor p/ espectador' até o B-N02 ficar público) | 02/11 18:30Z |
| B-N02 | How Many Retirees Actually Have $1 Million? (New Fed Data) | agendado (0KMtZW6mnmA, 8:34, renders 41602647484 / 41604889922 sem novo TTS) · cortes wcOw24o327A, 9hgo6eUcWDg · tela final: inscrição + B-N01 sobre o card (03/11) · sem teste A/B (canal com 6 inscritos não gera impressões p/ decidir) | 03/11 18:30Z |
| B-N03 | Social Security at 62, 67 or 70? The Break-Even Ages, From SSA's Own Data (COLA 2027 3,6%; tabela 6.B5.1: 45% aos 62 em 2008 → 23% em 2024; tábua 2023: 62→80⅓ H 60% M 71% casal 88%; regra do viúvo 82,5%) | roteiro 03/11: 1.288 palavras, 7 atos, Algieba, 37 checks ok · miniatura out/thumbs/b03_text.jpg · WATCH NEXT → B-N02 · teste visual edge 41614703544 | 04/11 18:30Z |
| B-N04 | What Retirees Actually Spend Each Month (BLS CE 65+) | banco | |
| B-N05 | The Income That Puts You in the Top 10% of Retirees (Censo CPS ASEC) | banco | |

- 02/11 12:20Z FEITO no Studio: nome "Nest Egg Atlas", @nesteggatlas (livre), descrição nova, banner e avatar (out/brandB/). Canal tinha 6 inscritos, 63 envios (todos de tecnologia; Shorts até 1.220 views, longos 3 views).
- 02/11 16:00Z FEITO (pedido do Kauan "apaga ou deixa privado"): 48 vídeos antigos públicos → privados (ytchan run 41476758663). Nada apagado. NÃO usar all=1 com vídeo agendado no canal.
- Cota de voz: gemini-2.5-flash-preview-tts funciona com Algieba (126 wpm, tom 4,4) como 3ª opção; 2.5-pro dá 429.

## B · How It Ticks (arquivado 01/11 — vídeos ficam privados no lançamento do Nest Egg Atlas)
| id | tema | estado | publicação |
|---|---|---|---|
| B-L01 | Tiny math errors that cost lives and millions | publicado (DJEANTgbtD0) | 29/10 18:40Z |
| B-L02 | Where did 69 GB of my 1 TB drive go? | agendado (_SgVH8bGG5k) · cortes -rmnWT3Jz6w, 17341VgauLg, ZLsxAGFVY-k, 9EkUwdLL7wo | 30/10 20:00Z |
| B-L03 | GPS só funciona por causa de Einstein | CANCELADO 30/10 (tema saturado: Veritasium, minutephysics) | — |
| B-L04 | Por que aviões não voam em linha reta (círculo máximo, Globe) | ideia | 01/11 |
| B-L05 | QR code rasgado que ainda lê (Reed–Solomon 7/15/25/30%) | ideia | |
