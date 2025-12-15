#!/usr/bin/env python
# -*- encoding: utf-8 -#-

# https://axidraw.com/doc/py_api/
# https://github.com/evil-mad/axidraw
# http://axidraw.com/docs

from common.axidraw import axi_draw_svg
import sys

axi_draw_svg(sys.argv[1])
