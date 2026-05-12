from pytest import approx


class TestComparingDoubles:
    def test_that_passes(self):
        assert 0.1 + 0.1 + 0.1 == approx(0.3)

    def test_that_specifies_precision(self):
        assert 0.1 + 0.1 + 0.1 == approx(0.3, abs=1.0e-5)
        assert 0.1 + 0.1 + 0.1 == approx(0.3, rel=1.0e-3)
