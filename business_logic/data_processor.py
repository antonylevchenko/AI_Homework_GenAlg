import os

#A processor for reading required data from source text files.
class DataProcessor:
    __file_path: str

    max_weight: int
    max_volume: float
    items: list

    def __init__(self, file_path: str):
        assert os.path.exists(file_path) and os.path.splitext(file_path)[-1].lower() == '.txt', \
            'Incorrect source file.'
        self.__file_path = file_path
        with open (self.__file_path, 'r') as source_file:
            limitations = source_file.readline().split(' ')
            self.max_weight = int(limitations[0])
            self.max_volume = float(limitations[1])
            self.items = []
            test = self.max_volume
            for line in source_file:
                item_data = line.split(' ')
                new_item = (int(item_data[0]), float(item_data[1]), int(item_data[2]))
                self.items.append(new_item)

