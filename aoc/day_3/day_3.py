from dataclasses import dataclass
from typing import List, Tuple, Union
from math import prod

with open("aoc/day_3/input.txt", "r") as f:
    _input = f.read()


with open("aoc/day_3/test.txt", "r") as f:
    _test = f.read()


@dataclass
class TreeSquare:
    _c: str


@dataclass
class OpenSquare:
    _c: str


@dataclass
class SlopeLine:
    raw: str
    parsed: List[Union[TreeSquare, OpenSquare]]

    @classmethod
    def from_raw(cls, raw: str) -> "SlopeLine":
        return cls(
            raw=raw,
            parsed=[TreeSquare(c) if c == "#" else OpenSquare(c) for c in raw],
        )

    def duplicate(self) -> None:
        self.raw = self.raw + self.raw
        self.parsed = self.parsed + self.parsed


class SlopeIsOver(Exception):
    pass


class SlopeShallBeExtended(Exception):
    pass


@dataclass
class Slope:
    slope_lines: List[SlopeLine]
    _coord_right = 0
    _coord_down = 0
    _rules = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    @classmethod
    def from_raw(cls, raw: str) -> "Slope":
        return cls(
            slope_lines=[SlopeLine.from_raw(r) for r in raw.splitlines()]
        )

    def _get(
        self, coord_right: int, coord_down: int
    ) -> Union[TreeSquare, OpenSquare]:
        try:
            _down = self.slope_lines[coord_down]
        except IndexError as e:
            raise SlopeIsOver from e
        try:
            return _down.parsed[coord_right]
        except IndexError as e:
            raise SlopeShallBeExtended from e

    def _repeat_to_the_right(self) -> None:
        for line in self.slope_lines:
            line.duplicate()

    def _increment_coords_part_1(self) -> None:
        self._coord_right += 3
        self._coord_down += 1

    def _increment_coords_by_rule(self, rule: Tuple[int, int]) -> None:
        self._coord_right += rule[0]
        self._coord_down += rule[1]

    def _reset_coords(self) -> None:
        self._coord_right = 0
        self._coord_down = 0

    def count_trees_part_1(self) -> int:
        # starting point shall be OpenSquare
        assert isinstance(
            self._get(self._coord_right, self._coord_down), OpenSquare
        )
        tree_count = 0
        self._increment_coords_part_1()
        while True:
            try:
                tree_or_open = self._get(self._coord_right, self._coord_down)
                if isinstance(tree_or_open, TreeSquare):
                    tree_count += 1
            except SlopeShallBeExtended:
                print("Extending the slope to the right")
                self._repeat_to_the_right()
            except SlopeIsOver:
                print("Slope should be over")
                return tree_count
            else:
                self._increment_coords_part_1()

    def count_trees_part_2(self) -> Tuple[List[int], int]:
        tree_count_list = []
        for rule in self._rules:
            tree_count = 0
            self._reset_coords()
            assert isinstance(
                self._get(self._coord_right, self._coord_down), OpenSquare
            )
            self._increment_coords_by_rule(rule)
            while True:
                try:
                    tree_or_open = self._get(
                        self._coord_right, self._coord_down
                    )
                    if isinstance(tree_or_open, TreeSquare):
                        tree_count += 1
                except SlopeShallBeExtended:
                    print("Extending the slope to the right")
                    self._repeat_to_the_right()
                except SlopeIsOver:
                    print("Slope should be over")
                    tree_count_list.append(tree_count)
                    break
                else:
                    self._increment_coords_by_rule(rule)
        return tree_count_list, prod(tree_count_list)


if __name__ == "__main__":
    # part 1
    # test
    slope = Slope.from_raw(_test)
    trees = slope.count_trees_part_1()
    print(f"TEST - Encountered {trees} trees")
    # prod
    slope = Slope.from_raw(_input)
    trees = slope.count_trees_part_1()
    print(f"PROD - Encountered {trees} trees")
    # part 2
    # test
    slope = Slope.from_raw(_test)
    tree_list, trees_multiplied = slope.count_trees_part_2()
    print(
        f"TEST - Encountered {tree_list} trees, multiplied they give {trees_multiplied}"
    )
    # prod
    slope = Slope.from_raw(_input)
    tree_list, trees_multiplied = slope.count_trees_part_2()
    print(
        f"PROD- Encountered {tree_list} trees, multiplied they give {trees_multiplied}"
    )
