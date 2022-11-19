from common.page import PAGE_WIDTH, PAGE_HEIGHT, PAGE_MARGIN
# --- svg preview -------------------------------------------------------------
def svg_pointlist(points):
    return ' '.join([f"{p[0]},{p[1]}" for p in points])
    
def svg_preview(*paths):
    polylines = [f'<polyline points="{svg_pointlist(p)}" fill="none" stroke="black" stroke-width="0.2"/>' for p in paths]
    svgout = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
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
            <rect fill="none" stroke="blue" stroke-width="0.2" width="{PAGE_WIDTH}" height="{PAGE_HEIGHT}"/>
            {polylines}
        </g>
        </svg>
        """
    with open('preview.svg','w') as fsvg:
        fsvg.write(svgout)
