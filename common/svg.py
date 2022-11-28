from common.page import PAGE_WIDTH, PAGE_HEIGHT, PAGE_MARGIN

# --- svg preview -------------------------------------------------------------
def svg_pointlist(points):
    return " ".join([f"{p[0]},{p[1]}" for p in points])


def svg_margins():
    return [
        f"""<rect fill="none" stroke="blue" stroke-width="0.2" width="{PAGE_WIDTH}" height="{PAGE_HEIGHT}"/>"""
    ]


def svg_rects(*specs):
    return [
        f'<rect x="{r[0]}" y="{r[1]}" width="{r[2]}" height="{r[3]}" fill="none" stroke="black" stroke-width="0.2"/>'
        for r in specs
    ]


def svg_polylines(*paths):
    return [
        f'<polyline points="{svg_pointlist(p)}" fill="none" stroke="black" stroke-width="0.2"/>'
        for p in paths
    ]


def svg_circles(*positions):
    return [
        f'<circle cx="{p[0]}" cy="{p[1]}" r="{p[2]}" fill="none" stroke="black" stroke-width="0.2"/>'
        for p in positions
    ]


def svg_doc(*elements):
    text = "\n".join(elements)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <svg
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:svg="http://www.w3.org/2000/svg"
            xmlns="http://www.w3.org/2000/svg"
            version="1.1"
            id="test"
            viewBox="0 0 {PAGE_WIDTH + PAGE_MARGIN * 2} {PAGE_HEIGHT + PAGE_MARGIN * 2}"
            height="{PAGE_HEIGHT + PAGE_MARGIN * 2}mm"
            width="{PAGE_WIDTH + PAGE_MARGIN * 2}mm">
        <g transform="translate({PAGE_MARGIN},{PAGE_MARGIN})">
            {text}
        </g>
        </svg>
        """


def svg_write(doc, filename="preview"):
    with open(f"{filename}.svg", "w") as fsvg:
        fsvg.write(doc)
    with open(f"{filename}.html", "w") as hsvg:
        hsvg.write(
            f'''
            <!DOCTYPE html>
              <html>
                <body>
                  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:#fafafa;border:solid 1px #e0e0e0">
                    {doc}
                  </div>
                </body>
              </html>
              '''
        )
