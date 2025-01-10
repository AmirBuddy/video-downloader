import requests
import m3u8
from tqdm import tqdm  # Optional, for progress bars
import os

def fetch_playlist(url):
    # Send a GET request to the playlist URL
    response = requests.get(url)
    
    # Ensure the request was successful
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch playlist: {response.status_code}")
        return None

def download_segment(segment_url, output_filename):
    response = requests.get(segment_url, stream=True)
    
    with open(output_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print(f"Downloaded {output_filename}")

def parse_playlist(playlist_text):
    # Parse the playlist using the m3u8 library
    playlist = m3u8.loads(playlist_text)

    # Extract segment URLs
    segment_urls = [segment.uri for segment in playlist.segments]
    return segment_urls

def download_video_segments(segment_urls, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Download each segment
    for idx, segment_url in enumerate(tqdm(segment_urls, desc="Downloading segments")):
        output_filename = os.path.join(output_folder, f"segment_{idx + 1}.ts")
        download_segment(segment_url, output_filename)

def main():
    # URL of the main playlist (GET request URL you mentioned earlier)
    playlist_url = "https://tralvoxmoon.xyz/file2/V66LYT8Ua+FCgr82YCE~xX4eFVfhpUvYp8LdxQWhRrkTa+FZffNbMRg+DBxVA9jEhmHS~WCL6G6PRDrCTsCNQCivggWtuEfw1CQYrBzx1UnEn6G9okGla2JhMyS1lpNnQjuChgeJqNE6Ub9Md7m9xYlqJSw7Vstph6VGQbf2r3I=/MTA4MA==/aW5kZXgubTN1OA==.m3u8"
    
    # Fetch the main playlist
    playlist_text = fetch_playlist(playlist_url)
    
    if playlist_text:
        # Parse the playlist to get segment URLs
        segment_urls = parse_playlist(playlist_text)
        
        # Download the segments
        output_folder = "video_segments"
        download_video_segments(segment_urls, output_folder)
        
        print("All segments downloaded!")
    else:
        print("Failed to fetch playlist.")

if __name__ == "__main__":
    main()
