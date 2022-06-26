# implements Queyranne's algorithm for minimizing symmetric submodular
# functions
# author: Andreas Krause (krausea@gmail.com)
#
# function R = sfo_queyranne(F,V)
# F is the symmetric submodular function
# V is the index set
# Returns an optimal solution to min F(A) s.t. 0<|A|<n
#
# Example:
#   G = [1 1 0; 1 0 1; 0 1 1]; F = sfo_fn_cutfun(G);
#   A = sfo_queyranne(F,1:3)

import numpy as np
import setdiff 
import cutfun 
    
def sfo_queyranne(F = None,V = None): 
    n = len(V)
    S = np.array([])
    for j in np.arange(1,n+1).reshape(-1):
        S[j] = V(j)
    
    s = np.zeros((1,n - 1))
    A = np.array([])
    inew = np.arange(1,n+1)
    for h in np.arange(1,(n - 1)+1).reshape(-1):
        Fnew = lambda A = None: F(np.array([S[A]]))
        # find a pendant pair
        t,u = sfo_pendentpair(Fnew,inew)
        # this gives a candidate solution
        A[h] = S[u]
        s[h] = Fnew(u)
        S[t] = np.array([S[t],S[u]])
        inew = setdiff.sfo_setdiff_fast(inew,u)
        S[u] = - S[u]
    
    # return best candidate solution
    i = np.where(s == np.amin(s),1)
    R = A[i]
    return R
    ##
# implements the pendant pair finding subroutine of queyranne's algorithm
# (Queyranne '95)
# F is the submodular function
# inds is an array of indices; (typically, 1:n)
    
    
def sfo_pendentpair(F = None,V = None): 
    x = 1
    
    vnew = V(x)
    n = len(V)
    Wi = []
    used = np.zeros((1,n))
    used[x] = 1
    for i in np.arange(1,(n - 1)+1).reshape(-1):
        vold = vnew
        Wi = np.array([Wi,vold])
        # now update the keys
        keys = 1e+99 * np.ones((1,n))
        for j in np.arange(1,n+1).reshape(-1):
            if used(j):
                continue
            keys[j] = F(np.array([Wi,V(j)])) - F(V(j))
        argmin = np.where(keys == np.amin(keys),1)
        vnew = V(argmin)
        used[argmin] = 1
    
    s = vold
    t = vnew
    return s, t


G = [[1,0,1],[1,0,0],[1,1,1]]
F = cutfun.sfo_fn_cutfun(G)
A = sfo_queyranne(F,[1,2,3])
print(A)