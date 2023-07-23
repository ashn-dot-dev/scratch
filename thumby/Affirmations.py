# /Games/Affirmations/Affirmations.py
#
# Displays an affirmation from a set of affirmation phrases as scrolling text
# across the screen. Created as a gift for my partner so that they could carry
# around positive affirmations on a keychain.
import random
import thumby

FPS = 30 # Reasonable speed for scrolling text.
BORDER_WIDTH = 5

# BITMAP: width: 9, height: 9
HEART = bytearray([
    12,30,63,126,252,126,63,30,12,
    0,0,0,0,0,0,0,0,0
])
HEART_LEN = 9
HEART_OFFSET = 2

PHRASES = [
    "i love you",
    "you are a strong woman",
    "i love your smile",
    "you are my honey bee",
    "i am lucky to have you as my partner",
    "you are so special to me",
    "you are loved by those around you",
    "you give me butterflies",
]
BONUS = "bonus affirmation"

# NOTE: For some reason the random seed always seems to be the same, so
# shuffling the list is deterministic. =A
"""
# The Thumby MicroPython random module does not seem to contain shuffle.
def shuffle(lst):
    for i in reversed(range(1, len(lst))):
        j = random.randrange(0, len(lst) - 1)
        lst[i], lst[j] = lst[j], lst[i]

shuffle(PHRASES)
"""

phrase = 0
offset = 0
bonus = False

thumby.display.setFPS(FPS)

while True:
    thumby.display.fill(0)
    thumby.display.blit(
        HEART,
        HEART_OFFSET,
        HEART_OFFSET,
        HEART_LEN, HEART_LEN, 0, 0, 0)
    thumby.display.blit(
        HEART,
        HEART_OFFSET,
        thumby.display.height - HEART_LEN - HEART_OFFSET,
        HEART_LEN, HEART_LEN, 0, 0, 0)
    thumby.display.blit(
        HEART,
        thumby.display.width - HEART_LEN - HEART_OFFSET,
        HEART_OFFSET,
        HEART_LEN, HEART_LEN, 0, 0, 0)
    thumby.display.blit(
        HEART,
        thumby.display.width - HEART_LEN - HEART_OFFSET,
        thumby.display.height - HEART_LEN - HEART_OFFSET,
        HEART_LEN, HEART_LEN, 0, 0, 0)
    thumby.display.drawText(PHRASES[phrase] if not bonus else BONUS, thumby.display.width - offset, 16, 1)

    # Actions are listed in priority order. The first action to be selected
    # will dicate the behavior of this frame, e.g. if A and B are both pressed
    # on the same frame then the action for A is taken over B.
    if thumby.buttonA.justPressed():
        # Advance to the next phrase.
        phrase = (phrase + 1) % len(PHRASES)
        offset = 0
        bonus = False
    elif thumby.buttonB.justPressed():
        # Reset the current phrase.
        offset = 0
        bonus = False
    elif thumby.buttonD.justPressed():
        # Cycle forwards in the phrases (same as A button action).
        offset = 0
        bonus = True
    elif thumby.buttonL.justPressed():
        # Cycle backwards in the phrases.
        phrase = (phrase - 1) % len(PHRASES)
        offset = 0
        bonus = False
    elif thumby.buttonR.justPressed():
        # Cycle forwards in the phrases (same as A button action).
        phrase = (phrase + 1) % len(PHRASES)
        offset = 0
        bonus = False
    else:
        # Continue playing the current phrase.
        offset += 1

    thumby.display.update()
