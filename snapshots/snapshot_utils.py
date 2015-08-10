import string
import subprocess

def snapshot(input, output, stage_id, time, dimensions):
    """takes snapshots of the video specified by input 
    at the given frequency and stores them as jpg's in 
    'output_dir'"""
    snap_ps = subprocess.call(("ffmpeg", 
                                "-ss", time,
                                "-noaccurate_seek",
                                "-i", input,
                                "-filter:v",
                                "scale=" + str(dimensions['width']) 
                                + ':' + str(dimensions['height']), 
                                "-qscale:v", "2", # best jpeg quality possible
                                "-vframes", "1",
                                output + stage_id + '-' + time[0:2] + '_' + time[3:] + '.jpg'))

def get_frame_dims(input):
    """return the frame dimensions of the video specified 
    by input.  
    ---------
    NOTE: This returns the dimensions of the 
    stored video, not necessarily how it is supposed to be
    viewed (look up Storage Aspect Ratio vs Display Aspect
    Ratio for more details)."""
    data_ps = subprocess.Popen(("ffprobe", "-v", "quiet",
                                "-print_format", "json",
                                "-show_streams",
                                input),
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
    data_msg = subprocess.check_output(('grep', 'height\|width'), 
                                    stdin=data_ps.stdout)
    msg = clean_msg(data_msg)
    dims = msg[:-1].split(',') # remove trailing comma before splitting
    dims = [int(dim.split(':')[1]) for dim in dims]
    dimensions = {'width': dims[0],
                  'height': dims[1]}
    return dimensions

def get_video_duration(path):
    """returns duration of the video specified by `path`
    as a string in the format HH:MM:SS"""
    ffmpeg_ps = subprocess.Popen(("ffmpeg", "-i", path),
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT)
    output = subprocess.check_output(('grep', 'Duration'), 
                                    stdin=ffmpeg_ps.stdout)
    duration = output[12:20]
    return duration

def get_num_frames(duration, fps):
    """returns the total number of frames contained
    in a video with the duration specified as a string
    HH:MM:SS"""
    hours = int(duration[:2])
    mins = int(duration[3:5])
    seconds = int(duration[6:8]) + (60 * mins) + (60 * 60 * hours)
    num_frames = seconds * fps
    return num_frames

def clean_msg(msg):
    """cleans up messages by removing whitespace
    and newline characters."""
    msg = msg.replace(' ', '')
    msg = msg.replace('\n', '')
    return msg