#!/usr/bin/env python3
"""
render_demo_video.py - Generates an end-to-end 1080p MP4 demo video for Incident-Sentinel.
Renders each phase of the war room using rich, takes headless 1080p snapshots via Brave,
and stitches them with ffmpeg into demo_video.mp4.
"""

import os
import shutil
import subprocess
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

FRAMES_DIR = "/home/ronit138/.hermes/cache/scratch/video_frames"
OUTPUT_VIDEO = "/home/ronit138/Incident-Sentinel/demo_video.mp4"
FFMPEG = "/home/ronit138/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
BRAVE = "/usr/bin/brave-browser"

os.makedirs(FRAMES_DIR, exist_ok=True)

def wrap_html(body_html: str, subtitle: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
    margin: 0;
    padding: 30px 50px;
    box-sizing: border-box;
    height: 1080px;
    width: 1920px;
    overflow: hidden;
  }}
  .header-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #30363d;
    padding-bottom: 12px;
    margin-bottom: 20px;
  }}
  .logo {{
    font-size: 26px;
    font-weight: 700;
    color: #58a6ff;
  }}
  .meta {{
    font-size: 18px;
    color: #8b949e;
  }}
  .badge {{
    background: #238636;
    color: #ffffff;
    padding: 4px 10px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 14px;
  }}
  .footer-bar {{
    position: absolute;
    bottom: 20px;
    left: 50px;
    right: 50px;
    display: flex;
    justify-content: space-between;
    color: #8b949e;
    font-size: 16px;
    border-top: 1px solid #21262d;
    padding-top: 10px;
  }}
  pre {{
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace !important;
    font-size: 20px !important;
    line-height: 1.35 !important;
    background: #161b22 !important;
    padding: 24px !important;
    border-radius: 10px !important;
    border: 1px solid #30363d !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5) !important;
  }}
</style>
</head>
<body>
  <div class="header-bar">
    <div class="logo">🛡️ Incident-Sentinel &nbsp;|&nbsp; <span style="color:#f0883e;">Switch Agent Room Demo</span></div>
    <div class="meta">Phase: <span style="color:#58a6ff; font-weight:600;">{subtitle}</span> &nbsp; <span class="badge">Track 01: Best Business Workflow</span></div>
  </div>
  
  {body_html}

  <div class="footer-bar">
    <div>Repository: <strong>https://github.com/ronitgupta138/Incident-Sentinel</strong></div>
    <div>Sole Author: <strong>Ronit Gupta</strong> (@ronitgupta138)</div>
    <div>Orchestrated via <strong>Switch Agent Protocol</strong></div>
  </div>
