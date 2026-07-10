# betti numbers of simplicial homology in Z/2
# bouqueting / velverette 2026

from math import log2
from itertools import combinations

# helper from SO to make debug output nicer 
# (remove pesky "frozenset" name)
class _frozenset(frozenset):
    def __repr__(self):
        return (frozenset.__repr__(self)).replace('_frozenset','',1)

class SimpComplex:
    """Finite-dimensional simplicial complex. 
    n-simplices are `set`s of `int`s, stored 
    in a `dict` of `set`s called `data`. May
    may also be accessed in a flat list."""
    def __init__(self):
        self.data = {-1: set(_frozenset())}
        self.dim = -1

    def empty(self):
        self.data = {-1: set(_frozenset())}
        self.dim = -1
    
    def scrub(self):
        """Helper method! Ensure clean data."""
        kill = []
        for n in self.data.keys():
            if n == -1: 
                self.data[n] = set(_frozenset())
                continue
            if not self.data[n]:
                kill += [n]

        for n in kill: self.data.pop(n, None)
        self.dim = max(self.data.keys())
    
    def nSimplices(self, n):
        if n not in self.data.keys(): return set()
        for simp in self.data[n]: print(simp)
        return self.data[n]
    
    def allSimplices(self):
        """Return list of all simplices."""
        buffer = []
        for n in self.data.keys():
            buffer += list(self.nSimplices(n))
        print(buffer)
        return buffer
    
    def addSimplex(self, vertices: list):
        if not vertices:
            print("empty vertex list"); return

        # all subsimplices
        for n in range(len(vertices) + 1):
            for subset in combinations(vertices, n):
                simp = _frozenset(subset)
                if n not in self.data.keys():
                    self.data[n] = set()
                self.data[n].add(simp)
        self.scrub()
    
    def delSimplex(self, simplex: set):
        n = len(simplex)
        if n not in self.data.keys():
            print("no simplices of dim"); return
        
        self.data[n].discard(_frozenset(simplex)) # safe
        self.scrub()

def simplexBoundary(simplex: set) -> set:
    """Accepts a simplex, returns its faces."""
    # because we are working in Z/2, no coefficient
    # data need be computed. so pure combinatorics!
    if not simplex: return set()

    faces = combinations(simplex, len(simplex) - 1)
    bdry = set([_frozenset(face) for face in faces])
    return bdry

def chainBoundary(chain: list) -> set:
    """Expects a list of simplices."""
    if not chain: 
        return set(_frozenset())

    bdry = set()
    for simp in chain: 
        bdry = bdry ^ simplexBoundary(simp)
    return bdry

def nthBetti(complex: SimpComplex, n: int) -> int:
    """nth Betti number for homology in Z/2."""
    n += 1

    # cycles
    cycles = set()
    nSimps = complex.nSimplices(n)

    # get all n-chains
    nChains = []
    for i in range(len(nSimps) + 1):
        chains = combinations(nSimps, i) # of length n
        nChains += [_frozenset(chain) for chain in chains]
    nChains = list(set(nChains))
    print(nChains)
    
    for chain in nChains:
        bdry = chainBoundary(set(chain))
        if not bdry: cycles.add(_frozenset(chain))

    # boundaries
    bdries = set()
    n1Simps = complex.nSimplices(n + 1)

    # get all (n+1)-chains
    n1Chains = []
    for i in range(len(n1Simps) + 1):
        xchains = combinations(n1Simps, i) # of length n
        n1Chains += [set(chain) for chain in xchains]

    for chain in n1Chains:
        bdry = chainBoundary(chain)
        bdries.add(_frozenset(bdry))
    
    n -= 1
    betti = log2(len(cycles)) - log2(len(bdries))

    print(f"{len(cycles)} cycles: {cycles}")
    print(f"{len(bdries)} bdries: {bdries}")
    print(f"{n}th betti number is {betti}")
    return betti
