\ First create a word named STARS which will print out n stars on the same
\ line, given n on the stack:
\
\ 10 STARS↵********** ok

: STARS ( n -- )
    0 DO 42 EMIT LOOP ;

10 STARS CR

CR ( ------------------------------------------------------------------------- )

\ Next define BOX which prints out a rectangle of stars, given the width and
\ height (number of lines), using the stack order ( width height — ).
\
\ 10 3 BOX
\ **********
\ **********
\ ********** ok

: BOX ( w h -- )
    0 DO DUP STARS CR LOOP DROP ;

10 3 BOX

CR ( ------------------------------------------------------------------------- )

\ Now create a word named \STARS which will print a skewed array of stars (a
\ rhomboid), given the height on the stack. Use a DO loop and, for simplicity,
\ make the width a constant ten stars.
\
\    3 \STARS
\ **********
\  **********
\   ********** ok

: \STARS ( n -- )
    0 DO
        I 0 DO
            J 0 = IF LEAVE THEN
            32 EMIT
        LOOP
        10 STARS CR
    LOOP ;

3 \STARS CR ;

CR ( ------------------------------------------------------------------------- )

\ Now create a word which slants the stars the other direction: call it /STARS.
\ It should take the height as a stack input and use a constant ten width. Use
\ a DO loop.

: /STARS ( n -- )
    DUP 0 DO
        DUP I 1 + <> IF
        DUP I 1 + - 0 DO
            32 EMIT
        LOOP
        THEN
        10 STARS CR
    LOOP
    DROP ;

3 /STARS CR ;

CR ( ------------------------------------------------------------------------- )

\ Now redefine this last word, using a BEGIN…UNTIL loop.

: /STARS ( n -- )
    BEGIN
        DUP I - 1 - SPACES
        10 STARS CR
    1 - DUP NOT
    UNTIL DROP ;

3 /STARS CR ;

CR ( ------------------------------------------------------------------------- )

\ Write a definition called DIAMONDS which will print out the given number of
\ diamond shapes, as shown in this example.
\
\   2 DIAMONDS
\                      *
\                     ***
\                    *****
\                   *******
\                  *********
\                 ***********
\                *************
\               ***************
\              *****************
\             *******************
\             *******************
\              *****************
\               ***************
\                *************
\                 ***********
\                  *********
\                   *******
\                    *****
\                     ***
\                      *
\                      *
\                     ***
\                    *****
\                   *******
\                  *********
\                 ***********
\                *************
\               ***************
\              *****************
\             *******************
\             *******************
\              *****************
\               ***************
\                *************
\                 ***********
\                  *********
\                   *******
\                    *****
\                     ***
\                      *

: DIAMOND ( -- )
    9 0 DO
        9 I - SPACES
        I 0 DO
            J 0 = IF LEAVE THEN
            42 EMIT
        LOOP
        42 EMIT
        I 0 DO
            J 0 = IF LEAVE THEN
            42 EMIT
        LOOP
        CR
    LOOP
    9 2 * 1 + 0 DO 42 EMIT LOOP CR
    9 0 DO
        I 1 + SPACES
        8 I - 0 DO
            J 8 = IF LEAVE THEN
            42 EMIT
        LOOP
        42 EMIT
        8 I - 0 DO
            J 8 = IF LEAVE THEN
            42 EMIT
        LOOP
        CR
    LOOP ;

: DIAMONDS ( n -- )
    0 DO DIAMOND LOOP ;

2 DIAMONDS

CR ( ------------------------------------------------------------------------- )

: R% 10 */ 5 + 10 / ;

: DOUBLED ( balance interest-rate -- )
    SWAP DUP -ROT 21 1 DO
        CR ." YEAR " I 2 U.R
        2DUP R% +  DUP ."    BALANCE " .
        ROT DUP >R -ROT DUP R> 2 * > IF
            CR ." doubled in " I . ." years " LEAVE
        THEN
    LOOP 2DROP DROP ;

1000 6 DOUBLED CR

CR ( ------------------------------------------------------------------------- )

\ Define a word called ** that will compute exponential values, like this:
\
\    7 2 ** .  49 ok 
\
\ (seven squared)
\
\    2 4 ** .  16 ok 
\
\ (two to the fourth power). For simplicity, assume positive exponents only
\ (but make sure ** works correctly when the exponent is one — the result
\ should be the number itself)

: ** ( base exponent -- base-raised-to-the-exponent )
    DUP 0 = IF 2DROP 1 ELSE
    DUP 1 = IF DROP ELSE
    1 - OVER >R
    BEGIN
        R> DUP >R
        ROT *
        SWAP 1 -
    DUP NOT UNTIL
    R> 2DROP
    THEN THEN ;

: TEST-** ( base exponent -- base-raised-to-the-exponent )
    2DUP SWAP . ." to the power " . ." equals " ** . CR ;

7 2 TEST-**
2 4 TEST-**
5 0 TEST-**
5 1 TEST-**
1 5 TEST-**
