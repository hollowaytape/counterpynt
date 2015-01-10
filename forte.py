import mingus.core.chords as chords
import mingus.core.intervals as intervals

augurs_of_spring_chord = chords.from_shorthand("Eb7|Fb")
interval_class_map = [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]

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
    for note_first in chord:
        for note_second in chord[note_first::]:
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