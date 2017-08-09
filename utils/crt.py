from utils import modinv

def easy_crt(mods):
    '''
    Use Chinese Restsatz to get the solution of modular equation system
    '''
    
    while len(mods) > 1:
        mods.sort(key=lambda x: x[1])
        e = mods.pop(0)

        a, m = e[0], e[1]
        b, n = mods[0][0], mods[0][1]

        amb=a-b

        n_1 = modinv(n, m)
        r = b+n*(((a-b) * n_1) % m)
        mn = m*n

        mods[0] = (r % mn, mn)

    return mods[0][0]
