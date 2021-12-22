# data

data = {'player_1': 8, 'player_2': 10}



# part 1

def simulate_deterministic_game(player_positions, options):
	"""roll a predestined die of X sides, with specific starting positions, and determine everything"""

	# initialize the game state based on input positions and rules that I imagine will change in part 2
	game_state = {
		'player_1': {
			'position': player_positions['player_1'],
			'score': 0
		},
		'player_2': {
			'position': player_positions['player_2'],
			'score': 0
		},
		'status': {
			'roll_count': 0,
			'current_turn': options['starting_player'],
			'next_roll': options['starting_roll']
		},
		'settings': {
			'board_size': options['board_size'],
			'rolls_per_turn': options['rolls_per_turn'],
			'target_score': options['target_score'],
			'die_sides': options['die_sides']
		}
	}

	# keep playing until somebody wins
	while game_state['player_1']['score'] < game_state['settings']['target_score'] and game_state['player_2']['score'] < game_state['settings']['target_score']:
		game_state = simulate_turn(game_state)

	return game_state



def simulate_turn(game_state):
	"""roll the dice and update the game state"""

	# roll the dice the right number of times"""
	rolls_this_turn = 0
	running_total = 0
	while rolls_this_turn < game_state['settings']['rolls_per_turn']:

		# count the die roll
		rolls_this_turn += 1
		game_state['status']['roll_count'] += 1
		
		# get the die roll and update the die
		running_total += game_state['status']['next_roll']
		game_state['status']['next_roll'] += 1
		if game_state['status']['next_roll'] > game_state['settings']['die_sides']:
			game_state['status']['next_roll'] = 1
		
	# update the player's score and position
	game_state[game_state['status']['current_turn']]['position'] = (game_state[game_state['status']['current_turn']]['position'] + running_total) % game_state['settings']['board_size']
	if game_state[game_state['status']['current_turn']]['position'] == 0:
		game_state[game_state['status']['current_turn']]['position'] = game_state['settings']['board_size']
	game_state[game_state['status']['current_turn']]['score'] += game_state[game_state['status']['current_turn']]['position']		

	# switch the turn
	if game_state['status']['current_turn'] == 'player_1':
		game_state['status']['current_turn'] = 'player_2'
	else:
		game_state['status']['current_turn'] = 'player_1'

	return game_state



def get_arbitrary_data_point(game_state):
	"""given a game_state, multiply the losing score by the number of rolls"""

	# figure out the losing score
	if game_state['player_1']['score'] >= game_state['settings']['target_score']:
		losing_score = game_state['player_2']['score']
	else:
		losing_score = game_state['player_1']['score']

	# multiply by the number of rolls
	return losing_score * game_state['status']['roll_count']



# print(get_arbitrary_data_point(simulate_deterministic_game(data, {
# 	'starting_player': 'player_1',
# 	'board_size': 10,
# 	'rolls_per_turn': 3,
# 	'starting_roll': 1,
# 	'target_score': 1000,
# 	'die_sides': 100
# })))



# part 2

def preload_possible_rolls(options):
	"""get the x^3 possible roll combos"""

	# get all 3^die_sides possibilities
	possible_rolls = []
	first_roll = 1
	while first_roll <= options['die_sides']:
		second_roll = 1
		while second_roll <= options['die_sides']:
			third_roll = 1
			while third_roll <= options['die_sides']:
				possible_rolls.append(first_roll + second_roll + third_roll)
				third_roll += 1
			second_roll += 1
		first_roll += 1

	return possible_rolls



def preload_possible_states(options):
	"""given a set of options, figure out how many possible states there are"""

	# victory states
	possible_states = {
		'v:1': 0,
		'v:2': 0
	}

	# all possible combinations of score, position, and turn
	score_p1 = 0
	while score_p1 < options['target_score']:
		position_p1 = 1
		while position_p1 <= options['board_size']:
			score_p2 = 0
			while score_p2 < options['target_score']:
				position_p2 = 1
				while position_p2 <= options['board_size']:
					possible_states['t:1,s1:' + str(score_p1) + ',p1:' + str(position_p1) + ',s2:' + str(score_p2) + ',p2:' + str(position_p2)] = 0
					possible_states['t:2,s1:' + str(score_p1) + ',p1:' + str(position_p1) + ',s2:' + str(score_p2) + ',p2:' + str(position_p2)] = 0
					position_p2 += 1
				score_p2 += 1
			position_p1 += 1
		score_p1 += 1

	return possible_states



