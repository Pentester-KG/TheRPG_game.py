from enum import Enum
from random import randint, choice


class SuperAbility(Enum):
    HEAL = 1
    CRITICAL_DAMAGE = 2
    BOOST = 3
    BLOCK_DAMAGE_REVERT = 4
    ONE_FOR_ALL = 5
    Self_sacrifice = 6
    Drake = 7
    Pioneer_Rage = 8
    Dicey_Shot = 9


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__damage = damage
        self.__health = health

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return (f'{self.__name} health: {self.__health} '
                f'damage: {self.__damage}')


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None

    @property
    def defence(self):
        return self.__defence

    def choose_defence(self, heroes):
        self.__defence = choice([e.value for e in SuperAbility])
        hero = choice(heroes)
        self.__defence = hero.ability

    def attack(self, heroes):
        for hero in heroes:
            if hero.health > 0:
                if (hero.ability == SuperAbility.BLOCK_DAMAGE_REVERT and
                        self.defence != SuperAbility.BLOCK_DAMAGE_REVERT):
                    coef = randint(1, 2)
                    hero.blocked_damage = int(self.damage / (coef * 5))
                    hero.health -= (self.damage - hero.blocked_damage)
                else:
                    hero.health -= self.damage

    def __str__(self):
        return (f'BOSS ' + super().__str__()
                + f' defence: {self.__defence}')


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss):
        boss.health -= self.damage

    def apply_super_power(self, boss, heroes):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage,
                         SuperAbility.CRITICAL_DAMAGE)

    def apply_super_power(self, boss, heroes):
        coef = randint(2,5)
        boss.health -= self.damage * coef
        print(f'Warrior {self.name} '
              f'hit critically {self.damage * coef}')


class Magic(Hero):
    def __init__(self, name, health, damage, boost_amount):
        super().__init__(name, health, damage, SuperAbility.BOOST)
        self.boost_amount = boost_amount

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            hero.damage += self.boost_amount


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage,
                         SuperAbility.BLOCK_DAMAGE_REVERT)
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss, heroes):
        boss.health -= self.__blocked_damage
        print(f'Berserk {self.name} reverted {self.blocked_damage}')


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage,
                         SuperAbility.HEAL)
        self.__heal_points = heal_points

    @property
    def heal_points(self):
        return self.__heal_points

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.health += self.__heal_points


round_number = 0
class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.Self_sacrifice)

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health == 0 and hero.ability != SuperAbility.Self_sacrifice:
                hero.health += self.health
                self.health = 0
                print(f'🦠{self.name} revived {hero.name}')


class Ludoman(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.Dicey_Shot)

    def apply_super_power(self, boss, heroes):
        coef = randint(1, 9)
        coef2 = randint(1, 9)
        if coef == coef2:
            boss.health -= (coef * coef2) * 2
            print(f'{self.name} have spin on {coef * coef2} damage')
        else:
            randhero = choice(heroes)
            randhero.health -= coef + coef2
            print(f'{self.name} damaged teammate {randhero.name} on {coef + coef2}')


class Hacker(Hero):
    def __init__(self, name, heath, damage):
        super().__init__(name, heath, damage, SuperAbility.Drake)
        self.boss_health = None

    def steal_health(self, n):
        if self.boss_health >= n:
            chosen_hero = random.choices(self.heroes)
            self.boss_health -= n
            chosen_hero["health"] += n


class Spitfire(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.Pioneer_Rage)
        self.attack_power = 10
        self.aggression = 0
        self.heroes_list = []

    def attack(self, boss):
        for hero in self.heroes_list:
            if hero.health <= 0:
                continue  # Skip deceased heroes
            self.aggression += 0.8
        boss.damage += self.aggression  # Change boss.attack to boss.damage

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0


class Deku(Hero):

    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.ONE_FOR_ALL)

    def apply_super_power(self, boss, heroes):
        coef = randint(1, 2)
        if coef == 1:
            pass
        elif coef == 2:
            coef2 = randint(1, 3)
            if coef2 == 1:
                self.damage += int(round(self.damage * 0.2, 0))
                self.health -= int(round(self.health * 0.2, 0))
                print(f'🧨{self.name} power increased by {20}%\n☸️{self.name} hp - 20% ')

            if coef2 == 2:
                self.damage += int(round(self.damage * 0.5, 0))
                self.health -= int(round(self.health * 0.5, 0))
                print(f'🧨{self.name} power increased by {100}%\n☸️{self.name} hp - 50% ')

            if coef2 == 3:
                self.damage += int(round(self.damage * 1, 0))
                self.health -= int(round(self.health * 0.9, 0))
                print(f'🧨{self.name} power increased by {100}%\n☸️{self.name} hp - 90% ')


def start_game():
    boss = Boss('Tanos', 1000, 50)

    warrior_1 = Warrior('Ahiles', 280, 5)
    warrior_2 = Warrior('Sponge Bob', 270, 10)
    magic = Magic('Hendolf', 180, 20, boost_amount=5)
    berserk = Berserk('Gatz', 220, 20)
    doc = Medic('Haus', 250, 5, 15)
    junior = Medic('Zolo', 290, 5, 5)
    witcher = Witcher('Gran', 100, 0)
    magic1 = Magic('Ainz', 100, 10, boost_amount=5)
    hacker = Hacker('NOname052', 270, 0)
    spitfire = Spitfire('Kaze', 100, 15)
    ludoman = Ludoman('Joker', 100, 0)
    deku = Deku('Izuku', 100, 20)

    heroes_list = [warrior_1, warrior_2, magic1, berserk, doc, junior, magic, witcher, hacker, spitfire, ludoman, deku]
    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


def is_game_over(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
    return all_heroes_dead


def show_statistics(boss, heroes):
    print(f'ROUND: {round_number} ----------')
    print(boss)
    for hero in heroes:
        print(hero)


def play_round(boss, heroes):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if (hero.health > 0 and boss.health > 0 and
                hero.ability != boss.defence):
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


start_game()
