---
name: afwf-genpass-cli
description: Generate one secure password, short ID, or UUID4 from the shell via the afwf-genpass CLI (the `*-one` subcommands). Use when the user asks for a random password, random ID/slug/token, or UUID4 on the command line — or wants to pipe one into another shell command, env var, or script.
---

# afwf-genpass CLI

`afwf-genpass` is a Python CLI that powers the Alfred workflow of the same
name. It exposes three Alfred Script Filter subcommands (`genpass`, `genid`,
`genuuid4`) **and** three "single value" variants — `genpass-one`, `genid-one`,
`genuuid4-one` — that print exactly one value to stdout. **Only the `*-one`
variants are documented here**, because they are the only ones meaningful
outside Alfred.

## Subcommands (stdout, one value)

```
afwf-genpass genpass-one [--length INT]   # default 12, range 8..32
afwf-genpass genid-one   [--length INT]   # default 16, range 6..32
afwf-genpass genuuid4-one                 # no parameters
```

- `genpass-one` — random password. Always contains at least one lowercase,
  one uppercase, one digit, and one symbol from `!%@#&^*`; starts with a
  letter; excludes the visually-confusing characters `1 l I O 0`.
- `genid-one` — YouTube-style short ID from a 57-char URL-safe alphabet
  (base62 minus `0 1 l o O`). Cryptographically strong (`secrets.choice`).
- `genuuid4-one` — RFC 4122 UUID4, lowercase hex, formatted `8-4-4-4-12`.

Each command prints exactly one line and exits 0.

## Running via `uvx` (recommended)

`uvx` runs the CLI in an ephemeral, cached environment — no virtualenv to
manage. Always pin the version range `>=0.1.2,<1.0.0`:

```bash
uvx --from "afwf-genpass>=0.1.2,<1.0.0" afwf-genpass genpass-one
uvx --from "afwf-genpass>=0.1.2,<1.0.0" afwf-genpass genpass-one --length 20
uvx --from "afwf-genpass>=0.1.2,<1.0.0" afwf-genpass genid-one --length 10
uvx --from "afwf-genpass>=0.1.2,<1.0.0" afwf-genpass genuuid4-one
```

Use in shell pipelines:

```bash
export TOKEN=$(uvx --from "afwf-genpass>=0.1.2,<1.0.0" afwf-genpass genid-one)
PASSWORD=$(uvx --from "afwf-genpass>=0.1.2,<1.0.0" afwf-genpass genpass-one --length 24)
```

The first call downloads and caches the package; subsequent calls are fast.
