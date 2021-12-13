# data

data = ['CV-mk','gm-IK','sk-gm','ca-sk','sx-mk','gm-start','sx-ca','kt-sk','ca-VS','kt-ml','kt-ca','mk-IK','end-sx','end-sk','gy-sx','end-ca','ca-ml','gm-CV','sx-kt','start-CV','IK-start','CV-kt','ml-mk','ml-CV','ml-gm','ml-IK']



# part 1

def count_valid_paths(data):
	"""determines the number of valid paths from start to end, not repeating capital caves"""

	mapping = get_connections(data)
	mapping = build_paths(mapping, ['start'])

	start_to_end_paths = 0
	for path in mapping['paths']:
		if path[len(path) - 1] == 'end':
			start_to_end_paths += 1

	return start_to_end_paths, mapping



def get_connections(paths):
	"""build more useful map"""

	mapping = {'caves': {}, 'paths': []}

	for path in paths:
		from_cave = path.split('-')[0]
		to_cave = path.split('-')[1]

		mapping = add_cave_to_map(from_cave, to_cave, mapping)
		mapping = add_cave_to_map(to_cave, from_cave, mapping)
	
	return mapping



def add_cave_to_map(from_cave, to_cave, mapping):
	"""adds this cave to the map"""

	if from_cave not in mapping['caves'].keys():
		mapping['caves'][from_cave] = {
			'type': None,
			'connections': [to_cave]
		}
		if from_cave == 'start':
			mapping['caves'][from_cave]['type'] = 'start'
		elif from_cave == 'end':
			mapping['caves'][from_cave]['type'] = 'end'
		elif from_cave.isupper():
			mapping['caves'][from_cave]['type'] = 'big'
		else:
			mapping['caves'][from_cave]['type'] = 'small'
	else:
		mapping['caves'][from_cave]['connections'].append(to_cave)

	return mapping



def build_paths(mapping, path):
	"""continues a particular path until its next junction, disallowing revisiting small caves"""

	if path not in mapping['paths']:
		mapping['paths'].append(path)

	last_visited = path[len(path) - 1]
	if last_visited == 'end':
		return mapping

	for destination in mapping['caves'][last_visited]['connections']:
		if destination in path and mapping['caves'][destination]['type'] != 'big':
			continue
		else:
			new_path = path.copy()
			new_path.append(destination)
			mapping = build_paths(mapping, new_path)

	return mapping



# print(count_valid_paths(data))



# part 2

def build_paths(mapping, path):
	"""continues a particular path until its next junction, allowing revisiting only one small cave per path"""

	if path in mapping['paths']:
		return mapping

	mapping['paths'].append(path)

	last_visited = path[len(path) - 1]
	if last_visited == 'end':
		return mapping

	for destination in mapping['caves'][last_visited]['connections']:
		if destination in path and mapping['caves'][destination]['type'] == 'start':
			continue
		elif destination in path and mapping['caves'][destination]['type'] == 'end':
			continue
		elif destination in path and mapping['caves'][destination]['type'] == 'small':
			small_caves_visited = []
			time_for_more = True
			for cave in path:
				if mapping['caves'][cave]['type'] != 'small':
					continue
				elif cave in small_caves_visited:
					time_for_more = False
					break
				else:
					small_caves_visited.append(cave)

			if time_for_more:
				new_path = path.copy()
				new_path.append(destination)
				mapping = build_paths(mapping, new_path)
		else:
			new_path = path.copy()
			new_path.append(destination)
			mapping = build_paths(mapping, new_path)

	return mapping



# print(count_valid_paths(data))
