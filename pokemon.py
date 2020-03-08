import os, random, time, msvcrt, yaml

stream = open('config.yaml', 'r', encoding="utf8")
data = yaml.full_load(stream)
PLAY_MUSIC = data['music']
PRINT_COLORED = data['colored']

if PLAY_MUSIC:
	import pygame
if PRINT_COLORED:
	import colorama
	colorama.init()
	Style = colorama.Style
	Fore  = colorama.Fore
	Back  = colorama.Back
	team_colors = [f'{Style.BRIGHT}{Fore.YELLOW}', f'{Style.BRIGHT}{Fore.GREEN}', f'{Style.BRIGHT}{Fore.MAGENTA}', f'{Style.BRIGHT}{Fore.CYAN}', f'{Fore.RED}', f'{Style.BRIGHT}{Fore.BLUE}', f'{Style.DIM}{Fore.CYAN}', f'{Style.DIM}{Fore.YELLOW}', f'{Style.DIM}{Fore.GREEN}', f'{Style.DIM}{Fore.MAGENTA}']

os.system('title Битва покемонов')
teams = []
team_size = data['team-size']
team_num = data['team-num']
names = data['names']
team_names = data['team-names']
max_team_size = names.__len__() // team_num

def print_color(string):
	if not PRINT_COLORED:
		print(string)
		return

	def is_number(string):
		try:
			float(string)
			return True
		except ValueError:
			return False

	for team in teams:
		string = string.replace(team.name, team_colors[team.id] + team.name + Style.RESET_ALL)
		for fighter in team.fighters:
			string = string.replace(fighter.name, team_colors[team.id] + fighter.name + Style.RESET_ALL)
	for word in string.split():
		word = word.replace(",", "")
		if is_number(word) or is_number(word.replace("%", "")):
			string = string.replace(word, Style.BRIGHT + word + Style.RESET_ALL)
		elif is_number(word.replace("!", "")):
			string = string.replace(word, Style.BRIGHT + Fore.RED + word + Style.RESET_ALL)
	print(string)

class Fighter():
	def __init__(self, name):
		self.name = name
		self.HP = random.randint(data['fighter']['hp']['min'], data['fighter']['hp']['max'])
		self.power = random.randint(data['fighter']['power']['min'], data['fighter']['power']['max'])
		self.critical_chance = random.uniform(data['fighter']['critical-chance']['min'], data['fighter']['critical-chance']['max'])
		self.critical_multiplier = random.uniform(data['fighter']['critical-multiplier']['min'], data['fighter']['critical-multiplier']['max'])
		self.accuracy = random.uniform(data['fighter']['accuracy']['min'], data['fighter']['accuracy']['max'])
		self.damage_deviation = data['fighter']['damage-deviation']
		self.alive = True
		self.ready = True

	def greeting(self):
		print_color(random.choice([
			f'Привет, я {self.name}!',
			f'{self.name} появляется!',
			f'Встречайте... {self.name}!']))

	def info(self):
		print_color(
			f'{self.HP} HP, ' +
			f'{self.power} ATK, ' +
			f'{round(self.critical_chance * 100)}% ШАНС КРИТА, ' +
			f'{round(self.critical_multiplier * 100)}% КРИТ УРОН, ' +
			f'{round(self.accuracy * 100)}% ТОЧНОСТЬ')

	def attack(self, target):
		if random.uniform(0, 1) > self.accuracy:
			print_color(f'{self.name} бьёт {target.name}, но промахивается.')
		else:
			damage = round(self.power * random.uniform(1 - self.damage_deviation, 1 + self.damage_deviation))
			damage_info = f'{damage}'
			if random.uniform(0, 1) <= self.critical_chance:
				damage = round(damage * self.critical_multiplier)
				damage_info = f'{damage}!'
			target.HP = target.HP - damage
			if target.HP < 0:
				target.HP = 0
			print_color(f'{self.name} бьёт {target.name} на {damage_info}, и здоровье {target.name} становится {target.HP}.')

	def is_alive(self):
		if self.alive and self.HP == 0:
			self.alive = False
			print_color(random.choice([
				f'{self.name} больше не может сражаться.',
				f'{self.name} теряет волю к сражению.',
				f'{self.name} покидает арену.']))
		return self.alive

class Team():
	def __init__(self, name, id, fighters):
		self.name = name
		self.id = id
		self.fighters = fighters
		self.alive = True

	def attack(self, target, double_hit_chance):
		for fighter in self.fighters:
			if fighter.alive and fighter.ready:
				x = 0
				for i in range(team_size - 1, -1, -1):
					if target.fighters[i].HP > 0:
						x = i
				fighter.attack(target.fighters[x])
				if (random.uniform(0, 1) <= double_hit_chance):
					print_color(f'{fighter.name} бьёт дважды за раунд.')
					x = 0
					for i in range(team_size - 1, -1, -1):
						if target.fighters[i].HP > 0:
							x = i
					fighter.attack(target.fighters[x])
				fighter.ready = False

	def is_alive(self):
		if self.alive:
			self.alive = False
			for fighter in self.fighters:
				self.alive += fighter.is_alive()
			if not self.alive and team_size > 1:
				print_color(f'{self.name} терпит поражение')
		return self.alive

	def team_points(self):
		points = 0
		for fighter in self.fighters:
			if fighter.HP > 0:
				points += fighter.HP
				points += fighter.power * 3
		return points

