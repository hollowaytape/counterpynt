""" A program to generate a simple two-voice fugue from an inputted series of notes.
Somehow, when writing a fugue, you have to write a melody that agrees with itself
displaced into the future by a certain number of notes. I probably couldn't write a program
that writes fugues, but for now I am content to find the fugue-est way of fugueing a melody.
"""

# Vertically aligned sharps and flats are equivalent, but can affect the interval in certain complicated ways.
notes_sharps = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
notes_flats =  ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

notes_wrong = ['B#', 'Cb', 'E#', 'Fb']

# Each interval can here be defined in semitones.
interval_value = {0: "unison", 1: "minor second", 2: "major second", 3: "minor third", 4: "major third",
                  5: "perfect fourth", 6: "tritone", 7: "perfect fifth", 8: "minor sixth",
                  9: "major sixth", 10: "minor seventh", 11: "major seventh", 12: "octave"}

# Each interval now is defined in the terms of its consonance or dissonance. Later, weighting by perfectness.
# Perfects: Unison, p5, octave.             Imperfects: m3, Maj3, m6, Maj6.           Dissonances: All others.
interval_quality = ['perfect', 'dissonance', 'dissonance', 'imperfect', 'imperfect',
                    'dissonance', 'dissonance', 'perfect', 'imperfect',
                    'imperfect', 'dissonance', 'dissonance', 'perfect']


class Interval:
    def __init__(self, lo, hi):
        self.lo = lo
        self.hi = hi

        if lo in notes_wrong or hi in notes_wrong:
            raise ValueError('Note does not exist.')          # I would rather fix the note than raise an exception...
        if "#" in self.lo and "b" in self.hi:                 # Sharps/flats can't coexist, so replace the higher note.
            self.hi = notes_sharps[notes_flats.index(hi)]     # Find the corresponding sharp note to the flat.
        elif "b" in self.lo and "#" in self.hi:
            self.hi = notes_flats[notes_sharps.index(hi)]

        if "#" in lo or "#" in hi:
            lo_index = notes_sharps.index(lo)
            hi_index = notes_sharps.index(hi)
            self.distance = hi_index - lo_index
        else:
            lo_index = notes_flats.index(lo)
            hi_index = notes_flats.index(hi)
            self.distance = hi_index - lo_index

        self.name = interval_value[self.distance]
        self.quality = interval_quality[self.distance]
        # self.weight = interval_weight[distance] (not yet implemented)

    def __repr__(self):
        return self.name

# Testing.
a_to_b = Interval('C', 'D#')
print a_to_b.lo
print a_to_b.hi
print a_to_b.distance
print a_to_b.name
print a_to_b.quality
print a_to_b