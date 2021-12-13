# data

data = ['3172537688','4566483125','6374512653','8321148885','4342747758','1362188582','7582213132','6887875268','7635112787','7242787273']


# part 1

def count_flashes(data, steps):
	"""converts to grid, then simulates # days and counts flashes"""

	grid = convert_to_grid(data)

	flashes = 0
	step = 0
	while step < steps:
		grid, new_flashes = simulate_step(grid)
		flashes += new_flashes
		step += 1

	return {'flashes': flashes, 'grid': grid}



def convert_to_grid(rows):
	"""turns rows into 2-dimensional grid"""

	# this will create grid[y][x]
	grid = []
	for row in rows:
		new_row = []
		for number in list(row):
			cell = {'energy': int(number), 'flashed': False}
			new_row.append(cell)
		grid.append(new_row)

	return grid



def simulate_step(grid):
	"""simulates a step in time"""

	x = 0
	y = 0
	height = len(grid)
	width = len(grid[0])

	unresolved_nines = 0
	for x in range(width):
		for y in range(height):
			grid[y][x]['energy'] += 1
			if grid[y][x]['energy'] > 9 and not grid[y][x]['flashed']:
				unresolved_nines += 1

	while unresolved_nines > 0:
		for x in range(width):
			for y in range(height):
				if grid[y][x]['energy'] > 9 and not grid[y][x]['flashed']:
					grid[y][x]['flashed'] = True
					unresolved_nines -= 1

					# all directions
					if y - 1 >= 0 and x - 1 >= 0 and not grid[y - 1][x - 1]['flashed'] and grid[y - 1][x - 1]['energy'] <= 9:
						grid[y - 1][x - 1]['energy'] += 1
						if grid[y - 1][x - 1]['energy'] > 9:
							unresolved_nines += 1
					if y - 1 >= 0 and not grid[y - 1][x]['flashed'] and grid[y - 1][x]['energy'] <= 9:
						grid[y - 1][x]['energy'] += 1
						if grid[y - 1][x]['energy'] > 9:
							unresolved_nines += 1
					if y - 1 >= 0 and x + 1 < width and not grid[y - 1][x + 1]['flashed'] and grid[y - 1][x + 1]['energy'] <= 9:
						grid[y - 1][x + 1]['energy'] += 1
						if grid[y - 1][x + 1]['energy'] > 9:
							unresolved_nines += 1
					if x + 1 < width and not grid[y][x + 1]['flashed'] and grid[y][x + 1]['energy'] <= 9:
						grid[y][x + 1]['energy'] += 1
						if grid[y][x + 1]['energy'] > 9:
							unresolved_nines += 1
					if y + 1 < height and x + 1 < width and not grid[y + 1][x + 1]['flashed'] and grid[y + 1][x + 1]['energy'] <= 9:
						grid[y + 1][x + 1]['energy'] += 1
						if grid[y + 1][x + 1]['energy'] > 9:
							unresolved_nines += 1
					if y + 1 < height and not grid[y + 1][x]['flashed'] and grid[y + 1][x]['energy'] <= 9:
						grid[y + 1][x]['energy'] += 1
						if grid[y + 1][x]['energy'] > 9:
							unresolved_nines += 1
					if y + 1 < height and x - 1 >= 0 and not grid[y + 1][x - 1]['flashed'] and grid[y + 1][x - 1]['energy'] <= 9:
						grid[y + 1][x - 1]['energy'] += 1
						if grid[y + 1][x - 1]['energy'] > 9:
							unresolved_nines += 1
					if x - 1 >= 0 and not grid[y][x - 1]['flashed'] and grid[y][x - 1]['energy'] <= 9:
						grid[y][x - 1]['energy'] += 1
						if grid[y][x - 1]['energy'] > 9:
							unresolved_nines += 1

	flashes = 0
	for x in range(width):
		for y in range(height):
			if grid[y][x]['flashed']:
				flashes += 1
				grid[y][x]['flashed'] = False
				grid[y][x]['energy'] = 0

	return grid, flashes



# print(count_flashes(data, 100))



# part 2

def find_first_synchronization(data):
	"""finds the first time all octopuses flash simultaneously"""

	grid = convert_to_grid(data)
	step = 0
	flashes = 0

	while not is_all_zeroes(grid):
		grid, new_flashes = simulate_step(grid)
		flashes += new_flashes
		step += 1

	return {'steps': step, 'flashes': flashes, 'grid': grid}



def is_all_zeroes(grid):
	"""determines if all octopuses just flashed and are now all zeroes"""

	x = 0
	y = 0
	height = len(grid)
	width = len(grid[0])

	for x in range(width):
		for y in range(height):
			if grid[y][x]['energy'] != 0:
				return False

	return True



# print(find_first_synchronization(data))
