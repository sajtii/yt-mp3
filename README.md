# yt-mp3
A Python script to download music from YouTube (not YouTube Music) that meets my needs. It downloads, extracts, and converts the best audio available for free users into MP3 format and embeds the video thumbnail as cover art after processing it into a square.

Built on top of [yt-dlp](https://github.com/yt-dlp/yt-dlp), it uses [pillow](https://pypi.org/project/pillow/) to process images and [mutagen](https://pypi.org/project/mutagen/) to embed the cover art.

### Why did I create this script?
I was tired of online YouTube-to-MP3 converters, their low-quality audio, and their inability to embed cover art, which is important to me. Why? Because it looks nice on media players and on my smartwatch, which I use frequently to control music

yt-dlp itself is hard to use, and I couldn’t find a way to process thumbnails the way I wanted, so I created a script that does everything for me.


## Requirements

 - [FFmpeg](https://www.ffmpeg.org/)

    - The easiest way to install FFmpeg on Windows is to use Chocolatey, but first you have to install that.
Open Windows PowerShell as administrator (not cmd, not terminal) and paste the following command:
        
        ```Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))```

        [More info about Chocolatey](https://chocolatey.org/install#individual)

      - After installing Chocolatey, run:```choco install ffmpeg```
        
    - On Linux, install the ```ffmpeg``` package using your distribution’s package manager.
    - On macOS, use Homebrew:```brew install ffmpeg```

- [Python](https://www.python.org/)
  - On Windows, if you’ve installed Chocolatey, you can use it to install Python:```choco install python```. Alternatively, [download](https://www.python.org/downloads/) Python manually. During installation, ensure you check the "Add to PATH" box; otherwise, running the script will be difficult.
-  [yt-dlp](https://pypi.org/project/yt-dlp/), [Pillow](https://pypi.org/project/pillow/), [Mutagen](https://pypi.org/project/mutagen/)
    - If Python is installed, run:```pip install yt-dlp pillow mutagen```

## Usage
- Download and unzip (if zipped) the script.
- Open cmd, Terminal, PowerShell, or your preferred shell.
- ```cd``` into the folder where the script is
- ```python ytmp3.py```

If ```>``` appears, you’re ready to go.
- Paste a YouTube video or playlist link
- Choose how to process the cover art (four options are available)
![crop](https://github.com/user-attachments/assets/f08ac4dd-0ce5-4331-bf07-bac6b096ee5b)
- Your downloaded songs will appear in a folder called ```Downloads``` next to the script.

## Additional commands
- ```idc```: Toggles a switch. When enabled, all cover art is processed at full size without prompting for a decision. Useful for large playlists if you don’t care about customizing cover art or are fine with full-sized images.
- ```e``` or ```exit```: Exits the script. Alternatively, close the window.
