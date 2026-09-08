"""
Regenerate the whole image set in the brand deck's printed treatment.

    python3 tools/build_imagery.py

Sources are the untouched photographs in assets/img/.photo-originals/ — the
first run copies them there, and every run afterwards works from those, so the
treatment never compounds on itself. Safe to re-run after changing any
composition below. Requires Pillow.
"""
import sys, os, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from riso import *
from PIL import Image

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")
ORIG = os.path.join(IMG, ".photo-originals")
os.makedirs(ORIG, exist_ok=True)
os.chdir(IMG)

def source(name, frm=None):
    """
    Always work from the untouched photograph, so reruns don't compound.
    `frm` prints this plate from a different photograph — used where a plate's
    own source was an isolated landmark portrait.
    """
    keep = os.path.join(ORIG, name)
    if not os.path.exists(keep) and os.path.exists(name):
        shutil.copy2(name, keep)
    if frm:
        alt = os.path.join(ORIG, frm)
        return Image.open(alt if os.path.exists(alt) else frm)
    return Image.open(keep)

def out(im, name, q=76):
    im.save(name, quality=q, method=6)
    print("  %-42s %s" % (name, im.size))

# --------------------------------------------------------------------------
# Service cards — charcoal sheet, the flat shape in the card's pillar colour.
# Each triangle is placed differently so the six read as a set, not a repeat.
# --------------------------------------------------------------------------
# Sized close to the card's own aspect so `cover` crops as little as possible,
# and the triangles stay near the centre so they survive the crop at every
# breakpoint rather than sliding out of frame on a narrow card.
CARDS = [
    ("advertising-research",  BLUE,   (0.58, 0.60, 0.86, 1.05, 0.0)),
    ("management-consultancy", RED,   (0.40, 0.62, 0.80, 1.00, 0.0)),
    ("marketing-research",    BLUE,   (0.52, 0.66, 1.02, 1.16, 0.0)),
    ("innovation-ai",         ORANGE, (0.62, 0.52, 0.70, 1.22, 0.0)),
    ("sourcing-procurement",  RED,    (0.46, 0.70, 0.94, 0.94, 0.0)),
    ("project-development",   ORANGE, (0.55, 0.56, 0.90, 1.12, 0.0)),
]
print("service cards")
for i, (slug, col, tri) in enumerate(CARDS):
    src = source("svc-%s.webp" % slug)
    out(riso(src, (720, 560), INK, col, tri=tri, tri_alpha=0.66,
             photo_strength=0.78, curve=(0.18, 0.90, 0.95), seed=11 + i * 7),
        "svc-%s.webp" % slug, q=82)

# --------------------------------------------------------------------------
# Page heroes — bone sheet, the printed plate the deck uses as an inset panel.
# --------------------------------------------------------------------------
# Composition varies across the set — scale, placement, and whether the mark is
# printed solid or as the logomark's outline — so ten plates read as a press run
# rather than as one template applied ten times.
#            name                         colour  (cx, cy, w, h, rot)              outline
HEROES = [
    ("hero-dubai",    BLUE,   (0.58, 0.58, 0.90, 0.80, 0.0), False),
    ("about-hero",    BLUE,   (0.40, 0.66, 1.10, 1.05, 0.0), False),
    ("services-hero", ORANGE, (0.60, 0.60, 0.92, 0.82, 0.0), False),
    ("contact-hero",  RED,    (0.50, 0.50, 0.72, 0.62, 0.0), True),
]
SERVICE_HEROES = [
    ("hero-advertising-research",   BLUE,   (0.52, 0.62, 0.98, 0.92, 0.0), False),
    ("hero-management-consultancy", RED,    (0.46, 0.48, 0.68, 0.60, 0.0), True),
    ("hero-marketing-research",     BLUE,   (0.62, 0.70, 1.14, 1.10, 0.0), False),
    ("hero-innovation-ai",          ORANGE, (0.44, 0.56, 0.80, 0.74, 0.0), False),
    ("hero-sourcing-procurement",   RED,    (0.55, 0.64, 1.02, 0.98, 0.0), False),
    ("hero-project-development",    ORANGE, (0.48, 0.52, 0.74, 0.66, 0.0), True),
]
print("page heroes")
for i, (name, col, tri, ol) in enumerate(HEROES):
    src = source(name + ".webp")
    out(riso(src, (1040, 1387), BONE, col, tri=tri, tri_alpha=0.86 if ol else 0.62,
             outline_only=ol, photo_strength=0.74, seed=3 + i * 5), name + ".webp")
    sm = source(name + "-sm.webp")
    out(riso(sm, (620, 827), BONE, col, tri=tri, tri_alpha=0.86 if ol else 0.62,
             outline_only=ol, photo_strength=0.74, grain_amount=10,
             seed=3 + i * 5), name + "-sm.webp", q=80)

