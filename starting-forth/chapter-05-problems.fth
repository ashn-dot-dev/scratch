\ Translate the following algebraic expression into a Forth definition:
\
\     -ab/c
\
\ given ( a b c -- )

: EXPR1 ( a b c -- answer )
    */ NEGATE ;

: TEST-EXPR1 ( a b c -- )
    .S EXPR1 . CR ;

1 1 1 TEST-EXPR1
2 1 1 TEST-EXPR1
1 2 1 TEST-EXPR1
3 5 2 TEST-EXPR1
-3 -5 2 TEST-EXPR1
3 5 -2 TEST-EXPR1

CR ( ------------------------------------------------------------------------- )

\ Given these four numbers on the stack:
\
\     ( 6 70 123 45 -- )
\
\ write an expression that prints the largest value.

: EXPR2 ( a b c d -- )
    MAX MAX MAX . ;

: TEST-EXPR2 ( a b c d -- )
    .S EXPR2 CR ;

1 2 3 4 TEST-EXPR2
4 3 2 1 TEST-EXPR2
1 2 3 -4 TEST-EXPR2
-4 3 2 1 TEST-EXPR2
-1 -2 -3 -4 TEST-EXPR2
-4 -3 -2 -1 TEST-EXPR2

CR ( ------------------------------------------------------------------------- )

( Combining problems 3 and 4. )

\ In “calculator style,” convert the following temperatures, using these
\ formulas:
\
\ °C = (°F - 32) / 1.8
\ °F = (°C x 1.8) + 32
\ °K = °C + 273
\
\ (For now, express all arguments and results in whole degrees.)
\ 0° F in Celsius
\ 212° F in Celsius
\ -32° F in Celsius
\ 16° C in Fahrenheit
\ 233° K in Celsius

\ Now define words to perform the conversions in Prob. 3. Use the following
\ names:
\
\ F>C  F>K  C>F  C>K  K>F  K>C
\
\ Test them with the above values.

: F>C ( deg-f -- deg-c )
    32 - 10 18 */ ;

0 F>C . CR
212 F>C . CR
-32 F>C . CR

: C>F ( deg-c -- deg-f )
    18 * 320 + 10 / ;

16 C>F . CR

: K>C ( deg-k -- deg-c )
    273 - ;

233 K>C . CR
