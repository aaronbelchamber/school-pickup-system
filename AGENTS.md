> **Standing preferences for this drive live outside this repo.** They are
> the files in `E:\project-hub\docs\standards\`, and all of them apply. Read them before
> working here. They are canonical: where any of them and anything below
> disagree, they win and the text below is the thing to fix.
>
> | File | Covers |
> |---|---|
> | `PREFERENCES.md` | *what* to build for and against -- the port bands, launching processes without a window, URL hygiene, hosting and cloud access, destructive automation |
> | `PRACTICES.md` | *how* to build it -- applicable skills, script placement, file size, planning before editing, who owns what across projects, design systems, database schema design, issue tracking |
> | `VERIFICATION.md` | proving the work is right -- the cheapest sufficient check, exercising a claim rather than reading one, breaking what a test guards to prove it fails, reporting *did not run* as its own outcome, stop conditions, self-review, when CI earns its cost |
> | `COLLABORATION.md` | how to do either while someone else is in the same tree -- version control and branch conventions, worktrees rather than `main`, and the changes only Aaron can make |
> | `DOCUMENTATION.md` | keeping the written record true -- writing a doc in the tense of what exists, the doc health check, session retros and where a learning gets routed |
>
> `PREFERENCES.md` is the entry point and links the others, but do not rely on
> reaching them by link. **List `E:\project-hub\docs\standards\*.md` and read what is there**,
> rather than trusting the table above to still be the whole set: it was one file
> until it passed its own size rule, four times over, most recently on
> 6 September 2026. A count written into this block is a census of a directory
> that grows, which is the failure `COLLABORATION.md` records about censuses
> generally -- it goes stale with nothing reporting that it has.
>
> If that path does not resolve -- a different machine, an unmounted drive --
> recover them rather than carrying on as though there were no standing
> preferences: `gh repo clone aaronbelchamber/project-hub`.

# AGENTS.md — School Pickup System

Read [MISSION.md](MISSION.md) first. The one thing to take from it before
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
