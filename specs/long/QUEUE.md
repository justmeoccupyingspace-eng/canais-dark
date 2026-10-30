# Fila de vídeos longos (1 por canal por dia)

Rotina diária (cota Gemini zera ~07:00Z até 1/nov; depois ~08:00Z):
1. ~07:10Z disparar `longo.yml` mode=full para o A (gemini-3.1-flash-tts-preview, Charon) e o B (gemini-3.8-flash-tts, Iapetus).
2. Revisar preview (sheet, gates, loudness, frames com texto). Correção só de texto → `prep_run=<run>` (lpatch aplica sem gastar cota).
3. Publicar no MESMO dia do render (decisão do Kauan, 29/10): A às 18:00Z, B às 20:00Z (`upload=A|B`, `at=`). Thumbnail: automática pela API (canais verificados em 29/10); conferir a anotação "thumbnail aplicada" no job final.
4. Shorts = 4 cortes do longo do dia (sem cota TTS): `python scripts/mkclips.py specs/long/<x>.json <videoId> <run_final> <run_prep> auto:<publishAt do longo>` → `cortes.yml cfg=specs/clips/<x>.json` (só render) → revisar previews no branch `cortes-<run>` → `cortes.yml use_run=<run> upload=A|B`. Horários (decisão do Kauan 29/10: 2 cortes na noite do longo + 2 na manhã seguinte, antes do próximo longo; Brasília fixo = UTC−3):
   - A: longo 15:00 BRT (18:00Z) → cortes 19:00 e 22:00 BRT (22:00Z, 01:00Z) + 09:00 e 12:00 BRT do dia seguinte (12:00Z, 15:00Z).
   - B: longo 17:00 BRT (20:00Z) → cortes 20:00 e 23:00 BRT (23:00Z, 02:00Z) + 10:00 e 13:00 BRT do dia seguinte (13:00Z, 16:00Z).
   - Noite BRT = tarde/noite nos EUA (maior público); manhã BRT = noite em PH/ID/IN. Se o longo atrasar, mover cortes com `ytresched.yml` (ids, at, ch).

Limite: ≤10 pedidos/dia por modelo; cada ato ≤210 palavras = 1 pedido (roteiro de ~1.150 palavras ≈ 7–9 pedidos).

## A · Chartbound
| id | tema | estado | publicação |
|---|---|---|---|
| A-L01 | Poland passed Japan | publicado | 27/10 |
| A-L02 | South Korea's scariest number | publicado (PP9J1_ZcpBo) | 29/10 18:40Z |
| A-L03 | Ireland is the richest country in Europe. It isn't. | roteiro + dados ok | 30/10 18:00Z |
| A-L04 | Bulgaria/Latvia: os países que estão sumindo (pop. WB) | ideia | 31/10 |
| A-L05 | Germany, sick man of Europe again? (PIB 2023–25) | ideia | 01/11 |
| A-L06 | O iene que derreteu (JPY, juros BoJ) | ideia | |

## B · How It Ticks
| id | tema | estado | publicação |
|---|---|---|---|
| B-L01 | Tiny math errors that cost lives and millions | publicado (DJEANTgbtD0) | 29/10 18:40Z |
| B-L02 | Where did 69 GB of my 1 TB drive go? | roteiro ok | 30/10 20:00Z |
| B-L03 | GPS só funciona por causa de Einstein (38 µs/dia ≈ 11 km) | roteiro ok | 31/10 |
| B-L04 | Por que aviões não voam em linha reta (círculo máximo, Globe) | ideia | 01/11 |
| B-L05 | QR code rasgado que ainda lê (Reed–Solomon 7/15/25/30%) | ideia | |
