"""
Some tests with AGA8

Code comes from https://github.com/Dseal95/AGA8-Detail with some modifications
it's a python port of C version (see https://github.com/usnistgov/AGA8)
"""

from AGA8 import AGA8Detail

# compositions in the x array use the following order and must be sent as mole fractions
x = [
    0.0,     # 0 - PLACEHOLDER
    0.9278,  # 1 - Methane C1 (CH4)
    0.0116,  # 2 - Nitrogen (N)
    0.0118,  # 3 - Carbon dioxide (CO2)
    0.0401,  # 4 - Ethane C2 (C2H6)
    0.0064,  # 5 - Propane C3 (C3H8)
    0.0,     # 6 - Iso-Butane IC4 (i-C4H10)
    0.0,     # 7 - n-Butane NC4 (n-C4H10)
    0.0,     # 8 - Isopentane IC5 (i-C5H12)
    0.0,     # 9 - n-Pentane NC5 (n-C5H12)
    0.0,     # 10 - n-Hexane (C6H14)
    0.0,     # 11 - n-Heptane (C7H16)
    0.0,     # 12 - n-Octane (C8H18)
    0.0,     # 13 - n-Nonane (C9H20)
    0.0,     # 14 - n-Decane (C10H22)
    0.0,     # 15 - Hydrogen (H)
    0.0,     # 16 - Oxygen (O)
    0.0,     # 17 - Carbon monoxide (CO)
    0.0,     # 18 - Water (H2O)
    0.0,     # 19 - Hydrogen sulfide (H2S)
    0.0,     # 20 - Helium (He)
    0.0,     # 21 - Argon (Ar)
]

# use AGA8Detail class
aga8_detail = AGA8Detail(p_bara=1.013, t_celsius=0.0, x=x).run()
print(f'Z factor = {aga8_detail.z}')
