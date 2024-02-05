def remove_duplicates(a):
    freq_dict = {}
    for ele in a:
        if ele in freq_dict.keys():
            freq_dict[ele] +=1
        else:
            freq_dict[ele] = 1
    
    final_arr = []
    for ele in freq_dict.keys():
        if freq_dict[ele] == 1:
            final_arr.append(ele)
    
    return final_arr

array = [1,2,3,4,5,5,1]
array2 = [1,2,2,2,2,2,2]

print(remove_duplicates(array))
print(remove_duplicates(array2))
