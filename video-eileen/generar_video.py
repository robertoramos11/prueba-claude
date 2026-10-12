"""Genera un video romántico "Te amo Eileen" a partir de foto.jpg.

Uso:
    python3 generar_video.py                 # crea te_amo_eileen.mp4 (sin música)
    ./agregar_cancion.sh medialuna.mp3       # le pone la canción de fondo
"""
import math
import random
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = Path(__file__).parent
FOTO = AQUI / "foto.jpg"
SALIDA = AQUI / "te_amo_eileen.mp4"

W, H = 1440, 1080
FPS = 30
DURACION = 20.0
N = int(FPS * DURACION)

FUENTE_TE_AMO = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
FUENTE_NOMBRE = "/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf"

# Paleta tomada de la foto: rosa de las rosas, crema del papel, verde del jardín
ROSA = (236, 72, 140)
ROSA_CLARO = (255, 182, 208)
CREMA = (255, 240, 232)

random.seed(14)


def suave(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def tramo(t, a, b):
    return suave((t - a) / (b - a))


# ---------- Etalonaje "de amor" ----------
def etalonar(img):
    a = np.asarray(img).astype(np.float32) / 255.0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # Calidez rosada: sube rojos, baja un poco verdes, sombras con tinte magenta
    r = r * 1.06 + 0.03
    g = g * 0.95 + 0.01
    b = b * 0.98 + 0.035
    a = np.stack([r, g, b], -1)
    # Contraste suave tipo película y negros levantados
    a = 0.04 + 0.92 * (a + 0.12 * (a - 0.5) * (1 - np.abs(2 * a - 1)))
    # Saturar un poco los rosas sin quemar el verde
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2])[..., None]
    rosidad = np.clip((a[..., 0] - a[..., 1]) * 2.5, 0, 1)[..., None]
    a = lum + (a - lum) * (0.92 + 0.35 * rosidad)
    a = np.clip(a, 0, 1)
    base = Image.fromarray((a * 255).astype(np.uint8))

    # Brillo difuso (bloom) en altas luces
    luces = base.point(lambda v: max(0, v - 170) * 3)
    luces = luces.filter(ImageFilter.GaussianBlur(28))
    base = Image.fromarray(
        np.clip(np.asarray(base, np.float32) + np.asarray(luces, np.float32) * 0.35
                * np.array([1.0, 0.82, 0.88]), 0, 255).astype(np.uint8))
    return base


def viñeta(w, h):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
    m = np.clip((d - 0.55) / 0.85, 0, 1) ** 1.6
    capa = np.zeros((h, w, 4), np.uint8)
    capa[..., 0], capa[..., 1], capa[..., 2] = 120, 20, 60
    capa[..., 3] = (m * 170).astype(np.uint8)
    return Image.fromarray(capa, "RGBA")


def fuga_de_luz(w, h):
    """Destellos cálidos en las esquinas, como luz de tarde."""
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.ellipse((-w * 0.25, -h * 0.35, w * 0.35, h * 0.35), fill=(255, 150, 190, 90))
    d.ellipse((w * 0.75, h * 0.65, w * 1.3, h * 1.3), fill=(255, 120, 170, 80))
    return capa.filter(ImageFilter.GaussianBlur(120))


# ---------- Corazones ----------
def corazon(tam, color, alfa=255, contorno=0):
    s = 4  # supermuestreo para bordes suaves
    lienzo = Image.new("RGBA", (tam * s, tam * s), (0, 0, 0, 0))
    pts = []
    for i in range(200):
        t = i / 200 * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((tam * s / 2 + x * tam * s / 36, tam * s / 2.15 - y * tam * s / 36))
    d = ImageDraw.Draw(lienzo)
    if contorno:
        d.line(pts + [pts[0]], fill=color + (alfa,), width=contorno * s, joint="curve")
    else:
        d.polygon(pts, fill=color + (alfa,))
    return lienzo.resize((tam, tam), Image.LANCZOS)


