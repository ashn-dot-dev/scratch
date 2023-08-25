(
Define a word called GIFT which, when executed, will type
out the name of some gift. For example, you might try:

       : GIFT ." BOOKENDS " ;

Now define a word called GIVER which will print out a
person's first name. Finally, define a word called THANKS
which includes the new FORTH words GIFT and GIVER, and
prints out a message something like this:

        DEAR STEPHANIE,
        THANKS FOR THE BOOKENDS. ok
)

: GIFT ." CHOCOLATE COOKIES" ;
: GIVER ." STEPHANIE" ;
: THANKS  ." DEAR " GIVER ." , " CR ." THANKS FOR THE " GIFT ." ." CR ;
THANKS

( ---------------------------------------------------------------------------- )

(
Define a word called TEN.LESS which takes a number on the
stack, subtracts teP,r and returns the answer on the stack.
{Hint: you can use +.}
)

: TEN.LESS ( n -- n-10 ) 10 - ;
0 TEN.LESS . CR
10 TEN.LESS . CR
-1 TEN.LESS . CR
1 TEN.LESS . CR

( ---------------------------------------------------------------------------- )

(
After entering the words in Prob. 1, enter a new definition
for GIVER to print someone else's name, then execute THANKS
again. Can you explain why THANKS still prints out the first
giver's name?
)

: GIVER ." JOHN" ;
THANKS

(
THANKS was compiled with the existing GIVER, and the lookup of the GIVER
word is executed at compile time and not run time.
)
