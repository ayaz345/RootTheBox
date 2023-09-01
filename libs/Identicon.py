# source: https://github.com/evuez/svg-identicon
# Modified for 2 x 1 ratio - RootTheBox
from os import path
from hashlib import md5
from tornado.options import options


def _svg(width, height, body, color):
    return """<?xml version="1.0"?>
    <svg width="{w}" height="{h}"
        viewBox="0 0 {w} {h}"
        viewport-fill="red"
        xmlns="http://www.w3.org/2000/svg">
    <rect x="0" y="0" width="{w}" height="{h}" fill="{color}"/>
    {body}
    </svg>""".format(
        w=width, h=height, body=body, color=color
    )


def _rect(x, y, width, height, color, stroke, stroke_weight):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{color}" stroke="{stroke}" stroke-width="{stroke_weight}"/>'


def identicon(str_, size, background="#f0f0f0", square=False):
    digest = int(md5(str_.encode("utf-8")).hexdigest(), 16)
    color = "#{:06x}".format(digest & 0xFFFFFF)
    stroke_weight = 0.02
    digest, body = digest >> 24, ""
    x = y = 0
    if square:
        for _ in range(size**2 // 2):
            if digest & 1:
                body += _rect(x, y, 1, 1, color, background, stroke_weight)
                body += _rect(size - x - 1, y, 1, 1, color, background, stroke_weight)
            digest, y = digest >> 1, y + 1
            x, y = (x + 1, 0) if y == size else (x, y)
        image_data = _svg(size, size, body, background)
    else:
        for _ in range(size**2):
            if digest & 1:
                body += _rect(x, y, 1, 1, color, background, stroke_weight)
                body += _rect(
                    size * 2 - x - 1, y, 1, 1, color, background, stroke_weight
                )
            digest, y = digest >> 1, y + 1
            x, y = (x + 1, 0) if y == size else (x, y)
        image_data = _svg(size * 2, size, body, background)
    avatar = f"upload/{str(digest)}.svg"
    file_path = path.join(options.avatar_dir, avatar)
    with open(file_path, "w") as fp:
        fp.write(image_data)
    return avatar
