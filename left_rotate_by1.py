def rotate(nums):
    n = len(nums)
    index = 0
    arr = []
    
    for i in range(n-1):
        arr.append(nums[i+1])
        index +=1

    arr.append(nums[0])

    return arr


        
        