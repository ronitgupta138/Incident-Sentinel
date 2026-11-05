#!/usr/bin/env python3
"""
capture_war_room_video.py - Captures each state of war_room_demo.html at 1920x1080
with exact viewport scroll control so every single message, card, and button is
clearly and prominently visible.
"""

import os
import subprocess
import time

FRAMES_DIR = "/home/ronit138/.hermes/cache/scratch/war_room_frames"
OUTPUT_VIDEO = "/home/ronit138/Incident-Sentinel/demo_video.mp4"
OUTPUT_GIF = "/home/ronit138/Incident-Sentinel/demo_preview.gif"
FFMPEG = "/home/ronit138/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
BRAVE = "/usr/bin/brave-browser"
HTML_PATH = "/home/ronit138/Incident-Sentinel/war_room_demo.html"

os.makedirs(FRAMES_DIR, exist_ok=True)

with open(HTML_PATH, "r") as f:
    base_html = f.read()

def render_state(idx: int, visible_count: int, is_approved: bool, typing_text: str, scroll_y: int, duration: int):
    patch_js = f"""
    <script>
      window.addEventListener('load', () => {{
        for (let i = 0; i <= {visible_count}; i++) {{
          const el = document.getElementById('msg' + i);
          if (el) el.classList.add('visible');
        }}
        const approveBtn = document.getElementById('approveBtn');
        const inputDisplay = document.getElementById('inputDisplay');
        const typingBox = document.getElementById('typingBox');
        const typingText = document.getElementById('typingText');
        
        if ({str(is_approved).lower()}) {{
          approveBtn.classList.add('clicked');
          approveBtn.innerHTML = '<span>✓</span> APPROVED by Ronit Gupta (09:42:48 UTC)';
        }}
        if ('{typing_text}') {{
          typingBox.style.visibility = 'visible';
          typingText.textContent = '{typing_text}';
        }} else {{
          typingBox.style.visibility = 'hidden';
        }}
        const msgContainer = document.getElementById('msgContainer');
        msgContainer.scrollTop = {scroll_y};
      }});
    </script>
    </body>
    """
    
    modified_html = base_html.replace("window.addEventListener('load', () => {\n    startSimulation();\n  });", "").replace("</body>", patch_js)
    
    temp_html = os.path.join(FRAMES_DIR, f"state_{idx}.html")
    png_path = os.path.join(FRAMES_DIR, f"state_{idx}.png")
    
    with open(temp_html, "w") as f:
        f.write(modified_html)
        
    subprocess.run([
        BRAVE,
        "--headless",
        "--disable-gpu",
        "--window-size=1680,1050",
        f"--screenshot={png_path}",
        temp_html
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"Captured State {idx} (scroll_y={scroll_y}, duration={duration}s)")
    return png_path, duration

# (idx, visible_count, is_approved, typing_text, scroll_y, duration)
states = [
    (0, 0, False, "", 0, 5),                                                                     # Initial view: GitHub deploy bot (TOP ANCHORED)
    (1, 1, False, "", 0, 6),                                                                     # PagerDuty Alert Ingestion (TOP ANCHORED)
    (2, 2, False, "@sentinel-triager is querying FastMCP telemetry...", 0, 5),                   # Ronit asks + Triager typing (TOP ANCHORED)
    (3, 3, False, "", 160, 9),                                                                   # Triager Diagnosis Card (Clean mid view)
    (4, 4, False, "", 400, 8),                                                                   # Remediator Approval Card (Focused on button)
    (5, 5, True, "@sentinel-operator is executing deployment rollback...", 600, 6),             # Ronit Approves (Focused on confirmation)
    (6, 6, True, "", 950, 10),                                                                   # Operator Rollback & Probes & Recovery Card
]

inputs_txt = os.path.join(FRAMES_DIR, "inputs.txt")
last_png = None
with open(inputs_txt, "w") as f:
    for idx, count, approved, typing, sy, dur in states:
        png, d = render_state(idx, count, approved, typing, sy, dur)
        last_png = png
        f.write(f"file '{png}'\n")
        f.write(f"duration {dur}\n")
    if last_png:
        f.write(f"file '{last_png}'\n")

print("\nEncoding to 1080p MP4 with FFmpeg...")
subprocess.run([
    FFMPEG,
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", inputs_txt,
    "-fps_mode", "vfr",
    "-pix_fmt", "yuv420p",
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    OUTPUT_VIDEO
], check=True)

print("Generating high-definition animated GIF preview...")
subprocess.run([
    FFMPEG,
    "-y",
    "-i", OUTPUT_VIDEO,
    "-vf", "fps=5,scale=1280:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
    "-loop", "0",
    OUTPUT_GIF
], check=True)

print(f"\n✨ NEW PERFECT-SCROLL DEMO VIDEO READY: {OUTPUT_VIDEO} ({os.path.getsize(OUTPUT_VIDEO)/(1024*1024):.2f} MB)")
