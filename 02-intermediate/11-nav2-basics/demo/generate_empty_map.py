#!/usr/bin/env python3
"""Generates a trivial 10x10m all-free-space map (empty_map.pgm +
empty_map.yaml) so this chapter's demo has a map to load without
requiring a separate SLAM mapping session first.

A real map normally comes from driving the robot around with
slam_toolbox and saving the result — this script exists purely so
nav2_params.yaml's map_server has something valid to load for a first
look at Nav2, matching the empty Gazebo world from Chapter 7/9 (no
obstacles to map anyway).
"""

import os

# Map size: 10m x 10m at 0.05m/pixel resolution = 200x200 pixels.
RESOLUTION = 0.05
WIDTH_M = 10.0
HEIGHT_M = 10.0
WIDTH_PX = int(WIDTH_M / RESOLUTION)
HEIGHT_PX = int(HEIGHT_M / RESOLUTION)

OUTPUT_DIR = os.path.dirname(__file__)
PGM_PATH = os.path.join(OUTPUT_DIR, "empty_map.pgm")
YAML_PATH = os.path.join(OUTPUT_DIR, "empty_map.yaml")


def write_pgm():
    # PGM (Portable Gray Map) is a simple, plain-text-header image format
    # Nav2's map_server understands directly — no image library needed to
    # produce one. Pixel value 254 = free space (map_server's "occupied
    # if below free_thresh" convention, matching the .yaml below), 0
    # would mean occupied, 205 would mean unknown.
    with open(PGM_PATH, "wb") as f:
        header = f"P5\n{WIDTH_PX} {HEIGHT_PX}\n255\n"
        f.write(header.encode("ascii"))
        f.write(bytes([254]) * (WIDTH_PX * HEIGHT_PX))


def write_yaml():
    # origin: bottom-left corner of the image in map coordinates, in
    # meters — centered here so (0,0) (where the robot spawns, per
    # Chapter 7/9's launch files) lands in the middle of the map.
    origin_x = -WIDTH_M / 2.0
    origin_y = -HEIGHT_M / 2.0
    content = f"""image: empty_map.pgm
resolution: {RESOLUTION}
origin: [{origin_x}, {origin_y}, 0.0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
"""
    with open(YAML_PATH, "w") as f:
        f.write(content)


def main():
    write_pgm()
    write_yaml()
    print(f"Wrote {PGM_PATH} ({WIDTH_PX}x{HEIGHT_PX}px) and {YAML_PATH}")


if __name__ == "__main__":
    main()
