import argparse
from importlib.metadata import version

from wind.core.generator import Wind
from wind.core.models import GenerationOptions


def red(text: str) -> str:
    return f"\033[1;31m{text}\033[0m"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Wind: Pattern-based wordlist generator.",
        add_help=False,
    )

    info = parser.add_argument_group("Target Information")

    info.add_argument(
        "words",
        nargs="+",
        help=(
            "Words used as generation sources. "
            "Multiple words can be provided separated by spaces "
            "or as a comma-separated value."
        ),
    )

    info.add_argument(
        "-n",
        "--numbers",
        nargs="+",
        type=str,
        help=(
            "Numbers used as generation sources. "
            "Multiple values can be provided separated by spaces "
            "or as comma-separated values. "
            "Dates are also accepted (DD/MM/YYYY)."
        ),
    )

    wordlist = parser.add_argument_group("Wordlist Settings")

    wordlist.add_argument(
        "-mx",
        "--max-length",
        type=int,
        default=16,
        help="Maximum password length (default: 16)",
    )

    wordlist.add_argument(
        "-s",
        "--special",
        action="store_true",
        help="Include special characters",
    )

    wordlist.add_argument(
        "-l",
        "--leet",
        action="store_true",
        help="Use leet transformations (l1k3 7h1s)",
    )

    wordlist.add_argument(
        "-c",
        "--case",
        action="store_true",
        help="Apply case transformations",
    )

    wordlist.add_argument(
        "-o",
        "--output",
        type=str,
        default="wordlist.txt",
        help="Output file name (default: wordlist.txt)",
    )

    meta = parser.add_argument_group("Information")

    meta.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help menu",
    )

    meta.add_argument(
        "-v",
        "--version",
        action="version",
        # version=f"Wind v{version('wind')}",
        help="Show program version",
    )

    return parser


def normalize_cli_values(values: list[str] | None) -> list[str]:
    if not values:
        return []

    result: list[str] = []

    for value in values:
        result.extend(item.strip() for item in value.split(",") if item.strip())

    return result


def print_header(options: GenerationOptions) -> None:
    print(red("Wind - Pattern-based Wordlist Generator"))
    print("─" * 50)

    print("\nWordlist Settings")
    print("─" * 50)
    print(f"Max. length  : {options.max_length}")
    print(f"Special      : {'yes' if options.special else 'no'}")
    print(f"Leet         : {'yes' if options.leet else 'no'}")
    print(f"Case         : {'yes' if options.case_variation else 'no'}")
    print(f"Output       : {options.output}")
    print()


def print_progress(_, total: int) -> None:
    print(
        f"\rGenerated: {total:,}",
        end="",
        flush=True,
    )


def print_result(result) -> None:
    if result.generated == 0:
        print(f"{red('[x]')} " "No passwords generated. Please check your input data.")
        return

    print(red("[✓] Wordlist generation complete!\n"))

    print(f"    Output file   : {red(result.output)}")
    print(f"    Words total   : {red(f'{result.generated:,}')}")
    print(f"    Duplicates    : {red(f'{result.skipped:,}')}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    words = normalize_cli_values(args.words)
    numbers = normalize_cli_values(args.numbers)

    if not words:
        parser.error("At least one word must be provided.")

    if args.max_length < 4:
        parser.error("Maximum length cannot be smaller than 4.")

    options = GenerationOptions(
        max_length=args.max_length,
        leet=args.leet,
        special=args.special,
        case_variation=args.case,
        numbers=numbers,
        output=args.output,
    )

    print_header(options=options)

    print(red("[*] Generating wordlist...\n"))

    wind = Wind()

    try:
        result = wind.generate_wordlist(
            words=words, options=options, progress=print_progress
        )

    except KeyboardInterrupt:
        print(f"\n{red('[!]')} Generation stopped by user.")
        raise SystemExit(130)

    except ValueError as exc:
        print(f"{red('[x]')} {exc}")
        raise SystemExit(1)

    except Exception as exc:
        print(f"{red('[x]')} {exc}")
        raise SystemExit(1)

    print("\n")
    print_result(result)
