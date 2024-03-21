from math import *

# function for converting a vector to a tuple
def tuple2vec3(t):
    try:
        x,y,z = t
    except:
        raise ValueError("Invalid tuple for tuple2vec3 function")
    
    return vec3(x,y,z)

def tuple2vec2(t):
    try:
        x,y = t
    except:
        raise ValueError("Invalid tuple for tuple2vec2 function")
    
    return vec2(x,y)

# mess of a class
class vec3:
    
    def __init__(self, x:float = 0, y:float = 0, z:float = 0 ):
        self.x = x
        self.y = y
        self.z = z
    
    ## conversions
    # string
    def __str__(s):
        return "[ "+str(s.x)+" "+str(s.y)+" "+str(s.z)+" ]"
    
    # represetation
    def __repr__(s):
        return s.__str__()
    
    # list
    def __list__(s):
        return [ s.x, s.y, s.z ]
    
    # touple
    def __tuple__(s):
        return ( s.x, s.y, s.z )
    
    # dict
    def __dict__(s):
        return { "x": s.x, "y": s.y, "z": s.z }
    
    # convert the vector to a tuple
    def tuple(s):
        return ( s.x, s.y, s.z, )
    
    # convert all the values to int
    def int(s):
        return vec3(int(s.x),int(s.y),int(s.z))
    
    # average the values
    def average(s, common:int = 1 ):
        return s / common
    
    def length(s):
        return sqrt((s.x*s.x)+(s.y*s.y)+(s.z*s.z))
    
    def normal(s):
        l = s.length()
        x = vec3(s.x,s.y,s.z)
        x.x /= l
        x.y /= l
        x.z /= l
        return x
    
    ## Math operators
    #addition
    def __add__(s, b):
        if type(b) in [ int, float ]:
            b = vec3(b,b,b)
        elif type(b) != vec3:
            raise TypeError("Can only add number or vector to vector")
        
        x = s.x + b.x
        y = s.y + b.y
        z =s.z + b.z
        
        return vec3(x, y, z)
    
    # subtraction
    def __sub__(s, b):
        if type(b) in [ int, float ]:
            b = vec3(b,b,b)
        elif type(b) != vec3:
            raise TypeError("Can only subtract number or vector from vector")
        
        x = s.x - b.x
        y = s.y - b.y
        z =s.z - b.z
        
        return vec3(x, y, z)
    
    # multiplication
    def __mul__(s, b):
        if type(b) in [ int, float ]:
            b = vec3(b,b,b)
        elif type(b) != vec3:
            raise TypeError("Can only multiply number or vector with vector")
        
        x = s.x * b.x
        y = s.y * b.y
        z =s.z * b.z
        
        return vec3(x, y, z)
    
    # divide
    def __truediv__(s, b):
        if type(b) in [ int, float ]:
            b = vec3(b,b,b)
        elif type(b) != vec3:
            raise TypeError("Can only divide vector by number or vector")
        
        x = s.x / b.x
        y = s.y / b.y
        z =s.z / b.z
        
        return vec3(x, y, z)
    
    # divide and floor
    def __floordiv__(s, b):
        if type(b) in [ int, float ]:
            b = vec3(b,b,b)
        elif type(b) != vec3:
            raise TypeError("Can only divide vector by number or vector")
        
        x = s.x // b.x
        y = s.y // b.y
        z =s.z // b.z
        
        return vec3(x, y, z)
    
    # modulus
    def __mod__(self, b):
        if type(b) in [ int, float ]:
            b = vec3(b,b,b)
        elif type(b) != vec3:
            raise TypeError("Can only take modulus of vector with number or vector")
        
        self.x %= b.x
        self.y %= b.y
        self.z %=b.z
        
        return vec3(self.x,self.y,self.z)
    
    # power
    def __pow__(s, b):
        if type(b) in [ int, float ]:
            b = vec3(b,b,b)
        elif type(b) != vec3:
            raise TypeError("Can only take the power of vector with number or vector")
        
        x = s.x ** b.x
        y = s.y ** b.y
        z =s.z ** b.z
        
        return vec3(x, y, z)
    
    ## Comparisons
    # less than
    def __lt__(s, b):
        if type(b) != vec3:
            raise TypeError("Can only compare vector with vector")
        
        x = s.x < b.x
        y = s.y < b.y
        z = s.z < b.z
        
        return x and y and z
    
    # greater than
    def __gt__(s, b):
        if type(b) != vec3:
            raise TypeError("Can only compare vector with vector")
        
        x = s.x > b.x
        y = s.y > b.y
        z = s.z > b.z
        
        return x and y and z
    
    # less or equal
    def __le__(s, b):
        if type(b) != vec3:
            raise TypeError("Can only compare vector with vector")
        
        x = s.x <= b.x
        y = s.y <= b.y
        z = s.z <= b.z
        
        return x and y and z
    
    # greator or equal
    def __ge__(s, b):
        if type(b) != vec3:
            raise TypeError("Can only compare vector with vector")
        
        x = s.x >= b.x
        y = s.y >= b.y
        z = s.z >= b.z
        
        return x and y and z
    
    # Equals
    def  __eq__(s, b):
        if type(b) != vec3:
            raise TypeError("Can only compare vector with vector")
        
        x = s.x == b.x
        y = s.y == b.y
        z = s.z == b.z
        
        return x and y and z
    
    # not equals
    def __ne__(s, b):
        if type(b) != vec3:
            raise TypeError("Can only compare vector with vector")
        
        x = s.x != b.x
        y = s.y != b.y
        z = s.z != b.z
        
        return x and y and z

