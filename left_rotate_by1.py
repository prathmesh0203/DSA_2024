def rotate(nums):
    n = len(nums)
    index = 0
    arr = []
    
    for i in range(n-1):
        arr.append(nums[i+1])
        index +=1

    arr.append(nums[0])

    return arr

def rotate_by_k(nums,k):
    n = len(nums)
    new_arr = []
    for i in range(n):
        new_arr.append(0)

    for i in range(n):
        if (k+i)<(n-1):
            new_arr[i] = nums[k+i+1]
        else:
            new_arr[i] = nums[i-k]

    return new_arr


nums = [1,2,3,4,5,6,7]
k = 3
nums2 = [-1,-100,3,99]
k2 = 2

print(rotate(nums2))
        
        