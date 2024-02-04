# O(n+n)
import sys
def getSecondOrderElements(n,a) -> [int]:
    max_element = a[0]
    min_element = a[0]
    for i in range(n):
        if a[i]> max_element:
            max_element = a[i]

        if a[i]< min_element:
            min_element = a[i]

    pre_max = -sys.maxsize
    pre_min = sys.maxsize

    for i in range(n):
        if a[i]> pre_max and a[i]< max_element:
            pre_max = a[i]

        if a[i]< pre_min and a[i]> min_element:
            pre_min = a[i]

    return [pre_max, pre_min]



#Optimal Solution
def getSecondMax(n,a):
    max = a[0]
    second_max = -1

    for i in range(n):
        if a[i] > max:
            second_max = max
            max = a[i]

        if (a[i]< max )and (a[i]> second_max):
            second_max =a[i]

    return second_max

def getSecondMin(n,a):
    min = a[0]
    second_min = sys.maxsize

    for i in range(n):
        if a[i]<min:
            second_min = min
            min = a[i]

        elif a[i]!= min and a[i]< second_min:
            second_min = a[i]

    return second_min

def getSecondOrderElements2(n,a):
    second_min = getSecondMin(n,a)
    second_max = getSecondMax(n,a)

    return [second_max,second_min]




# print("Better")
# print(getSecondOrderElements(6,[2,3,4,5,9,8]))
print("Optimal")
print(getSecondOrderElements2(6,[2,3,4,5,9,8]))


