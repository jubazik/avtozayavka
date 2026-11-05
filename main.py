import asyncio

from bot.setting import main
from gu_12.zayavka import Zayavka
from gu_12.letter import save_docx



def console():
    wagon_type =  input("Тип вагоны: ")
    month = input("Месяц: ")
    decade_ = input("Декада: ")
    numbers_ = input("Номера вагонов: ").replace(",", " ").split()

    try:
        z1 = Zayavka(wagon_type=wagon_type.lower(), wagons=numbers_, month=month, decade=decade_)
    except ValueError as e:
        print(f"Ошибка: {e}")
        return


    print(z1.summary())
    save_docx(z1)


if __name__ == "__main__":
    asyncio.run(main())
