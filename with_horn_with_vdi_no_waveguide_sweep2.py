from setup_control.snippets import sweep_parameter
from setup_control.experiment_wrapper import set_freq_synth_frequency
import numpy as np

"""
Horns are 92.85mm apart.

Uses a time constant of 300ms, 12dB/oct, 0.2mV sensitivity, load time of 4s, lock in time of 4s. Sweeps from 12.5GHz to 16.5GHz in 25MHz steps. Returns values in volts.
"""

for i in range(0, 3):
    sweep_parameter(set_freq_synth_frequency, np.linspace(12.5, 16.5, num=160, endpoint=True), time_constant=300,  sensitivity=0.2, load_time=4, lock_in_time=4, multiplier=1,
                    save_path='with_horn_with_vdi_no_waveguide_sweep_data_folder2/sweep_num_' + str(i))
