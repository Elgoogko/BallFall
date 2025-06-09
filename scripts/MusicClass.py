import pretty_midi
from pydub import AudioSegment
import pygame
from tools.formatCLI import *
import os

pygame.mixer.init()

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
            self.allNotes = []
            self.playedNotes = []
        
            for inst in self.midiFile.instruments:
                if not inst.is_drum and len(inst.notes) > 0:
                    for n in inst.notes:
                        self.allNotes.append( (n.start, n.end, n.pitch, n.velocity) )
                    break

            self.allNotes.sort(key=lambda n: n[0])  # sort by start time
        
        # notes de 0 à 127
        self.samples_folder = "./sounds/piano_notes"  # adapte le nom de ton dossier
        self.pitch_to_audio = {}
        self.load_piano_samples()

        musicController.cleanCache()

    def playNote(self, n: int): 
        if self.midiFile is None:
            self.playedNotes.append(None)
        else:
            note = self.allNotes[n]
            self.playedNotes.append(note)

           # Compléter la partie pygame.mixer.Sound
            pitch = note[2]
            velocity = note[3]
            if pitch in self.pitch_to_audio and self.pitch_to_audio[pitch]:
            # Sauvegarder temporairement le sample dans un fichier pour le charger avec pygame
                temp_file = f"./cache/temp_note_{pitch}.wav"
                self.pitch_to_audio[pitch].export(temp_file, format="wav")

                sound = pygame.mixer.Sound(temp_file)
                # Ajuste le volume en fonction de la vélocité (facultatif)
                sound.set_volume(velocity / 127.0)
                sound.play()
            # Debug
            # print(f"Added note to list : {self.playedNotes[-1]}")

    def pitch_to_note_name(self, pitch):
        note_num = pitch % 12
        octave = (pitch // 12) - 1
        return f"{musicController.note_names[note_num]}{octave}"
    
    def load_piano_samples(self):
        for pitch in range(21, 109):
            note_name = self.pitch_to_note_name(pitch)
            file_path = f"{self.samples_folder}/piano_{note_name}.wav"
            try:
                audio = AudioSegment.from_wav(file_path)
                self.pitch_to_audio[pitch] = audio
            except FileNotFoundError:
                printWarning(f"Sample missing: {file_path}")
                self.pitch_to_audio[pitch] = None
    
    def export_audio(self, output_file="output_piano.wav", total_duration_ms=60000):
        print(f"Export\n time : {total_duration_ms}\n file : {output_file}")
        final_audio = AudioSegment.silent(total_duration_ms)

        for start_sec, end_sec, pitch, velocity in self.allNotes:
            if pitch in self.pitch_to_audio and self.pitch_to_audio[pitch]:
                note_audio = self.pitch_to_audio[pitch]

                # ajuster durée
                duration_ms = int((end_sec - start_sec) * 1000)
                note_audio = note_audio[:duration_ms]  # truncate if needed

                # ajuster volume
                gain = (velocity - 64) / 64 * 6
                note_audio = note_audio + gain

                start_ms = int(start_sec * 1000)
                final_audio = final_audio.overlay(note_audio, position=start_ms)

        final_audio.export(output_file, format="wav")
        printSuccess(f"Audio export : {output_file}")
    
    @staticmethod
    def cleanCache():
        if(not os.path.exists("./cache")):
            os.mkdir("cache")
        else:
            for file in os.listdir("./cache"):
                os.remove(os.path.join("./cache", file))
        printSuccess(" cache cleaned.")