# mess of a class
class vec2:
    
    def __init__(self, x:float = 0, y:float = 0 ):
        self.x = x
        self.y = y
    
    ## conversions
    # string
    def __str__(s):
        return "[ "+str(s.x)+" "+str(s.y)+" ]"
    
    # represetation
    def __repr__(s):
        return s.__str__()
    
    # list
    def __list__(s):
        return [ s.x, s.y ]
    
    # touple
    def __tuple__(s):
        return ( s.x, s.y )
    
    # dict
    def __dict__(s):
        return { "x": s.x, "y": s.y }
    
    # convert the vector to a tuple
    def tuple(s):
        return ( s.x, s.y )
    
    # convert all the values to int
    def int(s):
        return vec2(int(s.x),int(s.y))
    
    # average the values
    def average(s, common:int = 1 ):
        return s / common
    
    def length(s):
        return sqrt((s.x*s.x)+(s.y*s.y))
    
    def normal(s):
        l = s.length()
        x = vec2(s.x,s.y)
        x.x /= l
        x.y /= l
        return x
    
    def ceil(s):
        s.x = ceil(s.x)
        s.y = ceil(s.y)

        return s
    
    ## Math operators
    #addition
    def __add__(s, b):
        if type(b) in [ int, float ]:
            b = vec2(b,b)
        elif type(b) != vec2:
            raise TypeError("Can only add number or vector to vector")
        
        x = s.x + b.x
        y = s.y + b.y
        
        return vec2(x, y)
    
    # subtraction
    def __sub__(s, b):
        if type(b) in [ int, float ]:
            b = vec2(b,b)
        elif type(b) != vec2:
            raise TypeError("Can only subtract number or vector from vector")
        
        x = s.x - b.x
        y = s.y - b.y
        
        return vec2(x, y)
    
    # multiplication
    def __mul__(s, b):
        if type(b) in [ int, float ]:
            b = vec2(b,b)
        elif type(b) != vec2:
            raise TypeError("Can only multiply number or vector with vector")
        
        x = s.x * b.x
        y = s.y * b.y
        
        return vec2(x, y)
    
    # divide
    def __truediv__(s, b):
        if type(b) in [ int, float ]:
            b = vec2(b,b)
        elif type(b) != vec2:
            raise TypeError("Can only divide vector by number or vector")
        
        x = s.x / b.x
        y = s.y / b.y
        
        return vec2(x, y)
    
    # divide and floor
    def __floordiv__(s, b):
        if type(b) in [ int, float ]:
            b = vec2(b,b)
        elif type(b) != vec2:
            raise TypeError("Can only divide vector by number or vector")
        
        x = s.x // b.x
        y = s.y // b.y
        
        return vec2(x, y)
    
    # modulus
    def __mod__(self, b):
        if type(b) in [ int, float ]:
            b = vec2(b,b)
        elif type(b) != vec2:
            raise TypeError("Can only take modulus of vector with number or vector")
        
        self.x %= b.x
        self.y %= b.y
        
        return vec2(self.x,self.y)
    
    # power
    def __pow__(s, b):
        if type(b) in [ int, float ]:
            b = vec2(b,b)
        elif type(b) != vec2:
            raise TypeError("Can only take the power of vector with number or vector")
        
        x = s.x ** b.x
        y = s.y ** b.y
        
        return vec2(x, y)
    
    ## Comparisons
    # less than
    def __lt__(s, b):
        if type(b) != vec2:
            raise TypeError("Can only compare vector with vector")
        
        x = s.x < b.x
        y = s.y < b.y
        
        return x and y
    
    # greater than
    def __gt__(s, b):
        if type(b) != vec2:
            raise TypeError("Can only compare vector with vector")
        
        x = s.x > b.x
        y = s.y > b.y
        
        return x and y
    
    # less or equal
    def __le__(s, b):
        if type(b) != vec2:
            raise TypeError("Can only compare vector with vector")
        
        x = s.x <= b.x
        y = s.y <= b.y
        
        return x and y
    
    # greator or equal
    def __ge__(s, b):
        if type(b) != vec2:
            raise TypeError("Can only compare vector with vector")
        
        x = s.x >= b.x
        y = s.y >= b.y
        
        return x and y
    
    # Equals
    def  __eq__(s, b):
        if type(b) != vec2:
            raise TypeError("Can only compare vector with vector")
        
        x = s.x == b.x
        y = s.y == b.y
        
        return x and y
    
    # not equals
    def __ne__(s, b):
        if type(b) != vec2:
            raise TypeError("Can only compare vector with vector")
        
        x = s.x != b.x
        y = s.y != b.y
        
        return x and y