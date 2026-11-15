"""
LATINSENSEISHON — CLOUD RUNNER MOTOR 24/7 ULTRA FLUIDO
Emite a Kick y Twitch con 0% de uso de CPU (Copy Mode / Pass-through).
Incluye:
1. Emision de Serie: Nezha Conquista al Rey Dragón (1979) — Joya Cultural de Oro.
2. Cache local en SSD: 0 lag de red y bucles instantaneos sin micro-cortes.
3. Anti-Sleep Keep-Alive: Ping cada 5 minutos para que Render Free Tier NUNCA se duerma.
4. Servidor Web Dashboard Maestro (index.html) con Ingenieria de Audiencias y Parrilla 24H.
"""

import os, time, subprocess, threading, sys, urllib.request
from flask import Flask, jsonify, send_file
from datetime import datetime

app = Flask(__name__, static_folder=".")

TWITCH_KEY = os.getenv("TWITCH_STREAM_KEY", "live_851574809_4d9Yt5LRXhlGi1NMUmYuC1JIj97REN").strip()
KICK_KEY   = os.getenv("KICK_STREAM_KEY",   "sk_us-west-2_OmepOf8fu8i6_KBoStM2ArcXUnnwXhDeyew4jBBoiYs").strip()

# Nueva serie seleccionada: Nezha Conquista al Rey Dragón (1979) — Animación tradicional de culto
FUENTE_REMOTA = "https://archive.org/download/temporuss-animes-nezha-conquers-the-drag-media-vfs-lf-9-ee-4-wc-001-360p/Temporuss-Animes-Nezha-Conquers-the-Drag_Media_VfsLf9EE4Wc_001_360p.mp4"
VIDEO_LOCAL   = "/tmp/nezha_1979_stream.mp4"

# URL publica de Render para auto-despertar
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL", "https://latinsenseishon-stream.onrender.com")

ESTADO = {
    "twitch": "INICIANDO",
    "kick": "INICIANDO",
    "serie": "Nezha Conquista al Rey Dragón (1979) — El Sacrificio Legendario",
    "inicio": str(datetime.utcnow()),
    "modo": "ZERO_CPU_ANTI_SLEEP_24_7",
    "ultima_actividad": ""
}

def log(canal, msg):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    line = f"[{ts}] [{canal}] {msg}"
    print(line, flush=True)
    ESTADO["ultima_actividad"] = line

def preparar_video_local():
    """Descarga el video al disco local una sola vez para eliminar cortes y latencia."""
    if not os.path.exists(VIDEO_LOCAL) or os.path.getsize(VIDEO_LOCAL) < 1000000:
        log("sistema", f"Descargando {ESTADO['serie']} a almacenamiento local para 0 lag...")
        try:
            urllib.request.urlretrieve(FUENTE_REMOTA, VIDEO_LOCAL)
            log("sistema", f"Video listo ({os.path.getsize(VIDEO_LOCAL)} bytes).")
        except Exception as e:
            log("sistema", f"Error descarga local: {e}. Usando URL remota como respaldo.")
            return FUENTE_REMOTA
    return VIDEO_LOCAL

def keep_alive_daemon():
    """Realiza un ping HTTP externo cada 5 minutos para evitar que Render hiberne el contenedor."""
    log("sistema", "Iniciando guardia Anti-Sleep 24/7...")
    time.sleep(60)
    while True:
        try:
            req = urllib.request.Request(
                f"{RENDER_URL}/healthz",
                headers={"User-Agent": "AntiSleep-Daemon/1.0"}
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                log("anti-sleep", f"Latido exitoso ({resp.status}). Render despierto 24/7.")
        except Exception as e:
            log("anti-sleep", f"Alerta latido: {e}")
        time.sleep(300) # Cada 5 minutos (Render hiberna a los 15)

def worker_stream(canal, rtmp_dest, archivo_video):
    while True:
        ESTADO[canal] = "TRANSMITIENDO_FLUIDO"
        log(canal, f"Lanzando flujo directo de NEZHA a {canal.upper()}...")
        
        cmd = [
            "ffmpeg",
            "-re",
            "-stream_loop", "-1",
            "-i", archivo_video,
            "-c:v", "copy",
            "-c:a", "copy",
            "-flvflags", "no_duration_filesize",
            "-max_muxing_queue_size", "2048",
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
        time.sleep(2)

@app.route("/", methods=["GET"])
def home():
    if os.path.exists("index.html"):
        return send_file("index.html")
    return jsonify({
        "status": "ok",
        "motor": "LATINSENSEISHON CLOUD RUNNER ZERO-LAG 24/7",
        "estado": ESTADO
    })

@app.route("/healthz", methods=["GET"])
@app.route("/api/status", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "motor": "LATINSENSEISHON CLOUD RUNNER ZERO-LAG 24/7",
        "estado": ESTADO
    })

if __name__ == "__main__":
    archivo = preparar_video_local()
    
    # Hilo Anti-Sleep (Evita hibernacion de Render)
    t_keepalive = threading.Thread(target=keep_alive_daemon, daemon=True)
    t_keepalive.start()
    
    # Hilos de transmision directa a Twitch y Kick
    t_twitch = threading.Thread(
        target=worker_stream,
        args=("twitch", f"rtmp://live.twitch.tv/app/{TWITCH_KEY}", archivo),
        daemon=True
    )
    t_kick = threading.Thread(
        target=worker_stream,
        args=("kick", f"rtmps://fa723fc1b171.global-contribute.live-video.net:443/app/{KICK_KEY}", archivo),
        daemon=True
    )
    t_twitch.start()
    t_kick.start()
    
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
