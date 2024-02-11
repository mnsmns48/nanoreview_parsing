from typing import Optional, List, Annotated

from sqlalchemy import String, SmallInteger, ARRAY, Text, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


title_pk = Annotated[str, mapped_column(primary_key=True, unique=True)]
brand_pk = Annotated[str, mapped_column(primary_key=True)]


class Main(Base):
    title: Mapped[title_pk]
    brand: Mapped[brand_pk]
    category: Mapped[Optional[str]] = mapped_column(String(15))
    advantage: Mapped[Optional[List]] = mapped_column(ARRAY(Text))
    disadvantage: Mapped[Optional[List]] = mapped_column(ARRAY(Text))
    total_score: Mapped[Optional[int]] = mapped_column(SmallInteger)
    announced: Mapped[Optional[str]] = mapped_column(String(7))
    release_date: Mapped[Optional[str]] = mapped_column(String(7))


class Display(Base):
    title: Mapped[title_pk] = mapped_column(ForeignKey('main.title'))
    brand: Mapped[brand_pk]
    total_value: Mapped[Optional[int]] = mapped_column(SmallInteger)
    display_type: Mapped[Optional[str]] = mapped_column(String(20))
    d_size: Mapped[Optional[float]]
    resolution: Mapped[Optional[str]] = mapped_column(String(15))
    refresh_rate: Mapped[Optional[int]] = mapped_column(SmallInteger)
    ppi: Mapped[Optional[int]] = mapped_column(SmallInteger)
    adaptive_refresh_rate: Mapped[Optional[bool]]
    hdr_support: Mapped[Optional[str]] = mapped_column(String(30))
    screen_protection: Mapped[Optional[str]] = mapped_column(String(30))
    pwm: Mapped[Optional[str]] = mapped_column(String(30))
    response_time: Mapped[Optional[int]] = mapped_column(SmallInteger)


class Performance(Base):
    title: Mapped[title_pk] = mapped_column(ForeignKey('main.title'))
    brand: Mapped[brand_pk]
    total_value: Mapped[Optional[int]] = mapped_column(SmallInteger)
    chipset: Mapped[Optional[str]] = mapped_column(String(50))
    max_clock: Mapped[Optional[int]] = mapped_column(SmallInteger)
    ram_size: Mapped[Optional[List]] = mapped_column(ARRAY(SmallInteger))
    memory_type: Mapped[Optional[str]] = mapped_column(String(10))
    channels: Mapped[Optional[int]] = mapped_column(SmallInteger)
    storage_size: Mapped[Optional[List]] = mapped_column(ARRAY(SmallInteger))
    storage_type: Mapped[Optional[str]] = mapped_column(String(15))
    memory_card: Mapped[Optional[bool]]
    cpu_cores: Mapped[Optional[str]] = mapped_column(String(25))
    architecture: Mapped[Optional[List]] = mapped_column(ARRAY(Text))
    l3_cache: Mapped[Optional[int]] = mapped_column(SmallInteger)
    lithography_process: Mapped[Optional[int]] = mapped_column(SmallInteger)
    graphics: Mapped[Optional[str]] = mapped_column(String(35))
    gpu_clock: Mapped[Optional[int]] = mapped_column(SmallInteger)
    geekbench_singlecore: Mapped[Optional[int]] = mapped_column(SmallInteger)
    geekbench_multicore: Mapped[Optional[int]] = mapped_column(SmallInteger)
    antutu_benchmark_: Mapped[Optional[int]] = mapped_column(Integer)
    total_score: Mapped[Optional[int]] = mapped_column(Integer)


