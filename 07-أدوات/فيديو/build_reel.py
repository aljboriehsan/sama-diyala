# Builds a vertical reel (1080x1920, 30 fps) from clip segments cut on the music beat,
# with the small logo on top, city labels, and an end card.
# Usage: python3 build_reel.py <config.json>
import json, subprocess, sys, os, hashlib

cfg = json.load(open(sys.argv[1]))
base = os.path.dirname(os.path.abspath(sys.argv[1]))
P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)

segs = cfg["segments"]            # [{src, start, dur, label?}]
music, m_off = P(cfg["music"]), cfg["music_offset"]
total = sum(s["dur"] for s in segs)
W, H, FPS = 1080, 1920, 30

inputs, filters = [], []
cum = 0.0
stab = cfg.get("stabilize", False)
cache = os.path.join(base, ".cache"); os.makedirs(cache, exist_ok=True)
for i, s in enumerate(segs):
    # "end" = end of the source shot: a shot shorter than dur is slowed down to fill it (no cut inside a segment)
    sp = min(1.0, (s["end"] - s["start"]) / s["dur"]) if "end" in s else 1.0
    win = s["dur"] * sp
    src_in = ["-ss", str(s["start"]), "-t", str(win + 0.2), "-i", P(s["src"])]
    inputs += src_in
    n = int(round((cum + s["dur"]) * FPS)) - int(round(cum * FPS))   # frame-exact cumulative cuts
    cum += s["dur"]
    z = s.get("zoom", 0.05)
    pre = ""
    if stab and s.get("stab", True):   # two-pass vid.stab on the exact source window (per-segment "stab": false skips it)
        trf = os.path.join(cache, f"stab_{hashlib.md5(f'{s["src"]}|{s["start"]}|{win:.3f}'.encode()).hexdigest()[:12]}.trf")
        if not os.path.exists(trf):
            subprocess.run(["ffmpeg", "-v", "error", "-y"] + src_in + ["-vf", f"vidstabdetect=shakiness=8:accuracy=15:result={trf}", "-f", "null", "-"], check=True)
        pre += f"vidstabtransform=input={trf}:smoothing=20:optzoom=1:interpol=bicubic,"
    if sp < 0.999:
        pre += f"setpts=(PTS-STARTPTS)/{sp:.4f},minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,"
    # zoom on a 2x canvas so the push-in moves in half-pixel steps (no stair-step wobble)
    filters.append(
        f"[{i}:v]{pre}fps={FPS},scale={2*W}:{2*H}:flags=lanczos,setsar=1,"
        f"zoompan=z='1+{z}*on/{n}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
        f"trim=end_frame={n},setpts=PTS-STARTPTS,"
        f"eq=contrast=1.04:saturation=1.06,unsharp=5:5:0.4[v{i}]")
k = len(segs)
filters.append("".join(f"[v{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0[base]")

# overlays
idx = k
ov_inputs, chain, last = [], [], "base"
def add_input(path):
    global idx
    ov_inputs.extend(["-loop", "1", "-t", str(total), "-i", P(path)])
    idx += 1
    return idx - 1

t_end = total - cfg["end_card_dur"]
# small logo
li = add_input(cfg["logo"])
chain.append(f"[{li}:v]format=rgba,colorchannelmixer=aa=0.88[lg]")
chain.append(f"[{last}][lg]overlay=x=(W-w)/2:y={cfg.get('logo_y',150)}:enable='lt(t,{t_end+0.15})'[o0]"); last = "o0"
# city labels (consecutive segments with the same label share one label)
t, groups = 0.0, []
for s in segs:
    lab = s.get("label")
    if lab and groups and groups[-1][0] == lab and abs(groups[-1][2] - t) < 1e-6:
        groups[-1][2] = t + s["dur"]
    elif lab:
        groups.append([lab, t, t + s["dur"]])
    t += s["dur"]
for j, (lab, a, b) in enumerate(groups):
    ii = add_input(cfg["labels"][lab])
    chain.append(f"[{ii}:v]format=rgba,fade=t=in:st={a}:d=0.2:alpha=1,fade=t=out:st={b-0.2}:d=0.2:alpha=1[lb{j}]")
    chain.append(f"[{last}][lb{j}]overlay=x=0:y={H-cfg.get('label_bottom',560)}:enable='between(t,{a},{b})'[o{j+1}]"); last = f"o{j+1}"
# timed full-frame overlays: [{img, start, end, fade_in?, fade_out?, rise?}] (rise = px it slides up while fading in)
for j, ov in enumerate(cfg.get("overlays", [])):
    oi = add_input(ov["img"])
    a, b = ov["start"], ov["end"]; ofi, ofo, r = ov.get("fade_in", 0), ov.get("fade_out", 0.3), ov.get("rise", 0)
    f = "format=rgba" + (f",fade=t=in:st={a}:d={ofi}:alpha=1" if ofi else "") + f",fade=t=out:st={b-ofo}:d={ofo}:alpha=1"
    chain.append(f"[{oi}:v]{f}[ov{j}]")
    y = f"'{r}*pow(max(0,1-(t-{a})/{ofi}),2)'" if r and ofi else "0"
    chain.append(f"[{last}][ov{j}]overlay=x=0:y={y}:eval=frame:enable='between(t,{a},{b})'[ovo{j}]"); last = f"ovo{j}"
# end card
ei = add_input(cfg["end_card"])
chain.append(f"[{ei}:v]format=rgba,fade=t=in:st={t_end+0.1}:d=0.45:alpha=1[ec]")
chain.append(f"[{last}][ec]overlay=0:0:enable='gte(t,{t_end})'"+(f",fade=t=in:st=0:d={cfg['fade_in']}" if cfg.get('fade_in') else "")+",format=yuv420p[vout]")

ai = idx
audio = ["-ss", str(m_off), "-t", str(total), "-i", music]
fo = cfg.get("music_fade_out", 1.8)   # 0 = let the track end naturally
af = f"[{ai}:a]afade=t=in:st=0:d=0.05" + (f",afade=t=out:st={total-fo}:d={fo}" if fo else "") + "[aout]"

cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ov_inputs + audio + [
    "-filter_complex", ";".join(filters + chain + [af]),
    "-map", "[vout]", "-map", "[aout]", "-t", str(total),
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", P(cfg["out"])]
subprocess.run(cmd, check=True)
print("ok", round(total, 2), "s ->", cfg["out"])
