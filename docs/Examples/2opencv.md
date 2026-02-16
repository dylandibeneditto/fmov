# Hello World with OpenCV

![output](../assets/opencv.mp4)

```py title="main.py"
from fmov import Video
import cv2
import numpy as np
from tqdm import tqdm

# using 'with Video() as video' makes rendering simpler, as when the context ends it calls render automatically
with Video(path="video.mp4", width=1920, height=1080, fps=60) as video:
    total_frames = video.time_to_frame("20s") # turns the timestamp "20s" into the number of frames in the video

    # create all the frames in the video (tqdm is a progress bar)
    for i in tqdm(range(total_frames), total=total_frames, desc="Rendering"):

        frame = np.zeros((video.height, video.width, 3), dtype=np.uint8)

        cv2.putText(
            frame,
            f"Hello world! This is frame {i}",
            (100, video.height // 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (255, 255, 255),  # white in BGR
            2,
            cv2.LINE_AA
        )

        # Convert BGR to RGB (because ffmpeg input is rgb24)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        video.add(frame) # add the frame to the end of the video
```
