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
> | `ARCHITECTURE.md` | keeping one system coherent as it grows -- one fact with one owner, a declared read surface, a class that outgrew its own description, a protocol repeated instead of expressed |
> | `DESIGN_SYSTEM.md` | the dashboard's own tokens, plus two rules marked to apply everywhere -- above-the-fold density and `mm/dd/YYYY` date formatting |
> | `SITES.md` | Aaron's public web properties -- voice and imagery, the register for his own writing, screenshots of the internal tools when published, image format floors, one-writable-copy content, web hosting and site access |
> | `DATABASE.md` | whether, and how, something lives in a database -- whether it belongs in one at all, schema design, reading and writing through a shared data layer, coordinating concurrent schema changes |
> | `BRANCH_GUARD.md` | the hook that enforces the never-write-on-`main` rule -- what it denies, the `--allow` and `--realign-pass` override windows, the shell-command matcher |
> | `WINDOWS.md` | commands and filesystem operations that behave differently on Windows than the tool producing them assumes -- which tool actually creates a working symlink or junction, which command dialect for Aaron |
>
> `PREFERENCES.md` is the entry point and links the others, but do not rely on
> reaching them by link. **List `E:\project-hub\docs\standards\*.md` and read what is there**,
> rather than trusting the table above to still be the whole set: it was one file
> until it passed its own size rule, eight times over, most recently on
> 12 September 2026 when `BRANCH_GUARD.md` and `WINDOWS.md` came out. A count written into this block is a census of a directory
> that grows, which is the failure `COLLABORATION.md` records about censuses
> generally -- it goes stale with nothing reporting that it has.
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
