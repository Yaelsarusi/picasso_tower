from enum import Enum, IntEnum
from typing import List, Optional, Tuple, Union
from dataclasses import dataclass
import math

class Floor(IntEnum):
    First = 1
    Second = 2
    Third = 3
    Fourth = 4
    Fifth = 5

MIN_FLOOR = min(floor.value for floor in Floor)
MAX_FLOOR = max(floor.value for floor in Floor)

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
    color: Color
    animal: Animal

    def __contains__(self, value: Union[Floor, Color, Animal]):
        return value == self.floor or value == self.color or self.animal == value

class Hint(object): 
    """Base class for all the hint classes"""

    def check_if_satisfied(self, floor_assignments: List[FloorAssignment]) -> bool:
        """ Checks if the hint is satisfied in the given floor assignments. """
        ...

    def get_possible_floor_assignments(self, 
                                       empty_floors: List[Floor], 
                                       all_animal_options: List[Animal], 
                                       all_color_options: List[Color], 
                                       floor_assignments: List[FloorAssignment]) -> List[Tuple[Optional[FloorAssignment], Optional['Hint']]]:
        """
        Returns a list of all posssible tuples, of floor assignments and additional hints.
        The combination of both will satisfy the original hint to completion.
        """
        ...


def find_floor_assignment_by_attribute(attribute: Union[Floor, Color, Animal], floor_assignments: List[FloorAssignment]) -> Optional[FloorAssignment]:
    floor_assignment_with_attribute = list(filter(lambda x: attribute in x, floor_assignments))
    if len(floor_assignment_with_attribute) == 1:
        return floor_assignment_with_attribute[0]
    return None

def remove_value(lst, value):
    return list(filter(lambda x: x != value, lst))

@dataclass
class GetOptionsIfValidReturnType:
    is_valid: bool
    new_options: List[Union[Color, Animal, Floor]]
    floor_assignment: Union[List[Color], List[Animal], List[Floor]]

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
    def __init__(self, 
                 attr1: Union[Floor, Color, Animal], 
                 attr2: Union[Floor, Color, Animal],
                 difference: int): # Reminder: Don't change the initializer signature
        self._attr1 = attr1
        self._attr2 = attr2
        self._difference = difference
    
    def check_if_satisfied(self, floor_assignments: List[FloorAssignment]):
        """
        Checks if the hint is satisfied in the given floor assignments. 
        A Relative hint is satisfied if in the given floor assignment lists, exists 2 floor assignments that satisfy:
        * Both have one of the respective hint attributes.
        * Their floor distance is the hint given difference.
        """
        floor_assignment_with_attr1 = find_floor_assignment_by_attribute(self._attr1, floor_assignments)
        floor_assignment_with_attr2 = find_floor_assignment_by_attribute(self._attr2, floor_assignments)

        # Checks if both attributes were assigned to floors
        if floor_assignment_with_attr1 is not None and floor_assignment_with_attr2 is not None:
            new_floor = floor_assignment_with_attr2.floor.value + self._difference
            # check if floor difference is correct
            if new_floor <= MAX_FLOOR and new_floor >= MIN_FLOOR:
                return Floor(new_floor) in floor_assignment_with_attr1

        return False
    
    def get_options_if_valid(self, options: Union[List[Color], List[Animal], List[Floor]], floor_assignments: List[FloorAssignment]) -> GetOptionsIfValidReturnType:
        if self._attr1 in options:
            return GetOptionsIfValidReturnType(True, [self._attr1], [])
        elif self._attr2 in options:
            floor_assignment_with_attr1 = find_floor_assignment_by_attribute(self._attr1, floor_assignments)

            new_floor = floor_assignment_with_attr1.floor.value - self._difference
            if new_floor <= MAX_FLOOR and new_floor >= MIN_FLOOR:
                return GetOptionsIfValidReturnType(False, [], [(None, [AbsoluteHint(Floor(new_floor), self._attr2 )])])
            return GetOptionsIfValidReturnType(False, [], [])
        else:
            return GetOptionsIfValidReturnType(False, [], [])
    
    def get_possible_floor_assignments(self, 
                                       empty_floors: List[Floor], 
                                       all_animal_options: List[Animal], 
                                       all_color_options: List[Color], 
                                       floor_assignments: List[FloorAssignment]) -> List[Tuple[Optional[FloorAssignment], Optional['Hint']]]:
        """
        A possible floor assignment of a relative hint:
        1) A floor assignment to satisfy the first attribute of the hint if it's not already in the floor assignments given.
        2) An Absolute hint that links between the existing (or new) floor assignment that thas the first attribute, and a future floor assignmnet of the second attribute.
        """

        animal_options = all_animal_options
        color_options = all_color_options
        floor_options = empty_floors

        if isinstance(self._attr1, Animal):
            get_options_if_valid = self.get_options_if_valid(all_animal_options, floor_assignments)
            if not get_options_if_valid.is_valid:
                return get_options_if_valid.floor_assignment
            else:
                animal_options = get_options_if_valid.new_options

        if isinstance(self._attr1, Floor):
            get_options_if_valid = self.get_options_if_valid(empty_floors, floor_assignments)
            if not get_options_if_valid.is_valid:
                return get_options_if_valid.floor_assignment
            else:
                floor_options = get_options_if_valid.new_options
        
        if isinstance(self._attr1, Color):
            get_options_if_valid = self.get_options_if_valid(all_color_options, floor_assignments)
            if not get_options_if_valid.is_valid:
                return get_options_if_valid.floor_assignment
            else:
                color_options = get_options_if_valid.new_options
            
        possible_options = []
        for floor in floor_options:
            for animal in animal_options:
                for color in color_options:
                    new_floor = floor.value + self._difference
                    
                    # out of bounds, is not a possibility
                    if new_floor > MAX_FLOOR or new_floor < MIN_FLOOR:
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
    def __init__(self, attr1: Union[Floor, Color, Animal], attr2: Union[Floor, Color, Animal]): # Reminder: Don't change the initializer signature
        self._attr1 = attr1
        self._attr2 = attr2

    def check_if_satisfied(self, floor_assignments: List[FloorAssignment]) -> bool:
        """
        Checks if the hint is satisfied in the given floor assignments. 
        Absolute hint will be sattisfied if we can find a floor assignment that has both of the hint's attributes.
        """
        for floor_assignments in floor_assignments:
            if self._attr1 in floor_assignments and self._attr2 in floor_assignments:
                return True
        return False

    def get_possible_floor_assignments(self, 
                                       empty_floors: List[Floor], 
                                       all_animal_options: List[Animal], 
                                       all_color_options: List[Color], 
                                       floor_assignments: List[FloorAssignment]) -> List[Tuple[Optional[FloorAssignment], Optional['Hint']]]:
        """
        Returns a list of all posssible tuples, of floor assignments and additional hints.
        The combination of both will satisfy the original hint to completion.
        In Absolute hints, no additional hint will be provided (will always be None).
        """
        animal_options = all_animal_options
        color_options = all_color_options
        floor_options = empty_floors

        if isinstance(self._attr1, Floor):
            if self._attr1 in empty_floors:
                floor_options = [self._attr1]
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
                floor_options = [self._attr2]
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
        for floor in floor_options:
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
    def __init__(self, attr1: Union[Floor, Color, Animal], attr2: Union[Floor, Color, Animal]): # Reminder: Don't change the initializer signature
        self._attr1 = attr1
        self._attr2 = attr2
        # A NeighborHint is a directionless relative hint with distance 1. 
        self.relative_hints = [RelativeHint(attr1, attr2, 1),  RelativeHint(attr2, attr1, 1)]

    def check_if_satisfied(self, floor_assignments: List[FloorAssignment]) -> bool:
        """
        Checks if the hint is satisfied in the given floor assignments. 
        A Neighbor hint a a directitonless relative hint.
        It will be satisfied if one of the relaive hints are satisfied.
        """
        for relative_hint in self.relative_hints:
            if relative_hint.check_if_satisfied(floor_assignments=floor_assignments):
                return True
        return False

    def get_possible_floor_assignments(self, 
                                       empty_floors: List[Floor], 
                                       all_animal_options: List[Animal], 
                                       all_color_options: List[Color], 
                                       floor_assignments: List[FloorAssignment]) -> List[Tuple[Optional[FloorAssignment], Optional['Hint']]]:
        """
        Returns a list of all posssible tuples, of floor assignments and additional hints.
        The combination of both will satisfy the original hint to completion.
        A NeighborHint is a direcctionless Relative hint.
        Return all possible floor assignments of both directional hints that are neighborhint.
        """
        return self.relative_hints[0].get_possible_floor_assignments(empty_floors, 
                                                                     all_animal_options, 
                                                                     all_color_options, 
                                                                     floor_assignments) \
                + self.relative_hints[0].get_possible_floor_assignments(empty_floors, 
                                                                        all_animal_options, 
                                                                        all_color_options, 
                                                                        floor_assignments)

