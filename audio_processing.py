from pydub import AudioSegment
import os

def normalize_audio(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    normalized = match_target_amplitude(audio, -20.0)
    equalized = equalize_audio(normalized)
    equalized.export(output_path, format="wav")

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

# Basic equalization: boost bass, reduce harsh highs
# You can adjust the filter frequencies and gains as needed

def equalize_audio(audio):
    # Apply a low-pass filter to reduce harsh highs
    audio = audio.low_pass_filter(12000)  # Cut above 12kHz
    # Apply a high-pass filter to reduce muddiness
    audio = audio.high_pass_filter(60)    # Cut below 60Hz
    # Optionally, boost bass (below 200Hz) and presence (3-6kHz)
    bass = audio.low_pass_filter(200).apply_gain(2.0)
    presence = audio.high_pass_filter(3000).low_pass_filter(6000).apply_gain(1.0)
    # Mix the boosted bands back in
    audio = audio.overlay(bass).overlay(presence)
    return audio

# Placeholder for equalization and AI enhancement 