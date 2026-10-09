# Exercise 2: Code (Against the Plan)

**Goal:** Approve the plan from Exercise 1 and let Claude implement WebP conversion, using the test suite as the source of truth. This is the Code step of the loop.

## Background

Once the plan looks right, you approve it and Claude works through the steps. Claude does its best to troubleshoot before it considers the plan finished, but sometimes you will need to step in. Because you planned first, you also have the context of how you got here, which helps guide Claude's next decisions.

Three things make this phase smoother, and all of them are already set up in this project:

- **Success criteria.** The plan should state what "correct" looks like. Here it is concrete: the pipeline returns WebP bytes, the original frame is preserved, and the tests pass.
- **Tools that let Claude check its own work.** `pytest`, `ruff`, and `mypy` give fast, objective feedback, so there is less back-and-forth with you.
- **A test suite as the source of truth.** `tests/test_image_pipeline.py` defines the feature, so Claude troubleshoots against real feedback instead of guessing. Make sure tests are reliable before you trust them, to avoid false positives.

## Steps

1. When the plan looks right, **Approve** it. Claude begins working through the steps. You can let it auto-accept file edits or confirm each one.

2. After the change, run the checks:

   ```bash
   pytest
   ruff check .
   ruff format --check .
   mypy
   ```

3. Read the results. If a test fails, let Claude troubleshoot against the failing assertion rather than guessing. The failing test tells Claude precisely what "correct" means.

4. If Claude keeps running into the same issue, ask it to save the solution to `CLAUDE.md`, so it does not rediscover the fix next time.

5. Stop when every check passes and you have reviewed the change yourself. You will commit in Exercise 3.

## What to observe

- Approving the plan is the moment Claude switches from read-only exploration to making edits. You chose when that happened.
- `test_webp_output_has_riff_webp_magic_bytes` is written to fail until the feature exists. Watch it move from failing to passing as the implementation lands.
- A test that fails for the right reason is useful. It is the signal that guides the implementation.
- If the plan included your revision, Claude also adds a stronger test, for example one that opens the output with Pillow and checks that it really is a WebP image of the same size.

## Look at the code

Open the tests before you run anything:

- `tests/conftest.py` builds `jpeg_frame`, a small real JPEG image, with Pillow. Using a real image means a real encoder can be tested, not only a byte pattern.
- `tests/test_image_pipeline.py` checks that WebP output starts with `RIFF`, followed by a 4-byte size and then `WEBP`. Every WebP file starts this way.
- The module docstring says plainly that the WebP test is written to fail until the feature is implemented.

The failing WebP test is not a defect. It is the source of truth that defines the feature. Make it pass by implementing the feature, not by weakening the test.

Then open `src/snapshot_service/pipeline/image_pipeline.py` again and compare the implementation against its `Success criteria`. The feature is done when the pipeline can return WebP bytes, the original frame is still available, and all checks pass.

## Learning outcome

You practiced the Code step. You approved a reviewed plan, implemented it against clear success criteria, and used a reliable test suite, plus a linter and type checker, so troubleshooting was grounded in real feedback rather than guesswork.
