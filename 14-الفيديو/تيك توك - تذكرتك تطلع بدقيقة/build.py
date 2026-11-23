# Office TikTok: original sound from each clip, music only under the end card.
# Run from the repo root: python3 "14-الفيديو/تيك توك - تذكرتك تطلع بدقيقة/build.py"
import subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(D))
L = os.path.join(R, '14-الفيديو/مقاطع/المكتب')
FPS, W, H = 30, 1080, 1920
# (clip, start, dur, gain dB, blur boxes [x,y,w,h,radius]) — boxes hide booking data on screen/tickets
segs = [
 ('المكتب - الحجز على الكيبورد.mov',        0.80, 2.0, 10, [(0, 0, 1080, 930, 22)]),
 ('المكتب - الطابعة تخرج التذكرة.mov',     0.25, 2.0, 6,  [(330, 880, 600, 560, 7)]),
 ('المكتب - ختم التذكرة.mov',              0.95, 1.6, 7,  [(160, 620, 760, 520, 6)]),
 ('المكتب - وضع التذكرة في الغلاف.mov',    2.20, 1.6, 11, []),
 ('المكتب - تسليم التذكرة للزبون.mov',     0.00, 1.6, 11, []),
 ('المكتب - جولة في القاعة وجدار العراقية.mov', 2.60, 3.6, 4, []),
]
MUSIC = os.path.join(R, '14-الفيديو/موسيقى/leberch-travel-documentary-519393.mp3'); M_START = 96.8
total = sum(s[2] for s in segs); t_end = total - 2.2
inp, fv, fa = [], [], []
for i, (f, ss, d, g, boxes) in enumerate(segs):
    inp += ['-ss', str(ss), '-t', str(d + 0.15), '-i', os.path.join(L, f)]
    n = int(round(d * FPS))
    v = f'[{i}:v]fps={FPS},scale={W}:{H}:flags=lanczos,setsar=1,eq=contrast=1.05:saturation=1.06'
    if boxes:
        fv.append(v + f',split={len(boxes)+1}[b{i}' + ''.join(f'][c{i}_{k}' for k in range(len(boxes))) + ']')
        cur = f'b{i}'
        for k, (x, y, w, h, r) in enumerate(boxes):
            fv.append(f'[c{i}_{k}]crop={w}:{h}:{x}:{y},boxblur={r}:2[bl{i}_{k}]')
            fv.append(f'[{cur}][bl{i}_{k}]overlay={x}:{y}[o{i}_{k}]'); cur = f'o{i}_{k}'
        fv.append(f'[{cur}]trim=end_frame={n},setpts=PTS-STARTPTS[v{i}]')
    else:
        fv.append(v + f',trim=end_frame={n},setpts=PTS-STARTPTS[v{i}]')
    fa.append(f'[{i}:a]atrim=0:{d},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,'
              f'afade=t=in:st=0:d=0.02,afade=t=out:st={d-0.03}:d=0.03[a{i}]')
k = len(segs)
fv.append(''.join(f'[v{i}]' for i in range(k)) + f'concat=n={k}:v=1:a=0[base]')
fa.append(''.join(f'[a{i}]' for i in range(k)) + f'concat=n={k}:v=0:a=1[orig]')
hook = k; endc = k + 1; mus = k + 2
inp += ['-loop', '1', '-t', str(total), '-i', os.path.join(D, 'عناصر/البداية.png'),
        '-loop', '1', '-t', str(total), '-i', os.path.join(D, 'عناصر/الختام.png'),
        '-ss', str(M_START), '-t', str(total - t_end + 0.2), '-i', MUSIC]
fv.append(f'[{hook}:v]format=rgba,fade=t=out:st=1.75:d=0.25:alpha=1[hk]')
fv.append(f'[{endc}:v]format=rgba,fade=t=in:st={t_end}:d=0.45:alpha=1[ec]')
fv.append(f"[base][hk]overlay=0:0:enable='lt(t,2.0)'[b1]")
fv.append(f"[b1][ec]overlay=0:0:enable='gte(t,{t_end})',format=yuv420p[vout]")
# the office ambience dips under the music; music fades in with the end card and ends with the track
fa.append(f"[orig]volume='if(gte(t,{t_end}),0.35,1)':eval=frame[od]")
fa.append(f'[{mus}:a]aresample=48000,aformat=channel_layouts=stereo,volume=1.5,afade=t=in:st=0:d=0.35,adelay={int(t_end*1000)}|{int(t_end*1000)}[mu]')
fa.append('[od][mu]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.9[aout]')
out = os.path.join(D, 'تذكرتك تطلع بدقيقة.mp4')
cmd = ['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fv + fa), '-map', '[vout]', '-map', '[aout]',
       '-t', str(total), '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
       '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
       '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True); print('ok', round(total, 2), 's')
