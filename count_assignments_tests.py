
from count_assignments import AbsoluteHint, Animal, Color, Floor, FloorAssignment, NeighborHint, RelativeHint, count_assignments
import math

def test_check_is_satisfied_absolute_hint():
    assert AbsoluteHint(Animal.Bird, Floor(1)).check_if_satisfied([FloorAssignment(floor=Floor(1), animal=Animal.Bird, color=Color.Blue)])
    assert AbsoluteHint(Color.Blue, Floor(2)).check_if_satisfied([FloorAssignment(floor=Floor(2), animal=Animal.Bird, color=Color.Blue)])
    assert AbsoluteHint(Animal.Bird, Color.Blue).check_if_satisfied([FloorAssignment(floor=Floor(3), animal=Animal.Bird, color=Color.Blue)])

    assert not AbsoluteHint(Color.Blue, Floor(2)).check_if_satisfied([FloorAssignment(floor=Floor(1), animal=Animal.Bird, color=Color.Blue)])
    assert not AbsoluteHint(Floor(1), Animal.Bird).check_if_satisfied([FloorAssignment(floor=Floor(3), animal=Animal.Bird, color=Color.Blue)])

def test_get_possible_floor_assignments_absolute_hint_impossible_hint():
    hint = AbsoluteHint(Animal.Bird, Floor(1))
    empty_floors = [Floor(2),Floor(3)]
    possible_animals = [Animal.Chicken, Animal.Frog]
    possible_colors = [Color.Blue, Color.Green]
    possible_floor_assignments = hint.get_possible_floor_assignments(empty_floors=empty_floors, all_animal_options=possible_animals, all_color_options=possible_colors, floor_assignments=[])
    assert len(possible_floor_assignments) == 0

def test_get_possible_floor_assignments_absolute_hint_possible_hint():
    hint = AbsoluteHint(Animal.Bird, Floor(2))
    empty_floors = [Floor(2), Floor(3)]
    possible_animals = [Animal.Bird, Animal.Frog]
    possible_colors = [Color.Blue, Color.Green]
    possible_floor_assignments = hint.get_possible_floor_assignments(empty_floors=empty_floors, all_animal_options=possible_animals, all_color_options=possible_colors, floor_assignments=[])
    assert len(possible_floor_assignments) == 2

def test_count_assignments_no_hints():
    counted_assignments = count_assignments([])
    assert counted_assignments == math.factorial(5)*math.factorial(5)

def test_count_assignments_absolute_hints_only():
    # Checks Absolute hints only
    
    one_absolute_hint = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
    ]

    two_contradicting_absolute_hints = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Bird, Floor.First),
    ]

    assert count_assignments(one_absolute_hint) == math.factorial(5)*math.factorial(4)
    assert count_assignments(two_contradicting_absolute_hints) == 0

def test_redundant_hints():
    redundant_absolute_hints = [
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

    redundant_absolute_hints2 = [
        AbsoluteHint(Floor.Fourth, Color.Yellow),
        AbsoluteHint(Color.Yellow, Floor.Fourth),
    ]
    
    redunant_relative_hints = [
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

    redunant_relative_hints2 = [
        RelativeHint(Animal.Rabbit, Floor.First, 2),
        RelativeHint(Floor.First, Animal.Rabbit, -2),
    ]

    redunant_neighbor_hints = [
        NeighborHint(Animal.Bird, Color.Blue),
        NeighborHint(Color.Blue, Animal.Bird)
    ]

    assert count_assignments(redundant_absolute_hints) == 1
    assert count_assignments(redundant_absolute_hints2) == math.factorial(5)*math.factorial(4)
    
    assert count_assignments(redunant_relative_hints) == 1
    assert count_assignments(redunant_relative_hints2) == math.factorial(5)*math.factorial(4)
    
    assert count_assignments(redunant_neighbor_hints) == 4608


def test_duplicated_hints():
    duplicated_absolute_hint = [
        AbsoluteHint(Animal.Rabbit, Floor.First),
        AbsoluteHint(Animal.Rabbit, Floor.First)
    ]

    duplicated_neibouring_hints = [
        NeighborHint(Animal.Chicken, Color.Blue),
        NeighborHint(Animal.Chicken, Color.Blue)
    ]

    assert count_assignments(duplicated_absolute_hint) == math.factorial(5)*math.factorial(4)
    assert count_assignments(duplicated_neibouring_hints) == math.factorial(5)

def test_relative_hints():
    single_relative_hint = [
        RelativeHint(Animal.Rabbit, Color.Green, -2)
    ]

    absolute_hints_in_disguise = [
        # Relative hints with distance 0 should be like absolute hints
        RelativeHint(Animal.Rabbit, Floor.First, 0),
    ]

    assert count_assignments(single_relative_hint) == 1728
    assert count_assignments(absolute_hints_in_disguise) == math.factorial(5)*math.factorial(4)

def test_neighbor_hints():
    """
    Sanity check as neighbor hints are derived from relative.
    """
    single_neighbor_hint = [
        NeighborHint(Animal.Rabbit, Color.Green)
    ]
    assert(count_assignments(single_neighbor_hint) == 4608)

def assignment_tests():
    """
    Tests given in the assignment document.
    """
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

    assert count_assignments(HINTS_EX1) == 2
    assert count_assignments(HINTS_EX2) == 4

if __name__ == '__main__':
    test_check_is_satisfied_absolute_hint()
    test_get_possible_floor_assignments_absolute_hint_impossible_hint()
    test_get_possible_floor_assignments_absolute_hint_possible_hint()
    test_count_assignments_no_hints()

    test_count_assignments_absolute_hints_only()
    test_relative_hints()
    test_neighbor_hints()
    assignment_tests()

    test_redundant_hints()

    print('Success!')
