#!/usr/bin/env python3
#
# Plotting methods.
#

def axletter(axes, letter, offset=-0.05, tweak=0,
             weight='bold', fontsize=14, ha='center'):
    """
    Draw a letter (e.g. "A") near the top left of an axes system.

    Arguments:

    ``axes``
        The axes to label.
    ``letter``
        The letter (or text) to label the axes with.
    ``offset``
        An x offset, specified in figure coordinates. Using figure coordinates
        lets you align labels for different axes.
    ``tweak``
        An optional y coordinate tweak (in figure coordinates).
    ``weight``
        The font weight (default: bold)
    ``fontsize``
        The font size (default: 14)
    ``ha``
        Horizontal alignment (default: center)

    """
    # Get top of axes, in figure coordinates
    trans = axes.transAxes
    x, y = trans.transform((0, 1))
    trans = axes.get_figure().transFigure
    x, y = trans.inverted().transform((x, y))

    font = dict(weight=weight, fontsize=fontsize)
    axes.text(x + offset, y + tweak, letter, font, ha=ha, va='top',
              transform=trans)


#def axtext_low(axes, text, x=0, y)
