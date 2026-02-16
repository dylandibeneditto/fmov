import time
from fmov import Video
import cv2
import numpy as np
from tqdm import tqdm

with Video(path="video.mp4", width=1920*2, height=1080*2, fps=60, gpu=False) as video:
    total_frames = video.time_to_frame("10s")

    # accumulators
    t_alloc = 0.0
    t_text = 0.0
    t_convert = 0.0
    t_pipe = 0.0
    t_total = 0.0

    for i in tqdm(range(total_frames), total=total_frames, desc="Rendering"):
        frame_start = time.perf_counter()

        # Allocate
        s = time.perf_counter()
        frame = np.zeros((video.height, video.width, 3), dtype=np.uint8)
        t_alloc += time.perf_counter() - s

        # Draw text
        s = time.perf_counter()
        cv2.putText(
            frame,
            f"Hello world! This is frame {i}",
            (100, video.height // 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )
        t_text += time.perf_counter() - s

        # Convert BGR → RGB
        s = time.perf_counter()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        t_convert += time.perf_counter() - s

        # Pipe to ffmpeg
        s = time.perf_counter()
        video.add(frame)
        t_pipe += time.perf_counter() - s

        t_total += time.perf_counter() - frame_start

    # ---- summary ----
    print("\n=== Timing Summary (per frame avg) ===")
    print("allocate:  ", t_alloc / total_frames)
    print("draw text: ", t_text / total_frames)
    print("convert:   ", t_convert / total_frames)
    print("pipe:      ", t_pipe / total_frames)
    print("total:     ", t_total / total_frames)
