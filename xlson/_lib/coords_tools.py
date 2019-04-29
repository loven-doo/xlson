def coords_from_range(fc, lc):
    coords_list = list()
    for i in range(fc[0], lc[0]+1):
        for j in range(fc[1], lc[1]+1):
            coords_list.append((i, j))
    return coords_list
