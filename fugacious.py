""" A program to generate a simple two-voice fugue from an inputted series of notes.
Somehow, when writing a fugue, you have to write a melody that agrees with itself
displaced into the future by a certain number of notes. I probably couldn't write a program
that writes fugues, but for now I am content to find the fugue-est way of fugueing a melody.
"""

# Vertically aligned sharps and flats are equivalent, but can affect the interval in certain complicated ways.
notes_sharps = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
notes_flats =  ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

# Each interval can here be defined in semitones.
interval_value = {0: "unison", 1: "minor second", 2: "major second", 3: "minor third", 4: "major third",
                  5: "perfect fourth", 6: "tritone", 7: "perfect fifth", 8: "minor sixth",
                  9: "major sixth", 10: "minor seventh", 11: "major seventh", 12: "octave"}

# Each interval now is defined in the terms of its consonance or dissonance. Later, weighting by perfectness.
# Perfects: Unison, p5, octave.             Imperfects: m3, Maj3, m6, Maj6.           Dissonances: All others.
interval_quality = ['perfect', 'dissonance', 'dissonance', 'imperfect', 'imperfect',
                    'dissonance', 'dissonance', 'perfect', 'imperfect',
                    'imperfect', 'dissonance', 'dissonance', 'perfect']

def interval(a, b):
    # First, make sure they are both in the same sharps/flats category. If not raise SharpFlatCoexistenceError.
    # Then, find the index at which notes a and b appear in the notes_X list.
    # Then, take the difference between the two.
    # Then, find the interval_value which corresponds to the two.

# Does Inteval need to be a class? It has lots of properties (semitones, name, quality, weight).