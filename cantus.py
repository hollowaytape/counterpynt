"""
Three canti firmi from the "Composition in Simple Counterpoint" on p128 of the Sophomore Music manual.
To be used in counterpoint stuff.
"""

from mingus.containers import Track

first = Track()
for note in ('D', 'A', 'Bb', 'A', 'G', 'D', 'F', 'E', 'D'):
    first.add_notes(note, 1)
    # current_beat attribute is currently 0.0 for all of these notes - do they play simultaneously?

second = Track()
for note in ('E-4', 'A-3', 'A-4', 'G-4', 'F-4', 'E-4', 'D-4', 'F-4', 'E-4'):
    second.add_notes(note, 1)

third = Track()
for note in ('C', 'G', 'A', 'B', 'C', 'D', 'E', 'D', 'C'):
    third.add_notes(note, 1)

closer = Track()
for note in ('D', 'D', 'E', 'F#', 'F#', 'F#', 'G', 'A',
             'A', 'A', 'B', 'B', 'A', 'rest', 'rest', 'rest',
             'A', 'A', 'G', 'F#', 'G', 'G', 'F#', 'E',
             'D', 'D', 'E', 'C#', 'D', 'rest', 'rest', 'rest'):
    closer.add_notes(note, 1)

# rests need to be placed separately in mingus?? maybe forking them is a good idea at this point

print first
print second
print third