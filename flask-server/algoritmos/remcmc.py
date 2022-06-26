import numpy as np
import matplotlib.pyplot as plt
import numpy.matlib
    
def REMCMC(data = None,phi_measure = None,tau = None): 
    # -----------------------------------------------------------------------
# This code implements the Replica Exchange Markov Chain Monte Carlo method
# for finding the MIB described in Kitozono et al (2018), "Efficient Algorithms
# for Searching the Minimum Information Partition in Integrated
# Information Theory." This algorithm differs from theirs in that it looks
# for a bipartiton that minimizes *normalized* integrated information,
# rather than non-normalized integrated information. In principle this
# algorithm can be used for large systems, but it's very slow to converge
# for any size system. For this reason, we've written this code such that
# if you terminate it while running, it will store its current best guesses
# for the MIB in the variable 'output' in your workspace
# -----------------------------------------------------------------------
    
    # If you interrupt this function with ctrl+c, it will save the current
# partitions and integrated information values in the variable "output":
    print('If you terminate this script with ctrl+c, its interim results will be saved in a variable called "output"')
    cleanupObj = onCleanup(return_current_output)
    global interrupt_output
    
    def return_current_output(): 
        assignin('base','output',interrupt_output)
        return
    
    N = data.shape[1-1]
    
    np.random.randn('seed',12345)
    # INITIALIZE TEMPERATURES
    for i in np.arange(1,6+1).reshape(-1):
        S_t[i] = randsample(N,randsample(N - 1,1))
        # change the community assignment of a random node
        e = randsample(N,1)
        if np.any(S_t[i] == e):
            S_c[i] = setdiff(S_t[i],e)
        else:
            S_c[i] = np.array([[S_t[i]],[e]])
        # compute normalized integrated information for the old bipartition
        S_c_part = np.ones((1,N))
        S_c_part[S_c[i]] = 2
        S_c_out = phi_comp(data,S_c_part,phi_measure,tau,0)
        S_c_phi = S_c_out.phi_norm
        # compute normalized integrated information for the new bipartition
        S_t_part = np.ones((1,N))
        S_t_part[S_t[i]] = 2
        S_t_out = phi_comp(data,S_t_part,phi_measure,tau,0)
        S_t_phi = S_t_out.phi_norm
        # magnitude of changes in integrated information as a result of
# bipartition changes
        changes[i] = np.abs(S_t_phi - S_c_phi)
    
    temps = np.arange(1,1000000+100000,100000)
    
    # fit acceptance ratio as a function of temperature
    for i in np.arange(1,len(temps)+1).reshape(-1):
        rat[i] = mean(np.exp(- temps(i) * changes))
    
    # set the highest temperature so that its average acceptance ratio is 0.01
# (parameter set in Kitazono et al)
    top_temp_f = fit(np.transpose(temps),np.transpose(rat) - 0.01,'pchipinterp')
    new_temps[1] = fzero(top_temp_f,np.array([0,np.amax(temps)]))
    # set the lowest temperature so that its average acceptance ratio is 0.5
