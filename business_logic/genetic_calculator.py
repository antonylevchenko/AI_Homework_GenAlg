import random

from business_logic.data_processor import DataProcessor


# Own class for doing genetic calculations using given algorithm.
class GeneticCalculator:
    __basic_population_amount: int
    __maximum_iteration_amount: int
    __minimum_iteration_amount: int
    __data: DataProcessor
    __population: []
    __breed: []
    __specimens_for_breeding: []
    __iteration_counter: int
    __best_option: {}


    def __init__(self, data: DataProcessor,
                 basic_population_amount: int,
                 maximum_iteration_amount: int,
                 minimum_iteration_amount: int):
        self.data = data
        self.__basic_population_amount = basic_population_amount
        self.__maximum_iteration_amount = maximum_iteration_amount
        self.__minimum_iteration_amount = minimum_iteration_amount
        self.__population = []
        self.__specimens_for_breeding = []
        self.__breed = []
        self.__iteration_counter = 0
        self.__best_option = {}

    # Create random specimen by adding or not adding every item in the bag.
    # Resulting list represents which items have been added (1) or not (0).
    # result[i] == 1 means, that item № i has been added.
    def __create_random_specimen(self):
        items = []
        items_amount = self.data.items.__len__()
        for i in range(0, items_amount):
            value = random.getrandbits(1)
            items.append(value)
        specimen = self.__get_specimen_from_items(items)
        return specimen

    # Getting weight, volume and value for the specimen.
    def __get_specimen_from_items(self, items):
        weight = 0
        volume = 0
        value = 0
        i = 0
        for is_item_selected in items:
            if is_item_selected:
                weight += self.data.items[i][0]
                volume += self.data.items[i][1]
                value += self.data.items[i][2]
            i += 1
        new_specimen = {}
        new_specimen['weight'] = weight
        new_specimen['volume'] = round(volume, 2)
        if weight > self.data.max_weight or volume > self.data.max_volume:
            new_specimen['value'] = -1
        else:
            new_specimen['value'] = value
        new_specimen['items'] = items
        return new_specimen

    # Creating basic population
    def __create_basic_population(self):
        for i in range(0, self.__basic_population_amount):
            self.__population.append(self.__create_random_specimen())

    # Selection of top 20 % for breeding.
    # If specimens have equal value (most probably -1, which means, they are out of allowed borders
    # there is sorting by weight and volume, in which items with lesser weight/volume are considered better.
    # To make it work there is sorting by three keys and multiplication by -1.
    def __select_specimens_for_breeding(self):
        self.__order_population()
        amount = int(self.__population.__len__() * 0.2)
        result = []
        for i in range(0, amount):
            result.append(self.__population[i])
        self.__specimens_for_breeding = result

    def __order_population(self):
        self.__population = sorted(self.__population,
                                   key=lambda k: (k['value'], k['weight'] * (-1), k['volume'] * (-1)),
                                   reverse=True)

    # Creating a new breed and put it into self.__breed
    def __get_whole_breed(self):
        while self.__specimens_for_breeding.__len__() > 1:
            first_breeder = self.__specimens_for_breeding[0]
            self.__specimens_for_breeding.remove(first_breeder)
            index = random.randint(0, self.__specimens_for_breeding.__len__() - 1)
            second_breeder = self.__specimens_for_breeding[index]
            self.__specimens_for_breeding.remove(second_breeder)
            self.__get_children(first_breeder, second_breeder)

    # Creating two children fro a couple
    def __get_children(self, first_breeder, second_breeder):
        self.__get_child(first_breeder, second_breeder)
        self.__get_child(second_breeder, first_breeder)

    # Creating a child and adding it to the self.__breed
    def __get_child(self, first_breeder, second_breeder):
        positions = self.__get_random_positions(3)
        child_items = []
        i = 0
        while i < positions.__len__() - 1:
            current_breeder = []
            if (i % 2 != 0 ):
                current_breeder = first_breeder
            else:
                current_breeder = second_breeder
            area = current_breeder['items'][positions[i]:positions[i+1]]
            for item in area:
                child_items.append(item)
            i += 1
        child = self.__get_specimen_from_items(child_items)
        self.__breed.append(child)


    # Generating random positions.
    def __get_random_positions(self, amount: int):
        result = []
        result.append(0)
        for i in range(1, amount + 1):
            result.append(random.randint(result[i-1], self.data.items.__len__()- amount + i - 1))
        result.append(self.data.items.__len__() - 1)
        return result

    # Mutating random 10% of the current population.
    def __mutate(self):
        amount = int(self.__population.__len__() * 0.1)
        for i in range(0, amount):
            mutation_index = random.randint(0, self.__population.__len__() - 1)
            self.__mutate_specimen(mutation_index)

    # Mutating specimen by adding one of the items which it does not have
    def __mutate_specimen(self, specimen_index: int):
        potential_item_indexes_for_mutation = []
        i = 0
        for item in self.__population[specimen_index]['items']:
            if item == 0:
                potential_item_indexes_for_mutation.append(i)
            i += 1
        index_of_item_index = random.randint(0, potential_item_indexes_for_mutation.__len__() - 1)
        item_index_for_mutation = potential_item_indexes_for_mutation[index_of_item_index]
        self.__population[specimen_index]['items'][item_index_for_mutation] = 1
        self.__population[specimen_index] = self.__get_specimen_from_items(self.__population[specimen_index]['items'])

    # Creating new population by sorting it and replacing worst 30 % with current breed
    def __create_new_population(self):
        self.__order_population()
        i = 0
        exctinction_amount = int(self.__population.__len__() * 0.3)
        for replacement_index in range(self.__population.__len__() - exctinction_amount - 1,
                                       self.__population.__len__() - 1):
            if i <= self.__breed.__len__() - 1:
                self.__population[replacement_index] = self.__breed[i]
            i += 1
        self.__breed = []

    # Finishing calculations on one of the conditions:
    # 1. If there is less than 10% difference between two last best options and there were more
    # than __minimum_iteration_amount iterations.
    # 2. If there were more than __maximum_iteration_amount iterations
    def __check_if_has_to_stop(self):
        if self.__iteration_counter == self.__maximum_iteration_amount:
            return True
        elif self.__iteration_counter >= self.__minimum_iteration_amount:
            new_best_option = self.__find_best()
            if (self.__best_option == {}):
                self.__best_option = new_best_option
            else:
                if new_best_option['value'] * 1.1 >= self.__best_option['value']:
                    return True
        self.__iteration_counter += 1
        return False

    def __find_best(self):
        self.__order_population()
        return self.__population[0]

    def find_solution(self):
        self.__create_basic_population()
        while not self.__check_if_has_to_stop():
            self.__select_specimens_for_breeding()
            self.__get_whole_breed()
            self.__mutate()
            self.__create_new_population()
        result = self.process_result(self.__best_option)
        return result

        # A method processing result from to the required format.
    def process_result(self, result):
            summary_value = result['value']
            summary_weight = 0
            summary_volume = 0
            num = 0
            used_items_nums = []
            for item in result['items']:
                if item != 0:
                    summary_weight += self.data.items[num][0]
                    summary_volume += self.data.items[num][1]
                    used_items_nums.append(num + 1)
                num += 1

            inner_result = {}
            inner_result['value'] = summary_value
            inner_result['weight'] = summary_weight
            inner_result['volume'] = round(summary_volume, 2)
            inner_result['items'] = used_items_nums

            outer_result = {}
            outer_result['1'] = inner_result
            return outer_result



