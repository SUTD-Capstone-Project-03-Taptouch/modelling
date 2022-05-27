# Modelling
Some important info in case it gets lost in the sauce:

## Step 0: Audio splitting
Just paste the audio into the "rawaudio" folder and run `step0split.py`. It has an optional parameter `-d` that specifies how long you want your segments to be.
Statistics:
 - One 30-second audio clip takes ~11Mb at a sampling rate of 48000Hz.
 - The 2 samples were processed in about 13 seconds overall, or about 6.5 seconds per sample.
