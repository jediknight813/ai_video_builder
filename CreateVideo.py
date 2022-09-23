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


# song_Data = [{'text': '♪♪', 'start': 0.8, 'duration': 3.666}, {'text': "♪ YOU'RE ON THE PHONE WITH YOUR\nGIRLFRIEND, SHE'S UPSET ♪", 'start': 7.166, 'duration': 4.167}, {'text': "♪ SHE'S GOING OFF ABOUT\nSOMETHING THAT YOU SAID ♪", 'start': 11.366, 'duration': 3.5}, {'text': "♪ CAUSE SHE DOESN'T GET\nYOUR HUMOR LIKE I DO ♪", 'start': 14.9, 'duration': 6.666}, {'text': "♪ I'M IN THE ROOM,\nIT'S A TYPICAL TUESDAY NIGHT ♪", 'start': 21.6, 'duration': 4.266}, {'text': "♪ I'M LISTENING TO THE KIND\nOF MUSIC SHE DOESN'T LIKE ♪", 'start': 25.9, 'duration': 3.866}, {'text': "♪ AND SHE'LL NEVER KNOW\nYOUR STORY LIKE I DO ♪", 'start': 29.8, 'duration': 6.166}, {'text': '♪ BUT SHE WEARS SHORT SKIRTS,\nI WEAR T-SHIRTS ♪', 'start': 36.0, 'duration': 4.333}, {'text': "♪ SHE'S CHEER CAPTAIN\nAND I'M ON THE BLEACHERS ♪", 'start': 40.366, 'duration': 3.667}, {'text': '♪ DREAMING ABOUT THE DAY\nWHEN YOU WAKE UP AND FIND ♪', 'start': 44.066, 'duration': 3.167}, {'text': "♪ THAT WHAT YOU'RE LOOKING FOR\nHAS BEEN HERE THE WHOLE TIME ♪", 'start': 47.266, 'duration': 3.5}, {'text': "♪ IF YOU COULD SEE THAT I'M\nTHE ONE WHO UNDERSTANDS YOU ♪", 'start': 50.8, 'duration': 4.3}, {'text': "♪ BEEN HERE ALL ALONG,\nSO WHY CAN'T YOU SEE? ♪", 'start': 55.133, 'duration': 5.433}, {'text': '♪ YOU, YOU BELONG WITH ME,\nYOU BELONG WITH ME ♪', 'start': 60.6, 'duration': 9.1}, {'text': '♪ WALKING THE STREETS WITH YOU\nAND YOUR WORN-OUT JEANS ♪', 'start': 69.733, 'duration': 4.267}, {'text': "♪ I CAN'T HELP THINKING THIS\nIS HOW IT OUGHT TO BE ♪", 'start': 74.033, 'duration': 3.767}, {'text': '♪ LAUGHING ON A PARK BENCH,\nTHINKING TO MYSELF ♪', 'start': 77.833, 'duration': 3.667}, {'text': "♪ HEY, ISN'T THIS EASY? ♪", 'start': 81.533, 'duration': 2.467}, {'text': "♪ AND YOU'VE GOT A SMILE THAT\nCOULD LIGHT UP THIS WHOLE TOWN ♪", 'start': 84.033, 'duration': 4.6}, {'text': "♪ I HAVEN'T SEEN IT IN A WHILE\nSINCE SHE BROUGHT YOU DOWN ♪", 'start': 88.666, 'duration': 3.834}, {'text': "♪ YOU SAY YOU'RE FINE,\nI KNOW YOU BETTER THAN THAT ♪", 'start': 92.533, 'duration': 3.433}, {'text': '♪ HEY, WHAT YA DOING\nWITH A GIRL LIKE THAT? ♪', 'start': 96.0, 'duration': 3.2}, {'text': '♪ SHE WEARS HIGH HEELS,\nI WEAR SNEAKERS ♪', 'start': 99.233, 'duration': 3.967}, {'text': "♪ SHE'S CHEER CAPTAIN\nAND I'M ON THE BLEACHERS ♪", 'start': 103.233, 'duration': 3.8}, {'text': '♪ DREAMING ABOUT THE DAY\nWHEN YOU WAKE UP AND FIND ♪', 'start': 107.066, 'duration': 2.867}, {'text': "♪ THAT WHAT YOU'RE LOOKING FOR\nHAS BEEN HERE THE WHOLE TIME ♪", 'start': 109.966, 'duration': 3.667}, {'text': "♪ IF YOU COULD SEE THAT I'M THE\nONE WHO UNDERSTANDS YOU ♪", 'start': 113.666, 'duration': 3.867}, {'text': "♪ BEEN HERE ALL ALONG,\nSO WHY CAN'T YOU SEE? ♪", 'start': 117.566, 'duration': 6.534}, {'text': '♪ YOU BELONG WITH ME ♪', 'start': 124.133, 'duration': 4.4}, {'text': '♪ STANDING BY AND WAITING\nAT YOUR BACK DOOR ♪', 'start': 128.566, 'duration': 4.234}, {'text': '♪ ALL THIS TIME HOW\nCOULD YOU NOT KNOW ♪', 'start': 132.833, 'duration': 3.2}, {'text': '♪ BABY, YOU BELONG WITH ME,\nYOU BELONG WITH ME ♪', 'start': 136.066, 'duration': 11.3}, {'text': '♪ OH, I REMEMBER\nYOU DRIVING TO MY HOUSE IN\nTHE MIDDLE OF THE NIGHT ♪', 'start': 156.2, 'duration': 5.3}, {'text': "♪ I'M THE ONE\nWHO MAKES YOU LAUGH ♪", 'start': 161.533, 'duration': 1.8}, {'text': "♪ WHEN YOU KNOW YOU'RE\n'BOUT TO CRY ♪", 'start': 163.366, 'duration': 2.234}, {'text': "♪ AND I KNOW YOUR FAVORITE SONGS\nYOU TELL ME 'BOUT YOUR DREAMS ♪", 'start': 165.633, 'duration': 3.6}, {'text': "♪ THINK I KNOW WHERE YOU BELONG,\nTHINK I KNOW IT'S WITH ME ♪", 'start': 169.266, 'duration': 5.534}, {'text': "♪ CAN'T YOU SEE THAT I'M\nTHE ONE WHO UNDERSTANDS YOU ♪", 'start': 174.833, 'duration': 3.867}, {'text': "♪ BEEN HERE ALL ALONG,\nSO WHY CAN'T YOU SEE? ♪", 'start': 178.733, 'duration': 6.067}, {'text': '♪ YOU BELONG WITH ME♪', 'start': 184.833, 'duration': 4.533}, {'text': '♪ STANDING BY AND WAITING\nAT YOUR BACK DOOR ♪', 'start': 189.4, 'duration': 3.733}, {'text': '♪ ALL THIS TIME HOW\nCOULD YOU NOT KNOW ♪', 'start': 193.166, 'duration': 3.667}, {'text': '♪ BABY, YOU BELONG WITH ME,\nYOU BELONG WITH ME ♪', 'start': 196.866, 'duration': 9.8}, {'text': '♪ YOU BELONG WITH ME♪', 'start': 206.7, 'duration': 2.933}, {'text': '♪ HAVE YOU EVER\nTHOUGHT JUST MAYBE ♪', 'start': 209.666, 'duration': 4.934}, {'text': '♪ YOU BELONG WITH ME ♪', 'start': 214.633, 'duration': 3.4}, {'text': '♪ YOU BELONG WITH ME ♪', 'start': 218.066, 'duration': 4.767}]



