import itertools

class Factor:
    def __init__(self, variables, default=0):
        self.variables = variables
        keys = [tuple(sorted(zip(self.variables.keys(),r)))
                for r in itertools.product(*self.variables.values())];
        self.f = dict(zip(keys, [default]*len(keys)))

    def __getitem__(self,e):
        return self.f[tuple(sorted(self._filter_inputs(e).items()))]

    def __setitem__(self,e,x):
        k = tuple(sorted(self._filter_inputs(e).items()));
        if (k in self.f):
            self.f[k] = x;
        else:
            raise KeyError(e)

    def _filter_inputs(self,e):
        return dict([(k,v) for k,v in e.items() if k in self.variables])

    def inputs(self):
        return [dict(a) for a in self.f.keys()];

    def values(self):
        return [a for a in self.f.values()];


# functions to implment below

def tarun(l1,l2):
    l3={}
    for a in l1:
        l3[a]=l1[a]
    for a in l2:
        if a not in l1:
            l3[a]=l2[a]
    return l3
def tarun2(l,vout):
    l3={}
    for a in l:
        l3[a]=l[a]
    if vout in l3:
        l3.pop(vout)
    return l3
def tarun3(vout,b,a):
    l3={}
    for g in a:
        l3[g]=a[g]
    l3[vout]=b
    return l3

def factor_product(f1,f2):
    l1=f1.variables
    l2=f2.variables
    l3=tarun(l1,l2)
    f=Factor(l3)
    for e in f.inputs():
        f[e]=f1[e]*f2[e]
    return f

def factor_sum(f,vout):
    #for e in f.inputs():
    #    print str(e)+ " = " + str(f[e])
    l=f.variables
    if(vout not in l):
            return f
    l1=tarun2(l,vout)
    f1=Factor(l1)
    for a in f1.inputs():
            for b in l[vout]:
                c=tarun3(vout,b,a)
                f1[a]=f1[a]+f[c]  
    return f1
    
def variable_order(factors,variables):
    S=[]
    I=[]
    L=[]
    for a in factors:
        l1=a.variables
        for b in l1:
            if b not in S:
                S.append(b)
    if(len(variables)==len(S)):
        return 0
    for t in S:
        if t not in variables:
            I.append(t)
    
    for t in I:
        q=[]
        for a in factors:
            l1=a.variables
            if t in l1:
                for c in l1:
                    if(t!=c):
                        q.append(c)
        L.append(q)
    mini=10000000000000000000
    can=0
    for a in range(0,len(L)):
        if(len(L[a])<mini):
            mini=len(L[a])
            can=a
    return I[can]


    




def marginal_inference(factors, variables, elim_order=None):
    b=variable_order(factors,variables)
    f2=Factor({})
    while(b!=0):
        F=[]
        q=[]
        count=0
        for a in factors:
            l1=a.variables
            if b in l1:
                F.append(a)
                q.append(count)
                count=count-1
            count=count+1
        if(len(F)==1):
            f2=F[0]
        else:
            f2=factor_product(F[0],F[1])
        for c in range(0,len(F)-2):
            f2=factor_product(f2,F[c+2])
        f2=factor_sum(f2,b)
        for a in q:
            factors.pop(a)
        factors.append(f2)
        b=variable_order(factors,variables)  
    f1=Factor({})
    if(len(factors)==1):
        f1=factors[0]
    else:
        f1=factor_product(factors[0],factors[1])
    for c in range(0,len(factors)-2):
        f1=factor_product(f1,factors[c+2])
    sum=0
    for e in f1.inputs():
        sum=f1[e]+sum
    for e in f1.inputs():
        f1[e]=f1[e]/sum
    return f1



