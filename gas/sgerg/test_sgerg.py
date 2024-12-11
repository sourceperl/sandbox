from SGERG_88 import SGERG


def valid_sgerg(sgerg: SGERG, p_bar: float, t_celsius: float, z_ref: float, tolerance: float):
    z, _rho_m = sgerg.run(p_bar=p_bar, t_celsius=t_celsius)
    diff_as_percent = 100.0 * (z - z_ref)/z_ref
    assert -tolerance < diff_as_percent < tolerance, \
        f'z_ref: {z_ref} z: {z} diff {diff_as_percent:.3f}% (hs :{sgerg.hs})'


def test_gas1():
    sgerg = SGERG(hs=40.66, d=0.581, x_co2=0.006, x_h2=0.0)
    # 60 bara
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=-3.15, z_ref=0.840_84, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=6.85, z_ref=0.862_02, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=16.85, z_ref=0.880_07, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=36.85, z_ref=0.908_81, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=56.85, z_ref=0.929_96, tolerance=0.01)
    # 120 bara
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=-3.15, z_ref=0.721_46, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=6.85, z_ref=0.759_69, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=16.85, z_ref=0.792_57, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=36.85, z_ref=0.844_92, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=56.85, z_ref=0.883_22, tolerance=0.01)


def test_gas2():
    sgerg = SGERG(hs=40.62, d=0.609, x_co2=0.005, x_h2=0.0)
    # 60 bara
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=-3.15, z_ref=0.833_97, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=6.85, z_ref=0.856_15, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=16.85, z_ref=0.875_00, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=36.85, z_ref=0.904_91, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=56.85, z_ref=0.926_90, tolerance=0.01)
    # 120 bara
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=-3.15, z_ref=0.711_40, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=6.85, z_ref=0.750_79, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=16.85, z_ref=0.784_72, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=36.85, z_ref=0.838_77, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=56.85, z_ref=0.878_32, tolerance=0.01)


def test_gas3():
    sgerg = SGERG(hs=43.53, d=0.650, x_co2=0.015, x_h2=0.0)
    # 60 bara
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=-3.15, z_ref=0.794_15, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=6.85, z_ref=0.822_10, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=16.85, z_ref=0.845_53, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=36.85, z_ref=0.882_23, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=56.85, z_ref=0.908_93, tolerance=0.01)
    # 120 bara
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=-3.15, z_ref=0.643_22, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=6.85, z_ref=0.690_62, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=16.85, z_ref=0.731_96, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=36.85, z_ref=0.797_78, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=56.85, z_ref=0.845_54, tolerance=0.01)


def test_gas4():
    sgerg = SGERG(hs=34.16, d=0.599, x_co2=0.016, x_h2=0.095)
    # 60 bara
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=-3.15, z_ref=0.885_69, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=6.85, z_ref=0.901_50, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=16.85, z_ref=0.915_07, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=36.85, z_ref=0.936_84, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=56.85, z_ref=0.953_02, tolerance=0.01)
    # 120 bara
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=-3.15, z_ref=0.808_43, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=6.85, z_ref=0.836_13, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=16.85, z_ref=0.859_99, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=36.85, z_ref=0.898_27, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=56.85, z_ref=0.926_62, tolerance=0.01)


def test_gas5():
    sgerg = SGERG(hs=36.64, d=0.686, x_co2=0.076, x_h2=0.0)
    # 60 bara
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=-3.15, z_ref=0.826_64, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=6.85, z_ref=0.850_17, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=16.85, z_ref=0.870_03, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=36.85, z_ref=0.901_24, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=56.85, z_ref=0.923_94, tolerance=0.01)
    # 120 bara
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=-3.15, z_ref=0.695_57, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=6.85, z_ref=0.738_28, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=16.85, z_ref=0.774_63, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=36.85, z_ref=0.831_66, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=56.85, z_ref=0.872_69, tolerance=0.01)


def test_gas6():
    sgerg = SGERG(hs=36.58, d=0.644, x_co2=0.011, x_h2=0.0)
    # 60 bara
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=-3.15, z_ref=0.854_06, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=6.85, z_ref=0.873_88, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=16.85, z_ref=0.890_71, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=36.85, z_ref=0.917_36, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=60.0, t_celsius=56.85, z_ref=0.936_90, tolerance=0.01)
    # 120 bara
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=-3.15, z_ref=0.749_39, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=6.85, z_ref=0.784_73, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=16.85, z_ref=0.814_90, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=36.85, z_ref=0.862_66, tolerance=0.01)
    valid_sgerg(sgerg, p_bar=120.0, t_celsius=56.85, z_ref=0.897_49, tolerance=0.01)
