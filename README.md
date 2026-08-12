# IMO Tutor

A versioned, shareable IMO-level mathematics coaching workflow for ChatGPT.

## Goals

- One problem per working chat; archive the chat after durable notes are written.
- Do not reveal a solution before the student submits an attempt unless hints are explicitly requested.
- Review handwritten solutions for correctness, rigor, strategy, exposition, and extensibility.
- Persist original images, normalized mathematical text, and structured metadata to Google Drive.
- Retrieve old problems from a Google Sheets index by problem ID or fuzzy natural-language conditions.

## V0.1 design

V0.1 intentionally uses one installable ChatGPT Skill with eight internal workflow modules. This minimizes installation and coordination overhead while keeping the behavior modular.

```text
skills/imo-tutor/
  SKILL.md
  workflows/
  references/
```

Google Drive is the student's private data store. This public repository contains workflow definitions and schemas only; it must not contain student solutions, private Drive IDs, or credentials.

## Current workflow

1. Upload a new problem image/text.
2. Classify it, rate difficulty on the AoPS 1–10 scale, tag it, and persist the problem record.
3. Keep the solution locked. Provide H1–H6 hints only when requested.
4. Upload the student's handwritten solution.
5. Preserve the original image, transcribe to Markdown/LaTeX, review the proof, and record structured error tags.
6. Optionally compare with a reference solution.
7. Compile a durable note and update Google Sheets indexes.
8. Archive the working chat. Later, open a new chat and retrieve by ID or natural language, e.g. `最近做错的2道几何题`.

## Development

Run deterministic contract tests with:

```bash
python -m unittest discover -s tests
```

Behavioral eval cases live under `evals/` and are used during manual/agent testing.

See `project/SETUP.md` for installation and Google Drive setup.
