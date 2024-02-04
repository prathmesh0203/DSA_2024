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
def getSecondOrderElements2(n,a):
    max_ele = a[0]
    second_max = 0

    for i in range(n):
        if a[i]>max_ele:
            max_ele = a[i]
            second_max = 


print("Better")
print(getSecondOrderElements(6,[2,3,4,5,9,8]))
print("Optimal")
print(getSecondOrderElements2(6,[2,3,4,5,9,8]))


