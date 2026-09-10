---
title: "Additional structural and cellular-automaton observations"
date: "10 September 2026 — optional supplement"
geometry: margin=1in
fontsize: 11pt
---

These hand arguments supplement the main author note. They are not part of
the supplied Lean certificate, and no literature priority is claimed. The
first two use Alexander's population axioms as stated in the main note.

# 1. Bounded root-path spread forces universality

Let $d(v)$ and $D(v)$ be the shortest and longest root-to-$v$ path lengths.
Both exist because the ancestor set is finite. Put $\Delta(v)=D(v)-d(v)$.

**Proposition.** If $\Delta(v)\le K$ at infinitely many vertices, for some
fixed finite $K$, then every label sequence is realized. More precisely,
each sequence is realized from some vertex within $K$ edges of a root.

Fix a desired sequence $s$ and prepend any word of length $K$, obtaining
$a$. At a vertex $v$ with $\Delta(v)\le K$, prescribe the first $D(v)$
symbols of $a$ backwards until a root is reached. If the resulting path
has length $\ell$, then

$$d(v)\le\ell\le D(v),\qquad j=D(v)-\ell\in\{0,\ldots,K\}.$$

Read forwards, its labels are $a[j:D(v)]$. Delete the first $K-j$ edges.
The remaining path starts within $K$ edges of a root and spells the first
$D(v)-K$ symbols of $s$, whenever $D(v)\ge K$. The infinitely many chosen
vertices have unbounded $d(v)$, because only finitely many vertices are
reachable within any fixed number of steps from the finitely many roots.
Thus arbitrarily long prefixes of $s$ occur from the finite set $V_K$.
König's lemma supplies an infinite realization.

Consequently every non-universal population has only finitely many vertices
with $\Delta(v)\le K$, for each finite $K$. In particular, a population
whose edges all advance one synchronous generation realizes every sequence;
such a search restriction cannot produce an avoider. The construction in
the main note uses edge lengths 1 and 2.

# 2. Minimum uniform branching and finite degree defects

For an $n$-letter alphabet, a population cannot have outdegree at most $n-1$
at every vertex. If $F$ is finite, ancestrally closed, contains all $r$ roots,
and has $N$ vertices, then

$$n(N-r)\le |E(F)|\le(n-1)N,$$

forcing $N\le nr$. Such sets exhaust the infinite graph, a contradiction.
For example take increasing birthdate sublevels containing all roots.

If instead every outdegree is at most $n$, set
$o(v)=n-\operatorname{outdeg}(v)$ and
$i(v)=\operatorname{indeg}(v)-n$ for non-roots. Both are nonnegative.
Exact counting on the same ancestral sets gives

$$|E(F,V\backslash F)|=nr-\sum_{v\in F}o(v)
 -\sum_{\substack{v\in F\\v\text{ not a root}}}i(v).$$

Hence the total integer degree defect is at most $nr$. Outside finitely
many exceptional vertices, indegree and outdegree are exactly $n$, with
one incoming edge of each label. Every such ancestral cut has at most $nr$
crossing edges. The binary avoiding construction lies at this minimum
uniform branching threshold; degree two does not force universality.

# 3. A directional CA bound under incomplete rule information

Let $D$ be a finite set of spatial displacements from a parent cell to a
child. Assume a newborn has at least $b\ge1$ distinct live predecessors
among those displacements, and a survivor remains at its own position.
For a nonempty finite live configuration, put

$$H_a(t)=\max\{a\cdot z:z\text{ is live at time }t\},$$

where $a$ is any linear spatial direction, and let

$$\kappa_b(a)=\max\bigl(0,\text{the }b\text{th largest of }
                           \{a\cdot d:d\in D\}\bigr).$$

**Proposition.** $H_a(t+1)\le H_a(t)+\kappa_b(a)$ whenever the next
configuration is nonempty, hence $H_a(t)\le H_a(0)+t\kappa_b(a)$ while
live cells remain.

Among any $b$ live predecessor displacements, at least one has projection
at most the $b$th largest projection in all of $D$. For a birth at $z$,
choose that predecessor $z-d$. Then

$$a\cdot z=a\cdot(z-d)+a\cdot d\le H_a(t)+\kappa_b(a).$$

Survivors satisfy the same inequality because $\kappa_b(a)\ge0$.
An empty configuration cannot produce births under $b\ge1$, so the
undefined maximum on an empty set causes no need for a new case of the bound.

This supplies a spatial envelope without specifying the entire local rule.
It does not predict the future configuration or assert existence of a
spaceship achieving the envelope. It is closely related to the established
CA speed-limit arguments of Nathaniel Johnston, *The B36/S125 “2x2” Life-Like
Cellular Automaton*, [arXiv:1203.1644](https://arxiv.org/abs/1203.1644),
Section 3, and Alexander's application. It is included as a reusable
formulation under partial rule information, not advertised as a new sharp
speed-limit theorem.
