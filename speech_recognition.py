from google.cloud import speech_v1
from google.cloud import texttospeech_v1
import asyncio
import io

class SpeechHandler:
    def __init__(self):
        self.speech_client = speech_v1.SpeechClient()
        self.tts_client = texttospeech_v1.TextToSpeechClient()

    async def transcribe_audio(self, audio_content: bytes, language_code: str = "nl-NL") -> str:
        """Transcribe audio content using Google Speech-to-Text."""
        audio = speech_v1.RecognitionAudio(content=audio_content)
        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.OGG_OPUS,
            language_code=language_code,
            model="default",
            enable_automatic_punctuation=True,
        )

        try:
            response = await asyncio.to_thread(
                self.speech_client.recognize, config=config, audio=audio
            )
            if response.results:
                return response.results[0].alternatives[0].transcript
            return ""
        except Exception as e:
            print(f"Error in transcription: {e}")
            return ""

    async def generate_audio(self, text: str, language_code: str = "nl-NL") -> bytes:
        """Generate audio from text using Google Text-to-Speech."""
        synthesis_input = texttospeech_v1.SynthesisInput(text=text)
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL,
        )
        audio_config = texttospeech_v1.AudioConfig(
            audio_encoding=texttospeech_v1.AudioEncoding.MP3,
        )

        try:
            response = await asyncio.to_thread(
                self.tts_client.synthesize_speech,
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )
            return response.audio_content
        except Exception as e:
            print(f"Error in audio generation: {e}")
            return b""

    async def evaluate_pronunciation(self, reference: str, transcription: str) -> float:
        """
        Evaluate pronunciation accuracy using simple string comparison.
        Returns a score between 0 and 1.
        """
        reference = reference.lower().strip()
        transcription = transcription.lower().strip()
        
        if not reference or not transcription:
            return 0.0
            
        # Using Levenshtein distance for basic comparison
        from difflib import SequenceMatcher
        return SequenceMatcher(None, reference, transcription).ratio()