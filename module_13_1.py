import asyncio


async def start_strongman1(name, power):
    print(f'Силач {name} начал соревнования.')
    for i in range(1, 6):
        print(f'Силач {name} поднял {i} шар.')
        await asyncio.sleep(5/power)
    print(f'Силач {name} закончил соревнования.')


async def start_strongman2(name, power):
    print(f'Силач {name} начал соревнования.')
    for i in range(1, 6):
        print(f'Силач {name} поднял {i} шар.')
        await asyncio.sleep(5/power)
    print(f'Силач {name} закончил соревнования.')


async def start_strongman3(name, power):
    print(f'Силач {name} начал соревнования.')
    for i in range(1, 6):
        print(f'Силач {name} поднял {i} шар.')
        await asyncio.sleep(5/power)
    print(f'Силач {name} закончил соревнования.')


async def start_tournament():
    task1 = asyncio.create_task(start_strongman1("Pasha", 3))
    task2 = asyncio.create_task(start_strongman2("Denis", 4))
    task3 = asyncio.create_task(start_strongman3('Apollon', 5))
    await task1
    await task2
    await task3

asyncio.run(start_tournament())

