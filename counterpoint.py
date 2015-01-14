"""
1. Use only consonances. (not 2, 4, 7)
2. Begin and end on a perfect consonance. (unison, 5th, octave)
3. Use unison only at the beginning and end.
4. Avoid consecutive perfect consonances in parallel motion.
5. Alternate perfect and imperfect consonances as much as possible.
6. Use contrary motion as much as possible.
7. When writing two consecutive perfect consonances, let one voice move stepwise, the other skipwise.
8. Move stepwise as much as possible.

So, the algorithm will probably look like this:

randomly start either on unison, fifth, or octave above
for each note after:
    direction = opposite of cantus' previous direction (up/down)
    magnitude = opposite of cantus' previous magnitude (step/skip)
    consonance = opposite of cantus & counterpoint's previous consonance (perfect/imperfect)

    place the same note as before
    penalty = 0
    while the interval between the cantus' note and the contrapuntal note isn't the opposite of the previous interval:
        move one semitone in direction
        penalty =+ 1
    if penalty counter too (how?) high, try the other direction

    if the penalty for each direction is too high, maybe try the other kind of consonance?

Wait, let me figure out what the priority of each of these 8 rules should be...


"""

from cantus import first, second, third
from random import randint

initial = first[1][0][2].to_int() + (0, 7, 12)[randint(0, 2)]
# first(1= the non-instrument part of the track, 0 = first bar, 2 = the note part of the bar)
# there has to be a clearer way of accessing the note in a track...

# then, add either 0, 7, or 12 semitones to it - unison, fifth, or octave