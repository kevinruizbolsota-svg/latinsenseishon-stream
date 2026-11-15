"""
LATINSENSEISHON — CLOUD RUNNER MOTOR 24/7 ULTRA FLUIDO
Emite a Kick y Twitch con 0% de uso de CPU (Copy Mode / Pass-through).
Incluye:
1. Control de Emisión: Reproducción dinámica por canal con API REST.
2. Botones de Control: Prender, Apagar, Cambiar Serie, Insertar Propaganda.
3. Anti-Sleep Keep-Alive: Ping cada 5 minutos para que Render Free Tier NUNCA se duerma.
4. Servidor Web Dashboard Maestro (index.html) con Controles Interactivos y Telemetría.
"""

import os, time, subprocess, threading, sys, urllib.request
from flask import Flask, jsonify, send_file, request
from datetime import datetime

app = Flask(__name__, static_folder=".")

TWITCH_KEY = os.getenv("TWITCH_STREAM_KEY", "live_851574809_4d9Yt5LRXhlGi1NMUmYuC1JIj97REN").strip()
KICK_KEY   = os.getenv("KICK_STREAM_KEY",   "sk_us-west-2_OmepOf8fu8i6_KBoStM2ArcXUnnwXhDeyew4jBBoiYs").strip()

CATALOGO = {
    "nezha": {
        "titulo": "Nezha Conquista al Rey Dragón (1979) — El Sacrificio Legendario",
        "url": "https://archive.org/download/temporuss-animes-nezha-conquers-the-drag-media-vfs-lf-9-ee-4-wc-001-360p/Temporuss-Animes-Nezha-Conquers-the-Drag_Media_VfsLf9EE4Wc_001_360p.mp4",
        "local": "/tmp/nezha_1979_stream.mp4",
        "loop": True
    },
    "superman": {
        "titulo": "Superman Clásico (1941) — Colección Completa Fleischer Studios",
        "url": "https://ia800501.us.archive.org/11/items/superman_1941/superman_1941_512kb.mp4",
        "local": "/tmp/superman_1941_stream.mp4",
        "loop": True
    },
    "propaganda": {
        "titulo": "Propaganda KRC — Comercial Oficial de la Marca & Tienda",
        "url": "https://archive.org/download/popeye_patriotic_popeye_1957/popeye_patriotic_popeye_1957_512kb.mp4",
        "local": "/tmp/propaganda_stream.mp4",
        "loop": False
    }
}

RENDER_URL = os.getenv("RENDER_EXTERNAL_URL", "https://latinsenseishon-stream.onrender.com")

SERIE_ACTUAL = "nezha"
TRANSMITIENDO_ACTIVO = True
PROCESOS = {
    "twitch": None,
    "kick": None
}

ESTADO = {
    "twitch": "INICIANDO",
    "kick": "INICIANDO",
    "serie": CATALOGO[SERIE_ACTUAL]["titulo"],
    "serie_id": SERIE_ACTUAL,
    "activo": True,
    "inicio": str(datetime.utcnow()),
    "modo": "ZERO_CPU_ANTI_SLEEP_24_7",
    "ultima_actividad": ""
}

def log(canal, msg):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    line = f"[{ts}] [{canal}] {msg}"
    print(line, flush=True)
    ESTADO["ultima_actividad"] = line

def descargar_video(clave):
    item = CATALOGO.get(clave)
    if not item:
        return None
    ruta_local = item["local"]
    if not os.path.exists(ruta_local) or os.path.getsize(ruta_local) < 500000:
        log("sistema", f"Descargando en background: {item['titulo']}...")
        try:
            urllib.request.urlretrieve(item["url"], ruta_local)
            log("sistema", f"Descarga completa ({os.path.getsize(ruta_local)} bytes).")
            return ruta_local
        except Exception as e:
            log("sistema", f"Error descarga: {e}. Usando enlace remoto directo.")
            return item["url"]
    return ruta_local

def keep_alive_daemon():
    """Realiza un ping HTTP externo cada 5 minutos para evitar que Render hiberne el contenedor."""
    log("sistema", "Iniciando guardia Anti-Sleep 24/7...")
    time.sleep(30)
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
        time.sleep(300)

