---
title: "Biologically unavoidable sequences: a classification and related notes"
date: "10 September 2026 — research packet for discussion"
geometry: margin=1in
fontsize: 11pt
---

# The main claim

Under Definition 1 of Alexander's *Biologically unavoidable sequences* [1],
the biologically unavoidable sequences over a finite alphabet are **exactly
the eventually periodic sequences**. The new direction is an explicit avoiding
population for every other sequence. The eventually periodic direction is
Theorem 10 of the published paper (Theorem 6 of the nine-page arXiv version),
with the small proof repair below.

This packet presents a proof for scrutiny. The negative construction has
substantial Lean verification, described in the last section. Neither
independent human review nor literature priority is claimed.

We use zero-based indices and edge labels. A population is an infinite
directed graph with finitely many roots, finite outdegree at every vertex,
real birthdates strictly increasing along edges and finite sublevel sets,
and an incoming edge of each alphabet label at every non-root. A realizing
path may start at **any** vertex.

# 1. The binary construction and proof

Fix $s:\mathbb N\to\{0,1\}$ and put

$$r(2j)=s(j),\qquad r(2j+1)=1-s(j).$$

Let $P_s$ have vertices $\mathbb N$ and birthdate $t(v)=v$. For every $v\ge2$
put the following two incoming edges, and no others:

$$v-1\longrightarrow v\quad\text{with label }r(v),$$
$$v-2\longrightarrow v\quad\text{with label }1-r(v).$$

There is no edge $0\to1$. The roots are exactly 0 and 1. Vertex 0 has one
child, and each vertex $u\ge1$ has two children. Every non-root has two
distinct parents, with complementary labels. Birthdates increase strictly,
their sublevel sets are finite, and the graph is infinite. Thus these are
populations in the paper's precise edge-labelled sense.

**Claim.** If $P_s$ realizes $s$, then $s$ is eventually periodic.

Suppose $v_0,v_1,\ldots$ is an infinite matching path. Each increment is 1 or
2. Inductively,

$$v_k\ge 2k.$$

Indeed, if $v_k\ge2k+1$, the next vertex is at least $2k+2$. If $v_k=2k$,
an increment of 1 would have label $r(2k+1)=1-s(k)$, so is impossible. At
$k=0$ this edge is absent; the same conclusion holds. The base case is
$v_0\ge0$.

Consequently $d_k=v_k-2k$ is a nonnegative integer sequence with increments
in $\{-1,0\}$. It eventually stabilizes at some $d\ge0$. From some $K$
onward every path increment is therefore 2, so

$$s(k)=1-r(2k+d+2),\qquad k\ge K.$$

If $d=2e+1$, this says $s(k)=s(k+e+1)$, giving positive eventual period
$e+1$. If $d=2e$, it says $s(k)=1-s(k+e+1)$; applying the relation twice
gives period $2e+2$. Either case forces eventual periodicity.

Thus **every non-eventually-periodic binary target is avoided by its own
$P_s$, from all starting vertices**. The graph depends on the target; this
does not produce one graph avoiding every aperiodic sequence.

# 2. Finite alphabets and vertex genders

Let $A$ be finite and $s:\mathbb N\to A$ not eventually periodic. At least
one indicator projection $\pi:A\to\{0,1\}$ has a non-eventually-periodic
image $\pi\circ s$. Otherwise all finitely many symbol indicators would be
eventually periodic. Beyond the maximum of their starting thresholds, a
common multiple of their positive periods would be a period of $s$.

Construct the binary population $P_{\pi\circ s}$. Replace each vertex $v$
by the copies $(v,a)$, $a\in A$. For every binary edge $u\to v$ with label
$c$, add

$$ (u,a)\longrightarrow(v,b)\quad\text{with label }a
   \quad\text{for all }a,b\in A\text{ satisfying }\pi(a)=c.$$

Give each copy birthdate $v$. There are $2|A|$ roots, at most $2|A|$
children per vertex, and exactly one incoming parent of each label at every
non-root. The other axioms are inherited. An $s$-path would project to a
$\pi\circ s$-path in the binary population, which is impossible.

Moreover, label $a$ is the source copy's second coordinate: assigning gender
$a$ to $(v,a)$ makes this a **vertex-gendered** population. For a binary
alphabet this yields four roots and at most four children per vertex. The
smaller two-root/two-child construction uses the more general edge-labelled
definition.

**Thue–Morse example.** Put $t(k)$ equal to the parity of the number of ones
in the binary expansion of $k$. Then $t(2k)=t(k)$ and
$t(2k+1)=1-t(k)$, so the auxiliary sequence $r$ equals $t$ itself. The
incoming labels at $v$ are simply $t(v)$ and $1-t(v)$.

For completeness, $t$ is not eventually periodic. If $p>0$ were an eventual
period, then for every sufficiently large $m$, $t(2^m-p)=t(2^m)=1$.
But $2^m-p$ is the $m$-bit complement of $p-1$, so

