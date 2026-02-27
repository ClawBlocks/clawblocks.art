#!/usr/bin/env python3
"""
ASCII Flow Field Generator
Deterministic generative art from a seed number.
Same seed + params = same output every time.
"""

import math
import sys
import hashlib

# ── Palettes ─────────────────────────────────────────────
# Each palette maps flow intensity (0.0-1.0) to characters
# Ordered light → dark
PALETTES = {
    "mondrian":  list("   ..::|##"),
    "neon":      list("  .*+=#%@&"),
    "earth":     list("  .,:;oO#@"),
    "ocean":     list("  ~-=+*#%@"),
    "vapor":     list("  ._-~=+*#"),
    "midnight":  list("  .'`-~=*#"),
    "ember":     list("  .,-~:;*#"),
    "candy":     list("  .,oO0@#&"),
    "arctic":    list("  ._-=+*#@"),
    "forest":    list("  .,;:!|#@"),
    "glitch":    list("  _/|\\-=+#"),
    "binary":    list("     01#@@"),
    "static":    list("  .:-=+*#%"),
    "zen":       list("  . , - ~ "),
    "brutalist": list("  .|#@@@@#"),
}

# ── Flow Types ───────────────────────────────────────────

def perlin_flow(x, y, seed_val):
    """Smooth organic flow using layered sine waves"""
    s = seed_val
    v = (math.sin(x * 0.3 + s) * math.cos(y * 0.2 + s * 0.7) +
         math.sin(x * 0.1 - y * 0.15 + s * 1.3) * 0.5 +
         math.cos(x * 0.05 + y * 0.08 + s * 0.3) * 0.3)
    return (v + 2) / 4  # normalize to 0-1

def vortex_flow(x, y, seed_val):
    """Spiraling inward toward center(s)"""
    cx = 20 + math.sin(seed_val) * 8
    cy = 10 + math.cos(seed_val) * 5
    dx, dy = x - cx, y - cy
    dist = math.sqrt(dx*dx + dy*dy) + 0.1
    angle = math.atan2(dy, dx) + dist * 0.3 + seed_val
    v = (math.sin(angle * 2 + dist * 0.5) + 1) / 2
    return v

def radial_flow(x, y, seed_val):
    """Radiating outward from center"""
    cx = 20 + math.sin(seed_val * 1.7) * 10
    cy = 10 + math.cos(seed_val * 2.3) * 5
    dist = math.sqrt((x-cx)**2 + (y-cy)**2)
    v = (math.sin(dist * 0.4 + seed_val) + 1) / 2
    return v

def spiral_flow(x, y, seed_val):
    """Logarithmic spiral pattern"""
    cx, cy = 20, 10
    dx, dy = x - cx, y - cy
    angle = math.atan2(dy, dx)
    dist = math.sqrt(dx*dx + dy*dy)
    v = (math.sin(angle * 3 + math.log(dist + 1) * 4 + seed_val) + 1) / 2
    return v

def turbulent_flow(x, y, seed_val):
    """Chaotic multi-frequency interference"""
    v = 0
    for i in range(1, 5):
        freq = 0.1 * i + seed_val * 0.01
        phase = seed_val * i * 0.7
        v += math.sin(x * freq + phase) * math.cos(y * freq * 0.8 + phase) / i
    return (v + 2) / 4

def ridge_flow(x, y, seed_val):
    """Sharp ridges like mountain topography"""
    v = perlin_flow(x, y, seed_val)
    return abs(v * 2 - 1)  # fold to create ridges

def cellular_flow(x, y, seed_val):
    """Cell-like regions with borders"""
    min_dist = 999
    for i in range(6):
        h = hashlib.md5(f"{seed_val}-{i}".encode()).hexdigest()
        cx = int(h[:4], 16) % 40
        cy = int(h[4:8], 16) % 20
        dist = math.sqrt((x-cx)**2 + (y-cy)**2)
        min_dist = min(min_dist, dist)
    return min(min_dist / 12, 1.0)

def wave_flow(x, y, seed_val):
    """Interference pattern from multiple wave sources"""
    v = 0
    for i in range(3):
        h = hashlib.md5(f"{seed_val}-wave-{i}".encode()).hexdigest()
        cx = int(h[:4], 16) % 40
        cy = int(h[4:8], 16) % 20
        dist = math.sqrt((x-cx)**2 + (y-cy)**2)
        v += math.sin(dist * 0.8 + seed_val * 0.5)
    return (v / 3 + 1) / 2

