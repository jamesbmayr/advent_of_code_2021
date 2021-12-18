# data

data = 'x=138..184, y=-125..-71'



# part 1

def get_all_valid_trajectories(data):
	"""what's the highest possible y for any arc that lands in the target area?"""

	x_range = data.split(', ')[0].split('=')[1].split('..')
	y_range = data.split(', ')[1].split('=')[1].split('..')
	target = {
		'x': [int(x_range[0]), int(x_range[1])],
		'y': [int(y_range[0]), int(y_range[1])]
	}

	trajectories = []
	vx = 1								# if vx is 0 or negative, it can't possibly get to the target area
	while vx <= target['x'][1]: 		# if vx is larger than the farthest edge of the target area, it's guaranteed to overshoot
		vy = target['y'][0]				# if vy is less than the bottom of the y range, it's guaranteed to undershoot
		while vy <= target['x'][1]: 	# if vy is positive, it arcs up; after vy steps, vy goes negative
										# after 2 * vy steps, y = 0 again; this is equivalent to a negative vy starting at x = 2 * vy;
										# even if x is 0 at that point, if 2 * vy is larger the farthest edge, it's guaranteed to overshoot
			coordinates, hits_target = get_trajectory(vx, vy, target)
			if hits_target:
				ranked_by_height = sorted(coordinates, key=lambda c: c[1])

				trajectories.append({
					'vx': vx,
					'vy': vy,
					'coordinates': coordinates,
					'highest_y': ranked_by_height[len(ranked_by_height) - 1]
				})
			vy += 1
		vx += 1

	trajectories.sort(key=lambda t: t['highest_y'])
	return trajectories



def get_trajectory(vx, vy, target):
	"""steps through the projectile motion until it's in or past the target area"""

	x = 0
	y = 0
	coordinates = [[x,y]]
	while x <= target['x'][1] and (vx > 0 or (target['x'][0] <= x and x <= target['x'][1] and y > target['y'][0])):
		x += vx
		y += vy
		coordinates.append([x,y])

		if target['x'][0] <= x and x <= target['x'][1] and target['y'][0] <= y and y <= target['y'][1]:
			return coordinates, True
		
		if vx > 0:
			vx -= 1
		elif vx < 0:
			vx += 1
		vy -= 1

	return coordinates, False



# all_trajectories = get_all_valid_trajectories(data)
# print(all_trajectories[len(all_trajectories) - 1])



# part 2

# print(len(get_all_valid_trajectories(data)))