$$t(2^m-p)=(m\bmod2)\mathbin{\mathrm{xor}}t(p-1),$$

which alternates with $m$. This is a contradiction.

# 3. A small repair to the positive direction

Write $V_j$ for the finite set of vertices reachable within $j$ edges of
a root. In Theorem 10, deleting $V_{k-1}$ can leave a surviving non-root
with only some of its required incoming labels.

For example, take vertices $a_i,b_i$ at integer time $i\ge0$, with the
time-zero pair as roots. Normally every vertex at time $i\ge1$ has parent
$a_{i-1}$ of label 0 and parent $b_{i-1}$ of label 1. Replace the label-0
parent of $a_2$ by $a_0$. Deleting the roots leaves $a_2$ with a label-1
parent but no label-0 parent.

After deleting $V_{k-1}$, also delete **all** remaining incoming edges to
the surviving boundary $V_k\backslash V_{k-1}$. Those finitely many vertices
become roots. Every vertex outside $V_k$ keeps all its original parents:
a parent in $V_{k-1}$ would put its child in $V_k$. Hence the modified
graph is a population. Apply the periodic-path theorem there, and prepend
the prescribed $k$ labels in the original graph. Its starting point lies
outside $V_{k-1}$, so these backward choices cannot reach a root too early.
The purely periodic case needs no deletion.

This repairs the proof step and preserves the positive theorem. More
generally, prepending any finite word preserves biological unavoidability
in both directions.

# 4. The other questions in the paper

## Universal avoiding populations: a scoped negative answer

Fix an avoidable sequence $s$. Interpret an embedding as an injective vertex
map preserving directed edges and their labels. Then there is no universal
population avoiding $s$. In fact, even a countable family of countable
finite-outdegree hosts cannot contain every avoiding population under these
embeddings.

Here is the argument, using the standard degree-growth diagonal obstruction
for locally finite graphs [2]. Fix one avoiding population $P$. Replace
each vertex $v$ by a nonempty finite number $f(v)$ of copies, and replace
each edge by all corresponding edges between its copy sets. Birthdates are
inherited. All axioms survive, and projection and lifting show that this
blowup has exactly the same infinite label language as $P$.

Choose a directed ray $v_0\to v_1\to\cdots$ in $P$; one exists by finite
roots, finite outdegree, and König's lemma. Enumerate all pairs of a proposed
host and one of its vertices as $(W_i,u_i)$. Let $M_i$ be the maximum
outdegree in the finite forward ball of radius $i$ about $u_i$. Set
$f(v_{i+1})=M_i+1$, and take one copy elsewhere, including at $v_0$.
If an embedding sent $v_0$ to the enumerated $u_i$, a chosen copy of $v_i$
would map inside that ball yet have at least $M_i+1$ distinct children.
Injectivity contradicts the definition of $M_i$.

The hosts need not avoid $s$. The result also excludes the more restrictive
induced or birthdate-preserving embeddings. It says nothing comparable
about noninjective homomorphisms, subdivisions, or classes with a fixed
source-degree bound. The paper's broader wording does not select one of
these conventions, so this is a scoped answer.

## Matching-tree ranks: exact barriers, but a coarse ordinal invariant

For a start $v$, let $T(v,s)$ be the tree of finite paths matching prefixes
of $s$. It is finitely branching. König's lemma gives

$$s\text{ is not realized from }v
\quad\Longleftrightarrow\quad T(v,s)\text{ has finite height}.$$

Thus $P$ avoids $s$ exactly when each starting vertex has some finite
blocking prefix. The bound may depend on the start.

Every finite word occurs somewhere in every population: choose an endpoint
outside $V_{m-1}$ for a word of length $m$, and select parents in reverse
label order. Therefore, in an avoiding population, the finite heights are
unbounded over all starts. If a super-root is attached above all the
$T(v,s)$, its well-founded rank is exactly $\omega$. This gives a precise
rank test, but that one aggregate rank cannot distinguish avoiders. It is
not a full classification by richer ordinal invariants.

## A category consequence

Let $K_v$ be the set of sequences realized from $v$. Finite branching makes
$K_v$ closed: if every finite prefix is realizable from $v$, König's lemma
gives the infinite path. The population is countable by its finite birthdate
sublevels, so $L(P)=\bigcup_vK_v$ is $F_\sigma$.

If some $K_v$ contains a cylinder of all sequences extending a finite word
$w$, deleting the $w$ part of each realizing path shows that $P$ realizes
every sequence. Thus either $P$ is universal, or every $K_v$ is nowhere
dense, $L(P)$ is meagre, and the avoided language is a dense $G_\delta$.

# 5. Why individual avoidance is compatible with many aperiodic paths

