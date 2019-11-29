try:
    from lineusmusic import Keyboard
    from lineus import LineUs
except ImportError:
    print('\n*** You need to install the lineusmusic module: \'pip install lineusmusic\' ***')
    exit(1)

# Don't forget to 'pip install lineusmusic' before you run the code.

# Music notation is lower case for natural notes and upper case for sharp, so 'a' is natural a
# and A is a#. Next, we have the octave, '-' is one octave down and '+' one up. The key is fixed
# as c major at the moment so this means that the note below c on the keyboard is b-. Lastly we have the duration.
# The default length is one beat, the length of which is set using set_bpm(), and you can set the length to
# multiples of this. So, for example a2 is an 'a' note played for two beats. An 'r' indicates a rest of one beat.
#
# When you create the Keyboard object it moves Line-us to a 'home' position. This is keyboard
# specific but for the Volca and Stylophone it's 'c' so the input() is included in the code to allow you to
# make sure your Line-us is in the right position before playing the song.
#
# It's easy to add a new keyboard type (see the LineUsMusic module docs for details) but for now we have
# support for Stylophone and the Korg VolcaFM (actually it will work for some of the other Volcas too).
# Line-us can't reach to full range of the Volca keyboard so there are two options keyboard='VolcaFM'
# and keyboard='VolcaFMLow'. I've included scales for the keyboards we support so you can see what notes
# you have available.

areFriendsElectric = ('c', 'c', 'g', 'r', 'A-', 'A-', 'f', 'r', 'c', 'c', 'g', 'r', 'A-', 'A-', 'A', 'e')
closeEncounters = ('g', 'a', 'f', 'f-', 'c')        # only for VolcaFMLow

volca_low_scale = ('f-', 'g-', 'a-', 'b-', 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'c+', 'd+', 'e+')
volca_scale = ('g-', 'a-', 'b-', 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'c+', 'd+', 'e+', 'f+')
stylophone_scale = ('a-', 'A-', 'b-', 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'c+', 'd+', 'e+')

song = areFriendsElectric

my_lineus = LineUs()
my_lineus.connect('line-us.local')
k = Keyboard(my_lineus, keyboard='Stylophone')
k.set_bpm(110)

input('Set Line-us to \'c\':')

for song_note in song:
    k.play_note(song_note)