# (parameter set in Kitazono et al)
    bottom_temp_f = fit(np.transpose(temps),np.transpose(rat) - 0.5,'pchipinterp')
    new_temps[6] = fzero(bottom_temp_f,np.array([0,np.amax(temps)]))
    # set intermediate temperatures through a geometric progression
    clear('temps')
    temps = new_temps
    for m in np.arange(2,5+1).reshape(-1):
        temps[m] = temps(1) * (temps(6) / temps(1)) ** ((m - 1) / 5)
    
    clear('new_temps')
    N = data.shape[1-1]
    # start with random bipartitions for each of the 6 temperatures
    for i in np.arange(1,len(temps)+1).reshape(-1):
        S_t[i] = randsample(N,randsample(N - 1,1))
    
    figure
    
    converge = 0
    
    t = 1
    while converge == 0:

        for i in np.arange(1,len(temps)+1).reshape(-1):
            # change the community assignment of a random node
            e = randsample(N,1)
            if np.any(S_t[i] == e):
                S_c[i] = setdiff(S_t[i],e)
            else:
                S_c[i] = np.array([[S_t[i]],[e]])
            # new bipartition
            S_c_part = np.ones((1,N))
            S_c_part[S_c[i]] = 2
            # old bipartition
            S_t_part = np.ones((1,N))
            S_t_part[S_t[i]] = 2
            # normalized integrated information across the new bipartition
            S_c_out = phi_comp(data,S_c_part,phi_measure,tau,0)
            S_c_phi = S_c_out.phi_norm
            S_c_phi_full = S_c_out.phi
            # normalized integrated information across the old bipartition
            S_t_out = phi_comp(data,S_t_part,phi_measure,tau,0)
            S_t_phi = S_t_out.phi_norm
            S_t_phi_full = S_t_out.phi
            # changes in integrated information
            phi_diff[i,t] = S_t_phi - S_c_phi
            # compute the bipartition swap probability r
            r[i,t] = np.exp(temps(i) * (phi_diff(i,t)))
            # accept or reject new bipartition?
            alpha = np.amin(np.array([1,r(i,t)]))
            u = rand
            if u < alpha:
                S_t[i] = S_c[i]
                phi[i] = S_c_phi
                full_phi[i] = S_c_phi_full
            else:
                phi[i] = S_t_phi
                full_phi[i] = S_t_phi_full
            all_phi[i,t] = phi(i)
        # plot current values of normalized integrated information
        plt.plot(np.transpose(all_phi))
        plt.xlabel('Iteration')
        plt.ylabel('\Phi (normalized, non-extrapolated)')
        plt.title(np.array(['Minimization of \Phi Across 6 Sequences, Each With Its Own Temperature','(this will pause every 5 iterations, for the first 200, to update temps)']))
        drawnow
        # every 5 steps, exchange temperatures according to the Metropolis
# criterion
        if np.mod(t,5) == 0:
            for i in np.arange(1,len(temps) - 1+1).reshape(-1):
                r_prime = np.exp((temps(i + 1) - temps(i)) * (phi(i + 1) - phi(i)))
                p = np.amin(np.array([1,r_prime]))
                u = rand
                # swap or not swap temperatures across sequences?
                if u < p:
                    temp1 = S_t[i]
                    temp2 = S_t[i + 1]
                    S_t[i] = temp2
                    S_t[i + 1] = temp1
        # update temperatures every 5 steps, until the 200th step
        if np.mod(t,5) == 0 and t < 200:
            old_temps = temps
            # regress mean of normalized integrated information as a function
# of temperature
            mean_func = fit(np.transpose(temps),nanmean(all_phi(:,np.arange((t - 4),t+1)),2),'pchipinterp')
            # regress variance of normalized integrated information as a function
# of temperature (add a small positive constant to avoid dividing by
# zero in case there were no partition changes at a particular
# temperature)
            var_func = fit(np.transpose(temps),nanstd(all_phi(:,np.arange((t - 4),t+1)),[],2) ** 2 + 1e-05,'pchipinterp')
            # store changes in normalized integrated information
            changes = np.abs(phi_diff(phi_diff <= 0))
            # calculate new low and high temperatures, so that the average
# acceptance ratio for the high temperature is 0.01 and the average
# acceptance ratio for the low temperature is 0.5
            clear('rat')
            temps = np.arange(1,1000000+100000,100000)
            for i in np.arange(1,len(temps)+1).reshape(-1):
                rat[i] = mean(np.exp(- temps(i) * changes))
            top_temp_f = fit(np.transpose(temps),np.transpose(rat) - 0.01,'pchipinterp')
            new_temps[1] = fzero(top_temp_f,np.array([0,np.amax(temps)]))
            bottom_temp_f = fit(np.transpose(temps),np.transpose(rat) - 0.5,'pchipinterp')
            new_temps[6] = fzero(bottom_temp_f,np.array([0,np.amax(temps)]))
            clear('temps')
            # set the intermediate temperatures by minimizing the following
