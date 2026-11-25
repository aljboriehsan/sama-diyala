# Paid-ad version of the office video (Facebook/Instagram, Diyala + Baghdad): same shots and sounds as the TikTok,
# Tajawal text, and a 5 s animated end card ("احجز الآن عبر الواتساب") rendered frame by frame from عناصر/الختام.html.
# Outputs 9:16 (Reels/Stories) and a 4:5 crop (Feed).
# Run from the repo root: python3 "14-الفيديو/إعلان ممول - تذكرتك تطلع بدقيقة/build.py"
import subprocess, os, glob
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(D))
L = os.path.join(R, '14-الفيديو/مقاطع/المكتب')
FPS, W, H = 30, 1080, 1920
# (clip, start, dur, gain dB, blur boxes [x,y,w,h,radius]) — boxes hide booking data on screen/tickets
segs = [
 ('المكتب - الحجز على الكيبورد.mov',        0.60, 3.0, 10, [('mask', 'عناصر/قناع الشاشة.png', 20)]),
 ('المكتب - الطابعة تخرج التذكرة.mov',     0.25, 2.0, 6,  [(400, 1030, 420, 280, 7)]),
 ('المكتب - ختم التذكرة.mov',              0.95, 1.6, 7,  [(330, 630, 440, 140, 6), (160, 770, 790, 150, 6)]),
 ('المكتب - وضع التذكرة في الغلاف.mov',    2.20, 1.6, 11, []),
 ('المكتب - تسليم التذكرة للزبون.mov',     0.00, 1.6, 11, []),
 ('المكتب - جولة في القاعة وجدار العراقية.mov', 2.40, 2.2, 4, []),
 # the rest of the pan, slowed to fill the 5 s end card (only seen under it)
 ('المكتب - جولة في القاعة وجدار العراقية.mov', 4.60, 5.0, 4, [], 7.05),
]
EC = 5.0
MUSIC = os.path.join(R, '14-الفيديو/موسيقى/leberch-travel-documentary-519393.mp3'); M_START = 95.0   # the track ends at 100.05: the music starts with the end card and ends with the track
total = sum(s[2] for s in segs); t_end = total - EC
FR = os.path.join(D, '.cache/end_frames')
subprocess.run(['node', os.path.join(R, '07-أدوات/فيديو/render_anim.js'), os.path.join(D, 'عناصر/الختام.html'), FR, str(EC), str(FPS)], check=True)
subprocess.run(['node', os.path.join(R, '07-أدوات/فيديو/render_anim.js'), os.path.join(D, 'عناصر/البداية.html'), os.path.join(D, '.cache/hook'), '0.04', '25'], check=True)
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
            if b[0] == 'mask':   # blur only inside a feathered mask image (white = blurred)
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
    if src_end:   # room tone of the slowed tail: real speed, fading out, padded to the segment length
        fa.append(f'[{i}:a]atrim=0:{win},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,'
                  f'afade=t=out:st={win-1.0}:d=1.0,apad=whole_dur={d}[a{i}]')
        continue
    fa.append(f'[{i}:a]atrim=0:{d},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={g}dB,'
              f'afade=t=in:st=0:d=0.02,afade=t=out:st={d-0.03}:d=0.03[a{i}]')
k = len(segs)
fv.append(''.join(f'[v{i}]' for i in range(k)) + f'concat=n={k}:v=1:a=0[base]')
fa.append(''.join(f'[a{i}]' for i in range(k)) + f'concat=n={k}:v=0:a=1[orig]')
hook = k; endc = k + 1; mus = k + 2
inp += ['-loop', '1', '-t', str(total), '-i', os.path.join(D, '.cache/hook/0000.png'),
        '-framerate', str(FPS), '-i', os.path.join(FR, '%04d.png'),
        '-ss', str(M_START), '-t', str(total - t_end + 0.2), '-i', MUSIC]
for j, (tag, path) in enumerate(masks):
    inp += ['-loop', '1', '-t', str(total), '-i', path]
    fv[:] = [x.replace('{' + tag + '}', f'{mus + 1 + j}:v') for x in fv]
fv.append(f'[{hook}:v]format=rgba,fade=t=out:st=2.75:d=0.25:alpha=1[hk]')
fv.append(f'[{endc}:v]format=rgba,setpts=PTS-STARTPTS+{t_end}/TB[ec]')   # fades are inside the animation
fv.append(f"[base][hk]overlay=0:0:enable='lt(t,3.0)'[b1]")
fv.append(f"[b1][ec]overlay=0:0:eof_action=repeat,format=yuv420p[vout]")
# the office ambience dips under the music; music fades in with the end card and ends with the track
fa.append(f"[orig]volume='if(gte(t,{t_end}),0.35,1)':eval=frame[od]")
fa.append(f'[{mus}:a]aresample=48000,aformat=channel_layouts=stereo,volume=1.5,afade=t=in:st=0:d=0.35,adelay={int(t_end*1000)}|{int(t_end*1000)}[mu]')
fa.append('[od][mu]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.9[aout]')
out = os.path.join(D, 'تذكرتك تطلع بدقيقة - إعلان 9x16.mp4')
cmd = ['ffmpeg', '-v', 'error', '-y'] + inp + ['-filter_complex', ';'.join(fv + fa), '-map', '[vout]', '-map', '[aout]',
       '-t', str(total), '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
       '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
       '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True)
# Feed 4:5: crop y=230 keeps the hook and the end card centred
out45 = os.path.join(D, 'تذكرتك تطلع بدقيقة - إعلان 4x5.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-vf', 'crop=1080:1350:0:230', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
                '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-c:a', 'copy', '-movflags', '+faststart', out45], check=True)
print('ok', round(total, 2), 's')
