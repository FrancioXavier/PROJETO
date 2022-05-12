from math import ceil


def make_pagination_range(page_range, qty_pages, current_page):
    midde_range = ceil(qty_pages/2)
    start_range = current_page - midde_range
    stop_range = current_page + midde_range

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset
    return page_range[start_range:stop_range]
