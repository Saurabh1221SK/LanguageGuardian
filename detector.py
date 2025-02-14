import speech_recognition as sr
import queue
import tempfile
import os

class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_queue = queue.Queue()
        self.listening = False

    def start_listening(self):
        self.listening = True
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.listening:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio)
                    self.audio_queue.put(text)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    print(f"Audio error: {e}")
                    break

    def stop_listening(self):
        self.listening = False

    def process_audio_file(self, audio_file):
        audio_file.seek(0)
        ext = audio_file.name.split('.')[-1].lower()
        if ext != 'wav':
            from pydub import AudioSegment
            try:
                audio_segment = AudioSegment.from_file(audio_file, format=ext)
            except Exception as e:
                return f"Error reading audio file: {e}"
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                audio_segment.export(temp_audio.name, format="wav")
                temp_audio_path = temp_audio.name
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_file.read())
                temp_audio_path = temp_audio.name
        with sr.AudioFile(temp_audio_path) as source:
            audio = self.recognizer.record(source)
        try:
            text = self.recognizer.recognize_google(audio)
            os.remove(temp_audio_path)
            return text
        except sr.UnknownValueError:
            os.remove(temp_audio_path)
            return "Could not understand the audio."
        except Exception as e:
            os.remove(temp_audio_path)
            return f"Error processing audio: {e}"
