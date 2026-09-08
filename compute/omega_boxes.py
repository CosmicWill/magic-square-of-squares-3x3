"""Class enumeration for any number of split primes with every exponent 1 (entry 127): the box
(1, ..., 1) with N frames.  Labels are the nonzero vectors of {-1, 0, 1}^N up to sign; a class is four
labels A, B, C, D with signs eps, taken up to the frame group (S_N x conjugations), the global sign and
the A<->B swap (which flips eps_D) -- the same canonical form as omega3.canon_cand, whose (1,1,1)
enumeration this reproduces exactly (750 three-frame lemma survivors of 2916 three-frame classes).
Only classes using every frame are enumerated ('N-frame classes'); the prime-column lemma may be applied
before canonicalisation, being invariant under the group.  No curve engine exists beyond N = 3: these
classes are decided by the lemma and the height system alone."""
from itertools import permutations, product


def labels_of(N):
    return [lab for lab in product((-1, 0, 1), repeat=N) if any(lab) and next(x for x in lab if x != 0) > 0]


def canon_lab(lab, eps):
    fn = next(x for x in lab if x != 0)
    if fn < 0:
        return tuple(-x for x in lab), -eps
    return tuple(lab), eps


def group_table(N):
    """TABLE[g][lab] = (image label, sign picked up) for every element g of S_N x conjugations."""
    labs = labels_of(N)
    table = []
    for perm in permutations(range(N)):
        for conj in product((1, -1), repeat=N):
            table.append({lab: canon_lab(tuple(conj[i] * lab[perm[i]] for i in range(N)), 1) for lab in labs})
    return table


def canon(cand, table):
    A, B, C, D, eA, eB, eC, eD = cand
    best = None
    for tab in table:
        a, sa = tab[A]; b, sb = tab[B]; c, sc = tab[C]; d, sd = tab[D]
        ea, eb, ec, ed = eA * sa, eB * sb, eC * sc, eD * sd
        key1 = (a, b, c, d, ea, eb, ec, ed) if ea > 0 else (a, b, c, d, -ea, -eb, -ec, -ed)
        key2 = (b, a, c, d, eb, ea, ec, -ed) if eb > 0 else (b, a, c, d, -eb, -ea, -ec, ed)
        if best is None or key1 < best:
            best = key1
        if key2 < best:
            best = key2
    return best


def lemma_fails(labels):
    """The prime-column lemma on four labels (any number of columns)."""
    for j in range(len(labels[0])):
        mags = [abs(lab[j]) for lab in labels]
        M = max(mags)
        if M and mags.count(M) < 3:
            return True
    return False


def enumerate_classes(N, lemma_filter=True, table=None):
    """The canonical N-frame classes (all frames used), optionally only those passing the lemma.
    Returns (classes, counts) with counts = {raw, n_frame, lemma_pass_raw} over the raw quadruples
    (A one of the N orbit representatives, B < ... as generated, signs eB, eC, eD, eA = 1)."""
    labs = labels_of(N)
    table = table or group_table(N)
    reps = [tuple([1] * k + [0] * (N - k)) for k in range(1, N + 1)]
    out = set(); n_raw = n_frame = n_pass = 0
    for A in reps:
        for B in labs:
            if B == A:
                continue
            rest = [x for x in labs if x not in (A, B)]
            for C, D in permutations(rest, 2):
                labels = (A, B, C, D)
                n_raw += 8
                if not all(any(lab[j] != 0 for lab in labels) for j in range(N)):
                    continue
                n_frame += 8
                if lemma_filter and lemma_fails(labels):
                    continue
                n_pass += 8
                for eB, eC, eD in product((1, -1), repeat=3):
                    out.add(canon((A, B, C, D, 1, eB, eC, eD), table))
    return sorted(out), {"raw": n_raw, "n_frame": n_frame, "lemma_pass_raw": n_pass}