# cost function (Eqs. 45 & 46 in Kitazono et al):
            e_func = lambda x = None: nansum(np.array([(0.5 * erfc((mean_func(x(2)) - mean_func(x(1))) / (np.sqrt(2 * (var_func(x(2)) + var_func(x(1)))))) + (1 - 0.5 * erfc((mean_func(x(2)) - mean_func(x(1))) / (np.sqrt(2 * (var_func(x(2)) + var_func(x(1))))))) * np.exp((x(1) - x(2)) * (mean_func(x(1)) - mean_func(x(2))))) ** (- 4),(0.5 * erfc((mean_func(x(3)) - mean_func(x(2))) / (np.sqrt(2 * (var_func(x(3)) + var_func(x(2)))))) + (1 - 0.5 * erfc((mean_func(x(3)) - mean_func(x(2))) / (np.sqrt(2 * (var_func(x(3)) + var_func(x(2))))))) * np.exp((x(2) - x(3)) * (mean_func(x(2)) - mean_func(x(3))))) ** (- 4),(0.5 * erfc((mean_func(x(4)) - mean_func(x(3))) / (np.sqrt(2 * (var_func(x(4)) + var_func(x(3)))))) + (1 - 0.5 * erfc((mean_func(x(4)) - mean_func(x(3))) / (np.sqrt(2 * (var_func(x(4)) + var_func(x(3))))))) * np.exp((x(3) - x(4)) * (mean_func(x(3)) - mean_func(x(4))))) ** (- 4),(0.5 * erfc((mean_func(x(5)) - mean_func(x(4))) / (np.sqrt(2 * (var_func(x(5)) + var_func(x(4)))))) + (1 - 0.5 * erfc((mean_func(x(5)) - mean_func(x(4))) / (np.sqrt(2 * (var_func(x(5)) + var_func(x(4))))))) * np.exp((x(4) - x(5)) * (mean_func(x(4)) - mean_func(x(5))))) ** (- 4),(0.5 * erfc((mean_func(x(6)) - mean_func(x(5))) / (np.sqrt(2 * (var_func(x(6)) + var_func(x(5)))))) + (1 - 0.5 * erfc((mean_func(x(6)) - mean_func(x(5))) / (np.sqrt(2 * (var_func(x(6)) + var_func(x(5))))))) * np.exp((x(5) - x(6)) * (mean_func(x(5)) - mean_func(x(6))))) ** (- 4)]))
            # set the lower and upper bounds for the minimization. These
# bounds are either set according to the highest and lowest
# temperatures set above, or set so as to avoid temperatures
# that, when fed into the variance function defined above,
# yield negative variance)
            a = new_temps(1)
            b = new_temps(6)
            if var_func(b) > 0:
                lower_bound = np.matlib.repmat(b,1,6)
            else:
                first_vals = var_func(np.arange(0,old_temps(1)+1))
                if np.any(first_vals < 0):
                    first_ind = find(first_vals < 0,1) - 1
                    lower_bound = np.matlib.repmat(fzero(var_func,np.array([first_ind,old_temps(1)])),1,6)
                else:
                    lower_bound = np.zeros((1,6))
            if var_func(a) > 0:
                upper_bound = np.matlib.repmat(a,1,6)
            else:
                if np.any(var_func(np.arange((lower_bound(1) + 1),(a * 100)+(a / 100),(a / 100))) <= 0):
                    upper_bound = np.matlib.repmat(fzero(var_func,np.array([lower_bound(1) + 1,a * 100])) - 1,1,6)
                else:
                    upper_bound = []
            # set new temperatures by minimizing the cost function:
            evalc('temps = fmincon(e_func, old_temps,[],[],[],[], lower_bound, upper_bound);')
            temps[1] = new_temps(1)
            temps[6] = new_temps(6)
        # after the 300th iteration, start calculating the convergence
# criterion defined in Brooks & Gelman (1998). Terminate the script if
# all sequences reach a convergence criterion Rc of 1.01
        if t > 300:
            new_phi = all_phi(:,np.arange(201,end()+1))
            n = new_phi.shape[2-1]
            for i in np.arange(1,new_phi.shape[1-1]+1).reshape(-1):
                s1 = new_phi(i,np.arange(1,np.round(n / 2)+1))
                s2 = new_phi(i,np.arange(np.round(n / 2) + 1,end()+1))
                B = (((nanmean(s1) - nanmean(np.array([s1,s2]))) ** 2) + ((nanmean(s2) - nanmean(np.array([s1,s2]))) ** 2)) * n
                W = (nansum((s1 - nanmean(s1)) ** 2) + nansum((s2 - nanmean(s2)) ** 2)) / (2 * (n - 1))
                var = (n - 1) / n * W + B / n
                V[i] = var + B / (2 * n)
                R[i] = V(i) / W
            d = 2 * V / (std(V) ** 2)
            Rc = np.multiply((d + 3) / (d + 1),R)
            if np.all(Rc < 1.01):
                converge = 1
        # store output
        output.phi = full_phi
        output.phi_norm = phi
        output.partitions = S_t
        # store interrupt output in case you terminate this script through
# ctrl+c
        interrupt_output = output
        t = t + 1

    
    return
    
    return output