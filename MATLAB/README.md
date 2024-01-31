# Matlab

The matlab scripts here attempt to identify why Rev A oscillates at ~10.8 GHz. One theory is that the large SMA landing pad causes an impedance mismatch that makes the amplifier unstable at certain frequencies. `StabilityAnalysis.m` simulates the chain of two amplifiers and attenuator using scattering parameters from the Mini-Circuits website, then simulates the chain with a mismatched transmission line at the input and output. The s-parameters of the chain with two mismatched lines shows resonance at ~10.9 GHz.
