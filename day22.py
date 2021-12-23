# part 1

def get_instructions(file_name):
	"""get a list of structured instructions"""

	# read the lines from the file
	with open(file_name) as file:
		lines = file.readlines()
		lines = [element.strip() for element in lines]

	# loop through the file
	instructions = []
	for line in lines:

		# pase the information
		parsed_line = line.split(' ')
		action = parsed_line[0]
		coordinates = parsed_line[1].split(',')
		x = coordinates[0].split('=')[1].split('..')
		y = coordinates[1].split('=')[1].split('..')
		z = coordinates[2].split('=')[1].split('..')

		# compile into a dictionary
		instructions.append({
			'action': action,
			'x_start': int(x[0]),
			'x_end': int(x[1]),
			'y_start': int(y[0]),
			'y_end': int(y[1]),
			'z_start': int(z[0]),
			'z_end': int(z[1])
		})

	return instructions



def run_instruction(state, instruction, bounds):
	"""update the state given an instruction and a set of bounds"""

	# skip out-of-bounds instructions
	if bounds:
		for edge in instruction.values():
			if type(edge) == int and (edge < bounds[0] or edge > bounds[1]):
				return state

	# loop through the cuboid
	x = instruction['x_start']
	while x <= instruction['x_end']:
		y = instruction['y_start']
		while y <= instruction['y_end']:
			z = instruction['z_start']
			while z <= instruction['z_end']:

				# get current coordinates
				cell = str(x) + ',' + str(y) + ',' + str(z)

				# turning on
				if cell not in state and instruction['action'] == 'on':
					state.add(cell)

				# turning off
				elif cell in state and instruction['action'] == 'off':
					state.remove(cell)

				z += 1
			y += 1
		x += 1

	return state



def get_state_after_instructions(instructions, bounds):
	"""given a set of instructions, determine the final state"""

	state = set()
	for instruction in instructions:
		state = run_instruction(state, instruction, bounds)

	return state



# print(len(get_state_after_instructions(get_instructions('input_22.txt'), [-50, 50])))



# part 2

def has_overlap(prism_a, prism_b):
	"""determine if there is overlap between two prisms"""

	# A--A--B--B
	if prism_a['x_end'] < prism_b['x_start']:
		return False
	# B--B--A--A
	if prism_b['x_end'] < prism_a['x_start']:
		return False
	# A--A--B--B
	if prism_a['y_end'] < prism_b['y_start']:
		return False
	# B--B--A--A
	if prism_b['y_end'] < prism_a['y_start']:
		return False
	# A--A--B--B
	if prism_a['z_end'] < prism_b['z_start']:
		return False
	# B--B--A--A
	if prism_b['z_end'] < prism_a['z_start']:
		return False

	return True



def get_overlap(prism_a, prism_b):
	"""determine the volume of overlap between two prisms, if any"""

	if not has_overlap(prism_a, prism_b):
		return None

	# assume no overlap
	overlap = {'x_start': None, 'x_end': None, 'y_start': None, 'y_end': None, 'z_start': None, 'z_end': None}

	# check x
	# A--B--A--B
	if prism_a['x_start'] < prism_b['x_start'] and prism_b['x_start'] <= prism_a['x_end'] and prism_a['x_end'] < prism_b['x_end']:
		overlap['x_start'], overlap['x_end'] = prism_b['x_start'], prism_a['x_end']
	# A--B--B--A
	elif prism_a['x_start'] <= prism_b['x_start'] and prism_b['x_end'] <= prism_a['x_end']:
		overlap['x_start'], overlap['x_end'] = prism_b['x_start'], prism_b['x_end']
	# B--A--B--A
	elif prism_b['x_start'] < prism_a['x_start'] and prism_a['x_start'] <= prism_b['x_end'] and prism_b['x_end'] < prism_a['x_end']:
		overlap['x_start'], overlap['x_end'] = prism_a['x_start'], prism_b['x_end']
	# B--A--A--B
	elif prism_b['x_start'] <= prism_a['x_start'] and prism_a['x_end'] <= prism_b['x_end']:
		overlap['x_start'], overlap['x_end'] = prism_a['x_start'], prism_a['x_end']

	# check y
	# A--B--A--B
	if prism_a['y_start'] < prism_b['y_start'] and prism_b['y_start'] <= prism_a['y_end'] and prism_a['y_end'] < prism_b['y_end']:
		overlap['y_start'], overlap['y_end'] = prism_b['y_start'], prism_a['y_end']
	# A--B--B--A
	elif prism_a['y_start'] <= prism_b['y_start'] and prism_b['y_end'] <= prism_a['y_end']:
		overlap['y_start'], overlap['y_end'] = prism_b['y_start'], prism_b['y_end']
	# B--A--B--A
	elif prism_b['y_start'] < prism_a['y_start'] and prism_a['y_start'] <= prism_b['y_end'] and prism_b['y_end'] < prism_a['y_end']:
		overlap['y_start'], overlap['y_end'] = prism_a['y_start'], prism_b['y_end']
	# B--A--A--B
	elif prism_b['y_start'] <= prism_a['y_start'] and prism_a['y_end'] <= prism_b['y_end']:
		overlap['y_start'], overlap['y_end'] = prism_a['y_start'], prism_a['y_end']

	# check z
	# A--B--A--B
	if prism_a['z_start'] < prism_b['z_start'] and prism_b['z_start'] <= prism_a['z_end'] and prism_a['z_end'] < prism_b['z_end']:
		overlap['z_start'], overlap['z_end'] = prism_b['z_start'], prism_a['z_end']
	# A--B--B--A
	elif prism_a['z_start'] <= prism_b['z_start'] and prism_b['z_end'] <= prism_a['z_end']:
		overlap['z_start'], overlap['z_end'] = prism_b['z_start'], prism_b['z_end']
	# B--A--B--A
	elif prism_b['z_start'] < prism_a['z_start'] and prism_a['z_start'] <= prism_b['z_end'] and prism_b['z_end'] < prism_a['z_end']:
		overlap['z_start'], overlap['z_end'] = prism_a['z_start'], prism_b['z_end']
	# B--A--A--B
	elif prism_b['z_start'] <= prism_a['z_start'] and prism_a['z_end'] <= prism_b['z_end']:
		overlap['z_start'], overlap['z_end'] = prism_a['z_start'], prism_a['z_end']

	# no overlap
	if overlap['x_start'] != None and overlap['y_start'] != None and overlap['z_start'] != None:
		return overlap
	else:
		return None



