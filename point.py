#create a list of names
names = ["Alice", "Bob", "Charlie"]
# print the list of names
print(names)

#modify the function by randomly selecting a name from the list and print a greeting
import random

def print_random_greeting(name_list):
    name = random.choice(name_list)
    print(f"Hello, {name}!")

print_random_greeting(names)