def preload_effects(possible_states, possible_rolls, options):
	"""determine the 27 things that would happen as a result of a given situation"""

	effects = {}

	# loop through all possible states
	for possible_state in possible_states:
		# ignore victory states
		if possible_state[0] == 'v':
			continue

		# get the factors for this combo
		factors = possible_state.split(',')
		turn = factors[0].split(':')[1]
		score_p1 = int(factors[1].split(':')[1])
		position_p1 = int(factors[2].split(':')[1])
		score_p2 = int(factors[3].split(':')[1])
		position_p2 = int(factors[4].split(':')[1])

		# remove 1 from this state
		effects[possible_state] = {
			possible_state: -1
		}

		# who goes next
		next_turn = '1' if turn == '2' else '2'

		# loop through all possible rolls
		for possible_roll in possible_rolls:
			# get p1's updated position and score
			if turn == '1':
				new_position_p1 = (position_p1 + possible_roll) % options['board_size']
				if new_position_p1 == 0:
					new_position_p1 = options['board_size']
				new_score_p1 = min(score_p1 + new_position_p1, options['target_score'])
				new_position_p2 = position_p2
				new_score_p2 = score_p2
			
			# get p2's updated position and score
			if turn == '2':
				new_position_p2 = (position_p2 + possible_roll) % options['board_size']
				if new_position_p2 == 0:
					new_position_p2 = options['board_size']
				new_score_p2 = min(score_p2 + new_position_p2, options['target_score'])
				new_position_p1 = position_p1
				new_score_p1 = score_p1

			# get new state string
			if new_score_p1 == options['target_score']:
				new_state = 'v:1'
			elif new_score_p2 == options['target_score']:
				new_state = 'v:2'
			else:
				new_state = 't:' + next_turn + ',s1:' + str(new_score_p1) + ',p1:' + str(new_position_p1) + ',s2:' + str(new_score_p2) + ',p2:' + str(new_position_p2)

			# add to list of effects of this possible state
			if new_state in effects[possible_state]:
				effects[possible_state][new_state] += 1
			else:
				effects[possible_state][new_state] = 1

	return effects



def simulate_quantum_game(data, options):
	"""track the number of games in each state until they are all victory states"""

	# get the full scope of how things could play out
	possible_rolls = preload_possible_rolls(options)
	possible_states = preload_possible_states(options)
	effects = preload_effects(possible_states.keys(), possible_rolls, options)

	# initialize
	turn = options['starting_player']
	score_p1 = 0
	position_p1 = data['player_1']
	score_p2 = 0
	position_p2 = data['player_2']
	possible_states['t:' + turn + ',s1:' + str(score_p1) + ',p1:' + str(position_p1) + ',s2:' + str(score_p2) + ',p2:' + str(position_p2)] = 1

	# iterate until there are no more non-victory states
	finished = False
	while not finished:
		possible_states = iterate_step(possible_states, effects)
		finished = determine_if_finished(possible_states)

	return {'p1': possible_states['v:1'], 'p2': possible_states['v:2']}



def iterate_step(possible_states, effects):
	"""simulate one round by updating state counts"""

	# make a copy of the possible states with current counts
	new_states = {key: value for key, value in possible_states.items()}

	# loop through the current states
	for possible_state in possible_states:
		# skip victory
		if possible_state[0] == 'v':
			continue

		# loop through the effects that result from each of these states
		for affected_state in effects[possible_state]:
			# update the counts of the affected states
			new_states[affected_state] += (effects[possible_state][affected_state] * possible_states[possible_state])

	return new_states



def determine_if_finished(possible_states):
	"""given dictionary of all possible states, count how many are not victory"""

	# loop through to find possible non-victory states that still happen
	count_of_states = 0
	finished = True
	for key, value in possible_states.items():
		if key != 'v:1' and key != 'v:2' and value > 0:
			finished = False
		count_of_states += value

	return finished



# print(simulate_quantum_game(data, {
# 	'starting_player': '1',
# 	'board_size': 10,
# 	'target_score': 21,
# 	'die_sides': 3
# }))
