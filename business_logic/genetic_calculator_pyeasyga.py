from pyeasyga import pyeasyga
from business_logic.data_processor import DataProcessor


# A class for doing genetic calculations using pyeasyga library
class GeneticCalculatorPyEasyGa:

    data: DataProcessor
    max_weight: int
    max_volume: float

    def __init__(self, data: DataProcessor):
        self.data = data




    def find_solution(self):

        genetic_algorithm = pyeasyga.GeneticAlgorithm(self.data.items) # initializing genetic algorithm
        genetic_algorithm.population_size = 200 # setting population size to 200 (default value is 50)

        max_weight = self.data.max_weight
        max_volume = self.data.max_volume

        # define a fitness function
        def fitness(individual, items):
            weight, volume, value = 0, 0, 0
            for (selected, item) in zip(individual, items):
                if selected:
                    weight += item[0]
                    volume += item[1]
                    value += item[2]
            if weight > max_weight or volume > max_volume:
                value = 0
            return value


        genetic_algorithm.fitness_function = fitness
        genetic_algorithm.run()
        result = genetic_algorithm.best_individual()
        processed_result = self.process_result(result)
        return processed_result


    def process_result(self, result):
        summary_value = result[0]
        summary_weight = 0
        summary_volume = 0
        num = 0
        used_items_nums = []
        for item in result[1]:
            if item != 0:
                summary_weight += self.data.items[num][0]
                summary_volume += self.data.items[num][1]
                used_items_nums.append(num+1)
            num += 1

        inner_result = {}
        inner_result['value']=summary_value
        inner_result['weight']=summary_weight
        inner_result['volume']=round(summary_volume, 2)
        inner_result['items']=used_items_nums

        outer_result = {}
        outer_result['1'] = inner_result
        return outer_result

