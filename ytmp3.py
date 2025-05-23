import yt_dlp
import sys
import os
from PIL import Image, ImageFilter
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from urllib.parse import urlparse, parse_qs

com = None
title = None
script_dir = os.path.dirname(os.path.abspath(__file__))
def_dir = os.path.join(script_dir, "Downloads")
os.makedirs(def_dir, exist_ok=True)
idc = False



ydl_opts = {
    'quiet': True,
    'format': 'bestaudio',
    'extract_audio': True,
    'audio_format': 'mp3',
    'audio_quality': '0',
    'outtmpl': os.path.join(def_dir, '%(title)s.%(ext)s'),
    'writethumbnail': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '0',
    }, {
        'key': 'FFmpegThumbnailsConvertor',
        'format': 'jpg',
        'when': 'before_dl'
    },{
        'key': 'FFmpegMetadata'
    }],
}

def extract_list(id):
    url = f'https://www.youtube.com/playlist?list={id}'
    opts = {
        'quiet': True,
        'extract_flat': True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        result = ydl.extract_info(url, download=False)
        if 'entries' in result:
            video_urls = [entry['url'] for entry in result['entries']]
        print(f'{len(video_urls)} videos found in the playlist.')
    return video_urls

def get_id(url):
    videos = []
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    if parsed.netloc == 'youtu.be':
        v_id = parsed.path.lstrip('/')
        v_url = f'https://www.youtube.com/watch?v={v_id}'
        videos.append(v_url)
    elif 'list' in params and 'v' in params:
        print('Playlist detected!')
        print('Would you like to download the entire playlist or just the current video?')
        while True:
            dec = input('y/yes or n/no (download the current video): ')
            if dec in ('y', 'Y', 'yes', 'YES', 'Yes'):
                videos = extract_list(params['list'][0])
                break
            elif dec in ('n', 'N', 'no', 'No', 'NO'):
                v_url = f'https://www.youtube.com/watch?v={params['v'][0]}'
                videos.append(v_url)
                break
    elif 'v' in params:
        if params['v']:
            v_url = f'https://www.youtube.com/watch?v={params['v'][0]}'
            videos.append(v_url)
    elif 'list' in params and params['list'][0]:
        print('Playlist detected!')
        videos = extract_list(params['list'][0])
    return videos


def download(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        info = info_dict.copy()
        name = os.path.splitext(ydl.prepare_filename(info))[0]
        return name


def crop_cover(filename):
    path = os.path.join(def_dir, filename + '.jpg')
    img = Image.open(path)
    width, height = img.size
    crop_left, crop_middle, crop_right, crop_full = None, None, None, None
    preview_path = None
    if not idc:
        x = 0
        crop_left = img.crop((x, 0, x + height, height))
        crop_left = crop_left.resize((width, width), Image.Resampling.LANCZOS)
        x = (width // 2) - (height // 2)
        crop_middle = img.crop((x, 0, x + height, height))
        crop_middle = crop_middle.resize((width, width), Image.Resampling.LANCZOS)
        x = width - height
        crop_right = img.crop((x, 0, x + height, height))
        crop_right = crop_right.resize((width, width), Image.Resampling.LANCZOS)

    crop_full = Image.new("RGB", (width, width))

    zoom_f = width / height
    zoomed_size = (int(width * zoom_f), int(height * zoom_f))
    zoomed_img = img.resize(zoomed_size, Image.Resampling.LANCZOS)

    blurred_img = zoomed_img.filter(ImageFilter.GaussianBlur(radius=10))
    b_width, b_height = blurred_img.size
    x = (width // 2) - (b_width // 2)
    y = (width // 2) - (b_height // 2)

    crop_full.paste(blurred_img, (x, y))
    y = (width // 2) - (height // 2)
    crop_full.paste(img, (0, y))

    if not idc:
        preview = Image.new("RGB", (width * 4, width))
        preview.paste(crop_left, (0, 0))
        preview.paste(crop_middle, (width, 0))
        preview.paste(crop_right, (width * 2, 0))
        preview.paste(crop_full, (width * 3, 0))
        preview_path = os.path.join(script_dir, 'preview.jpg')
        preview.save(preview_path)
        print(f"Where would you like to crop the cover art for '{os.path.basename(filename)}'?")
        print('The preview image is available in the script’s folder.')
        while True:
            crop_target = input('r - right, m - middle, l - left, f - full size: ')
            if crop_target in ('l', 'L'):
                crop_left.save(path)
                break
            elif crop_target in ('m', 'M'):
                crop_middle.save(path)
                break
            elif crop_target in ('r', 'R'):
                crop_right.save(path)
                break
            elif crop_target in ('f', 'F'):
                crop_full.save(path)
                break

    if idc:
        crop_full.save(path)
    if preview_path is not None:
        os.remove(preview_path)

def burn_cover(title):
    audio_path = os.path.join(def_dir, title + '.mp3')
    cover_path = os.path.join(def_dir, title + '.jpg')
    audio = MP3(audio_path, ID3=ID3)
    try:
        audio.add_tags()
    except:
        pass

    with open(cover_path, 'rb') as file:
        cover_data = file.read()

    audio.tags.add(
        APIC(
            encoding =0,
            mime='image/jpeg',
            type=3,
            desc='Front Cover',
            data=cover_data
        )
    )
    audio.save()
    os.remove(cover_path)

while True:
    com = input(">")

    if com in ('e', 'E', 'exit', 'EXIT', 'Exit'):
        sys.exit()
    elif com in ('idc', 'IDC', 'Idc'):
        idc = not idc
        if idc:
            print('Every song is downloaded with full-sized cover art.')
        elif not idc:
            print('You can choose how to format the cover art.')
    elif "youtube" in com or "youtu.be" in com:
        if 'music.youtube.com' in com:
            print('YouTube Music is not supported!')
        else:
            ids = get_id(com)
            prog = len(ids)
            count = 1
            for i in ids:
                print(f'[{count}/{prog}] Downloading...')
                title = download(i)
                crop_cover(title)
                burn_cover(title)
                print(f"[{count}/{prog}] '{os.path.basename(title)}' successfully downloaded and processed!")
                count += 1
    else:
        print('Unknown command or URL.')