"""Finite controls for 44m; not a test of infinite universality or halting."""
from itertools import product
from pathlib import Path
import json


def edges(s, n):
    result = []
    for v in range(2, n + 1):
        label = s(v // 2) ^ (v % 2)
        result.extend([(v - 1, v, label), (v - 2, v, 1 - label)])
    return result


words = lifted = 0
for p in range(1, 7):
    for w in product((0, 1), repeat=p):
        q = 2 * p
        rho = lambda v: w[(v // 2) % p] ^ (v % 2)
        for a in range(q):
            incoming = [((a - 1) % q, 1, rho(a)),
                        ((a - 2) % q, 2, 1 - rho(a))]
            assert {e[2] for e in incoming} == {0, 1}
        for word in product((0, 1), repeat=8):
            phase = 0
            reverse = []
            for label in reversed(word):
                delay = 1 if rho(phase) == label else 2
                reverse.append((delay, label))
                phase = (phase - delay) % q
            vertex = phase + 10 * q
            for delay, label in reversed(reverse):
                vertex += delay
                assert (rho(vertex) ^ (delay - 1)) == label
                lifted += 1
            words += 1

paired_regions = 0
for length in range(1, 8):
    for w in product((0, 1), repeat=length):
        periodic = lambda k: w[k] if k < length else 0
        aperiodic = lambda k: w[k] if k < length else (k - length).bit_count() % 2
        assert edges(periodic, 2 * length - 1) == edges(aperiodic, 2 * length - 1)
        paired_regions += 1

long_matches = 0
for n in range(1, 129):
    s = lambda k: 0 if k <= n else (k - n - 1).bit_count() % 2
    graph = set(edges(s, 2 * n + 1))
    assert all((1 + 2 * k, 3 + 2 * k, s(k)) in graph for k in range(n))
    long_matches += 1

report = {
    'status': 'PASS',
    'periodic_template_words_checked': words,
    'lifted_edges_checked': lifted,
    'indistinguishable_regions_checked': paired_regions,
    'arbitrarily_long_match_family_controls': long_matches,
    'scope': 'Finite controls. Infinite universality, nonidentification and computability reductions are hand proofs in 44m.',
}
Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
