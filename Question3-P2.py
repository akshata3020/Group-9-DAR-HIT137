global_variable = 100
my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

def process_numbers(numbers):#Make the variables of the function input
    global global_variable
    local_variable = 5

    while local_variable > 0:
        if local_variable % 2 == 0:
            numbers.remove(local_variable)
        local_variable -= 1

    return numbers

my_set = {1,2,3,4,5,5,4,3,2,1}
result = process_numbers(numbers = my_set)
def modify_dict(local_variable):#Make the variables of the function input
    my_dict['key4'] = local_variable

modify_dict(5)

def update_global():
    global global_variable
    global_variable += 10
update_global()#Use this function once
for i in range(5):
    print(i)
    i += 1 #useless
if my_set is not None and my_dict['key4'] == 10:
    print("contition met!")
if 5 not in my_dict:
    print("5 not found in the dictionary!")# in only can Query whether the key is in the dictionary,
                                           # but cannot determine whether the value is in the dictionary
print(global_variable)
print(my_dict)
print(my_set)
