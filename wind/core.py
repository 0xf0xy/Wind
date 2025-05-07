"""
MIT License

Copyright (c) 2025 0xf0xy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from importlib.resources import files
from itertools import product
from rich import print
import json


class Wind:
    """
    Wind: Pattern-based password wordlist generator.
    """

    def __init__(self):
        """
        Initialize Wind instance and load the configuration.
        """
        self._load_config()

    def _load_config(self):
        """
        Load data from the JSON file.

        Sets common numbers, special characters, number/year ranges, leet mappings, and password patterns.
        """
        with files("wind.data").joinpath("config.json").open("r") as f:
            config = json.load(f)
            self.common_numbers = config.get("common_numbers")
            self.special_chars = config.get("special_chars")
            self.numbers_range = config.get("numbers_range")
            self.years_range = config.get("years_range")
            self.leet_map = config.get("leet_map")
            self.passwd_patterns = config.get("passwd_patterns")

    @staticmethod
    def clean_birth(birth: str) -> list[str]:
        """
        Process a birth date string and extract possible numeric parts.

        Args:
            birth (str): Birth date in the format "DD/MM/YYYY".

        Returns:
            list[str]: List containing day, month, year, and full birthdate as strings.
        """
        if not birth:
            return []

        birth = birth.replace("/", "")

        return [birth[:2], birth[2:4], birth[:4], birth[-4:], birth]

    @staticmethod
    def apply_case_variations(word: str, upper: bool, capitalize: bool) -> set[str]:
        """
        Apply case variations to a word based on options.

        Args:
            word (str): The input word.
            upper (bool): Whether to add the uppercase version.
            capitalize (bool): Whether to add the capitalized version.

        Returns:
            set[str]: Set containing all case variations.
        """
        variations = {word}
        if upper:
            variations.add(word.upper())
        if capitalize:
            variations.add(word.capitalize())

        return variations

    def apply_leet(self, word: str) -> set[str]:
        """
        Generate leetspeak variations of a word based on the configured leet map.

        Args:
            word (str): The input word.

        Returns:
            set[str]: Set of leetspeak variations.
        """
        variants = set([word])

        for i, char in enumerate(word.lower()):
            if char in self.leet_map:
                new_variants = set()
                for variant, replacement in product(variants, self.leet_map[char]):
                    new = variant[:i] + replacement + variant[i + 1 :]
                    new_variants.add(new)
                variants.update(new_variants)

        return variants

    def generate_passwds(
        self,
        words: dict[str],
        base_numbers: list[str],
        min_len: int,
        max_len: int,
        leet: bool,
        special: bool,
        upper: bool,
        capitalize: bool,
    ) -> set[str]:
        """
        Generate password combinations based on defined patterns.

        Args:
            words (dict[str]): Dictionary with name, surname, pets, and keywords.
            base_numbers (list[str]): List of birthdates, years, or custom numbers.
            min_len (int): Minimum password length.
            max_len (int): Maximum password length.
            leet (bool): Apply leetspeak transformations.
            special (bool): Include special characters.
            upper (bool): Include uppercase variations.
            capitalize (bool): Include capitalized variations.

        Returns:
            set[str]: Set of generated password combinations.
        """
        combos = set()

        numbers = (
            base_numbers
            if base_numbers
            else {
                str(n) for n in range(self.numbers_range[0], self.numbers_range[1] + 1)
            }.union(str(y) for y in range(self.years_range[0], self.years_range[1] + 1))
        )
        numbers.update(self.common_numbers)

        symbols = self.special_chars if special else [""]

        name = words.get("name")
        surname = words.get("surname")
        pets = words.get("pets")
        keywords = words.get("keywords")

        for pet, keyword, pattern, symbol, number in product(
            pets, keywords, self.passwd_patterns, symbols, numbers
        ):
            result = pattern.format(
                name=name,
                surname=surname,
                pet=pet,
                number=number,
                symbol=symbol,
                keyword=keyword,
            )

            if min_len <= len(result) <= max_len:
                for variation in self.apply_case_variations(result, upper, capitalize):
                    combos.add(variation)
                    if leet:
                        combos.update(self.apply_leet(variation))

        return combos

    def generate_wordlist(self, data: dict[str], options: dict[str]) -> list[str]:
        """
        Generate a wordlist based on user data and generation options.

        Args:
            data (dict[str]): Contains name, surname, pets, birth, keywords.
            options (dict[str]): Generation options:
                - leet (bool): Apply leetspeak.
                - special (bool): Include special characters.
                - upper (bool): Include uppercase variations.
                - capitalize (bool): Include capitalized variations.
                - min_length (int): Minimum password length.
                - max_length (int): Maximum password length.

        Returns:
            list[str]: Sorted list of generated passwords.
        """
        words = {
            "name": data.get("name"),
            "surname": (data.get("surname") or ""),
            "pets": [p.lower() for p in (data.get("pets") or "").split(",") if p]
            or [""],
            "keywords": [
                k.lower() for k in (data.get("keywords") or "").split(",") if k
            ]
            or [""],
        }

        print("[bold blue]*[/bold blue] Generating wordlist\n")

        wordlist = self.generate_passwds(
            words=words,
            base_numbers=self.clean_birth(data.get("birth")),
            min_len=options.get("min_length"),
            max_len=options.get("max_length") or options.get("min_length"),
            leet=options.get("leet"),
            special=options.get("special"),
            upper=options.get("upper"),
            capitalize=options.get("capitalize"),
        )

        output = f"{options.get("output") or data.get("name")}.txt"

        with open(output, "w") as f:
            for word in sorted(wordlist):
                f.write(f"{word}\n")

            print(
                f"[bold green]+[/bold green] Total words generated: [bold green]{len(wordlist)}[/bold green]"
            )
            print(
                f"[bold green]+[/bold green] Wordlist saved as: [bold green]{output}[/bold green]"
            )
