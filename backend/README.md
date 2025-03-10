# Sudoku Solver Backend

Yup, here we are. Backend of this project is written in Python 3.12 with usage of FastAPI framework in standard format.

## Solving algorythm
Initially, I tried to implement solving algorythm inspired by popular sudoku solving strategies. Scanning based strategies were pretty easy to implement properly, but the real problem occured when I tried to write an effective algorythm based on board analysis methods (such as "Normal Pair", "Hidden Pair" and their multi-tile variants). I found the scanning techniques to be insufficient to solve most boards alone, so there was no way to leave just them in my project.

Then I tried to solve sudokus using the A* algorythm, even though such problems as solving a sudoku board are not its main purpose. This strategy turned out to be lacking in terms of performance, as it took lots of time and quite some memory to solve boards this way.

Then, I realised. You can't make infinite moves on a sudoku board. Worst case scenario, one would make 9^81 moves, which is a super fat upper approximation in case of an empty board$^1$. Yeah, that's a lot, but let's be honest, most cases one wouldn't even do half as much moves. Either way, it means that the series of moves are... endful? Certainly not endless. So, I implemented a backtracking algorythm with some alpha culling and MRV (Minimum Remaining Values) heuristic, not worrying about possible endless loops.

---

$^1$Empty board is an instance of a nondeterministic sudoku board. It means, that there's more than one solution to such board. For a sudoku board to be considered deterministic (meaning it has only one solution), it has to have no less than 17 tiles filled. Even then, the board is most likely nondeterministic, but there are no deterministic boards with 16 or less filled tiles. Well, there are even some nondeterministic boards with 79 filled tiles (out of 81). 

