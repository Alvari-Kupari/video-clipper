import os
from moviepy import VideoFileClip, concatenate_videoclips
import sys


VIDEO_EXTENSIONS = (
    ".mp4", ".mov", ".avi", ".mkv",  # modern formats
    ".ts", ".vob", ".mpg", ".mpeg", ".m2ts",  # DVD / old formats
    ".flv", ".wmv", ".webm", ".3gp", ".mts"  # other legacy / niche formats
)



def pause_and_exit(code=0):
    input("\nPress Enter to close...")
    sys.exit(code)




def print_help_commands():
    print("\nAvailable commands:")
    print("  stop              - exit the program")
    print("  help              - show this command list")
    print("  start-end [...]   - clip times, supports formats:")
    print("                      seconds     (e.g. 25-90)")
    print("                      mm:ss       (e.g. 0:13-1:49)")
    print("                      hh:mm:ss    (e.g. 2:12:49-3:01:59)\n")

def parse_time_str(t):
    parts = t.split(":")
    if len(parts) == 1:  # seconds only
        return float(parts[0])
    elif len(parts) == 2:  # mm:ss
        m, s = map(float, parts)
        return m * 60 + s
    elif len(parts) == 3:  # hh:mm:ss
        h, m, s = map(float, parts)
        return h * 3600 + m * 60 + s
    else:
        raise ValueError("Invalid time format")

def parse_clip_times(user_input):
    clips = []
    try:
        for part in user_input.split():
            start_str, end_str = part.split("-")
            start, end = parse_time_str(start_str), parse_time_str(end_str)
            if start >= end:
                return None
            clips.append((start, end))
        return clips
    except Exception:
        return None

def process_video(video_path, output_path):
    print(f"\nInspecting video: {os.path.basename(video_path)}")
    video = VideoFileClip(video_path)

    # Always save as .mp4
    base_name = os.path.splitext(os.path.basename(output_path))[0]
    output_path = os.path.join(os.path.dirname(output_path), f"{base_name}.mp4")

    while True:
        choice = input("Enter clip times (type 'help' for options): ").strip().lower()

        if choice == "stop":
            print("Stopping program.")
            pause_and_exit(0)

        elif choice == "help":
            print_help_commands()
            continue

        else:
            clips = parse_clip_times(choice)
            if clips is None:
                print("Invalid format. Example: 25-90 0:13-1:49 2:12:49-3:01:59\n")
                continue

            print(f"Clipping {len(clips)} section(s)...")
            try:
                video_clips = [video.subclipped(start, end) for start, end in clips]
            
            except ValueError:
                print("Invalid clip time: one or more of the clip times is longer than the length of the video. Please try again.")
                continue
            
            final = concatenate_videoclips(video_clips)
            print(f"Writing output to {output_path}")
            final.write_videofile(output_path, codec="libx264", audio_codec="aac")
            print(f"✅ Done: {output_path}")
            break

    video.close()


def main():
    # keep asking for input folder until valid
    while True:
        videos_input_location = input("\nEnter the full path of the folder with all the videos: ").strip()
        if os.path.isdir(videos_input_location):
            break
        print(f"❌ '{videos_input_location}' is not a valid folder. Please try again.")

    # keep asking for output folder until valid
    while True:
        videos_output_location = input("\nEnter the full path of the folder you want the clipped videos to go to: ").strip()
        if os.path.isdir(videos_output_location):
            break
        print(f"❌ '{videos_output_location}' is not a valid folder. Please try again.")

    print(f"\nLooking for videos in {videos_input_location}\n")

    while True:
        filename = input("\nEnter the name of the file you want to clip (or type 'stop' to exit): ").strip()

        if filename.lower() == "stop":
            print("Stopping program.")
            pause_and_exit(0)

        files = os.listdir(videos_input_location)
        video_file = None

        # look for a file starting with the given name (ignoring extension)
        for f in files:
            name, ext = os.path.splitext(f)
            if name.lower() == filename.lower() and ext.lower() in VIDEO_EXTENSIONS:
                video_file = f
                break

        if not video_file:
            print(f"❌ File '{filename}' not found in {videos_input_location}. Please try again.")
            continue

        input_path = os.path.join(videos_input_location, video_file)
        output_path = os.path.join(videos_output_location, f"clipped_{video_file}")

        process_video(input_path, output_path)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("SOME UNKNOWN ERROR OCCURRED. PLEASE SCREENSHOT THE TERMINAL AND SEND TO ALVARI")
        input("\nPress Enter to exit...")



os.system("pause")
