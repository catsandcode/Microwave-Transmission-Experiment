"""
The snippets module provides functions that might be useful for performing measurements and analyzing data. Some functions
in the module are completely unrelated to data acquisition, and are purely analysis. It is essentially a module of code
that would otherwise be repeated lots of times in experiment runs.
"""

import time
import experiment_wrapper as experiment_wrapper
import numpy as np


def print_attributes(sweep):
    """
    Prints the attributes associated with the sweep to the console. This should be included in notes about each sweep.

    :param sweep: The sweep to extract attributes from.
    """
    to_print = ''
    for key in sweep.keys():
        # If this is not the data key, add the key and the key's value to to_print
        if key != 'data':
            to_print += key + ': ' + str(sweep[key])
        # Append units
        if key == 'slope':
            to_print += 'dB/oct'
        elif key == 'power':
            to_print += 'dBm'
        elif key == 'lock_in_time':
            to_print += 's'
        elif key == 'sensitivity':
            to_print += 'mV'
        elif key == 'chopper_frequency':
            to_print += 'kHz'
        elif key == 'chopper_amplitude':
            to_print += 'V'
        elif key == 'load_time':
            to_print += 's'
        elif key == 'time_constant':
            to_print += 'ms'
        elif key == 'freq_synth_frequency':
            to_print += 'GHz'
        # If this is not the data key, add a new line
        if key != 'data':
            to_print += '\n'
    print(to_print)


def sweep_parameter(parameter_set_func, values_to_sweep, time_constant=100, sensitivity=0.2, slope=12, load_time=4, lock_in_time=0, chopper_amplitude=5, chopper_frequency=1, power=15, freq_synth_frequency=250, multiplier=18, save_path=''):
    """
    This method sweeps a parameter through a set of values. Any parameter can be chosen. If the chosen parameter is represented in one of this functions arguments, whatever is entered for that argument will be ignored,

    :param parameter_set_func: The function that sets the parameter the user wishes to sweep through, i.e. wrapper.set_continuous_wave_freq.

    :param values_to_sweep: The values to sweep the parameter through, i.e. range(200, 301, 2),

    :param time_constant: The lock-in amplifier time constant in ms.

    :param sensitivity: The lock-in amplifier sensitivity in mV.

    :param slope: The lock-in amplifier roll off slope in dB/octave.

    :param load_time: The amount of time to give the instruments to finish setting up before data collection begins.

    :param lock_in_time: The amount of time to give the lock in amplifier to lock back onto the reference signal after a parameter is changed.

    :param chopper_amplitude: The amplitude of the chopper signal in V.

    :param chopper_frequency: The frequency of the chopper signal in kHz.

    :param power: The power of the sweeper in dBm.

    :param freq_synth_frequency: The frequency of the sweeper in GHz.

    :param multiplier: The multiplier (i.e. product of all frequency multipliers in the setup).

    :param save_path: If a non-empty string variable save_path is passed the the sweep will be saved as a .npy file with the sweep settings saved in metadata.

    :return: The data collected, where the first column is frequency, the second column is X, and the third column is Y. X and Y are in volts.
    """
    experiment_wrapper.initialize()

    # Set the frequency multiplier, as it is particular to the experiment
    experiment_wrapper.set_freq_multiplier(multiplier)

    # Setup the frequency synthesizer
    experiment_wrapper.set_freq_synth_frequency(freq_synth_frequency)
    experiment_wrapper.set_freq_synth_power(power)
    experiment_wrapper.set_freq_synth_enable(True)

    # Setup chopper
    experiment_wrapper.set_chopper_amplitude(chopper_amplitude)
    experiment_wrapper.set_chopper_frequency(chopper_frequency)
    experiment_wrapper.set_chopper_on(True)

    # Setup lock-in
    experiment_wrapper.set_time_constant(time_constant)
    experiment_wrapper.set_sensitivity(sensitivity)
    experiment_wrapper.set_low_pass_slope(slope)

    # Sleep to allow instruments to adjust settings
    time.sleep(load_time)

    # Create a new array to save data to
    data = np.array([0,0,0], float)  # This row will be deleted later

    # Sweep the selected parameter and record data
    for value in values_to_sweep:
        print('At sweep value ' + str(value))

        # Set selected parameter to the given value
        parameter_set_func(value)

        # Sleep to allow lock-in to lock to new frequency and for time constant to average
        time.sleep((time_constant * 5.0 / 1000.0) + lock_in_time)  # Sleep for five time constants plus the lock_in_time

        # Get data from the lock-in amplifier and and add it to the data array
        (x, y) = experiment_wrapper.snap_data()

        # If a blank string was read, replace will None
        if x == '':
            x = None
        if y == '':
            y = None

        data_row = np.array([value, x, y])
        data = np.vstack((data, data_row))

    # Delete the first row in the collected data, as it was created to give the array shape earlier but holds no useful data
    data = np.delete(data, 0, 0)

    # Close instruments
    experiment_wrapper.close()

    if save_path != '':
        np.savez(save_path, data = data, parameter_set_func=str(parameter_set_func), time_constant=time_constant, sensitivity=sensitivity, slope=slope, load_time=load_time, lock_in_time=lock_in_time, chopper_amplitude=chopper_amplitude, chopper_frequency=chopper_frequency, power=power, freq_synth_frequency=freq_synth_frequency, multiplier=multiplier)

    # Return data
    return data


# Define the clean data function, which replaces empty strings in the sweeps with None
def clean_data(arr, remove=False, rpl='nan'):
    """
    Cleans a data array, removing blank or non-number entries. Any changes are documented by printing to the console. Returns a numpy array populated with floats.

    :param arr: The array to clean.

    :param remove: If true, rows with empty strings will simply be removed.

    :param rpl: The string to replace empty strings with.

    :return: A cleaned numpy array populated with floats.
    """
    # Define is_num function, which returns true if num is in fact a string representation of a number
    def is_num(num):
        if num == '':
            return False
        else:
            try:
                num = float(num)
            except ValueError:
                return False
            return True

    # Define are_cols_num function, which returns true if every column in array can be respresented by a number
    def are_cols_num(arr, c):
        for i in range(c):
            if not is_num(arr[i]):
                return False
        return True
    # Set array type to object
    arr = arr.astype(dtype=object)
    # Iterate over the array
    r, c = arr.shape
    i = 0
    while i < r:
        if remove:
            if not are_cols_num(arr[i, :], c):  # If every column in array at row i is not a number, enter if block
                print('error in ' + str(arr[i, :]) + ', removing...')
                arr = np.delete(arr, i, 0)  # Set the value to whatever was passed to the function
                # Reset r and c, as the remove operation has resized the array
                r, c = arr.shape
            else:
                # Increment i if no deletion has occurred
                i += 1
        else:
            if not are_cols_num(arr[i, :], c):  # If every column in array at row i is not a number, enter if block
                print('error in ' + str(arr[i, :]) + ', fixing...')
                for j in range(1, c):  # For each column (excluding the first column) in the row
                    arr.itemset((i, j), rpl)  # Set the value to whatever was passed to the function
                print('fixed to ' + str(arr[i, :]))
            # Increment i
            i += 1
    print('converting to a float array...')
    arr = np.array(arr, dtype=float)  # Return the new array, populated with float objects
    return arr
