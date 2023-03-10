import sympy as sym
from fractions import Fraction

def main():
    k = sym.Symbol('k')
    coef = [1,4,1,-6+k]
    matrix = routh_array(coef) 

    if len(matrix) != len(coef):
        print("Original Array:")
        print_matrix(matrix,len(coef)) 
        s = sym.Symbol('s')
        print(s**2*matrix[-2][0]+matrix[-2][1])
        print("Pole Crossing located at: " 
                + str(sym.solve(s**2*matrix[-2][0]+matrix[-2][1])))

        print("\nReversed Array to check stability:")
        matrix = routh_array(coef[::-1])

    print_matrix(matrix,len(coef))
    stable = check_stability(matrix) 
    if stable is True and len(matrix) is len(coef):
        print("System is Stable")

def first_layers(coef):
    a = coef[::2]
    b = coef[1::2] 
    b += [0]*(len(a)-len(b))
    return [a,b]

def routh_array(coef):
    lines = first_layers(coef) 
    for i in range(len(coef)-2):
        new_line  = []
        new_value = [0]*len(lines[0])
        for j in range(1,len(lines[0])):
            new_value[j-1] = (find_next([lines[-2][0],lines[-2][j]],
                                [lines[-1][0],lines[-1][j]]))
            if new_value[j-1] == 'nan':
                return lines 
        lines += [new_value]
    return lines

def find_next(a,b):
    if b[0] == 0:
        return 'nan'
    try:
       terms = Fraction(b[0]*a[1]/b[0]).limit_denominator()
    except TypeError:
       terms = b[0]*a[1]/b[0]
    try:
       terms -= Fraction(a[0]*b[1]/b[0]).limit_denominator()
    except TypeError:
       terms -= a[0]*b[1]/b[0]
    return terms 

def print_matrix(lines,len_coef):
    # get largest term length for each column
    col_max = [1]*len(lines[0])
    for line in lines:
        for i,term in enumerate(line):
            col_max[i] = max(col_max[i],len(str(term)))

    # draw top line
    print(end="   ┌")
    for width in col_max[:-1]:
        for i in range(width):
            print(" ",end="")
        print("   ",end="")
    for i in range(col_max[-1]):
        print(" ",end="")
    print("  ┐")

    # match the column width to the largest term and center 
    for indx, line in enumerate(lines):
        print("s"+replace_suberscript(str(len_coef-indx-1).ljust(1)),end=" ")
        print(end="│ ")
        for i,term in enumerate(line[:-1]):
            print(str(term).center(int(col_max[i])),end=" , ")
        print(str(line[-1]).center(int(col_max[i+1]))+" │")

    # draw bottom line
    print(end="   └")
    for width in col_max[:-1]:
        for i in range(width):
            print(" ",end="")
        print("   ",end="")
    for i in range(col_max[-1]):
        print(" ",end="")
    print("  ┘",end="\n\n")
    
def replace_suberscript(number):
    super_scripts = ["⁰","¹","²","³","⁴","⁵","⁶","⁷","⁸","⁹"]
    number = str(number)
    for indx, script in enumerate(super_scripts):
        number = number.replace(str(indx),script)
    return number

def check_stability(lines):
    k_values = []
    k_ranges = []
    for line in lines:
        try:
            if line[0] < 0:
                print("System not stable")
                return False

        except TypeError:
            k_ranges.append(sym.solve(line[0]>0))
            k_values.append(sym.solve(line[0]))
            
    if len(k_values) == 0:
        return True

    else:
        print("Decision Boundaries: ")
        for value in sum(k_values,[]):
            print(Fraction(float(value)).limit_denominator(),end=" ")
        print(end="\n")
        for k_range in k_ranges:
            print(k_range)
        
    return sum(k_values,[])

if __name__ == '__main__':
  main()
