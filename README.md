<h1 align="center">WIND</h1>

<p align="center">
  <em>pattern-based wordlist generator</em>
</p>

<p align="center">
  <img src="https://img.shields.io/github/release/0xf0xy/Wind?color=AAAAAA&style=for-the-badge&labelColor=111111"/>
  <img src="https://img.shields.io/badge/python-3.10+-AAAAAA?style=for-the-badge&logo=python&logoColor=FFFFFF&labelColor=111111"/>
  <img src="https://img.shields.io/github/license/0xf0xy/Wind?color=AAAAAA&style=for-the-badge&labelColor=111111"/>
</p>

<br>

> [!WARNING]
>
> **Wind is intended for educational, research, and authorized security testing purposes only.**
>
> Generated wordlists should only be used against systems, accounts, and environments where you have explicit permission to perform security testing.
>
> The author is not responsible for misuse of this software.

<br>

## > Overview

**Wind** is a modular, pattern-based wordlist generator designed to create structured password candidates from user-defined words and configurable generation patterns.

Instead of relying exclusively on random combinations, Wind uses **patterns** to describe how candidate strings should be constructed.

Wind was built primarily as a learning and security research project around:

* Password pattern analysis
* Dictionary-based auditing
* Candidate generation
* Security research
* CLI application design
* Modular Python architecture

<br>

## > How It Works

Wind receives a collection of words and applies generation patterns to them.

A pattern describes the structure of a candidate.

For example:

```text
{word}{number}
```

represents a candidate composed of:

```text
word + number
```

Given:

```text
cat
flowers
codes
```

Wind can produce candidates such as:

```text
cat1
cat42
flowers7
codes123
...
```

Patterns can also contain multiple components:

```text
{word}{symbol}{number}
```

or:

```text
{word}{symbol}{word}
```

For multiple `{word}` components, each occurrence can receive a different word from the provided input set.

For example:

```text
{word}{symbol}{word}
```

with:

```text
cat
flowers
codes
```

can generate:

```text
cat!cat
cat!flowers
cat!codes

flowers!cat
flowers!flowers
flowers!codes

codes!cat
codes!flowers
codes!codes
...
```

This allows Wind to describe candidate structures without hardcoding every possible combination into the generation engine.

<br>

## > Pattern Components

Patterns are composed using placeholders.

| Component  | Description                                |
| ---------- | ------------------------------------------ |
| `{word}`   | Uses one of the words supplied by the user |
| `{number}` | Generates a numeric component              |
| `{symbol}` | Generates a symbol component               |

Components can be combined to create more complex structures.

<br>

## > Patterns

Pattern definitions are stored separately from the generation engine.

The default pattern data is located at:

```text
wind/data/patterns.json
```

The engine is responsible for **how candidates are generated**.

The pattern data is responsible for **which structures should be generated**.

```text
Generation Engine
       │
       │ interprets
       ▼
   Pattern Data
       │
       ▼
Candidate Structure
```

This makes the pattern system easier to modify and extend.

<br>

## > Custom Patterns

Wind's pattern system is designed to be extensible.

Instead of modifying the generation engine whenever a new candidate structure is needed, patterns can be defined through the project's pattern data.

For example:

```text
{word}{number}
{word}{symbol}{number}
{word}{symbol}{word}
{word}{number}{symbol}
{word}{symbol}{word}{number}
```

The engine interprets these structures and expands them using the provided input.

This approach keeps generation logic independent from the specific patterns being used.

<br>

## > Installation

### Requirements

* Python 3.10+
* `pip`

Wind has no external runtime dependencies.

Clone the repository:

```bash
git clone https://github.com/0xf0xy/Wind.git
cd Wind
```

Install Wind:

```bash
pip install .
```

Verify the installation:

```bash
wind -h
```

<br>

## > Usage

Provide the words that should be used during generation:

```bash
wind cat,flowers,codes -l -c -s
```

For available commands and options:

```bash
wind -h
```

<br>

## > Project Status

Wind is an experimental project focused on security research, experimentation and learning.

The project is under active development and its architecture and behavior may change between releases.

<br>

---

<p align="center">
  <a href="https://github.com/0xf0xy"><b>0xf0xy</b></a> •
  <a href="./LICENSE"><b>MIT License</b></a>
</p>
