# 🏛️ MANIFIESTO CÓSMICO & ARQUITECTURA MAESTRA DE TRANSMISIÓN 24/7
## Proyecto: LATINSENSEISHON / LOS CALLE TV / STUDIO PRODIGIO
**Creador Supremo:** Kevin Esteban Ruiz Calle (KRC)  
**Propósito:** Transmisión multimedia eterna 24/7 en Twitch y Kick con conmutación inteligente Híbrida (PC Local + Render Cloud) y automatización absoluta para consumo humano y de Inteligencias Artificiales.

---

```
                       ╔═══════════════════════════════════════╗
                       ║   LOS CALLE TV — NÚCLEO CÓSMICO 24/7  ║
                       ╚═══════════════════════════════════════╝
                                          │
            ┌─────────────────────────────┴─────────────────────────────┐
            ▼                                                           ▼
┌───────────────────────────────┐                           ┌───────────────────────────────┐
│     TIER 1: PC LOCAL MASTER   │                           │     TIER 2: RENDER CLOUD      │
│  (Filtros PRO, 1080p, Ticker) │                           │  (Anti-Caídas Zero-CPU 24/7)  │
└───────────────┬───────────────┘                           └───────────────┬───────────────┘
                │                                                           │
                │◄──────────────── CONMUTADOR HÍBRIDO ─────────────────────►│
                │                                                           │
                └─────────────────────────────┬─────────────────────────────┘
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
          ┌───────────────────────┐                       ┌───────────────────────┐
          │      TWITCH 24/7      │                       │       KICK 24/7       │
          │   (Políticas DMCA)    │                       │  (Mayor Permisividad) │
          └───────────────────────┘                       └───────────────────────┘
```

---

