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


class Interval:
    def __init__(self, lo, hi):
        self.lo = lo
        self.hi = hi

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

# Testing.
a_to_b = Interval('C', 'C')
print a_to_b.lo
print a_to_b.hi
print a_to_b.semitone_distance
print a_to_b.number
print a_to_b.quality
print a_to_b.weight
print a_to_b

user_subject = []
note_input = 0

print "Fugacious v0.1"
print "Input the subject of your fugue, one note at a time."
while True:
    note_input = raw_input("> ")
    if note_input[0] not in 'ABCDEFG':
        raise ValueError('Invalid note input.')
    if note_input in notes_corrected:
        note_input = notes_corrected[note_input]
        print "%s has been renamed %s." % (note_input, notes_corrected[note_input])

    user_subject.append(note_input)
    print user_subject