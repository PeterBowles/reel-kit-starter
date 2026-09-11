#!/usr/bin/env python3
"""
Landscape source -> vertical 9:16. Detects the face x-position by sampling
frames across the whole take, takes the median, and holds ONE crop-x for the
entire take (a locked frame reads as intentional; per-segment tracking reads
as jittery). Falls back to `fallback` if no face is found.

Used by build.py per segment. Can also be run standalone to print the
recommended crop-x for a time range.

Requires: opencv-python-headless<5 (4.x has CascadeClassifier), ffmpeg.
"""
import subprocess, sys, os, json, statistics, tempfile
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

def _grab(src, t, out):
    subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{t:.3f}","-i",src,
                    "-vframes","1",out], check=True)

def face_cx_samples(src, start, end, n=7):
    """Return list of detected face-center x positions across [start,end]."""
    cascade = cv2.CascadeClassifier(CASCADE_PATH)
    if cascade.empty():
        raise RuntimeError(f"cascade failed to load: {CASCADE_PATH}")
    xs = []
    span = max(0.1, end - start)
    with tempfile.TemporaryDirectory() as td:
        for i in range(n):
            t = start + span * (i + 0.5) / n
            fp = os.path.join(td, f"f{i}.png")
            try:
                _grab(src, t, fp)
                img = cv2.imread(fp)
                if img is None:
                    continue
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = cascade.detectMultiScale(gray, 1.1, 5, minSize=(120,120))
                if len(faces):
                    x,y,w,h = max(faces, key=lambda f: f[2]*f[3])
                    xs.append(x + w//2)
            except Exception:
                continue
    return xs

def crop_x_for_segment(src, start, end, crop_w=608, frame_w=1920, fallback=680):
    """Median face-centered crop-x, clamped to frame. Falls back if no face."""
    xs = face_cx_samples(src, start, end)
    if not xs:
        return fallback, "fallback (no face detected)"
    cx = int(statistics.median(xs))
    x = cx - crop_w // 2
    x = max(0, min(frame_w - crop_w, x))
    return x, f"face median cx={cx} from {len(xs)} samples"

def reframe_filter(crop_x, crop_w=608, crop_h=1080):
    return f"crop={crop_w}:{crop_h}:{crop_x}:0,scale=1080:1920"

def is_landscape(src):
    out = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
        "stream=width,height","-of","csv=p=0",src],capture_output=True,text=True).stdout.strip()
    w, h = (int(x) for x in out.split(",")[:2]); return w > h, w, h

if __name__ == "__main__":
    # standalone: reframe.py <src> <start> <end>
    src, start, end = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    x, why = crop_x_for_segment(src, start, end)
    print(f"crop_x={x}  ({why})")
    print(f"filter: {reframe_filter(x)}")