def header(string, ch):
	a = 60 - string.__len__() - 2
	if PRINT_COLORED:
		print(Style.BRIGHT + ch * (a // 2) + ' ' + string + ' ' + ch * (a - a // 2) + Style.RESET_ALL)
	else:
		print(ch * (a // 2) + ' ' + string + ' ' + ch * (a - a // 2))

class Arena():
	def __init__(self, teams):
		self.HP_multiplier = random.randint(data['arena']['hp-multiplier']['min'], data['arena']['hp-multiplier']['max'])
		self.power_multiplier = random.randint(data['arena']['power-multiplier']['min'], data['arena']['power-multiplier']['max'])
		self.double_hit_chance = random.uniform(data['arena']['double-hit-chance']['min'], data['arena']['double-hit-chance']['max'])
		self.teams = teams

	def greetings(self):
		header('Добро пожаловать на Арену!', '=')
		print_color(f'Условия боя: HP участников изменены в {self.HP_multiplier} раз(а), а сила атаки - в {self.power_multiplier} раз(а).\nУчастники могут ударить дважды за раунд с вероятностью {round(self.double_hit_chance * 100)}%.\nПравила боя: Схватка продолжается, пока в строю не останется одна сторона.')
		if team_size == 1:
			header('Поприветствуем участников', '=')
		for team in self.teams:
			if team_size > 1:
				header(team.name, '=')
			for fighter in team.fighters:
				fighter.HP *= self.HP_multiplier
				fighter.power *= self.power_multiplier
				fighter.greeting()
				fighter.info()

	def battle(self):
		header('Бой', '=')
		round_num = 1
		while self.teams_alive() > 1:
			header(f'{round_num} раунд', '-')
			round_num += 1
			for team in self.teams:
				if team.alive:
					for fighter in team.fighters:
						fighter.ready = True
					t = 0
					for team2 in self.teams:
						if team.id != team2.id:
							team_points = team2.team_points()
							if team_points > t:
								t = team_points
								target = team2
					team.attack(target, self.double_hit_chance)

	def results(self):
		header('Подведение результатов', '=')
		if self.winner == -1:
			print(f'Битва заканчивается ничьёй!')
		else:
			winner = self.teams[self.winner]
			if team_size == 1:
				string = random.choice([
					'Побеждает ',
					'Одерживает верх ',
					'Забирает победу ',
					'Победитель: '])
			else:
				string = random.choice([
					'Побеждают ',
					'Одерживают верх ',
					'Забирают победу ',
					'Победители: '])
			for i in range(team_size):
				string += winner.fighters[i].name
				if i == team_size - 2:
					string += ' и '
				elif i <= team_size - 2:
					string += ', '
			print_color(string + '!')

	def teams_alive(self):
		self.winner = -1
		teams_alive = 0
		for team in self.teams:
			if team.is_alive():
				teams_alive = teams_alive + 1
				self.winner = team.id
		return teams_alive

class Music():
	if PLAY_MUSIC:
		pygame.mixer.init()
		def __init__(self, filename):
			pygame.mixer.music.load(filename)
			pygame.mixer.music.play(-1)
			self.music_is_playing = True

		def toggle_music(self):
			if self.music_is_playing:
				pygame.mixer.music.pause()
				self.music_is_playing = False
			else:
				pygame.mixer.music.unpause()
				self.music_is_playing = True

def random_fight(team_size):
	os.system(['clear','cls'][os.name == 'nt'])
	global teams
	teams = []
	available_names = names.copy()
	for team_id in range(team_num):
		fighters = []
		for i in range(team_size):
			fighters.append(Fighter(random.choice(available_names)))
			available_names.remove(fighters[i].name)
		teams.append(Team(team_names[team_id], team_id, fighters))
	arena = Arena(teams)
	arena.greetings()
	arena.battle()
	arena.results()
	b1 = f'{Back.WHITE}{Fore.BLACK} ' if PRINT_COLORED else '#'
	b2 = f' {Style.RESET_ALL}' if PRINT_COLORED else '#'
	print(f'{b1}Enter{b2} Новый бой {b1}S{b2} Размер команды ' + ['', f'{b1}M{b2} Музыка '][PLAY_MUSIC] + f'{b1}Esc{b2} Выход')

if PLAY_MUSIC:
	music = Music(data['music-name'])
random_fight(team_size)

while True:
	pressedKey = msvcrt.getch()
	if PLAY_MUSIC and ord(pressedKey) == ord('m'):
		music.toggle_music()
	elif ord(pressedKey) == ord('s'):
		f = False
		while not f:
			string = input(f'Введите желаемый размер команды [1-{max_team_size}]: ')
			try:
				f = int(string) in range(1, max_team_size + 1)
				if f:
					team_size = int(string)
			except ValueError:
				f = string == ''
		random_fight(team_size)
	elif ord(pressedKey) == 13:
		random_fight(team_size)
	elif ord(pressedKey) == 27:
		print('\n' + random.choice(['Увидимся!', 'До встречи на арене!', 'Возвращайся ещё!']))
		time.sleep(1)
		exit()
