"""Allen Forte has a theory of musical harmony based on set theory, and he says it's the key to
understanding some of the weirder 20th century music.

His analysis does a lot with "intervalic vectors," which are lists of each kind of interval in a chord.

I'm hoping to see what I can do with Forte-style analyses of music in the form of MIDI files.
"""

import mingus.core.chords as chords
import mingus.core.intervals as intervals

augurs_of_spring_chord = chords.from_shorthand("Eb7|Fb")               # Example chord w/ interesting vector
interval_class_map = [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]              # Interval with i semitones is class A[i].


def interval_class(note_first, note_second):
    """ class 1: minor seconds/major sevenths (1 or 11)
        class 2: major seconds/minor sevenths (2 or 10)
        class 3: minor thirds /major sixths   (3 or 9)
        class 4: major thirds /minor sixths   (4 or 8)
        class 5: perfect fourths & fifths     (5 or 7)
        class 6: tritones                     (6)
    """
    return interval_class_map[intervals.measure(note_first, note_second)]


def chord_to_vector(chord):
    vector = [0, 0, 0, 0, 0, 0]
    for i_first, note_first in enumerate(chord):                         # For each note,
        for i_second, note_second in enumerate(chord[i_first+1:]):       # pair it with each subsq. note
            determined_class = interval_class(note_first, note_second)
            vector[(determined_class - 1)] += 1
    return vector

"""
to determine the vector of a chord:
    set the vector = [0, 0, 0, 0, 0, 0]
    for every note in the chord:
        for every note from the next until the last one:
            measure the interval
            determine which part of the vector it goes in
            insert it into the vector
    return the vector
"""

print chord_to_vector(augurs_of_spring_chord)