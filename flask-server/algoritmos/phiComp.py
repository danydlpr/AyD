import numpy as np
    
def phi_comp(data = None,part = None,phi_measure = None,tau = None,extrapolate = None): 
    # -----------------------------------------------------------------------
#   FUNCTION: phi_comp.m
#   PURPOSE:  Calculate a given phi measure, across a particular partition,
#   over a given time-lag, extrapolated or not to infinite observations
    
    #   INPUT:  data         -  Time-series data matrix, where rows correspond
#                           to channels/neurons/voxels,
#                           and columns to observations.
    
    #           part         -  The partition across which to calculate phi.
#                           This can either be a vector of numbers
#                           containing the community assignment of each
#                           channel/neuron/voxel, or it can be one of the
#                           following strings, which determine which kind
#                           of partition to look for:
    
    #                                   1. 'MIP' - this will exhaustively
#                                   search for the "minimum information
#                                   partition," which is *extremeley*
#                                   computationally expensive and not
#                                   recommended for anything but super tiny
#                                   systems (< 8 nodes)
    
    #                                   2. 'MIB' - this will exhaustively
#                                   search for the "minimum information
#                                   bipartition." This can be computed in a
#                                   reasonable time for networks of up to
#                                   about 18 nodes, but becomes intractable
#                                   for larger systems
    
    #                                   3. 'SpectClust' - this will implement
#                                   the spectral clustering based approach
#                                   described in the paper.
    
    #                                   4. 'atomic' - this will implement the
#                                   "atomic" partition as first
#                                   described in  Oizumi, Masafumi, et al.
#                                   "Measuring integrated information from
#                                   the decoding perspective." PLoS Comput
#                                   Biol 12.1 (2016): e1004654. This
#                                   partition treats every node as its own
#                                   community. As such, it takes no time to
#                                   compute.
    
    #                                   5. 'queyranne' - this will quickly find
#                                   the bipartition that minimizes mutual
#                                   information, as described in
#                                   Kitazono et al (2018), Entropy.
    
    #                                   5. 'REMCMC' - this will use a Replica
#                                   Exchange Markov Chain Monte Carlo
#                                   method to find a bipartition that
#                                   minimizes normalized integrated
#                                   information,  as described in
#                                   Kitazono et al (2018), Entropy. It's
#                                   extremely slow, but is tractable for
#                                   large systems
    
    #           phi_measure  -  The phi measure to be used. The options are
#                           'phi_M' and 'phi_G', both of which are
#                           theoretically well-bounded measures. phi_M is
#                           explained in Tegmark (2016), and is the
#                           time-reverse of the measure originally called
#                           "stochastic interaction" by Nihat Ay. phi_G is
#                           geometric integrated information (i.e. it was
#                           derived from information geometry) (Ouizumi et
#                           al 2016)
    
    #           tau          -  The time-lag over which to calculate phi.
#                           Currently there's no consensus on best
#                           practices for picking a time-lag, but (as we
#                           describe in the paper) it's been suggested that
#                           you should pick a time-lag that maximizes
#                           integrated information
    
    #           extrapolate  -  This is a flag. Set it to 1 if you want the
#                           code to extrapolate to infinite observations
#                           (as described in the paper) for every partition
#                           it tries. The code will then select as the MIB
#                           the partition that minimizes normalized
#                           integrated information, extrapolated. While
#                           this will get you closer to the ground-truth,
#                           it adds *a lot* of computation time (for e.g.,
#                           for even a 16-node system, it can mean the
#                           difference between a few minutes of computing
#                           and a few days). If you want non-extrapolated
#                           (and quick) estimates, set this flag to 0.
    
    
    #   OUTPUT: the following variables are stored in a struct variable called
#            "output"
#           phi         -  the phi value
#           phi_norm    -  the phi value normalized by community size and
#                          number
#           partition   -  the partition identified by whatever
#                          partitioning algorithm was chosen (or the
#                          partition specified)
#           entropy     -  the entropy of the system
    
    
    #   Daniel Toker and Friedrich T. Sommer, May 2018.
    
    # -----------------------------------------------------------------------
    
    # If the partition has already been specified as a vector, where each value
# corresponds to the community assignment of a particular node, then
# calculate phi across that partition
    if not ischar(part)  and not len(tau)==0 :
        nobs = data.shape[2-1]
        num_nodes = data.shape[1-1]
        t_range1 = np.arange(1,nobs - tau+1,1)
        t_range2 = np.arange(1 + tau,nobs+1,1)
        Cov_X = data(:,t_range2) * np.transpose(data(:,t_range2)) / (nobs - tau - 1)
        Cov_Y = data(:,t_range1) * np.transpose(data(:,t_range1)) / (nobs - tau - 1)
        Cov_XY = (data(:,t_range2) * np.transpose(data(:,t_range1))) / (nobs - tau - 1)
        output = phi_calc(phi_measure,Cov_X,Cov_Y,Cov_XY,part)
    
    # Calculate phi across the atomic partition (Oizumi et al, 2016)
    if str(part) == str('atomic'):
        output = phi_comp(data,np.arange(1,data.shape[1-1]+1),phi_measure,tau,extrapolate)
    
    # Calculate phi across the partition that minimizes mutual information in
# space (as quickly determined by the Queyrenne algorithm for minimizing
# submodular functions)
    if str(part) == str('queyranne'):
        output = queyranne(data,phi_measure,tau,extrapolate)
    
    # Calculate integrated information using the spectral clustering-based
# approach described in the paper
    if str(part) == str('SpectClust'):
        output = spectral_partition(data,phi_measure,tau,extrapolate)
    
    # Iterate through all possible bipartions, and pick the one that minimizes
# phi (normalized). This is the minimum information bipartition (MIB)
    if str(part) == str('MIB'):
        output = mib(data,phi_measure,tau,extrapolate)
    
    if str(part) == str('REMCMC'):
        output = REMCMC(data,phi_measure,tau)
    
    # Iterate through all possible partions, and pick the one that minimizes
# phi (normalized). This is the minimum information partition (MIP). This
# is EXTREMELEY computationally expensive
    if str(part) == str('MIP'):
        output = mip(data,phi_measure,tau,extrapolate)
    
    output.entropy = entropy_gauss(cov(np.transpose(data)))
    return output