#!/usr/bin/env python3
"""Render reproducible SVG evidence from one local, unmodified trajectory clip.

Standard library only. Run from any directory. See docs/crowd-evidence.md for
provenance, deterministic subsampling, and interpretation boundaries.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
from html import escape
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = (
    ROOT.parent / "Cambridge crowdflow ai" / "crowdflow-ai-package" / "data"
    / "TopView_trajectories" / "TopView_1A.txt"
)
WIDTH, HEIGHT = 1440, 1000
PAPER = "#101b1c"
INK = "#e8eee4"
MUTED = "#99aaa7"
ACCENT = "#dfff00"
MAX_TRAJECTORIES = 160
MAX_POINTS = 80
CELL = 0.25


@dataclass(frozen=True, slots=True)
class Observation:
    frame: int
    x: float
    y: float


def evenly_spaced_indices(length: int, limit: int) -> list[int]:
    """Keep both endpoints; select nearest evenly spaced indices (half up)."""
    if length <= limit:
        return list(range(length))
    return [math.floor(i * (length - 1) / (limit - 1) + 0.5) for i in range(limit)]


def read_clip(source: Path) -> tuple[dict[int, list[Observation]], str, int]:
    tracks: dict[int, list[Observation]] = defaultdict(list)
    raw = source.read_bytes()
    count = 0
    for line_no, line in enumerate(raw.decode("utf-8-sig").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split()
        if len(fields) != 9:
            raise ValueError(f"Line {line_no}: expected 9 columns, found {len(fields)}")
        # Source header: id frame x/m y/m z/m id_global t/s x_RGF y_RGF.
        # In particular, x/y are columns 3/4; frame is not a position.
        person_id, frame = int(fields[0]), int(fields[1])
        x, y, z = map(float, fields[2:5])
        global_id = int(fields[5])
        t, x_rgf, y_rgf = map(float, fields[6:9])
        if not all(math.isfinite(n) for n in (x, y, z, t, x_rgf, y_rgf)):
            raise ValueError(f"Line {line_no}: non-finite numeric value")
        if person_id < 0 or frame < 0 or global_id < 0:
            raise ValueError(f"Line {line_no}: negative identifier or frame")
        tracks[person_id].append(Observation(frame, x, y))
        count += 1
    if not tracks:
        raise ValueError("The source clip has no observations")
    for person_id, points in tracks.items():
        points.sort(key=lambda p: p.frame)
        if any(a.frame == b.frame for a, b in zip(points, points[1:])):
            raise ValueError(f"ID {person_id} has duplicate frame observations")
    return dict(tracks), hashlib.sha256(raw).hexdigest(), count


class Plot:
    """One uniform metre-to-pixel scale; positive y points upwards."""

    def __init__(self, tracks: dict[int, list[Observation]]) -> None:
        points = (point for track in tracks.values() for point in track)
        first = next(points)
        x_min = x_max = first.x
        y_min = y_max = first.y
        for point in points:
            x_min, x_max = min(x_min, point.x), max(x_max, point.x)
            y_min, y_max = min(y_min, point.y), max(y_max, point.y)
        self.observed_bounds = (x_min, x_max, y_min, y_max)
        self.x_min, self.x_max = math.floor(x_min), math.ceil(x_max)
        self.y_min, self.y_max = math.floor(y_min), math.ceil(y_max)
        available_width, available_height = 1200, 720
        self.scale = min(
            available_width / (self.x_max - self.x_min),
            available_height / (self.y_max - self.y_min),
        )
        self.width = (self.x_max - self.x_min) * self.scale
        self.height = (self.y_max - self.y_min) * self.scale
        self.left = 136 + (available_width - self.width) / 2
        self.top = 200 + (available_height - self.height) / 2

    def xy(self, x: float, y: float) -> tuple[float, float]:
        return (
            self.left + (x - self.x_min) * self.scale,
            self.top + (self.y_max - y) * self.scale,
        )


def txt(x: float, y: float, label: str, size: int = 16, color: str = MUTED,
        extra: str = "") -> str:
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" '
            f'fill="{color}" {extra}>{escape(label)}</text>')


def begin(title: str, description: str) -> list[str]:
    return [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="{WIDTH}" height="{HEIGHT}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">{escape(description)}</desc>',
        '<style>text{font-family:Arial,Helvetica,sans-serif} '
        '.mono{font-family:Consolas,monospace} .grid{stroke:#7f9994;stroke-opacity:.13;stroke-width:1}</style>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{PAPER}"/>',
        '<path d="M88 42h1264" stroke="#829994" stroke-opacity=".25"/>',
        txt(88, 76, "CROWDFLOW AI / OBSERVED MOVEMENT", 13, ACCENT,
            'letter-spacing="2"'),
    ]


def axes(plot: Plot) -> list[str]:
    parts = []
    for x in range(plot.x_min, plot.x_max + 1):
        px, bottom = plot.xy(x, plot.y_min)
        _, top = plot.xy(x, plot.y_max)
        parts += [
            f'<path class="grid" d="M{px:.2f} {top:.2f}V{bottom:.2f}"/>',
            txt(px, bottom + 25, str(x), 14, MUTED, 'text-anchor="middle" class="mono"'),
        ]
    for y in range(plot.y_min, plot.y_max + 1):
        left, py = plot.xy(plot.x_min, y)
        right, _ = plot.xy(plot.x_max, y)
        parts += [
            f'<path class="grid" d="M{left:.2f} {py:.2f}H{right:.2f}"/>',
            txt(left - 20, py + 5, str(y), 14, MUTED,
                'text-anchor="end" class="mono"'),
        ]
    parts += [
        f'<rect x="{plot.left:.2f}" y="{plot.top:.2f}" width="{plot.width:.2f}" '
        f'height="{plot.height:.2f}" fill="none" stroke="#829994" stroke-opacity=".34"/>',
        txt(plot.left, plot.top - 20, "y / m", 13),
        txt(plot.left + plot.width, plot.top + plot.height + 25, "x / m", 13,
            MUTED, 'text-anchor="end" transform="translate(0 25)"'),
    ]
    return parts


def write_paths(output: Path, tracks: dict[int, list[Observation]], plot: Plot,
                count: int) -> tuple[list[int], int]:
    ids = sorted(tracks)
    selected = [ids[i] for i in evenly_spaced_indices(len(ids), MAX_TRAJECTORIES)]
    title = "Paths through one clip."
    desc = (
        f"TopView_1A: {len(selected)} of {len(ids)} track IDs, selected at evenly spaced "
        f"indices from ascending ID order. Up to {MAX_POINTS} frame-ordered positions "
        "per displayed track. Local x and y coordinates in metres use an equal scale. "
        "Green dots mark the first recorded position of each displayed track, not entry points."
    )
    parts = begin(title, desc)
    parts += [
        txt(88, 125, title, 39, INK),
        txt(88, 159, f"TOPVIEW_1A   /   {len(selected)} OF {len(ids)} TRACK IDs   /   EQUAL-SCALE LOCAL COORDINATES", 14),
    ]
    parts += axes(plot)
    parts.append('<g fill="none" stroke="#e8eee4" stroke-opacity=".29" stroke-width="1.45" stroke-linecap="round" stroke-linejoin="round">')
    starts = []
    plotted_points = 0
    for person_id in selected:
        track = tracks[person_id]
        sampled = [track[i] for i in evenly_spaced_indices(len(track), MAX_POINTS)]
        coords = [plot.xy(point.x, point.y) for point in sampled]
        plotted_points += len(coords)
        geometry = " ".join(f"{x:.2f},{y:.2f}" for x, y in coords)
        parts.append(f'<polyline points="{geometry}"><title>Track ID {person_id}: '
                     f'{len(sampled)} of {len(track)} observations</title></polyline>')
        starts.append(coords[0])
    parts.append('</g><g fill="#dfff00" fill-opacity=".74">')
    parts += [f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.5"/>' for x, y in starts]
    parts += ['</g>',
              '<circle cx="92" cy="981" r="3" fill="#dfff00"/>',
              txt(105, 986, "First recorded position", 13),
              txt(1352, 986, f"Deterministic subset / max. {MAX_POINTS} positions per track / {count:,} source rows", 13,
                  MUTED, 'text-anchor="end"'), '</svg>']
    output.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return selected, plotted_points


def color_between(start: tuple[int, int, int], end: tuple[int, int, int], value: float) -> str:
    return "#" + "".join(f"{round(a + (b - a) * value):02x}" for a, b in zip(start, end))


def write_frequency(output: Path, tracks: dict[int, list[Observation]], plot: Plot,
                    count: int) -> tuple[int, int]:
    bins: Counter[tuple[int, int]] = Counter()
    for track in tracks.values():
        for point in track:
            ix = math.floor((point.x - plot.x_min) / CELL)
            iy = math.floor((point.y - plot.y_min) / CELL)
            bins[(ix, iy)] += 1
    peak = max(bins.values())
    title = "Where recorded positions accumulate."
    desc = (
        f"TopView_1A: all {count:,} source positions from {len(tracks)} track IDs, "
        f"counted in {CELL:g} by {CELL:g} metre square cells. Each cell's relative sample "
        "frequency is its count divided by all source positions. Colour is linear from zero "
        f"to the largest cell's relative frequency. The largest cell contains {peak:,} observations "
        f"({peak / count:.4%}). This is accumulated sample frequency, not instantaneous occupancy, "
        "calibrated pedestrian density, crowd risk, or a distinct-person count."
    )
    parts = begin(title, desc)
    parts += [
        txt(88, 125, title, 39, INK),
        txt(88, 159, f"TOPVIEW_1A   /   ALL {count:,} POSITIONS   /   0.25 m SQUARE CELLS", 14),
    ]
    parts.append('<g>')
    for (ix, iy), cell_count in sorted(bins.items()):
        x, y = plot.xy(plot.x_min + ix * CELL, plot.y_min + (iy + 1) * CELL)
        side = CELL * plot.scale
        intensity = cell_count / peak
        color = color_between((21, 46, 47), (223, 255, 0), intensity)
        parts.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{side:.2f}" height="{side:.2f}" '
            f'fill="{color}" stroke="{PAPER}" stroke-width=".7">'
            f'<title>Cell x {plot.x_min + ix * CELL:.2f} to {plot.x_min + (ix + 1) * CELL:.2f} m, '
            f'y {plot.y_min + iy * CELL:.2f} to {plot.y_min + (iy + 1) * CELL:.2f} m: '
            f'{cell_count:,} / {count:,} positions ({cell_count / count:.4%})</title></rect>'
        )
    parts.append('</g>')
    parts += axes(plot)
    # Relative frequency and colour both vary linearly from zero to the maximum.
    stops = []
    for i in range(21):
        value = i / 20
        stops.append(f'<stop offset="{value:.3f}" stop-color="{color_between((21, 46, 47), (223, 255, 0), value)}"/>')
    parts += [
        '<defs><linearGradient id="frequency">' + ''.join(stops) + '</linearGradient></defs>',
        txt(88, 986, "Relative sample frequency / linear colour scale / not calibrated occupancy", 13),
        '<rect x="1005" y="966" width="210" height="9" fill="url(#frequency)"/>',
        txt(990, 987, "0", 12, MUTED, 'text-anchor="end" class="mono"'),
        txt(1352, 987, f"max {peak / count:.2%}", 12, MUTED, 'text-anchor="end" class="mono"'),
        '</svg>',
    ]
    output.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return len(bins), peak


def write_documentation(source: Path, sha256: str, tracks: dict[int, list[Observation]],
                        plot: Plot, count: int, selected: list[int], plotted_points: int,
                        occupied_cells: int, peak: int) -> None:
    all_frames = [point.frame for track in tracks.values() for point in track]
    low, high = min(all_frames), max(all_frames)
    observed = plot.observed_bounds
    source_reference = source.as_posix()
    try:
        source_reference = "../" + source.relative_to(ROOT.parent).as_posix()
    except ValueError:
        pass
    document = f'''# CrowdFlow SVG evidence

Generated by `scripts/render_crowd_evidence.py` with Python standard-library modules only.
No source data are edited, copied into the published website, or inferred by an AI model.

## Source

- Clip: **TopView_1A only**.
- Local source: `{source_reference}`.
- SHA-256: `{sha256}`.
- Header columns, parsed in order: `id frame x/m y/m z/m id_global t/s x_RGF y_RGF`.
- The header identifies x/y as local metres, x_RGF/y_RGF as EPSG:2154 metres, and recording at 30 fps.
- There are **{count:,} position records** and **{len(tracks):,} local track IDs**.
- Observed frame range: **{low}–{high}**, spanning **{(high - low) / 30:.3f} seconds** between the endpoint frames. This does not assert continuously complete detection.
- Observed local x range: **{observed[0]:.3f}–{observed[1]:.3f} m**; y range: **{observed[2]:.3f}–{observed[3]:.3f} m**.
- Finite numerical values, exactly nine columns, and no repeated frames within each local ID are checked. IDs are not assumed to identify unique people across clips.

## Geometry

Both SVGs use a 1440 × 1000 viewBox and the same local x/y coordinate system.
The same pixel-per-metre scale is applied to both axes, preserving spatial proportions.
Positive y is upwards. The axes are rounded outwards to integer metres; no spatial measurements are stretched, cropped, smoothed or interpolated into a field.
No site boundary or obstacle layout is inferred from the point extents.

## `crowd-paths.svg`

1. Sort all {len(tracks)} local IDs in ascending numeric order.
2. Choose {len(selected)} indices evenly across that order, including the first and last ID. For a list of length `n` and limit `k`, index `i` is `floor(i * (n - 1) / (k - 1) + 0.5)` for `i = 0…k-1`. Lists shorter than the limit are kept in full.
3. Within each chosen ID, sort records by frame and apply the same endpoint-preserving rule to select **at most {MAX_POINTS} observed positions**.
4. Join those positions in order with straight SVG polyline segments. The result contains **{plotted_points:,} plotted positions**. Straight segments are visual connections, not measurements between samples; frame gaps are not reconstructed.
5. A green dot marks each track's **first recorded position**. It does not necessarily mark a physical entrance or the beginning of a person's journey.

This subset is deterministic, not a random or statistically representative sample. IDs with few positions are not excluded. The subset is for legibility, not for population or directional-flow estimation.

Selected IDs:

`{", ".join(map(str, selected))}`

## `crowd-density.svg`

The filename is retained for the portfolio's view-switching interface. The chart itself is labelled **relative sample frequency** rather than density.

- Every one of the {count:,} source positions contributes to one **{CELL:g} m × {CELL:g} m square cell** using `floor((coordinate - axis_min) / cell_size)`.
- The cell value is `cell_position_count / {count}`. There are **{occupied_cells:,} nonempty cells**.
- The largest cell contains **{peak:,} records**, or **{peak / count:.4%}** of all positions in this clip.
- Colour intensity is `cell_position_count / maximum_cell_position_count`. This linear scale is disclosed in the legend. Cell tooltips retain the exact count and relative frequency.
- Empty cells retain the dark background. Grid lines mark 1 m intervals; rendered cells are 0.25 m squares.

The figure aggregates positions across the clip. A person seen for longer contributes more records. Occlusion, detection coverage, frame gaps and track fragmentation can change the pattern. It is **not instantaneous occupancy, unique-person frequency, calibrated people/m², exposure-normalized spatial probability, speed, congestion, crowd risk or evidence of an intervention's effect**.

The SVG assets are derived figures; the source dataset is not republished. Check the original dataset's license and attribution requirements before any additional redistribution. The clip header provides measurement definitions, not a full calibration or completeness assessment.

## Reproduce

Run from the repository root with Python 3.10+:

```console
python scripts/render_crowd_evidence.py
```

The command deterministically rewrites only `assets/portfolio/crowd-paths.svg`, `assets/portfolio/crowd-density.svg` and this documentation file. The default source stays outside the repository. An optional `--source` argument allows the same-format clip location to be specified; the documentation records the actual file hash.
'''
    (ROOT / "docs" / "crowd-evidence.md").write_text(document, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    args = parser.parse_args()
    source = args.source.resolve()
    if source.name != "TopView_1A.txt":
        parser.error("These portfolio figures are intentionally restricted to TopView_1A.txt")
    tracks, sha256, count = read_clip(source)
    plot = Plot(tracks)
    output = ROOT / "assets" / "portfolio"
    output.mkdir(parents=True, exist_ok=True)
    (ROOT / "docs").mkdir(parents=True, exist_ok=True)
    selected, plotted_points = write_paths(output / "crowd-paths.svg", tracks, plot, count)
    occupied_cells, peak = write_frequency(output / "crowd-density.svg", tracks, plot, count)
    write_documentation(source, sha256, tracks, plot, count, selected, plotted_points,
                        occupied_cells, peak)
    print(f"Rendered {len(selected)} / {len(tracks)} tracks; all {count:,} frequency samples.")
    print(f"SHA-256 {sha256}")


if __name__ == "__main__":
    main()
