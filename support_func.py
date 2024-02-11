async def data_convert(data: str) -> str:
    month = {
        'Январь': '01',
        'Февраль': '02',
        'Март': '03',
        'Апрель': '04',
        'Май': '05',
        'Июнь': '06',
        'Июль': '07',
        'Август': '08',
        'Сентябрь': '09',
        'Октябрь': '10',
        'Ноябрь': '11',
        'Декабрь': '12'
    }
    return f"{data.split(' ')[1]}-{month.get(data.split(' ')[0])}"


def change_key(key: str) -> str:
    for_change = {
        '5g_support': '_5g_support',
        'geekbench_5_singlecore': 'geekbench_singlecore',
        'geekbench_multicore': 'geekbench_multicore',
        'antutu_benchmark_9': 'antutu_benchmark_',
        'physical_parameters': 'physicalparameters',
        'nfc': 'nfcc'
    }
    if key in for_change.keys():
        return for_change.get(key)
    else:
        return key
