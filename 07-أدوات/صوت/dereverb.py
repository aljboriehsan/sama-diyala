# Late-reverberation suppression for a voice recorded in a room (phone / WhatsApp voice notes).
# Spectral subtraction of the estimated late reverb (Lebart et al. 2001): the late reverb at frame t
# is the smoothed power Δ seconds earlier, decayed by the room's T60. numpy only; audio via ffmpeg.
# Usage: python3 dereverb.py <in> <out.wav> [T60 seconds=0.5] [strength=1.0] [floor dB=-14]
import sys, subprocess, numpy as np
src, dst = sys.argv[1], sys.argv[2]
T60 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
BETA = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
FLOOR = 10 ** ((float(sys.argv[5]) if len(sys.argv) > 5 else -14) / 20)
SR, N, HOP, DELTA = 48000, 1024, 256, 0.05
x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                                 capture_output=True, check=True).stdout, dtype=np.float32).astype(np.float64)
win = np.hanning(N)
pad = np.concatenate([np.zeros(N), x, np.zeros(N)])
nf = (len(pad) - N) // HOP + 1
idx = np.arange(N)[None, :] + HOP * np.arange(nf)[:, None]
X = np.fft.rfft(pad[idx] * win, axis=1)
P = np.abs(X) ** 2
# temporal smoothing of the power
Ps = np.empty_like(P); Ps[0] = P[0]
for t in range(1, nf): Ps[t] = 0.55 * Ps[t - 1] + 0.45 * P[t]
d = int(round(DELTA * SR / HOP))
decay = 10 ** (-6 * DELTA / T60)                     # power decay over Δ for the given T60
Pl = np.zeros_like(Ps); Pl[d:] = decay * Ps[:-d]
G = np.maximum(1 - BETA * Pl / np.maximum(Ps, 1e-12), FLOOR ** 2) ** 0.5
for t in range(1, nf): G[t] = np.maximum(G[t], 0.6 * G[t - 1] + 0.4 * G[t]) if False else 0.35 * G[t - 1] + 0.65 * G[t]   # soften musical noise
Y = np.fft.irfft(X * G, n=N, axis=1) * win
y = np.zeros(len(pad)); norm = np.zeros(len(pad))
for t in range(nf):
    y[t * HOP:t * HOP + N] += Y[t]; norm[t * HOP:t * HOP + N] += win ** 2
y = (y / np.maximum(norm, 1e-6))[N:N + len(x)]
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', dst],
               input=y.astype(np.float32).tobytes(), check=True)
print('ok', dst)
