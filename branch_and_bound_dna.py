# http://nbviewer.jupyter.org/url/www.csbio.unc.edu/mcmillan/Media/Lecture5.ipynb
# DNA use case
nucleotideMap = { 'a':0, 'c':1, 'g':2, 't':3 }
reverseMap = { 0:'a', 1:'c', 2:'g', 3:'t' }
ScoreCount = 0

def getAndClearScoreCount():
    global ScoreCount
    rval = ScoreCount
    ScoreCount = 0
    return rval

def Score(s, DNA, l):
    """ compute the consensus SCORE of a given l-base
        alignment given offsets into each DNA string.
            s = list of starting indices, 1-based, 0 means ignore
            DNA = list of nucleotide strings
            l = Target Motif length"""
    global ScoreCount
    ScoreCount += 1
    score = 0
    for i in xrange(l):
       # loop over string positions
       cnt = [0 for x in xrange(4)]
       for j in xrange(len(s)):
           # loop over DNA strands
           sval = s[j]
           if (sval != 0):
               cnt[nucleotideMap[DNA[j][sval-1+i]]] += 1
       score += max(cnt)
    return score


def Consensus(s, DNA, l):
    """ compute the consensus STRING of a given l-base
        alignment given offsets into each DNA string.
            s = list of starting indices, 1-based, 0 means ignore
            DNA = list of nucleotide strings
            l = Target Motif length """
    cstring = ''
    for i in xrange(l):
       # loop over string positions
       cnt = [0 for x in xrange(4)]
       for j in xrange(len(s)):
           # loop over DNA strands
           sval = s[j]
           if (sval != 0):
               cnt[nucleotideMap[DNA[j][sval-1+i]]] += 1
       cstring += reverseMap[cnt.index(max(cnt))]
    return cstring

def NextLeaf(a, L, k):
    """ generates all L^k permutations of
        of the list of integers, "a", when
        initialized with k*[1] """
    for i in reversed(xrange(L)):
        if (a[i] < k):
            a[i] += 1
            break
        else:
            a[i] = 1
    return a


def NextVertex(a, i, L, k):
    """ generates all nodes in a
        search tree with L^k leafs """
    if (i < L):
        a[i] = 1
        return (a, i+1)
    else:
        for j in reversed(xrange(L)):
            if (a[j] < k):
                a[j] += 1
                return (a, j+1)
            a[j] = 0
    return (a, 0)


def Bypass(a, i, L, k):
    """ ignore the children of an interior node beyond i generations """
    for j in reversed(xrange(i)):
        if (a[j] < k):
            a[j] += 1
            return (a, j+1)
        a[j] = 0
    return (a, 0)


def BranchAndBoundMotifSearch(DNA,t,n,l):
    # traverses a search tree of alignments
    # of 't' DNA fragments (of length 'n')
    # while pruning hopless excursions in
    # search for the 'l'-mer with the
    # maximum consensus score
    s = [0 for i in xrange(t)]
    bestScore = 0
    i = 0
    while (i > 0 or bestScore == 0):
        if (i < t):
            optimisticScore = Score(s, DNA, l) + (t-i)*l
            if (optimisticScore < bestScore):
                s, i = Bypass(s,i,t,n-l+1)
            else:
                s, i = NextVertex(s,i,t,n-l+1)
        else:
            score = Score(s, DNA, l)
            if (score > bestScore):
                print s, " = ", score
                bestScore = score
                bestMotif = [x for x in s]
            s, i = NextVertex(s,i,t,n-l+1)
    return bestMotif

# Example from notes
DNA = ["cctgatagacgctatctggctatccaggtacttaggtcctctgtgcgaatctatgcgtttccaaccat",
       "agtactggtgtacatttgatccatacgtacaccggcaacctgaaacaaacgctcagaaccagaagtgc",
       "aaacgttagtgcaccctctttcttcgtggctctggccaacgagggctgatgtataagacgaaaatttt",
       "agcctccgatgtaagtcatagctgtaactattacctgccacccctattacatcttacgtccatataca",
       "ctgttatacaacgcgtcatggcggggtatgcgttttggtcgtcgtacgctcgatcgttaccgtacggc"]

print "Branch-and-Bound Search = ",
s = BranchAndBoundMotifSearch(DNA,5,68,8)
print s, "=", Consensus(s,DNA,8)
print "iterations =", getAndClearScoreCount()
