"""
Module: song_generator

Module with functions for PSA #4 of COMP 110 (Fall 2019).

Authors:
1) Sawyer Dentz - sdentz@sandiego.edu
2) Matt Oderlin - moderlin@sandiego.edu
"""

import sound

# Do NOT modify the scale_volume function
def scale_volume(original_sound, factor):
    """
    Decreases the volume of a sound object by a specified factor.

    Paramters:
    original_sound (type; Sound): The sound object whose volume is to be decreased.
    factor (type: float): The factor by which the volume is to be decreased.

    Returns:
    (type: Sound) A new sound object that is a copy of original_sound, but with volumes
    scaled by factor.
    """

    scaled_sound = sound.copy(original_sound)

    for smpl in scaled_sound:
        # Scale left channel of smpl
        current_left = smpl.left
        scaled_left = round(current_left * factor)
        smpl.left = scaled_left

        # Scale right channel of smpl
        current_right = smpl.right
        scaled_right = round(current_right * factor)
        smpl.right = scaled_right

    return scaled_sound


def mix_sounds(snd1, snd2):
    """
    Mixes together two sounds (snd1 and snd2) into a single sound.
    If the sounds are of different length, the mixed sound will be the length
    of the longer sound.

    This returns a new sound: it does not modify either of the original
    sounds.

    Parameters:
    snd1 (type: Sound) - The first sound to mix
    snd2 (type: Sound) - The second sound to mix

    Returns:
    (type: Sound) A Sound object that combines the two parameter sounds into a
    single, overlapping sound.
    """

    if len(snd1) > len(snd2):
        longer_sound = snd1.copy()
        shorter_sound = snd2
    else:
        longer_sound = snd2.copy()
        shorter_sound = snd1

    for i in range(len(shorter_sound)):
        longer_sound[i].left += shorter_sound[i].left
        longer_sound[i].right += shorter_sound[i].right

    return longer_sound


def song_generator(notestring):
    """
    Generates a sound object containing a song specified by the notestring.

    Parameter:
    notestring (type: string) - A string of musical notes and characters to
    change the volume and/or octave of the song.

    Returns:
    (type: Sound) A song generated from the notestring given as a paramter.
    """

    song_1 = sound.create_silent_sound(1)
    song_2 = sound.create_silent_sound(1)
    length = 1
    octave = 0
    volume = 1
    part_2 = False
    bpm = 180

    # Set bpm to what is inside of the substring
    if "]" in notestring:
        notestring_list = notestring.split("]")
        bpm = int(notestring_list[0][1:])
        notestring = notestring_list[1]

    for n in notestring:
        # Test for pause
        if n == "P":
            if not part_2:
                song_1 += sound.create_silent_sound(int(44100 / (bpm / 60)) * length)
                length = 1
            else:
                song_2 += sound.create_silent_sound(int(44100 / (bpm / 60)) * length)
                length = 1
        
        # Test for note
        elif n in ["A", "B", "C", "D", "E", "F", "G"]:
            if not part_2:
                song_1 += scale_volume(sound.Note(n, int(44100 / (bpm / 60)) * length, octave), volume)
                length = 1
            else:
                song_2 += scale_volume(sound.Note(n, int(44100 / (bpm / 60)) * length, octave), volume)
                length = 1
        
        # Test for octave
        elif n == ">":
            octave += 1
        elif n == "<":
            octave -= 1

        # Test for volume
        elif n == "+":
            volume += 0.2
        elif n == "-":
            volume -= 0.2

        # Test for parts
        elif n == "|":
            length = 1
            octave = 0
            volume = 0
            part_2 = True

        # Otherwise, n must be length
        else:
            length = int(n)
    return mix_sounds(song_1, song_2)


"""
Don't modify anything below this point.
"""

def main():
    """
    Asks the user for a notestring, generates the song from that
    notestring, then plays the resulting song.
    """
    import sounddevice
    print("Enter a notestring (without quotes):")
    ns = input()
    song = song_generator(ns)
    song.play()
    sounddevice.wait()

if __name__ == "__main__":
    main()
