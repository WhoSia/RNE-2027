from fractions import Fraction
from itertools import product
from types import SimpleNamespace
from unittest import TestCase

from joint_pocket_sensing import joint_policy
from uncertain_pocket_sensing import ACTIONS, erasure_policy, reading_support


def exhaustive(groups, capacity, mode, upper):
    states = [
        (reading, delta)
        for count, bounds in groups.items()
        for reading in reading_support(count, capacity, mode)
        for delta in range(bounds.low, bounds.high + 1)
    ]
    readings = sorted({reading for reading, _ in states})

    def loss(choice, delta):
        return max(0, delta if choice == "lead" else -delta)

    return min(
        max(
            (1 - probability) * loss(policy[reading], delta) + probability * loss(fallback, delta)
            for reading, delta in states
            for probability in (0, upper / 2, upper)
        )
        for fallback in ACTIONS
        for actions in product(ACTIONS, repeat=len(readings))
        for policy in (dict(zip(readings, actions, strict=True)),)
    )


class JointPocketSensing(TestCase):
    def test_branch_optimum_matches_independent_enumeration(self):
        for middle in (None, (-5, 1), (-2, -1), (1, 3)):
            groups = {0: SimpleNamespace(low=3, high=5), 3: SimpleNamespace(low=-7, high=-2)}
            if middle is not None:
                groups[1] = SimpleNamespace(low=middle[0], high=middle[1])
            for mode, upper in product(
                ("exact", "fullness", "miss_one", "off_by_one"),
                map(Fraction, ("0", "1/10", "1/2", "1")),
            ):
                with self.subTest(middle=middle, mode=mode, upper=upper):
                    result, _ = joint_policy(groups, 3, mode, upper)
                    self.assertEqual(result, exhaustive(groups, 3, mode, upper))
                    if mode == "exact":
                        self.assertEqual(result, erasure_policy(groups, upper)[0])

    def test_flag_does_not_rescue_an_ambiguous_reading(self):
        groups = {0: SimpleNamespace(low=5, high=5), 2: SimpleNamespace(low=-7, high=-7)}
        result, _ = joint_policy(groups, 2, "off_by_one", Fraction(1, 4))
        self.assertEqual(result, 5)
