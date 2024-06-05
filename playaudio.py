from pydub import AudioSegment
from pydub.playback import play

def play_mp3(file_path):
    audio = AudioSegment.from_mp3(file_path)
    play(audio)
    