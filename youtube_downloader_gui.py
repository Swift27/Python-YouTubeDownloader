import customtkinter
import re
from pytube import YouTube
import os
from moviepy.editor import VideoFileClip, AudioFileClip
from tkinter import filedialog
from moviepy.editor import * 

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    # Set up the user interface
    def __init__(self):
        super().__init__()

        self.only_video = False
        self.only_audio = False
        self.url = ""

        heading_font = customtkinter.CTkFont(family="Roboto", size=45, weight="bold")
        label_font = customtkinter.CTkFont(family="Roboto", size=14)
        paste_button_font= customtkinter.CTkFont(family="Roboto", size=14, weight="bold")
        download_button_font= customtkinter.CTkFont(family="Roboto", size=24, weight="bold")

        # configure window
        self.title("YouTube Downloader")
        self.minsize(1140,580)

        # configure grid layout (4x4)
        self.columnconfigure((0,1), weight=0)
        self.columnconfigure(2, weight=1)
        self.rowconfigure((0,1,2,3), weight=1)

        # Heading
        self.heading = customtkinter.CTkLabel(self, text="YouTube Downloader", font=heading_font)
        self.heading.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Link frame
        self.link_frame = customtkinter.CTkFrame(self)
        self.link_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=50, pady=20)
        self.link_frame.columnconfigure((0,2), weight=1)
        self.link_frame.columnconfigure(1, weight=10)
        self.link_frame.rowconfigure(0, weight=1)
        self.link_frame.rowconfigure(1, weight=0)
        self.video_title_label = customtkinter.CTkLabel(self.link_frame, text="Video Title", wraplength=200, font=label_font)
        self.video_title_label.grid(row=0, column=0, sticky="nsew", padx=50)
        self.link_text_box = customtkinter.CTkEntry(self.link_frame, placeholder_text="Enter URL...", font=label_font)
        self.link_text_box.grid(row=0, column=1, sticky="ew")
        self.invalid_link_label = customtkinter.CTkLabel(self.link_frame, text="Invalid URL.", font=label_font)
        self.invalid_link_label.grid(row=1, column=1, sticky="nw", pady=(0,10))
        self.invalid_link_label.grid_remove()
        self.select_button = customtkinter.CTkButton(self.link_frame, text="Select", font=paste_button_font, cursor="hand2", command=self.get_url)
        self.select_button.grid(row=0, column=2, sticky="ew", padx=50)

        # Quality settings frame
        self.quality_settings_frame = customtkinter.CTkFrame(self)
        self.quality_settings_frame.grid(row=2, column=0, sticky="nsew", padx=(50,10), pady=20)
        self.quality_settings_frame.columnconfigure((0,1), weight=1)
        self.quality_settings_frame.rowconfigure((0,1), weight=1)
        self.video_quality_label = customtkinter.CTkLabel(self.quality_settings_frame, text="Video resolution", font=label_font)
        self.video_quality_label.grid(row=0, column=0, sticky="ew")
        self.video_quality_combobox = customtkinter.CTkComboBox(self.quality_settings_frame, font=label_font, values=["1080p"])
        self.video_quality_combobox.grid(row=1, column=0, sticky="ew", padx=(20,10))
        self.audio_quality_label = customtkinter.CTkLabel(self.quality_settings_frame, text="Audio quality", font=label_font)
        self.audio_quality_label.grid(row=0, column=1, sticky="ew")
        self.audio_quality_combobox = customtkinter.CTkComboBox(self.quality_settings_frame, font=label_font, values=["160kbps"])
        self.audio_quality_combobox.grid(row=1, column=1, sticky="ew", padx=(10,20))

        # Length settings frame
        self.length_settings_frame = customtkinter.CTkFrame(self)
        self.length_settings_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=20)
        self.length_settings_frame.columnconfigure((0,1), weight=1)
        self.length_settings_frame.rowconfigure((0,1), weight=1)
        self.length_label = customtkinter.CTkLabel(self.length_settings_frame, text="Length", font=label_font)
        self.length_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.video_start_text_box = customtkinter.CTkEntry(self.length_settings_frame, placeholder_text="0:00", font=label_font)
        self.video_start_text_box.grid(row=1, column=0, sticky="ew", padx=(20,10))
        self.video_end_text_box = customtkinter.CTkEntry(self.length_settings_frame, placeholder_text="0:00", font=label_font)
        self.video_end_text_box.grid(row=1, column=1, sticky="ew", padx=(10,20))

        # Extra settings frame
        self.extra_settings_frame = customtkinter.CTkFrame(self)
        self.extra_settings_frame.grid(row=2, column=2, sticky="nsew", padx=(10,50), pady=20)
        self.extra_settings_frame.columnconfigure((0,1), weight=1)
        self.extra_settings_frame.rowconfigure((0,1), weight=1)
        self.only_video_check_box = customtkinter.CTkCheckBox(self.extra_settings_frame, text="Download only video", font=label_font, command=self.only_video_pressed)
        self.only_video_check_box.grid(row=0, column=1, sticky="ew", pady=(10,0))
        self.only_audio_check_box = customtkinter.CTkCheckBox(self.extra_settings_frame, text="Download only audio", font=label_font, command=self.only_audio_pressed)
        self.only_audio_check_box.grid(row=1, column=1, sticky="ew", pady=(0,10))

        # Download button
        self.download_button = customtkinter.CTkButton(self, text="Download", font=download_button_font, cursor="hand2", command=self.download_button_pressed)
        self.download_button.grid(row=3, column=1, sticky="nsew", pady=50)

    """
    --------------------------------------------------------------------------------------------------------
    """

    def get_url(self):
        self.url_ = self.link_text_box.get()
        if re.search(r"^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})?$", self.url_):
            self.url = self.url_
            self.invalid_link_label.grid_remove()
            self.yt = YouTube(self.url)
            self.get_qualities(self.yt)
            self.get_video_informations(self.yt)
        else:
            self.invalid_link_label.grid()

    def get_qualities(self, yt):
        video_resolutions = [stream.resolution for stream in yt.streams.filter(type="video", progressive=False, file_extension="webm")]
        audio_qualities = [stream.abr for stream in yt.streams.filter(type="audio", progressive=False, file_extension="webm")]

        self.video_quality_combobox.configure(values=video_resolutions)
        self.audio_quality_combobox.configure(values=audio_qualities)

        self.video_quality_combobox.set(video_resolutions[0])
        self.audio_quality_combobox.set(audio_qualities[0])

    def get_video_informations(self, yt):
        self.video_title = yt.title
        self.video_author = yt.author
        self.video_length = yt.length

        self.video_title_label.configure(text=self.video_title)

        self.video_start_text_box.delete(0)
        self.video_end_text_box.delete(0)
        self.video_start_text_box.insert(0, "0:00")
        self.video_end_text_box.insert(0, f"{int(self.video_length)//60}:{(int(self.video_length)%60):02d}")

    def only_video_pressed(self):
        self.only_video = self.only_video_check_box.get()
        if self.only_video and self.only_audio:
            self.only_audio = not self.only_audio
            self.only_audio_check_box.deselect()
        print(self.only_video)

    def only_audio_pressed(self):
        self.only_audio = self.only_audio_check_box.get()
        if self.only_audio and self.only_video:
            self.only_video = not self.only_video
            self.only_video_check_box.deselect()
        print(self.only_audio)

    def download_button_pressed(self):
        if self.url:
            self.invalid_link_label.grid_remove()
            self.download_path = filedialog.askdirectory()
            self.video_quality = self.video_quality_combobox.get()
            self.audio_quality = self.audio_quality_combobox.get()
            self.download_video_and_audio(self.yt, self.video_quality, self.audio_quality, self.download_path, self.only_video, self.only_audio, "")
        else:
            self.invalid_link_label.grid()

    def download_video_and_audio(self, yt, video_quality, audio_quality, download_path, only_video, only_audio, file_name):
        print(self.download_path)
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

        if not (self.only_audio or self.only_video):
            self.merge_clip(self.download_path, "")

    def merge_clip(self, download_path, file_name):
        # Merge the downloaded video and audio to a single video with audio
        video_file = os.path.join(download_path, "video.webm")
        audio_file = os.path.join(download_path, "audio.webm")

        if os.path.isfile(video_file):
            video_clip = VideoFileClip(video_file)
        else:
            print("Video error")
        if os.path.isfile(audio_file):
            audio_clip = AudioFileClip(audio_file)
        else:
            print("audio error")

        video_clip_with_audio = video_clip.set_audio(audio_clip)  
        if file_name:
            video_clip_with_audio.write_videofile(os.path.join(download_path, f"{file_name}.mp4"))
        else:
            video_clip_with_audio.write_videofile(os.path.join(download_path, "final.mp4"))

        os.remove(video_file)
        os.remove(audio_file)

if __name__ == "__main__":
    app = App()
    app.mainloop()