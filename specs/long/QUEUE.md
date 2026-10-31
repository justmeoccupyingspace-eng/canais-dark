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
- Shorts: os templated antigos (Etiópia 746, Egito ~790) superam os cortes do longo (5–135). Cortes não são o canal de descoberta; servem de vitrine para o longo.

## Telas finais / cards (estado 31/10 01:40Z)
- Poland (XGmxZPO8lx8): tela final → Korea + inscrição; cards: Korea 7:21, Ireland 4:47 ("Europe's richest? Not really").
- Korea (PP9J1_ZcpBo): tela final → Poland + inscrição.
- Ireland (EpQQtd0o78Q): tela final → Korea (bate com o "watch next 0.72" do outro) + inscrição; card Poland 5:30.
- B-L02 (_SgVH8bGG5k): tela final → B-L01 (bate com o "watch next 0.1+0.2") + inscrição.
- Regra: o vídeo da tela final tem que ser o mesmo do "WATCH NEXT" renderizado no outro; setar no Studio no dia da publicação.

## TikTok C (alerta 31/10)
- Template escuro (gabgen) zerou: MDC 29/10 19:30, negação 30/10 12:30, Pitágoras 30/10 19:30 = 0 views (MDC com 27 h). Antes: 107–219 por post. Template claro do Kauan segue com views (111, 34).
- Agendados c-318…c-331 (02–08/11, 12:30/19:30) são todos template escuro. Se 31/10 12:30 (Excel) e 19:30 (colocação) também ficarem em 0 após 3 h, o template está sendo filtrado → trocar visual/áudio antes de 02/11 (agendado no TikTok não edita, só apaga — apagar é do Kauan).

## A · Chartbound
| id | tema | estado | publicação |
|---|---|---|---|
| A-L01 | Poland passed Japan | publicado | 27/10 |
| A-L02 | South Korea's scariest number | publicado (PP9J1_ZcpBo) | 29/10 18:40Z |
| A-L03 | Ireland is the richest country in Europe. It isn't. | agendado (EpQQtd0o78Q) · cortes 6z26Abz-OT4, ScvCTM6mp9s, uxy6Av-fHBw, MmF-8_Niq0I | 30/10 18:00Z |
| A-L04 | Latvia Lost 30% of Its People. There Was No War. | agendado (LinIPuj7wDI) · cortes 9NsLyIXALV4, xAsXXbTTBAY, APX7b0usW5M, ScuyYnuARNU | 31/10 18:00Z |
| A-L05 | Saudi Arabia Is No Richer Than in 1990 (Golfo) | agendado (s7VEEc8S61c, voz Charon no 3.8, 8:02) · cortes TZSIH-yJFQI, wdyKVv2WiXo | 31/10 23:00Z |
| A-L06 | Portugal Was Richer Than Eastern Europe. Not Anymore. (Polônia à frente em PPP 2025; Eslovênia/Chéquia/Malta/Lituânia de vez) | roteiro + checks ok (41183488650), 1.124 palavras, voz 3.1 · tela final → Polônia | 01/11 18:00Z |
| A-L07 | Turkey Caught Up With Greece. Despite 50% Inflation. (PPP 2025 empatado; nominal 1,45×) | roteiro + checks ok (41184357770), 1.266 palavras, voz 3.8 · tela final → A-L06 | 01/11 23:00Z (cortes A2) |
| A-L08 | Vietnã passou a Indonésia (PPP e nominal, 2025) | banco: Vietnã tem concorrência (Statrys 941 mil); ângulo da ultrapassagem é novo | |
| A-L09 | Espanha passou o Japão em PIB por pessoa nominal (2024) | banco | |
| ~~Germany~~ / ~~Iene~~ | reprovados no filtro | — | |

Ferramentas de pauta: `mine.yml` (sem input = garimpo de ultrapassagens/quem subiu/quem caiu no WDI; com `dump` = séries do WDI para explorar) → branch mine-<run>. O datamapper do IMF bloqueia os runners (403): para projeção do WEO, snapshot com fonte.

## B · How It Ticks
| id | tema | estado | publicação |
|---|---|---|---|
| B-L01 | Tiny math errors that cost lives and millions | publicado (DJEANTgbtD0) | 29/10 18:40Z |
| B-L02 | Where did 69 GB of my 1 TB drive go? | agendado (_SgVH8bGG5k) · cortes -rmnWT3Jz6w, 17341VgauLg, ZLsxAGFVY-k, 9EkUwdLL7wo | 30/10 20:00Z |
| B-L03 | GPS só funciona por causa de Einstein | CANCELADO 30/10 (tema saturado: Veritasium, minutephysics) | — |
| B-L04 | Por que aviões não voam em linha reta (círculo máximo, Globe) | ideia | 01/11 |
| B-L05 | QR code rasgado que ainda lê (Reed–Solomon 7/15/25/30%) | ideia | |
