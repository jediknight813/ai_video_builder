from hashlib import new
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from pydub import *
from PIL import Image
import subprocess
from pytube import YouTube
import os
from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi
from pathlib import Path


def create_video(youtube_url, styles=", detailed aesthetic lofi illustration, portrait, landscape art", length="full", steps=16):
    sub_data = []
    subtitles = []
    size = (1000, 512)
    cleanup_files()
    get_youtube_video_audio(youtube_url)
    song_Data = get_video_transcription(youtube_url)

    if length == "full":
        audio_seg = AudioSegment.from_wav("./video-audio/musicWav.wav")
        total_in_secs = audio_seg.duration_seconds
        audioclip = AudioFileClip("./video-audio/musicMp3.mp3")
    else:
        new_data = []
        for i in song_Data:
            if int(i["start"]) <= length:
                new_data.append(i)
        song_Data = new_data
        total_in_secs = length
        audioclip = AudioFileClip("./video-audio/musicMp3.mp3").subclip(0, length)

    
    if color_clip(size, total_in_secs) == "finished":
        
        for i in song_Data:
            subtitles.append([(i["start"], i["duration"]+i["start"]), i["text"]])
            if len(['text']) >= 1:
                sub_data.append([(i["start"], i["duration"]+i["start"]), i["text"]])
        

        imageGen = add_images(sub_data, styles, steps)
        add_subtitles(imageGen, subtitles)
        videoclip = VideoFileClip("./output/subs.mp4")
        videoclip = videoclip.set_audio(audioclip)
        videoclip.write_videofile("./finished-video/final_video.mp4", fps=videoclip.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
        cleanup_files()


def add_images(sub_data, styles, steps):
    image_index = -1
    current_video_generation = 0
    for i in sub_data: 
        image_index = image_index+1
        with open('./images/'+str(image_index)+'.png', 'wb') as f:
            text_data = i[1].replace('♪', ', music vibe')
            text_data = text_data.replace('\\n', "-")
            text_data = text_data.strip()
            text_data += styles               
            text_data = text_data.lower()

            print("image prompt: " + text_data)
            subprocess.call(["python3", "./stable_diffusion/demo.py", "--prompt", text_data, "--num-inference-steps", str(steps), "--output", ('./images/'+str(image_index)+'.png')])
            f.close()

        video_title = "videoGen"+str(current_video_generation)
        video_title = "videoGen0"
        video = VideoFileClip("./output/"+video_title+".mp4")
        image = ImageClip('./images/'+str(image_index)+'.png').set_start(i[0][0]).set_duration(15).set_pos(("center","top"))
        final = CompositeVideoClip([video, image])
        final.write_videofile("./output/videoGen"+str(current_video_generation)+".mp4", temp_audiofile='temp-audio.m4a', fps=5, remove_temp=True, codec="libx264", audio_codec="aac", threads=7)
    
    return "./output/videoGen"+str(current_video_generation)+".mp4"


def color_clip(size, duration, fps=5, color=(0,0,0), output='./output/videoGen0.mp4'):
    ColorClip(size, color, duration=duration).write_videofile(output, fps=fps)
    return "finished"


def add_subtitles(video_path, subtitles):
    print("here is the path: " + video_path)
    generator = lambda txt: TextClip(txt, font='Arial', fontsize=24, color='white')

    subtitles = SubtitlesClip(subtitles, generator)

    video = VideoFileClip(video_path)
    result = CompositeVideoClip([video, subtitles.set_pos(('center','bottom'))])

    result.write_videofile("./output/subs.mp4", fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")


def get_youtube_video_audio(url):
    yt = YouTube(str(url))
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path="./video-audio")
    #base, ext = os.path.splitext(out_file)
    new_file = "./video-audio/musicMp3" + '.mp3'
    os.rename(out_file, new_file)
    subprocess.call(['ffmpeg', '-i', './video-audio/musicMp3.mp3','./video-audio/musicWav.wav'])
    print(yt.title + " has been successfully downloaded.")


def get_video_transcription(youtube_url):
    id=extract.video_id(youtube_url)
    transcript_list = YouTubeTranscriptApi.list_transcripts(id)
    transcript = transcript_list.find_manually_created_transcript(['en'])  
    return transcript.fetch()

def cleanup_files():
    [f.unlink() for f in Path("./video-audio").glob("*") if f.is_file()] 
    [f.unlink() for f in Path("./output").glob("*") if f.is_file()] 


if __name__ == '__main__':
    create_video("https://www.youtube.com/watch?v=VuNIsY6JdUw", ", A digital illustration, detailed, trending in artstation, fantasy vivid colors”", 10, 5)
