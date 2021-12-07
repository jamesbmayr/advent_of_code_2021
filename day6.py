# data

data = [3,5,1,5,3,2,1,3,4,2,5,1,3,3,2,5,1,3,1,5,5,1,1,1,2,4,1,4,5,2,1,2,4,3,1,2,3,4,3,4,4,5,1,1,1,1,5,5,3,4,4,4,5,3,4,1,4,3,3,2,1,1,3,3,3,2,1,3,5,2,3,4,2,5,4,5,4,4,2,2,3,3,3,3,5,4,2,3,1,2,1,1,2,2,5,1,1,4,1,5,3,2,1,4,1,5,1,4,5,2,1,1,1,4,5,4,2,4,5,4,2,4,4,1,1,2,2,1,1,2,3,3,2,5,2,1,1,2,1,1,1,3,2,3,1,5,4,5,3,3,2,1,1,1,3,5,1,1,4,4,5,4,3,3,3,3,2,4,5,2,1,1,1,4,2,4,2,2,5,5,5,4,1,1,5,1,5,2,1,3,3,2,5,2,1,2,4,3,3,1,5,4,1,1,1,4,2,5,5,4,4,3,4,3,1,5,5,2,5,4,2,3,4,1,1,4,4,3,4,1,3,4,1,1,4,3,2,2,5,3,1,4,4,4,1,3,4,3,1,5,3,3,5,5,4,4,1,2,4,2,2,3,1,1,4,5,3,1,1,1,1,3,5,4,1,1,2,1,1,2,1,2,3,1,1,3,2,2,5,5,1,5,5,1,4,4,3,5,4,4]



# part 1

def iterate_day(population):
	"""simulates how the population of fish changes after one day"""

	cycle_reset = 6
	childhood = 2

	new_population = []

	for fish in population:
		if fish == 0:
			new_population.append(cycle_reset)
			new_population.append(cycle_reset + childhood)
		else:
			new_population.append(fish - 1)

	return new_population



def iterate_for_days(population, days):
	"""simulates the population of fish changing for the given number of days"""

	today = 0
	while today < days:
		population = iterate_day(population)
		today += 1

	return {"size": len(population), "population": population}



# print(iterate_for_days(data, 80))



# part 2

def convert_to_counts(population):
	"""exponential looping was bad so this converts to counts"""

	cycle_length = 7
	childhood = 2
	
	population_counts = [0 for x in range(cycle_length + childhood)]

	for fish in population:
		population_counts[fish] = population_counts[fish] + 1

	return population_counts



def iterate_day_counts(population_counts):
	"""updates the population counts by one day"""

	cycle_length = 7
	childhood = 2

	new_population_counts = [0 for x in range(cycle_length + childhood)]

	index = 0
	while index < len(population_counts):
		if index == 0:
			new_population_counts[cycle_length + childhood - 1] += population_counts[index]
			new_population_counts[cycle_length - 1] += population_counts[index]
		else:
			new_population_counts[index - 1] += population_counts[index]
		index += 1

	return new_population_counts



def iterate_for_days_efficiently(population, days):
	"""simulates the population counts of fish for the given number of days"""

	population_counts = convert_to_counts(population)

	today = 0
	while today < days:
		population_counts = iterate_day_counts(population_counts)
		today += 1

	size = 0
	for count in population_counts:
		size += count

	return {"size": size, "population_counts": population_counts}



# print(iterate_for_days_efficiently(data, 256))
