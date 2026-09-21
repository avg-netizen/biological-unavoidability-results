"""Finite-extension controls; no countable claim is inferred from these tests."""
from itertools import product
from pathlib import Path
import json


def target(j, k):
    return ((k + j // 2).bit_count() & 1) ^ (j & 1)


def extension(prefix, j):
    n = len(prefix) - 1
    c = -n - 2

    def r(v):
        return prefix[v] if v <= n else target(j, (v - c) // 2) ^ ((v - c) & 1)

    return r, c


def barrier(r, j, start, cutoff=100000):
    states = {start}
    queried = 1
    for k in range(cutoff):
        new = set()
        for u in states:
            for v in (u + 1, u + 2):
                if v < 2:
                    continue
                queried = max(queried, v)
                label = r(v) if v == u + 1 else 1 - r(v)
                if label == target(j, k):
                    new.add(v)
        states = new
        if not states:
            return k + 1, queried
    raise AssertionError(('finite control cutoff reached', j, start, cutoff))


def main():
    preserved_prefix_controls = 0
    boundary_edges = 0
    max_barrier = 0
    for bits in product((0, 1), repeat=6):
        for j in range(4):
            r, c = extension(bits, j)
            assert tuple(r(v) for v in range(6)) == bits
            for start in range(12):
                b, _ = barrier(r, j, start)
                max_barrier = max(max_barrier, b)
                states = {start}
                for k in range(b):
                    new = set()
                    for u in states:
                        for v in (u + 1, u + 2):
                            if v < 2:
                                continue
                            label = r(v) if v == u + 1 else 1 - r(v)
                            if label == target(j, k):
                                if v > 5:
                                    assert v - 2 * (k + 1) >= c
                                    boundary_edges += 1
                                new.add(v)
                    states = new
                assert not states
                preserved_prefix_controls += 1

    # Diagonal enumeration of requirements (j,i), first six diagonals.
    prefix = [0, 0]
    certificates = []
    for diagonal in range(6):
        for j in range(diagonal + 1):
            start = diagonal - j
            r, c = extension(prefix, j)
            b, max_read = barrier(r, j, start)
            last = max(len(prefix), max_read)
            old = prefix[:]
            prefix = [r(v) for v in range(last + 1)]
            assert prefix[:len(old)] == old
            certificates.append({'target_index': j, 'start': start,
                                 'empty_depth': b, 'last_frozen': last, 'boundary': c})
            # All earlier certificates survive every later extension.
            for cert in certificates:
                vals = lambda v: prefix[v]
                got, _ = barrier(vals, cert['target_index'], cert['start'], cert['empty_depth'])
                assert got == cert['empty_depth']

    # General alphabets: arbitrary permutations at the first two non-roots.
    from itertools import permutations
    general_controls = {}
    for n in (2, 3, 4):
        count = 0
        longest = 0
        for pair in product(permutations(range(n)), repeat=2):
            end = n + 1
            c = -(n - 1) * (end + n)
            def label(v, a):
                if v <= end:
                    return pair[v - n][a - 1]
                return (((v - c) // n).bit_count() + a - (v - c) % n - 1) % n
            for v in range(n, end + 100):
                assert set(label(v, a) for a in range(1, n + 1)) == set(range(n))
            for start in range(8):
                states = {start}
                for k in range(10000):
                    new = set()
                    for u in states:
                        for a in range(1, n + 1):
                            v = u + a
                            if v >= n and label(v, a) == k.bit_count() % n:
                                if v > end:
                                    assert v - n * (k + 1) >= c
                                new.add(v)
                    states = new
                    if not states:
                        break
                assert not states
                count += 1
                longest = max(longest, k + 1)
        general_controls[n] = {'preserved_permutation_pairs': len(list(permutations(range(n)))) ** 2,
                               'start_controls': count, 'largest_first_empty_time': longest}

        # Periodic positive controls for the C=0 single-target construction.
        for period in range(1, 4):
            for word in product(range(n), repeat=period):
                for k in range(32):
                    v = n * period - 1 + n * (k + 1)
                    edge = (word[(v // n) % period] + n - (v % n) - 1) % n
                    assert edge == word[k % period]

    output = {
        'status': 'all finite controls passed; countable theorem requires the hand proof',
        'preserved_prefixes': 64, 'prefix_length': 6,
        'targets': 't, complement(t), shift(t), complement(shift(t))',
        'starts': [0, 11], 'preserved_prefix_controls': preserved_prefix_controls,
        'tail_boundary_edges_checked': boundary_edges,
        'largest_barrier_in_prefix_controls': max_barrier,
        'staged_target_family': 's_j(k)=t(k+floor(j/2)) xor (j mod 2)',
        'stages': certificates, 'final_prefix_length': len(prefix),
        'final_prefix': ''.join(map(str, prefix)),
        'general_alphabet_controls': general_controls
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({k: output[k] for k in ('status', 'preserved_prefix_controls',
                                           'tail_boundary_edges_checked',
                                           'largest_barrier_in_prefix_controls',
                                           'final_prefix_length', 'general_alphabet_controls')}, indent=2))


if __name__ == '__main__':
    main()
