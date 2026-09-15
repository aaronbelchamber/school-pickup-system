> **Standing preferences for this drive live outside this repo**, in
> `E:\project-hub\docs\standards\`. **List `*.md` there and read what is
> present** rather than working from a list here -- the set grows each time one
> of them outgrows its own size rule, so a list or a count written into this
> block would be a census of a moving directory. All of them apply and all are
> canonical: where any of them and anything below disagree, they win and the
> text below is the thing to fix. `PREFERENCES.md` is the entry point.
>
> If that path does not resolve -- a different machine, an unmounted drive --
> recover them rather than carrying on as though there were no standing
> preferences: `gh repo clone aaronbelchamber/project-hub`.

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
manifest -- so it does not appear on Central Project Hub's band map and does
not need a slot. If a spike ever needs a local server, take an even slot from
the `62000-62099` band and check `E:\.portfolio\band-claims.json` first;
`PREFERENCES.md` has the rules.
