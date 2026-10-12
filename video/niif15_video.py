"""Genera un video explicativo de la NIIF 15 (1920x1080, 30 fps) con Pillow + ffmpeg.

Uso: python3 video/niif15_video.py  ->  video/niif15.mp4
"""
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
OUT = Path(__file__).with_name("niif15.mp4")

# Paleta (verde NIIF 006D77)
BG = (247, 247, 242)
PRIMARY = (0, 109, 119)
SOFT = (131, 197, 190)
PALE = (237, 246, 249)
ACCENT = (226, 149, 120)
INK = (29, 45, 53)
MUTED = (96, 112, 120)
WHITE = (255, 255, 255)

FD = "/usr/share/fonts/opentype/inter/"
_fonts = {}


def font(weight, size):
    key = (weight, size)
    if key not in _fonts:
        name = {"r": "Inter-Regular", "m": "Inter-Medium", "s": "Inter-SemiBold",
                "b": "Inter-Bold", "d": "InterDisplay-Bold"}[weight]
        _fonts[key] = ImageFont.truetype(FD + name + ".otf", size)
    return _fonts[key]


def clamp(x):
    return max(0.0, min(1.0, x))


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def prog(t, start, dur=0.6):
    return ease((t - start) / dur)


def mix(c1, c2, a):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * a) for i in range(3))


def wrap(text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if f.getlength(test) <= width:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, f, color, a=1.0, bg=BG, anchor="la", rise=30):
    if a <= 0:
        return
    x, y = xy
    d.text((x, y + (1 - a) * rise), s, font=f, fill=mix(bg, color, a), anchor=anchor)


def para(d, xy, s, f, color, width, a=1.0, bg=BG, lh=1.35, anchor="la"):
    x, y = xy
    for i, line in enumerate(wrap(s, f, width)):
        text(d, (x, y + i * f.size * lh), line, f, color, a, bg, anchor)


def fmt(n):
    return f"{n:,.0f}".replace(",", ".")


def header(d, t, title, kicker):
    a = prog(t, 0.1)
    d.rectangle([0, 0, W, 10], fill=PRIMARY)
    text(d, (120, 90), kicker.upper(), font("s", 28), PRIMARY, a)
    text(d, (120, 130), title, font("d", 68), INK, a)
    d.rectangle([120, 230, 120 + int(160 * a), 236], fill=ACCENT)


def footer(d):
    d.text((W - 120, H - 60), "NIIF 15 · Ingresos de contratos con clientes",
           font=font("m", 24), fill=MUTED, anchor="ra")


# ---------------- Escenas ----------------

def s_title(d, t):
    band = int(W * 0.42 * ease(t / 0.8))
    d.rectangle([0, 0, band, H], fill=PRIMARY)
    a = prog(t, 0.5, 0.8)
    text(d, (140, 330), "NIIF", font("d", 150), WHITE, a, PRIMARY)
    text(d, (140, 480), "15", font("d", 260), SOFT, a, PRIMARY)
    a2 = prog(t, 1.2, 0.8)
    para(d, (W * 0.42 + 120, 380),
         "Ingresos de actividades ordinarias procedentes de contratos con clientes",
         font("b", 64), INK, 900, a2)
    a3 = prog(t, 2.0, 0.8)
    text(d, (W * 0.42 + 120, 720), "El modelo de cinco pasos, con un ejemplo práctico",
         font("r", 36), MUTED, a3)


def s_principle(d, t):
    header(d, t, "¿Cuándo y por cuánto se reconoce un ingreso?", "Principio básico")
    a = prog(t, 0.8, 0.8)
    box = [120, 320, W - 120, 760]
    if a > 0:
        d.rounded_rectangle(box, 24, fill=mix(BG, PALE, a))
        d.rectangle([120, 320, 132, 760], fill=mix(PALE, PRIMARY, a))
    q = ("Una entidad reconoce los ingresos para representar la transferencia de los "
         "bienes o servicios comprometidos con los clientes, por un importe que refleje "
         "la contraprestación a la que espera tener derecho a cambio de ellos.")
    para(d, (190, 380), q, font("m", 50), INK, W - 440, prog(t, 1.4, 1.0), PALE, 1.45)
    text(d, (190, 690), "NIIF 15, párrafo 2", font("s", 28), PRIMARY, prog(t, 2.6), PALE)
    a4 = prog(t, 4.0, 0.8)
    text(d, (120, 830), "Idea clave: el ingreso se reconoce cuando el cliente obtiene el control.",
         font("s", 40), ACCENT, a4)
    footer(d)


