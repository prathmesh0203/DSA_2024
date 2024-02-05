def checksorted(a):
    n = len(a)
    sum = 0
    for i in range(1,n):
        if a[i] < a[i-1]:
            sum += 1
        else:
            sum = sum
    
    return(sum == 0)

    
arr = [1,2,3,4,5]
arr2 = [3,4,5,6,8]

print(checksorted(arr))
print(checksorted(arr2))
            