"""Música original sintetizada para el video (sin muestras ni material de terceros).
Estilo: corporativo / tecnológico suave, 96 BPM, progresión I–V–vi–IV en Re mayor."""
import sys
import numpy as np
import wave

SR = 44100
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 264.0
OUT = sys.argv[2] if len(sys.argv) > 2 else 'musica.wav'
N = int(SR * DUR)
BPM = 96
BEAT = 60 / BPM
BAR = 4 * BEAT
rng = np.random.default_rng(7)

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

# Acordes (MIDI): D, A, Bm, G
CHORDS = [
    (50, [62, 66, 69, 74]),   # D
    (45, [61, 64, 69, 73]),   # A
    (47, [62, 66, 71, 74]),   # Bm
    (43, [62, 67, 71, 74]),   # G
]
L = np.zeros(N); R = np.zeros(N)

def add(buf, start, sig):
    i = int(start * SR)
    if i >= N: return
    j = min(N, i + len(sig))
    buf[i:j] += sig[:j - i]

def env_adsr(n, a, r, sus=1.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4))
    rel = n / SR - r
    e = np.where(t > rel, e * np.clip(1 - (t - rel) / r, 0, 1), e)
    return e * sus

# Intensidad por secciones (alineada con las escenas del video)
def nivel(t, partes):
    for a, b, v in partes:
        if a <= t < b: return v
    return 0.0

DRUMS = [(38, 171.5, 1.0), (178.5, 250.0, 1.0)]
ARP = [(10, 256, 1.0)]
BASS = [(20, 256, 1.0)]

n_bars = int(np.ceil(DUR / BAR)) + 1
for b in range(n_bars):
    t0 = b * BAR
    if t0 >= DUR: break
    root, notes = CHORDS[b % 4]
    # --- Pad: sierras desafinadas con pocos armónicos (cálidas) ---
    n = int((BAR + 1.2) * SR)
    t = np.arange(n) / SR
    e = env_adsr(n, 0.6, 1.2)
    for k, m in enumerate(notes):
        f = hz(m)
        for side, det in ((0, -0.08), (1, 0.08)):
            s = np.zeros(n)
            for d in (-det, 0, det):
                ff = f * 2 ** (d / 12)
                ph = rng.uniform(0, 2 * np.pi)
                for h in range(1, 7):
                    s += np.sin(2 * np.pi * ff * h * t + ph * h) / h ** 1.6
            s *= e * 0.018 * (1 + 0.15 * np.sin(2 * np.pi * 0.2 * t + k))
            add(L if side == 0 else R, t0, s)
    # --- Bajo: corcheas con raíz y quinta ---
    if nivel(t0, BASS):
        for i in range(8):
            m = root if i not in (3, 7) else root + 7
            nb = int(BEAT / 2 * SR * 0.95)
            tt = np.arange(nb) / SR
            f = hz(m)
            s = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt) + 0.12 * np.sin(6 * np.pi * f * tt))
            s *= np.exp(-tt * 3.5) * np.minimum(1, tt / 0.005) * env_adsr(nb, 0.003, 0.03)
            s *= 0.16 if i % 2 == 0 else 0.11
            add(L, t0 + i * BEAT / 2, s); add(R, t0 + i * BEAT / 2, s)
    # --- Arpegio pulsado (campana suave) con eco ---
    if nivel(t0, ARP):
        pat = [0, 1, 2, 3, 2, 1, 2, 3, 0, 2, 1, 3, 2, 3, 1, 2]
        for i, p in enumerate(pat):
            if b < 8 and i % 2: continue  # más espaciado al inicio
            m = notes[p] + 12
            nb = int(0.9 * SR)
            tt = np.arange(nb) / SR
            f = hz(m)
            s = (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 5) + 0.3 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 9)
                 + 0.08 * np.sin(2 * np.pi * 3.01 * f * tt) * np.exp(-tt * 14))
            s *= np.minimum(1, tt / 0.004) * 0.05
            pan = 0.5 + 0.35 * np.sin(i * 0.9)
            st = t0 + i * BEAT / 4
            add(L, st, s * (1 - pan) * 1.4); add(R, st, s * pan * 1.4)
            # eco de corchea con puntillo, alternando lados
            add(R, st + BEAT * 0.75, s * 0.32 * (1 - pan) * 1.4); add(L, st + BEAT * 1.5, s * 0.16 * pan * 1.4)
    # --- Batería suave ---
    if nivel(t0, DRUMS):
        for i in range(4):
            st = t0 + i * BEAT
            # bombo
            nb = int(0.35 * SR); tt = np.arange(nb) / SR
            f = 45 + 75 * np.exp(-tt * 30)
            k = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) * 0.32
            if i in (0, 2) or (i == 3 and b % 2):
                add(L, st if i != 3 else st + BEAT / 2, k); add(R, st if i != 3 else st + BEAT / 2, k)
            # palmada / caja suave en 2 y 4
            if i in (1, 3):
                nb = int(0.25 * SR); tt = np.arange(nb) / SR
                nz = rng.standard_normal(nb)
                nz = np.convolve(nz, np.ones(6) / 6, 'same') - np.convolve(nz, np.ones(40) / 40, 'same')
                c = nz * np.exp(-tt * 18) * 0.10 + np.sin(2 * np.pi * 190 * tt) * np.exp(-tt * 25) * 0.05
                add(L, st, c * 0.9); add(R, st, c)
            # platillo cerrado en contratiempos
            for o in (0.5,):
                nb = int(0.08 * SR); tt = np.arange(nb) / SR
                nz = np.diff(rng.standard_normal(nb + 1))
                hh = nz * np.exp(-tt * 55) * 0.035
                add(L, st + o * BEAT, hh * 0.8); add(R, st + o * BEAT, hh)

# --- Bombeo suave del pad con el bombo (sensación de pulso) ---
t_all = np.arange(N) / SR
phase = (t_all % BEAT) / BEAT
duck = 1 - 0.18 * np.exp(-phase * 6)
on = np.zeros(N)
for a, b, v in DRUMS:
    on[int(a * SR):int(min(b, DUR) * SR)] = 1
L *= np.where(on > 0, duck, 1); R *= np.where(on > 0, duck, 1)

# --- Reverberación por convolución (cola de ruido decreciente) ---
def reverb(x, seed, secs=2.6, mix=0.22):
    nir = int(secs * SR)
    t = np.arange(nir) / SR
    ir = np.random.default_rng(seed).standard_normal(nir) * np.exp(-t * 3.2)
    ir = np.convolve(ir, np.ones(8) / 8, 'same')  # más oscura
    ir /= np.sqrt(np.sum(ir ** 2))
    size = 1 << int(np.ceil(np.log2(len(x) + nir)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[:len(x)]
    return x + mix * y

L = reverb(L, 1); R = reverb(R, 2)

# --- Entrada y salida con fundido ---
fade_in = np.minimum(1, t_all / 2.5)
fade_out = np.clip((DUR - t_all) / 7.0, 0, 1)
L *= fade_in * fade_out; R *= fade_in * fade_out

# --- Normalización suave ---
st = np.stack([L, R], axis=1)
st = np.tanh(st / np.max(np.abs(st)) * 1.2) / np.tanh(1.2)
st *= 0.89
pcm = (st * 32767).astype(np.int16)
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('ok', OUT, DUR)
