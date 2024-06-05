from pydub import AudioSegment
from pydub.playback import play
import threading
import time


def play_audio_segment(audio_segment):
    play(audio_segment)

def play_mp3(file_path, volume_reduction_db=0.3):
    audio = AudioSegment.from_file(file_path)
    quieter_audio = audio - volume_reduction_db
    play_thread = threading.Thread(target=play, args=(quieter_audio,))
    play_thread.start()
    
    
def frozen_play(filepath):
    audio = AudioSegment.from_file(filepath)
    play(audio)