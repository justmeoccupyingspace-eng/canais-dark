#!/usr/bin/env bash
# Para cada spec da lista: dados reais -> voz -> render -> upload. Spec pode trazer "publish": {"channel":"A","privacy":"private"}.
set -euo pipefail
mkdir -p out public/build
python3 scripts/fx.py
while read -r f; do
  [ -z "$f" ] && continue
  n=$(basename "$f" .json)
  python3 scripts/data.py "$f" public/build/$n.data.json
  python3 scripts/tts.py public/build/$n.data.json public/build/$n.json
  python3 scripts/audit.py public/build/$n.json || echo "audit falhou (não bloqueia)"
  node scripts/render.mjs public/build/$n.json out/$n.mp4
  ch=$(python3 -c "import json,sys;d=json.load(open('$f'));print(d.get('publish',{}).get('channel',''))")
  pv=$(python3 -c "import json,sys;d=json.load(open('$f'));print(d.get('publish',{}).get('privacy',''))")
  ch=${ch:-${MANUAL_CHANNEL:-A}}; pv=${pv:-${MANUAL_PRIVACY:-private}}
  if [ "$ch" = "C" ]; then
    echo "canal C: sem upload automático; vídeo fica no artefato (out/$n.mp4)"
  elif [ "${MANUAL_UPLOAD:-true}" != "false" ]; then
    python3 scripts/upload.py "$ch" out/$n.mp4 public/build/$n.json "$pv"
  fi
done < "$1"
