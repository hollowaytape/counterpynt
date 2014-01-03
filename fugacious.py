""" A program to generate a two-voice simple fugue from an inputted series of notes.
Somehow, when writing a fugue, you have to write a melody that agrees with itself
displaced into the future by a certain number of notes. I probably couldn't write a program
that writes fugues, but for now I am content to find the fugue-est way of fugueing a melody.

A similar project in my head is  a program that writes a countermelody given a canta firma.
Zarlino's rules are rigid enough, right?

Next steps: more test melodies, different note durations/octaves, MIDI playing, imitations, ASCII note graphics,
            perfect fourth dissonance toggle, key signatures, three-part fugues
"""

import time
import rtmidi

notes_naturals = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Vertically aligned sharps and flats are equivalent, but can affect the interval's spelling.
notes_sharps = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
notes_flats =  ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

# Some notes are not valid. Here they can be corrected to a different name for the same pitch.
notes_corrected = {'B#': 'C', 'Cb': 'B', 'E#': 'F', 'Fb': 'E'}

# The letter difference between the two notes, ignoring sharps/flats, gives the interval's number.
interval_number = ['unison', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh']

# Number of semitones between notes in a scale so that each interval is major or perfect.
diatonic_distance = [0, 2, 4, 5, 7, 9, 11, 12]

# The difference in semitones, in relation to the number, gives the interval's quality.
# A difference of 0 from the expected number of semitones, naturally, accesses index 0 of this list, "major".
# A difference of 1 will access "augmented", -1 will access "minor", and so forth.
interval_quality_imperfect = ['major', 'augmented', 'double augmented', 'double diminished', 'diminished', 'minor']

# Unison, 4th, 5th, and octave follow a slightly different nomenclature.
interval_quality_perfect = ['perfect', 'augmented', 'double augmented', 'double diminished', 'diminished']

perfects = ['perfect unison', 'perfect fifth', 'perfect octave']
imperfects = ['minor third', 'major third', 'minor sixth', 'major sixth']

# Dictionary comprehension mapping each note to its MIDI notation (in octave 4).
notes_midi = {note: 57 + notes_sharps.index(note) for note in notes_sharps}


class Note:
    def __init__(self, pitch, octave=4, duration=1):
        self.pitch = pitch
        self.octave = octave
        self.duration = duration

        self.pitch_midi = notes_midi[self.pitch] + ((self.octave - 4) * 12)

    def __repr__(self):
        return self.pitch + str(self.octave)


class Interval:
    def __init__(self, lo, hi):
        self.lo = lo
        self.hi = hi

        if "x" in self.lo or "x" in self.hi:                  # Dummy interval between one or more "rests".
            self.name = "unaccompanied note"
            self.weight = 0

        else:
            if "#" in self.lo and "b" in self.hi:             # Sharps/flats can't coexist, so replace the higher note.
                self.hi = notes_sharps[notes_flats.index(hi)]     # Find the corresponding sharp note to the flat.
            elif "b" in self.lo and "#" in self.hi:
                self.hi = notes_flats[notes_sharps.index(hi)]

            if "#" in self.lo or "#" in self.hi:
                lo_index = notes_sharps.index(self.lo)
                hi_index = notes_sharps.index(self.hi)
                if lo_index > hi_index:
                    self.semitone_distance = hi_index + (len(notes_sharps) - lo_index)   # If the hi note is "lower", it's
                else:                                                                    # higher but with a lower letter.
                    self.semitone_distance = hi_index - lo_index
            else:
                lo_index = notes_flats.index(self.lo)
                hi_index = notes_flats.index(self.hi)
                if lo_index > hi_index:
                    self.semitone_distance = hi_index + (len(notes_flats) - lo_index)
                else:
                    self.semitone_distance = hi_index - lo_index

            self.number = interval_number[notes_naturals.index(self.hi[0]) - notes_naturals.index(self.lo[0])]

            distance_from_major = (self.semitone_distance - diatonic_distance[interval_number.index(self.number)])
            if self.number in ("unison", "fourth", "fifth", "octave"):
                self.quality = interval_quality_perfect[distance_from_major]
            else:
                self.quality = interval_quality_imperfect[distance_from_major]

            self.name = self.quality + ' ' + self.number

            if self.quality == "perfect":      # Perfect consonances receive the highest weight.
                self.weight = 2
            elif self.name in ['minor third', 'major third', 'minor sixth', 'major sixth']:  # Imperfects receive lower.
                self.weight = 1
            else:                              # Dissonances are negative.
                self.weight = -1

    def __repr__(self):
        return self.name

# Test melodies.
songbook = {"a_scale": ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            "c_scale": ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
            "rowboat": ['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'D', 'E', 'E', 'E',   # "Row, Row, Row Your Boat"
                        'E', 'E', 'D', 'E', 'E', 'F', 'G', 'G', 'G', 'x', 'x', 'x',   # Each note is a triplet, no rests.
                        'C', 'C', 'C', 'G', 'G', 'G', 'E', 'E', 'E', 'C', 'C', 'C',   # Kinda awkward.
                        'G', 'G', 'F', 'E', 'E', 'D', 'C', 'C', 'C', 'x', 'x', 'x']   # Rounds are kinda like fugues.
            }


def format_melody(notes):
    """Formats the strings from manual_input() and turns them into appropriate Note objects."""
    formatted_list = []
    for note in notes:
        if note in notes_corrected:
            n = Note(notes_corrected[note])                              # Let the user know?
        if note == "-":                                                  # Syntax for a previous note continuing.
            n = Note(notes[notes.index(note) - 1])                       # Replace with the previous note's value.
        else:
            n = Note(note)
        formatted_list.append(n)
        print formatted_list
    return formatted_list


def play_melody(song):
    """Takes a list of notes, or tuples of simultaneous notes, and plays them through MIDI."""
    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()

    if available_ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("My virtual output")

    # For each "beat" (group of simultaneous notes) in the subject, make a list of note-ons/note-offs to trigger.
    for beat in song:
        notes_on, notes_off = ([], [])
        for note in beat:
            # Each MIDI message is a tuple of channel, pitch, and velocity. Channel 1 is 0x90, 2 is 0x91, etc.
            note_on = [(0x90 + beat.index(note)), note.pitch_midi, 112]
            notes_on.append(note_on)
            note_off = [(0x80 + beat.index(note)), note.pitch_midi, 0]
            notes_off.append(note_off)
        for note in notes_on:
            midiout.send_message(note)
        time.sleep(0.25)
        for note in notes_off:
            midiout.send_message(note)

    del midiout


def manual_input():
    # Need more forgiving syntax.
    user_subject = []
    print "Input a melody, one note at a time.\n'x' is a rest, '-' extends the previous note, 'end' to finish."
    while True:
        note_input = upper(raw_input("> "))
        if note_input[0] not in 'ABCDEFGx- end':
            raise ValueError('Invalid note input.')
        if note_input == "end":
            play_melody(format_melody(user_subject))
            print "Find the fugue? y/n"
            yesno = raw_input("> ")
            if "y" in yesno:
                find_fugue(user_subject)
        else:
            user_subject.append(note_input)
            print user_subject


def load_melody():
    print "Enter the name of the melody."
    melody = raw_input("> ")
    find_fugue(songbook[melody])


def find_fugue(user_subject):
    score_list = []
    for note_index in range(0, len(user_subject)):       # Ending a fugue is not something for computers to do.
        user_subject.append(user_subject[note_index])    # Instead, we'll simply repeat the subject twice.
    length = len(user_subject) / 2
    for stagger in range(1, length):                     # Test every amount of stagger from the 2nd to last notes.
        weight_sum = 0
        for note_index in range(0, length):                   # Sum the weights of each interval.
            i = Interval(user_subject[note_index], user_subject[note_index + stagger])
            """print note_index, "note index", stagger, "staggger"
            print i.lo, i.hi, i""" # For debugging.
            weight_sum += i.weight
        score_list.append(weight_sum)

    print user_subject
    print score_list
    print "The most consonant fugue would enter %s notes after the first." % score_list.index(max(score_list))
    # Multiple options for where to begin the fugue? A list of all the maxima would be nice to have.

print "Fugacious v0.1"
print "a) Manual input b) Name of a hard-coded melody"
input_mode = raw_input("> ")

if 'a' in input_mode:
    manual_input()
elif 'b' in input_mode:
    load_melody()