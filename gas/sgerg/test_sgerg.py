import pytest
from SGERG_88 import SGERG

# some const
TOLERANCE = 1e-4


def test_gas1():
    sgerg = SGERG(hs=40.66, d=0.581, x_co2=0.006, x_h2=0.0)
    # 60 bara
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=-3.15)
    assert z == pytest.approx(0.840_84, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=6.85)
    assert z == pytest.approx(0.862_02, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=16.85)
    assert z == pytest.approx(0.880_07, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=36.85)
    assert z == pytest.approx(0.90881, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=56.85)
    assert z == pytest.approx(0.929_96, rel=TOLERANCE)
    # 120 bara
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=-3.15)
    assert z == pytest.approx(0.721_46, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=6.85)
    assert z == pytest.approx(0.759_69, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=16.85)
    assert z == pytest.approx(0.792_57, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=36.85)
    assert z == pytest.approx(0.844_92, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=56.85)
    assert z == pytest.approx(0.883_22, rel=TOLERANCE)


def test_gas2():
    sgerg = SGERG(hs=40.62, d=0.609, x_co2=0.005, x_h2=0.0)
    # 60 bara
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=-3.15)
    assert z == pytest.approx(0.833_97, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=6.85)
    assert z == pytest.approx(0.856_15, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=16.85)
    assert z == pytest.approx(0.875_00, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=36.85)
    assert z == pytest.approx(0.904_91, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=56.85)
    assert z == pytest.approx(0.926_90, rel=TOLERANCE)
    # 120 bara
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=-3.15)
    assert z == pytest.approx(0.711_40, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=6.85)
    assert z == pytest.approx(0.750_79, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=16.85)
    assert z == pytest.approx(0.784_72, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=36.85)
    assert z == pytest.approx(0.838_77, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=56.85)
    assert z == pytest.approx(0.878_32, rel=TOLERANCE)


def test_gas3():
    sgerg = SGERG(hs=43.53, d=0.650, x_co2=0.015, x_h2=0.0)
    # 60 bara
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=-3.15)
    assert z == pytest.approx(0.794_15, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=6.85)
    assert z == pytest.approx(0.822_10, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=16.85)
    assert z == pytest.approx(0.845_53, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=36.85)
    assert z == pytest.approx(0.882_23, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=56.85)
    assert z == pytest.approx(0.908_93, rel=TOLERANCE)
    # 120 bara
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=-3.15)
    assert z == pytest.approx(0.643_22, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=6.85)
    assert z == pytest.approx(0.690_62, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=16.85)
    assert z == pytest.approx(0.731_96, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=36.85)
    assert z == pytest.approx(0.797_78, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=56.85)
    assert z == pytest.approx(0.845_54, rel=TOLERANCE)


def test_gas4():
    sgerg = SGERG(hs=34.16, d=0.599, x_co2=0.016, x_h2=0.095)
    # 60 bara
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=-3.15)
    # assert z == pytest.approx(0.885_69, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=6.85)
    # assert z == pytest.approx(0.901_50, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=16.85)
    # assert z == pytest.approx(0.915_07, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=36.85)
    # assert z == pytest.approx(0.936_84, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=56.85)
    # assert z == pytest.approx(0.953_02, rel=TOLERANCE)
    # 120 bara
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=-3.15)
    # assert z == pytest.approx(0.808_43, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=6.85)
    # assert z == pytest.approx(0.836_13, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=16.85)
    # assert z == pytest.approx(0.859_99, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=36.85)
    # assert z == pytest.approx(0.898_27, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=56.85)
    # assert z == pytest.approx(0.926_62, rel=TOLERANCE)


def test_gas5():
    sgerg = SGERG(hs=36.64, d=0.686, x_co2=0.076, x_h2=0.0)
    # 60 bara
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=-3.15)
    assert z == pytest.approx(0.826_64, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=6.85)
    assert z == pytest.approx(0.850_17, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=16.85)
    assert z == pytest.approx(0.870_03, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=36.85)
    assert z == pytest.approx(0.901_24, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=56.85)
    assert z == pytest.approx(0.923_94, rel=TOLERANCE)
    # 120 bara
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=-3.15)
    assert z == pytest.approx(0.695_57, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=6.85)
    assert z == pytest.approx(0.738_28, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=16.85)
    assert z == pytest.approx(0.774_63, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=36.85)
    assert z == pytest.approx(0.831_66, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=56.85)
    assert z == pytest.approx(0.872_69, rel=TOLERANCE)


def test_gas6():
    sgerg = SGERG(hs=36.58, d=0.644, x_co2=0.011, x_h2=0.0)
    # 60 bara
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=-3.15)
    # assert z == pytest.approx(0.854_06, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=6.85)
    assert z == pytest.approx(0.873_88, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=16.85)
    assert z == pytest.approx(0.890_71, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=36.85)
    # assert z == pytest.approx(0.917_36, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=60.0, t_celsius=56.85)
    assert z == pytest.approx(0.936_90, rel=TOLERANCE)
    # 120 bara
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=-3.15)
    assert z == pytest.approx(0.749_39, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=6.85)
    assert z == pytest.approx(0.784_73, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=16.85)
    assert z == pytest.approx(0.814_90, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=36.85)
    assert z == pytest.approx(0.862_66, rel=TOLERANCE)
    z, _rho_m = sgerg.run(p_bar=120.0, t_celsius=56.85)
    assert z == pytest.approx(0.897_49, rel=TOLERANCE)
