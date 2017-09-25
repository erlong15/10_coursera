# Граббер информации по курсам Coursera

Скрипт граббит случайные 20 курсов и записывает информацию о них в файл формата xlsx.

# Перед началом использования

Для работы необходим python версии 3.4 и выше
Требуется установить необходимые пакеты для работы. 

pip install -r requirements.txt 

# Как использовать
 В скрипт можно передать параметры:
 * -с <кол-во скачиваемых курсов> - по умолчанию 5
 * -o <файл для сохранения данных> по умолчанию courses.xlsx в каталоге запуска
 
Также можно запросить помощь по запуску

```
(venv) [lucky@lucky 10_coursera]$ python coursera.py -h
usage: coursera.py [-h] [-c COUNT] [-o OUTPUT]

this is a coursera random courses grabber.

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        How much courses do you want to scrape (default: 5)
  -o OUTPUT, --output OUTPUT
                        Output excel file name (default: courses.xlsx)

```

Пример запуска для получении 2х случайных записей в файл crs.xlsx
```
python coursera.py -c 2 -o crs.xlsx
```

в выходной файл пишутся следующие данные:
* название курса
* когда ближайшее начало
* продолжительность
* рейтинг
* ссылка ну курс

В зависимости от географического размещения сервера полученные данные могут быть на разных языках.

# Цель проекта

Тренировочный код для проекта [DEVMAN.org](https://devman.org)
