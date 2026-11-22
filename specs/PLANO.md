## v5.2 (22/11 23:50Z) — CORREÇÃO: o corte da série Polônia foi precipitado
- Eslovênia FbzDub5I2_8 foi de 19 (08:12Z) para 1.096 views (23:41Z) em 15 h — mesmo padrão da Estônia (263 → 2.081 numa noite). Longo só se julga com 48 h. Hungria (33) segue morta.
- Molde que pega: "X Was N% Richer Than Poland" com N grande (Estônia 46% → 6,4 mil; Eslovênia 71% → 1,1 mil; Hungria 29% → 33). Próximo: A-L34 Tchéquia 87% (specs/long/a-L34.py, checks OK no CI run 45084991111), 23/11 23:00Z.
- Volta: 1 longo/dia do A às 23:00Z enquanto o molde segurar (≥500 views em 48 h na mediana dos 3 últimos). Cota 6/dia = longo A 1 + Shorts A 2 + Shorts B 3. Short A das 20:00Z só quando sobrar envio.
- Próximos países do molde: precisa de dado do FMI fora do imf_v4 (Portugal, Grécia, Letônia, Croácia 25% é fraco). Pesquisar antes de escrever.

## v5.1 (22/11 08:30Z) [cortes de longo REVERTIDOS pela v5.2] — cortes antecipados, sem esperar data
- SÉRIE POLÔNIA (longos do A): MORTA AGORA. Hungria 27 views em ~33 h, Eslovênia 19 em ~9 h (corte era 500 em 48 h). Não espera 24/11. Longos param até a pesquisa achar tema com prova (≥100 mil em canal novo) — Croácia cancelada.
- A Shorts: 3/dia (14:00Z, 17:00Z, 20:00Z) a partir de 23/11, usando o envio que era do longo. Cota 6/dia = A 3 + B 3, cada envio publica em ≤ 48 h (compensa no mesmo dia, nada de empurrar para depois).
- Meta YPP de 31/01 (1.000 inscr. no A): ritmo atual ~1–2 inscr./dia → NÃO chega. Marco 30/11 = 250; hoje 135. Se 30/11 < 250, assume-se perdido e a prioridade passa a ser views de Shorts (10 mi/90 d) nos dois canais.

## PLANO v5 (22/11/2026) — regras duras (Kauan: "mais duro e honesto", "foco é resultado")
Diagnóstico com dados (ytstats até 19/11): Shorts do B de 1:45–2:15 retêm 33–45% (o público sai aos 43–57 s) → o feed não empurra além de ~1–1,6 mil. Shorts do A de ~60 s retêm 78–93% (Alasca 2,8 mil). Longos do A retêm 20–27%; série Polônia decaindo (Hungria 23 views em 27 h).
- B: todo Short novo ≤ 140 palavras (≈50 s; o gerador bloqueia acima disso). 3 Shorts/dia (15:00Z, 19:00Z e 22:00Z). Só "pedaço do Brasil × vizinho" e "estado/região vira país". CORTE 30/11: mediana dos Shorts curtos < 3 mil → trocar o tema do canal.
- A Shorts: 2/dia (14:00Z e 17:00Z), só compra/venda/troca de território e "como um país pequeno aguentou/sobreviveu". ~60 s.
- A longos: 1/dia só enquanto valer. CORTE 24/11: Hungria + Eslovênia + Croácia com mediana < 500 views em 48 h → fim da série Polônia (longos param até achar tema novo pela pesquisa).
- Cota YouTube: 6 envios/dia (B 3 + A 2 + A longo 1). Shorts sem miniatura personalizada (só com "thumb_set": true).
- Compilado longo do B: CORTADO (9 views). Temas abstratos no B: CORTADOS.

# PLANO v4 — RESULTADO (17/11/2026 01:30 BRT). Kauan: "A ÚNICA IMPORTÂNCIA É RESULTADO". Não alavancou → dropa. Pesquisa → replica → mede → corta.

