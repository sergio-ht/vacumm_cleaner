import random
from abc import ABC, abstractmethod
from statistics import mean


class Environment:
    def __init__(self, rooms=2) -> None:
        self.rooms = [random.randint(0, 1) for _ in range(rooms)]


class Vacuum(ABC):
    def __init__(self, environment: Environment) -> None:
        self.environment = environment
        self.position = random.randint(0, 1)

    def move_left(self):
        if self.position == 1:
            self.position -= 1

    def move_right(self):
        if self.position == 0:
            self.position += 1

    def clean_room(self):
        self.environment.rooms[self.position] = 0

    def is_dirty(self):
        return self.environment.rooms[self.position]

    @abstractmethod
    def clean_all(self):
        pass


class RandomVacuum(Vacuum):
    def clean_all(self):
        cost = 0
        while 1 in self.environment.rooms:
            action = random.choice([self.move_left, self.move_right, self.clean_room])
            action()
            cost += 1

        return cost


class IntelligentPartialVacuum(Vacuum):
    def move(self):
        if self.position == 0:
            self.move_right()
        else:
            self.move_left()

    def clean_all(self):
        cost = 0
        # check current room
        if self.is_dirty():
            self.clean_room()
            cost += 1
        # change room
        self.move()
        cost += 1
        # check other room
        if self.is_dirty():
            self.clean_room()
            cost += 1
        return cost


class IntelligentToalVacuum(Vacuum):
    def move(self):
        if self.position == 0:
            self.move_right()
        else:
            self.move_left()

    def clean_all(self):
        cost = 0
        while 1 in self.environment.rooms:
            if self.is_dirty():
                self.clean_room()
            else:
                self.move()
            cost += 1
        return cost


def main():
    # select number of tests
    tests = 10000
    # perform tests for each model
    r_costs = [RandomVacuum(Environment()).clean_all() for _ in range(tests)]
    ip_costs = [
        IntelligentPartialVacuum(Environment()).clean_all() for _ in range(tests)
    ]
    it_costs = [IntelligentToalVacuum(Environment()).clean_all() for _ in range(tests)]
    # print average
    print("Aleatoria: ", mean(r_costs))
    print("Parcial: ", mean(ip_costs))
    print("Total: ", mean(it_costs))


main()
