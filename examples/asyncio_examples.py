import asyncio
from time import sleep
from threading import Thread

x = 0

def add(cond):
    global x
    while True:
        print(x)
        x += 1
        print(f'sleeping after x={x}')
        cond.notify()
        sleep(1)

def pred():
    res = x==3
    print(f' predicate {res}')
    return res

async def say(what, when, cond):
    await asyncio.sleep(when)
    global x
    x += 1
    cond.notify()
    print(what)

async def main():
    cond = asyncio.Condition()
    async with cond:
        asyncio.create_task(say('first', 1, cond))
        asyncio.create_task(say('first2', 2, cond))
        asyncio.create_task(say('first3', 3, cond))
        asyncio.create_task(say('first4', 4, cond))
        print('waiting for x')
        await cond.wait_for(pred)
        print('done wiating x')
    print('done')

if __name__ == '__main__':
    asyncio.run(main())
    print('exited func')