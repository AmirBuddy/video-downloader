# Video Downloader

## Description

The **Video Ripper** script is a tool that allows you to scrape video content from a video streaming website, extract video segments, and download them to your local storage. The script works by scraping a movie page, extracting `.m3u8` video links, and then downloading the segments using those links.

The `.m3u8` files are key to streaming videos, as they contain references to video segments (in chunks) that are played sequentially to create a full video stream. These files are part of the HTTP Live Streaming (HLS) protocol, which is commonly used for live video streaming and on-demand video delivery.

This script allows you to download videos in segments, which are useful when dealing with long videos or unreliable network connections, as the download can be resumed easily.

## Features

- **Web Scraping**: Scrapes video URLs from the provided movie page.
- **Extracts `.m3u8` Links**: Extracts video segment URLs from both fixed server sources and multi-language sources.
- **Downloads Segments**: Downloads the video segments and saves them locally with an optional folder for organization.
- **Resume Downloads**: Skips existing downloaded segments to allow resumption of interrupted downloads.
- **Progress Bar**: Shows the download progress of the video segments.

## How It Works

### 1. **Scraping the Movie Page**
   - The script begins by scraping a specific movie page URL (e.g., `https://vidsrc.su/embed/movie/{movie_id}`).
   - The `movie_id` is passed as an argument to generate the URL for the specific movie.
   - BeautifulSoup is used to parse the HTML content of the page.

### 2. **Extracting Video Links**
   - **Fixed Server Links**: The script looks for specific `<script>` tags in the page HTML that contain the video stream URLs. These links usually point to `.m3u8` files, which define how a video is segmented into smaller chunks.
   - **Multi-Language Links**: If available, the script can extract multi-language `.m3u8` links from the page. This allows you to choose which language version of the video to download.

### 3. **Parsing the `.m3u8` File**
   - The `.m3u8` file contains the metadata and URLs for video segments. Each segment is a small piece of the full video, and the `.m3u8` file lists the duration and the URL for each segment.
   - The script fetches the `.m3u8` playlist file, parses it to extract segment URLs and durations, and compiles a list of video segments to download.

### 4. **Downloading Video Segments**
   - The script downloads each segment (typically in `.ts` format) by sending HTTP GET requests to the segment URLs.
   - Each segment is saved in a local folder with an optional naming convention based on the segment index and duration.

### 5. **Resuming Downloads**
   - If you have already downloaded some segments, the script checks whether the segment file exists locally. If it does, the segment is skipped, and the download continues from the next available segment.
   - This feature is particularly useful for resuming downloads that may have been interrupted or paused.

### 6. **Progress Bar**
   - The script provides a visual progress bar using the `tqdm` library to show the download status of all segments.
   
## `.m3u8` Links and HLS Streaming

### Introduction to HLS, M3U8, and FFmpeg
- **HLS (HTTP Live Streaming):**:

      HLS is a streaming communication protocol created by Apple. It is used for delivering audio and video content over HTTP. HLS breaks the video into small chunks (usually 10-15 seconds) that are sent to the client and played back in real-time. This allows for adaptive bitrate streaming where the client can switch between different video qualities based on the available bandwidth.

- **M3U8:**:

      M3U8 is a file format used by HLS for listing the video segments. It contains URLs pointing to the segments of the video (often in .ts format). The file itself is a text file formatted in a specific way, listing different streams and media segments.

- **FFmpeg:**

      FFmpeg is a powerful multimedia framework used for decoding, encoding, transcoding, muxing, demuxing, streaming, and playing almost any type of multimedia content. In this project, it is used for concatenating the video segments (in .ts format) into a single playable video file.

### What is `.m3u8`?

`.m3u8` is a playlist file format used for HTTP Live Streaming (HLS). It is used to define the video segments that make up a video stream. 

- The `.m3u8` file contains references to individual video segments (typically `.ts` files) and provides metadata such as segment duration, resolution, and bitrates.
- Each segment is a chunk of video data, usually just a few seconds long.
- The `.m3u8` file allows players (like the one used in web browsers) to stream the video by requesting these segments sequentially.

### Example of `.m3u8` Playlist:

```
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:10
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:10.0,
http://example.com/video/segment0.ts
#EXTINF:10.0,
http://example.com/video/segment1.ts
#EXTINF:10.0,
http://example.com/video/segment2.ts
```

In this example:
- Each `#EXTINF` tag specifies the duration of the segment (in seconds).
- Each segment (e.g., `segment0.ts`) is a part of the full video, and the `.m3u8` file provides the URL to each segment.

### Why Use `.m3u8` Files?

- **Adaptive Streaming**: `.m3u8` files are used in adaptive bitrate streaming, which allows the video player to choose the appropriate quality based on the viewer's internet speed.
- **Segmented Video**: Videos are broken into smaller chunks (segments), which makes it easier to stream over the internet without having to load the entire video at once.
- **Resilience**: Since the video is divided into segments, the player can handle interruptions better. If the connection drops, it can resume from the last downloaded segment.

## Requirements

- Python 3.x
- The following Python packages are required:
  - `requests`
  - `beautifulsoup4`
  - `m3u8`
  - `ffmpeg` (Optional, if you need to process or convert the downloaded segments)
  - `tqdm`

You can install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

## How to Use

1. **Clone the Repository**:
   - Clone the repository to your local machine using `git`:
   
   ```bash
   git clone https://github.com/yourusername/video-ripper.git
   ```

2. **Run the Script**:
   - Replace `movie_id` with the ID of the movie you want to download (you can find the `movie_id` in the URL of the movie page).
   - Run the script:
   
   ```bash
   python video_ripper.py
   ```

   The script will scrape the movie page, extract the `.m3u8` video links, and start downloading the video segments to the `downloaded_segments/` folder.

3. **Resuming Downloads**:
   - If the download was interrupted, the script will resume from where it left off (starting from the 760th segment or any other segment that was previously downloaded).

4. **Organizing Downloads**:
   - The segments will be saved in the `downloaded_segments/` folder, and each segment will be named according to its index and duration, e.g., `segment_1_10.0s.ts`.

## Example Output

```
Downloading segments: 100%|██████████| 10/10 [00:30<00:00,  3.00s/it]
```

## License

This project is open-source and free to use. You can modify or extend it as needed. However, make sure to respect copyright and usage restrictions when downloading and distributing videos.
