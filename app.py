def build_ffmpeg_cmd(source_url):
    twitch_rtmp = f"rtmp://live.twitch.tv/app/{TWITCH_KEY}"
    kick_rtmp   = f"rtmps://fa723fc1b171.global-contribute.live-video.net:443/app/{KICK_KEY}"
    
    tee_target = f"[f=flv:onfail=ignore]{twitch_rtmp}|[f=flv:onfail=ignore]{kick_rtmp}"
    
    return [
        "ffmpeg",
        "-re",
        "-stream_loop", "-1",
        "-i", source_url,
        "-vf", "scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-tune", "zerolatency",
        "-b:v", "1200k",
        "-maxrate", "1200k",
        "-bufsize", "2400k",
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
