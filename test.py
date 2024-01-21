# Sample list of numbers
original_list = [1, 2, 3, 4, 5]

# Repeat each number 5 times using list comprehension
result_list = [num for num in original_list for _ in range(5)]

# Display the result
print(result_list)