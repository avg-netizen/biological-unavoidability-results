import Mathlib.Data.Nat.Find
import Mathlib.Order.Monotone.Basic
import Mathlib.Data.Finset.Prod
import Mathlib.Data.Fintype.Prod

/- Binary negative direction of inquiry 44j. No population-existence assumptions
are hidden in the path theorem: vertices and labelled edges are defined below. -/
namespace BiologicalAvoidance

def interleave (s : ℕ → Bool) (v : ℕ) : Bool :=
  if v % 2 = 0 then s (v / 2) else !(s (v / 2))

def Edge (s : ℕ → Bool) (u v : ℕ) (a : Bool) : Prop :=
  2 ≤ v ∧ ((v = u + 1 ∧ a = interleave s v) ∨
            (v = u + 2 ∧ a = !(interleave s v)))

def EventuallyPeriodic {A : Type*} (s : ℕ → A) : Prop :=
  ∃ K p : ℕ, 0 < p ∧ ∀ k, K ≤ k → s (k + p) = s k

lemma interleave_even (s : ℕ → Bool) (k : ℕ) :
    interleave s (2*k) = s k := by
  simp [interleave, Nat.mul_comm]

lemma interleave_odd (s : ℕ → Bool) (k : ℕ) :
    interleave s (2*k+1) = !(s k) := by
  simp [interleave, Nat.add_div, Nat.mul_comm]

lemma parents (s : ℕ → Bool) (v : ℕ) (hv : 2 ≤ v) :
    Edge s (v-1) v (interleave s v) ∧
    Edge s (v-2) v (!(interleave s v)) := by
  constructor
  · exact ⟨hv, Or.inl ⟨by omega, rfl⟩⟩
  · exact ⟨hv, Or.inr ⟨by omega, rfl⟩⟩

lemma every_label_parent (s : ℕ → Bool) (v : ℕ) (hv : 2 ≤ v) (a : Bool) :
    ∃ u, Edge s u v a := by
  obtain ⟨h1,h2⟩ := parents s v hv
  cases h : interleave s v <;> cases a <;> simp_all
  all_goals first | exact ⟨v-1,h1⟩ | exact ⟨v-2,h2⟩

theorem path_forces_eventual_periodicity (s : ℕ → Bool) (v : ℕ → ℕ)
    (hpath : ∀ k, Edge s (v k) (v (k+1)) (s k)) : EventuallyPeriodic s := by
  classical
  have lower : ∀ k, 2*k ≤ v k := by
    intro k
    induction k with
    | zero => omega
    | succ k ih =>
      obtain ⟨_, h | h⟩ := hpath k
      · obtain ⟨step, lab⟩ := h
        by_cases eq : v k = 2*k
        · have pos : v (k+1) = 2*k+1 := by omega
          rw [pos, interleave_odd] at lab
          cases hs : s k <;> simp_all
        · omega
      · omega
  let d : ℕ → ℕ := fun k => v k - 2*k
  have dstep : ∀ k, d (k+1) ≤ d k := by
    intro k
    have h := hpath k
    have h0 := lower k
    have h1 := lower (k+1)
    dsimp [d]
    rcases h.2 with h | h <;> omega
  have anti : Antitone d := antitone_nat_of_succ_le dstep
  have hex : ∃ n, ∃ k, d k = n := ⟨d 0, 0, rfl⟩
  obtain ⟨K, hK⟩ := Nat.find_spec hex
  have stable : ∀ k, K ≤ k → d k = d K := by
    intro k hk
    have lo : Nat.find hex ≤ d k := Nat.find_min' hex ⟨k,rfl⟩
    have hi := anti hk
    omega
  have position : ∀ k, K ≤ k → v k = 2*k + d K := by
    intro k hk
    have h0 := lower k
    have h1 := stable k hk
    dsimp [d] at h1 ⊢
    omega
  have tail_label : ∀ k, K ≤ k → s k = !(interleave s (2*k+d K+2)) := by
    intro k hk
    have p0 := position k hk
    have p1 := position (k+1) (by omega)
    obtain ⟨_, h | h⟩ := hpath k
    · omega
    · obtain ⟨_, lab⟩ := h
      have eq : v (k+1) = 2*k+d K+2 := by omega
      simpa [eq] using lab
  let e := d K / 2
  have split : d K = 2*e ∨ d K = 2*e+1 := by dsimp [e]; omega
  rcases split with even | odd
  · have flip : ∀ k, K ≤ k → s k = !(s (k+e+1)) := by
      intro k hk
      have h := tail_label k hk
      have eq : 2*k+d K+2 = 2*(k+e+1) := by omega
      simpa [eq, interleave_even] using h
    refine ⟨K, 2*(e+1), by omega, ?_⟩
    intro k hk
    have h1 := flip k hk
    have h2 := flip (k+e+1) (by omega)
    have eq : k+e+1+e+1 = k+2*(e+1) := by omega
    rw [eq] at h2
    cases h0 : s k <;> cases hmid : s (k+e+1) <;>
      cases hend : s (k+2*(e+1)) <;> simp_all
  · refine ⟨K, e+1, by omega, ?_⟩
    intro k hk
    have h := tail_label k hk
    have eq : 2*k+d K+2 = 2*(k+e+1)+1 := by omega
    simpa [eq, interleave_odd, Nat.add_assoc] using h.symm

