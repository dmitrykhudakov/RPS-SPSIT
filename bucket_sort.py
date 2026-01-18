def bucket_sort(arr):
    if not arr:
        return []
    
    if len(arr) <= 1:
        return arr.copy()
    
    num_buckets = len(arr)
    
    min_val = min(arr)
    max_val = max(arr)
    
    if min_val == max_val:
        return arr.copy()
    
    buckets = [[] for _ in range(num_buckets)]
    
    for num in arr:
        index = int((num - min_val) * (num_buckets - 1) / (max_val - min_val + 1))
        index = max(0, min(index, num_buckets - 1))
        buckets[index].append(num)
    
    for i in range(num_buckets):
        if buckets[i]:
            buckets[i] = insertion_sort(buckets[i])
    
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result


def insertion_sort(arr):
    if len(arr) <= 1:
        return arr
    
    sorted_arr = arr.copy()
    
    for i in range(1, len(sorted_arr)):
        key = sorted_arr[i]
        j = i - 1
        
        while j >= 0 and sorted_arr[j] > key:
            sorted_arr[j + 1] = sorted_arr[j]
            j -= 1
        
        sorted_arr[j + 1] = key
    
    return sorted_arr