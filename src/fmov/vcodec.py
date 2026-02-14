import subprocess

def pick_vcodec(gpu: bool):
    codecs = get_vcodecs(gpu)

    if "h264_videotoolbox" in codecs:
        return "h264_videotoolbox"
    elif "h264_nvenc" in codecs:
        return "h264_nvenc"

    return codecs[0]

def get_vcodecs(gpu: bool):
    encoders = []
    if gpu:
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-encoders"],
            capture_output=True,
            text=True
        )

        for line in result.stdout.splitlines():
            line = line.strip()
            if "nvenc" in line or "videotoolbox" in line or "qsv" in line or "amf" in line:
                encoders.append(line.split()[1])

    if len(encoders) == 0:
        encoders = ["libx264"]

    return encoders

def get_vcodec_settings(vcodec):
    match vcodec:
        case "libx264":
            return { 
                "name": "libx264",
                "preset": "ultrafast",
                "crf": "8"
            }
        case "h264_videotoolbox":
            return {
                "name": "h264_videotoolbox",
                "b:v": "5000000",
                "pix_fmt": "yuv420p",
            }
        case "hevc_videotoolbox":
            return {
                "name": "hevc_videotoolbox",
                "b:v": "8000000",
                "pix_fmt": "yuv420p",
            }
        case "h264_nvenc":
            return {
                "name": "h264_nvenc",
                "preset": "llhq",
                "b:v": "5000000",
                "pix_fmt": "yuv420p",
            }
        case "hevc_nvenc":
            return {
                "name": "hevc_nvenc",
                "preset": "llhq",
                "b:v": "8000000",
                "pix_fmt": "yuv420p",
            }
        case v if "qsv" in v:
            return {
                "name": vcodec,
                "b:v": "5000000",
                "pix_fmt": "yuv420p",
            }
        case v if "amf" in v:
            return {
                "name": vcodec,
                "b:v": "5000000",
                "pix_fmt": "yuv420p",
            }

    # fallback for unknown encoder
    return { "name": vcodec }

