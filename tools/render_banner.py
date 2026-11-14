"""Renders the README banner, .github/assets/meetube/banner.webp: the logo, the name and one line.

    python tools/render_banner.py
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ASSETS = os.path.join(os.path.dirname(__file__), '..', '.github', 'assets', 'meetube')
FONTS = 'C:/Windows/Fonts/'
RED = (255, 69, 58)
W, H = 2400, 360


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def glow(center, radius, color, alpha):
    layer = Image.new('RGBA', (W, H), color + (0,))
    mask = Image.new('L', (W, H), 0)
    x, y = center
    ImageDraw.Draw(mask).ellipse((x - radius, y - radius, x + radius, y + radius), fill=alpha)
    layer.putalpha(mask.filter(ImageFilter.GaussianBlur(radius * 0.6)))
    return layer


def banner():
    img = Image.new('RGBA', (W, H), (22, 22, 26, 255))
    img.alpha_composite(glow((230, H * 0.5), 460, RED, 120))
    img.alpha_composite(glow((W * 0.88, H * 1.05), 560, (120, 60, 255), 90))
    logo = Image.open(os.path.join(ASSETS, 'icon.png')).convert('RGBA').resize((220, 220), Image.LANCZOS)
    img.alpha_composite(logo, (90, (H - 220) // 2))
    d = ImageDraw.Draw(img)
    x, title_f = 360, font('seguibl.ttf', 136)
    d.text((x, 190), 'MeeTube', font=title_f, fill=(255, 255, 255), anchor='ls')
    d.text((x + d.textlength('MeeTube ', font=title_f), 190), 'TV', font=title_f, fill=RED, anchor='ls')
    d.text((x + 4, 264), 'YouTube, reimagined for the big screen.', font=font('seguisb.ttf', 50),
           fill=(225, 225, 232), anchor='ls')
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, W - 1, H - 1), 40, fill=255)
    out.paste(img, (0, 0), mask)
    ImageDraw.Draw(out).rounded_rectangle((0, 0, W - 1, H - 1), 40, outline=(255, 255, 255, 26), width=2)
    return out


if __name__ == '__main__':
    path = os.path.join(ASSETS, 'banner.webp')
    banner().save(path, quality=88, method=6)
    print(path, os.path.getsize(path) // 1024, 'KB')
