#!/usr/bin/env bash
# Pone una canción de fondo al video, con entrada y salida suaves.
# Uso: ./agregar_cancion.sh medialuna.mp3 [segundo_de_inicio]
#   segundo_de_inicio: desde qué parte de la canción empezar (por defecto 0,
#   p. ej. 45 para arrancar en el coro).
set -euo pipefail
cd "$(dirname "$0")"
CANCION="${1:?Indica el archivo de la canción, p. ej. ./agregar_cancion.sh medialuna.mp3}"
INICIO="${2:-0}"
[ -f te_amo_eileen.mp4 ] || python3 generar_video.py
ffmpeg -y -loglevel error -i te_amo_eileen.mp4 -ss "$INICIO" -i "$CANCION" \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k \
  -af "afade=t=in:st=0:d=1.5,afade=t=out:st=17.5:d=2.5" -shortest \
  -movflags +faststart te_amo_eileen_con_musica.mp4
echo "Listo: te_amo_eileen_con_musica.mp4"
