from dataclasses import dataclass, field
from typing import Callable


@dataclass(slots=True)
class GenerationOptions:
    max_length: int = 16

    leet: bool = False
    special: bool = False
    case_variation: bool = False

    numbers: list[str] = field(default_factory=list)

    output: str = "wordlist.txt"


@dataclass(slots=True)
class GenerationResult:
    output: str
    generated: int
    skipped: int
    completed: bool = True


ProgressCallback = Callable[[str, int], None]
