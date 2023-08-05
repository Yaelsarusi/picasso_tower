from enum import Enum, IntEnum
from typing import List, Optional
from dataclasses import dataclass
import math

class Floor(IntEnum):
    First = 1
    Second = 2
    Third = 3
    Fourth = 4
    Fifth = 5


class Color(Enum):
    Red = 'Red'
    Green = 'Green'
    Blue = 'Blue'
    Yellow = 'Yellow'
    Orange = 'Orange'


class Animal(Enum):
    Frog = 'Frog'
    Rabbit = 'Rabbit'
    Grasshopper = 'Grasshopper'
    Bird = 'Bird'
    Chicken = 'Chicken'


class AttributeType(Enum):
    Floor = 'Floor'
    Color = 'Color'
    Animal = 'Animal'

@dataclass
class FloorAssignment:
    floor: Floor
    color: Optional[Color]
    animal: Optional[Animal]

    def __contains__(self, value):
        return value == self.floor or value == self.color or self.animal == value

class Hint(object): 
    """Base class for all the hint classes"""

    def check_if_satisfied(self, floor_assignments):
        """ Hello documentaion """
        ...

    def get_possible_floor_assignments(self, empty_floors, all_animal_options, all_color_options, floor_assignments):
        """
        """
        ...

class RelativeHint(Hint):
    """
    Represents a hint of a relation between two floor
    that are of a certain distance of each other.
    Examples:
    The red floor is above the blue floor:
        RelativeHint(Color.Red, Color.Blue, 1)
    The frog lives three floor below the yellow floor:
        RelativeHint(Animal.Frog, Color.Yellow, -3)
    The third floor is two floors below the fifth floor:
        RelativeHint(Floor.Third, Floor.Fifth, -2)
    """
    def __init__(self, attr1, attr2, difference): # Reminder: Don't change the initializer signature
        self._attr1 = attr1
        self._attr2 = attr2
        self._difference = difference

    
    def check_if_satisfied(self, floor_assignments):
        floor_assignment_with_attr1 = list(filter(lambda x: self._attr1 in x, floor_assignments))
        floor_assignment_with_attr2 = list(filter(lambda x: self._attr2 in x, floor_assignments))

        if len(floor_assignment_with_attr1) == 1 and len(floor_assignment_with_attr2) == 1:
            # both attributes were assigned to floors,
            # check if difference is correct
            new_floor = floor_assignment_with_attr2[0].floor.value + self._difference
            if new_floor < 6 and new_floor > 0:
                return Floor(new_floor) in floor_assignment_with_attr1[0]

        return False
    
    def get_possible_floor_assignments(self, empty_floors, all_animal_options, all_color_options, floor_assignments):
        animal_options = all_animal_options
        color_options = all_color_options
        floor_options = empty_floors

        if isinstance(self._attr1, Floor):
            if self._attr1 in empty_floors:
                floor_options = [self._attr1]
            elif self._attr2 in empty_floors:
                floor_assignment_with_attr1 = list(filter(lambda x: self._attr1 in x, floor_assignments))
                new_floor = floor_assignment_with_attr1[0].floor.value - self._difference
                if new_floor < 6 and new_floor > 0:
                    return [(None, [AbsoluteHint(Floor(new_floor), self._attr2 )])]
                return []
            else:
                return []
        
        if isinstance(self._attr1, Animal):
            if self._attr1 in all_animal_options:
                animal_options = [self._attr1]
            elif self._attr2 in all_animal_options:
                floor_assignment_with_attr1 = list(filter(lambda x: self._attr1 in x, floor_assignments))
                new_floor = floor_assignment_with_attr1[0].floor.value - self._difference
                if new_floor < 6 and new_floor > 0:
                    return [(None, [AbsoluteHint(Floor(new_floor), self._attr2 )])]
                return []
            else:
                return []
        
        if isinstance(self._attr1, Color):
            if self._attr1 in all_color_options:
                color_options = [self._attr1]
            elif self._attr2 in all_color_options:
                floor_assignment_with_attr1 = list(filter(lambda x: self._attr1 in x, floor_assignments))
                new_floor = floor_assignment_with_attr1[0].floor.value - self._difference
                if new_floor < 6 and new_floor > 0:
                    return [(None, [AbsoluteHint(Floor(new_floor), self._attr2 )])]
                return []
            else:
                return []
            
        possible_options = []
        for floor in floor_options:
            for animal in animal_options:
                for color in color_options:
                    new_floor = floor.value + self._difference
                    
                    # out of bounds, is not a possibility
                    if new_floor > 5 or new_floor < 1:
                        continue

                    new_hint_to_satisfy = AbsoluteHint(Floor(new_floor), self._attr2)
                    
                    # return it as a possibility, but return the new hint as well:
                    possible_options.append((FloorAssignment(floor=floor, color=color, animal=animal), [new_hint_to_satisfy]))
                        

        return possible_options

