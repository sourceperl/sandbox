import pytest
from SGERG_88 import SGERG


def test_gas1():
    sgerg = SGERG(hs=40.66, d=0.581, x_co2=0.006, x_h2=0.0)
    # 60 bara
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=-3.15)
    assert z == pytest.approx(0.840_84, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=6.85)
    assert z == pytest.approx(0.862_02, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=16.85)
    assert z == pytest.approx(0.880_07, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=36.85)
    assert z == pytest.approx(0.90881, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=56.85)
    assert z == pytest.approx(0.929_96, rel=1e-5)
    # 120 bara
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=-3.15)
    assert z == pytest.approx(0.721_46, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=6.85)
    assert z == pytest.approx(0.759_69, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=16.85)
    assert z == pytest.approx(0.792_57, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=36.85)
    assert z == pytest.approx(0.844_92, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=56.85)
    assert z == pytest.approx(0.883_22, rel=1e-5)


def test_gas2():
    sgerg = SGERG(hs=40.62, d=0.609, x_co2=0.005, x_h2=0.0)
    # 60 bara
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=-3.15)
    assert z == pytest.approx(0.833_97, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=6.85)
    assert z == pytest.approx(0.856_15, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=16.85)
    assert z == pytest.approx(0.875_00, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=36.85)
    assert z == pytest.approx(0.904_91, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=56.85)
    assert z == pytest.approx(0.926_90, rel=1e-5)
    # 120 bara
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=-3.15)
    assert z == pytest.approx(0.711_40, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=6.85)
    assert z == pytest.approx(0.750_79, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=16.85)
    assert z == pytest.approx(0.784_72, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=36.85)
    assert z == pytest.approx(0.838_77, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=56.85)
    assert z == pytest.approx(0.878_32, rel=1e-5)


def test_gas3():
    sgerg = SGERG(hs=43.53, d=0.650, x_co2=0.015, x_h2=0.0)
    # 60 bara
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=-3.15)
    assert z == pytest.approx(0.794_15, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=6.85)
    assert z == pytest.approx(0.822_10, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=16.85)
    assert z == pytest.approx(0.845_53, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=36.85)
    assert z == pytest.approx(0.882_23, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=56.85)
    assert z == pytest.approx(0.908_93, rel=1e-5)
    # 120 bara
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=-3.15)
    assert z == pytest.approx(0.643_22, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=6.85)
    assert z == pytest.approx(0.690_62, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=16.85)
    assert z == pytest.approx(0.731_96, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=36.85)
    assert z == pytest.approx(0.797_78, rel=1e-5)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=56.85)
    assert z == pytest.approx(0.845_54, rel=1e-5)


def test_gas4():
    sgerg = SGERG(hs=34.16, d=0.599, x_co2=0.016, x_h2=0.095)
    # 60 bara
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=-3.15)
    # assert z == pytest.approx(0.885_69, rel=1e-5)
