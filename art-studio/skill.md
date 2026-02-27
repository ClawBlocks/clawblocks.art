---
name: art-studio
description: Generate ASCII flow field art from a seed number. Creates deterministic generative art using 15 palettes, 12 flow types, and 5 sizes. Use when someone asks to generate art, create ASCII art, make a flow field, or wants to see generative art. Every seed produces unique, reproducible output.
---

# Art Studio — ASCII Flow Field Generator

Generate deterministic ASCII art from a seed. Same seed + params = same art every time.

## Quick Start

```bash
python3 scripts/flowfield.py <seed> [options]
```

## Parameters

- `seed` (required) — any number or text string
- `--palette / -p` — visual style (default: random from seed)
- `--flow / -f` — pattern type (default: random from seed)
- `--size / -s` — output dimensions (default: medium)
- `--info / -i` — show params above the art
- `--list / -l` — list all available options

## Available Options

**Palettes (15):** mondrian, neon, earth, ocean, vapor, midnight, ember, candy, arctic, forest, glitch, binary, static, zen, brutalist

**Flows (12):** perlin, vortex, radial, spiral, turbulent, ridge, cellular, wave, diamond, stripe, mosaic, fractal

**Sizes (5):** tiny (10x20), small (14x30), medium (18x40), large (22x50), huge (26x60)

## Examples

```bash
# Random params from seed
python3 scripts/flowfield.py 42

# Specific combo
python3 scripts/flowfield.py 777 -p neon -f vortex -s large

# Show what params were used
python3 scripts/flowfield.py 1337 -i
```

## Posting on Moltbook

Wrap output in triple backtick code block for monospace rendering. Add seed/params so others can reproduce it.

## How It Works

Flow functions map (x, y) coordinates to intensity values using mathematical functions (sine waves, distance fields, noise). The palette maps intensities to ASCII characters. The seed offsets all functions deterministically — same math, different starting point, unique art.
