#!/usr/bin/env python3
"""Generates a small synthetic dataset: places a cube in an Isaac Sim
scene, randomizes its pose and the scene lighting across N iterations,
and writes RGB images + bounding-box annotations to a local output
folder using Replicator's BasicWriter — a minimal, complete example of
the render-randomize-capture loop described in DEEP_DIVE.md.

A cube (not the Chapter 5 arm) is used here specifically to keep this
demo fast and its bounding box trivial to sanity-check by eye — the
loop structure is identical regardless of what object is being
randomized.

Run with Isaac Sim's own Python environment — see demo/README.md.
"""

import os

from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": True})

import omni.replicator.core as rep

NUM_FRAMES = 20
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def main():
    # A camera, positioned to look down at the origin where the
    # randomized cube will appear — this becomes the "render product"
    # annotators attach to below.
    camera = rep.create.camera(position=(0, 0, 3), look_at=(0, 0, 0))
    render_product = rep.create.render_product(camera, resolution=(640, 480))

    # The object being randomized. semantics=[("class", "cube")] tags it
    # so the bounding_box annotator knows to include it as a labeled
    # object rather than treating it as untagged background geometry.
    cube = rep.create.cube(semantics=[("class", "cube")], position=(0, 0, 0))

    # A light whose intensity and color get randomized each frame (see
    # DEEP_DIVE.md's domain randomization section) — without this, every
    # image would share identical lighting, one of the low-diversity
    # traps DEEP_DIVE.md warns about.
    light = rep.create.light(light_type="distant")

    # rep.randomizer.register wraps a function that mutates the scene
    # each time it's triggered — this is what actually varies pose and
    # lighting between captures, rather than every frame being an
    # identical render of the same static setup.
    def randomize_scene():
        with cube:
            rep.modify.pose(
                position=rep.distribution.uniform((-0.5, -0.5, 0), (0.5, 0.5, 0)),
                rotation=rep.distribution.uniform((0, 0, 0), (0, 0, 360)),
            )
        with light:
            rep.modify.attribute("intensity", rep.distribution.uniform(500, 3000))
            rep.modify.attribute(
                "color", rep.distribution.uniform((0.5, 0.5, 0.5), (1.0, 1.0, 1.0))
            )
        return cube.node

    rep.randomizer.register(randomize_scene)

    # rep.trigger.on_frame wires randomize_scene to run once before every
    # captured frame — this is what actually drives the re-randomize step
    # of the render-and-capture loop, rather than something the main loop
    # below needs to call directly.
    with rep.trigger.on_frame(num_frames=NUM_FRAMES):
        rep.randomizer.randomize_scene()

    # Attach annotators for the two label types this demo captures: the
    # plain image, and tight 2D bounding boxes around semantically
    # tagged objects (the cube, tagged above).
    rgb_annotator = rep.AnnotatorRegistry.get_annotator("rgb")
    rgb_annotator.attach(render_product)
    bbox_annotator = rep.AnnotatorRegistry.get_annotator("bounding_box_2d_tight")
    bbox_annotator.attach(render_product)

    # BasicWriter handles saving each captured frame's annotator outputs
    # to OUTPUT_DIR in a generic folder structure — see DEEP_DIVE.md for
    # when you'd reach for a format-specific writer (COCO/KITTI) instead.
    writer = rep.WriterRegistry.get("BasicWriter")
    writer.initialize(output_dir=OUTPUT_DIR, rgb=True, bounding_box_2d_tight=True)
    writer.attach([render_product])

    # rep.orchestrator.run() drives the render-and-capture loop from
    # DEEP_DIVE.md: for each of NUM_FRAMES (configured above via
    # rep.trigger.on_frame), it re-runs randomize_scene, renders, and
    # hands the result to the attached annotators/writer — one labeled
    # training example per iteration.
    rep.orchestrator.run()
    rep.orchestrator.wait_until_complete()

    print(f"Done. {NUM_FRAMES} frames written to: {OUTPUT_DIR}")
    simulation_app.close()


if __name__ == "__main__":
    main()