class AbsoluteHint(Hint):
    """
    Represents a hint on a specific floor. Examples:
    The third floor is red:
        AbsoluteHint(Floor.Third, Color.Red)
    The frog lives on the fifth floor:
        AbsoluteHint(Animal.Frog, Floor.Fifth)
    The orange floor is the floor where the chicken lives:
        AbsoluteHint(Color.Orange, Animal.Chicken)
    """
    def __init__(self, attr1, attr2): # Reminder: Don't change the initializer signature
        self._attr1 = attr1
        self._attr2 = attr2

    def check_if_satisfied(self, floor_assignments):
        for floor_assignments in floor_assignments:
            if self._attr1 in floor_assignments and self._attr2 in floor_assignments:
                return True
        return False

    def get_possible_floor_assignments(self, empty_floors, animal_options, color_options, floor_assignments):
        if isinstance(self._attr1, Floor):
            if self._attr1 in empty_floors:
                empty_floors = [self._attr1]
            else:
                return []
        
        if isinstance(self._attr1, Animal):
            if self._attr1 in animal_options:
                animal_options = [self._attr1]
            else:
                return []
        
        if isinstance(self._attr1, Color):
            if self._attr1 in color_options:
                color_options = [self._attr1]
            else:
                return []
            
        if isinstance(self._attr2, Floor):
            if self._attr2 in empty_floors:
                empty_floors = [self._attr2]
            else:
                return []
        
        if isinstance(self._attr2, Animal):
            if self._attr2 in animal_options:
                animal_options = [self._attr2]
            else:
                return []
        
        if isinstance(self._attr2, Color):
            if self._attr2 in color_options:
                color_options = [self._attr2]
            else:
                return []

        possible_options = []
        for floor in empty_floors:
            for animal in animal_options:
                for color in color_options:
                    possible_options.append((FloorAssignment(floor=floor, color=color, animal=animal), []))
        return possible_options

class NeighborHint(Hint):
    """
    Represents a hint of a relation between two floors that are adjacent
    (first either above or below the second).
    Examples:
    The green floor is neighboring the floor where the chicken lives:
        NeighborHint(Color.Green, Animal.Chicken)
    The grasshopper is a neighbor of the rabbit:
        NeighborHint(Animal.Grasshopper, Animal.Rabbit)
    The yellow floor is neighboring the third floor:
        NeighborHint(Color.Yellow, Floor.Third)
    """
    def __init__(self, attr1, attr2): # Reminder: Don't change the initializer signature
        self._attr1 = attr1
        self._attr2 = attr2
        self.relative_hints = [RelativeHint(attr1, attr2, 1),  RelativeHint(attr2, attr1, 1)]

    def check_if_satisfied(self, floor_assignments):
        for relative_hint in self.relative_hints:
            if relative_hint.check_if_satisfied(floor_assignments=floor_assignments):
                return True
        return False

    def get_possible_floor_assignments(self, empty_floors, animal_options, color_options, floor_assignments):
        return self.relative_hints[0].get_possible_floor_assignments(empty_floors, animal_options, color_options, floor_assignments) + self.relative_hints[0].get_possible_floor_assignments( empty_floors, animal_options, color_options, floor_assignments)

def remove_value(lst, value):
    return list(filter(lambda x: x != value, lst))