</body>
</html>"""

def render_step(idx: int, subtitle: str, duration: int, content_fn):
    console = Console(record=True, width=115)
    content_fn(console)
    inner_html = console.export_html(inline_styles=True)
    full_html = wrap_html(inner_html, subtitle)
    
    html_path = os.path.join(FRAMES_DIR, f"step_{idx}.html")
    png_path = os.path.join(FRAMES_DIR, f"step_{idx}.png")
    
    with open(html_path, "w") as f:
        f.write(full_html)
        
    subprocess.run([
        BRAVE,
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1080",
        f"--screenshot={png_path}",
        html_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f"Rendered Step {idx}: {subtitle} ({duration}s)")
    return png_path, duration

steps_metadata = []

# --- Step 0: Title Card ---
def step0(c: Console):
    c.print(Panel(
        Text.from_markup(
            "[bold cyan]Incident-Sentinel 🛡️[/bold cyan]\n"
            "[white]Autonomous SRE Incident Response & Canary Deployment Safety Room on Switch[/white]\n\n"
            "[yellow]WeMakeDevs × DevTools Academy × Switch Hackathon[/yellow]\n"
            "[green]Track 01: Best Business Workflow[/green]  |  [blue]Sole Author: Ronit Gupta[/blue]\n\n"
            "[dim]Turn enterprise chat (Slack / Teams / Discord / Mattermost) into an automated\n"
            "multi-agent incident war room with human-in-the-loop rollback safety.[/dim]"
        ),
        title="[bold blue]Executive Overview[/bold blue]",
        border_style="cyan",
        padding=(2, 4)
    ))
    
    table = Table(title="Autonomous Multi-Agent Teammates in Switch Room #incident-war-room", border_style="dim")
    table.add_column("Agent Identity", style="bold green")
    table.add_column("Protocol Role", style="bold yellow")
    table.add_column("Capabilities & Tool Integrations", style="white")
    table.add_row("@sentinel-triager", "Telemetry Diagnostic", "FastMCP error query, commit correlation, blast radius mapping")
    table.add_row("@sentinel-remediator", "Mitigation Engineer", "Git diff inspection, DB schema compatibility, approval card generation")
    table.add_row("@sentinel-operator", "Rollback Dispatcher", "Human approval gatekeeper, zero-downtime rollback, synthetic health probes")
    c.print(table)

# --- Step 1: Outage Trigger ---
def step1(c: Console):
    step0(c)
    c.print("\n")
    c.print(Panel(
        Text.from_markup(
            "[bold red]🚨 CRITICAL ALERT TRIGGERED: HIGH ERROR RATE DETECTED[/bold red]\n"
            "• Service: [bold white]cart-service[/bold white] (Production APAC)\n"
            "• Target: [bold white]/api/v1/checkout[/bold white]\n"
            "• Condition: HTTP 500 error rate exceeded 45.0% threshold ([bold red]Current: 48.7%[/bold red])\n"
            "• Incident Time: [bold yellow]09:42:10 UTC[/bold yellow] | Alert Channel: [bold cyan]#incident-war-room[/bold cyan]"
        ),
        title="[bold red]PagerDuty Telemetry Alert Ingestion[/bold red]",
        border_style="red"
    ))
    c.print("[bold green]👤 SRE-Lead (Human):[/bold green] [italic]@sentinel-triager checkout is failing since 09:40. Can you investigate root cause?[/italic]")

# --- Step 2: Triager Analysis ---
def step2(c: Console):
    c.print(Panel(
        Text.from_markup(
            "[bold green]👤 SRE-Lead (Human):[/bold green] [italic]@sentinel-triager checkout is failing since 09:40. Can you investigate root cause?[/italic]\n\n"
            "[bold cyan]@sentinel-triager:[/bold cyan] Ingesting FastMCP metrics across cart-service instances and correlating recent git deployment commits..."
        ),
        title="[bold cyan]Phase 1: Multi-Agent Triage[/bold cyan]",
        border_style="cyan"
    ))
    
    diag_table = Table(title="Incident Telemetry Diagnosis (@sentinel-triager)", border_style="cyan")
    diag_table.add_column("Metric", style="bold white")
    diag_table.add_column("Observed Value", style="bold red")
    diag_table.add_column("Normal Baseline", style="bold green")
    diag_table.add_row("Service Status", "DEGRADED (P1 Severity)", "HEALTHY")
    diag_table.add_row("HTTP 500 Error Rate", "48.7% (1,420 errors/5m)", "< 0.01%")
    diag_table.add_row("p99 Tail Latency", "3,840.5 ms", "28.0 ms")
    diag_table.add_row("Culprit Deployment", "v2.14.0 (Commit 8f3a91b)", "v2.13.2 (Commit 4e1c07a)")
    diag_table.add_row("Root Cause Analysis", "NullPointerException: CartSession.getDiscount()", "Clean Operation")
    c.print(diag_table)
    c.print("[bold cyan]@sentinel-triager:[/bold cyan] [italic]Diagnosis complete. Culprit deploy is v2.14.0. Handing off to @sentinel-remediator to evaluate rollback blast radius.[/italic]")

# --- Step 3: Human Approval Card ---
def step3(c: Console):
    step2(c)
    c.print("\n")
    c.print(Panel(
        Text.from_markup(
            "[bold yellow]⚠️ HUMAN-IN-THE-LOOP APPROVAL REQUIRED FOR INFRASTRUCTURE ROLLBACK[/bold yellow]\n\n"
            "• [bold white]Proposed Action:[/bold white] Rollback deployment [red]v2.14.0[/red] ➔ [green]v2.13.2[/green]\n"
            "• [bold white]Impacted Pods:[/bold white] cart-service-prod-01..12 (100% traffic shift)\n"
            "• [bold white]Schema Compatibility:[/bold white] [bold green]PASS[/bold green] (v2.13.2 DB migration is backwards-compatible)\n"
            "• [bold white]Estimated Recovery Time:[/bold white] < 45 seconds\n\n"
            "[bold white]Safety Invariant:[/bold white] Destructive actions require explicit human sign-off from on-call engineer.\n"
            "[bold yellow]Action:[/bold yellow] Reply [bold green]'APPROVE'[/bold green] to authorize execution or [bold red]'REJECT'[/bold red] to cancel."
        ),
        title="[bold yellow]Mitigation Gate (@sentinel-remediator)[/bold yellow]",
        border_style="yellow"
    ))

# --- Step 4: Human Sign-off & Execution ---
def step4(c: Console):
    step3(c)
    c.print("\n")
    c.print("[bold green]👤 Ronit Gupta (On-Call SRE):[/bold green] [bold white underline]APPROVE[/bold white underline]")
    c.print("[bold magenta]@sentinel-operator:[/bold magenta] [italic]Authorization verified by Ronit Gupta. Executing deployment rollback to v2.13.2 across cluster...[/italic]")

# --- Step 5: Synthetic Health Probes ---
def step5(c: Console):
    c.print(Panel(
        Text.from_markup(
            "[bold green]👤 Ronit Gupta (On-Call SRE):[/bold green] [bold white underline]APPROVE[/bold white underline]\n"
            "[bold magenta]@sentinel-operator:[/bold magenta] Rollback executed. Initiating synthetic health probes across all 4 critical endpoints..."
        ),
        title="[bold magenta]Phase 2: Automated Rollback Dispatch[/bold magenta]",
        border_style="magenta"
    ))
    
    probe_table = Table(title="Synthetic Health & Verification Probes (@sentinel-operator)", border_style="green")
    probe_table.add_column("Probe ID", style="dim")
    probe_table.add_column("Target Endpoint", style="bold white")
    probe_table.add_column("HTTP Response", style="bold green")
    probe_table.add_column("p99 Latency", style="cyan")
    probe_table.add_row("PRB-01", "/api/v1/cart/session", "HTTP 200 OK", "18.2 ms")
    probe_table.add_row("PRB-02", "/api/v1/checkout/calculate", "HTTP 200 OK", "22.4 ms")
    probe_table.add_row("PRB-03", "/api/v1/checkout/payment", "HTTP 200 OK", "26.1 ms")
    probe_table.add_row("PRB-04", "/api/v1/inventory/reserve", "HTTP 200 OK", "19.5 ms")
    c.print(probe_table)
    
    c.print(Panel(
        Text.from_markup(
            "[bold green]🎉 INCIDENT DECLARED RESOLVED — SYSTEM OPERATIONAL[/bold green]\n"
            "• Current Version: [bold green]v2.13.2 (Stable)[/bold green]\n"
            "• Error Rate: [bold green]0.0%[/bold green] (All pods healthy)\n"
            "• p99 Latency: [bold green]24.5 ms[/bold green]\n"
            "• Total Outage Duration: [bold yellow]2 minutes, 48 seconds[/bold yellow] (MTTR cut by 93%)\n"
            "• Post-Mortem Report: Compiled and saved to [cyan]docs/postmortems/INC-8924.md[/cyan]"
        ),
        title="[bold green]Recovery Summary[/bold green]",
        border_style="green"
    ))

# --- Step 6: Closing Summary ---
def step6(c: Console):
    step5(c)
    c.print("\n")
    c.print(Panel(
        Text.from_markup(
            "[bold cyan]Incident-Sentinel Architecture Summary[/bold cyan]\n\n"
            "1. [bold white]Declarative Switch Template:[/bold white] incident-sentinel.template.yaml\n"
            "2. [bold white]FastMCP Tool Server:[/bold white] Exposes live metrics, git diffs, and rollback execution\n"
            "3. [bold white]Human Safety Protocol:[/bold white] Strict Human-in-the-Loop gating before infrastructure mutation\n"
            "4. [bold white]Cross-Platform:[/bold white] Works natively across Slack, Teams, Discord & Mattermost\n\n"
            "[green]Repository:[/green] [white]https://github.com/ronitgupta138/Incident-Sentinel[/white]\n"
            "[yellow]WeMakeDevs Hackathon Submission — Built with Switch[/yellow]"
        ),
        title="[bold blue]Ready for Production Submission[/bold blue]",
        border_style="blue"
    ))

steps = [
    (0, "Executive Architecture & Overview", 6, step0),
    (1, "Outage Alert Ingestion (48.7% 500s)", 7, step1),
    (2, "FastMCP Telemetry Triage & Root Cause", 9, step2),
    (3, "Human Approval Card Generation", 8, step3),
    (4, "Human-in-the-Loop Sign-off ('APPROVE')", 6, step4),
    (5, "Automated Rollback & Synthetic Verification", 9, step5),
    (6, "Incident Resolution & Architecture Summary", 7, step6),
]

last_png_path = None
inputs_txt = os.path.join(FRAMES_DIR, "inputs.txt")
with open(inputs_txt, "w") as f:
    for idx, subtitle, dur, fn in steps:
        png_path, duration = render_step(idx, subtitle, dur, fn)
        last_png_path = png_path
        f.write(f"file '{png_path}'\n")
        f.write(f"duration {duration}\n")
    # Repeat the last frame for clean exit
    if last_png_path:
        f.write(f"file '{last_png_path}'\n")

print(f"\nCompiling frames with FFmpeg into {OUTPUT_VIDEO}...")
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

print(f"\n🎉 DEMO VIDEO CREATED CLEANLY: {OUTPUT_VIDEO}")
print(f"File size: {os.path.getsize(OUTPUT_VIDEO) / (1024*1024):.2f} MB")
