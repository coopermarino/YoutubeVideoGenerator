import os
import random
from moviepy.editor import *

charactersFolder = "characters/"
songs = "songs/"
stats = "stats/"

video_resolution = (1080, 1920)


def selectcharacters():
    
    #Gets 2 Random Charates from the characters folderer
    files = os.listdir(charactersFolder)

    # Choose 2 random files from the list
    random_characters = random.sample(files, 2)

    character_names = []
    # Print the names of the random files
    for character in random_characters:
        name, extension = os.path.splitext(character)
        character_names.append(name)
        
   
    
    
    return character_names, random_characters


def makeIntro(characters, random_characters):
    
    characterIntroClips = []

    for i in range(len(random_characters)):
        random_character = random_characters[i]
        print(random_character)
        character_clip = ImageClip(f'{charactersFolder}{random_character}')

        character_clip_aspect_ratio = character_clip.w / character_clip.h
        
        required_width = video_resolution[1] * character_clip_aspect_ratio

        character = character_clip.set_duration(2).resize(width=required_width).crop(x1=(required_width-video_resolution[0])/2, x2=(required_width+video_resolution[0])/2).resize(height=video_resolution[1])


        characterIntroClips.append(character)

    IntroBackgroundClip = concatenate_videoclips(characterIntroClips)
    # Adds the VS Overlay
   
    vs_clip = VideoFileClip("resources/VS-Animation.mp4")

    # Center the vs_clip in the video resolution
    vs_clip = vs_clip.fx(vfx.mask_color, color=[30, 130, 35], thr=180, s=5)
    vs_clip = vs_clip.resize(width=video_resolution[1])


    intro_Final = CompositeVideoClip([IntroBackgroundClip, vs_clip.set_position(("center", "center"))])
    return intro_Final


def renderFinal(intro):

    final_movie = intro

    final_movie = final_movie.resize(height=video_resolution[1])
    final_movie = final_movie.set_fps(25)

    # Save the final movie to a file
    final_movie.write_videofile("output.mp4", fps=25, codec="libx264")


if __name__ == "__main__":
    characters, random_characters = selectcharacters()
    intro = makeIntro(characters, random_characters)

    renderFinal(intro)
    



