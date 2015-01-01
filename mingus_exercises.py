import mingus.core.notes as notes
from mingus.midi import fluidsynth as fluidsynth
from math import sqrt

def fibonacci(n):
    return int(((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5)))

first_hundred_fibs = [fibonacci(x) for x in range(100)]
fib_notes = [notes.int_to_note(x % 12) for x in first_hundred_fibs]

print first_hundred_fibs
print fib_notes

fluidsynth.init("RolandNicePiano.sf2")
for note in fib_notes:
    fluidsynth.play_Note(note)