## 🧭 TABLA DE CONTENIDOS
1. [Visión & Filosofía KRC](#1-visión--filosofía-krc)
2. [Topología Híbrida (Local vs Nube)](#2-topología-híbrida-local-vs-nube)
3. [Diferencias Críticas: Twitch vs Kick](#3-diferencias-críticas-twitch-vs-kick)
4. [Especificaciones de Codificación FFmpeg](#4-especificaciones-de-codificación-ffmpeg)
5. [Pipeline Visual & Assets Gráficos](#5-pipeline-visual--assets-gráficos)
6. [Ecosistema de Archivos & Scripts (StudioProdigio)](#6-ecosistema-de-archivos--scripts-studioprodigio)
7. [Automatización de Títulos y Metadatos (Helix API)](#7-automatización-de-títulos-y-metadatos-helix-api)
8. [Matriz de Credenciales & Variables de Entorno](#8-matriz-de-credenciales--variables-de-entorno)
9. [Protocolo de Restauración Rápida (Disaster Recovery de 5 Minutos)](#9-protocolo-de-restauración-rápida-disaster-recovery-de-5-minutos)

---

## 1. VISIÓN & FILOSOFÍA KRC

LOS CALLE TV nace con la visión de crear un canal de televisión digital perpetuo (24 horas al día, 7 días a la semana, 365 días al año). 
- **Continuidad Absoluta:** Si el PC local se apaga, se reinicia o sufre un corte de luz, la nube toma el relevo de inmediato. Si el PC local enciende, la nube se repliega para ceder el canal y permitir filtros visuales de calidad de estudio.
- **Transmisión de Obras Maestras:** Contenido clásico de dominio público (Superman 1941, Popeye, Nezha, Clásicos de Oro) y series de alta resonancia cultural sin cortes publicitarios invasivos.

---

## 2. TOPOLOGÍA HÍBRIDA (LOCAL VS NUBE)

### Modo 1: PC Local (Estudio Prodigio)
* **Función:** Generación de señal en vivo de máxima fidelidad audiovisual.
* **Resolución:** 1920x1080p @ 25/30 fps.
* **Tasa de Bits:** 4500 kbps (CBR / Constant Bitrate).
* **Mejoras Aplicadas:** Reducción de ruido analógico (`hqdn3d`), nitidez (`unsharp`), corrección cromática (`eq`), barra marquesina dorada inferior con noticias y logo solar KRC transparente.
* **Supervisor:** `stream_eterno.py` vigila los procesos en segundo plano. Si FFmpeg cae por micro-parpadeos de red, se reanuda en menos de 2 segundos en el segundo exacto donde quedó.

### Modo 2: Render Cloud Runner (`latinsenseishon-stream`)
* **Función:** Guardián de respaldo en la nube cuando el PC principal está apagado.
* **Infraestructura:** Contenedor Docker en Render (Free Tier).
* **Consumo de Recursos:** 0% CPU (Modo `-c:v copy -c:a copy` directo desde fuentes optimizadas de Internet Archive).
* **Keep-Alive:** Mecanismo integrado de self-ping cada 5 minutos para evitar que el contenedor de Render entre en hibernación.
* **API de Conmutación:**
  - `POST /api/control/toggle_stream {"accion": "start"}` -> Enciende la emisión en la nube.
  - `POST /api/control/toggle_stream {"accion": "stop"}` -> Apaga la emisión en la nube (libera la ranura RTMP para el PC local).

---

## 3. DIFERENCIAS CRÍTICAS: TWITCH VS KICK

Cualquier IA o desarrollador que configure estas plataformas DEBE conocer estas diferencias para evitar baneos o cortes:

| Característica | Twitch | Kick |
| :--- | :--- | :--- |
| **URL del Servidor Ingest** | `rtmp://live.twitch.tv/app/` | `rtmps://fa723fc1b171.global-contribute.live-video.net:443/app/` |
| **Protocolo Requerido** | RTMP estándar (puerto 1935) | **RTMPS obligatorio con TLS/SSL** (puerto 443) |
| **Políticas DMCA / Música** | **Extremadamente estricto.** Detección algorítmica inmediata de audio comercial. | Moderado / Permisivo. Mayor tolerancia a emisiones de prueba y clásicos. |
| **Actualización de Títulos** | Requiere **OAuth2 App Token + User Token** vía API Helix (`PATCH /helix/channels`). | Por ahora se gestiona desde el Creator Dashboard de Kick o Webhook API. |
| **Tolerancia a Caídas de Bitrate** | Si la señal se corta más de 30 segundos, da por terminado el VOD/Stream. | Acepta buffers y reconexiones más permisivas sin cerrar la sesión. |
| **Límite de Bitrate Sugerido** | Máximo 6000 kbps (4500 kbps es el punto dulce para evitar lag a espectadores). | Acepta hasta 8000 kbps sin inconvenientes. |

---

## 4. ESPECIFICACIONES DE CODIFICACIÓN FFMPEG

Para transmitir en simultáneo a Twitch y Kick sin saturar la red, se utiliza el multiplexor `tee` de FFmpeg con cola FIFO:

```bash
ffmpeg -re -i "video_origen.mp4" \
  -filter_complex "[filtros_visuales]" \
  -c:v libx264 -preset veryfast -tune film -b:v 4500k -maxrate 4500k -bufsize 9000k -pix_fmt yuv420p \
  -g 60 -keyint_min 60 -sc_threshold 0 \
  -c:a aac -b:a 128k -ar 44100 -ac 2 \
  -use_fifo 1 -fifo_options "attempt_recovery=1:recover_any_error=1:drop_pkts_on_overflow=1" \
  -f tee "[f=flv:onfail=ignore]rtmp://live.twitch.tv/app/$TWITCH_KEY|[f=flv:onfail=ignore]rtmps://fa723fc1b171.global-contribute.live-video.net:443/app/$KICK_KEY"
```

* **`-use_fifo 1`:** Esencial. Si Twitch o Kick sufren un hipo de red, una plataforma no congela ni tumba a la otra.
* **`-g 60`:** Crea un Keyframe (GOP) cada 2 segundos exactos (30fps * 2 = 60). Requisito estricto de Twitch para visualización fluida.

---

## 5. PIPELINE VISUAL & ASSETS GRÁFICOS

El renderizado local se compone en 4 capas dentro de `-filter_complex`:

1. **Capa 0 (Base de Video):** 
   - Escala el video original a 1920x1080 manteniendo relación de aspecto y rellenando barras con negro suave (`pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black`).
   - Aplica filtro de nitidez y reducción de ruido: `hqdn3d=2:1:3:3,unsharp=3:3:0.5:3:3:0.0`.
   - Realce de color y brillo: `eq=contrast=1.08:brightness=0.04:saturation=1.22`.
2. **Capa 1 (Barra Dorada Ticker):**
   - Archivo: `assets/frame/ticker_dorado.png` (1920x56 px).
   - Ubicación: Pegada exactamente al borde inferior de la pantalla (`y=1024` a `1080`).
3. **Capa 2 (Texto en Movimiento Marquesina):**
   - Fuente: Arial Bold (`arialbd.ttf`), tamaño 28px.
   - Color: Negro carbón (`0x111111`) con relieve suave (`shadowcolor=0xFFFFFF@0.35`).
   - Lee dinámicamente de `TICKER_TEXTO.txt` con `reload=1` (permite cambiar los anuncios en vivo sin reiniciar el directo).
4. **Capa 3 (Logo Solar KRC):**
   - Archivo: `assets/logo/Koyal-Photoroom.png` (Medallón dorado con guitarra y tricolor patrio).
   - Ubicación: Esquina superior derecha (`overlay=W-w-35:30`), con transparencia elegante (`aa=0.68`).

---

## 6. ECOSISTEMA DE ARCHIVOS & SCRIPTS (StudioProdigio)

* **`stream_eterno.py`:** Orquestador principal. Previene la suspensión de Windows con la API `SetThreadExecutionState`, gestiona la conmutación apagando Render al iniciar y encendiéndolo al salir, y vigila la ejecución ininterrumpida de `dbz_stream_all.py`.
* **`dbz_stream_all.py`:** Motor de transmisión de contenidos. Gestiona las colas de reproducción (`dbz_to_play` -> `dbz_played`), guarda la posición en segundos en `dbz_stream_state.json` para reanudar transmisiones sin saltos de escena y sincroniza títulos con Twitch.
* **`TICKER_TEXTO.txt`:** Mensajes que se desplazan por la barra dorada en tiempo real.
* **`TITULO_DIRECTO_ACTUAL.txt`:** Guarda el nombre del episodio en curso.
* **`conmutador_hibrido.py`:** Script auxiliar de prueba y chequeo de salud para conmutar estados de Render.
* **Archivos `.bat` en Escritorio:**
  - `STREAM ETERNO 24-7.bat`: Enciende todo el ecosistema local.
  - `APAGAR DIRECTOS.bat`: Activa la nube en Render de inmediato y finaliza de forma segura los procesos del PC.

---

## 7. AUTOMATIZACIÓN DE TÍTULOS Y METADATOS (HELIX API)

Para cambiar el título del directo en Twitch sin entrar manualmente a la web:
* **Endpoint:** `PATCH https://api.twitch.tv/helix/channels?broadcaster_id={USER_ID}`
* **Cabeceras Obligatorias:**
  - `Client-Id: {CLIENT_ID}`
  - `Authorization: Bearer {ACCESS_TOKEN}`
  - `Content-Type: application/json`
* **Cuerpo JSON:**
  ```json
  {
    "title": "🔴 [24/7 EN VIVO] Los Calle TV — Cine Clásico & Series de Culto Sin Cortes"
  }
  ```
* En el script local, se ejecuta automáticamente cada vez que arranca un nuevo archivo multimedia leyendo el mapeo desde `dbz_titulos.json`.

---

## 8. MATRIZ DE CREDENCIALES & VARIABLES DE ENTORNO

> ⚠️ **Nota para Agentes:** Estas credenciales son las llaves maestras configuradas para el canal oficial `los-calle-tv`:

* **Twitch Stream Key:** `live_851574809_4d9Yt5LRXhlGi1NMUmYuC1JIj97REN`
* **Kick Stream Key:** `sk_us-west-2_OmepOf8fu8i6_KBoStM2ArcXUnnwXhDeyew4jBBoiYs`
* **Twitch Broadcaster User ID:** `851574809`
* **Twitch Client ID:** `gp762nuuoqcoxypju8c569th9wz7q5`
* **Twitch OAuth Token:** `20touvvbmo8dg3p5b8z4smeqeaz94u`
* **Render Service URL:** `https://latinsenseishon-stream.onrender.com`
* **Repositorio GitHub:** `https://github.com/kevinruizbolsota-svg/latinsenseishon-stream.git`

---

## 9. PROTOCOLO DE RESTAURACIÓN RÁPIDA (DISASTER RECOVERY DE 5 MINUTOS)

Si un agente o usuario necesita reconstruir este entorno desde una máquina vacía con Windows:

1. **Instalar FFmpeg y Python 3.12:**
   ```powershell
   winget install Gyan.FFmpeg
   winget install Python.Python.3.12
   ```
2. **Crear estructura de carpetas en `C:\Users\kevin\StudioProdigio`:**
   - Carpetas requeridas: `dbz_to_play`, `dbz_played`, `assets\logo`, `assets\frame`.
3. **Copiar assets base:**
   - Colocar el logo en `assets\logo\Koyal-Photoroom.png`.
   - Colocar la barra dorada en `assets\frame\ticker_dorado.png`.
4. **Instalar dependencias de Python:**
   ```powershell
   pip install flask pillow requests
   ```
5. **Configurar `stream_config.json`:**
   ```json
   {
     "twitch": { "active": true, "key": "TU_TWITCH_KEY" },
     "kick": { "active": true, "key": "TU_KICK_KEY" }
   }
   ```
6. **Ejecutar `stream_eterno.py`:**
   El sistema arrancará la emisión local, silenciará la nube de Render y transmitirá en bucle infinito auto-recuperable.