def diamond_flow(x, y, seed_val):
    """Diamond/manhattan distance pattern"""
    cx = 20 + math.sin(seed_val) * 8
    cy = 10 + math.cos(seed_val) * 5
    dist = abs(x - cx) + abs(y - cy)
    v = (math.sin(dist * 0.3 + seed_val) + 1) / 2
    return v

def stripe_flow(x, y, seed_val):
    """Angled stripes with variable width"""
    angle = seed_val * 0.7
    proj = x * math.cos(angle) + y * math.sin(angle)
    width = 3 + math.sin(seed_val * 1.3) * 2
    v = (math.sin(proj / width * math.pi) + 1) / 2
    return v

def mosaic_flow(x, y, seed_val):
    """Blocky mosaic tiles"""
    tile_size = 3 + int(seed_val) % 4
    tx = int(x / tile_size)
    ty = int(y / tile_size)
    h = hashlib.md5(f"{seed_val}-{tx}-{ty}".encode()).hexdigest()
    return int(h[:2], 16) / 255

def fractal_flow(x, y, seed_val):
    """Simple fractal-like recursive pattern"""
    v = 0
    scale = 1.0
    px, py = x + seed_val, y + seed_val * 0.7
    for _ in range(5):
        v += math.sin(px * scale) * math.cos(py * scale) / scale
        scale *= 2.1
        px += seed_val * 0.3
        py += seed_val * 0.5
    return (v + 2) / 4

FLOWS = {
    "perlin": perlin_flow,
    "vortex": vortex_flow,
    "radial": radial_flow,
    "spiral": spiral_flow,
    "turbulent": turbulent_flow,
    "ridge": ridge_flow,
    "cellular": cellular_flow,
    "wave": wave_flow,
    "diamond": diamond_flow,
    "stripe": stripe_flow,
    "mosaic": mosaic_flow,
    "fractal": fractal_flow,
}

# ── Sizes ────────────────────────────────────────────────
SIZES = {
    "tiny":   (10, 20),
    "small":  (14, 30),
    "medium": (18, 40),
    "large":  (22, 50),
    "huge":   (26, 60),
}

# ── Generator ────────────────────────────────────────────

def generate(seed, palette_name="earth", flow_name="perlin", size_name="medium"):
    # Resolve params
    seed_val = int(hashlib.md5(str(seed).encode()).hexdigest()[:8], 16) / 1e8
    
    palette = PALETTES.get(palette_name, PALETTES["earth"])
    flow_fn = FLOWS.get(flow_name, FLOWS["perlin"])
    rows, cols = SIZES.get(size_name, SIZES["medium"])
    
    lines = []
    for y in range(rows):
        line = ""
        for x in range(cols):
            v = flow_fn(x, y, seed_val)
            v = max(0, min(1, v))  # clamp
            idx = int(v * (len(palette) - 1))
            line += palette[idx]
        lines.append(line)
    
    return "\n".join(lines)

def random_from_seed(seed):
    """Deterministically pick random params from seed"""
    h = hashlib.md5(str(seed).encode()).hexdigest()
    palettes = list(PALETTES.keys())
    flows = list(FLOWS.keys())
    p = palettes[int(h[:4], 16) % len(palettes)]
    f = flows[int(h[4:8], 16) % len(flows)]
    return p, f

# ── CLI ──────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="ASCII Flow Field Generator")
    parser.add_argument("seed", type=str, help="Seed (number or text)")
    parser.add_argument("--palette", "-p", default=None, choices=list(PALETTES.keys()),
                        help="Color palette (default: random from seed)")
    parser.add_argument("--flow", "-f", default=None, choices=list(FLOWS.keys()),
                        help="Flow type (default: random from seed)")
    parser.add_argument("--size", "-s", default="medium", choices=list(SIZES.keys()),
                        help="Output size (default: medium)")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List all palettes and flows")
    parser.add_argument("--info", "-i", action="store_true",
                        help="Show params alongside art")
    
    args = parser.parse_args()
    
    if args.list:
        print("PALETTES:", ", ".join(PALETTES.keys()))
        print("FLOWS:", ", ".join(FLOWS.keys()))
        print("SIZES:", ", ".join(SIZES.keys()))
        return
    
    palette = args.palette
    flow = args.flow
    
    if palette is None or flow is None:
        rp, rf = random_from_seed(args.seed)
        palette = palette or rp
        flow = flow or rf
    
    art = generate(args.seed, palette, flow, args.size)
    
    if args.info:
        print(f"Seed: {args.seed} | Palette: {palette} | Flow: {flow} | Size: {args.size}")
        print("---")
    
    print(art)

if __name__ == "__main__":
    main()
