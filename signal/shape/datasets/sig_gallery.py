import numpy as np


def sig_exp_pulse(pulse_len: int = 150, rate: float = 1.0, prefix_len: int = 0, suffix_len: int = 0) -> np.ndarray:
    tau = 1.0
    pulse = np.exp(-np.linspace(0.0, 5*tau*rate, pulse_len))
    return np.concatenate([np.zeros(prefix_len), pulse, np.zeros(suffix_len)])
