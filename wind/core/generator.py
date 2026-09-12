import json
import re
import sqlite3
import tempfile
from collections.abc import Generator, Iterable
from importlib.resources import files
from pathlib import Path

from .models import GenerationOptions, GenerationResult, ProgressCallback


class Wind:

    DEFAULT_NUMBERS_RANGE = (0, 100)
    DEFAULT_YEARS_RANGE = (1990, 2025)

    COMMON_NUMBERS = ("123", "1234", "12345")

    SPECIAL_CHARS = (
        "!",
        "@",
        "#",
        "$",
        "%",
        "&",
        "*",
        "_",
    )

    LEET_MAP = {
        "a": ("4",),
        "e": ("3",),
        "i": ("1",),
        "o": ("0",),
        "s": ("5",),
        "t": ("7",),
    }

    SUPPORTED_COMPONENTS = {"word", "number", "symbol"}

    PATTERN_REGEX = re.compile(r"{([^{}]+)}")

    def __init__(self) -> None:
        self.patterns = self._load_patterns()

    @staticmethod
    def _load_patterns() -> list[str]:
        config_path = files("wind.data").joinpath("patterns.json")

        with config_path.open("r", encoding="utf-8") as file:
            config = json.load(file)

        patterns = config.get("patterns", [])

        if not isinstance(patterns, list):
            raise ValueError("'patterns' must be a list.")

        if not all(isinstance(pattern, str) for pattern in patterns):
            raise ValueError("Every pattern must be a string.")

        return patterns

    @staticmethod
    def normalize_words(words: Iterable[str] | str | None) -> list[str]:
        if words is None:
            return []

        if isinstance(words, str):
            words = words.split(",")

        normalized: list[str] = []
        seen: set[str] = set()

        for word in words:
            word = word.strip().lower()

            if not word:
                continue

            if word in seen:
                continue

            seen.add(word)
            normalized.append(word)

        return normalized

    @staticmethod
    def clean_date(values: Iterable[str] | None) -> list[str]:
        if not values:
            return []

        result: list[str] = []

        for value in values:
            value = value.strip()

            if not value:
                continue

            normalized = value.replace("/", "").replace("-", "")

            if normalized.isdigit() and len(normalized) == 8:
                result.extend(
                    [
                        normalized[:2],
                        normalized[2:4],
                        normalized[:4],
                        normalized[-4:],
                        normalized,
                    ]
                )
                continue

            if value.isdigit():
                result.append(value)

        return result

    def _generate_numbers(
        self, custom_numbers: Iterable[str] | None = None
    ) -> Generator[str, None, None]:
        seen: set[str] = set()

        if custom_numbers:
            for number in custom_numbers:
                number = str(number)

                if number in seen:
                    continue

                seen.add(number)
                yield number

            return

        start, end = self.DEFAULT_NUMBERS_RANGE

        for number in range(start, end + 1):
            value = str(number)

            if value in seen:
                continue

            seen.add(value)
            yield value

        start_year, end_year = self.DEFAULT_YEARS_RANGE

        for year in range(start_year, end_year + 1):
            value = str(year)

            if value in seen:
                continue

            seen.add(value)
            yield value

        for number in self.COMMON_NUMBERS:
            if number in seen:
                continue

            seen.add(number)
            yield number

    def apply_leet(self, value: str) -> Generator[str, None, None]:
        def generate(index: int, current: str) -> Generator[str, None, None]:
            if index >= len(value):
                yield current
                return

            character = value[index]
            lower_character = character.lower()

            yield from generate(index + 1, current + character)

            for replacement in self.LEET_MAP.get(lower_character, ()):
                yield from generate(index + 1, current + replacement)

        yield from generate(0, "")

    @staticmethod
    def _case_variations(value: str, enabled: bool) -> Generator[str, None, None]:
        yield value

        if not enabled:
            return

        yield value.upper()
        yield value.capitalize()

    @classmethod
    def _parse_pattern(cls, pattern: str) -> list[tuple[str, str]]:
        tokens: list[tuple[str, str]] = []

        position = 0

        for match in cls.PATTERN_REGEX.finditer(pattern):
            if match.start() > position:
                tokens.append(("literal", pattern[position : match.start()]))

            component = match.group(1)

            if component not in cls.SUPPORTED_COMPONENTS:
                raise ValueError(f"Unsupported pattern component: " f"{{{component}}}")

            tokens.append(("component", component))

            position = match.end()

        if position < len(pattern):
            tokens.append(("literal", pattern[position:]))

        return tokens

    @staticmethod
    def _lazy_product(
        sources: list[Iterable[str]],
    ) -> Generator[tuple[str, ...], None, None]:
        if not sources:
            yield ()
            return

        first = sources[0]

        for value in first:
            remaining = Wind._lazy_product(sources[1:])

            for combination in remaining:
                yield (value, *combination)

    def _build_sources(
        self,
        components: list[str],
        words: list[str],
        custom_numbers: Iterable[str] | None,
        symbols: tuple[str, ...],
    ) -> list[Iterable[str]]:
        sources: list[Iterable[str]] = []

        for component in components:
            if component == "word":
                sources.append(words)

            elif component == "symbol":
                sources.append(symbols)

            elif component == "number":
                sources.append(self._generate_numbers(custom_numbers=custom_numbers))

        return sources

    def generate(
        self, words: Iterable[str] | str, options: GenerationOptions
    ) -> Generator[str, None, None]:
        normalized_words = self.normalize_words(words)

        if not normalized_words:
            return

        custom_numbers = self.clean_date(options.numbers)

        symbols = self.SPECIAL_CHARS if options.special else ("",)

        for pattern in self.patterns:
            try:
                tokens = self._parse_pattern(pattern)

            except ValueError:
                continue

            components = [
                value for token_type, value in tokens if token_type == "component"
            ]

            if not components:
                continue

            sources = self._build_sources(
                components=components,
                words=normalized_words,
                custom_numbers=custom_numbers,
                symbols=symbols,
            )

            for combination in self._lazy_product(sources):
                values = iter(combination)

                result: list[str] = []

                for token_type, value in tokens:
                    if token_type == "literal":
                        result.append(value)

                    else:
                        result.append(next(values))

                password = "".join(result)

                if not (4 <= len(password) <= options.max_length):
                    continue

                for variation in self._case_variations(
                    password, options.case_variation
                ):
                    if options.leet:
                        yield from self.apply_leet(variation)

                    else:
                        yield variation

    @staticmethod
    def _create_seen_database(path: str) -> sqlite3.Connection:
        connection = sqlite3.connect(path)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                password TEXT PRIMARY KEY
            )
            """)

        connection.commit()

        return connection

    def generate_wordlist(
        self,
        words: Iterable[str] | str,
        options: GenerationOptions,
        progress: ProgressCallback | None = None,
    ) -> GenerationResult:
        output_path = Path(options.output)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        generated = 0
        skipped = 0

        with tempfile.NamedTemporaryFile(suffix=".db", delete=True) as database_file:
            connection = self._create_seen_database(database_file.name)

            try:
                with output_path.open("w", encoding="utf-8") as output:
                    for password in self.generate(words=words, options=options):
                        cursor = connection.execute(
                            """
                            INSERT OR IGNORE INTO passwords(password)
                            VALUES(?)
                            """,
                            (password,),
                        )

                        if cursor.rowcount == 0:
                            skipped += 1
                            continue

                        output.write(password)
                        output.write("\n")

                        generated += 1

                        if progress:
                            progress(password, generated)

                connection.commit()

            finally:
                connection.close()

        return GenerationResult(
            output=str(output_path),
            generated=generated,
            skipped=skipped,
            completed=True,
        )
