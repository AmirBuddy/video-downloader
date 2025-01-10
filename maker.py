import os
import imageio_ffmpeg as ffmpeg
import subprocess

import os

# Create filelist.txt from the .ts segments in the video_segments folder
def create_filelist(output_folder):
    # Get all .ts files from the output folder
    ts_files = [f for f in os.listdir(output_folder) if f.endswith('.ts')]
    
    # Sort the files lexicographically (in case their names are like segment_1.ts, segment_2.ts, etc.)
    ts_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))  # Sort based on the segment number
    
    # Write the list to a file
    filelist_path = os.path.join(output_folder, "filelist.txt")
    with open(filelist_path, 'w') as f:
        for ts_file in ts_files:
            # Use absolute path for the segment files
            segment_path = os.path.join(os.getcwd(), output_folder, ts_file)
            f.write(f"file '{segment_path}'\n")

    print(f"Filelist created at {filelist_path}.")
    return filelist_path

# Merge the .ts segments into a single video using imageio-ffmpeg
def merge_segments_with_ffmpeg(output_folder, output_filename):
    # Create filelist.txt
    filelist_path = create_filelist(output_folder)

    # Get the path to ffmpeg using imageio_ffmpeg
    ffmpeg_path = ffmpeg.get_ffmpeg_exe()

    # Run ffmpeg to merge the segments
    command = [
        ffmpeg_path, "-f", "concat", "-safe", "0", "-i", filelist_path, "-c", "copy", output_filename
    ]
    
    # Execute the command
    subprocess.run(command, check=True)
    print(f"Video saved as {output_filename}")

# Main function to execute the merging
def main():
    # Path to the folder containing the video segments
    output_folder = "video_segments"
    output_filename = "output_video.mp4"  # Desired output file name
    
    # Call the function to merge the segments
    merge_segments_with_ffmpeg(output_folder, output_filename)

# Execute the main function if this script is run directly
if __name__ == "__main__":
    main()
