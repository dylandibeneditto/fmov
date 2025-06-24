from src.fmov import Video
from PIL import Image
import numpy as np

# describes each frame
def generate_frame(frame: int, video: Video) -> Image:
    if frame % 10 == 0:
        video.audio("./examples/audio.wav", at=frame, volume=1.0)
    
    width, height = video.width, video.height
    # Create a random noise array
    array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    # Convert the array to a PIL Image
    return Image.fromarray(array)

video = Video(path="output.mp4", dimensions=(1920, 1080), fps=30, function=generate_frame, length="10s")
# allows for scrubbing through the video, WITHOUT rendering out the full video 
video.preview()

# saves the video to the output path
video.save()