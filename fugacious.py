""" A program to generate a two-voice simple fugue from an inputted series of notes.
Somehow, when writing a fugue, you have to write a melody that agrees with itself
displaced into the future by a certain number of notes. I probably couldn't write a program
that writes fugues, but for now I am content to find the fugue-est way of fugueing a melody.

A similar project in my head is  a program that writes a countermelody given a canta firma.
Zarlino's rules are rigid enough, right?
"""

notes_naturals = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Vertically aligned sharps and flats are equivalent, but can affect the interval's spelling.
notes_sharps = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
notes_flats =  ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

# Some notes are not valid. Here they can be corrected to a different name for the same pitch.
notes_corrected = {'B#': 'C', 'Cb': 'B', 'E#': 'F', 'Fb': 'E'}

# The letter difference between the two notes, ignoring sharps/flats, gives the interval's number.
interval_number = ['unison', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh']

# The difference in semitones, in relation to the number, gives the interval's quality.
# A difference of 0 from the expected number of semitones, naturally, accesses index 0 of this list, "major".
# A difference of 1 will access "augmented", -1 will access "minor", and so forth.
interval_quality_imperfect = ['major', 'augmented', 'double augmented', 'double diminished', 'diminished', 'minor']

# Unison, 4th, 5th, and octave follow a slightly different nomenclature.
interval_quality_perfect = ['perfect', 'augmented', 'double augmented', 'double diminished', 'diminished']

# Number of semitones between notes in a scale so that each interval is major or perfect.
diatonic_distance = [0, 2, 4, 5, 7, 9, 11, 12]


class Interval:
    def __init__(self, lo, hi):
        if lo[0] not in 'ABCDEFG' and hi[0] not in 'ABCDEFG':
            raise ValueError("Invalid note input.")

        self.lo = lo
        self.hi = hi
                                          # Maybe a separate sanitize() method would be... cleaner?
        if lo in notes_corrected:                             # Convert invalid note names to the correct ones.
            self.lo = notes_corrected[lo]                     # i.e. B# becomes C.
        if hi in notes_corrected:
            self.hi = notes_corrected[hi]

        if "#" in self.lo and "b" in self.hi:                 # Sharps/flats can't coexist, so replace the higher note.
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
        print self.semitone_distance
        print self.number
        print diatonic_distance[interval_number.index(self.number)]
        if self.number in ("unison", "fourth", "fifth", "octave"):
            self.quality = interval_quality_perfect[self.semitone_distance
                                                    - diatonic_distance[interval_number.index(self.number)]]
        else:
            self.quality = interval_quality_imperfect[self.semitone_distance
                                                      - diatonic_distance[interval_number.index(self.number)]]


    def __repr__(self):
        return self.quality + ' ' + self.number

# Testing.
a_to_b = Interval('C', 'B')
print a_to_b.lo
print a_to_b.hi
print a_to_b.semitone_distance
print a_to_b.number
print a_to_b.quality
print a_to_b