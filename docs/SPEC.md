# Formato do spec
Arquivo em `specs/queue/<canal>-<nnn>-<slug>.json`; ao entrar na fila (push), o workflow `produce` gera dados, voz, vídeo e envia.
- `channel`: chartbound | howitticks | valeopreco (tema e voz)
- `publish`: {channel: A|B, privacy: private|unlisted|public}
- `yt`: title, description, tags, lang. Aceita `{first_y} {last_y} {first} {last} {pct} {times}` quando há cena de gráfico com `source`.
- `scenes[]`: `title` (text, sub) · `text` (text) · `stat` (label, value ou value_from, prefix, suffix) · `chart` (kind line|bar, title, subtitle, data[] ou source{fred,from,to,step,round,scale}, note, caption)
- Toda cena: `narration` (voz) e `duration` mínima em segundos (a voz estica se precisar).
- Duração total ideal 25 a 45 s (Shorts).
