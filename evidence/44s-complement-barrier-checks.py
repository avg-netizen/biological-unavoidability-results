"""Finite controls for complement avoidance and Thue–Morse barriers.

The infinite claims are proved in the author packet's complement-and-barriers.md.
This deliberately uses sets of reachable vertices, not an interval shortcut.
"""
from itertools import groupby, product
import json
from pathlib import Path


def thue(n):
    return n.bit_count() & 1


def outgoing(s, u):
    for v in (u + 1, u + 2):
        if v < 2:
            continue
        incoming = {v - 1: s(v // 2) ^ (v & 1),
                    v - 2: 1 ^ s(v // 2) ^ (v & 1)}
        yield v, incoming[u]


def lowbit(n):
    assert n > 0
    return n & -n


def weight(i):
    return sum(lowbit(d // 2 + 1) for d in range(i + 1))


def first_empty(start, flip, cutoff):
    states = {start}
    for k in range(cutoff):
        states = {v for u in states for v, label in outgoing(thue, u)
                  if label == (thue(k) ^ flip)}
        if not states:
            return k + 1
    raise AssertionError((start, flip, cutoff, sorted(states)))


def main():
    boundary_edges = 0
    for word in product((0, 1), repeat=10):
        s = lambda k, word=word: word[k]
        for start in range(8):
            for flip in (0, 1):
                states = {start}
                for k in range(6):
                    new = set()
                    for u in states:
                        for v, label in outgoing(s, u):
                            if label != (s(k) ^ flip):
                                continue
                            assert v - 2 * (k + 1) >= -flip
                            assert v - 2 * (k + 1) in (u - 2 * k, u - 2 * k - 1)
                            new.add(v)
                            boundary_edges += 1
                    states = new

    periodic_controls = 0
    for period in range(1, 9):
        for word in product((0, 1), repeat=period):
            s = lambda k, word=word: word[k % len(word)]
            for flip in (0, 1):
                start = 2 * period - 1 - flip
                for k in range(128):
                    u = start + 2 * k
                    assert (u + 2, s(k) ^ flip) in list(outgoing(s, u))
                periodic_controls += 1

    longest_runs = {}
    for shift in range(1, 257):
        values = [thue(k) ^ thue(k + shift) for k in range(8192)]
        run = max(sum(1 for _ in group) for _, group in groupby(values))
        assert run <= 3 * lowbit(shift)
        longest_runs[shift] = run

    for m in range(1, 1025):
        direct = sum(lowbit(q) for q in range(1, m + 1))
        identity = m + sum(2 ** (j - 1) * (m // 2 ** j)
                           for j in range(1, m.bit_length()))
        recurrence = (m + 1) // 2 + 2 * sum(lowbit(q) for q in range(1, m // 2 + 1))
        assert direct == identity == recurrence
        assert 2 * direct <= 2 * m + m * (m.bit_length() - 1)

    barriers = [[], []]
    for start in range(1024):
        w = weight(start)
        for flip in (0, 1):
            bound = start + flip + 1 + 3 * w
            b = first_empty(start, flip, bound)
            assert b <= bound
            barriers[flip].append(b)

    output = {
        "status": "all finite controls passed; infinite assertions use the hand proofs",
        "boundary_controls": {"binary_words": 1024, "word_length": 10,
                              "starts": [0, 7], "steps": 6,
                              "matching_edges_checked": boundary_edges},
        "periodic_positive_controls": periodic_controls,
        "correlation_controls": {"shifts": [1, 256], "positions": [0, 8191],
                                 "longest_runs": longest_runs},
        "arithmetic_identity_controls": 1024,
        "barrier_starts": [0, 1023],
        "first_empty_times_t": barriers[0],
        "first_empty_times_complement": barriers[1],
        "largest_first_empty_time": max(map(max, barriers)),
        "bound": "first-empty time <= i + flip + 1 + 3*sum(lowbit(d//2+1),d=0..i)"
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({key: output[key] for key in
                      ('status', 'boundary_controls', 'periodic_positive_controls',
                       'barrier_starts', 'largest_first_empty_time')}, indent=2))


if __name__ == '__main__':
    main()
