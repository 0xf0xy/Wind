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

from wind.core import Wind
import argparse


def build_parser():
    parser = argparse.ArgumentParser(
        description="Wind: Pattern-based wordlist generator", add_help=False
    )

    info = parser.add_argument_group("Target Info")
    info.add_argument("name", type=str.lower, help="Target name")
    info.add_argument("-sn", "--surname", type=str.lower, help="Target surname")
    info.add_argument("-b", "--birth", help="Birth date (DD/MM/YYYY)")
    info.add_argument("-p", "--pet", help="Pet names (comma-separated)")
    info.add_argument("-k", "--keywords", help="Additional keywords (comma-separated)")

    wordlist = parser.add_argument_group("Wordlist Settings")
    wordlist.add_argument(
        "-mn", "--min-length", type=int, default=8, help="Minimum word length"
    )
    wordlist.add_argument("-mx", "--max-length", type=int, help="Maximum word length")
    wordlist.add_argument(
        "-s", "--special", action="store_true", help="Include special characters"
    )
    wordlist.add_argument(
        "-l", "--leet", action="store_true", help="Use leet transformations (l1k3 7h1s)"
    )
    wordlist.add_argument(
        "-c", "--case", action="store_true", help="Apply case transformations"
    )
    wordlist.add_argument("-o", "--output", help="Output file name")

    meta = parser.add_argument_group("Information")
    meta.add_argument("-h", "--help", action="help", help="Show this help menu")
    meta.add_argument(
        "-v",
        "--version",
        action="version",
        version="Wind v1.0.0",
        help="Show program version",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    data = {
        "name": args.name,
        "surname": args.surname,
        "pets": args.pet,
        "birth": args.birth,
        "keywords": args.keywords,
    }

    options = {
        "leet": args.leet,
        "special": args.special,
        "case": args.case,
        "min_length": args.min_length,
        "max_length": args.max_length,
        "output": args.output,
    }

    wind = Wind()
    wind.generate_wordlist(data, options)
