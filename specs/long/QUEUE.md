# Fila de vídeos longos (1 por canal por dia)

Rotina diária (cota Gemini zera ~07:00Z até 1/nov; depois ~08:00Z):
1. ~07:10Z disparar `longo.yml` mode=full para o A (gemini-3.1-flash-tts-preview, Charon) e o B (gemini-3.8-flash-tts, Iapetus).
2. Revisar preview (sheet, gates, loudness, frames com texto). Correção só de texto → `prep_run=<run>` (lpatch aplica sem gastar cota).
3. Agendar: A às 18:00Z, B às 20:00Z do dia seguinte (`upload=A|B`, `at=`). Thumbnail: o Kauan sobe à mão até verificar o canal.
4. Short do dia de cada canal = teaser do longo (mesmo tema, "vídeo completo no canal").

Limite: ≤10 pedidos/dia por modelo; cada ato ≤210 palavras = 1 pedido (roteiro de ~1.150 palavras ≈ 7–9 pedidos).

## A · Chartbound
| id | tema | estado | publicação |
|---|---|---|---|
| A-L01 | Poland passed Japan | publicado | 27/10 |
| A-L02 | South Korea's scariest number | agendado | 30/10 18:00Z |
| A-L03 | Ireland is the richest country in Europe. It isn't. | roteiro + dados ok | 31/10 18:00Z |
| A-L04 | Bulgaria/Latvia: os países que estão sumindo (pop. WB) | ideia | 01/11 |
| A-L05 | Germany, sick man of Europe again? (PIB 2023–25) | ideia | 02/11 |
| A-L06 | O iene que derreteu (JPY, juros BoJ) | ideia | |

## B · How It Ticks
| id | tema | estado | publicação |
|---|---|---|---|
| B-L01 | Tiny math errors that cost lives and millions | render | 30/10 20:00Z |
| B-L02 | Where did 69 GB of my 1 TB drive go? | roteiro ok | 31/10 20:00Z |
| B-L03 | GPS só funciona por causa de Einstein (38 µs/dia ≈ 10 km) | ideia | 01/11 |
| B-L04 | Por que aviões não voam em linha reta (círculo máximo, Globe) | ideia | 02/11 |
| B-L05 | QR code rasgado que ainda lê (Reed–Solomon 7/15/25/30%) | ideia | |
