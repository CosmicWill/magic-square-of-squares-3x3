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
    "a2_function_field",
    "a3_congrua",
    "a4_eight_squares",
]


def load():
    import importlib

    for m in MODULES:
        importlib.import_module(f"{__name__}.{m}")
