import os, random, time, msvcrt, yaml

stream = open('config.yaml', 'r')
data = yaml.safe_load(stream)
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
	team_colors = [Style.BRIGHT + Fore.YELLOW, Style.BRIGHT + Fore.GREEN]

os.system('title Битва покемонов')
pokemon_names = ['Пикачу', 'Иви', 'Сильвеон', 'Бульбазавр', 'Амбреон', 'Райчу', 'Пичу', 'Чаризард', 'Мьюту', 'Эспеон', 'Сквиртл', 'Деденне', 'Шеймин', 'Лифеон', 'Хупа', 'Ивельтал', 'Чармандер', 'Грениндзя', 'Зубат', 'Парас']
teams = []
team_size = data['team-size']
team_num = data['team-num']
max_team_size = pokemon_names.__len__() // 2

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
	for team_id in range(0, team_num):
		for fighter in teams[team_id].fighters:
			string = string.replace(fighter.name, team_colors[team_id] + fighter.name + Style.RESET_ALL)
	for word in string.split():
		word = word.replace(",", "")
		if is_number(word) or is_number(word.replace("%", "")):
			string = string.replace(word, Style.BRIGHT + word + Style.RESET_ALL)
		elif is_number(word.replace("!", "")):
			string = string.replace(word, Style.BRIGHT + Fore.RED + word + Style.RESET_ALL)
	print(string)

class Pokemon():
	def __init__(self, name):
		self.name = name
		self.HP = random.randint(data['pokemon']['hp']['min'], data['pokemon']['hp']['max'])
		self.power = random.randint(data['pokemon']['power']['min'], data['pokemon']['power']['max'])
		self.critical_chance = random.uniform(data['pokemon']['critical-chance']['min'], data['pokemon']['critical-chance']['max'])
		self.critical_multiplier = random.uniform(data['pokemon']['critical-multiplier']['min'], data['pokemon']['critical-multiplier']['max'])
		self.accuracy = random.uniform(data['pokemon']['accuracy']['min'], data['pokemon']['accuracy']['max'])
		self.damage_deviation = data['pokemon']['damage-deviation']
		self.is_able_to_fight = True

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
		return self.HP > 0

class Team():
	def __init__(self, size, fighters):
		self.size = size
		self.fighters = fighters

	def is_alive(self):
		res = False
		for fighter in self.fighters:
			res += fighter.is_able_to_fight
		return res

	def attack(self, target, double_hit_chance):
		for fighter in self.fighters:
			if fighter.is_able_to_fight:
				x = 0
				for i in range(target.size - 1, -1, -1):
					if target.fighters[i].is_alive():
						x = i
				fighter.attack(target.fighters[x])
				if (random.uniform(0, 1) <= double_hit_chance):
					print(f'{fighter.name} бьёт дважды за раунд.')
					x = 0
					for i in range(target.size - 1, -1, -1):
						if target.fighters[i].is_alive():
							x = i
					fighter.attack(target.fighters[x])

	def check_fighters(self):
		for fighter in self.fighters:
			f = fighter.is_able_to_fight
			fighter.is_able_to_fight = fighter.is_alive()
			if f != fighter.is_able_to_fight:
				print(random.choice([
					f'{fighter.name} больше не может сражаться.',
					f'{fighter.name} теряет волю к сражению.',
					f'{fighter.name} покидает арену.']))

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
		print(f'Условия боя: HP участников изменены в {self.HP_multiplier} раз(а), а сила атаки - в {self.power_multiplier} раз(а).\nУчастники могут ударить дважды за раунд с вероятностью {round(self.double_hit_chance * 100)}%.')
		for i in range(0, team_num):
			if self.teams[0].size == 1:
				header('Поприветствуем участников', '=')
			else:
				header(['Первая', 'Вторая', 'Третяя', 'Четвёртая', 'Пятая', 'Шестая', 'Седьмая', 'Восьмая', 'Девятая', 'Десятая'][i] +' команда', '=')
			for fighter in self.teams[i].fighters:
				fighter.HP *= self.HP_multiplier
				fighter.power *= self.power_multiplier
				fighter.greeting()
				fighter.info()

	def battle(self):
		header('Бой', '=')
		round_num = 1
		teams_alive = self.teams_alive()
		while len(teams_alive) > 1:
			header(f'{round_num} раунд', '-')
			round_num += 1
			#teams_
			#for j in (0, len(teams_alive)):
				#i = teams_alive
			self.teams[0].attack(self.teams[1], self.double_hit_chance)
			self.teams[1].attack(self.teams[0], self.double_hit_chance)
			self.teams[0].check_fighters()
			self.teams[1].check_fighters()
			teams_alive = self.teams_alive()

	def results(self):
		header('Подведение результатов', '=')
		if self.winner == -1:
			print(f'Битва заканчивается ничьёй!')
		else:
			winner = self.teams[self.winner]
			if winner.size == 1:
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
			for i in range(0, winner.fighters.__len__()):
				string += winner.fighters[i].name
				if i == winner.size - 2:
					string += ' и '
				elif i <= winner.size - 2:
					string += ', '
			print_color(f'{string}!')

	def teams_alive(self):
		self.winner = -1
		teams_alive = []
		for i in range(0, team_num):
			if self.teams[i].is_alive():
				teams_alive.append(i)
				self.winner = i
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
	os.system('cls')
	global teams
	teams = []
	names = pokemon_names.copy()
	for team_id in range(0, team_num):
		pokemons = []
		for i in range(0, team_size):
			pokemons.append(Pokemon(random.choice(names)))
			names.remove(pokemons[i].name)
		teams.append(Team(team_size, pokemons))
	arena = Arena(teams)
	arena.greetings()
	arena.battle()
	arena.results()
	if PRINT_COLORED:
		button_begin = f'{Back.WHITE}{Fore.BLACK} '
		button_end = f' {Style.RESET_ALL}'
	else:
		button_begin = '#'
		button_end = '#'
	if PLAY_MUSIC:
		print(f'{button_begin}Enter{button_end} Новый бой {button_begin}S{button_end} Размер команды {button_begin}M{button_end} Музыка {button_begin}Esc{button_end} Выход')
	else:
		print(f'{button_begin}Enter{button_end} Новый бой {button_begin}S{button_end} Размер команды {button_begin}Esc{button_end} Выход')

if PLAY_MUSIC:
	music = Music('pokemon.mp3')
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
