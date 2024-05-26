def even_odd_reorder(arr):
    print("Reordering even and odd elements of the array, even first")
    next_even, next_odd = 0, len(arr) - 1
    """O(n) time complexity and O(1) space complexity"""
    while next_even < next_odd:
        if arr[next_even] % 2 == 0:
            next_even += 1
        else:
            arr[next_even], arr[next_odd] = arr[next_odd], arr[next_even]
            next_odd -= 1
    return arr


class Notes:
    """Notes related to arrays"""
    print("Retreiving and updating a[i] takes O(1) time")
    print("Deletion from an array at i index takes O(n - 1) time")
    """Performing array operations like re-ordering takes
    O(N) time where N is the length of the array
    Array prblems can be solved by breaking the array into subarrays
    """
    sample_input = [1, 2, 3, 4, 5, 6]
    print(even_odd_reorder(sample_input))
    """Instead of deleting an array consider overwriting it
    Filling an array from the front is slow, see if its possible to write values from the back
    when operating on 2d arrays use parallel logic for rows and columns
    Arrays in python are provided by list type
    tuples are very similar to list except for the fact that they are immutable
    Lists can be dynamically resized in python
    Basic operations: len(A), A.append(42), A.remove(42), A.insert(3, 29)"""

