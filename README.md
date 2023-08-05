## Python Exercise
In "Picasso Tower" there are five floors. Each floor has a different color: red, green, blue, yellow
and orange. It is unknown which floor is of which color, but there's exactly one floor of each
color.
On each floor lives one animal: a frog, a rabbit, a grasshopper, a bird and a chicken. It is
unknown which animal lives on which floor.

An "assignment" defines which color is each floor, and which animal lives on each floor. There
are 14,400 possible assignments (make sure you understand why!).

Given a list of hints, your goal is to find the number of unique assignments that satisfy these
hints.

Example 1. Hints:
1. The rabbit lives on the 1st floor.
2. The chicken lives on the 2nd floor.
3. The 3rd floor is yellow.
4. The bird lives on the 5th floor.
5. The grasshopper lives on the blue floor.
6. The red floor and the green floors are neighboring floors (neighboring floors are two floors where the first is directly above or directly below the second).

For these hints, there are exactly 2 possible solutions. Let’s analyze the possible solutions:
After 4 hints -
5. Bird
4.
3. Yellow
2. Chicken
1. Rabbit

After 5 hints -
5. Bird
4. Grasshopper Blue
3. Yellow
2. Chicken
1. Rabbit

After 5 hints - fill missing animal
5. Bird
4. Grasshopper Blue
3. Frog Yellow
2. Chicken
1. Rabbit

After 6 hints -
5. Bird Orange
4. Grasshopper Blue
3. Frog Yellow
2. Chicken Red/Green
1. Rabbit Green/Red

Example 2. Hints:
1. The bird lives on the 5th floor.
2. The 1st floor is green.
3. The frog lives on the yellow floor.
4. The frog is a neighbor of the grasshopper (two animals are neighbors when they live on
neighboring floors).
5. The red and orange floors are neighboring floors.
6. The chicken lives 4 floors below the blue floor.

For these hints, there are exactly 4 possible solutions:
(1, Green, Chicken), (2, Orange, Rabbit), (3, Red, Grasshopper), (4, Yellow, Frog), (5, Blue,
Bird)
(1, Green, Chicken), (2, Red, Rabbit), (3, Orange, Grasshopper), (4, Yellow, Frog), (5, Blue,
Bird)
(1, Green, Chicken), (2, Yellow, Frog), (3, Red, Grasshopper), (3, Orange, Rabbit), (5, Blue,
Bird)
(1, Green, Chicken), (2, Yellow, Frog), (3, Orange, Grasshopper), (3, Red, Rabbit), (5, Blue,
Bird)

Example 3. A single hint:
1. The rabbit lives 2 floors below the green floor.
The number of possible solutions in this case is 1728

Attached is count_assignments.py, a Python file that contains a few base classes to get you
going.
You may make any changes to the file and the classes. You may (and are advised) to create
new additional classes and / or helper functions. The sole requirement is that the API of the
function count_assignments stays the same:
● The function's name must stay count_assignments.
● Its input is a single argument which is a list of Hint objects (instances of the sub-classes
AbsoluteHint, RelativeHint, NeighborHint).
● The API for initializing these sub-classes must also stay the same, although their
implementation may be modified.
● The returned value is an integer specifying the amount of unique valid assignments that
satisfy the input hints

General guidelines:
● Your program must be written in Python 3 (the attached code is Python 3).
● Keep in mind that there are only 14,400 possible assignments. Your solution does not
need to support a generalized version of the problem described.
● Test your code to make sure it deals with all the edge cases.
● Keep the code simple and with a Pythonic approach.
● Your code should be documented and conform to Python style guidelines.
● Your submission should only contain text files, do not submit binary files.

Good luck!