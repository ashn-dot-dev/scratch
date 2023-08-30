\ Write two words called BAKE-PIE and EAT-PIE. The first word increases the
\ number of available PIES by one. The second decreases the number by one and
\ thanks you for the pie. But if there are no pies, it types “What pie?” (make
\ sure you start out with no pies.)
\
\ EAT-PIE↵What pie? ok
\ BAKE-PIE↵ok
\ EAT-PIE↵Thank you! ok

VARIABLE PIES
0 PIES !

: BAKE-PIE PIES @ 1 + PIES ! ." Baked pie!" CR ;
: EAT-PIE
    PIES @ 0 = IF
        ." What pie?"
    ELSE
        PIES @ 1 - PIES ! ." Thank you!"
    THEN CR ;

." PIES: " PIES @ . CR
BAKE-PIE
BAKE-PIE
BAKE-PIE
." PIES: " PIES @ . CR
EAT-PIE
EAT-PIE
BAKE-PIE
EAT-PIE
EAT-PIE
." PIES: " PIES @ . CR
EAT-PIE

CR ( ------------------------------------------------------------------------- )

\ Write a word called FREEZE-PIES that takes all the available pies and adds
\ them to the number of pies in the freezer. Remember that frozen pies cannot
\ be eaten.
\
\ BAKE-PIE BAKE-PIE FREEZE-PIES↵ok
\ PIES ?↵0 ok
\ FROZEN-PIES ?↵2 ok

VARIABLE FROZEN-PIES
0 FROZEN-PIES !

: FREEZE-PIES
    PIES @
    DUP ." Freezing " . ." pie(s)... "
    FROZEN-PIES @ +
    DUP . ." total." CR
    FROZEN-PIES ! 0 PIES ! ;

BAKE-PIE
FREEZE-PIES
BAKE-PIE
BAKE-PIE
FREEZE-PIES
FREEZE-PIES
BAKE-PIE
FREEZE-PIES

CR ( ------------------------------------------------------------------------- )

\ Define a word called .BASE that prints the current value of the variable BASE
\ in decimal. Test it by first changing BASE to some value other than ten.
\ (This one is trickier than it may seem.)
\
\ DECIMAL .BASE 10↵ok
\ HEX .BASE 16↵ok

: .BASE
    BASE @ DUP DECIMAL . BASE ! ;

DECIMAL .BASE CR
OCTAL .BASE CR
HEX .BASE CR
DECIMAL ( restore base to decimal )

CR ( ------------------------------------------------------------------------- )

." Skipping problem 4 because it is not interesting to me..." CR

CR ( ------------------------------------------------------------------------- )

\ In order to keep track of the inventory of colored pencils in your office,
\ create an array, each cell of which contains the count of a different colored
\ pencil. Define a set of words so that, for example, the phrase RED PENCILS
\ returns the address of the cell that contains the count of red pencils, etc.
\ Then set these variables to indicate the following counts:
\
\ 23 red pencils
\ 15 blue pencils
\ 12 green pencils
\ 0 orange pencils

VARIABLE INVENTORY 4 CELLS ALLOT
0 CONSTANT RED
1 CONSTANT BLUE
2 CONSTANT GREEN
3 CONSTANT ORANGE

: PENCILS ( pencil -- pencil-addr ) INVENTORY SWAP CELLS + ;

23 RED PENCILS !
15 BLUE PENCILS !
12 GREEN PENCILS !
0 ORANGE PENCILS !

." RED PENCILS: " RED PENCILS @ . CR
." BLUE PENCILS: " BLUE PENCILS @ . CR
." GREEN PENCILS: " GREEN PENCILS @ . CR
." ORANGE PENCILS: " ORANGE PENCILS @ . CR

CR ( ------------------------------------------------------------------------- )

\ A histogram is a graphic representation of a series of values. Each value is
\ shown by the height or length of a bar. In this exercise you will create an
\ array of values and print a histogram that displays a line of “*”s for each
\ value. First create an array with about ten cells. Initialize each element of
\ the array with a value in the range of zero to seventy. Then define a word
\ PLOT that will print a line for each value. On each line print the number of
\ the cell followed by a number of “*”s equal to the contents of that cell. For
\ example, if the array has four cells and contains the values 1, 2, 3 and 4,
\ then PLOT would produce:
\
\ 1 *
\ 2 **
\ 3 ***
\ 4 ****

VARIABLE BUCKETS 10 CELLS ALLOT

1 BUCKETS 0 CELLS + !
2 BUCKETS 1 CELLS + !
3 BUCKETS 2 CELLS + !
4 BUCKETS 3 CELLS + !
32 BUCKETS 4 CELLS + !
64 BUCKETS 5 CELLS + !
12 BUCKETS 6 CELLS + !
11 BUCKETS 7 CELLS + !
13 BUCKETS 8 CELLS + !
16 BUCKETS 9 CELLS + !

: PLOT
    10 0 DO
        I .
        BUCKETS I CELLS + @ 0 DO
             42 EMIT
        LOOP
        CR
    LOOP ;

PLOT

CR ( ------------------------------------------------------------------------- )

." Skipping problem 4 because it is not interesting to me..." CR
