import pretty_midi
import time
from pydub import AudioSegment
from formatCLI import * 

class musicController():
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self, midiFileName : str):
        if midiFileName is None:
            self.midiFile = None
            self.allNotes = []
            self.playedNotes = []
            self.startTime = 0
        else:
            self.midiFile = pretty_midi.PrettyMIDI(midiFileName)
            self.allNotes = [n for inst in self.midiFile.instruments for n in inst.notes]
            self.allNotes.sort(key=lambda n: n.start)
            self.playedNotes = []
            self.startTime = 0
        
        # notes de 0 à 127
        self.samples_folder = "./sounds/piano_notes"  # adapte le nom de ton dossier
        self.pitch_to_audio = {}
        self.load_piano_samples()

    def playNote(self, n: int): 
        if self.midiFile is None:
            self.playedNotes.append((time.time() - self.startTime, None, None))
        else:
            note = self.allNotes[n]
            self.playedNotes.append((time.time() - self.startTime, note.pitch, note.velocity))
            print(f"Added note to list : {self.playedNotes[-1]}")

    def pitch_to_note_name(self, pitch):
        note_num = pitch % 12
        octave = (pitch // 12) - 1
        return f"{musicController.note_names[note_num]}{octave}"
    
    def load_piano_samples(self):
        for pitch in range(128):
            note_name = self.pitch_to_note_name(pitch)
            file_path = f"{self.samples_folder}/piano_{note_name}.wav"
            try:
                audio = AudioSegment.from_wav(file_path)
                self.pitch_to_audio[pitch] = audio
            except FileNotFoundError:
                printWarning(f"Sample missing: {file_path}")
                self.pitch_to_audio[pitch] = None
    
    def export_audio(self, output_file="output_piano.wav", total_duration_ms=60000):
            final_audio = AudioSegment.silent(duration=total_duration_ms)

            for start_time_sec, pitch, velocity in self.playedNotes:
                if pitch is not None and self.pitch_to_audio.get(pitch):
                    note_audio = self.pitch_to_audio[pitch]

                    # ajuster volume en fonction de velocity
                    gain = (velocity - 64) / 64 * 6  # ajustable selon besoin
                    note_audio = note_audio + gain

                    start_time_ms = int(start_time_sec * 1000)
                    final_audio = final_audio.overlay(note_audio, position=start_time_ms)

            final_audio.export(output_file, format="wav")
            printSuccess(f"Audio export : {output_file}")


