from setup_control.snippets import sweep_parameter
from setup_control.experiment_wrapper import set_freq_synth_frequency
import numpy as np

"""
Horns are 98.67mm apart.

Uses a time constant of 100ms, 12dB/oct, 0.2mV sensitivity, load time of 4s, lock in time of 0.2s. Sweeps from 225GHz to 300GHz in 500MHz steps. Returns values in volts.
"""

for i in range(0, 3):
    sweep_parameter(set_freq_synth_frequency, np.linspace(225, 300, num=150, endpoint=True), time_constant=100,  sensitivity=0.2, load_time=4, lock_in_time=0.2, multiplier=18,
                    save_path='sweep_tuning_test2/200ms_sweep_num_' + str(i))


"""
Horns are 98.67mm apart.

Uses a time constant of 100ms, 12dB/oct, 0.2mV sensitivity, load time of 4s, lock in time of 0.1s. Sweeps from 225GHz to 300GHz in 500MHz steps. Returns values in volts.
"""

for i in range(0, 3):
    sweep_parameter(set_freq_synth_frequency, np.linspace(225, 300, num=150, endpoint=True), time_constant=100,  sensitivity=0.2, load_time=4, lock_in_time=0.1, multiplier=18,
                    save_path='sweep_tuning_test2/100ms_sweep_num_' + str(i))

"""
Horns are 98.67mm apart.

Uses a time constant of 100ms, 12dB/oct, 0.2mV sensitivity, load time of 4s, lock in time of 0s. Sweeps from 225GHz to 300GHz in 500MHz steps. Returns values in volts.
"""

for i in range(0, 3):
    sweep_parameter(set_freq_synth_frequency, np.linspace(225, 300, num=150, endpoint=True), time_constant=100,  sensitivity=0.2, load_time=4, lock_in_time=0, multiplier=18,
                    save_path='sweep_tuning_test2/0ms_sweep_num_' + str(i))