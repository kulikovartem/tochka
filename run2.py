import sys
import collections
import heapq

def min_steps_to_collect_all_keys(grid):
    H, W = len(grid), len(grid[0])
    starts = []
    key_positions = {}
    for i in range(H):
        for j in range(W):
            c = grid[i][j]
            if c == '@':
                starts.append((i, j))
            elif 'a' <= c <= 'z':
                key_positions[c] = (i, j)
    N = len(key_positions)
    if N == 0:
        return 0

    keys = sorted(key_positions)
    key_to_bit = {k: idx for idx, k in enumerate(keys)}
    ALL_KEYS_MASK = (1 << N) - 1

    nodes = starts + [key_positions[k] for k in keys]
    M = len(nodes)
    dist_graph = [[] for _ in range(M)]
    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for src in range(M):
        sx, sy = nodes[src]
        q = collections.deque([(sx, sy, 0, 0)])
        seen = {(sx, sy): {0}}

        while q:
            x, y, doors_mask, dist = q.popleft()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < H and 0 <= ny < W):
                    continue
                cell = grid[nx][ny]
                if cell == '#':
                    continue

                new_mask = doors_mask
                if 'A' <= cell <= 'Z':
                    bit = key_to_bit.get(cell.lower())
                    if bit is not None:
                        new_mask |= 1 << bit

                prev_masks = seen.get((nx, ny))
                if prev_masks is not None:
                    skip = any((pm & new_mask) == pm for pm in prev_masks)
                    if skip:
                        continue
                    to_remove = {pm for pm in prev_masks if (new_mask & pm) == new_mask}
                    prev_masks -= to_remove
                    prev_masks.add(new_mask)
                else:
                    seen[(nx, ny)] = {new_mask}

                nd = dist + 1
                if 'a' <= cell <= 'z':
                    bit = key_to_bit[cell]
                    tgt = 4 + bit
                    dist_graph[src].append((tgt, nd, new_mask))

                q.append((nx, ny, new_mask, nd))

    start_positions = tuple(range(4))
    heap = [(0, start_positions, 0)]
    best = {(start_positions, 0): 0}

    while heap:
        steps, pos, mask = heapq.heappop(heap)
        if mask == ALL_KEYS_MASK:
            return steps
        if best[(pos, mask)] < steps:
            continue

        for i in range(4):
            u = pos[i]
            for tgt, dist, req in dist_graph[u]:
                bit = tgt - 4
                if (mask >> bit) & 1:
                    continue
                if (mask & req) != req:
                    continue
                new_mask = mask | (1 << bit)
                new_pos = list(pos)
                new_pos[i] = tgt
                new_pos = tuple(new_pos)
                new_steps = steps + dist
                state = (new_pos, new_mask)
                if best.get(state, float('inf')) > new_steps:
                    best[state] = new_steps
                    heapq.heappush(heap, (new_steps, new_pos, new_mask))

    return -1

if __name__ == "__main__":
    grid = [line.rstrip('\n') for line in sys.stdin]
    print(min_steps_to_collect_all_keys(grid))
