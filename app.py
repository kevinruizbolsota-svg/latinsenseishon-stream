"""
LATINSENSEISHON — CLOUD RUNNER MOTOR 24/7 ULTRA FLUIDO
Emite a Kick y Twitch con 0% de uso de CPU (Copy Mode / Pass-through).
Velocidad: 1.0x perfecta y sin cortes ni lag.
"""

import os, time, subprocess, threading, sys
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

TWITCH_KEY = os.getenv("TWITCH_STREAM_KEY", "live_851574809_4d9Yt5LRXhlGi1NMUmYuC1JIj97REN").strip()
KICK_KEY   = os.getenv("KICK_STREAM_KEY",   "sk_us-west-2_OmepOf8fu8i6_KBoStM2ArcXUnnwXhDeyew4jBBoiYs").strip()

# Video fuente ya codificado en H264 y AAC de forma nativa
FUENTE = "https://ia800501.us.archive.org/11/items/superman_1941/superman_1941_512kb.mp4"

ESTADO = {
    "twitch": "INICIANDO",
    "kick": "INICIANDO",
    "inicio": str(datetime.utcnow()),
    "modo": "ZERO_CPU_PASSTHROUGH",
    "ultima_actividad": ""
}

def log(canal, msg):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    line = f"[{ts}] [{canal}] {msg}"
    print(line, flush=True)
    ESTADO["ultima_actividad"] = line

def worker_stream(canal, rtmp_dest):
    while True:
        ESTADO[canal] = "TRANSMITIENDO_FLUIDO"
        log(canal, f"Lanzando flujo directo a {canal.upper()}...")
        
        # Modo ultra ligero: copia directa de paquetes sin re-codificar (0% consumo de CPU)
        cmd = [
            "ffmpeg",
            "-re",
            "-stream_loop", "-1",
            "-i", FUENTE,
            "-c:v", "copy",
            "-c:a", "copy",
            "-f", "flv",
            rtmp_dest
        ]
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in p.stdout:
                if "frame=" in line and int(line.split("frame=")[1].strip().split()[0]) % 300 == 0:
                    log(canal, line.strip())
            p.wait()
        except Exception as e:
            log(canal, f"Error: {e}")
            
        ESTADO[canal] = "RECONECTANDO"
        time.sleep(3)

@app.route("/", methods=["GET"])
@app.route("/healthz", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "motor": "LATINSENSEISHON CLOUD RUNNER ZERO-LAG",
        "estado": ESTADO
    })

if __name__ == "__main__":
    t_twitch = threading.Thread(
        target=worker_stream,
        args=("twitch", f"rtmp://live.twitch.tv/app/{TWITCH_KEY}"),
        daemon=True
    )
    t_kick = threading.Thread(
        target=worker_stream,
        args=("kick", f"rtmps://fa723fc1b171.global-contribute.live-video.net:443/app/{KICK_KEY}"),
        daemon=True
    )
    t_twitch.start()
    t_kick.start()
    
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
