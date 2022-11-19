# --- page setup (mm) ---------------------------------------------------------
PAGE_WIDTH = 350
PAGE_HEIGHT = 250
PAGE_MARGIN = 5

def gen_border(CX, CY, W_XT, H_XT):
    return [
        [CX-W_XT, CY-H_XT],
        [CX+W_XT, CY-H_XT],
        [CX+W_XT, CY+H_XT],
        [CX-W_XT, CY+H_XT],
        [CX-W_XT, CY-H_XT]
    ]
