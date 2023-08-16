Solutions to [LeetCode](https://leetcode.com/) problems with a focus on runtime
performance over memory use. Recorded times are usually taken from the best run
for a particular solution.

## Notes and Observations
I tried LeetCode for the first time on the evening of 2023-08-15. My opinion of
LeetCode had been somewhat negative, as I had mostly associated the site with
the competitive programming grinds that young software developers would subject
themselves to in order to prepare for FAANG interviews. I am not a fan of the
adversarial relationship that this interview style creates, and the way that
these types of interviews disadvantage candidates who do not have the free time
to commit to studying competitive programming problems. But I figured it was
not fair to pass judgment on a platform that I had never actually used, so I
created a new account and gave a smattering of problems a try.

For my introduction to LeetCode I solved a total of six problems, problem 1
"Two Sum", problem 3 "Longest Substring Without Repeating Characters", problem
4 "Median of Two Sorted Arrays", problem 9 "Palindrome Number", problem 36
"Valid Sudoku", and problem 49 "Group Anagrams". These were all problems that I
had never completed before, and I chose to solve them all in C++20. Of the
problems I solved, the easiest for me was "Palindrome Number" and the most
difficult was "Longest Substring Without Repeating Characters". While solving
the longest substring problem, I *did* figure out how to use the sliding window
technique, but implement it efficiently without using `std::map` took me an
additional hour after my initial solve. It was like 11:00 PM at the time, so my
tiredness was likely a contributing factor, but an optimized solution still
took longer than anticipated.

Since I was solving these problems recreationally, I decided to optimize for
runtime performance, similar to how I would always optimize for lower cycle
counts in TIS-100. It was actually really fun solving a problem the beautiful
way, and then sliding towards the ugly end the language to implement more speed
hacks. Optimizations such as replacing `std::optional<T>` with `T` and a
sentinel value, using integers and `std::array` for small sets and maps over
`std::[unordered_]set` and `std::[unordered_]map`, and reducing redundant work
by performing multiple operations in a single loop rather than using multiple
loops with separate passes, was all super fun.

However, I have to say that I am somewhat disappointed by the metrics reported
by LeetCode, and have come to the conclusion that the reported runtime metrics
are unreliable. During run submissions I noticed that the runtime of a solution
could be wildly different from run to run, even with the exact same code. I
would expect that the performance *would* differ from machine to machine and
from submission to submission due to hardware differences, but I was hoping
that this variance would be accounted for and normalized in the reported
metrics. Unfortunately this does not seem to be the case. For instance, my
optimized solution for problem 3 reported a runtime of 0 ms (beating 100% of
submissions) on multiple occasions. But that same solution reported a runtime
of 3 ms, 6 ms, and 9 ms (beating 97.83%, 90.55%, and 83.46% of submissions,
respectively) on other occasions. Testing whether changes to my solution were
more efficient was difficult, because there was no way to know whether runtime
performance differences were do to code changes or run variance.

I ran a test to check how bad this variance really was by solving a super easy
problem (problem 9 "Palindrome Number") on the morning of 2023-08-16, and
running the same solution ten times in a row within the span of about a minute.
These runs produced the following results:

```
Status   Language Runtime Memory
Accepted C++      15 ms   5.9 MB
Accepted C++      19 ms   6.1 MB
Accepted C++       3 ms   6 MB
Accepted C++       7 ms   5.9 MB
Accepted C++      12 ms   5.9 MB
Accepted C++      10 ms   6 MB
Accepted C++       7 ms   6 MB
Accepted C++      12 ms   5.9 MB
Accepted C++      18 ms   6 MB
Accepted C++      14 ms   5.9 MB
```

Stats for the 19 ms run reported that the runtime beat 31.6% of submissions,
while the 3ms run reported that the runtime beat 97.18% of submissions. Again,
this was the **same code** submitted for each run. Somewhat disappointing to
see as someone who cares about optimizing for runtime performance and who
enjoys competing on performance numbers.

Okay so additional miscellaneous notes... The site is an absolute clusterfuck
to navigate. Compared to a site like ProjectEuler.net, LeetCode feels cramped
and full of extraneous crap. Maybe I would care more about all the extra bells
and whistles if I was grinding problems out every day, but right now I really
wish there was just a single page with all problems in a list sorted by their
problem number and nothing else. The problems themselves were enjoyable, and
the wording of the questions was clear, but the difficulty seemed off.
Difficulty will be different for each person, but I fail to see any world where
"Median of Two Sorted Arrays" is considered harder in difficulty than "Longest
Substring Without Repeating Characters". I don't like how the C++ solutions are
always a public function in a `Solution` class. All of the problems I solved
were done as free functions, so I don't know why the `Solution` class was
necessary. I would usually solve the problem with a free function and then have
the `Solution` class' member function forward to my free function. Obviously
LeetCode has to restrict allowed languages to what they can actually run, but
having to use a language like C++ instead of Sunder like I can do with Project
Euler or Advent of Code is less fun for me personally.

Overall my impressions of LeetCode are about as mid as you can get. I enjoyed
the problems that I solved, but the construction of the site and the lackluster
runtime metric reporting left a bit of a sour taste in my mouth. In the future,
I might return to solve more problems for funzies, but right now I do not see
myself investing a ton of time into the site when other programming challenges
like Advent of Code and Project Euler exist.