Every population has a root-starting path with labels in any prescribed
nonempty one-sided subshift $X$ (a closed, forward-shift-invariant set).

Choose $s\in X$. For arbitrarily large $N$, choose an endpoint outside
$V_{N-1}$. Its ancestor set is finite, so take a prefix of $s$ longer than
any path ending there. Prescribe that prefix backwards until a root is
reached. Reading forward gives a factor of $s$, on a root path of length at
least $N$. The forest of such factor-labelled root paths is prefix closed,
finitely branching and has finitely many roots. König's lemma gives a path
whose every prefix is a factor of $s$, hence whose labels lie in $X$.

Apply this to the orbit closure of a mechanical word
$s_\alpha(k)=\lfloor(k+1)\alpha\rfloor-\lfloor k\alpha\rfloor$. Every
block of length $m$ has a number of ones differing from $m\alpha$ by less
than one. The root path in that orbit closure therefore has frequency
$\alpha$. For irrational $\alpha$ it is aperiodic, and different slopes
give different sequences. **Every binary population realizes continuum
many aperiodic sequences**, despite every individual aperiodic sequence
having an avoiding population.

# 6. Universality and finite observation in the new family

The construction has a second exact property:

$$P_s\text{ realizes every binary sequence}
\quad\Longleftrightarrow\quad s\text{ is eventually periodic}.$$

The negative direction is §1. If $s$ has eventual period $p$, then $r$ has
eventual period $q=2p$. Form a finite residue multigraph modulo $q$, with
the two incoming transitions into residue $a$, labelled by the eventual
$r(a)$ and its complement, and marked with delays 1 and 2. Every state
has an incoming transition of each label. Every finite word can therefore
be read backwards; finite branching and finitely many possible starts give
an infinite path for every infinite word. Starting sufficiently late in
$P_s$, lift each transition by its marked delay. This realizes the word in
the actual population. The marked delays retain the information needed
to lift the quotient path.

The graph through vertex $N$ depends only on $s(0),\ldots,s(\lfloor N/2\rfloor)$.
Any such prefix can be continued with zeros or with Thue–Morse. The resulting
populations agree on that entire finite region, but one is universal and
the other is not. This also obstructs any finite adaptive sequence of local
edge queries.

Even a program describing the graph does not decide universality. Given a
machine $M$, let $s_M(k)$ be the $k$th Thue–Morse bit if $M$ has not halted
within $k$ steps, and zero otherwise. This sequence and its graph are total
computable objects. The graph is universal exactly when $M$ halts. Conversely,
using zeros until a halt is detected and then starting a Thue–Morse tail
gives a universal graph exactly when $M$ never halts. Thus neither universality
nor non-universality is semidecidable on these presentations, even with the
promise that all population axioms hold.

For a fixed aperiodic $s$, breadth-first matching from any vertex terminates
with an empty set by §1 and König's lemma. There is no bound uniform in the
target even for starting vertex 1: a target with $N+1$ initial zeros and an
aperiodic tail admits $N$ matching edges along $v_k=1+2k$. Obtaining useful
explicit bounds for the fixed Thue–Morse target remains a quantitative question.

# Verification and questions for discussion

The included Lean source checks the binary path argument, the indicator
reduction, and all population axioms for the finite-alphabet construction
using natural-valued birthdates. Embedding those dates in the reals is a
hand argument in this snapshot: for any real $R$, choose a natural $T>R$
and use the finite strict sublevel below $T$. The positive theorem,
Thue–Morse aperiodicity, and the other extensions above are hand proofs.

The recorded Lean 4.32.0-rc1 check exits successfully; its printed endpoints
use only `propext`, `Classical.choice`, and `Quot.sound`. The finite Python
controls independently transcribe edges and matching sets. They supplement
the proofs, and do not establish infinite claims by extrapolation.

The user selected the paper and directed the research. OpenAI Codex developed
the construction, proofs, formalization and exposition. No independent human
mathematical review is recorded. We would especially welcome corrections to
the definition correspondence, pointers to earlier solutions, and clarification
of the intended universal-object notion. The manuscript's final classification
question is answered by the proposed proof; its full range of ordinal or
embedding questions is not claimed to be exhausted.

# References

1. Samuel A. Alexander, *Biologically unavoidable sequences*, Electronic
   Journal of Combinatorics **20**(1) (2013), P31.
   [Published paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v20i1p31/pdf/),
   [DOI](https://doi.org/10.37236/3035),
   [arXiv:1212.0186](https://arxiv.org/abs/1212.0186).
   We refer to the published Definition 1, Theorem 10 and §6.
2. Florian Lehner, *A note on classes of subgraphs of locally finite graphs*,
   [author-hosted primary paper](https://www.florian-lehner.net/pdf/universal-locally-finite.pdf).
   Used for the antecedent degree-growth obstruction; the label-language
   preserving blowup above is spelled out separately.
