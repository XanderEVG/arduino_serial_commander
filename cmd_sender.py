import sys
import serial
import serial.tools.list_ports
import argparse
import time
from argparse import RawTextHelpFormatter
import datetime

cmd_help = """Доступные команды:
SCTI - Установить время (первые 3 байта: часы, минуты, секунды)
GCTI - Получить время
SOCR - Установить OCR (делитель таймера, первые 2 байта, первый - старший). Значение по умолчанию в приборе 250
GOCR - Получить OCR
SMIS - Установить MIS (количество миллисекунд в секунде, для подстройки). Значение по умолчанию в приборе 997  // python3 cmd_sender.py -c SMIS -v0 3 -v1 228
GMIS - Получить MIS
SDAY - Установить статистику (количество дней)
GDAY - Получить статистику (количество дней)
RLCD - Перезагрузить дисплей
FLCD - Выключить дисплей
OLCD - Включить дисплей   
GHUM - Получить влажность
GTEM - Получить температуру
PAUS - Выключить все на n секунд (2 байта)
-----------------------------------------
AUTO_TIME - Установить текущее время
COMPARE_TIME - Сравнить время с реальным
SET_OCR_HUMAN - Получить OCR разбивая 1 аргумент на байты
SET_MIS_HUMAN - Получить MIS разбивая 1 аргумент на байты

"""
parser = argparse.ArgumentParser(description='Kanabis control', formatter_class=RawTextHelpFormatter)
parser.add_argument('-c', action="store", dest="cmd", required=True, help=cmd_help)

parser.add_argument('-v0', action="store", dest="v0", default=0, type=int, help='1 байт данных')
parser.add_argument('-v1', action="store", dest="v1", default=0, type=int, help='2 байт данных')
parser.add_argument('-v2', action="store", dest="v2", default=0, type=int, help='3 байт данных')
parser.add_argument('-v3', action="store", dest="v3", default=0, type=int, help='4 байт данных')
parser.add_argument('-v', '--debug', action='store_true')
args = parser.parse_args()


if args.cmd == "AUTO_TIME":
    now = datetime.datetime.now()
    args.cmd = "SCTI"
    args.v0 = now.hour
    args.v1 = now.minute
    args.v2 = now.second


if args.cmd == "COMPARE_TIME":
    now = datetime.datetime.now()
    print("      {0:02d}:{1:02d}:{2:02d}".format(now.hour, now.minute, now.second))
    args.cmd = "GCTI"

if args.cmd == "SET_OCR_HUMAN":
    exit("Не реализовано")

if args.cmd == "SET_MIS_HUMAN":
    exit("Не реализовано")

ports = serial.tools.list_ports.comports()
port = None
for p in ports:
    if "ttyUSB" in p.device:
        port = p.device
if port is None:
    sys.exit("error: Нет доступных портов")


try:
    ser = serial.Serial(port, 115200)
    ser.timeout = 1
    ser.write_timeout = 1.0
except Exception as e:
    sys.exit("error: Ошибка открытия порта - " + str(e))

if ser.isOpen():
    ser.write(b'CMD_')
    cmd_temp = args.cmd.encode().decode("utf-8")
    cmd_ascii = cmd_temp.encode("ascii", "ignore")
    ser.write(cmd_ascii)
    ser.write(b'_')
    packet = bytearray()
    packet.append(args.v0)
    packet.append(args.v1)
    packet.append(args.v2)
    packet.append(args.v3)
    ser.write(packet)
    ser.write(b'_END\n')
    time.sleep(0.05)
    data = ser.readline()
    answer = data.decode("utf-8")
    print(answer)

else:
    sys.exit("error: Ошибка открытия порта")

