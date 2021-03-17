from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig

speech_config = SpeechConfig(subscription="your_key", region="your_region")

audio_config = AudioOutputConfig(filename="file.wav")

synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
synthesizer.speak_text_async("A simple test to write to a file.")