STEPS = [
    ("Identificar el contrato", "con el cliente"),
    ("Identificar las obligaciones", "de desempeño"),
    ("Determinar el precio", "de la transacción"),
    ("Asignar el precio", "a cada obligación"),
    ("Reconocer el ingreso", "al satisfacer cada obligación"),
]


def s_steps(d, t):
    header(d, t, "Modelo de cinco pasos", "Cómo se aplica")
    bw, gap, top = 300, 54, 380
    x0 = (W - (5 * bw + 4 * gap)) // 2
    for i, (l1, l2) in enumerate(STEPS):
        a = prog(t, 1.0 + i * 1.6, 0.7)
        if a <= 0:
            continue
        x = x0 + i * (bw + gap)
        y = top + (1 - a) * 40
        fill = mix(BG, PRIMARY if i == 4 else WHITE, a)
        d.rounded_rectangle([x, y, x + bw, y + 380], 22, fill=fill,
                            outline=mix(BG, PRIMARY, a), width=3)
        on = WHITE if i == 4 else INK
        num_c = SOFT if i == 4 else PRIMARY
        d.text((x + 34, y + 30), str(i + 1), font=font("d", 110), fill=mix(fill, num_c, a))
        para(d, (x + 34, y + 190), l1, font("b", 32), on, bw - 60, a, fill, 1.25)
        para(d, (x + 34, y + 280), l2, font("r", 28), MUTED if i != 4 else PALE,
             bw - 60, a, fill, 1.25)
        if i < 4:
            aa = prog(t, 1.6 + i * 1.6, 0.4)
            if aa > 0:
                ax = x + bw + 10
                ay = top + 190
                d.line([ax, ay, ax + int((gap - 22) * aa), ay], fill=ACCENT, width=6)
                if aa > 0.9:
                    d.polygon([(ax + gap - 20, ay - 12), (ax + gap - 6, ay),
                               (ax + gap - 20, ay + 12)], fill=ACCENT)
    a = prog(t, 10.0, 0.8)
    text(d, (W // 2, 860), "Pasos 1 a 4: cuánto se reconoce   ·   Paso 5: cuándo se reconoce",
         font("m", 34), MUTED, a, anchor="ma")
    footer(d)


def s_example(d, t):
    header(d, t, "Equipo + mantenimiento por Bs 120.000", "Ejemplo · Pasos 1 a 4")
    a = prog(t, 0.6)
    para(d, (120, 280),
         "Una empresa en La Paz vende un equipo industrial e incluye 12 meses de "
         "mantenimiento, por un precio único de Bs 120.000.",
         font("r", 36), INK, W - 240, a)

    cols = [120, 720, 1110, 1430]
    heads = ["Obligación de desempeño", "Precio de venta\nindependiente", "Proporción",
             "Precio asignado"]
    ty = 430
    ah = prog(t, 2.0)
    if ah > 0:
        d.rectangle([120, ty, W - 120, ty + 90], fill=mix(BG, PRIMARY, ah))
        for c, h in zip(cols, heads):
            for k, line in enumerate(h.split("\n")):
                text(d, (c + 24, ty + 18 + k * 32 - (0 if "\n" in h else -14)), line,
                     font("s", 28), WHITE, ah, PRIMARY, rise=0)

    rows = [("Equipo (se entrega hoy)", 100000, "100 / 125", 96000),
            ("Mantenimiento 12 meses", 25000, "25 / 125", 24000),
            ("Total", 125000, "", 120000)]
    for r, (name, pvi, prop, asig) in enumerate(rows):
        ar = prog(t, 3.0 + r * 1.2)
        if ar <= 0:
            continue
        y = ty + 90 + r * 100
        total = r == 2
        rowbg = PALE if total else WHITE
        d.rectangle([120, y, W - 120, y + 100], fill=mix(BG, rowbg, ar))
        d.line([120, y + 100, W - 120, y + 100], fill=mix(BG, SOFT, ar), width=2)
        f = font("b" if total else "m", 34)
        text(d, (cols[0] + 24, y + 30), name, f, INK, ar, rowbg, rise=0)
        text(d, (cols[1] + 24, y + 30), "Bs " + fmt(pvi), f, INK, ar, rowbg, rise=0)
        text(d, (cols[2] + 24, y + 30), prop, f, MUTED, ar, rowbg, rise=0)
        count = ease((t - 7.0 - r * 0.3) / 1.4)
        if count > 0:
            text(d, (cols[3] + 24, y + 30), "Bs " + fmt(asig * count),
                 font("b", 34), PRIMARY if not total else INK, ar, rowbg, rise=0)

    a5 = prog(t, 10.0)
    text(d, (120, 880), "El descuento de Bs 5.000 se reparte en proporción a los precios "
         "de venta independientes.", font("m", 32), ACCENT, a5)
    footer(d)


def s_recognition(d, t):
    header(d, t, "¿En un momento o a lo largo del tiempo?", "Ejemplo · Paso 5")
    lw = (W - 240 - 60) // 2
    for i in range(2):
        a = prog(t, 0.8 + i * 1.0)
        if a <= 0:
            continue
        x = 120 + i * (lw + 60)
        d.rounded_rectangle([x, 300, x + lw, 840], 24, fill=mix(BG, WHITE, a),
                            outline=mix(BG, SOFT, a), width=3)
        kick = ["EN UN MOMENTO DETERMINADO", "A LO LARGO DEL TIEMPO"][i]
        ttl = ["Equipo", "Mantenimiento"][i]
        text(d, (x + 50, 350), kick, font("s", 26), PRIMARY, a, WHITE)
        text(d, (x + 50, 395), ttl, font("d", 60), INK, a, WHITE)

    # Equipo: una sola barra al entregar
    a = prog(t, 2.6)
    if a > 0:
        x = 120
        text(d, (x + 50, 500), "Bs 96.000", font("d", 84), PRIMARY, a, WHITE)
        para(d, (x + 50, 620), "Se reconoce completo cuando el cliente recibe el equipo "
             "y obtiene su control.", font("r", 32), MUTED, lw - 100, a, WHITE)

    # Mantenimiento: 12 meses que se llenan
    a = prog(t, 3.4)
    if a > 0:
        x = 120 + lw + 60
        filled = int(clamp((t - 4.0) / 6.0) * 12 + 0.0001)
        text(d, (x + 50, 500), f"Bs 2.000 × mes", font("d", 84), PRIMARY, a, WHITE)
        cw, cg = 50, 12
        for m in range(12):
            cx = x + 50 + m * (cw + cg)
            col = PRIMARY if m < filled else PALE
            d.rounded_rectangle([cx, 640, cx + cw, 720], 8, fill=mix(WHITE, col, a))
        text(d, (x + 50, 750), f"Reconocido: Bs {fmt(filled * 2000)} de Bs 24.000",
             font("m", 32), INK, a, WHITE, rise=0)
    footer(d)


def s_close(d, t):
    d.rectangle([0, 0, W, H], fill=PRIMARY)
    a = prog(t, 0.3, 0.8)
    text(d, (W // 2, 360), "El ingreso sigue a la transferencia del control",
         font("d", 76), WHITE, a, PRIMARY, anchor="ma")
    a2 = prog(t, 1.2, 0.8)
    items = ["Contrato", "Obligaciones", "Precio", "Asignación", "Reconocimiento"]
    total_w = sum(font("s", 34).getlength(s) for s in items) + 4 * 90
    x = (W - total_w) / 2
    for k, s in enumerate(items):
        text(d, (x, 540), s, font("s", 34), SOFT, a2, PRIMARY)
        x += font("s", 34).getlength(s)
        if k < 4:
            text(d, (x + 45, 540), "→", font("s", 34), ACCENT, a2, PRIMARY, anchor="ma")
            x += 90
    a3 = prog(t, 2.2, 0.8)
    text(d, (W // 2, 760), "Fuente: NIIF 15 (IASB). Video de prueba con fines didácticos.",
         font("r", 28), PALE, a3, PRIMARY, anchor="ma")


SCENES = [(s_title, 5.0), (s_principle, 8.0), (s_steps, 13.0),
          (s_example, 13.5), (s_recognition, 11.5), (s_close, 5.0)]
FADE = 0.4  # fundido a fondo entre escenas


def main():
    total = sum(d for _, d in SCENES)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", str(OUT)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fn, dur in SCENES:
        for i in range(int(dur * FPS)):
            t = i / FPS
            img = Image.new("RGB", (W, H), BG)
            fn(ImageDraw.Draw(img), t)
            fade = min(1.0, t / FADE if fn is not s_title else 1.0,
                       (dur - t) / FADE if fn is not s_close else 1.0)
            if fade < 1.0:
                img = Image.blend(Image.new("RGB", (W, H), BG), img, max(0.0, fade))
            proc.stdin.write(img.tobytes())
    proc.stdin.close()
    proc.wait()
    print(f"{OUT} ({total:.1f} s)")


if __name__ == "__main__":
    main()
