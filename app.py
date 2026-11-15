"""
LATINSENSEISHON — CLOUD RUNNER MOTOR 24/7 (RENDER DOCKER)
Emite a Twitch y Kick con compatibilidad estricta HLS / Twitch Ingest.
"""

import os, time, subprocess, threading, sys
from flask import Flask, jsonify, request, send_file
from datetime import datetime

app = Flask(__name__)

TWITCH_KEY = os.getenv("TWITCH_STREAM_KEY", "live_851574809_4d9Yt5LRXhlGi1NMUmYuC1JIj97REN").strip()
KICK_KEY   = os.getenv("KICK_STREAM_KEY",   "sk_us-west-2_OmepOf8fu8i6_KBoStM2ArcXUnnwXhDeyew4jBBoiYs").strip()

FUENTES = [
    "https://ia800501.us.archive.org/11/items/superman_1941/superman_1941_512kb.mp4",
    "https://archive.org/download/superman_1941/superman_1941_512kb.mp4",
    "https://archive.org/download/popeye_patriotic_popeye/popeye_patriotic_popeye_512kb.mp4",
]

STREAM_PROC = None
ESTADO = {
    "estado": "INICIANDO",
    "fuente_actual": "",
    "inicio": str(datetime.utcnow()),
    "reinicios": 0,
    "ultima_actividad": ""
}

def log(msg):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)
    ESTADO["ultima_actividad"] = f"[{ts}] {msg}"

def build_ffmpeg_cmd(source_url):
    twitch_rtmp = f"rtmp://live.twitch.tv/app/{TWITCH_KEY}"
    kick_rtmp   = f"rtmps://fa723fc1b171.global-contribute.live-video.net:443/app/{KICK_KEY}"
    
    tee_target = f"[f=flv:onfail=ignore]{twitch_rtmp}|[f=flv:onfail=ignore]{kick_rtmp}"
    
    return [
        "ffmpeg",
        "-re",
        "-stream_loop", "-1",
        "-i", source_url,
        "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-profile:v", "main",
        "-b:v", "2000k",
        "-maxrate", "2000k",
        "-bufsize", "4000k",
        "-g", "60",
        "-keyint_min", "60",
        "-sc_threshold", "0",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-ac", "2",
        "-f", "tee",
        "-map", "0:v",
        "-map", "0:a?",
        tee_target
    ]

def motor_stream_loop():
    global STREAM_PROC, ESTADO
    fuente_idx = 0
    
    while True:
        source = FUENTES[fuente_idx % len(FUENTES)]
        ESTADO["fuente_actual"] = source
        ESTADO["reinicios"] += 1
        
        log(f">>> TRANSMITIENDO desde: {source}")
        log(f">>> Intento #{ESTADO['reinicios']}")
        
        try:
            cmd = build_ffmpeg_cmd(source)
            STREAM_PROC = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            ESTADO["estado"] = "TRANSMITIENDO_24_7"
            
            for line in STREAM_PROC.stdout:
                line_str = line.strip()
                if "frame=" in line_str or "error" in line_str.lower() or "fail" in line_str.lower():
                    log(f"FFmpeg: {line_str}")
            
            STREAM_PROC.wait()
            ret = STREAM_PROC.returncode
            log(f"FFmpeg finalizó con código {ret}")
            
        except Exception as e:
            log(f"ERROR en motor: {e}")
        
        fuente_idx += 1
        ESTADO["estado"] = "RECONECTANDO"
        time.sleep(5)

@app.route("/", methods=["GET"])
def dashboard():
    return send_file("index.html")

@app.route("/api/status", methods=["GET"])
@app.route("/healthz", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "motor": "LATINSENSEISHON CLOUD RUNNER 24/7",
        "canal": "LOS CALLE TV",
        "estado": ESTADO
    })

if __name__ == "__main__":
    t = threading.Thread(target=motor_stream_loop, daemon=True)
    t.start()
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