class Camera(Base):
    title: Mapped[title_pk] = mapped_column(ForeignKey('main.title'))
    brand: Mapped[brand_pk]
    total_value: Mapped[Optional[int]] = mapped_column(SmallInteger)
    matrix_main: Mapped[Optional[int]] = mapped_column(SmallInteger)
    image_resolution_main: Mapped[Optional[str]] = mapped_column(String(15))
    zoom: Mapped[Optional[str]] = mapped_column(String(50))
    flash: Mapped[Optional[str]] = mapped_column(String(15))
    stabilization: Mapped[Optional[str]] = mapped_column(String(15))
    lenses: Mapped[Optional[str]] = mapped_column(String(40))
    wide_main_lens: Mapped[Optional[List]] = mapped_column(ARRAY(Text))
    telephoto_lens: Mapped[Optional[List]] = mapped_column(ARRAY(Text))
    ultra_wide_lens: Mapped[Optional[List]] = mapped_column(ARRAY(Text))
    slow_motion: Mapped[Optional[str]] = mapped_column(String(40))
    r1080p_video_recording: Mapped[Optional[str]] = mapped_column(String(30))
    r4k_video_recording: Mapped[Optional[str]] = mapped_column(String(30))
    r8k_video_recording: Mapped[Optional[str]] = mapped_column(String(30))
    megapixels_front: Mapped[Optional[float]]
    aperture_front: Mapped[Optional[str]] = mapped_column(String(10))
    video_resolution: Mapped[Optional[str]] = mapped_column(String(30))


class Energy(Base):
    title: Mapped[title_pk] = mapped_column(ForeignKey('main.title'))
    brand: Mapped[brand_pk]
    total_value: Mapped[Optional[int]] = mapped_column(SmallInteger)
    capacity: Mapped[Optional[int]] = mapped_column(SmallInteger)
    max_charge_power: Mapped[Optional[float]]
    battery_type: Mapped[Optional[str]] = mapped_column(String(35))
    wireless_charging: Mapped[Optional[str]] = mapped_column(String(30))
    reverse_charging: Mapped[Optional[str]] = mapped_column(String(30))
    fast_charging: Mapped[Optional[str]] = mapped_column(String(30))
    full_charging_time: Mapped[Optional[str]] = mapped_column(String(15))


class Communication(Base):
    title: Mapped[title_pk] = mapped_column(ForeignKey('main.title'))
    brand: Mapped[brand_pk]
    total_value: Mapped[Optional[int]] = mapped_column(SmallInteger)
    nfc: Mapped[Optional[bool]]
    number_of_sim: Mapped[Optional[int]] = mapped_column(SmallInteger)
    esim_support: Mapped[Optional[bool]]
    hybrid_slot: Mapped[Optional[bool]]
    wifi_standard: Mapped[Optional[str]] = mapped_column(String(40))
    wifi_features: Mapped[Optional[List]] = mapped_column(ARRAY(Text))
    bluetooth_version: Mapped[Optional[str]] = mapped_column(String(20))
    usb_type: Mapped[Optional[str]] = mapped_column(String(20))
    usb_version: Mapped[Optional[float]]
    usb_features: Mapped[Optional[List]] = mapped_column(ARRAY(Text))
    infrared_port: Mapped[Optional[bool]]
    type_of_sim_card: Mapped[Optional[str]] = mapped_column(String(20))
    _5g_support: Mapped[Optional[bool]]


class PhysicalParameters(Base):
    title: Mapped[title_pk] = mapped_column(ForeignKey('main.title'))
    brand: Mapped[brand_pk]
    height: Mapped[Optional[float]]
    width: Mapped[Optional[float]]
    thickness: Mapped[Optional[float]]
    weight: Mapped[Optional[float]]
    waterproof: Mapped[Optional[str]] = mapped_column(String(20))
    colors: Mapped[Optional[List]] = mapped_column(ARRAY(Text))
    rear_material: Mapped[Optional[str]] = mapped_column(String(20))
    frame_material: Mapped[Optional[str]] = mapped_column(String(20))
    fingerprint_scanner: Mapped[Optional[str]] = mapped_column(String(20))
    operating_system: Mapped[Optional[str]] = mapped_column(String(50))
    rom: Mapped[Optional[str]] = mapped_column(String(20))
    speakers: Mapped[Optional[str]] = mapped_column(String(20))
    headphone_audio_jack: Mapped[Optional[bool]]
    fm_radio: Mapped[Optional[bool]]
    dolby_atmos: Mapped[Optional[bool]]
    charger_out_of_the_box: Mapped[Optional[str]] = mapped_column(String(20))


class DataDirectory(Base):
    code: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    parent: Mapped[int]
    title: Mapped[str] = mapped_column(primary_key=True, unique=True)
    link: Mapped[str] = mapped_column(unique=True)
