# data

start = 'CHBBKPHCPHPOKNSNCOVB'
rules = ['SP -> K','BB -> H','BH -> S','BS -> H','PN -> P','OB -> S','ON -> C','HK -> K','BN -> V','OH -> F','OF -> C','SN -> N','PF -> H','CF -> F','HN -> S','SK -> F','SS -> C','HH -> C','SO -> B','FS -> P','CB -> V','NK -> F','KK -> P','VN -> H','KF -> K','PS -> B','HP -> B','NP -> P','OO -> B','FB -> V','PO -> B','CN -> O','HC -> B','NN -> V','FV -> F','BK -> K','VC -> K','KV -> V','VF -> V','FO -> O','FK -> B','HS -> C','OV -> F','PK -> F','VV -> S','NH -> K','SH -> H','VB -> H','NF -> P','OK -> B','FH -> F','CO -> V','BC -> K','PP -> S','OP -> V','VO -> C','NC -> F','PB -> F','KO -> O','BF -> C','VS -> K','KN -> P','BP -> F','KS -> V','SB -> H','CH -> N','HF -> O','CV -> P','NB -> V','FF -> H','OS -> S','CS -> S','KC -> F','NS -> N','NV -> O','SV -> V','BO -> V','BV -> V','CC -> F','CK -> H','KP -> C','KH -> H','KB -> F','PH -> P','VP -> P','OC -> F','FP -> N','HV -> P','HB -> H','PC -> N','VK -> H','HO -> V','CP -> F','SF -> N','FC -> P','NO -> K','VH -> S','FN -> F','PV -> O','SC -> N']



# part 1

def get_range_of_counts(polymer):
	"""given a polymer, what is the difference between frequency of most and least common elements"""

	letters = list(polymer)
	counts = {}
	for letter in letters:
		if letter in counts.keys():
			counts[letter] += 1
		else:
			counts[letter] = 1

	letter_keys = list(counts.keys())
	letter_keys.sort(key=lambda x: counts[x], reverse=True)

	return counts[letter_keys[0]] - counts[letter_keys[len(letter_keys) - 1]]



def get_polymer_after_steps(polymer, rules, count):
	"""apply rules to polymer for count steps"""

	rules = format_rules(rules)

	step = 0
	while step < count:
		polymer = update_polymer(polymer, rules)
		step += 1

	return polymer



def format_rules(rules):
	"""takes rule strings and creates object"""

	mapping = {}
	for rule in rules:
		condition = rule.split(' -> ')[0]
		insertion = rule.split(' -> ')[1]
		mapping[condition] = insertion

	return mapping



def update_polymer(polymer, rules):
	"""applies rules to polymer once"""

	output_polymer = ''
	input_polymer = list(polymer)

	index = 0
	while index < len(input_polymer) - 1:
		output_polymer += input_polymer[index]

		condition = input_polymer[index] + input_polymer[index + 1]
		if condition in rules.keys():
			output_polymer += rules[condition]

		index += 1

	output_polymer += input_polymer[len(input_polymer) - 1]

	return output_polymer



# print(get_range_of_counts(get_polymer_after_steps(start, rules, 15)))



# part 2

def count_letter_combinations(start, rules, count):
	"""tracks combinations of letters"""

	# shells
	combinations = format_combinations(start, rules)
	effects = format_effects(rules)

	# starting condition
	letters = list(start)
	index = 0
	while index < len(letters) - 1:
		combinations[letters[index] + letters[index + 1]] += 1
		combinations[letters[index]] += 1
		index += 1
	combinations[letters[len(letters) - 1]] += 1

	# iterate for # steps
	step = 0
	while step < count:
		combinations = update_combination_counts(combinations, effects)
		step += 1

	# output combinations + letters
	return combinations



def format_combinations(polymer, rules):
	"""figure out all possible combinations (and individuals) given a set of letters"""

	unique_letters = set(polymer + ''.join(rules).replace(' -> ', ''))
	combinations = {x + y: 0 for y in unique_letters for x in unique_letters}

	for letter in unique_letters:
		combinations[letter] = 0

	sorted_combinations = {key: value for key, value in sorted(combinations.items())}
	return sorted_combinations



def format_effects(rules):
	"""given ab -> c rules, sets effects of -ab +ac +cb"""

	effects = {}
	for rule in rules:
		condition = rule.split(' -> ')[0]
		insertion = rule.split(' -> ')[1]

		before = list(condition)[0]
		after = list(condition)[1]

		effects[condition] = { insertion: 1	}
		if before == insertion:
			# 'ab -> a' --> aab: ab, aa, ab : condition == insertion + after
			effects[condition][condition] = 0
			effects[condition][before + insertion] = 1
		elif after == insertion:
			# 'ab -> b' --> abb: ab, ab, bb : condition == before + insertion
			effects[condition][condition] = 0
			effects[condition][insertion + after] = 1
		else:
			# 'aa -> b' --> aba: aa, ab, ba : all distinct
			# 'ab -> c' --> acb: ab, ac, cb : all distinct
			effects[condition][condition] = -1
			effects[condition][before + insertion] = 1
			effects[condition][insertion + after] = 1

	return effects



def update_combination_counts(combinations, effects):
	"""applies effects to current combinations to adjust counts"""
	combinations_copy = combinations.copy()
	for combo in combinations:
		if combo in effects.keys():
			for effect in effects[combo]:
				combinations_copy[effect] += (effects[combo][effect] * combinations[combo])

	return combinations_copy



def get_range_of_final_counts(combinations):
	"""given the final state, get the difference between the most frequent and least frequent occurences"""

	lowest_count = 1000000000000000000000000000000 # arbitrarily large
	highest_count = 0

	counts = {key: value for key, value in sorted(combinations.items()) if len(key) == 1}

	for x in counts:
		if counts[x] > highest_count:
			highest_count = counts[x]
		if counts[x] < lowest_count:
			lowest_count = counts[x]

	return highest_count - lowest_count



# print(get_range_of_final_counts(count_letter_combinations(start, rules, 40)))