def intersect_two_prisms(prism_a, prism_b):
	"""get the overlap region, a split into regions, and b split into regions"""

	# get overlap
	overlap = get_overlap(prism_a, prism_b)
	
	# no overlap? easy
	if not overlap:
		return [prism_a], [prism_b], None

	# overlap? get subprisms
	subprisms_a = split_into_non_overlapping_prisms(prism_a, overlap)
	subprisms_b = split_into_non_overlapping_prisms(prism_b, overlap)

	return subprisms_a, subprisms_b, overlap



def split_into_non_overlapping_prisms(prism, overlap):
	"""split the prism into 8-27 prisms and return the ones that are not the overlap"""
	# x-split
	# OAA
	if overlap['x_start'] == prism['x_start'] and overlap['x_end'] < prism['x_end']:
		edges_x = [
			{'x_start': overlap['x_start'], 'x_end': overlap['x_end'], 'is_overlap': True},
			{'x_start': overlap['x_end'] + 1, 'x_end': prism['x_end']}
		]
	# AOA
	elif overlap['x_start'] > prism['x_start'] and overlap['x_end'] < prism['x_end']:
		edges_x = [
			{'x_start': prism['x_start'], 'x_end': overlap['x_start'] - 1},
			{'x_start': overlap['x_start'], 'x_end': overlap['x_end'], 'is_overlap': True},
			{'x_start': overlap['x_end'] + 1, 'x_end': prism['x_end']}
		]
	# AAO
	elif overlap['x_start'] > prism['x_start'] and overlap['x_end'] == prism['x_end']:
		edges_x = [
			{'x_start': prism['x_start'], 'x_end': overlap['x_start'] - 1},
			{'x_start': overlap['x_start'], 'x_end': overlap['x_end'], 'is_overlap': True}
		]
	# O
	elif overlap['x_start'] == prism['x_start'] and overlap['x_end'] == prism['x_end']:
		edges_x = [
			{'x_start': overlap['x_start'], 'x_end': overlap['x_end'], 'is_overlap': True}
		]

	# y-split
	# OAA
	if overlap['y_start'] == prism['y_start'] and overlap['y_end'] < prism['y_end']:
		edges_y = [
			{'y_start': overlap['y_start'], 'y_end': overlap['y_end'], 'is_overlap': True},
			{'y_start': overlap['y_end'] + 1, 'y_end': prism['y_end']}
		]
	# AOA
	elif overlap['y_start'] > prism['y_start'] and overlap['y_end'] < prism['y_end']:
		edges_y = [
			{'y_start': prism['y_start'], 'y_end': overlap['y_start'] - 1},
			{'y_start': overlap['y_start'], 'y_end': overlap['y_end'], 'is_overlap': True},
			{'y_start': overlap['y_end'] + 1, 'y_end': prism['y_end']}
		]
	# AAO
	elif overlap['y_start'] > prism['y_start'] and overlap['y_end'] == prism['y_end']:
		edges_y = [
			{'y_start': prism['y_start'], 'y_end': overlap['y_start'] - 1},
			{'y_start': overlap['y_start'], 'y_end': overlap['y_end'], 'is_overlap': True}
		]
	# O
	elif overlap['y_start'] == prism['y_start'] and overlap['y_end'] == prism['y_end']:
		edges_y = [
			{'y_start': overlap['y_start'], 'y_end': overlap['y_end'], 'is_overlap': True}
		]

	# z-split
	# OAA
	if overlap['z_start'] == prism['z_start'] and overlap['z_end'] < prism['z_end']:
		edges_z = [
			{'z_start': overlap['z_start'], 'z_end': overlap['z_end'], 'is_overlap': True},
			{'z_start': overlap['z_end'] + 1, 'z_end': prism['z_end']}
		]
	# AOA
	elif overlap['z_start'] > prism['z_start'] and overlap['z_end'] < prism['z_end']:
		edges_z = [
			{'z_start': prism['z_start'], 'z_end': overlap['z_start'] - 1},
			{'z_start': overlap['z_start'], 'z_end': overlap['z_end'], 'is_overlap': True},
			{'z_start': overlap['z_end'] + 1, 'z_end': prism['z_end']}
		]
	# AAO
	elif overlap['z_start'] > prism['z_start'] and overlap['z_end'] == prism['z_end']:
		edges_z = [
			{'z_start': prism['z_start'], 'z_end': overlap['z_start'] - 1},
			{'z_start': overlap['z_start'], 'z_end': overlap['z_end'], 'is_overlap': True}
		]
	# O
	elif overlap['z_start'] == prism['z_start'] and overlap['z_end'] == prism['z_end']:
		edges_z = [
			{'z_start': overlap['z_start'], 'z_end': overlap['z_end'], 'is_overlap': True}
		]

	# build prisms from all combinations of edges
	subprisms = []
	for edge_x in edges_x:
		for edge_y in edges_y:
			for edge_z in edges_z:
				if 'is_overlap' in edge_x and 'is_overlap' in edge_y and 'is_overlap' in edge_z:
					continue
				subprism = {}
				subprism.update(edge_x)
				subprism.update(edge_y)
				subprism.update(edge_z)
				if 'is_overlap' in subprism:
					subprism.pop('is_overlap')
				subprisms.append(subprism)

	return subprisms



