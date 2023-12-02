def a(l:str):
    # order in which the characters will be sorted (default 0-9, a-z)
    a = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

    try:
       return a.index(l.lower())
    except:
        return -1

def sort(o, exp = "o"):

    # Alphabeticly sorts a dict / list

    oo = [] # sorted before expresxion
    sorted = [] # sorted list after expression

    for so in o:
        # get current name
        name = eval(exp)

        done = len(sorted) == 0
        i = 0
        si = 0

        while not done:
            # check if object at index has lower value
            if len(sorted) <= i: break
            if si >= len(name): break
            if len(sorted[i]) > si:
                if   a( sorted[i][si] ) < a( name[si] ) : i  += 1; continue
                elif a( sorted[i][si] ) == a( name[si] ): si += 1; continue
                else: break
            else:
                break

        sorted.insert(i,name)
        oo.insert(i,so)

    return oo, sorted