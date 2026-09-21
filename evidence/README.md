# Optional evidence

The note can be read without running anything here.

- `44l-binary-avoidance.lean`: the checked finite-alphabet negative construction with natural-number birthdates.
- `44l-binary-avoidance.log`: recorded successful Lean 4.32.0-rc1 check; the printed endpoints use only `propext`, `Classical.choice`, and `Quot.sound`.
- `44k-classification-checks.py` and `.json`: independent finite graph and path controls.
- `44n-observation-controls.py` and `.json`: finite controls for periodic-template lifting and indistinguishable observations.

Run any Python file with Python 3; it uses only the standard library and writes its result beside itself. The Lean source imports mathlib at commit `360da6fa66c1273b76b6b2d8c5666fd5ac2e3b56`. This compact author packet includes the original checked source and log; it does not vendor mathlib. The separately prepared submission package provides a pinned project and reproduction runner.

Finite controls do not prove infinite avoidance. The proof and its quantifiers are in `../results.md` and the Lean file. The log is local verification, not independent human review.

September 20/21 additions: `44s-complement-barrier-checks.py` / `.json` check complementary targets and the quantitative Thue–Morse bound. `44u-countable-avoidance-checks.py` / `.json` check finite extensions, persistent staged certificates and general-alphabet cyclic labels. Their infinite claims are proved in the two new addenda; the older Lean log does not cover them.
