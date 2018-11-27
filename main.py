from business_logic.data_processor import DataProcessor
from business_logic.genetic_calculator_pyeasyga import GeneticCalculatorPyEasyGa
from business_logic.result_writer import *


source_file_path = 'sources/6.txt'
result_file_path = 'result/task_1.json'


def main():
    print('Processing data from ' + source_file_path + '...')
    data = DataProcessor(source_file_path)
    print('Data has been processed. ')
    print()
    print('Maximum allowed weight is ' + str(data.max_weight))
    print('Maximum allowed volume is ' + str(data.max_volume))
    print_items(data)
    print()
    print('Working on the task 1...')
    print('Trying to find the best solution using pyeasyga library...')
    ga_calculator_1 = GeneticCalculatorPyEasyGa(data)
    task_1_result = ga_calculator_1.find_solution()
    print('Task 1 is done. The result json has been written to ' + result_file_path)
    create_json(result_file_path, task_1_result)

def print_items(data: DataProcessor):
    print('There are ' + str(len(data.items)) + ' items:')
    print('# (weight, volume, value)')
    number = 1
    for item in data.items:
        print(str(number) + ' ' + str(item))
        number += 1


if __name__ == "__main__":
    main()































# from pyeasyga import pyeasyga
#
# # setup data
# data = [(821, 0.8, 118), (1144, 1, 322), (634, 0.7, 166), (701, 0.9, 195),
#         (291, 0.9, 100), (1702, 0.8, 142), (1633, 0.7, 100), (1086, 0.6, 145),
#         (124, 0.6, 100), (718, 0.9, 208), (976, 0.6, 100), (1438, 0.7, 312),
#         (910, 1, 198), (148, 0.7, 171), (1636, 0.9, 117), (237, 0.6, 100),
#         (771, 0.9, 329), (604, 0.6, 391), (1078, 0.6, 100), (640, 0.8, 120),
#         (1510, 1, 188), (741, 0.6, 271), (1358, 0.9, 334), (1682, 0.7, 153),
#         (993, 0.7, 130), (99, 0.7, 100), (1068, 0.8, 154), (1669, 1, 289)]
#
# ga = pyeasyga.GeneticAlgorithm(data)        # initialise the GA with data
# ga.population_size = 200                    # increase population size to 200
#
#
# # define a fitness function
# def fitness(individual, data):
#     weight, volume, price = 0, 0, 0
#     for (selected, item) in zip(individual, data):
#         if selected:
#             weight += item[0]
#             volume += item[1]
#             price += item[2]
#     if weight > 12210 or volume > 12:
#         price = 0
#     return price
#
# ga.fitness_function = fitness               # set the GA's fitness function
# ga.run()                                    # run the GA
# print(ga.best_individual())                  # print the GA's best solution