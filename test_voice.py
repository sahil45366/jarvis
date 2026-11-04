import torch
import torchaudio
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

print("Loading Chatterbox model...")

device = "cuda" if torch.cuda.is_available() else "cpu"

model = ChatterboxMultilingualTTS.from_pretrained(device=device)

print("Model loaded successfully!")

text = "Hello! Main Sahil ka personal AI assistant hoon. Main Hindi aur English dono mein baat kar sakta hoon."

wav = model.generate(
    text,
    language_id="hi",
    audio_prompt_path="Sahil_voice_reference_clean.wav"
)

torchaudio.save(
    "sahil_voice_test.wav",
    wav.cpu(),
    model.sr
)

print("Voice generated: sahil_voice_test.wav")