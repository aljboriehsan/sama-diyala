# Voiced paid-ad version (management note 25 Nov 2026: no silent video, add a voice-over and the
# company façade at the start). Office shots cut on the voice-over phrases, burned-in captions,
# the cleaned voice-over (صوت/الفويس أوفر - منظف.wav, made from the WhatsApp recording), office
# sounds low underneath, a light music bed, and the animated end card (both numbers with the WhatsApp logo).
# Outputs 9:16 (Reels/Stories) and a 4:5 crop (Feed).
# Run from the repo root: python3 "14-الفيديو/إعلان ممول - تذكرتك تطلع بدقيقة/build_vo.py"
import subprocess, os, json
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(D))
L = os.path.join(R, '14-الفيديو/مقاطع/المكتب')
FPS, W, H = 30, 1080, 1920
VO = os.path.join(D, 'صوت/الفويس أوفر 2 - الأصل مع إزالة الضجيج فقط.wav')   # 2nd recording as recorded: light afftdn + 5 dB gain only (Ihsan rejected the de-reverb/compression chain)
VO_SS, VO_AT = 1.05, 0.35   # skip the lead-in of the file; the voice starts 0.35 s into the video (first frame is the full façade)
VO_LAST = 21.43             # end of the last word, in file time
# (clip, start, dur, gain dB, blur boxes, source end for a slowed tail)
segs = [
 ('المكتب - الواجهة من الخارج والدخول.mov',  0.00, 6.6, 0,  []),     # "تذكرتك تطلع بدقيقة، من شركة سماء ديالى…" (cut in the pause 6.39–6.92)
 ('المكتب - الحجز على الكيبورد.mov',         0.60, 1.0, 10, [('mask', 'عناصر/قناع الشاشة.png', 20)]),  # "حجزك مضمون…"
 ('المكتب - الطابعة تخرج التذكرة.mov',      0.25, 0.85, 6, [(400, 1030, 420, 280, 7)]),
 ('المكتب - ختم التذكرة.mov',               0.95, 0.9, 7,  [(330, 630, 440, 140, 6), (160, 770, 790, 150, 6)]),
 ('المكتب - وضع التذكرة في الغلاف.mov',     2.20, 1.6, 11, []),     # "شرّفنا بموقع الشركة…" (from 9.35)
 ('المكتب - تسليم التذكرة للزبون.mov',      0.00, 2.4, 11, []),
 ('المكتب - جولة في القاعة وجدار العراقية (بديلة).mov', 0.00, 3.5, 4, []),   # "أو احجز وادفع وانت ببيتك…" (13.35–16.85)
]
t_end = sum(s[2] for s in segs)                    # end card starts here (17.5 s), under "تواصل ويانا…"
vo_len = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', VO], capture_output=True, text=True).stdout)
total = round(VO_AT + VO_LAST - VO_SS + 1.6, 2)     # 1.6 s of end card after the last word
EC = round(total - t_end, 2)
segs.append(('المكتب - جولة في القاعة وجدار العراقية (بديلة).mov', 3.50, EC, 4, [], 8.75))   # rest of the pan, slightly slowed, under the end card
# captions: (start, end, text) in video time = voice-over phrase times + VO_AT
CAPS = [   # video time = file time - 0.70
 (3.00, 6.45, 'من شركة سماء ديالى<br>الوكيل العام للخطوط الجوية العراقية في ديالى'),
 (6.88, 9.20, 'حجزك مضمون، وبالأسعار الرسمية'),
 (9.55, 13.30, 'شرّفنا بموقع الشركة في بعقوبة<br>قرب كراج البحيرة'),
 (13.45, 16.70, 'أو احجز وادفع وانت ببيتك<br>من أي محافظة'),
]
MUSIC = os.path.join(R, '14-الفيديو/موسيقى/lexin_music-inspiring-cinematic-ambient-116199.mp3'); M_START = 5.0   # calm ambient bed under the voice (asked by Ihsan)
CACHE = os.path.join(D, '.cache'); os.makedirs(CACHE, exist_ok=True)

# --- layers: end card frames and caption PNGs
FR = os.path.join(CACHE, 'end_frames_vo')
HK = os.path.join(CACHE, 'hook_vo')   # opening hook on the façade, 0–3 s (asked by Ihsan)
subprocess.run(['node', os.path.join(R, '07-أدوات/فيديو/render_anim.js'), os.path.join(D, 'عناصر/البداية.html'), HK, '3.0', str(FPS)], check=True)
subprocess.run(['node', os.path.join(R, '07-أدوات/فيديو/render_anim.js'), os.path.join(D, 'عناصر/الختام.html'), FR, str(EC), str(FPS)], check=True)
tpl = open(os.path.join(D, 'عناصر/ترجمة.html')).read()
cap_png = []
for i, (a, b, txt) in enumerate(CAPS):
    hp = os.path.join(CACHE, f'cap{i}.html'); open(hp, 'w').write(tpl.replace('{{TEXT}}', txt).replace('_fonts.css', os.path.join(D, 'عناصر/_fonts.css')))
    out = os.path.join(CACHE, f'cap{i}')
    subprocess.run(['node', os.path.join(R, '07-أدوات/فيديو/render_anim.js'), hp, out, '0.04', '25'], check=True)
    cap_png.append(os.path.join(out, '0000.png'))