theorem binary_avoidance (s : ℕ → Bool) (h : ¬ EventuallyPeriodic s) :
    ¬ ∃ v : ℕ → ℕ, ∀ k, Edge s (v k) (v (k+1)) (s k) := by
  rintro ⟨v,hv⟩
  exact h (path_forces_eventual_periodicity s v hv)

/- Every finite family of eventually periodic coordinate sequences has a
common eventual period. This closes the indicator-projection reduction. -/
lemma period_multiple {A : Type*} (s : ℕ → A) (K p : ℕ)
    (h : ∀ k, K ≤ k → s (k+p) = s k) (n k : ℕ) (hk : K ≤ k) :
    s (k+p*n) = s k := by
  induction n with
  | zero => simp
  | succ n ih =>
    calc
      s (k+p*(n+1)) = s ((k+p*n)+p) := by simp [Nat.mul_add, Nat.add_assoc]
      _ = s (k+p*n) := h _ (by omega)
      _ = s k := ih

lemma common_period {A : Type*} (F : Finset A) (q : A → ℕ → Bool)
    (h : ∀ a ∈ F, EventuallyPeriodic (q a)) :
    ∃ K p : ℕ, 0 < p ∧ ∀ k, K ≤ k → ∀ a ∈ F, q a (k+p) = q a k := by
  classical
  induction F using Finset.induction_on with
  | empty => exact ⟨0, 1, by omega, by simp⟩
  | @insert a F ha ih =>
    obtain ⟨Ka, pa, hpa, hqa⟩ := h a (by simp)
    obtain ⟨KF, pF, hpF, hqF⟩ := ih (fun b hb => h b (by simp [hb]))
    refine ⟨max Ka KF, pa*pF, Nat.mul_pos hpa hpF, ?_⟩
    intro k hk b hb
    rcases Finset.mem_insert.mp hb with rfl | hb
    · exact period_multiple (q b) Ka pa hqa pF k (by omega)
    · have ht : ∀ j, KF ≤ j → q b (j+pF) = q b j := fun j hj => hqF j hj b hb
      simpa [Nat.mul_comm] using period_multiple (q b) KF pF ht pa k (by omega)

theorem aperiodic_indicator {A : Type*} [Fintype A] (s : ℕ → A)
    (h : ¬ EventuallyPeriodic s) :
    ∃ pi : A → Bool, ¬ EventuallyPeriodic (fun k => pi (s k)) := by
  classical
  by_contra hn
  let q : A → ℕ → Bool := fun a k => decide (s k = a)
  have all : ∀ a ∈ (Finset.univ : Finset A), EventuallyPeriodic (q a) := by
    intro a _
    by_contra ha
    exact hn ⟨fun b => decide (b = a), ha⟩
  obtain ⟨K, p, hp, hq⟩ := common_period Finset.univ q all
  apply h
  refine ⟨K, p, hp, ?_⟩
  intro k hk
  have heq := hq k hk (s k) (Finset.mem_univ _)
  simpa [q] using heq

