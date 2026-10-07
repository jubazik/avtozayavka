from dataclasses import dataclass

@dataclass
class Zayavka:
    """ Атрибуты"""
    wagon_type: str
    numbers: list[int]
    month: str
    decade:int

    """Методы"""

    def count(self):
        return len(self.numbers)

    def summary(self):
        numbers_txt = ",".join(map(str, self.numbers))
        return f"{self.wagon_type}, количество {self.count()}, {self.month}, {self.decade}, {numbers_txt}"



numbers_list = [29125978, 29126018, 29126026,29125960, 57658841]

z1 = Zayavka(wagon_type='Крытые', month='Октябрь', decade=4, numbers=numbers_list)
print(z1.summary())

