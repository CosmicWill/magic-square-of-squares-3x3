"""Check modules are imported explicitly here (no dynamic discovery) so that
``python3 -m verify`` has a deterministic, reviewable registry."""

MODULES = [
    "f1_parametrization",
    "f2_ap_pythagorean",
    "f3_no_four_ap",
    "f4_congruences",
    "f5_local_solubility",
    "f6_known_squares",
    "sanity_gauntlet",
    # populated milestone by milestone:
    "a1_hill_machinery",
    "a1_eq29",
    "a2_function_field",
    "a3_congrua",
    "a4_eight_squares",
    "a5_surface",
    "a7_curves",
    "a7_conics",
    "a7_btva",
    "a8_descent",
    "a8_h20",
    "a9_spheres",
    "a9_mechanism",
    "a6_bounds",
]


def load():
    import importlib

    for m in MODULES:
        importlib.import_module(f"{__name__}.{m}")