/- Explicit population axioms with natural-valued birthdates. Finite sets
cover roots, children, and each strict birthdate sublevel. Natural birthdates
also satisfy the paper's real-birthdate condition by the standard embedding. -/
structure IsPopulation {A V : Type*} (E : V → V → A → Prop) (birth : V → ℕ) : Prop where
  label_unique : ∀ u v a b, E u v a → E u v b → a = b
  roots_finite : ∃ F : Finset V, ∀ v, (¬ ∃ u a, E u v a) → v ∈ F
  children_finite : ∀ u, ∃ F : Finset V, ∀ v a, E u v a → v ∈ F
  birth_finite : ∀ t, ∃ F : Finset V, ∀ v, birth v < t → v ∈ F
  born_lt : ∀ u v a, E u v a → birth u < birth v
  parents : ∀ v, (∃ u a, E u v a) → ∀ a, ∃ u, E u v a
  vertices_infinite : Infinite V

theorem binary_population (s : ℕ → Bool) : IsPopulation (Edge s) id := by
  constructor
  · intro u v a b ha hb
    rcases ha.2 with ha | ha <;> rcases hb.2 with hb | hb <;> first | omega | exact ha.2.trans hb.2.symm
  · refine ⟨Finset.range 2, ?_⟩
    intro v hv
    have hlt : v < 2 := by
      by_contra hn
      exact hv ⟨v-1, interleave s v, (parents s v (by omega)).1⟩
    exact Finset.mem_range.mpr hlt
  · intro u
    refine ⟨Finset.range (u+3), ?_⟩
    intro v a h
    apply Finset.mem_range.mpr
    rcases h.2 with h | h <;> omega
  · intro t
    exact ⟨Finset.range t, fun v hv => Finset.mem_range.mpr hv⟩
  · intro u v a h
    rcases h.2 with h | h <;> dsimp <;> omega
  · intro v hv a
    obtain ⟨u, b, hb⟩ := hv
    exact every_label_parent s v hb.1 a
  · infer_instance

def LiftEdge {A : Type*} (s : ℕ → A) (pi : A → Bool)
    (u v : ℕ × A) (a : A) : Prop :=
  a = u.2 ∧ Edge (fun k => pi (s k)) u.1 v.1 (pi a)

theorem lift_population {A : Type*} [Fintype A] (s : ℕ → A) (pi : A → Bool) :
    IsPopulation (LiftEdge s pi) Prod.fst := by
  classical
  letI : Nonempty A := ⟨s 0⟩
  constructor
  · intro u v a b ha hb
    exact ha.1.trans hb.1.symm
  · refine ⟨(Finset.range 2).product Finset.univ, ?_⟩
    intro v hv
    have hlt : v.1 < 2 := by
      by_contra hn
      obtain ⟨u, hu⟩ := every_label_parent (fun k => pi (s k)) v.1 (by omega) (pi (s 0))
      exact hv ⟨(u, s 0), s 0, rfl, hu⟩
    simpa using hlt
  · intro u
    refine ⟨(Finset.range (u.1+3)).product Finset.univ, ?_⟩
    intro v a h
    have hlt : v.1 < u.1+3 := by rcases h.2.2 with h | h <;> omega
    simpa using hlt
  · intro t
    refine ⟨(Finset.range t).product Finset.univ, ?_⟩
    intro v hv
    simpa using hv
  · intro u v a h
    rcases h.2.2 with h | h <;> omega
  · intro v hv a
    obtain ⟨u, b, hb⟩ := hv
    obtain ⟨w, hw⟩ := every_label_parent (fun k => pi (s k)) v.1 hb.2.1 (pi a)
    exact ⟨(w, a), rfl, hw⟩
  · infer_instance

theorem finite_alphabet_avoidance {A : Type*} [Fintype A] (s : ℕ → A)
    (h : ¬ EventuallyPeriodic s) :
    ∃ E : (ℕ × A) → (ℕ × A) → A → Prop,
      IsPopulation E Prod.fst ∧
      ¬ ∃ v : ℕ → ℕ × A, ∀ k, E (v k) (v (k+1)) (s k) := by
  obtain ⟨pi, hpi⟩ := aperiodic_indicator s h
  refine ⟨LiftEdge s pi, lift_population s pi, ?_⟩
  rintro ⟨v, hv⟩
  exact binary_avoidance (fun k => pi (s k)) hpi ⟨fun k => (v k).1, fun k => (hv k).2⟩

#print axioms path_forces_eventual_periodicity
#print axioms binary_population
#print axioms finite_alphabet_avoidance
end BiologicalAvoidance
