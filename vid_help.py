import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from video_errors import NotVideoError, InvalidTimeFormat
import os
import json


def convert_times(time_dict):
    start = time_dict['start'].split(":")
    end = time_dict['end'].split(":")

    if len(start) == 3 and len(end) == 3:
        start_seconds = int(start[0]) * 60 * 60
        start_seconds += int(start[1]) * 60
        start_seconds += int(start[-1])

        end_seconds = int(end[0]) * 60 * 60
        end_seconds += int(end[1]) * 60
        end_seconds += int(end[-1])

    elif len(start) == 2 and len(end) == 2:
        start_seconds = int(start[0]) * 60
        start_seconds += int(start[-1])

        end_seconds = int(end[0]) * 60
        end_seconds += int(end[-1])
    else:
        raise InvalidTimeFormat(f"Either {start} or {end} is invalid format "
                                "should be h:m:s or m:s")

    return start_seconds, end_seconds


class Video():
    def __init__(self, vid):
        self.video = vid
        self.vid_path = vid

    def __getitem__(self, iterable):
        """iterable should be an iterable with dicts of {"start": "0:08", "end": "0:20"}"""

        video_name = os.path.splitext(os.path.basename(self.vid_path))[0]
        for time_item in iterable:
            start, end = convert_times(time_item)
            target_name = f"{video_name}_clip{start}_{end}.mp4"
            vid = self.video.subclip(start, end)
            vid.write_videofile(target_name)

    @property
    def video(self):
        return self._video

    @video.setter
    def video(self, vid_path):
        print(vid_path)
        if not isinstance(vid_path, str):
            raise ValueError(f"Can only set video path. Given {type(vid_path)}")
        if not os.path.exists(vid_path):
            raise FileNotFoundError(f"The path {vid_path} does not exist.")
        if not vid_path.lower().endswith((".mpg", ".mp4", ".mpeg", "mpeg4")):
            file_name = os.path.basename(vid_path)
            raise NotVideoError(f"Video only supports mp4 files. Given {file_name}")

        self._video = mp.VideoFileClip(vid_path)

    def read_clip_script(self, clip_script):
        if not isinstance(clip_script, str):
            raise ValueError(f"Clip script is not a string.  Given {type(clip_script)}")
        if not os.path.exists(clip_script):
            raise FileNotFoundError(f"File given does not exist. File {clip_script}")

        with open(clip_script, 'r') as file:
            data = json.load(file)

        self[data]


if __name__ == "__main__":

    vid = Video("Vader Immortal Clips 2.mp4")

    vid.read_clip_script("clip_script.json")