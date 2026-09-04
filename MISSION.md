# Mission

**This is a concept, not a proof of concept.** Stated by Aaron 2026-09-04:
*"not even PoC level, it's a concept I'll want to flesh out."* The README
called it a proof of concept and that overstated what is here; corrected in
the same pass. What exists is the idea, written down at length, with four
camera/OCR spikes attached to show the reading step is tractable.

## What this is for

Automating the car line at school pickup. Today two teachers stand outside for
close to an hour, in whatever weather, reading a number off a printed card in
each car's window and typing it into a phone so the office can call that child
to the pickup line. The concept replaces the typing with a camera: a scanner
at driver height reads the card -- ideally a QR code, with the printed digits
as a fallback -- and submits the same number to the same system.

It is deliberately not an AI product. The interesting problem is operational,
not algorithmic: it removes a task that wastes teacher time and introduces
transcription errors, and the reading step is ordinary computer vision.

## Who it's for

A single school's front-office and teaching staff, and the parents queueing.
Aaron's children's school is the case it was written from.

## What is actually here

- `src/car_line_v4.py` and `src/car_line_alternatives/car_line_v1..v3.py` --
  four successive attempts at the same camera-to-number step, roughly 150-190
  lines each. They are versions of one spike, not components of one program:
  nothing imports another and there is no entry point.
- `tests/test_camera_capture.py` and `tests/test_json_server.py` -- two small
  scripts that exercise a camera and a JSON endpoint by hand.
- `data/request_log*.json` -- captured request shapes.
- `requirements.txt` -- `opencv-python`, `pytesseract`, `easyocr`, `imutils`,
  `requests`. The README records that `easyocr` gave the best results of the
  OCR libraries tried.

## What it is not

- **Not a running system.** There is no service, no scheduler, no deployment
  and no entry point. Nothing here has been used at a school.
- **Not integrated with anything.** Whether the software the office currently
  uses exposes an API is an open question the README raises and nobody has
  answered. The fallback idea -- emitting the digits as synthetic keystrokes
  into the existing app -- is a sentence, not code.
- **No QR reader yet**, which is the part the README argues should be the
  primary path because QR decoding is far more reliable than OCR on a printed
  number.
- **Not a product, and not scheduled.** Fleshing it out is intended; nothing
  here should be read as committed work in progress.

## Interfaces

```yaml
provides: []
consumes: []
```

Nothing is declared in either direction, and that is accurate rather than
unfinished: this concept consumes no other project on this drive and offers
nothing to one. The integration it would eventually need is with a school's
existing pickup software, which is external and unidentified.

## Related projects

None. It shares no code, contract or dependency with anything else in this
portfolio, and it is not part of the internal-tooling design-system estate --
`PRACTICES.md` scopes that to the tools that run the drive, and this is not
one of them.
