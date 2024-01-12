# The code here is the error fixed version of the decrypted text generated in part 1

global_var = 100
my_dict = {'key1': 'value1',  'key2': 'value2', 'key3': 'value3'}

def process_numbers(numbers = [1, 2, 3, 4, 5]): # numbers made into an optional argument
    global global_var
    local_var = 5

    while local_var > 0:
        if local_var % 2 == 0:
            numbers.remove(local_var)
        local_var -= 1

    return numbers

my_set = {1, 2, 3, 4, 5, 5, 4, 3, 2, 1}
result = process_numbers(numbers=my_set)

def modify_dict(local_var = 10): # local_variable made into optional argument
    my_dict['key4'] = local_var

modify_dict(5)

def update_global():
    global global_var
    global_var += 10

for i in range(5):
    print(i)
    i += 1

if my_set is not None and my_dict['key4'] == 10:
    print("Condition met!")

if 5 not in my_dict:
    print("5 not found in the dictionary!")

print(global_var)
print(my_dict)
print(my_set)