(
What will the phrase

    0= 0=

leave on the stack when the argument is

    -1?          0?        200?
)

 -1 .S 0 = 0 = . CR ( TRUE )
  0 .S 0 = 0 = . CR ( FALSE )
200 .S 0 = 0 = . CR ( TRUE )

CR ( ------------------------------------------------------------------------- )

( Explain what an artichoke has to do with any of this. )

." Your guess is as good as mine." CR

CR ( ------------------------------------------------------------------------- )

(
Define a word called CARD which, given a person’s age on the stack,
prints out either of these two messages {depending on the relevant laws
in your area}:

    ALCOHOLIC BEVERAGES PERMITTED or UNDER AGE
)

: DRINKING-AGE 21 ;
: CARD ( age -- )
    DRINKING-AGE <
    IF ." UNDER AGE"
    ELSE ." ALCOHOLIC BEVERAGES PERMITTEED"
    THEN ;
18 .S CARD CR
21 .S CARD CR
25 .S CARD CR

CR ( ------------------------------------------------------------------------- )

(
Define a word called SIGN.TEST that will test a number on the stack and print
out one of three messages:

    POSITIVE or ZERO or NEGATIVE
)

: SIGN.TEST ( n -- )
    DUP 0 > IF ." POSITIVE" DROP ELSE
    0 < IF ." NEGATIVE" ELSE
    ." ZERO"
    THEN THEN ;

-2 .S SIGN.TEST CR
-2 .S SIGN.TEST CR
0 .S SIGN.TEST CR
1 .S SIGN.TEST CR
2 .S SIGN.TEST CR

CR ( ------------------------------------------------------------------------- )

(
In Chap. 1, we defined a word called STARS in such a way that it always prints
at least one star, even if you say

    0 STARS↵* ok

Using the word STARS, define a new version of STARS that corrects this problem.
)

: STAR 42 EMIT ;
: STARS ( n -- ) 0 DO STAR LOOP ;
: STARS ( n -- ) DUP IF STARS ELSE DROP THEN ;

3 STARS ." <- 3" CR
2 STARS ." <- 2" CR
1 STARS ." <- 1" CR
0 STARS ." <- 0" CR

CR ( ------------------------------------------------------------------------- )

(
Write the definition for the word WITHIN which expects three arguments:

    { n lo-limit hi-limit -- }

and leaves a “true” flag only if “n” is within the range

    low-limit <= n < hi-limit
)

: WITHIN ( n lo-limit hi-limit -- )
    ROT DUP ROT <
    -ROT <= AND ;

: TEST-WITHIN ( n lo-limit hi-limit -- )
    3DUP SWAP ROT . . . ." WITHIN -> " WITHIN . CR ;

0 1 3 TEST-WITHIN
1 1 3 TEST-WITHIN
2 1 3 TEST-WITHIN
3 1 3 TEST-WITHIN
4 1 3 TEST-WITHIN

CR ( ------------------------------------------------------------------------- )

(
Here’s a number guessing game {which you may enjoy writing more than anyone
will enjoy playing}. First you secretly enter a number onto the stack {you can
hide your number after entering it by executing the word PAGE, which clears the
terminal screen}. Then you ask another player to enter a guess followed by the
word GUESS, as in

    100 GUESS

The computer will either respond “TOO HIGH,” “TOO LOW,” or “CORRECT!” Write the
definition of GUESS, making sure that the answer-number will stay on the stack
through repeated guessing until the correct answer is guessed, after which the
stack should be clear.
)

: GUESS ( n guess -- n? )
    2DUP SWAP < IF ." TOO LOW" THEN
    2DUP SWAP > IF ." TOO HIGH" THEN
    2DUP = IF ." CORRECT!" DROP THEN
    DROP ;

: TEST-GUESS ( n guess -- n? )
    ." number=" OVER . ." guess=" DUP . ." -> " GUESS CR ;

50
20 TEST-GUESS
70 TEST-GUESS
49 TEST-GUESS
51 TEST-GUESS
50 TEST-GUESS

CR ( ------------------------------------------------------------------------- )

(
Using nested tests and IF…ELSE…THEN statements, write a definition called
SPELLER which will spell out a number on the stack, from -4 to 4. If the number
is outside this range, it will print the message “OUT OF RANGE.” For example:

    2 SPELLER↵two ok
    -4 SPELLER↵negative four ok
    7 SPELLER↵OUT OF RANGE ok

Make it as short as possible. {Hint: The Forth word ABS gives the absolute
value of a number on the stack.}
)

: SPELLER ( n -- )
    DUP ABS 4 > IF ." OUT OF RANGE" ELSE
    DUP 0 < IF ." negative " THEN
    ABS
    DUP 0 = IF ." zero" ELSE
    DUP 1 = IF ." one" ELSE
    DUP 2 = IF ." two" ELSE
    DUP 3 = IF ." three" ELSE
    DUP 4 = IF ." four" ELSE
    THEN THEN THEN THEN THEN THEN DROP ;

: TEST-SPELLER ( n -- )
    DUP . ." SPELLER -> " SPELLER CR ;

-5 TEST-SPELLER
-4 TEST-SPELLER
-3 TEST-SPELLER
-2 TEST-SPELLER
-1 TEST-SPELLER
0 TEST-SPELLER
1 TEST-SPELLER
2 TEST-SPELLER
3 TEST-SPELLER
4 TEST-SPELLER
5 TEST-SPELLER

CR ( ------------------------------------------------------------------------- )

(
Using your definition of WITHIN from Prob. 6, write another number-guessing
game, called TRAP, in which you first enter a secret value, then a second
player tries to home in on it by trapping it between two numbers, as in this
dialogue:

    0 1000 TRAP↵BETWEEN ok
    330 660 TRAP↵BETWEEN ok
    440 550 TRAP↵NOT BETWEEN ok
    330 440 TRAP↵BETWEEN ok

and so on, until the player guesses the answer:

    391 391 TRAP↵YOU GOT IT! ok

Hint: you may have to modify the arguments to WITHIN so that TRAP does not say
“BETWEEN” when only one of the arguments is equal to the hidden value.
)

: TRAP ( n lo hi -- n )
    3DUP           ( n lo hi n lo hi )
    ROT DUP -ROT   ( n lo hi lo n hi n )
    =              ( n lo hi lo n hi=n )
    -ROT           ( n lo hi hi=n lo n )
    =              ( n lo hi hi=n lo=n )
    AND IF ." YOU GOT IT!" ELSE
    3DUP           ( n lo hi n lo hi )
    1 + WITHIN IF ." BETWEEN" ELSE ." NOT BETWEEN"
    THEN 2DROP     ( n )
    THEN ;

: TEST-TRAP ( num lo hi -- num )
    ROT DUP ." num=" . -ROT 2DUP SWAP ." lo=" . ." hi=" . TRAP CR ;

391
1 1000 TEST-TRAP
330 660 TEST-TRAP
440 550 TEST-TRAP
330 440 TEST-TRAP
330 391 TEST-TRAP
391 440 TEST-TRAP
391 391 TEST-TRAP
