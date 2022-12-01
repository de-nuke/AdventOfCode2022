"""
Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?

https://adventofcode.com/2022/day/1#part2
"""
calories_sums = []
calories_sum = 0
elf_number = None
with open("input.txt", "r") as f:
    for i, calories_line in enumerate(f.readlines(), start=1):
        print(calories_line)
        calories = calories_line.strip()
        if calories:
            calories_sum += int(calories)
        else:
            calories_sums.append(calories_sum)
            calories_sum = 0

sorted_calories_sums = list(reversed(sorted(calories_sums)))
print("Number of elves:", i)
print("Calories of top three elves:", sorted_calories_sums[0:3])
print("Sum of top three calories:", sum(sorted_calories_sums[0:3]))