## Formatos ativos (escolhidos por dados de canais NOVOS que cresceram, research/q_probe*_2026-11-17.json)
- B (Nest Egg Atlas → renomear "E Se no Mapa" pelo Studio): Shorts PT "E se...?" no mapa (modelo Hiperfocando: criado 03/11, 12 mil inscr., mediana 142 mil).
  Gerador: specs/ese_pt.py → specs/ese/b-pt-NNN.json → .github/workflows/ese.yml (upload=B). 2 por dia (15:00Z e 21:00Z).
  Longo B: compilação 16:9 dos Shorts (specs/comp/*.json → esecomp.yml, reaproveita voz; capítulos; ≥ 8 min).
- A (Chartbound): Shorts EN "história no mapa" (modelo One Map, One Battle: criado 07/10, 15,6 mil inscr., mediana 60 mil; 77–95 s).
  Gerador: specs/map_en.py → specs/ese/a-en-NNN.json → ese.yml (upload=A). 1 por dia 17:00Z (EUA). Longo A: compilação quando houver 5+.
- Série Polônia/dados longos: RETOMADA em 20/11 (dados: Estônia A-L30 263 → 5.630 em 2 dias; Japão×Itália 841). A = 1 longo/dia (specs/long/a-LNN.py → longo.yml, 23:00Z) + 1 Short/dia (17:00Z). Gêmeos do que performa: 'X Was N% Richer Than Poland. Now Poland Is Ahead' (Estônia, Hungria A-L32).
- Religioso (Fe): arquivado.

## Regras
- Corte: 10 vídeos OU 7 dias com mediana < 1 mil views → largar o formato e testar o próximo da lista de pesquisa (Mapvix: comparações de países 13–26 s sem voz; Runic: história de sobrevivência 20 min).
- Dobrar: vídeo > 10 mil → fazer 3 variações do mesmo tema em 48 h.
- Cotas: Gemini TTS 10/dia/modelo (renova 08:00Z) — B usa 3.1 (2 req/vídeo), A usa 3.8 (1 req/vídeo). YouTube API ~6 uploads/dia (renova 08:00Z).
- Reaproveitar voz: ese.yml input reuse=<run> (só re-renderiza).
- YPP: até 31/01/2027 vale a regra atual (1.000 inscr. + 10 mi de views de Shorts em 90 dias, ou 4.000 h). Meta B: Shorts.

## Agenda publicada (17/11)
- B: Cco17qjuIU0 Uruguai 17/11 14:00Z · QhWbhEEXkhw Acre 17/11 19:30Z · kyXKD4TAY8Y América do Sul 18/11 15:00Z · UjL00ZRCgGI Tordesilhas 18/11 21:00Z · 3AWSP_gZD9c Nordeste 19/11 15:00Z (1º com satélite).
- 17/11 08:11Z: disparados a-en-001..003 (upload A) e b-pt-006..008 (upload B). Compilação b-long-001 (prévia OK, run 44020083445) fica para 18/11 08:10Z (cota de upload: ~6 por dia).
- Fila após 08:00Z de 17/11: a-en-001 (17/11 22:00Z), a-en-002 (18/11 17:00Z), a-en-003 (19/11 17:00Z); b-pt-006 (19/11 21:00Z), b-pt-007 (20/11 15:00Z), b-pt-008 (20/11 21:00Z); compilação b-long-001 (20/11 23:00Z) se a prévia estiver boa.

# PLANO v3 — DINHEIRO PRIMEIRO (07/11/2026 23:55 BRT). Objetivo final do Kauan: monetizar e ter renda.

## 0. Prazo duro descoberto
- YouTube muda o YPP em 01/02/2027 (página oficial support.google.com/youtube/answer/72851 confirma a data; blog oficial de ago/2026, citado por vários sites: novos pedidos passam a precisar de 1.000 inscritos + 8.000 h em 365 dias, ou 20 mi de views de Shorts em 90 dias). Pedidos que chegarem até 31/01/2027 23:59 UTC são avaliados pela regra atual (4.000 h) — fonte AIR Media-Tech, não oficial.
- Chartbound até 31/01 (84 dias): faltam 890 inscritos (10,6/dia; hoje 2–4/dia; viral 31–33/dia) e ~2.870 h (34 h/dia ≈ 900 views de longo/dia a 2:20 de média; hoje 4–5 mil/dia com a onda da Espanha) → INSCRITO é a única restrição. Horas: 1.129, das quais 1.068 do Japão (valem até out/2027).
- Marcos lineares para chegar: 15/11 195 · 30/11 355 · 15/12 515 · 31/12 685 · 31/01 1.000. SE 30/11 < 250 → prazo perdido na prática: Chartbound passa a mirar 8.000 h (2º semestre 2027) e o esforço vai para C.
- Nest Egg Atlas (6 inscr., longos 0–1 view): chance ≈ 0 de YPP antes de 01/02 e depois precisa de 8.000 h → CONGELADO (sem longos, sem shorts); cota do modelo 3.8 vai para a dublagem polonesa do Chartbound. B-N09 (COLA) fica pronto na gaveta.

## 0.1 Ordem por dinheiro
1. C — apostila TJSP: ÚNICA renda possível antes de fev/2027. Janela: inscrições até 10/12, prova 14/03/2027. Kiwify: 8,99% + R$ 2,49 por venda, Pix na hora, sem mensalidade → líquido R$ 33,82 por venda de R$ 39,90. R$ 1.000/mês = 30 vendas. Bloqueios (só o Kauan): conta Kiwify (CPF/banco); OK para virar conta comercial no TikTok (link clicável na bio sem mínimo de seguidores; pessoal exige 1.000). Métrica: vendas/semana e leads/1.000 views. Regras: 0 vendas 7 dias após checkout no ar → trocar isca (planilha grátis) e testar R$ 29,90; ≥ 5 vendas/semana → Promote R$ 30/dia no vídeo de inscrição, cortar se custo por venda > R$ 20.
2. A — Chartbound: corrida até 31/01 (seções 1–7 abaixo continuam valendo, com os marcos acima). Teste de maior alavancagem: faixa de ÁUDIO POLONÊS (Studio → Idiomas tem coluna "Áudio"). 1º no Polônia > Japão (onda já caiu, ~300/dia, risco baixo, analytics por faixa de áudio); SE retenção da faixa PL ≥ inglês em 48 h → Espanha e todo vídeo PL. Também: marca-d'água de inscrição em todos os vídeos (precisa OK do Kauan).
3. B — congelado até prova em contrário.
- Antes do YPP o Chartbound não gera renda nenhuma; RPM real (e o peso do público polonês) só aparece depois de monetizar → medir por país no 1º mês e ajustar temas.

# PLANO ADAPTÁVEL v2 — 07/11/2026 23:40 BRT (dados até 08/11 02:09Z)
Regra geral: toda decisão tem um número que a dispara. Checagens: 11/11, 15/11, 22/11, 06/12 (ytstats + este arquivo). Sem o número, não muda.

## 1. Fatos (medidos)
- Chartbound: 110 inscritos, 73,5 mil views, 1.090 h. Monetização = 1.000 inscr. + 4.000 h → horas 27% feitas, inscritos 11%. INSCRITO é o gargalo.
- Conversão (inscritos por 1.000 views): canal 1,5 · Polônia > Japão 1,5 (84/55 mil) · Shorts 1,2 (11/9 mil, 0 h) · outros longos ~0,7 · Polônia > Espanha ~0,3 (2/6,3 mil). Referência de canal de dados saudável: 4–8.
- Público: 76% das views da Polônia; 82% das views de 1 vídeo; fonte = página inicial (52 mil). Coreia/Taiwan/Argentina (sem Polônia): 11–65 views.
- Retenção: todo longo perde ~50% até 0:52 (36–57% a 10%); Japão 30,9% média.
- Ritmo sem viral: 1,5–3 mil views/dia → 2–4 inscritos/dia. Viral (29–30/10): 31–33/dia.
- Nest Egg Atlas: 6 inscr., longos 0–1 view, busca = 4% (3× o A). TikTok: 103 seg., 80–100 views/post, 1 lead, 0 vendas; Promote R$ 5,60/mil views.
- Studio mostra coluna "Áudio" em Idiomas → o canal aceita FAIXA DE ÁUDIO em outro idioma (dublagem polonesa possível no mesmo vídeo).

## 2. Conta até 1.000
Faltam 890. Views necessárias = 890 / conversão: a 1,5/mil → 593 mil; a 4/mil → 222 mil; a 8/mil → 111 mil.
Sem viral e sem mudar nada: ~2,5/dia → 1.000 em ~12 meses. Com 1 hit/mês tipo Japão (+84) e conversão 1,5: ~5 meses. Com conversão 4/mil + 1 hit/mês: ~2,5 meses (fim de jan). → As DUAS alavancas são necessárias; conversão é a mais barata.

## 3. Alavancas, em ordem de impacto por esforço (cada uma com a métrica que a prova ou derruba)
| # | Alavanca | Ação | Métrica | Alvo | Se falhar |
|---|---|---|---|---|---|
| L1 | Conversão no vídeo | CTA no minuto 1 com gancho de série; lembrete curto no meio; comentário fixado EN+PL no dia; tela final c/ inscrição (A-L21 já assim) | inscritos/1.000 views dos vídeos novos (ytstats, 2 dias de atraso) | ≥ 4 até 15/11 (base 1,5) | testar CTA falado em polonês no vídeo (1 frase) e gancho mais concreto (data do próximo) |
| L2 | Áudio em polonês | faixa de áudio PL no mesmo vídeo (Gemini TTS em polonês, encaixada nos tempos de cada cena) — 1º teste: A-L21 em 09/11; legendas PL via Studio | retenção a 10% e inscr./1.000 do A-L21 vs. A-L17/A-L18; views da Polônia | retenção +10 p.p. OU conversão ≥ 2× | manter só título/descrição PL (custo zero) |
| L3 | Tema = nação que VENCE com público grande em inglês | série Polônia (Itália 08/11, Alemanha, Tchéquia, Coreia) → depois Romênia > Hungria, Croácia > Grécia, Lituânia × Espanha; Índia só com ângulo novo | views em 48 h; % PL | ≥ 2.000 em 48 h em ≥ 2 de 5 vídeos | trocar de nação-âncora pela que melhor converteu (não pela que mais viu) |
| L4 | Intro | número + cruzamento nos 8 s iniciais (regra desde A-L21) | retenção a 0:50 (ytstats 'long') | ≥ 65% (base 36–57) | encurtar para 6 min |
| L5 | Shorts | PAUSADOS desde 08/11 (11 inscr., 0 h, público África/Ásia) | — | reavaliar 22/11 só se L1–L3 estiverem no alvo | ficam pausados |
| L6 | Engajamento | responder os 30 comentários mais votados do Japão (EN/PL) pelo Studio; comentário fixado em todo vídeo PL | comentários/1.000 views; inscr. | ≥ 3/1.000 | parar (custo de tempo) |
| L7 | Página do canal | trailer = Japão; seção 1 = playlist Polônia; descrição EN+PL | inscritos vindos da página do canal (fonte YT_CHANNEL) | qualquer alta | — |
| L8 | Fora do YouTube | 1 comentário/dia com dado em r/poland, r/europe (sem spam) | tráfego EXT_URL (hoje 0) | ≥ 500 views/semana | parar |

## 4. Regras SE/ENTÃO (checagem a checagem)
### 11/11 (3 dias de CTA novo: A-L21 08/11, A-L22 09/11, A-L23 10/11)
- SE inscr./1.000 dos 3 ≥ 4 → L1 confirmada; manter. SENÃO SE ≥ 2 → manter + adicionar frase em polonês no CTA. SENÃO (< 2) → o problema é público, não pedido: priorizar L2 (áudio PL) e testar outra nação-âncora.
- SE A-L21 (Itália) ≥ 5.000 views em 72 h → série Polônia confirmada: 5 próximos todos Polônia/Europa Central. SENÃO SE ≥ 1.500 → alternar Polônia / outra nação vencedora. SENÃO (< 1.500) → a onda polonesa esgotou: ir para L3 com Romênia (próxima maior pool com rivalidade), Índia (ângulo per capita) e Turquia.
- B-N09 (COLA, 08/11): SE ≥ 300 views em 72 h → B vira canal de notícia de busca (2/semana). SENÃO → só o vídeo do Part B 2027 no dia do anúncio; depois decide em 23/11.
### 15/11
- Inscritos: alvo 160 (+50 em 8 dias). SE < 135 → conversão não respondeu: dublagem PL vira padrão em todo vídeo PL; CTA falado em polonês; testar título em polonês como PRINCIPAL (não localizado) em 1 vídeo.
- Retenção a 0:50 dos vídeos novos: SE < 55% em 2 de 3 → L4 falhou: próximo vídeo com 6 min e cold open de 5 s.
- TikTok: SE funil (saudação com amostra + checkout) estiver no ar e ≥ 5 leads/semana → Promote R$ 30 no vídeo de inscrição. SENÃO SE funil no ar e < 5 leads → trocar isca (planilha em vez de amostra) e preço (R$ 29,90). SENÃO (funil não montado) → nada de Promote; só orgânico.
### 22/11
- Inscritos: alvo 230. SE ≥ 230 → rota para 500 em 15/12 está viva; manter. SE 170–229 → manter plano, dobrar L3 (2 nações/semana). SE < 170 → mudança estrutural: avaliar (a) canal falar polonês nativo como padrão de áudio, (b) dobrar frequência com o 2º modelo TTS, (c) buscar 2ª nação-âncora com pool ≥ Polônia (Índia, Turquia, Indonésia/Vietnã em inglês = baixo; México/Brasil em inglês = baixo).
- B: SE nenhum vídeo ≥ 500 views → mothball (sem gasto de cota); cota do 3.8 vai para dublagem PL do A.
- Shorts: só voltam SE houver prova de conversão (≥ 2 inscr./1.000) em algum formato; hoje não há.
### 06/12 (mensal)
- SE inscr. ≥ 350 e h ≥ 2.000 → 1.000 em jan é plausível (P50). SE < 250 → reconsiderar o canal como negócio: horas já estariam ~60%, inscritos ~25%; a saída realista seria mudar de idioma-alvo (canal em polonês) ou mudar o produto (newsletter/afiliado) — decisão do Kauan.

## 5. Cenários (estimativa a partir das taxas medidas, não palpite)
| Cenário | Premissas | Inscritos em 31/12 (P10 / P50 / P90) |
|---|---|---|
| Nada muda | 2,5/dia, 0 virais | 200 / 250 / 400 |
| Plano v2 sem dublagem | conversão 1,5 → 3/mil, 1 vídeo ≥ 20 mil views/mês | 280 / 450 / 800 |
| Plano v2 com dublagem PL funcionando | conversão → 5/mil na Polônia, 1 hit/mês | 350 / 650 / 1.100 |
| Onda polonesa esgota e L3 não acha 2ª nação | 1,5/mil, 1,5 mil views/dia | 180 / 220 / 300 |

## 6. Agenda operacional
- 08/11 05:10 BRT: render A-L21 (7 atos, 3.1) + B-N09 (8 atos, 3.8); sem cortes; A-L21 título/descrição PL; A/B thumbs; telas finais; comentário fixado EN+PL nos dois; agendar TikTok semana 46; planilha TJSP (xlsx) para a isca.
- 09/11: faixa de áudio PL do A-L21 (TTS polonês no 3.8, encaixe por cena, upload em Studio → Idiomas → Polonês → Áudio); A-L22 Polônia × Alemanha; responder 30 comentários do Japão; página do canal (trailer, playlist, descrição).
- Diário: ytstats às 15:30 e 22:20 BRT com as 4 métricas: inscritos, inscr./1.000 por vídeo novo, retenção a 0:50, views 48 h. Registrar neste arquivo na seção 7.

## 7. Registro das checagens
- (vazio — 1ª em 11/11)
