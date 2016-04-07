from spiketrains import get_spiketrain
import core
import events
import numpy as np

import matplotlib.pyplot as plt 


def do_raster(raster_data, times, ticks, ax=None):
	'''
	Generalized raster plotting function

	Parameters
	------
	raster_data : list of lists of floats
		List of lists.  Each sublist corresponds to one row of events
		Each element of a sublist is an event times
	times : list of floats
		The beginning and end times to plot 
	ticks : list of floats
		Will add a vertical tick across the whole plot for each time in this list
	ax : Matplotlib axes handle, optional 
		Axes on which to produce raster. Default gca.

	Returns
	------
	raster_plot : 
		Handle to the raster plot 
	'''

	ntrials = len(raster_data)
	if ax is None:
		ax = plt.gca()
	ax.set_xlim(times)
	ax.set_ylim((1, ntrials+1))
	for trial, trialdata in enumerate(raster_data):
		ypts = [1+trial, 2+trial]
		for spiketime in trialdata:
			ax.plot([spiketime, spiketime], ypts, 'k', lw=1.5)

	for pltticks in ticks:
		ax.plot([pltticks, pltticks], [1, ntrials+1], 'r', lw=1.5)

	return ax



def plot_raster_cell_stim(spikes, trials, clusterID, stim, period, rec, fs, ax=None):
	'''
	Plots a spike raster for a single cell and stimulus 

	Parameters
	------
	spikes : pandas dataframe
		spike dataframe from core 
	trials : pandas dataframe
		trials dataframe from events
	clusterID : int
		ID number of the cluster you wish to make the raster for 
	stim : str 
		Name of the stimulus you wish to plot cluster's activity for 
	period : list of floats 
		Time window for the raster.  [Seconds_pre_stimulus_onset, Seconds_post_stimulus_end]
	rec : int 
		Recording ID 
	fs : float 
		Sampling rate 
	ax : Matplotlib axes handle, optional
		Axes on which to produce the raster.  Default is to use gca 
 	''' 


	stim_trials = trials[trials['stimulus']==stim]
	ntrials = len(stim_trials)
	stim_starts = stim_trials['time_samples'].values
	stim_ends = stim_trials['stimulus_end'].values

	stim_end_seconds = np.unique((stim_ends - stim_starts)/fs)[0]
	window = [period[0], stim_end_seconds+period[1]]
	raster_data = []
	for trial, start in enumerate(stim_starts):
		
		sptrain = get_spiketrain(rec, start, clusterID, spikes, window, fs)
		raster_data.append(sptrain)

	do_raster(raster_data, window, [0, stim_end_seconds], ax)

