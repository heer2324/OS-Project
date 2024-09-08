

def find_farthest_page(page_table, pages, current_index):
    farthest_index = -1
    farthest_page = None
    for page in page_table:
        index = len(pages)
        for i in range(current_index, len(pages)):
            if pages[i] == page:
                index = i
                break
        if index > farthest_index:
            farthest_index = index
            farthest_page = page
    return farthest_page

def optimal_page_replacement(pages, capacity):
    page_faults = 0
    page_table = []
    replacements = []
    page_tables = []

    for i, page in enumerate(pages):
        if page not in page_table:
            if len(page_table) == capacity:
                farthest_page = find_farthest_page(page_table, pages, i)
                farthest_index = page_table.index(farthest_page)
                page_table[farthest_index] = page
                replacements.append((farthest_page, page))
            else:
                page_table.append(page)
            page_faults += 1

        page_tables.append(page_table[:])  # Copy the page table to preserve its state
        
    matrix = get_page_table(page_tables)

    return matrix, page_faults, replacements


def get_page_table(page_tables):
    matrix = []
    max_len = max(len(pt) if isinstance(pt, list) else 1 for pt in page_tables)
    for i in range(max_len):
        row = []
        for pt in page_tables:
            if isinstance(pt, list) and i < len(pt):
                row.append(pt[i])
            else:
                row.append(-1)
        matrix.append(row)
    return matrix





def sstf(current_pos, req_queue):
    total_time = 0
    current_track = current_pos
    complete = []

    while req_queue:
        shortest_seek_time = float("inf")
        next_req = None

        for request in req_queue:
            seek_time = abs(request - current_track)
            if seek_time < shortest_seek_time:
                shortest_seek_time = seek_time
                next_req = request
        
        total_time += shortest_seek_time 
        req_queue.remove(next_req)
        complete.append(next_req)
        current_track = next_req  

    return total_time, complete

