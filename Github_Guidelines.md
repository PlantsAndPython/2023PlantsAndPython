# GitHub Guidelines
For anybody new to using git/GitHub, this is a doc of tips and tricks for smooth GitHub collaboration.

## Git
Git is a tool for moving files back and forth between a remote repository and your local machine. It is similar in principle to working with an HPCC, but it serves more for storage and collaboration than computing power. Below is a link for getting started with git, and some basic commands:  
https://education.github.com/git-cheat-sheet-education.pdf

## GitHub
Some key things that make collaboration with GitHub (or any version control tools) smooth(er):
- create a new, local branch using <code>git branch</code> when working on code, particularly if you are working on the same code as someone else in the group
- `push` to the repository when you have working code
- `merge` onto the `master` branch only when you have finished with the task your branch was meant to achieve
- it is better to make small, working changes and `merge` with `master` than make large changes and `push` all at once
- *please*, for the sake of all of us, don't `merge` broken code with the `master` branch
    - this leads to really ugly `merge` conflicts, which can be a pain to resolve


