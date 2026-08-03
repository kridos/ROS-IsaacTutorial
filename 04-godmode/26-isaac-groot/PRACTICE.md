# Practice: Isaac GR00T

1. **Try different instructions.** Run `groot_inference_demo.py` with
   several different `language_instruction` strings against the same
   `sample_scene.jpg`, and compare the resulting actions — do
   meaningfully different instructions produce meaningfully different
   predicted actions?

2. **Try different images.** Keep the instruction fixed and swap in 2-3
   different sample images (different object positions/scenes) — confirm
   the predicted action changes with the visual input, evidence the
   model is actually attending to the image, not just the text.

3. **Compare against a from-scratch policy.** Write a short comparison
   note: for a task as narrow as this demo's single inference step, list
   what Chapter 24's from-scratch RL approach would have needed
   (environment definition, reward design, training time) that this
   chapter's pre-trained-model approach skips — make DEEP_DIVE.md's
   foundation-model trade-off concrete in your own words.

4. **Read the action output's structure.** Print the *type* and shape of
   every key in the returned action dict (not just values), and cross-
   reference against your specific robot's actual joint count/action
   space — identify what an adaptation layer mapping this model's output
   onto a specific robot would need to do.

5. **Stretch:** research (via NVIDIA's current GR00T documentation —
   this changes fast) what a minimal fine-tuning dataset actually needs
   to look like for your chosen embodiment, and write a short plan
   (not code) for what data you'd need to collect to fine-tune GR00T for
   Chapter 28's mobile manipulator's actual arm.
