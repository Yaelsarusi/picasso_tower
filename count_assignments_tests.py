
from count_assignments import AbsoluteHint, Animal, Color, Floor, FloorAssignment, NeighborHint, RelativeHint

def test_check_is_satisfied_absolute_hint():
    assert AbsoluteHint(Animal.Bird, Floor(1)).check_if_satisfied(FloorAssignment(floor=Floor(1), animal=Animal.Bird, color=Color.Blue))
    assert not AbsoluteHint(Color.Blue, Floor(2)).check_if_satisfied(FloorAssignment(floor=Floor(1), animal=Animal.Bird, color=Color.Blue))
    assert AbsoluteHint(Color.Blue, Floor(2)).check_if_satisfied(FloorAssignment(floor=Floor(2), animal=Animal.Bird, color=Color.Blue))
    assert AbsoluteHint(Animal.Bird, Color.Blue).check_if_satisfied(FloorAssignment(floor=Floor(3), animal=Animal.Bird, color=Color.Blue))
    assert AbsoluteHint(Floor(1), Animal.Bird).check_if_satisfied(FloorAssignment(floor=Floor(3), animal=Animal.Bird, color=Color.Blue))

def test_get_possible_floor_assignments_absolute_hint():
    hint = AbsoluteHint(Animal.Bird, Floor(1))
    empty_floors = [Floor(2),Floor(3)]
    possible_animals = [Animal.Chicken, Animal.Frog]
    possible_colors = [Color.Blue, Color.Green]
    # assert len(hint.get_possible_floor_assignments(empty_floors=empty_floors, animal_options=possible_animals, color_options=possible_colors)) == 4

def test_get_possible_floor_assignments_relative_hint():
    hint = RelativeHint(Animal.Chicken, Color.Blue, -4)
    empty_floors = [Floor(1), Floor(5)]
    possible_animals = [Animal.Chicken, Animal.Frog]
    possible_colors = [Color.Blue, Color.Green]

    floor_assignment, additional_hints = hint.get_possible_floor_assignments(empty_floors=empty_floors, all_animal_options=possible_animals, all_color_options=possible_colors, floor_assignments=floor_assignment)

    print(floor_assignment)
    print(additional_hints[0]._attr1)
    print(additional_hints[0]._attr2)

    print(len(hint.get_possible_floor_assignments(empty_floors=empty_floors, all_animal_options=possible_animals, all_color_options=possible_colors)))
    

if __name__ == '__main__':
    test_get_possible_floor_assignments_relative_hint()
    