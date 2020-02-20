import os, random
class Pokemon:
	HP = 100
	power = 20
	mana = 50
	critical_chance = 0
	critical_multiplier = 150
	miss_chance = 0

	def __init__(self, name):
		self.name = name
		self.HP += random.randint(0, 20)
		self.power += random.randint(-5, 5)
		self.critical_chance += random.randint(0, 20)
		self.critical_multiplier += random.randint(0, 50)
		self.miss_chance += random.randint(0, 20)

	def greeting(self):
		print(f'Привет, я {self.name}!')

	def info(self):
		print(f'{self.HP} HP, {self.power} ATK, {self.critical_chance}% ШАНС КРИТА, {self.critical_multiplier}% КРИТ УРОН, {self.miss_chance}% ШАНС ПРОМАХА')

	def attack(self, target):
		is_miss = random.randint(0, 100) <= self.miss_chance
		if is_miss:
			print(f'{self.name} бьёт {target.name}, но промахивается.')
		else:
			is_critical = random.randint(0, 100) <= self.critical_chance
			if is_critical:
				damage = round(self.power * self.critical_multiplier / 100)
				print(f'{self.name} бьёт {target.name} на {damage} (крит урон!)', end = ", ")
			else:
				damage = self.power
				print(f'{self.name} бьёт {target.name} на {damage}', end = ", ")
			target.HP = target.HP - damage
			if target.HP < 0:
				target.HP = 0
			print(f'и здоровье {target.name} становится {target.HP}.')

	def is_alive(self):
		return self.HP > 0

class Arena:
	def __init__(self, fighter1, fighter2):
		self.HP_multiplier = random.randint(5,10)
		self.power_multiplier = random.randint(5,10)
		self.double_hit_chance = random.randint(0, 60)

		self.fighter1 = fighter1
		self.fighter2 = fighter2

	def greetings(self):
		print(f'Добро пожаловать на арену!\nУсловия боя: HP участников изменены в {self.HP_multiplier} раз(а), а сила атаки - в {self.power_multiplier} раз(а).\nУчастники могут ударить дважды за раунд с вероятностью {self.double_hit_chance}%.')
		self.fighter1.HP *= self.HP_multiplier
		self.fighter2.HP *= self.HP_multiplier
		self.fighter1.power *= self.power_multiplier
		self.fighter2.power *= self.power_multiplier
		print("=" * 30)
		self.fighter1.greeting()
		self.fighter1.info()
		self.fighter2.greeting()
		self.fighter2.info()

	def battle(self):
		print("=" * 30)
		round_num = 1
		while self.fighter1.is_alive() and self.fighter2.is_alive():
			print('-' * 9, f'{round_num} раунд', '-' * 9)
			print(f'{self.fighter1.name}: {self.fighter1.HP} HP | {self.fighter2.name}: {self.fighter2.HP} HP')
			round_num += 1
			self.fighter1.attack(self.fighter2)
			if (random.randint(0, 100) <= self.double_hit_chance):
				print(f'{self.fighter1.name} бьёт дважды за раунд.')
				self.fighter1.attack(self.fighter2)
			self.fighter2.attack(self.fighter1)
			if (random.randint(0, 100) <= self.double_hit_chance):
				print(f'{self.fighter2.name} бьёт дважды за раунд.')
				self.fighter2.attack(self.fighter1)
		print("=" * 30)

	def results(self):
		if self.fighter1.is_alive():
			print('Побеждает', self.fighter1.name, '!')
		elif self.fighter2.is_alive():
			print('Побеждает', self.fighter2.name, '!')
		else:
			print('Ничья!')

def random_fight():
	pokemon_names = ['Пикачу', 'Иви', 'Сильвеон', 'Бульбазавр', 'Амбреон', 'Райчу', 'Пичу', 'Чаризард', 'Мьюту', 'Эспеон', 'Сквиртл', 'Деденне', 'Шеймин', 'Лифеон', 'Хупа', 'Ивельтал', 'Чармандер', 'Грениндзя']
	pokemon1 = Pokemon(random.choice(pokemon_names))
	pokemon_names.remove(pokemon1.name)
	pokemon2 = Pokemon(random.choice(pokemon_names))
	arena = Arena(pokemon1, pokemon2)
	arena.greetings()
	arena.battle()
	arena.results()

while 1:
	os.system('cls')
	random_fight()
	input()
