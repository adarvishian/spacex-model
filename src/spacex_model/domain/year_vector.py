"""Length-26 year vector wrapper indexed [0..25] = years [2025..2050]."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

import numpy as np

from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS, LAST_YEAR

T = TypeVar("T", bound=np.generic)


@dataclass(frozen=True, slots=True)
class YearVector(Generic[T]):
    """Vectorized quantity over the model horizon."""

    values: np.ndarray

    def __post_init__(self) -> None:
        if self.values.shape != (HORIZON_YEARS,):
            msg = f"YearVector must have shape ({HORIZON_YEARS},), got {self.values.shape}"
            raise ValueError(msg)

    @classmethod
    def zeros(cls, dtype: type[T] = np.float64) -> YearVector[T]:
        return cls(values=np.zeros(HORIZON_YEARS, dtype=dtype))

    @classmethod
    def constant(cls, value: float) -> YearVector[np.float64]:
        return cls(values=np.full(HORIZON_YEARS, value, dtype=np.float64))

    def year_index(self, year: int) -> int:
        if year < FIRST_YEAR or year > LAST_YEAR:
            msg = f"Year {year} outside horizon [{FIRST_YEAR}, {LAST_YEAR}]"
            raise ValueError(msg)
        return year - FIRST_YEAR

    def at(self, year: int) -> T:
        return self.values[self.year_index(year)]

    def years(self) -> range:
        return range(FIRST_YEAR, LAST_YEAR + 1)

    def __len__(self) -> int:
        return HORIZON_YEARS
