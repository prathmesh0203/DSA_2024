from typing import List

def rotate(nums, k) -> None:
    temp = nums[:k]
    n = len(nums)
    for i in range(k,n):
        nums[i-k] = nums[i]
    
    j = 0
    for i in range(n-k,n):
        nums[i] = temp[j]
        j +=1
    
    return nums

