"""
LATINSENSEISHON — CLOUD RUNNER MOTOR 24/7 DUAL
Emite independientemente a Twitch y Kick a 30 FPS estables.
"""

import os, time, subprocess, threading, sys
from flask import Flask, jsonify, request, send_file
from datetime import datetime

app = Flask(__name__)

TWITCH_KEY = os.getenv("TWITCH_STREAM_KEY", "live_851574809_4d9Yt5LRXhlGi1NMUmYuC1JIj97REN").strip()
KICK_KEY   = os.getenv("KICK_STREAM_KEY",   "sk_us-west-2_OmepOf8fu8i6_KBoStM2ArcXUnnwXhDeyew4jBBoiYs").strip()

FUENTE = "https://ia800501.us.archive.org/11/items/superman_1941/superman_1941_512kb.mp4"

ESTADO = {
    "twitch": "INICIANDO",
    "kick": "INICIANDO",
    "inicio": str(datetime.utcnow()),
    "ultima_actividad": ""
}

def log(canal, msg):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    line = f"[{ts}] [{canal}] {msg}"
    print(line, flush=True)
    ESTADO["ultima_actividad"] = line

def worker_stream(canal, rtmp_dest, w, h, br):
    while True:
        ESTADO[canal] = "TRANSMITIENDO"
        log(canal, f"Conectando a {rtmp_dest.split('/app/')[0]}...")
        cmd = [
            "ffmpeg",
            "-re",
            "-stream_loop", "-1",
            "-i", FUENTE,
            "-vf", f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-tune", "zerolatency",
            "-b:v", f"{br}k",
            "-maxrate", f"{br}k",
            "-bufsize", f"{br*2}k",
            "-g", "60",
            "-keyint_min", "60",
            "-sc_threshold", "0",
            "-r", "30",
            "-c:a", "aac",
            "-b:a", "128k",
            "-ar", "44100",
            "-ac", "2",
            "-f", "flv",
            rtmp_dest
        ]
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in p.stdout:
                if "frame=" in line and int(line.split("frame=")[1].strip().split()[0]) % 150 == 0:
                    log(canal, line.strip())
            p.wait()
        except Exception as e:
            log(canal, f"Error: {e}")
        ESTADO[canal] = "RECONECTANDO"
        time.sleep(3)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "motor": "LATINSENSEISHON CLOUD RUNNER 24/7 DUAL INDEPENDIENTE",
        "canales": {
            "twitch": "twitch.tv/los_calle_tv",
            "kick": "kick.com/los-calle-tv"
        },
        "estado": ESTADO
    })

@app.route("/healthz", methods=["GET"])
def health():
    return home()

if __name__ == "__main__":
    t_twitch = threading.Thread(
        target=worker_stream,
        args=("twitch", f"rtmp://live.twitch.tv/app/{TWITCH_KEY}", 854, 480, 1000),
        daemon=True
    )
    t_kick = threading.Thread(
        target=worker_stream,
        args=("kick", f"rtmps://fa723fc1b171.global-contribute.live-video.net:443/app/{KICK_KEY}", 854, 480, 1000),
        daemon=True
    )
    t_twitch.start()
    t_kick.start()
    
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
