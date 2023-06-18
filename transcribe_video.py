import speech_recognition as sr
import moviepy.editor as mp

# Convert MP4 to WAV
video_path = "test.mp4"
audio_path = "audio.wav"

video = mp.VideoFileClip(video_path)
video.audio.write_audiofile(audio_path)

audio_path = "audio.wav"
output_file = "transcription.txt"

r = sr.Recognizer()

with sr.AudioFile(audio_path) as source:
    audio = r.record(source)

try:
    transcript = r.recognize_google(audio)
    print("Transcription:")
    print(transcript)

    with open(output_file, "w") as file:
        file.write(transcript)
        print(f"Transcription saved to {output_file}")
except sr.UnknownValueError:
    print("Speech recognition could not understand audio")
except sr.RequestError as e:
    print(f"Error occurred during speech recognition: {e}")