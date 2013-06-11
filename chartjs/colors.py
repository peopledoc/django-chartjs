# -*- coding: utf-8 -*-
COLORS = [
    (202, 201, 197),  # Light gray
    (171, 9, 0),      # Red
    (166, 78, 46),    # Light orange
    (255, 190, 67),   # Yellow
    (163, 191, 63),   # Light green
    (122, 159, 191),  # Light blue
    (140, 5, 84),     # Pink
    (166, 133, 93),   # Light brown
    (75, 64, 191),    # Red blue
    (237, 124, 60),    # orange
]


def next_color(color_list=COLORS):
    """Create a different color from a base color list.

    >>> color_list = (
    ...    (122, 159, 191),  # Light blue
    ...    (202, 201, 197),  # Light gray,
    ... )
    >>> g = next_color(color_list)
    >>> next(g)
    [122, 159, 191]
    >>> next(g)
    [202, 201, 197]
    >>> next(g)
    [63, 100, 132]
    >>> next(g)
    [143, 142, 138]
    >>> next(g)
    [4, 41, 73]
    >>> next(g)
    [84, 83, 79]
    """
    step = 1
    while True:
        for color in color_list:
            yield map(lambda base: (base + step) % 256, color)
        step += 197