print("service heroes")
for i, (name, col, tri, ol) in enumerate(SERVICE_HEROES):
    src = source(name + ".webp")
    out(riso(src, (1040, 1387), BONE, col, tri=tri, tri_alpha=0.86 if ol else 0.62,
             outline_only=ol, photo_strength=0.74, seed=21 + i * 4), name + ".webp")
    sm = source(name + "-sm.webp")
    out(riso(sm, (480, 640), BONE, col, tri=tri, tri_alpha=0.86 if ol else 0.62,
             outline_only=ol, photo_strength=0.74, grain_amount=9,
             seed=21 + i * 4), name + "-sm.webp", q=80)

# --------------------------------------------------------------------------
# Full-bleed bands — these carry white text, so the sheet stays charcoal and
# the flat shape sits far right at low strength rather than under the copy.
# --------------------------------------------------------------------------
print("bands")
BANDS = [("band-dusk", BLUE, 31), ("band-storm", ORANGE, 37)]
for name, col, seed in BANDS:
    src = source(name + ".webp")
    out(riso(src, (1700, 850), INK, col, tri=(0.82, 0.55, 0.62, 1.25, 0.0),
             tri_alpha=0.34, photo_strength=0.82, curve=(0.18, 0.9, 1.0), seed=seed),
        name + ".webp")
    sm = source(name + "-sm.webp")
    out(riso(sm, (900, 450), INK, col, tri=(0.82, 0.55, 0.62, 1.25, 0.0),
             tri_alpha=0.34, photo_strength=0.82, curve=(0.18, 0.9, 1.0),
             grain_amount=10, seed=seed), name + "-sm.webp", q=80)
# --------------------------------------------------------------------------
# Landmark substitutions.
#
# Four plates were isolated portraits of the Burj Khalifa and the Burj Al Arab
# — the building as the subject, filling the frame. Emaar and Jumeirah both
# assert commercial-image rights over their towers, and an isolated portrait is
# the exposed case; a tower appearing among dozens in a cityscape is not. These
# four are reprinted from wide skylines instead, each from a different region of
# the source so the hero and the card of one service never repeat a composition.
#
# band-dawn was carrying no references at all, so it costs nothing to spend here.
# --------------------------------------------------------------------------
SWAPS = [
    # name                            from            crop (x0,y0,x1,y1)     size          colour  triangle                        outline
    ("hero-innovation-ai",            "band-dawn.webp",     (0.50, 0.00, 0.83, 1.00), (1040, 1387), ORANGE, (0.44, 0.56, 0.80, 0.74, 0.0), False),
    ("hero-innovation-ai-sm",         "band-dawn.webp",     (0.50, 0.00, 0.83, 1.00), (480, 640),   ORANGE, (0.44, 0.56, 0.80, 0.74, 0.0), False),
    ("svc-innovation-ai",             "band-dawn.webp",     (0.02, 0.10, 0.52, 1.00), (720, 560),   ORANGE, (0.62, 0.52, 0.70, 1.22, 0.0), False),
    ("hero-sourcing-procurement",     "band-dusk.webp",     (0.04, 0.16, 0.35, 1.00), (1040, 1387), RED,    (0.55, 0.62, 1.00, 0.94, 0.0), False),
    ("hero-sourcing-procurement-sm",  "band-dusk.webp",     (0.04, 0.16, 0.35, 1.00), (480, 640),   RED,    (0.55, 0.62, 1.00, 0.94, 0.0), False),
    ("svc-sourcing-procurement",      "band-dusk.webp",     (0.62, 0.24, 1.00, 0.90), (720, 560),   RED,    (0.46, 0.70, 0.94, 0.94, 0.0), False),
]
print("landmark substitutions")
for i, (name, frm, crop, size, col, tri, ol) in enumerate(SWAPS):
    src = source(name + ".webp", frm=frm)
    card = name.startswith("svc-")
    im = riso(src, size, INK if card else BONE, col, tri=tri,
              tri_alpha=(0.66 if card else (0.86 if ol else 0.62)),
              outline_only=ol, crop=crop,
              photo_strength=0.78 if card else 0.74,
              curve=(0.18, 0.90, 0.95) if card else (0.12, 0.88, 1.05),
              grain_amount=9 if name.endswith("-sm") else 12,
              seed=57 + i * 6)
    out(im, name + ".webp", q=82 if card else (80 if name.endswith("-sm") else 76))

print("done")
