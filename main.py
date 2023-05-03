import os
import random
import json

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
    
    vs_clip = vs_clip.set_start(1)
    vs_clip = vs_clip.set_end(3)
    vs_clip = vs_clip.fadeout(0.2)

    intro_Final = CompositeVideoClip([IntroBackgroundClip, vs_clip.set_position(("center", "center"))])
    return intro_Final


import os
import json
import random

def getStats(characters):
    stats_folder = 'characters/stats'
    stats_files = [os.path.join(stats_folder, character + '.json') for character in characters]
    stats = []
    for stats_file in stats_files:
        if os.path.exists(stats_file):
            with open(stats_file) as f:
                stats.append(json.load(f))
        else:
            print(f"It looks like {os.path.basename(stats_file)} doesn't have a stats file.")
            create_stats_file = input("Do you want to automatically create one? (Y/N): ")
            if create_stats_file.lower() == 'y':
                stats_file_data = {}
                stats_file_data['name'] = os.path.basename(stats_file).replace('.json', '')
                randomise_stats = input("Do you want to randomise stats automatically? (Y/N): ")
                if randomise_stats.lower() == 'y':
                    stats_file_data['skills'] = {}
                    with open('resources/PotentialStats.txt') as f:
                        potential_stats = f.read().splitlines()
                    random_stats = random.sample(potential_stats, k=5)
                    for skill in random_stats:
                        stats_file_data['skills'][skill] = random.randint(0, 10)
                else:
                    num_manual_stats = 5
                    stats_file_data['skills'] = {}
                    for i in range(num_manual_stats):
                        stat = input(f"Enter stat {i+1}: ")
                        stat_name, stat_value = stat.split('=')
                        stat_name = stat_name.strip()
                        stat_value = int(stat_value.strip())
                        stats_file_data['skills'][stat_name] = stat_value
                with open(stats_file, 'w') as f:
                    json.dump(stats_file_data, f)
                stats.append(stats_file_data)
            else:
                print("To Proceed You Must Create a Stats File, This Can either be done manually or automated.")
                
    return stats

def compareStats(charaterStats):
    skills = set()
    for character in charaterStats:
        skills.update(character['skills'].keys())

    overall_scores = {character['name']: sum(character['skills'].values()) for character in charaterStats}
    results = {}

    for i, skill in enumerate(skills):
        character1_score = charaterStats[0]['skills'].get(skill, 0)
        character2_score = charaterStats[1]['skills'].get(skill, 0)

        if character1_score == character2_score:
            random_winner = charaterStats[random.randint(0, 1)]['name']
            overall_scores[random_winner] += 1
            print(f"Tie breaker randomising {skill} winner: {random_winner}")
            winner = random_winner
        else:
            winner = charaterStats[0]['name'] if character1_score > character2_score else charaterStats[1]['name']
            overall_scores[winner] += 1

        results[skill] = winner

    overall_winner_score = max(overall_scores.values())
    overall_winners = [k for k, v in overall_scores.items() if v == overall_winner_score]
    overall_winner = overall_winners[0] if len(overall_winners) == 1 else random.choice(overall_winners)
    results['overall_winner'] = overall_winner

    return json.dumps(results, indent=4)



def renderFinal(intro):

    clips_array_final = [intro]

    final_movie = concatenate_videoclips(clips_array_final)
    final_movie = final_movie.resize(height=video_resolution[1])
    final_movie = final_movie.set_fps(25)

    # Save the final movie to a file
    final_movie.write_videofile("output.mp4", fps=25, codec="libx264")



if __name__ == "__main__":
    characters, random_characters = selectcharacters()
    intro = makeIntro(characters, random_characters)
    characterStats = getStats(characters)
    statWinner = compareStats(characterStats)
    print(statWinner)

    #renderFinal(intro)
    



