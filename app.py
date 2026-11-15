"""
LATINSENSEISHON — CLOUD RUNNER MOTOR 24/7
Corre en Hugging Face Spaces (Docker) o Render.
Emite Superman 1941 (Dominio Público) a Twitch y Kick 24/7.
"""

import os, time, subprocess, threading, signal, sys
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# ── Claves de stream (sobreescribibles via Secrets de HuggingFace) ──
TWITCH_KEY = os.getenv("TWITCH_STREAM_KEY", "live_851574809_cckGIiMFJwCTm8Ce5NFfjm4CRkWN8m")
KICK_KEY   = os.getenv("KICK_STREAM_KEY",   "sk_us-west-2_OmepOf8fu8i6_KBoStM2ArcXUnnwXhDeyew4jBBoiYs")

# URLs de respaldo en Archive.org (Superman 1941 - 100% Dominio Público)
FUENTES = [
    "https://ia800501.us.archive.org/11/items/superman_1941/superman_1941_512kb.mp4",
    "https://archive.org/download/superman_1941/superman_1941_512kb.mp4",
    "https://ia601500.us.archive.org/8/items/popeye_theatricals/PopeyeTheatricals_512kb.mp4",
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
    twitch_rtmp = f"rtmp://ingest.global-contribute.live-video.net/app/{TWITCH_KEY}"
    kick_rtmp   = f"rtmps://fa723fc1b171.global-contribute.live-video.net:443/app/{KICK_KEY}"
    
    # Ticker con nombre del canal en el stream
    vf_filter = (
        "drawtext=text='🔴 LOS CALLE TV — Reviviendo tu Infancia 24/7':"
        "fontsize=24:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=5:"
        "x=10:y=10"
    )
    
    return [
        "ffmpeg",
        "-re",                          # Leer en tiempo real
        "-stream_loop", "-1",           # Loop infinito
        "-i", source_url,
        "-vf", vf_filter,              # Ticker superior
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-tune", "zerolatency",
        "-b:v", "1800k",               # Bitrate cloud-friendly (menos CPU)
        "-maxrate", "2000k",
        "-bufsize", "4000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-ac", "2",
        "-f", "tee",
        f"[f=flv:onfail=ignore]{twitch_rtmp}|[f=flv:onfail=ignore]{kick_rtmp}"
    ]

def motor_stream_loop():
    global STREAM_PROC, ESTADO
    fuente_idx = 0
    
    while True:
        source = FUENTES[fuente_idx % len(FUENTES)]
        ESTADO["fuente_actual"] = source
        ESTADO["reinicios"] += 1
        
        log(f">>> TRANSMITIENDO desde: {source}")
        log(f">>> Reinicio #{ESTADO['reinicios']}")
        
        try:
            cmd = build_ffmpeg_cmd(source)
            STREAM_PROC = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            ESTADO["estado"] = "TRANSMITIENDO_24_7"
            
            # Leer output de ffmpeg en tiempo real
            for line in STREAM_PROC.stdout:
                if "frame=" in line or "error" in line.lower() or "fail" in line.lower():
                    log(f"FFmpeg: {line.strip()}")
            
            STREAM_PROC.wait()
            ret = STREAM_PROC.returncode
            log(f"FFmpeg terminó con código {ret} — reconectando...")
            
        except Exception as e:
            log(f"ERROR en motor: {e}")
        
        # Si falla, intentar siguiente fuente
        fuente_idx += 1
        ESTADO["estado"] = "RECONECTANDO"
        log("Esperando 5s antes de reiniciar...")
        time.sleep(5)

# ── Endpoints Flask ──────────────────────────────────────────────────
@app.route("/", methods=["GET"])
@app.route("/healthz", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "motor": "LATINSENSEISHON CLOUD RUNNER 24/7",
        "canal": "LOS CALLE TV",
        "plataformas": ["twitch.tv/los_calle_tv", "kick.com/los-calle-tv"],
        "estado": ESTADO
    })

@app.route("/webhook/orden", methods=["POST"])
def recibir_orden():
    data = request.json or {}
    accion = data.get("accion", "status")
    if accion == "reiniciar" and STREAM_PROC:
        STREAM_PROC.terminate()
        log("Reinicio solicitado via webhook")
    return jsonify({"ok": True, "accion": accion, "estado": ESTADO})

if __name__ == "__main__":
    log("=== LATINSENSEISHON CLOUD RUNNER ARRANCANDO ===")
    t = threading.Thread(target=motor_stream_loop, daemon=True)
    t.start()
    # HuggingFace Spaces espera el servidor en puerto 7860
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "7860")))
