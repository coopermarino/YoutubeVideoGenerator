import os
import random
from moviepy.editor import *

# Set the video resolution to 1080x1920 (1080p vertical)
video_resolution = (1080, 1920)

# Set the duration of each image in seconds
image_duration = 2

# Set the path to the folder with images
image_folder_path = "characters/"

# Get a list of all image files in the folder
image_files = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if os.path.isfile(os.path.join(image_folder_path, f))]

# Define a function to load and resize an image
def load_and_resize_image(image_file):
    # Load the image file
    image = ImageClip(image_file)
    
    # Calculate the aspect ratio of the image
    image_aspect_ratio = image.w / image.h
    
    # Calculate the required width of the image to fit the video resolution
    required_width = video_resolution[1] * image_aspect_ratio
    
    # Set the duration of the image clip
    image_clip = image.set_duration(2)
    
    # Resize the image to the required width and scale to fit the video resolution
    image_clip = image_clip.resize(width=required_width)
    image_clip = image_clip.crop(x1=(required_width-video_resolution[0])/2, x2=(required_width+video_resolution[0])/2)
    image_clip = image_clip.resize(height=video_resolution[1])
    
    return image_clip

# Keep track of the previous image file
previous_image_file = None

# Create a list of image clips
image_clips = []
for i in range(len(image_files)):
    # Choose a random image file that is not the same as the previous one
    image_file = random.choice([f for f in image_files if f != previous_image_file])
    
    # Load and resize the image file
    image_clip = load_and_resize_image(image_file)
    
    # Add the image clip to the list and set the duration
    image_clips.append(image_clip)

    
    # Print the name of the image file to the console
    print(os.path.basename(image_file))
    
    # Update the previous image file
    previous_image_file = image_file
# Concatenate the image clips into a movie
print(image_clips)
movie = concatenate_videoclips(image_clips)
# Load the "VS-Animation.mp4" 
vs_clip = VideoFileClip("resources/VS-Animation.mp4")

# Center the vs_clip in the video resolution
vs_clip = vs_clip.fx(vfx.mask_color, color=[30, 130, 35], thr=180, s=5)
vs_clip = vs_clip.resize(width=video_resolution[1])

song = AudioFileClip("songs/afterdark.mp3").subclip(54)


# Create a CompositeVideoClip by overlaying the vs_clip onto the final_movie
final_movie = CompositeVideoClip([movie, vs_clip.set_position(("center", "center"))])
final_movie = final_movie.set_audio(song)
# Set the duration of the final movie to the total duration of the vs_clip and image clips
#final_movie.duration = vs_clip.duration + len(image_clips) * image_duration

# Set the video resolution and aspect ratio to 1080p vertical
final_movie = final_movie.resize(height=video_resolution[1])
final_movie = final_movie.set_fps(25)

# Save the final movie to a file
final_movie.write_videofile("output.mp4", fps=25, codec="libx264")
