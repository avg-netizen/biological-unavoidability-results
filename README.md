# Results concerning biologically unavoidable sequences

Prepared 10 September 2026 for Samuel A. Alexander. This is a research packet
for discussion, not a journal submission or a claim of established priority.

Start with **[results.pdf](results.pdf)**, or the equivalent
[HTML](results.html) / [Markdown](results.md). The main construction and proof
are self-contained. The later sections give scoped answers and extensions to
the questions in *Biologically unavoidable sequences*.

**September 20/21 continuation:**
[countable-avoidance.md](countable-avoidance.md) proves simultaneous avoidance
of any prescribed countable family of aperiodic targets, at optimal outdegree
for every finite alphabet. [complement-and-barriers.md](complement-and-barriers.md)
gives explicit complement avoidance and an $O((i+1)\log(i+2))$ Thue–Morse
matching cutoff. PDF and HTML versions of both addenda are included. These
new hand arguments and finite controls are outside the older Lean coverage.

- [cover-note.md](cover-note.md) is an editable covering-message draft.
- [additional-results.pdf](additional-results.pdf) is an optional supplement
  on root-path spread, minimum branching and a directional CA bound; its
  [Markdown source](additional-results.md) is included.
- [evidence/](evidence/README.md) contains optional Lean and Python evidence.
- [PROVENANCE.md](PROVENANCE.md) records origin, verification and source limits.

The central claim is that every non-eventually-periodic finite-alphabet
sequence has an avoiding population. The binary construction has two roots
and at most two children per vertex. Combined with your positive theorem,
this gives the classification by eventual periodicity.

Feedback would be particularly helpful on the correspondence with Definition 1,
any subsequent work we have missed, and the intended embedding convention in
the universality question. No claim is made to have settled every possible
ordinal characterization of realizing populations.
