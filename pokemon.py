import os, random, time, msvcrt, pygame, colorama
colorama.init()
Style = colorama.Style
Fore  = colorama.Fore
Back  = colorama.Back
os.system("title Битва покемонов")

class Pokemon:
	def __init__(self, name, color):
		self.name = name
		self.colored_name = color + self.name + Fore.WHITE + Style.NORMAL
		self.HP = random.randint(100, 120)
		self.power = random.randint(15, 25)
		self.critical_chance = random.uniform(0, 0.2)
		self.critical_multiplier = random.uniform(1.5, 2)
		self.accuracy = random.uniform(0.8, 1.0)
		self.damage_deviation = 0.15
		self.is_able_to_fight = True

	def greeting(self):
		print(random.choice([
			f'Привет, я {self.colored_name}!',
			f'{self.colored_name} появляется!',
			f'Встречайте... {self.colored_name}!']))

	def info(self):
		print(
			f'{Style.BRIGHT}{self.HP}{Style.NORMAL} HP, ' +
			f'{Style.BRIGHT}{self.power}{Style.NORMAL} ATK, ' +
			f'{Style.BRIGHT}{round(self.critical_chance * 100)}%{Style.NORMAL} ШАНС КРИТА, ' +
			f'{Style.BRIGHT}{round(self.critical_multiplier * 100)}%{Style.NORMAL} КРИТ УРОН, ' +
			f'{Style.BRIGHT}{round(self.accuracy * 100)}%{Style.NORMAL} ТОЧНОСТЬ')

	def attack(self, target):
		if random.uniform(0, 1) > self.accuracy:
			print(f'{self.colored_name} бьёт {target.colored_name}, но промахивается.')
		else:
			damage = round(self.power * random.uniform(1 - self.damage_deviation, 1 + self.damage_deviation))
			damage_info = f'{Style.BRIGHT}{damage}{Style.NORMAL}'
			if random.uniform(0, 1) <= self.critical_chance:
				damage = round(damage * self.critical_multiplier)
				damage_info = f'{Style.BRIGHT}{Fore.RED}{damage}!{Style.RESET_ALL}'
			target.HP = target.HP - damage
			if target.HP < 0:
				target.HP = 0
			print(f'{self.colored_name} бьёт {target.colored_name} на {damage_info}, и здоровье {target.colored_name} становится {Style.BRIGHT}{target.HP}{Style.NORMAL}.')

	def is_alive(self):
		return self.HP > 0

class Team:
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
					print(f'{fighter.colored_name} бьёт дважды за раунд.')
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
					f'{fighter.colored_name} больше не может сражаться.',
					f'{fighter.colored_name} теряет волю к сражению.',
					f'{fighter.colored_name} покидает арену.']))

def header(string, ch):
	a = 60 - string.__len__() - 2
	print(Style.BRIGHT + Fore.WHITE + ch * (a // 2) + ' ' + string + ' ' + ch * (a - a // 2) + Style.NORMAL)

class Arena:
	def __init__(self, team1, team2):
		self.HP_multiplier = random.randint(5, 10)
		self.power_multiplier = random.randint(8, 12)
		self.double_hit_chance = random.uniform(0, 0.6)
		self.team1 = team1
		self.team2 = team2

	def greetings(self):
		header('Добро пожаловать на Арену!', '=')
		print(f'{Style.BRIGHT}Условия боя:{Style.NORMAL} HP участников изменены в {Style.BRIGHT}{self.HP_multiplier}{Style.NORMAL} раз(а), а сила атаки - в {Style.BRIGHT}{self.power_multiplier}{Style.NORMAL} раз(а).\nУчастники могут ударить дважды за раунд с вероятностью {Style.BRIGHT}{round(self.double_hit_chance * 100)}%{Style.NORMAL}.')
		if self.team1.size == 1:
			header('Поприветствуем участников', '=')
		else:
			header('Первая команда', '=')
		for fighter in self.team1.fighters:
			fighter.HP *= self.HP_multiplier
			fighter.power *= self.power_multiplier
			fighter.greeting()
			fighter.info()
		if self.team1.size > 1:
			header('Вторая команда', '=')
		for fighter in self.team2.fighters:
			fighter.HP *= self.HP_multiplier
			fighter.power *= self.power_multiplier
			fighter.greeting()
			fighter.info()

	def battle(self):
		header('Бой', '=')
		round_num = 1
		while self.team1.is_alive() and self.team2.is_alive():
			header(f'{round_num} раунд', '-')
			round_num += 1
			self.team1.attack(self.team2, self.double_hit_chance)
			self.team2.attack(self.team1, self.double_hit_chance)
			self.team1.check_fighters()
			self.team2.check_fighters()

	def results(self):
		header('Подведение результатов', '=')
		if self.team1.is_alive() == False and self.team2.is_alive() == False:
			print(f'Битва заканчивается ничьёй!')
		else:
			string = ''
			if self.team1.is_alive():
				winner = self.team1
			elif self.team2.is_alive():
				winner = self.team2
			if winner.size == 1:
				string += random.choice([
					'Побеждает ',
					'Одерживает верх ',
					'Забирает победу ',
					'Победитель: '])
			else:
				string += random.choice([
					'Побеждают ',
					'Одерживают верх ',
					'Забирают победу ',
					'Победители: '])
			for i in range(0, winner.fighters.__len__()):
				string += winner.fighters[i].colored_name
				if i == winner.size - 2:
					string += ' и '
				elif i <= winner.size - 2:
					string += ', '
			print(f'{string}!')

class Music:
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

pokemon_names = ['Пикачу', 'Иви', 'Сильвеон', 'Бульбазавр', 'Амбреон', 'Райчу', 'Пичу', 'Чаризард', 'Мьюту', 'Эспеон', 'Сквиртл', 'Деденне', 'Шеймин', 'Лифеон', 'Хупа', 'Ивельтал', 'Чармандер', 'Грениндзя', 'Зубат', 'Парас']
team_size = 3
max_team_size = pokemon_names.__len__() // 2

def random_fight(team_size):
	os.system('cls')
	pokemons = []
	names = pokemon_names.copy()
	for i in range(0, team_size):
		pokemons.append(Pokemon(random.choice(names), Style.BRIGHT + Fore.YELLOW))
		names.remove(pokemons[i].name)
	team1 = Team(team_size, pokemons)
	pokemons = []
	for i in range(0, team_size):
		pokemons.append(Pokemon(random.choice(names), Style.BRIGHT + Fore.GREEN))
		names.remove(pokemons[i].name)
	team2 = Team(team_size, pokemons)
	arena = Arena(team1, team2)
	arena.greetings()
	arena.battle()
	arena.results()
	print(f'{Back.WHITE}{Fore.BLACK} Enter {Style.RESET_ALL} Новый бой {Back.WHITE}{Fore.BLACK} S {Style.RESET_ALL} Размер команды {Back.WHITE}{Fore.BLACK} M {Style.RESET_ALL} Музыка {Back.WHITE}{Fore.BLACK} Esc {Style.RESET_ALL} Выход')

music = Music('pokemon.mp3')
random_fight(team_size)

while True:
	pressedKey = msvcrt.getch()
	if ord(pressedKey) == ord('m'):
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
		print('\n' + Fore.CYAN + Style.BRIGHT + random.choice(['Увидимся!', 'До встречи на арене!', 'Возвращайся ещё!']) + Style.RESET_ALL)
		time.sleep(1)
		exit()
