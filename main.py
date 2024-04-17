from bs4 import BeautifulSoup
import requests
import re
import sys
import os

# Get the season number and episode number from the argument
if len(sys.argv) != 3:
    print("Usage: python3 main.py <season_number> <episode_number>")
    sys.exit(1)

season_number = sys.argv[1]
episode_number = sys.argv[2]

shortened_name = f"s{season_number}e{episode_number}"
url = f'https://www.diziyou.co/new-amsterdam-{season_number}-sezon-{episode_number}-bolum/'

# Fetch the HTML content
response = requests.get(url)
html_content = response.text

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Use regex to find the '<iframe id="diziyouPlayer" src="([^"]+)"' pattern
iframe_regex = re.compile(r'<iframe id="diziyouPlayer" src="([^"]+)"')
match = iframe_regex.search(html_content)

if match:
    iframe_src = match.group(1)
    print("Found iframe src:", iframe_src)

    # Extract the number from the src URL using another regex
    number_regex = re.compile(r'/player/(\d+)\.html')
    number_match = number_regex.search(iframe_src)

    if number_match:
        video_number = number_match.group(1)
        print("Extracted number:", video_number)

        m3u8_url = f'https://storage.diziyou.co/episodes/{video_number}/720p.m3u8'
        command = f'curl --output {shortened_name}.m3u8 --url {m3u8_url}'
        os.system(command)

        ffmpeg_command = f'ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i {shortened_name}.m3u8 -c copy {shortened_name}.mp4'
        os.system(ffmpeg_command)
        os.remove(f'{shortened_name}.m3u8')

        print("Done!")
else:
    print("No matching iframe found")