def create_video(youtube_url, styles=", detailed aesthetic lofi illustration, portrait, landscape art", length="full" ):
    sub_data = []
    subtitles = []
    size = (1000, 512)

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


    print(song_Data)
    

    if color_clip(size, total_in_secs) == "finished":
        
        for i in song_Data:
            subtitles.append([(i["start"], i["duration"]+i["start"]), i["text"]])
            #i['text'] = i['text'].replace('♪', '')
            if len(['text']) >= 1:
                sub_data.append([(i["start"], i["duration"]+i["start"]), i["text"]])
        

        imageGen = add_images(sub_data, styles)
        add_subtitles(imageGen, subtitles)


        videoclip = VideoFileClip("./output/subs.mp4")


        videoclip = videoclip.set_audio(audioclip)
        videoclip.write_videofile("./finished-video/final_video.mp4", fps=videoclip.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")



def add_images(sub_data, styles):
    image_index = -1
    current_video_generation = -1
    for i in sub_data: 
        image_index = image_index+1
        current_video_generation = current_video_generation+1


        with open('./images/'+str(image_index)+'.png', 'wb') as f:
            text_data = i[1].replace('♪', 'music ')
            text_data = text_data.replace('\\n', "-")
            text_data = text_data.strip()
            text_data += styles               
            text_data = text_data.lower()

            print("image prompt: " + text_data)


            subprocess.call(["python3", "./stable_diffusion/demo.py", "--prompt", text_data, "--num-inference-steps", "16", "--output", ('./images/'+str(image_index)+'.png')])
            f.close()


        video_title = "videoGen"+str(current_video_generation)

        if current_video_generation == 0:
            video_title = "videoGen0"
        else:
            prevGen = (current_video_generation-1)
            print("previus gen: videoGen"+str(prevGen)+".mp4")
            video_title = "videoGen"+str(prevGen-1)

        print("next gen: ./output/"+video_title+".mp4")

        video = VideoFileClip("./output/"+video_title+".mp4")


        image = ImageClip('./images/'+str(image_index)+'.png').set_start(i[0][0]).set_duration(15).set_pos(("center","top"))
        final = CompositeVideoClip([video, image])


        final.write_videofile("./output/videoGen"+str(current_video_generation)+".mp4", temp_audiofile='temp-audio.m4a', fps=5, remove_temp=True, codec="libx264", audio_codec="aac", threads=7)
        current_video_generation = current_video_generation+1
    
    return "./output/videoGen"+str(current_video_generation-1)+".mp4"


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
    [f.unlink() for f in Path("./video-audio").glob("*") if f.is_file()] 
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



if __name__ == '__main__':
    create_video("https://www.youtube.com/watch?v=VuNIsY6JdUw", ", A digital illustration, detailed, trending in artstation, fantasy vivid colors”", 10)
