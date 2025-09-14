# VIDEO CLIPPER

This is a python tool to clip videos. I made it for my mother to help her clip and sort some videos she had been wanting to organise for a while.
I figured I would make it public just to showcase some of my work.

# Instructions

# Setup and Running
You have 2 choices to run the tool, python, and packaging / running an executable.

To run the python program directly, you need to run (in the directory with main.py):
1. pip install pymovie
2. python main.py

To make and run the exe, run 

python -m PyInstaller --onefile --console main.py

then you can double click the exe, or run 

dist/main.exe  (in a terminal)


# Using the Tool
the first 2 inputs you must give the program are:
1. The input folder with the videos. 
2. The output folder where the clipped videos should go

Then, it will prompt you to enter the name of the file to clip. just enter the name of the file (without extension).

Then, it will ask you to write the clip times. The format is:

start1-end1 start2-end2 ... etc

Where start1, end1, start2, ... are in any of the following forms:
1. hh:mm:ss
2. mm:ss
3. ss

Examples:
1. `0-56 1:23-2:12`  
   → Clips and merges the video from **0s to 56s** AND **1 min 23s to 2 min 12s**  

2. `2:15-4:30`  
   → Clips the video from **2 min 15s** to **4 min 30s**  

3. `0:30-1:00 5:00-6:45 10:00-10:30`  
   → Creates a video with **three sections merged together**:  
      - 30s to 1m  
      - 5m to 6m45s  
      - 10m to 10m30s  

4. `360-420`  
   → Clips the video from **6 min (360s)** to **7 min (420s)**  

5. `0:00-0:10 0:45-1:00 2:00-2:05`  
   → Creates a highlights reel with **short clips** stitched together.  
