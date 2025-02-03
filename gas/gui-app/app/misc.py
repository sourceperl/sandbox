from tkinter import ttk


# some functions
def hs_to_mj(hs_kwh: float) -> float:
    """Convert Hs from kwh/nm3 to MJ/nm3."""
    return hs_kwh * 3.6


def hs_to_t25(hs_t0: float) -> float:
    """Convert Hs from t_comb = 0°C to 25 °C."""
    return hs_t0 * 0.997_4


def to_kelvin(celsius: float) -> float:
    """Converts temperature from Celsius to Kelvin."""
    return celsius + 273.15


def to_celsius(kelvin: float) -> float:
    """Converts temperature from Kelvin to Celsius."""
    return kelvin - 273.15


def set_grid_conf(widget: ttk.Frame) -> None:
    """Apply global geometry to this frame (maintain uniform geometry across the entire frame)."""
    widget.columnconfigure(0, minsize=400)
    widget.columnconfigure(1, minsize=350)
    widget.rowconfigure(0, minsize=250)
    widget.rowconfigure(1, minsize=200)
