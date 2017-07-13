from control.daq import sweep_parameter
from control.experiment_wrapper import set_freq_synth_frequency
import numpy as np
import sys

"""
Uses a time constant of 100ms, 12dB/oct, 0.2mV sensitivity, load time of 4s, lock in time of 0s. Sweeps from 225GHz to 275GHz in 250MHz steps. Returns values in volts.

Takes twelve sweeps, three without filter, then six with filter, and finally three without the filter. Each successive set of three sweeps is are at the powers 15dBm, 12dBm, 9dBm.
"""


def wait_for_user_confirmation(instruction):
    print instruction
    while True:
        s = raw_input('continue? y/[n]\n')
        if s.lower() == 'y':
            print 'continuing...'
            break
        elif s.lower() == 'n':
            print 'exiting...'
            sys.exit(0)

# Settings
freq_start = 225
freq_end = 275
num_steps = 200
time_const = 100
chop_freq = 1
sens = 0.2
load_time = 4
lock_time = 0
multiplier = 18

powers = [15.0, 12.0, 9.0]

# Start tests
wait_for_user_confirmation('please ensure that no filter is between the two antenna horns')

for p in powers:
    sweep_parameter(set_freq_synth_frequency, np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), power=p, time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier,
                    save_path='alumina_filter_test4/no_filter_power'+str(p)+'_0')

wait_for_user_confirmation('please place the filter between the two antenna horns')

for p in powers:
    sweep_parameter(set_freq_synth_frequency, np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), power=p, time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier,
                    save_path='alumina_filter_test4/with_filter_power'+str(p)+'_0')

for p in powers:
    sweep_parameter(set_freq_synth_frequency, np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), power=p, time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier,
                    save_path='alumina_filter_test4/with_filter_power'+str(p)+'_1')

wait_for_user_confirmation('please remove the filter between the two antenna horns')

for p in powers:
    sweep_parameter(set_freq_synth_frequency, np.linspace(freq_start, freq_end, num=num_steps, endpoint=True), power=p, time_constant=time_const, chopper_frequency=chop_freq, sensitivity=sens, load_time=load_time, lock_in_time=lock_time, multiplier=multiplier,
                    save_path='alumina_filter_test4/no_filter_power'+str(p)+'_1')