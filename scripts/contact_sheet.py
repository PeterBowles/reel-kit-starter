"""Frame grid for QC. Usage: python scripts/contact_sheet.py <video> -o sheet.jpg [--every 1.0] [--cols 6]"""
import argparse, subprocess
ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("-o", required=True)
ap.add_argument("--every", type=float, default=1.0); ap.add_argument("--cols", type=int, default=6)
a = ap.parse_args()
dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of",
      "default=noprint_wrappers=1:nokey=1",a.video],capture_output=True,text=True).stdout.strip())
n = max(1, int(dur / a.every)); rows = -(-n // a.cols)
subprocess.run(["ffmpeg","-y","-v","error","-i",a.video,"-vf",
    f"fps=1/{a.every},scale=270:-2,tile={a.cols}x{rows}","-frames:v","1",a.o],check=True)
print(f"wrote {a.o}: {n} frames, every {a.every}s")
