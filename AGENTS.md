> **Standing preferences apply to this repo.** The operator keeps them in
> cross-project files outside this repository, canonical wherever they and
> anything below disagree. They are not published, and an outside contributor
> does not need them: everything required to build, test and run this project is
> here.

# AGENTS.md — School Pickup System

Read [MISSION.md](docs/MISSION.md) first. The one thing to take from it before
touching anything: **this is a concept, not a proof of concept.** Aaron's
words, 2026-09-04. There is no running system here, and writing about it as
though there were is the specific way this repo can go wrong.

## What that means for a session working here

- **Do not describe the spikes as an application.** `src/car_line_v4.py` and
  the three under `src/car_line_alternatives/` are four attempts at one
  camera-to-number step. Nothing imports another; there is no entry point.
- **Write in the tense of what exists.** `DOCUMENTATION.md` has the standing
  rule and this repo is the easiest place on the drive to break it, because
  the README is written persuasively, in the future tense, about a system
  nobody has built.
- **The open questions are the valuable content.** Whether the school's
  current software has an API; whether synthetic keystrokes are an acceptable
  fallback; whether QR replaces OCR outright. Answering one is worth more than
  a fifth version of the reader.

## Running a spike

```bash
python -m venv venv && venv/Scripts/activate     # Windows
pip install -r requirements.txt
python src/car_line_v4.py                        # the most recent attempt
```

`easyocr` is the library the README settles on after trying the others; it
pulls a large model on first run. A camera is required for the capture path.

## Ports

None. Nothing here binds a port, and nothing here is declared in a launch
manifest, so it needs no slot. If a spike ever needs a local server, claim one
the way the standing `ESTATE_LAYOUT.md`, "Ports", says.
