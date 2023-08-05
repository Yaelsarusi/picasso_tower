from dataclasses import dataclass

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

@dataclass
class getOptionsIfValidReturnType:
    is_valid: bool
    new_options: List[]

def getOptionsIfValid(options) -> List[Union[Color, Animal, Floor]]:
    if self._attr1 in options:
        return (True, [self._attr1], None)
    elif self._attr2 in options:
        floor_assignment_with_attr1 = list(filter(lambda x: self._attr1 in x, floor_assignments))
        new_floor = floor_assignment_with_attr1[0].floor.value - self._difference
        if new_floor < 6 and new_floor > 0:
            return (False, [], [(None, [AbsoluteHint(Floor(new_floor), self._attr2 )])])
        return []
    else:
        return []