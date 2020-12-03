from dataclasses import dataclass
from typing import List, Union

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

    @classmethod
    def from_raw(cls, raw: str) -> "Slope":
        return cls(
            slope_lines=[SlopeLine.from_raw(r) for r in raw.splitlines()]
        )

    def _get(
        self, coord_right: int, coord_down: int
    ) -> Union[TreeSquare, OpenSquare]:
        # should raise IndexError if slope is too short to the right.
        # return self.slope_lines[coord_down].parsed[coord_right]
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

    def _increment_coords(self) -> None:
        self._coord_right += 3
        self._coord_down += 1

    def count_trees(self) -> int:
        # starting point shall be OpenSquare
        assert isinstance(
            self._get(self._coord_right, self._coord_down), OpenSquare
        )
        tree_count = 0
        self._increment_coords()
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
                self._increment_coords()


if __name__ == "__main__":
    # test
    slope = Slope.from_raw(_test)
    trees = slope.count_trees()
    print(f"TEST - Encountered {trees} trees")
    # prod
    slope = Slope.from_raw(_input)
    trees = slope.count_trees()
    print(f"PROD - Encountered {trees} trees")