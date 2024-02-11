import re

import aiohttp
from aiohttp import ClientTimeout
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from support_func import data_convert

ua = UserAgent()


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


async def pars_link(link: str) -> dict:
    data = dict()
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        async with session.get(url=link,
                               headers={
                                   'User-Agent': ua.random
                               },
                               timeout=ClientTimeout(total=1000)) as response:
            text = await response.text()
    soup = BeautifulSoup(text, 'lxml')
    all_ = await _all_specs(soup=soup)
    data.update(
        {
            'main': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'category': all_.get('Класс') if 'Класс' in all_.keys() else None,
                'advantage': [i.find_previous().getText() for i in soup.find_all(class_='icn-plus-css')],
                'disadvantage': [i.find_previous().getText() for i in soup.find_all(class_='icn-minus-css')],
                'total_score': int(all_.get('Итоговая оценка')) if 'Итоговая оценка' in all_.keys() else None,
                'announced': await data_convert(all_.get('Дата выхода')) if 'Дата выхода' in all_.keys() else None,
                'release_date': await data_convert(all_.get('Дата начала продаж')) if 'Дата начала продаж'
                                                                                      in all_.keys() else None,
            },
            'display': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'total_value': int(all_.get('Дисплей')) if 'Дисплей' in all_.keys() else None,
                'display_type': all_.get('Тип'),
                'd_size': float(all_.get('Размер').split(' ')[0]) if 'Размер' in all_.keys() else None,
                'resolution': all_.get('Разрешение').rsplit(' ', 1)[0] if 'Разрешение' in all_.keys() else None,
                'refresh_rate': int(all_.get('Частота обновления').split(' ')[0]) if 'Частота обновления'
                                                                                     in all_.keys() else None,
                'ppi': int(
                    all_.get('Плотность пикселей').split(' ')[0]) if 'Плотность пикселей' in all_.keys() else None,
                'adaptive_refresh_rate': False if all_.get('Адаптивная частота обновления') == 'Нет' else True,
                'hdr_support': all_.get('Поддержка HDR'),
                'screen_protection': all_.get('Защита дисплея'),
                'pwm': all_.get('ШИМ (PWM)'),
                'response_time': float(
                    all_.get('Время отклика').split(' ')[0]) if 'Время отклика' in all_.keys() else None,
            },
            'performance': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'total_value': int(all_.get('Производительность')) if 'Производительность' in all_.keys() else None,
                'chipset': all_.get('Чипсет'),
                'max_clock': int(
                    all_.get('Макс. частота').split(' ')[0]) if 'Макс. частота' in all_.keys() else None,
                'ram_size': [int(x.strip()) for x in all_.get('Объем ОЗУ').replace(' ГБ', '').split(',')],
                'memory_type': all_.get('Тип памяти'),
                'channels': int(all_.get('Количество каналов')) if 'Количество каналов' in all_.keys() else None,
                'storage_size': [int(x.strip()) for x in
                                 all_.get('Объем накопителя').replace(' ГБ', '').split(',')],
                'storage_type': all_.get('Тип накопителя'),
                'memory_card': False if all_.get('Карта памяти') == 'Нет' else True,
                'cpu_cores': all_.get('CPU-ядер'),
                'architecture': [x.strip() for x in
                                 all_.get('Архитектура').split('- ')[1:]] if 'Архитектура' in all_.keys() else None,
                'l3_cache': int(all_.get('Кэш L3').split(' ')[0]) if 'Кэш L3' in all_.keys() else None,
                'lithography_process': int(
                    all_.get('Размер транзистора').split(' ')[0]) if 'Размер транзистора' in all_.keys() else None,
                'graphics': all_.get('Графика'),
                'gpu_clock': int(all_.get('Частота GPU').split(' ')[0]) if all_.get('Частота GPU') else None,
                'geekbench_singlecore': int(all_.get('Geekbench 6 (одноядерный)')) if all_.get(
                    'Geekbench 6 (одноядерный)') else None,
                'geekbench_multicore': int(all_.get('Geekbench 6 (многоядерный)')) if all_.get(
                    'Geekbench 6 (многоядерный)') else None,
                'antutu_benchmark_': int(all_.get('AnTuTu Benchmark 10')) if all_.get('AnTuTu Benchmark 10') else None,
                'total_score': int(all_.get('Total score')) if all_.get('Total score') else None
            },
            'camera': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'total_value': int(all_.get('Камера')) if all_.get('Камера') else None,
                'matrix_main': float(all_.get('Матрица').split(' ')[0]) if all_.get('Матрица') else None,
                'image_resolution_main': all_.get('Разрешение фото'),
                'zoom': all_.get('Зум'),
                'flash': all_.get('Вспышка'),
                'stabilization': all_.get('Стабилизация'),
                'lenses': all_.get('Количество объективов'),
                'wide_main_lens': [x.strip() for x in all_.get('Основной объектив').split('- ')[1:]] if all_.get(
                    'Основной объектив') else None,
                'telephoto_lens': [x.strip() for x in all_.get('Телефото объектив').split('- ')[1:]] if all_.get(
                    'Телефото объектив') else None,
                'ultra_wide_lens': [x.strip() for x in
                                    all_.get('Сверхширокоугольный объектив').split('- ')[1:]] if all_.get(
                    'Сверхширокоугольный объектив') else None,
                'slow_motion': all_.get('Замедленная съемка'),
                'r1080p_video_recording': all_.get('Запись 1080p видео'),
                'r4k_video_recording': all_.get('Запись 4K видео'),
                'r8k_video_recording': all_.get('Запись 8K видео'),
                'megapixels_front': float(all_.get('Количество мегапикселей').split(' ')[0]) if all_.get(
                    'Матрица') else None,
                'aperture_front': all_.get('Апертура'),
                'video_resolution': all_.get('Разрешение видео')
            },
            'energy': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'total_value': int(all_.get('Батарея')) if all_.get('Батарея') else None,
                'capacity': int(all_.get('Объем').split(' ')[0]),
                'max_charge_power': float(all_.get('Макс. мощность зарядки').split(' ')[0]) if all_.get(
                    'Макс. мощность зарядки') else None,
                'battery_type': all_.get('Тип аккумулятора'),
                'wireless_charging': all_.get('Беспроводная зарядка'),
                'reverse_charging': all_.get('Реверсивная зарядка'),
                'fast_charging': all_.get('Быстрая зарядка'),
                'full_charging_time': all_.get('Время полной зарядки')
            },
            'communication': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'total_value': int(all_.get('Коммуникации')) if all_.get('Коммуникации') else None,
                'nfc': False if all_.get('NFC*') == 'Нет' else True,
                'number_of_sim': int(all_.get('Количество SIM*')) if all_.get('Количество SIM*') else None,
                'esim_support': False if all_.get('Поддержка eSIM*') == 'Нет' else True,
                'hybrid_slot': False if all_.get('Гибридный слот') == 'Нет' else True,
                'wifi_standard': all_.get('Версия Wi-Fi'),
                'wifi_features': [x.strip() for x in all_.get('Функции Wi-Fi').split('- ')[1:]] if all_.get(
                    'Функции Wi-Fi') else None,
                'bluetooth_version': all_.get('Версия Bluetooth'),
                'usb_type': all_.get('Тип USB'),
                'usb_version': float(all_.get('Версия USB')) if all_.get('Версия USB') else None,
                'usb_features': [x.strip() for x in all_.get('Функции USB').split('- ')[1:]] if all_.get(
                    'Функции USB') else None,
                'infrared_port': False if all_.get('Инфракрасный порт') == 'Нет' else True,
                'type_of_sim_card': all_.get('Тип SIM'),
                '_5g_support': False if all_.get('Поддержка 5G') == 'Нет' else True
            },
            'physicalparameters': {
                'title': soup.find('h1', class_="title-h1").text,
                'brand': soup.find('h1', class_="title-h1").text.split(' ')[0],
                'height': float(all_.get('Высота').split(' ')[0]) if all_.get('Высота') else None,
                'width': float(all_.get('Ширина').split(' ')[0]) if all_.get('Ширина') else None,
                'thickness': float(all_.get('Толщина').split(' ')[0]) if all_.get('Толщина') else None,
                'weight': float(all_.get('Вес').split(' ')[0]) if all_.get('Вес') else None,
                'waterproof': all_.get('Водонепроницаемость'),
                'colors': [x for x in all_.get('Доступные цвета').split(',')],
                'rear_material': all_.get('Материал задней панели'),
                'frame_material': all_.get('Материал рамки'),
                'fingerprint_scanner': all_.get('Сканер отпечатков пальцев'),
                'operating_system': all_.get('Операционная система'),
                'rom': all_.get('Оболочка UI'),
                'speakers': all_.get('Динамики'),
                'headphone_audio_jack': False if all_.get('3.5 мм аудио порт') == 'Нет' else True,
                'fm_radio': False if all_.get('FM-Радио') == 'Нет' else True,
                'dolby_atmos': False if all_.get('Dolby Atmos') == 'Нет' else True,
                'charger_out_of_the_box': all_.get('Зарядное устройство из коробки')
            }
        }
    )
    return data

    # for key, value in data.get('main').items():
    #     print(f'{key} {value}')
    # print('\n-----------------------------------------\n')
    # for key, value in data.get('display').items():
    #     print(f'{key} {value}')
    # print('\n-----------------------------------------\n')
    # for key, value in data.get('performance').items():
    #     print(f'{key} {value}')
    # print('\n-----------------------------------------\n')
    # for key, value in data.get('camera').items():
    #     print(f'{key} {value}')
    # print('\n-----------------------------------------\n')
    # for key, value in data.get('energy').items():
    #     print(f'{key} {value}')
    # print('\n-----------------------------------------\n')
    # for key, value in data.get('communication').items():
    #     print(f'{key} {value}')
    # print('\n-----------------------------------------\n')
    # for key, value in data.get('physicalparameters').items():
    #     print(f'{key} {value}')
