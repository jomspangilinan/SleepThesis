import csv
import time,csv,os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from numpy.fft import fft, fftfreq
from scipy.signal import find_peaks
from scipy.signal import argrelextrema
import math
from scipy import signal
t_vec, ir_vec, x_vec, y_vec, z_vec = [], [], [], [], []
def nextpow2(i):
  n = 2
  while n < i: n = n*2
  return n

def indices(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]


name = input("Enter filename: ")
fileName =  name + ".csv"
with open(fileName,newline='') as csvfile:
    csvreader = csv.reader(csvfile,delimiter=',')
    for row in csvreader:
        t_vec.append(float(row[0]))
        x_vec.append(float(row[1]))
        y_vec.append(float(row[2]))
        z_vec.append(float(row[3]))
        ir_vec.append(float(row[4]))


s1 = 0 # change this for different range of data
s2 = len(t_vec) # change this for ending range of data
t_vec = np.array(t_vec[s1:s2])

ir_vec = ir_vec[s1:s2]
samp_rate  = len(ir_vec)/60

w1 = 0.2 / (samp_rate / 2) # Normalize the frequency
w2 = 0.9 / (samp_rate / 2) # Normalize the frequency
b, a = signal.butter(1, [w1, w2], btype='band')
output_hr = signal.filtfilt(b, a, ir_vec)
output_x = signal.filtfilt(b, a, x_vec)
output_y = signal.filtfilt(b, a, y_vec)
output_z = signal.filtfilt(b, a, z_vec)
def fftPlot(x, fs):
  # Get length of data
  L = len(x)
  # Calculate optimal length of FFT using nextpow2
  NFFT = 2^nextpow2(L)
  # Calculate fft using Numpy FFT method
  INPUT = np.fft.fft(x, NFFT)/L
  # Create frequency (x) axis data for plotting
  fAxis = fs/2 * np.linspace(0, 1, int(NFFT/2) + 1)
  # Calculate magnitude response from FFT data
  mAxis = 2*abs(INPUT[0:int(NFFT/2) + 1])
  # Return frequency axis data, magnitude response, and FFT length
  return fAxis, mAxis, NFFT


freq, inputFFT, nfft = fftPlot(output_hr, samp_rate)


peaks_fft_loc, _ = find_peaks(inputFFT)
peaks_mag=np.array(inputFFT)[peaks_fft_loc]
peaks_actual_loc = np.array(freq)[peaks_fft_loc]

minValIndex = min(indices(peaks_actual_loc, lambda x: x>0.5))
maxValIndex = max(indices(peaks_actual_loc, lambda x: x<2))
heart_beat_loc = indices(peaks_mag, lambda x: x==max(peaks_mag[minValIndex:maxValIndex]))
hr = math.ceil((peaks_actual_loc[heart_beat_loc] * 60))
print(hr)
fig = plt.figure(figsize=(14,8))
ax1 = fig.add_subplot(111)
#ax1.set_xlabel('Frequency [Hz]',fontsize=24)
#ax1.set_ylabel('PPG Magnitude',fontsize=24,color='#CE445D',labelpad=10)
#ax1.tick_params(axis='both',which='major',labelsize=16)
plt1 = ax1.plot(freq,inputFFT,label='IR',color='#CE445D',linewidth=1)
plt1 = ax1.plot(peaks_actual_loc,peaks_mag,'x')

plt.show()
fig.savefig( name + "_hr.png", dpi=100)
plt.clf()



