import asyncio


async def main():
    print('If you want to parse the entire site, press "1", if you want to parse a separate link, then press "2"')
    try:
        choice = int(input())
        if choice == 1:
            await fullparse()
        if choice == 2:
            await one_link()
        else:
            print('Incorrect input, you must press "1" or "2"')
    except ValueError:
        print('Incorrect input!')

    await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