def backtrack(hints, floor_assignments, empty_floors, animal_options, color_options) -> int:
    if len(hints) == 0:
        return math.factorial(len(animal_options))*math.factorial(len(color_options))
    
    possible_options = 0
    possible_floor_assignment = hints[0].get_possible_floor_assignments(empty_floors, animal_options, color_options, floor_assignments)

    if len(possible_floor_assignment) == 0:
        # Check if hint was already satisfied
        if hints[0].check_if_satisfied(floor_assignments):
            return backtrack(hints=hints[1:], 
                                      floor_assignments = list(floor_assignments),
                                      empty_floors=list(empty_floors),
                                      animal_options=list(animal_options),
                                      color_options=list(color_options))

    for floor_assigmment, additional_hints in possible_floor_assignment:
        
        # TODO - FIX function "remove_value" so it will be generic for both cases
        if floor_assigmment is None:
            possible_options += backtrack(hints=hints[1:] + additional_hints, 
                                      floor_assignments = list(floor_assignments),
                                      empty_floors=list(empty_floors),
                                      animal_options=list(animal_options),
                                      color_options=list(color_options))
        else:
            possible_options += backtrack(hints=hints[1:] + additional_hints, 
                                        floor_assignments = list(floor_assignments) + [floor_assigmment],
                                        empty_floors=remove_value(empty_floors, floor_assigmment.floor),
                                        animal_options=remove_value(animal_options, floor_assigmment.animal),
                                        color_options=remove_value(color_options, floor_assigmment.color))

    return possible_options 

def count_assignments(hints: List[Hint]): # Reminder: Don't change the function signature
    """
    Given a list of Hint objects, return the number of
    valid assignments that satisfy these hints.
    """

    # Call the backtrack function to find all valid assignments
    empty_floors = [Floor.First, Floor.Second, Floor.Third, Floor.Fourth, Floor.Fifth]
    animal_options = [Animal.Bird, Animal.Chicken, Animal.Frog, Animal.Grasshopper, Animal.Rabbit]
    color_options = [Color.Blue, Color.Green, Color.Orange, Color.Red, Color.Yellow]

    return backtrack(hints=hints, floor_assignments=[], empty_floors=empty_floors, animal_options=animal_options, color_options=color_options)


HINTS_EX1 = [
    AbsoluteHint(Animal.Rabbit, Floor.First),
    AbsoluteHint(Animal.Chicken, Floor.Second),
    AbsoluteHint(Floor.Third, Color.Red),
    AbsoluteHint(Animal.Bird, Floor.Fifth),
    AbsoluteHint(Animal.Grasshopper, Color.Orange),
    NeighborHint(Color.Yellow, Color.Green),
]

HINTS_EX2 = [
    AbsoluteHint(Animal.Bird, Floor.Fifth),
    AbsoluteHint(Floor.First, Color.Green),
    AbsoluteHint(Animal.Frog, Color.Yellow),
    NeighborHint(Animal.Frog, Animal.Grasshopper),
    NeighborHint(Color.Red, Color.Orange),
    RelativeHint(Animal.Chicken, Color.Blue, -4)
]

HINTS_EX3 = [
    RelativeHint(Animal.Rabbit, Color.Green, -2)
]

HINTS_EX4 = [
    # Final assignment should be:
    # Floor |   Animal    | color
    #   5   | Grasshopper | Green
    #   4   |    Frog     | Yellow
    #   3   |    Bird     | Red
    #   2   |   Chicken   | Blue
    #   1   |   Rabbit    | Orange

    # Checks simple Absolute hints, when list of hints is large
    AbsoluteHint(Animal.Rabbit, Floor.First),
    AbsoluteHint(Animal.Chicken, Floor.Second),
    AbsoluteHint(Floor.Third, Animal.Bird),
    AbsoluteHint(Floor.Fourth, Animal.Frog),
    AbsoluteHint(Floor.Fifth, Animal.Grasshopper),
    AbsoluteHint(Floor.Fifth, Color.Green),
    AbsoluteHint(Animal.Chicken, Color.Blue),
    AbsoluteHint(Animal.Rabbit, Color.Orange),
    AbsoluteHint(Floor.Third, Color.Red),
    AbsoluteHint(Floor.Fourth, Color.Yellow),
]

HINTS_EX5 = [
    AbsoluteHint(Animal.Rabbit, Floor.First),
]

HINTS_EX6 = [
    # Tests contradicting hint assignments
    AbsoluteHint(Animal.Rabbit, Floor.First),
    AbsoluteHint(Animal.Bird, Floor.First),
]

