from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import re, os


def get_url() -> str:
    # Prompt user for URL of YouTube video, check if URL is valid, return URL
    while True:
        url = input("Enter URL: ").strip()
        if re.search(r"^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})?$", url):
            return url
        else:
            print("Invalid URL.")

def get_quality(yt):
    # Print the available video and audio qualities, prompt user for quality and return selected video quality and selected audio quality
    selected_video_resolution = ""
    selected_audio_quality = ""

    # All possible qualities for the specific video
    video_resolutions = [stream.resolution for stream in yt.streams.filter(type="video", progressive=False, file_extension="webm")]
    audio_qualities = audio_qualities = [stream.abr for stream in yt.streams.filter(type="audio", progressive=False, file_extension="webm")]

    # Prompt user for video quality
    while True:
        print(f"Available video resolutions: {*video_resolutions,}")
        video_resolution = input("Select video resolution: ")
        if video_resolution in video_resolutions:
            selected_video_resolution = video_resolution
            break
    
    # Prompt user for audio quality
    while True:
        print(f"Available audio qualities: {*audio_qualities,}")
        audio_quality = input("Select audio quality: ")
        if audio_quality in audio_qualities:
            selected_audio_quality = audio_quality
            break

    return selected_video_resolution, selected_audio_quality

def get_download_path():
    # Prompt user for download file path, check if file path exists and return the file path
    while True:
        file_path = input("Enter download path: ").strip()
        if os.path.exists(file_path):
            return "".join([part + "\\\\" for part in file_path.split("\\")])
        else:
            print("Invalid file path.")

def download_video_and_audio(yt, video_quality, audio_quality, download_path, only_video, only_audio, file_name):
    # Download video and audio seperately to the download_path
    if not only_audio:
        video_itag = yt.streams.filter(type="video", progressive=False, res=video_quality, file_extension="webm").itag_index.items()
    if not only_video:
        audio_itag = yt.streams.filter(type="audio", progressive=False, abr=audio_quality, file_extension="webm").itag_index.items()

    if not only_audio and len(video_itag) == 1:
        stream = yt.streams.get_by_itag([key for key, _ in video_itag][0])
        if only_video and file_name:
            stream.download(download_path, filename=f"{file_name}.webm")
        else:
            stream.download(download_path, filename="video.webm")

    if not only_video and (len(audio_itag) == 1) == 1:
        stream = yt.streams.get_by_itag([key for key, _ in audio_itag][0])
        if only_audio and file_name:
            stream.download(download_path, filename=f"{file_name}.webm")
        else:
            stream.download(download_path, filename="audio.webm")

def merge_clip(download_path, file_name):
    # Merge the downloaded video and audio to a single video with audio
    video_file = os.path.join(download_path, "video.webm")
    audio_file = os.path.join(download_path, "audio.webm")

    if os.path.isfile(video_file):
        video_clip = VideoFileClip(video_file)
    if os.path.isfile(audio_file):
        audio_clip = AudioFileClip(audio_file)

    video_clip_with_audio = video_clip.set_audio(audio_clip)  
    if file_name:
        video_clip_with_audio.write_videofile(os.path.join(download_path, f"{file_name}.mp4"))
    else:
        video_clip_with_audio.write_videofile(os.path.join(download_path, "final.mp4"))

    os.remove(video_file)
    os.remove(audio_file)

def get_extras():
    # Promp user for any extras (only video, only audio, specific file name)
    while True:
        extras_wanted = input("Would you like to make additional settings? (y/n) ").strip().lower()
        if extras_wanted == "y":
            return True
        elif extras_wanted == "n":
            return False
        else:
            print("Invalid input.")

def specify_extras():
    # Get all extra settings (only video, only audio, specific file name) and return them in a dictionary
    extras = {}

    while True:
        only_video = input("Do you want to download only the video without audio? (y/n) ").strip().lower()
        if only_video == "y":
            extras["only_video"] = True
            extras["only_audio"] = False
            break
        elif only_video == "n":
            extras["only_video"] = False
            only_audio = input("Do you want to download only the audio without video? (y/n) ").strip().lower()
            if only_audio == "y":
                extras["only_audio"] = True
                break
            elif only_audio == "n":
                extras["only_audio"] = False
                break
            else:
                print("Invalid input.")
        else:
            print("Invalid input.")

    file_name = input("What should the file name be? ").strip()
    extras["file_name"] = file_name

    return extras

def main():
    url = get_url()
    yt = YouTube(url)

    video_quality, audio_quality = get_quality(yt)
    download_path = get_download_path()

    extras = {}
    if get_extras():
        extras = specify_extras()

    download_video_and_audio(yt, video_quality, audio_quality, download_path, extras["only_video"], extras["only_audio"], extras["file_name"])
    if not (extras["only_video"] or extras["only_audio"]):
        merge_clip(download_path, extras["file_name"])

if __name__ == "__main__":
    main()