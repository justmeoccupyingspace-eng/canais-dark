"""Teste de 3 vozes Gemini para o Nest Egg Atlas (canal B): 1 pedido por voz, mede ritmo e variação de tom."""
import json, os, sys
import numpy as np, soundfile as sf
sys.path.insert(0, "scripts")
import ltts
spec = json.load(open("specs/long/b-N01.json"))
style = spec["voice"]["style"]
text = ("The typical household headed by someone aged fifty-five to sixty-four is worth about four hundred and twelve thousand dollars. "
        "Sixty-five to seventy-four: about four hundred and thirty-one thousand. Seventy-five and older: about five hundred and five thousand, "
        "up thirty-seven percent in just three years. But the typical household hides a huge spread.")
os.makedirs("out_vb", exist_ok=True)
rep = {}
for v in os.environ.get("VOICES", "Gacrux,Sadaltager,Algieba").split(","):
    try:
        x = ltts.gemini_once(text, v, style, os.environ.get("MODEL", "gemini-3.8-flash-tts"))
        sf.write(f"out_vb/{v}.wav", x, ltts.SR)
        m = ltts.metrics(x, len(text.split()))
        rep[v] = m; print(v, m)
    except Exception as e:
        rep[v] = {"erro": repr(e)[:300]}; print(v, "erro", repr(e)[:300])
json.dump(rep, open("out_vb/report.json", "w"), indent=1, default=float)