def con_brillo(sprite, radio, fuerza=1.0):
    glow = sprite.filter(ImageFilter.GaussianBlur(radio))
    if fuerza != 1.0:
        a = np.asarray(glow).copy()
        a[..., 3] = np.clip(a[..., 3] * fuerza, 0, 255)
        glow = Image.fromarray(a, "RGBA")
    out = Image.new("RGBA", sprite.size, (0, 0, 0, 0))
    out.alpha_composite(glow)
    out.alpha_composite(sprite)
    return out


class Particula:
    def __init__(self):
        self.reiniciar(primera=True)

    def reiniciar(self, primera=False):
        self.tam = random.choice([18, 22, 28, 34, 42, 54])
        self.x = random.uniform(0, W)
        self.y = random.uniform(0, H) if primera else H + 60
        self.vel = random.uniform(30, 75) * (self.tam / 40) ** 0.5
        self.fase = random.uniform(0, 2 * math.pi)
        self.amp = random.uniform(10, 40)
        self.alfa = random.uniform(0.45, 0.9)
        color = random.choice([ROSA, ROSA_CLARO, CREMA, (255, 105, 160)])
        base = corazon(self.tam, color)
        self.sprite = con_brillo(base, max(2, self.tam // 6), 1.2)

    def paso(self, dt, t):
        self.y -= self.vel * dt
        if self.y < -80:
            self.reiniciar()
        return (int(self.x + self.amp * math.sin(t * 1.3 + self.fase)), int(self.y))


def bokeh(n):
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    for _ in range(n):
        r = random.randint(20, 70)
        x, y = random.randint(0, W), random.randint(0, H)
        c = random.choice([ROSA_CLARO, CREMA, (255, 200, 150)])
        d.ellipse((x - r, y - r, x + r, y + r), fill=c + (random.randint(25, 60),))
    return capa.filter(ImageFilter.GaussianBlur(6))


# ---------- Texto ----------
def texto_con_brillo(txt, ruta, tam, color=(255, 255, 255)):
    f = ImageFont.truetype(ruta, tam)
    x0, y0, x1, y1 = f.getbbox(txt)
    pad = tam // 2
    w, h = x1 - x0 + pad * 2, y1 - y0 + pad * 2
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    sombra = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).text((pad - x0 + 3, pad - y0 + 5), txt, font=f, fill=(90, 10, 45, 170))
    capa.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(6)))

    brillo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(brillo).text((pad - x0, pad - y0), txt, font=f, fill=ROSA + (255,))
    capa.alpha_composite(brillo.filter(ImageFilter.GaussianBlur(tam // 7)))
    capa.alpha_composite(brillo.filter(ImageFilter.GaussianBlur(tam // 18)))

    ImageDraw.Draw(capa).text((pad - x0, pad - y0), txt, font=f, fill=color + (255,))
    return capa


def con_alfa(img, a):
    if a >= 1:
        return img
    arr = np.asarray(img).copy()
    arr[..., 3] = (arr[..., 3] * max(a, 0)).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def pegar_centrado(fondo, sprite, cx, cy, escala=1.0, alfa=1.0):
    if alfa <= 0.003:
        return
    if escala != 1.0:
        sprite = sprite.resize((max(1, int(sprite.width * escala)),
                                max(1, int(sprite.height * escala))), Image.LANCZOS)
    sprite = con_alfa(sprite, alfa)
    fondo.alpha_composite(sprite, (int(cx - sprite.width / 2), int(cy - sprite.height / 2)))


def main():
    foto = Image.open(FOTO).convert("RGB")
    # Margen extra para el zoom lento (Ken Burns)
    BW, BH = int(W * 1.18), int(H * 1.18)
    base = etalonar(foto.resize((BW, BH), Image.LANCZOS))

    vig = viñeta(W, H)
    fuga = fuga_de_luz(W, H)
    bok = bokeh(18)
    particulas = [Particula() for _ in range(26)]

    t_te_amo = texto_con_brillo("Te amo", FUENTE_TE_AMO, 120)
    t_nombre = texto_con_brillo("Eileen", FUENTE_NOMBRE, 210)
    c_grande = con_brillo(corazon(130, ROSA, 235, contorno=5), 10, 1.6)
    c_mini = con_brillo(corazon(46, ROSA), 6, 1.4)

    ff = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-f", "lavfi", "-t", str(DURACION), "-i", "anullsrc=r=44100:cl=stereo",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(SALIDA),
    ], stdin=subprocess.PIPE)

    # Punto focal: la pareja y el ramo (~ 51% x, 62% y de la foto)
    fx, fy = 0.51, 0.60
    for i in range(N):
        t = i / FPS
        # Zoom lento hacia la pareja
        z = 1.0 + 0.15 * suave(t / DURACION)
        cw, ch = BW / (1.18 * z) * 1.0, BH / (1.18 * z)
        cx = BW / 2 + (fx * BW - BW / 2) * suave(t / DURACION) * 0.5
        cy = BH / 2 + (fy * BH - BH / 2) * suave(t / DURACION) * 0.5
        x0 = min(max(cx - cw / 2, 0), BW - cw)
        y0 = min(max(cy - ch / 2, 0), BH - ch)
        cuadro = base.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert("RGBA")

        # Destello suave que "respira"
        cuadro.alpha_composite(con_alfa(fuga, 0.75 + 0.25 * math.sin(t * 1.1)))
        cuadro.alpha_composite(con_alfa(bok, 0.6 + 0.4 * math.sin(t * 0.7)), (int(math.sin(t * 0.3) * 20), 0))
        cuadro.alpha_composite(vig)

        for p in particulas:
            px, py = p.paso(1 / FPS, t)
            cuadro.alpha_composite(con_alfa(p.sprite, p.alfa * tramo(t, 0.3, 2.5)),
                                   (px - p.tam // 2, py - p.tam // 2))

        # Texto: "Te amo" aparece, luego "Eileen" con un pequeño rebote y latido
        a1 = tramo(t, 2.0, 3.6) * (1 - tramo(t, 18.0, 19.4))
        pegar_centrado(cuadro, t_te_amo, W / 2, 170 - 25 * (1 - tramo(t, 2.0, 3.6)), 1.0, a1)

        a2 = tramo(t, 3.8, 5.4) * (1 - tramo(t, 18.0, 19.4))
        lat = 1 + 0.025 * math.sin(max(0, t - 5.4) * 2 * math.pi / 1.2) * tramo(t, 5.4, 6.5)
        esc = (0.85 + 0.15 * tramo(t, 3.8, 5.4)) * lat
        pegar_centrado(cuadro, t_nombre, W / 2, 330, esc, a2)

        # Corazón que late junto al nombre
        a3 = tramo(t, 5.6, 6.8) * (1 - tramo(t, 18.0, 19.4))
        latido = 1 + 0.12 * max(0, math.sin((t - 5.6) * 2 * math.pi / 1.2)) ** 6
        pegar_centrado(cuadro, c_grande, W / 2, 485, 0.75 * latido, a3 * 0.9)
        for k, dx in enumerate((-300, 300)):
            pegar_centrado(cuadro, c_mini, W / 2 + dx, 340 + 8 * math.sin(t * 2 + k), 1.0,
                           tramo(t, 5.0 + k * 0.3, 6.2 + k * 0.3) * (1 - tramo(t, 18.0, 19.4)))

        rgb = cuadro.convert("RGB")
        # Entrada y salida en blanco rosado
        fade = max(1 - tramo(t, 0.0, 1.6), tramo(t, 18.6, 20.0))
        if fade > 0:
            rgb = Image.blend(rgb, Image.new("RGB", (W, H), (255, 228, 238)), fade)

        ff.stdin.write(rgb.tobytes())
        if i % 60 == 0:
            print(f"cuadro {i}/{N}", flush=True)

    ff.stdin.close()
    ff.wait()
    print("Listo:", SALIDA)


if __name__ == "__main__":
    main()
