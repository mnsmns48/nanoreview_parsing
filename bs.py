import re
import aiohttp
from aiohttp import ClientTimeout
from bs4 import BeautifulSoup
from logic import ua
from support_func import data_convert


async def _all_specs(soup: BeautifulSoup) -> dict:
    result_dict = dict()
    upper_data = soup.find_all(class_='two-columns-item mb')
    for line in upper_data:
        key = line.find(class_='score-bar-name').getText().strip()
        value = re.match(
            pattern=r'\d+',
            string=line.find(class_='score-bar-result').getText().strip()
        )
        result_dict.update({key: value.group()})
    specification_names = soup.find_all('td', class_='cell-h')
    specification_value = soup.find_all('td', class_='cell-s')
    if len(specification_names) == len(specification_value):
        for _name, _value in zip(specification_names, specification_value):
            result_dict.update({f'{_name.getText()}': _value.getText()})
    return result_dict


async def pars_link(link: str):
    data = dict()
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get(url=link,
                               headers={
                                   'User-Agent': ua.random
                               },
                               timeout=ClientTimeout(total=1000)) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'lxml')
    all_specs = await _all_specs(soup=soup)

    data.update(
        {
            'main': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'category': all_specs.get('Класс'),
                'advantage': [i.text for i in
                              soup.find('ul', class_='proscons-list two-columns-item').find_all('li')],
                'disadvantage': [i.text for i in
                                 soup.find_all('ul', class_='proscons-list two-columns-item')[1].find_all('li')],
                'total_score': int(all_specs.get('Итоговая оценка')),
                'announced': await data_convert(all_specs.get('Дата выхода')),
                'release_date': await data_convert(all_specs.get('Дата начала продаж'))
            },
            'display': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'total_value': int(all_specs.get('Дисплей')),
                'display_type': all_specs.get('Тип'),
                'd_size': float(all_specs.get('Размер').split(' ')[0]),
                'resolution': all_specs.get('Разрешение').rsplit(' ', 1)[0],
                'refresh_rate': int(all_specs.get('Частота обновления').split(' ')[0]),
                'ppi': int(all_specs.get('Плотность пикселей').split(' ')[0]),
                'adaptive_refresh_rate': False if all_specs.get('Адаптивная частота обновления') == 'Нет' else True,
                'hdr_support': all_specs.get('Поддержка HDR'),
                'screen_protection': all_specs.get('Защита дисплея'),
                'pwm': all_specs.get('ШИМ (PWM)'),
                'response_time': float(all_specs.get('Время отклика').split(' ')[0]),
            },
            'performance': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'total_value': int(all_specs.get('Производительность')),
                'chipset': all_specs.get('Чипсет'),
                'max_clock': int(all_specs.get('Макс. частота').split(' ')[0]),
                'ram_size': [int(x.strip()) for x in all_specs.get('Объем ОЗУ').replace(' ГБ', '').split(',')],
                'memory_type': all_specs.get('Тип памяти'),
                'channels': int(all_specs.get('Количество каналов')),
                'storage_size': [int(x.strip()) for x in
                                 all_specs.get('Объем накопителя').replace(' ГБ', '').split(',')],
                'storage_type': all_specs.get('Тип накопителя'),
                'memory_card': False if all_specs.get('Карта памяти') == 'Нет' else True,
                'cpu_cores': all_specs.get('CPU-ядер'),
                'architecture': [x.strip() for x in all_specs.get('Архитектура').split('- ')[1:]],
                'l3_cache': int(all_specs.get('Кэш L3').split(' ')[0]),
                'lithography_process': int(all_specs.get('Размер транзистора').split(' ')[0]),
                'graphics': all_specs.get('Графика'),
                'gpu_clock': int(all_specs.get('Частота GPU').split(' ')[0]),
                'geekbench_singlecore': int(all_specs.get('Geekbench 6 (одноядерный)')),
                'geekbench_multicore': int(all_specs.get('Geekbench 6 (многоядерный)')),
                'antutu_benchmark_': int(all_specs.get('AnTuTu Benchmark 10')),
                'total_score': int(all_specs.get('Total score'))
            },
            'camera': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'total_value': int(all_specs.get('Камера')),
                'matrix_main': float(all_specs.get('Матрица').split(' ')[0]),
                'image_resolution_main': all_specs.get('Разрешение фото'),
                'zoom': all_specs.get('Зум'),
                'flash': all_specs.get('Вспышка'),
                'stabilization': all_specs.get('Стабилизация'),
                'lenses': all_specs.get('Количество объективов'),
                'wide_main_lens': [x.strip() for x in all_specs.get('Основной объектив').split('- ')[1:]],
                'telephoto_lens': [x.strip() for x in all_specs.get('Телефото объектив').split('- ')[1:]],
                'ultra_wide_lens': [x.strip() for x in
                                    all_specs.get('Сверхширокоугольный объектив').split('- ')[1:]],
                'slow_motion': all_specs.get('Замедленная съемка'),
                'r1080p_video_recording': all_specs.get('Запись 1080p видео'),
                'r4k_video_recording': all_specs.get('Запись 4K видео'),
                'r8k_video_recording': all_specs.get('Запись 8K видео'),
                'megapixels_front': all_specs.get('Количество мегапикселей'),
                'aperture_front': all_specs.get('Апертура'),
                'video_resolution': all_specs.get('Разрешение видео')
            },
            'energy': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'total_value': int(all_specs.get('Батарея')),
                'capacity': int(all_specs.get('Объем').split(' ')[0]),
                'max_charge_power': float(all_specs.get('Макс. мощность зарядки').split(' ')[0]),
                'battery_type': all_specs.get('Тип аккумулятора'),
                'wireless_charging': all_specs.get('Беспроводная зарядка'),
                'reverse_charging': all_specs.get('Реверсивная зарядка'),
                'fast_charging': all_specs.get('Быстрая зарядка'),
                'full_charging_time': all_specs.get('Время полной зарядки')
            },
            'communication': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'total_value': int(all_specs.get('Коммуникации')),
                'nfc': False if all_specs.get('NFC*') == 'Нет' else True,
                'number_of_sim': int(all_specs.get('Количество SIM*')),
                'esim_support': False if all_specs.get('Поддержка eSIM*') == 'Нет' else True,
                'hybrid_slot': False if all_specs.get('Гибридный слот') == 'Нет' else True,
                'wifi_standard': all_specs.get('Версия Wi-Fi'),
                'wifi_features': [x.strip() for x in all_specs.get('Функции Wi-Fi').split('- ')[1:]],
                'bluetooth_version': all_specs.get('Версия Bluetooth'),
                'usb_type': all_specs.get('Тип USB'),
                'usb_version': float(all_specs.get('Версия USB')),
                'usb_features': [x.strip() for x in all_specs.get('Функции USB').split('- ')[1:]],
                'gps': [x.strip() for x in all_specs.get('GPS').split('- ')[1:]],
                'infrared_port': False if all_specs.get('Инфракрасный порт') == 'Нет' else True,
                'type_of_sim_card': all_specs.get('Тип SIM'),
                'multi_sim_mode': all_specs.get('Режим работы SIM'),
                '_5g_support': False if all_specs.get('Поддержка 5G') == 'Нет' else True
            },
            'physicalparameters': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'height': float(all_specs.get('Высота').split(' ')[0]),
                'width': float(all_specs.get('Ширина').split(' ')[0]),
                'thickness': float(all_specs.get('Толщина').split(' ')[0]),
                'weight': float(all_specs.get('Вес').split(' ')[0]),
                'waterproof': False if all_specs.get('Водонепроницаемость') == 'Нет' else True,
                'colors': [x for x in all_specs.get('Доступные цвета').split(',')],
                'rear_material': all_specs.get('Материал задней панели'),
                'frame_material': all_specs.get('Материал рамки'),
                'fingerprint_scanner': all_specs.get('Сканер отпечатков пальцев'),
                'operating_system': all_specs.get('Операционная система'),
                'rom': all_specs.get('Оболочка UI'),
                'speakers': all_specs.get('Динамики'),
                'headphone_audio_jack': False if all_specs.get('3.5 мм аудио порт') == 'Нет' else True,
                'fm_radio': False if all_specs.get('FM-Радио') == 'Нет' else True,
                'dolby_atmos': False if all_specs.get('Dolby Atmos') == 'Нет' else True,
                'charger_out_of_the_box': all_specs.get('Зарядное устройство из коробки')
            }
        }
        )
    for k, v in data.get('physicalparameters').items():
        print(k, v)

# for k, v in all_specs.items():
#     print(k, v)
