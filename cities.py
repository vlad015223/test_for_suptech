import json
import random

class CityPopulation:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cities = self._load_cities()

    # записываем данные с файла в словарь
    def _load_cities(self) -> dict:
        with open(self.file_path) as file:
            data = json.load(file)
        cities = {}
        for city_data in data:
            cities[city_data['name']] = city_data['population']
        return cities

    def get_random_city(self) -> str:
        total_population = sum(self.cities.values())
        # умножаем рандомное число от 0 до 1 на общее население людей со всех городов
        random_value = random.random() * total_population
        summary_population = 0
        # если полученное рандомное число входит в диапазон населения города, то возвращаем этот город
        for city, population in self.cities.items():
            summary_population += population
            if random_value <= summary_population:
                return city


city_population = CityPopulation("input.json")
print(city_population.get_random_city())
