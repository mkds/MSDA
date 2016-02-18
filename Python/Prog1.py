__author__ = 'Mohan Kandaraj'

# 1. fill in this function
#   it takes a list for input and return a sorted version
#   do this with a loop, don't use the built in list functions
def sortwithloops(input):
    """Implements Quick Sort"""
    if len(input) > 1:
        pivot = input[-1]
        swapPos = 0
        for i in range(0, len(input)):
            val = input[i]
            if val <= pivot:
                t = input[swapPos]
                input[swapPos] = val
                input[i] = t
                swapPos = swapPos + 1
        left = input[:swapPos - 1]
        right = input[swapPos:]
        inpos = input[swapPos - 1:swapPos]
        #Recursive Call
        return (sortwithloops(left) + inpos + sortwithloops(right))
    else:
        return input


#2. fill in this function
#   it takes a list for input and return a sorted version
#   do this with the built in list functions, don't use a loop
def sortwithoutloops(input):
    input.sort()
    return input  #return a value


#3. fill in this function
#   it takes a list for input and a value to search for
#	it returns true if the value is in the list, otherwise false
#   do this with a loop, don't use the built in list functions
def searchwithloops(input, value):
    for element in input:
        if value == element:
            return True
    return False



#4. fill in this function
#   it takes a list for input and a value to search for
#	it returns true if the value is in the list, otherwise false
#   do this with the built in list functions, don't use a loop
def searchwithoutloops(input, value):
    return value in input  #return a value


if __name__ == "__main__":
    L = [5, 3, 6, 3, 13, 5, 6]

    print sortwithloops(L)  # [3, 3, 5, 5, 6, 6, 13]
    print sortwithoutloops(L)  # [3, 3, 5, 5, 6, 6, 13]
    print searchwithloops(L, 5)  #true
    print searchwithloops(L, 11)  #false
    print searchwithoutloops(L, 5)  #true
    print searchwithoutloops(L, 11)  #false