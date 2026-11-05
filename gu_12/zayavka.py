from dataclasses import dataclass
import re

MONTHS = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль",
          "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]

WORDS = {1: "один", 2: "два", 3: "три", 4: "четыре", 5: "пять",
         6: "шесть", 7: "семь", 8: "восемь", 9: "девять", 10: "десять"}

DECADES = {1: "первую", 2: "вторую", 3: "третью"}

# Формы слова «вагон» после числа: (1, 2–4, 5+)
WAGON_FORMS = {
    "крытые": ("крытый вагон", "крытых вагона", "крытых вагонов"),
    "полувагоны": ("полувагон", "полувагона", "полувагонов"),
}


def plural(n: int, forms: tuple[str, str, str]) -> str:
    """Выбирает форму слова: 1 вагон, 2 вагона, 5 вагонов, 21 вагон, 11 вагонов."""
    one, few, many = forms
    if 11 <= n % 100 <= 14:
        return many
    if n % 10 == 1:
        return one
    if 2 <= n % 10 <= 4:
        return few
    return many


def check_digit_ok(number: str) -> bool:
    """Контрольная (8-я) цифра номера вагона: первые 7 цифр с весами 2,1,2,1,2,1,2."""
    digits = [int(c) for c in number]
    total = 0
    for i, d in enumerate(digits[:7]):
        p = d * (2 if i % 2 == 0 else 1)
        total += p // 10 + p % 10
    return (10 - total % 10) % 10 == digits[7]


@dataclass
class Zayavka:

    wagon_type: str
    wagons: list[str]
    month: str
    decade: int

    def __post_init__(self):
        self.wagon_type = str(self.wagon_type).strip().lower()
        if self.wagon_type not in WAGON_FORMS:
            raise ValueError("Тип вагонов: «крытые» или «полувагоны»")

        self.month = str(self.month).strip().lower()
        if self.month not in MONTHS:
            raise ValueError(f"Месяц «{self.month}»: введите название, например «октябрь»")

        if self.decade not in DECADES:
            raise ValueError("Декада: 1, 2 или 3")

        self.wagons = [str(n).strip() for n in self.wagons]
        if not self.wagons:
            raise ValueError("Не введено ни одного номера вагона")

        seen = set()
        for n in self.wagons:
            if not re.fullmatch(r"\d{8}", n):
                raise ValueError(f"Номер {n}: должно быть ровно 8 цифр")
            if not check_digit_ok(n):
                raise ValueError(f"Номер {n}: не сходится контрольная цифра, проверьте опечатку")
            if n in seen:
                raise ValueError(f"Номер {n} повторяется")
            seen.add(n)

    def ordinal_to_words(self):
        return DECADES[self.decade]

    def count(self):
        return len(self.wagons)

    def count_text(self):
        n = self.count()
        number = WORDS.get(n, str(n))       # до 10 словами, дальше цифрами
        return f"{number} {plural(n, WAGON_FORMS[self.wagon_type])}"

    def summary(self):
        return f"количество {self.count_text()}, {', '.join(self.wagons)}"