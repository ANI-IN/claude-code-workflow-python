# Exercise 1: Explore and Plan (in Plan Mode)

**Goal:** Let Claude read the codebase and propose an approach for adding WebP conversion, before a single line of code is written. This is the Explore and Plan half of the loop, and it is the cheapest place to catch problems.

## Background

Plan Mode lets Claude read your code but not edit it. Claude gathers context and returns a plan of action that you can review and measure against your own success criteria. Because nothing is written yet, this is the best moment to course-correct.

You can also run the Explore subagent outside Plan Mode when you only want a general summary of a codebase without intending to change it.

## Steps

1. Activate your virtual environment, then start Claude Code from the project root:

   ```bash
   source .venv/bin/activate
   claude
   ```

2. Enter Plan Mode. Press **Shift + Tab** until the footer reads "plan mode on".

3. Ask Claude to explore and plan the feature:

   ```
   I need to add WebP conversion to our snapshot pipeline. Figure out where
   in the pipeline it should happen, whether we need a new dependency, and
   how to approach it. Keep all endpoints TLS-only per our conventions.
   ```

4. Read the plan Claude returns. Decide whether it meets your criteria. If anything is off, such as the wrong location, a missing step, or no test coverage, ask for a revision now, before any code is written. For example:

   ```
   Revise: keep the original frame too, and add a test that asserts the
   output is valid WebP.
   ```

5. Do not approve yet. Stop once you have a plan you are happy with. You will approve and implement it in Exercise 2.

## What to observe

- In Plan Mode, Claude reads files but never edits them. Check that the footer reads "plan mode on" before you send the prompt.
- Claude will likely read `src/snapshot_service/pipeline/`, `src/snapshot_service/api/`, `pyproject.toml`, and the tests, then propose doing the conversion inside `src/snapshot_service/pipeline/image_pipeline.py`, where raw frames are already processed.
- A good plan answers the dependency question with evidence. Pillow is already installed, but only as a `dev` dependency for the tests. If the pipeline uses it at runtime, the plan should move it into the runtime `dependencies` list in `pyproject.toml`.
- The plan is a proposal, not a commitment. Requesting a revision here costs nothing, because no code exists yet.

## Look at the code

Open `src/snapshot_service/pipeline/image_pipeline.py` and study the starting state. Notice two things:

- The `FrameFormat` type allows `"webp"`, yet the code is marked as not implemented yet.
- Calling `process_frame(frame, output_format="webp")` raises `NotImplementedError("WebP conversion not implemented yet")`.

These are intentional. They describe the "before" state of the exercise and tell you exactly what the feature needs to do. Read the `FEATURE TASK` and `Success criteria` sections of the module docstring. They are your target for Exercise 2. Do not change anything yet.

## Learning outcome

You practiced the Explore and Plan half of the loop. You saw that Plan Mode keeps Claude read-only while it gathers context, and that reviewing and revising the plan, including its dependency choices, is the cheapest way to steer direction before any code exists.
