from pyaxidraw import axidraw
import sys

def axi_draw_paths(*paths):
    # --- init ----------------------------------------------------------------
    ad = axidraw.AxiDraw() # Initialize class
    ad.interactive()            # Enter interactive mode

    ad.options.speed_pendown = 40  # set pen-down speed to slow
    ad.options.units = 2           # Switch to mm units

    connected = ad.connect()    # Open serial port to AxiDraw
    if not connected:
        sys.exit() # end script

    # ad.update()                  # Process changes to options
    ad.moveto(0,0)                 # Pen-up return home

    # --- actual draw ---------------------------------------------------------
    for p in paths:
        ad.draw_path(p)

    # --- finit ---------------------------------------------------------------
    ad.moveto(0,0)              # Pen-up return home
    ad.disconnect()             # Close serial port to AxiDraw

def axi_draw_svg(input_svg):
    from pyaxidraw import axidraw 

    ad = axidraw.AxiDraw()
    ad.plot_setup(input_svg)
    
    ad.options.speed_pendown = 40  # set pen-down speed to slow
    ad.options.units = 2           # Switch to mm units
    ad.options.pen_pos_down = 30
    ad.options.pen_pos_up = 90
    ad.options.random_start = True

    # ad.options.reordering = 2
    ad.plot_run(True)
