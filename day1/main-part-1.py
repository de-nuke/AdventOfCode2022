"""
Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?

https://adventofcode.com/2022/day/1
"""
calories_sum = 0
total_max_calories = 0
elf_number = None
with open("input.txt", "r") as f:
    for i, calories_line in enumerate(f.readlines(), start=1):
        print(calories_line)
        calories = calories_line.strip()
        if calories:
            calories_sum += int(calories)
        else:
            if calories_sum > total_max_calories:
                total_max_calories = calories_sum
                elf_number = i
            calories_sum = 0

print("Number of elves:", i)
print("Most calories:", total_max_calories)
print("Which elf?:", elf_number)