def get_illuminated_regions(instructions):
	"""given a set of instructions, determine which regions are illuminated at the end"""

	nonoverlapping_illuminated_prisms = []
	for instruction in instructions:
		nonoverlapping_illuminated_prisms = apply_instruction(nonoverlapping_illuminated_prisms, instruction)

	return nonoverlapping_illuminated_prisms, count_illuminated_cells(nonoverlapping_illuminated_prisms)



def apply_instruction(nonoverlapping_illuminated_prisms, original_instruction):
	"""split the existing prisms into smaller prisms where they overlap with the instruction prism"""

	# set up the loop
	action = original_instruction.pop('action')
	instructions = [original_instruction]
	overlaps = []

	# loop through illuminated prisms to find which ones overlap
	prism_index = 0
	while prism_index < len(nonoverlapping_illuminated_prisms):

		# no overlap with the original instruction
		if not has_overlap(nonoverlapping_illuminated_prisms[prism_index], original_instruction):
			prism_index += 1
			continue

		# loop through all the current instruction subprisms
		instruction_index = 0
		while instruction_index < len(instructions):
			# get the subprisms of a, b, and overlap
			subprisms_a, subprisms_b, overlap = intersect_two_prisms(nonoverlapping_illuminated_prisms[prism_index], instructions[instruction_index])

			# no overlap
			if not overlap:
				instruction_index += 1
				continue

			# overlap
			overlaps.append(overlap)
			nonoverlapping_illuminated_prisms[prism_index:prism_index + 1] = subprisms_a
			prism_index -= 1
			instructions[instruction_index:instruction_index + 1] = subprisms_b
			instruction_index += len(subprisms_b)

		prism_index += 1

	# what to do about overlaps & subprisms
	if action == 'on':
		for overlap in overlaps:
			nonoverlapping_illuminated_prisms.append(overlap)
		for subprism in instructions:
			nonoverlapping_illuminated_prisms.append(subprism)			

	return nonoverlapping_illuminated_prisms




def count_illuminated_cells(prisms):
	"""loop through all nonoverlapping prisms and count up illuminated cells"""

	illuminated_count = 0
	for prism in prisms:
		volume = (prism['x_end'] - prism['x_start'] + 1) * (prism['y_end'] - prism['y_start'] + 1) * (prism['z_end'] - prism['z_start'] + 1)
		illuminated_count += volume

	return illuminated_count



# print(get_illuminated_regions(get_instructions('input_22.txt')))