def backtrack(hints: List[Hint], 
              floor_assignments: List[FloorAssignment], 
              empty_floors: List[Floor], 
              animal_options: List[Animal],
              color_options: List[Color]) -> int:
    """
    Counts all possible floor assignments that satisfy the list of hints, available floors, available colors and available animals given.
    """

    if len(hints) == 0:
        return math.factorial(len(animal_options))*math.factorial(len(color_options))
    
    possible_options = 0

    cur_hint = hints[0]
    possible_floor_assignment = cur_hint.get_possible_floor_assignments(empty_floors, animal_options, color_options, floor_assignments)

    if len(possible_floor_assignment) == 0:
        # Check if hint was already satisfied. If so, skip current hint.
        if cur_hint.check_if_satisfied(floor_assignments):
            return backtrack(hints=hints[1:], 
                                      floor_assignments = list(floor_assignments),
                                      empty_floors=list(empty_floors),
                                      animal_options=list(animal_options),
                                      color_options=list(color_options))

    for floor_assigmment, additional_hints in possible_floor_assignment:
        
        if floor_assigmment is None:
            # Hint attibute was already assigned in a previous floor, however additional hint was needed.``
            possible_options += backtrack(hints=hints[1:] + additional_hints, 
                                      floor_assignments = list(floor_assignments),
                                      empty_floors=list(empty_floors),
                                      animal_options=list(animal_options),
                                      color_options=list(color_options))
        else:
            # With the new floor assignment, cur hint is satisfied. Remove used attributes from available options, and continue to next hint.
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

    empty_floors = [Floor.First, Floor.Second, Floor.Third, Floor.Fourth, Floor.Fifth]
    animal_options = [Animal.Bird, Animal.Chicken, Animal.Frog, Animal.Grasshopper, Animal.Rabbit]
    color_options = [Color.Blue, Color.Green, Color.Orange, Color.Red, Color.Yellow]
    floor_assignments = []

    # Call the backtrack function to find all valid assignments
    return backtrack(hints=hints,
                     floor_assignments=floor_assignments, 
                     empty_floors=empty_floors, 
                     animal_options=animal_options, 
                     color_options=color_options)


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