inp, fv, fa, masks = [], [], [], []
for i, (f, ss, d, g, boxes, *rest) in enumerate(segs):
    src_end = rest[0] if rest else None
    win = (src_end - ss) if src_end else d
    inp += ['-ss', str(ss), '-t', str(win + 0.15), '-i', os.path.join(L, f)]
    n = int(round(d * FPS))
    slow = f'setpts=(PTS-STARTPTS)*{d/win:.4f},minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,' if src_end else ''
    v = f'[{i}:v]{slow}fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,eq=contrast=1.05:saturation=1.06'
    if boxes:
        fv.append(v + f',split={len(boxes)+1}[b{i}' + ''.join(f'][c{i}_{k}' for k in range(len(boxes))) + ']')
        cur = f'b{i}'
        for k, b in enumerate(boxes):
            if b[0] == 'mask':
                masks.append((f'm{i}_{k}', os.path.join(D, b[1])))
                fv.append(f'[c{i}_{k}]boxblur={b[2]}:2,format=rgba[bl{i}_{k}]')
                fv.append(f'[bl{i}_{k}][{{m{i}_{k}}}]alphamerge[bm{i}_{k}]')
                fv.append(f'[{cur}][bm{i}_{k}]overlay=0:0[o{i}_{k}]'); cur = f'o{i}_{k}'
                continue
            x, y, w, h, r = b
            fv.append(f'[c{i}_{k}]crop={w}:{h}:{x}:{y},boxblur={r}:2[bl{i}_{k}]')
            fv.append(f'[{cur}][bl{i}_{k}]overlay={x}:{y}[o{i}_{k}]'); cur = f'o{i}_{k}'
        fv.append(f'[{cur}]trim=end_frame={n},setpts=PTS-STARTPTS[v{i}]')
    else:
        fv.append(v + f',trim=end_frame={n},setpts=PTS-STARTPTS[v{i}]')
    if src_end:   # room tone of the slowed tail at real speed, fading out, padded
        fa.append(f'[{i}:a]atrim=0:{win},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,'
                  f'afade=t=out:st={win-1.0}:d=1.0,apad=whole_dur={d}[a{i}]')
    else:
        fa.append(f'[{i}:a]atrim=0:{d},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,'
                  f'afade=t=in:st=0:d=0.02,afade=t=out:st={d-0.03}:d=0.03[a{i}]')
k = len(segs)
fv.append(''.join(f'[v{i}]' for i in range(k)) + f'concat=n={k}:v=1:a=0[base]')
fa.append(''.join(f'[a{i}]' for i in range(k)) + f'concat=n={k}:v=0:a=1[orig]')

nxt = k
def add(args):
    global nxt
    inp.extend(args); nxt += 1; return nxt - 1
endc = add(['-framerate', str(FPS), '-i', os.path.join(FR, '%04d.png')])
hook = add(['-framerate', str(FPS), '-i', os.path.join(HK, '%04d.png')])
caps_i = [add(['-loop', '1', '-t', str(total), '-i', p]) for p in cap_png]
vo_i = add(['-ss', str(VO_SS), '-i', VO])
mus_i = add(['-ss', str(M_START), '-t', str(total + 0.2), '-i', MUSIC])
for tag, path in masks:
    j = add(['-loop', '1', '-t', str(total), '-i', path])
    fv[:] = [x.replace('{' + tag + '}', f'{j}:v') for x in fv]

fv.append(f'[{hook}:v]format=rgba,setpts=PTS-STARTPTS[hk]')
fv.append("[base][hk]overlay=0:0:eof_action=pass:enable='lt(t,3.0)'[bh]")
cur = 'bh'
for j, ((a, b, _), ci) in enumerate(zip(CAPS, caps_i)):
    fv.append(f'[{ci}:v]format=rgba,fade=t=in:st={a}:d=0.12:alpha=1,fade=t=out:st={b-0.12}:d=0.12:alpha=1[cp{j}]')
    fv.append(f"[{cur}][cp{j}]overlay=0:0:enable='between(t,{a},{b})'[cv{j}]"); cur = f'cv{j}'
fv.append(f'[{endc}:v]format=rgba,setpts=PTS-STARTPTS+{t_end}/TB[ec]')
fv.append(f"[{cur}][ec]overlay=0:0:eof_action=repeat,format=yuv420p[vout]")

vo_end = VO_AT + VO_LAST - VO_SS
fa.append(f"[orig]volume=0.32[od]")                                         # office sounds low under the voice
fa.append(f'[{vo_i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(VO_AT*1000)}|{int(VO_AT*1000)},volume=1.0[vo]')
fa.append(f"[{mus_i}:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:st=0:d=0.8,"
          f"volume='if(lt(t,{vo_end:.2f}),0.15,0.15+0.3*min(1,(t-{vo_end:.2f})/0.6))':eval=frame,afade=t=out:st={total-1.4:.2f}:d=1.4[mu]")   # audible calm bed under the voice (~-24 LUFS), rises after the last word, fades out at the end
fa.append('[od][vo][mu]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.89[aout]')

out = os.path.join(D, 'تذكرتك تطلع بدقيقة - إعلان بالصوت 9x16.mp4')
cmd = ['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fv + fa), '-map', '[vout]', '-map', '[aout]',
       '-t', str(total), '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
       '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
       '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True)
out45 = os.path.join(D, 'تذكرتك تطلع بدقيقة - إعلان بالصوت 4x5.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-vf', 'crop=1080:1350:0:230', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
                '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-c:a', 'copy', '-movflags', '+faststart', out45], check=True)
print('ok', total, 's; end card from', t_end, 'for', EC, 's')
