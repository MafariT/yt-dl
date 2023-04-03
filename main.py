import requests
from tqdm import tqdm
from pytube import YouTube, Playlist


def download_video(url, format):
    try:
        yt = YouTube(url)
        if format == 'mp3':
            stream = yt.streams.get_audio_only()
        else:
            stream = yt.streams.get_highest_resolution()
        total_size = stream.filesize

        # Downloading the video and show progress bar
        print(f"Downloading {yt.title}...")
        response = requests.get(stream.url, stream=True)
        with open(f"{yt.title}.{format}", "wb") as f:
            with tqdm(total=total_size, unit="B", unit_scale=True, desc=f"{yt.title}") as pbar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def download_playlist(playlist_url, format):
    try:
        playlist = Playlist(playlist_url)
        video_urls = playlist.video_urls

        for video_url in video_urls:
            download_video(video_url, format)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def start():
    url = input("Enter url: ")
    file_format = input("Enter file format (mp3, mp4): ")
    
    if "playlist" in url:
        download_playlist(url, file_format)
    else:
        download_video(url, file_format)


if __name__ == '__main__':
    start()
