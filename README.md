<h1 align="center">WIND</h1>

<p align="center">
  <em>pattern-based wordlist generator</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-EXPERIMENTAL-AAAAAA?style=for-the-badge&labelColor=111111"/>
  <img src="https://img.shields.io/badge/python-3.10+-AAAAAA?style=for-the-badge&logo=python&logoColor=FFFFFF&labelColor=111111"/>
  <img src="https://img.shields.io/github/license/0xf0xy/Wind?color=AAAAAA&style=for-the-badge&labelColor=111111"/>
</p>

<br>

> [!WARNING]
>
> This project is provided for **educational and security research purposes only**.
> 
> Generated wordlists should only be used against systems, accounts and environments where you have explicit authorization to perform security testing.
> 
> The author is not responsible for misuse of this software.

<br>

## > Overview

**Wind** is a pattern-based wordlist generator designed to create password candidates from user-defined words and configurable generation patterns.

Instead of relying on purely random combinations, Wind uses structured rules to generate candidates based on common password construction patterns.

The project can be used for:

* Password security research
* Dictionary-based auditing
* Credential pattern analysis
* Controlled security testing
* Educational purposes

<br>

## > Features

* Pattern-based wordlist generation
* User-defined input words
* Configurable generation parameters
* Structured candidate generation
* Extensible pattern system
* Patterns separated from the generation engine
* Command-line interface
* Lightweight implementation

<br>

## > How It Works

Wind uses patterns to define how input words are combined.

Available pattern components include:

```text
{word}
{number}
{symbol}
```

Patterns can be composed to describe different candidate structures:

```text
{word}{number}

{word}{symbol}{number}

{word}{symbol}{word}

{word}{number}{symbol}

{word}{symbol}{word}{number}
```

For example, given the input:

```text
cat
flowers
codes
```

the pattern:

```text
{word}{symbol}{word}
```

can generate candidates such as:

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

Each occurrence of `{word}` is treated as an independent source, allowing Wind to generate structured permutations from the provided input.

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

## > Patterns

Generation patterns are stored separately from the generation engine.

The default patterns are located at:

```text
wind/data/patterns.json
```

A pattern defines the structure of each generated candidate.

### Components

| Component  | Description                          |
| ---------- | ------------------------------------ |
| `{word}`   | Uses one of the provided input words |
| `{number}` | Generates a numeric component        |
| `{symbol}` | Generates a symbol component         |

For example:

```text
{word}{number}
```

may produce:

```text
cat1
cat42
flowers7
codes123
...
```

More complex structures can be created by combining multiple components.

<br>

## > Installation

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

## > Project Status

Wind is an experimental project focused on security research, experimentation and learning.

The project is under active development and its architecture and behavior may change between releases.

---

<p align="center">
  <a href="https://github.com/0xf0xy"><b>0xf0xy</b></a> •
  <a href="./LICENSE"><b>MIT License</b></a>
</p>
