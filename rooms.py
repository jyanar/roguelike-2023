import numpy as np

import tile_types


# Represents the square area in which a room may be placed.
class Area:
    def __init__(self, bw: int, bh: int, data: np.array = None):
        self.bw = bw
        self.bh = bh
        if data:
            self.data = data
        else:
            self.data = np.full((bw, bh), fill_value=tile_types.wall, order="F")
    
    def render(self) -> None:
        for i in range(self.bw):
            for j in range(self.bh):
                if self.data[i,j] == tile_types.wall:
                    print('#', end='')
                elif self.data[i,j] == tile_types.floor:
                    print('.', end='')
            print()
    
def gen_rectangle_room(bw: int, bh: int) -> Area:
    return Area(bw, bh, np.full((bw, bh), fill_value=tile_types.floor, order="F"))


#
#
# (x1,y1)-----------(x2,y1)
#   |                  |
#   |                  |
# (x1,y2)-----------(x2,y2)
#
#
def gen_overlapping_rectangles_room(bw: int, bh: int, nrect=2) -> Area:
    a = Area(bw, bh)
    for i in range(nrect):
        x1 = np.random.randint(0, bw-1)
        x2 = x1 + np.random.randint(x1, bw)
        y1 = np.random.randint(0, bh)
        y2 = y1 + np.random.randint(y1, bh)
        a.data[x1 : x2, y1 : y2] = tile_types.floor
    return a


