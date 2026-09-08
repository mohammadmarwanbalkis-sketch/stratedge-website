"""
Contrast check for text sitting on the riso plates.

A token-level check is not enough here: the text sits on a photograph under a
gradient scrim, so the real question is what the composite is at the height
where each piece of type actually lands. This samples the generated plates,
applies the scrim's alpha at that height, and reports the ratio.

    python3 tools/check_contrast.py

Exits non-zero if anything fails, so it can gate a build.
"""
import os, sys
from PIL import Image

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")

# keep these in step with :root in style.css
LIFT = {"blue": (0x70, 0x9f, 0xae), "red": (0xdf, 0x7d, 0x77), "orange": (0xf5, 0xb0, 0x2f)}
INK  = {"blue": (0x3e, 0x6c, 0x7b), "red": (0xb8, 0x37, 0x2f), "orange": (0x8a, 0x62, 0x08)}
WHITE = (255, 255, 255)
SCRIM = (24, 25, 25)
# .bs::before — rgba(24,25,25, a) at these stops
STOPS = [(0, .12), (.42, .38), (.72, .74), (1, .80)]

PLATES = {
    "svc-advertising-research": "blue",   "svc-management-consultancy": "red",
    "svc-marketing-research": "blue",     "svc-innovation-ai": "orange",
    "svc-sourcing-procurement": "red",    "svc-project-development": "orange",
    "prin-integrity": "blue",             "prin-rigour": "orange",
    "prin-discretion": "red",             "prin-accountability": "blue",
}
# where each piece of type sits, what colour it is, and the ratio it must clear
SLOTS = [
    ("label",  .14, "white", 4.5),   # .bs__pillar  0.58rem  -> small text
    ("number", .14, "white", 4.5),   # .bs__n       0.66rem  -> small text
    ("title",  .60, "lift",  3.0),   # .bs h3       >=1.19rem bold -> large text
    ("body",   .78, "body",  4.5),
    ("link",   .90, "lift",  4.5),   # .bs__go      0.63rem  -> small text
]

def lum(c):
    f = [x / 255 for x in c[:3]]
    f = [(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4) for v in f]
    return .2126 * f[0] + .7152 * f[1] + .0722 * f[2]

def ratio(a, b):
    l1, l2 = lum(a), lum(b)
    l1, l2 = max(l1, l2), min(l1, l2)
    return (l1 + .05) / (l2 + .05)

def composite(fg, alpha, bg):
    return tuple(round(fg[i] * alpha + bg[i] * (1 - alpha)) for i in range(3))

def alpha_at(y):
    for i in range(len(STOPS) - 1):
        y0, a0 = STOPS[i]; y1, a1 = STOPS[i + 1]
        if y0 <= y <= y1:
            return a0 + (a1 - a0) * ((y - y0) / (y1 - y0))
    return STOPS[-1][1]

def main():
    failures = []
    print("%-28s %-8s %7s %7s  %s" % ("plate", "slot", "ratio", "needs", ""))
    for plate, ink in PLATES.items():
        im = Image.open(os.path.join(IMG, plate + ".webp")).convert("RGB")
        w, h = im.size
        for name, y, kind, need in SLOTS:
            band = im.crop((0, int(h * (y - .06)), w, int(h * min(1, y + .06)))) \
                     .resize((1, 1), Image.BOX).getpixel((0, 0))
            bg = composite(SCRIM, alpha_at(y), band)
            fg = {"white": WHITE, "lift": LIFT[ink],
                  "body": composite(WHITE, .70, bg)}[kind]
            r = ratio(fg, bg)
            bad = r < need
            if bad:
                failures.append("%s / %s: %.2f:1 (needs %.1f)" % (plate, name, r, need))
            print("%-28s %-8s %7.2f %7.1f  %s" % (plate, name, r, need, "FAIL" if bad else ""))

    print("\nresting state, ink on the white card:")
    for n, c in INK.items():
        print("  %-7s %.2f:1" % (n, ratio(c, WHITE)))

    if failures:
        print("\n%d FAILURES:" % len(failures))
        for f in failures:
            print("  " + f)
        return 1
    print("\nAll plate text clears WCAG AA.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
