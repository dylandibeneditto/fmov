import cairo
import numpy as np
from PIL import Image
from fmov import Video

# This example demonstrates how to use PyCairo (vector graphics) to create a video with a moving rectangle.

def pilImageFromCairoSurface( surface ):
   cairoFormat = surface.get_format()
   if cairoFormat == cairo.FORMAT_ARGB32:
      pilMode = 'RGB'
      argbArray = np.frombuffer(surface.get_data(), dtype=np.uint8).reshape(-1, 4)
      rgbArray = argbArray[ :, 2::-1 ]
      pilData = rgbArray.reshape( -1 ).tobytes()
   else:
      raise ValueError( 'Unsupported cairo format: %d' % cairoFormat )
   pilImage = Image.frombuffer( pilMode,
         ( surface.get_width(), surface.get_height() ), pilData, "raw",
         pilMode, 0, 1 )
   pilImage = pilImage.convert( 'RGB' )
   return pilImage

width, height = 1920, 1080

with Video((width, height), framerate=30, path="./video.mp4", pix_fmt="rgba", prompt_deletion=False) as video:
   for i in range(video.seconds_to_frame(10)):
      surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
      ctx = cairo.Context(surface)

      # Make the background transparent
      ctx.set_source_rgba(0, 0, 0, 0)
      ctx.paint()

      ctx.set_source_rgba(1.0, 0.0, 0.0, 0.5) # semitransparent red color
      
      # This creates animation - the rectangle moves across the screen
      x_position = 50 + (i * 5) % (width - 300)  # Move the rectangle
      ctx.rectangle(x_position, 50, 300, 200)
      ctx.fill()
      
      newimage = pilImageFromCairoSurface(surface)

      video.pipe(newimage)