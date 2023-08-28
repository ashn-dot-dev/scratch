( What’s the difference between DUP DUP and 2DUP? )

( 3 cells ont the stack)
10 DUP DUP .S
DROP DROP DROP

( 2 double cells on the stack)
20 30 2DUP .S
2DROP 2DROP

CR ( ------------------------------------------------------------------------- )

(
Write a phrase which will reverse the order of the top four items on the
stack; that is, { 1 2 3 4 -- 4 3 2 1 }
)

: 4REVERSE SWAP 2SWAP SWAP ;

1 2 3 4 .S 4REVERSE .S
DROP DROP DROP DROP

CR ( ------------------------------------------------------------------------- )

(
Write a definition called 3DUP which will duplicate the top three
numbers on the stack; for example,

    { 1 2 3 -- 1 2 3 1 2 3 }
)

: 3DUP ( 1 2 3 -- 1 2 3 1 2 3)
    DUP 2OVER ROT ;

1 2 3 .S 3DUP .S
DROP DROP DROP
DROP DROP DROP

CR ( ------------------------------------------------------------------------- )

(
Write definitions for the following infix equations, given the stack
effects shown:

    a**2 + ab + c   { c a b -- result }
    {a-b}/{a+b}  { a b -- result }
)

( a*a + a*b + c)
: EXPR1 ( c a b -- result )
    2DUP * ( a*b )
    ROT ROT DROP
    DUP *  ( a*a )
    + + ;  ( a*a + a*b + c)

( 5**2 + 5*7 + 3 => 25 + 35 + 3 => 63 )
3 5 7 .S EXPR1 . CR

( {a-b} / {a+b} )
: EXPR2 ( a b -- result )
    2DUP +    ( a + b )
    ROT ROT - ( a - b )
    SWAP / ;  ( {a-b} / {a+b} )

13 -5 .S EXPR2 . CR

CR ( ------------------------------------------------------------------------- )

(
Write a set of words to compute prison sentences for hardened criminals
such that the judge can enter:

    CONVICTED-OF ARSON HOMICIDE TAX-EVASION↵ok
    WILL-SERVE↵35 years ok

or any series of crime beginning with the word CONVICTED-OF and ending
with WILL-SERVE. Use these sentences:

    HOMICIDE 20 years
    ARSON 10 years
    BOOKMAKING 2 years
    TAX-EVASION 5 years
)

: CONVICTED-OF 0 ;
: HOMICIDE 20 + ;
: ARSON 10 + ;
: BOOKMAKING 2 + ;
: TAX-EVASION 5 + ;
: WILL-SERVE . ." years" ;
CONVICTED-OF ARSON HOMICIDE TAX-EVASION
WILL-SERVE CR

CR ( ------------------------------------------------------------------------- )

(
You’re the inventory programmer at Maria’s Egg Ranch. Define a word
called

    EGG.CARTONS

which expects on the stack the total number of eggs laid by the chickens
today and prints out the number of cartons that can be filled with a
dozen each, as well as the number of leftover eggs.
)

: EGG.CARTONS ( n -- )
    12 /MOD . ." cartons with " . ." leftover eggs" ;

0 .S EGG.CARTONS CR
1 .S EGG.CARTONS CR
12 .S EGG.CARTONS CR
13 .S EGG.CARTONS CR
26 .S EGG.CARTONS CR
