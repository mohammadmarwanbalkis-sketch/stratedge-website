"""
Riso / screen-print treatment matching the Stratedge brand deck.

The deck's images are not plain photographs. They are a paper ground, a gritty
high-contrast photographic element, flat brand-colour geometry (usually a
triangle) printed slightly out of register, and visible grain. This rebuilds
that from the site's existing photography so the whole image set reads as one
printed family rather than a stock-photo grid.
"""
from PIL import Image, ImageOps, ImageFilter, ImageChops, ImageDraw
import random, math

BONE   = (206, 202, 190)   # #cecabe — the deck's paper ground
INK    = (36, 37, 37)      # #242525 — the deck's charcoal
BLUE   = (81, 138, 156)
RED    = (208, 66, 58)
ORANGE = (245, 176, 47)


def _curve(im, black=0.10, white=0.92, gamma=1.0):
    """Crush the blacks and clip the highlights the way a screen print does."""
    lut = []
    for i in range(256):
        v = i / 255.0
        v = (v - black) / max(1e-6, (white - black))
        v = min(1.0, max(0.0, v)) ** gamma
        lut.append(int(v * 255))
    return im.point(lut)


def _grain(size, amount=12, seed=7, blur=0.9):
    """
    Paper grain. Coarse noise, softened so it reads as fibre rather than as
    compression artefacts — and so WebP can still encode it. Sharper grain than
    this roughly doubles every file, which is not worth it on a hero image.
    """
    rnd = random.Random(seed)
    w, h = size
    small = Image.new("L", (max(1, w // 2), max(1, h // 2)))
    small.putdata([rnd.gauss(128, amount) for _ in range(small.width * small.height)])
    return small.resize(size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(blur))


def _speckle(size, n=420, seed=3, radius=(1, 3)):
    """The stray specks a riso drum leaves on the sheet."""
    rnd = random.Random(seed)
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    w, h = size
    for _ in range(n):
        x, y = rnd.randrange(w), rnd.randrange(h)
        r = rnd.randint(*radius)
        d.ellipse((x - r, y - r, x + r, y + r), fill=rnd.randint(40, 150))
    return m.filter(ImageFilter.GaussianBlur(0.6))


def duotone(gray, dark, light):
    """Map a grayscale plate between two ink colours."""
    lut = []
    for ch in range(3):
        for i in range(256):
            t = i / 255.0
            lut.append(int(dark[ch] + (light[ch] - dark[ch]) * t))
    return Image.merge("RGB", (gray, gray, gray)).point(lut)


def tri_outline_mask(size, pts, width, radius=None):
    """
    A rounded-corner triangle outline — the logomark itself, printed large.
    Drawn by stroking the polygon and rounding every join with a disc, which is
    what stroke-linejoin:round does in the SVG version of the same mark.
    """
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    ring = list(pts) + [pts[0]]
    d.line(ring, fill=255, width=width)
    r = radius if radius is not None else width // 2
    for x, y in pts:
        d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    return m


def tri_mask(size, pts, feather=0.0):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    if feather:
        m = m.filter(ImageFilter.GaussianBlur(feather))
    return m


def tri_points(size, cx, cy, w, h, rot=0.0):
    """An upward triangle centred on (cx,cy), in fractions of the canvas."""
    W, H = size
    cx, cy, w, h = cx * W, cy * H, w * W, h * H
    pts = [(0, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    c, s = math.cos(rot), math.sin(rot)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def riso(src, size, ground, accent, *, photo_strength=0.8, tri=None,
         tri_alpha=0.60, tri_outline=None, seed=7, grain_amount=12,
         ink=None, paper=None, curve=(0.12, 0.88, 1.05), invert_photo=False,
         second=None, second_alpha=0.5, outline_only=False, outline_w=0.055,
         crop=None):
    """
    ground  — the sheet the image is printed on (bone or charcoal)
    accent  — the flat brand colour laid over it
    ink     — the darkest tone the photographic plate reaches
    paper   — the lightest tone it reaches (defaults to the ground)
    tri     — (cx, cy, w, h, rot) for the flat triangle, in canvas fractions
    crop    — (x0, y0, x1, y1) region of the source to print, in fractions of
              the source, so one photograph can yield plates that share nothing
    second  — an optional second flat shape, same tuple shape, in `accent2`
    """
    W, H = size
    light_sheet = sum(ground) > 380
    ink = ink or ((58, 55, 50) if light_sheet else (12, 13, 13))
    paper = paper or (ground if light_sheet else (156, 154, 148))

    base = Image.new("RGB", size, ground)

    # --- the photographic plate: one gritty ink, not a full-colour picture
    if crop:
        sw, sh = src.size
        x0, y0, x1, y1 = crop
        src = src.crop((int(x0 * sw), int(y0 * sh), int(x1 * sw), int(y1 * sh)))
    ph = ImageOps.fit(src.convert("L"), size, Image.LANCZOS, centering=(0.5, 0.45))
    # normalise first: night shots and daylight shots otherwise print at wildly
    # different densities and the set stops reading as one press run
    ph = ImageOps.autocontrast(ph, cutoff=(1, 2))
    ph = _curve(ph, *curve)
    ph = ph.filter(ImageFilter.UnsharpMask(radius=2.4, percent=130, threshold=3))
    if invert_photo:
        ph = ImageOps.invert(ph)
    base = Image.blend(base, duotone(ph, ink, paper), photo_strength)

    # --- the flat colour, printed slightly out of register
    def lay(spec, colour, alpha, outline=None):
        pts = tri_points(size, *spec)
        m = (tri_outline_mask(size, pts, max(3, int(W * outline_w)))
             if outline_only else tri_mask(size, pts))
        flat = Image.new("RGB", size, colour)
        shaded = ImageChops.multiply(flat, Image.merge("RGB", (ph, ph, ph)))
        flat = Image.blend(flat, shaded, 0.38)
        off = m.transform(size, Image.AFFINE, (1, 0, -3, 0, 1, 2), Image.BILINEAR)
        base.paste(flat, (0, 0), off.point(lambda v: int(v * alpha)))
        if outline:
            ol = Image.new("RGB", size, outline)
            edge = Image.new("L", size, 0)
            ImageDraw.Draw(edge).polygon(pts, outline=255, width=max(2, W // 300))
            base.paste(ol, (0, 0), edge.point(lambda v: int(v * 0.9)))

    if second:
        lay(second, second[5] if len(second) > 5 else accent, second_alpha)
    if tri:
        lay(tri, accent, tri_alpha, tri_outline)

    # --- paper: grain, then specks
    g = _grain(size, grain_amount, seed)
    base = ImageChops.overlay(base, Image.merge("RGB", (g, g, g)))
    sp = _speckle(size, n=int(W * H / 5200), seed=seed + 11)
    spc = Image.new("RGB", size, ink if light_sheet else (255, 255, 255))
    base.paste(spc, (0, 0), sp.point(lambda v: int(v * 0.16)))
    return base