HINTS_EX7 = [
    # Relative hints with distance 0 should be like absolute hints
    RelativeHint(Animal.Rabbit, Floor.First, 0),
    RelativeHint(Animal.Chicken, Floor.Second, 0),
    RelativeHint(Floor.Third, Animal.Bird, 0),
    RelativeHint(Floor.Fourth, Animal.Frog, 0),
    RelativeHint(Floor.Fifth, Animal.Grasshopper, 0),
    RelativeHint(Floor.Fifth, Color.Green, 0),
    RelativeHint(Animal.Chicken, Color.Blue, 0),
    RelativeHint(Animal.Rabbit, Color.Orange, 0),
    RelativeHint(Floor.Third, Color.Red, 0),
    RelativeHint(Floor.Fourth, Color.Yellow, 0),
]

HINTS_EX8 = [
    # Relative hints with distance 0 should be like absolute hints
    RelativeHint(Animal.Rabbit, Floor.First, 0),
]

HINTS_EX9 = [
    NeighborHint(Animal.Rabbit, Color.Green)
]

def test():
    # Checks Absolute hints only
    assert(count_assignments([]) ==  math.factorial(5)*math.factorial(5)), f'Failed on example #4. got {count_assignments([])} expected 14400'
    assert(count_assignments(HINTS_EX5) == math.factorial(5)*math.factorial(4)), f'Failed on example #5. got {count_assignments(HINTS_EX5)} expected 2880'
    assert(count_assignments(HINTS_EX6) == 0), f'Failed on example #6. got {count_assignments(HINTS_EX6)} expected 0'
    
    # Checks when there are redundent hints
    assert(count_assignments(HINTS_EX4) == 1), f'Failed on example #4. got {count_assignments(HINTS_EX4)} expected 1'
    
    # Checks Relative hints
    assert(count_assignments(HINTS_EX3) == 1728), 'Failed on example #3'
    assert(count_assignments(HINTS_EX7) == 1), f'Failed on example #7. got {count_assignments(HINTS_EX7)} expected 1'
    assert(count_assignments(HINTS_EX8) == math.factorial(5)*math.factorial(4)), f'Failed on example #8. got {count_assignments(HINTS_EX8)} expected 2880'

    # Check Neighbor hints
    assert(count_assignments(HINTS_EX9) == 8*1728/3)

    assert count_assignments(HINTS_EX1) == 2, 'Failed on example #1'
    
    assert count_assignments(HINTS_EX2) == 4, 'Failed on example #2'

    
    
    print('Success!')


if __name__ == '__main__':
    test()

# def is_valid_picasso_tower(tower_assignment: List[FloorAssignment], hints: List[Hint]):
#     # Define your rule here
#     for hint in hints:
#         if not hint.valid_tower_assignment(tower_assignment):
#             return False
#     return True

# def backtrack(cur_floor: int, picasso_tower: List[FloorAssignment], animal_options: List[Animal], color_options: List[Color], hints: List[Hint]):
#     is_valid = is_valid_picasso_tower(picasso_tower, hints)
#     if not is_valid:
#         picasso_tower[cur_floor].animal = None
#         picasso_tower[cur_floor].color = None
#         return 0
#     # We've assigned all animals and colors, and at this point the tower is full and valid
#     if len(animal_options) == 0 and len(color_options) == 0:
#         return 1
#     assignment_count = 0
#     for idx, cur_animal in enumerate(animal_options):
#         for idx, cur_color in enumerate(color_options):
#             picasso_tower[cur_floor].animal = cur_animal
#             picasso_tower[cur_floor].color = cur_color
#             assignment_count += backtrack(cur_floor + 1, 
#                                         picasso_tower, 
#                                         animal_options[0:idx] + animal_options[idx+1:], 
#                                         color_options[0:idx] + color_options[idx +1:], 
#                                         hints)
#     return assignment_count


# def get_starting_assigment() -> List[FloorAssignment]:
#     floors_assignments = []
#     for i in range(1, 6):
#         floors_assignments.append(FloorAssignment(floor=Floor(i), color=None, animal=None))
#     return floors_assignments


# def count_assignments(hints: List[Hint]): # Reminder: Don't change the function signature
#     """
#     Given a list of Hint objects, return the number of
#     valid assignments that satisfy these hints.
#     TODO: Needs to be implemented
#     """
#     possible_assigment: List[FloorAssignment] = get_starting_assigment()

#     # Call the backtrack function to find all valid assignments

#     animal_options = [Animal.Bird, Animal.Chicken, Animal.Frog, Animal.Grasshopper, Animal.Rabbit]
#     color_options = [Color.Blue, Color.Green, Color.Orange, Color.Red, Color.Yellow]
    
#     return backtrack(0, possible_assigment, animal_options, color_options, hints)