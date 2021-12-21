# part 1

def get_lights_after_n_upgrades(file_name, n):
	"""given file name and number of upgrades, count the number of lights"""

	image_algorithm, image = get_algorithm_and_image(file_name)
	image_history = [image]
	print(image)

	while len(image_history) - 1 < n:
		next_image = get_next_image(image_algorithm, image_history[-1], len(image_history) - 1)
		print(next_image[0])
		image_history.append(next_image)

	return count_lights(image_history[-1])



def get_algorithm_and_image(file_name):
	with open(file_name) as file:
		lines = file.readlines()
		lines = [element.strip() for element in lines]

	image_algorithm = lines[0]
	image = lines[2:]
	return image_algorithm, image



def get_next_image(image_algorithm, image, iteration):
	"""loop through image pixels and get the next pixel for each"""

	height = len(image)
	width = len(image[0])

	next_image = []

	y = -1
	while y < height + 1:
		row = []
		next_image.append(row)
		x = -1
		while x < width + 1:
			pixels = get_9_grid_pixels(image, x, y, height, width, iteration)
			binary_string = convert_to_binary_string(pixels)
			decimal = convert_binary_to_decimal(binary_string)
			next_pixel = get_next_pixel(image_algorithm, decimal)
			row.append(next_pixel)
			x += 1
		y += 1

	return next_image



def get_9_grid_pixels(image, x, y, height, width, iteration):
	"""given coordinates, get the set of 9 pixels (neighbors and self)"""

	pixels = []
	for dy in range(-1, 2):
		for dx in range(-1, 2):
			cell_x = x + dx
			cell_y = y + dy

			if cell_x >= 0 and cell_y >= 0 and cell_x < width and cell_y < height:
				pixels.append(image[cell_y][cell_x])
			else:
				if iteration % 2 == 0:
					pixels.append('.')
				else:
					pixels.append('#')

	return pixels



def convert_to_binary_string(pixels):
	"""input 9 pixels and output a decimal number"""

	binary_string = ''

	for pixel in pixels:
		if pixel == '#':
			binary_string += '1'
		else:
			binary_string += '0'

	return binary_string



def convert_binary_to_decimal(binary_string):
	"""takes a binary string and outputs a decimal number"""

	return int(binary_string, 2)



def get_next_pixel(image_algorithm, number):
	"""given a number, get the next pixel from the image algorithm"""

	return image_algorithm[number]



def count_lights(image):
	"""given an image, count the number of # and ."""

	num_light = 0
	num_dark = 0

	height = len(image)
	width = len(image[0])

	y = 0
	while y < width:
		x = 0
		while x < width:
			if image[y][x] == '#':
				num_light += 1
			else:
				num_dark += 1
			x += 1
		y += 1

	return {'num_light': num_light, 'num_dark': num_dark}



# print(get_lights_after_n_upgrades('input_20.txt', 2))



# part 2

# print(get_lights_after_n_upgrades('input_20.txt', 50))
