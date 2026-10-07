from dataclasses import dataclass

@dataclass
class Zayavka:

    wagon_type: str
    numbers: list[str]
    month: str
    decade:int

    def count(self):
        return len(self.numbers)

    def summary(self):
        numbers_txt = ",".join(map(str, self.numbers))
        return f"{self.wagon_type}, количество {self.count()}, {self.month}, {self.decade}, {numbers_txt}"


wagon_type = input("Тип вагоны: ")
month = input("Месяц: ")
decade_ = int(input("Декада: "))
numbers_ = input("Номера вагонов через запятую:").split(',')


# numbers_list = [29125978, 29126018, 29126026,29125960, 57658841]

z1 = Zayavka(wagon_type=wagon_type, numbers=numbers_, month=month, decade=decade_)
print(z1.summary())