def worker_canal(canal, rtmp_dest):
    global TRANSMITIENDO_ACTIVO, SERIE_ACTUAL
    while True:
        if not TRANSMITIENDO_ACTIVO:
            ESTADO[canal] = "PAUSADO"
            time.sleep(2)
            continue
            
        serie_clave = SERIE_ACTUAL
        item = CATALOGO.get(serie_clave, CATALOGO["nezha"])
        ESTADO["serie"] = item["titulo"]
        ESTADO["serie_id"] = serie_clave
        ESTADO[canal] = "TRANSMITIENDO_FLUIDO"
        
        archivo_video = descargar_video(serie_clave)
        log(canal, f"Lanzando emision: {item['titulo']} a {canal.upper()}...")
        
        loop_flag = ["-stream_loop", "-1"] if item.get("loop", True) else []
        cmd = [
            "ffmpeg",
            "-re"
        ] + loop_flag + [
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
            PROCESOS[canal] = p
            for line in p.stdout:
                if not TRANSMITIENDO_ACTIVO or SERIE_ACTUAL != serie_clave:
                    p.terminate()
                    break
                if "frame=" in line and int(line.split("frame=")[1].strip().split()[0]) % 300 == 0:
                    log(canal, line.strip())
            p.wait()
        except Exception as e:
            log(canal, f"Excepcion en proceso: {e}")
            
        if not TRANSMITIENDO_ACTIVO:
            ESTADO[canal] = "PAUSADO"
        else:
            ESTADO[canal] = "TRANSICIONANDO"
        time.sleep(1)

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

@app.route("/api/control/cambiar_serie", methods=["POST"])
def cambiar_serie():
    global SERIE_ACTUAL, TRANSMITIENDO_ACTIVO
    data = request.get_json(silent=True) or {}
    serie = data.get("serie", "nezha")
    if serie not in CATALOGO:
        return jsonify({"error": "Serie desconocida", "catalogo": list(CATALOGO.keys())}), 400
    
    SERIE_ACTUAL = serie
    TRANSMITIENDO_ACTIVO = True
    ESTADO["activo"] = True
    ESTADO["serie"] = CATALOGO[serie]["titulo"]
    ESTADO["serie_id"] = serie
    log("control", f"Cambio de programacion solicitado -> {CATALOGO[serie]['titulo']}")
    
    # Reiniciar procesos suavemente
    for canal, p in PROCESOS.items():
        if p and p.poll() is None:
            try:
                p.terminate()
            except:
                pass
    return jsonify({"status": "ok", "mensaje": f"Emitiendo {CATALOGO[serie]['titulo']}", "estado": ESTADO})

@app.route("/api/control/toggle_stream", methods=["POST"])
def toggle_stream():
    global TRANSMITIENDO_ACTIVO
    data = request.get_json(silent=True) or {}
    accion = data.get("accion") # "start", "stop" o None (toggle)
    if accion == "start":
        TRANSMITIENDO_ACTIVO = True
    elif accion == "stop":
        TRANSMITIENDO_ACTIVO = False
    else:
        TRANSMITIENDO_ACTIVO = not TRANSMITIENDO_ACTIVO
        
    ESTADO["activo"] = TRANSMITIENDO_ACTIVO
    log("control", f"Accion manual de emision: {'PRENDIDO' if TRANSMITIENDO_ACTIVO else 'APAGADO'}")
    
    if not TRANSMITIENDO_ACTIVO:
        for canal, p in PROCESOS.items():
            if p and p.poll() is None:
                try:
                    p.terminate()
                except:
                    pass
    return jsonify({"status": "ok", "activo": TRANSMITIENDO_ACTIVO, "estado": ESTADO})


@app.route('/api/manifest')
def serve_manifest():
    p = os.path.join(app.static_folder, 'MASTER_ECOSYSTEM_MANIFEST.md')
    if os.path.exists(p):
        return send_file(p, mimetype='text/markdown')
    return jsonify({'error': 'Manifiesto no encontrado'}), 404

@app.route('/api/backup/download')
def download_backup_zip():
    p = os.path.join(app.static_folder, 'BACKUP_ECOSISTEMA_KRC.zip')
    if os.path.exists(p):
        return send_file(p, as_attachment=True, download_name='BACKUP_ECOSISTEMA_KRC.zip')
    return jsonify({'error': 'Backup zip no encontrado'}), 404

if __name__ == "__main__":
    t_keepalive = threading.Thread(target=keep_alive_daemon, daemon=True)
    t_keepalive.start()
    
    t_twitch = threading.Thread(
        target=worker_canal,
        args=("twitch", f"rtmp://live.twitch.tv/app/{TWITCH_KEY}"),
        daemon=True
    )
    t_kick = threading.Thread(
        target=worker_canal,
        args=("kick", f"rtmps://fa723fc1b171.global-contribute.live-video.net:443/app/{KICK_KEY}"),
        daemon=True
    )
    t_twitch.start()
    t_kick.start()
    
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
