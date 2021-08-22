import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Функция, возвращающая ссылку на xml-файл текущего года
def getUrl():
    url = 'http://xmlcalendar.ru/data/ru/' + getCurrentYear() + '/calendar.xml'

    return url

# Функция, возвращающая массив, содержащий названия каждого из
# нерабочих дней
def getHolydaysName():
    # Ссылка на xml-файл
    url = getUrl()

    # Берем данные из xml-файла, расположенного по адресу url,
    # преобразовываем их в строку, а затем из строки представляем
    # весь xml-документ ввиде дерева. root - переменная, являющаяся
    # корневым узлом дерева
    root = ET.fromstring(requests.get(url).content)

    # Массив, содержащий названия выходных дней
    holydaysName = []

    # Проходимся по всем дочерним узлам дерева
    for elem in root:
        # Если текущий тег равняется 'holidays', то
        if elem.tag == 'holidays':
            # проходимся по дочерним элементам в этом теге
            for item in elem:
                # и добавим в массив значения элемента с атрибутом 
                # title, содержащим название нерабочего дня
                holydaysName.append(item.attrib.get('title'))

    # Возвращаем массив с наименованиями выходных дней
    return holydaysName

# Функция возвращает двумерный массив с датами нерабочих дней
# и их названиями
def getHolydays():
    url = getUrl()

    root = ET.fromstring(requests.get(url).content)

    # Массив, содержащий названия выходных дней
    holydaysName = getHolydaysName()

    # Инициализация массива, содержащего даты выходных и их названия
    holydays = []
    holydays.append([])
    holydays.append([])

    # Проходимся по всем дочерним узлам дерева
    for elem in root:
        # Если текущий тег равняется 'days', то
        if elem.tag == 'days':
            # проходимся по дочерним элементам в этом теге
            for item in elem:
                # Если атрибут t, определяющий выходной (1) это день  
                # или сокращенный (2), текущего элемента равен 1, то
                if item.attrib.get('t') == '1': 
                    # добавляем в массив сначала число в формате "ДД.ММ"
                    holydays[0].append(item.attrib.get('d').split('.')[1]+\
                    '.'+item.attrib.get('d').split('.')[0])
                    # Затем проверяем, существует ли название у нерабочего дня
                    id = item.attrib.get('h')
                    # Если существует, то добавляем его в массив
                    if id != None:
                        holydays[1].append(holydaysName[int(id)-1])
                    else:
                        # иначе добавляем в массив пустое значение
                        holydays[1].append(None)

    # Возвращаем массив с датами и наименованиями нерабочих дней
    return holydays

# Функция возвращает текстовую переменную со значением текущего года
def getCurrentYear():
    year = str(datetime.now().year)

    return year


def getResponse(month = None):
    holydays = getHolydays()

    response = ''

    if month == None:
        response = 'Список выходных дней в году:\n'
        for i in range(0, len(holydays[0])):
            if holydays[1][i] == None:
                response += holydays[0][i] + '\n'
            else:
                response += holydays[0][i] + ' - ' + holydays[1][i] + '\n'
    elif month == 'январь':
        response = 'Список выходных дней в январе:\n'
        response += getHolydaysByMonth(holydays, '01')
    elif month == 'февраль':
        response = 'Список выходных дней в феврале:\n'
        response += getHolydaysByMonth(holydays, '02')
    elif month == 'март':
        response = 'Список выходных дней в марте:\n'
        response += getHolydaysByMonth(holydays, '03')
    elif month == 'апрель':
        response = 'Список выходных дней в апреле:\n'
        response += getHolydaysByMonth(holydays, '04')
    elif month == 'май':
        response = 'Список выходных дней в мае:\n'
        response += getHolydaysByMonth(holydays, '05')
    elif month == 'июнь':
        response = 'Список выходных дней в июне:\n'
        response += getHolydaysByMonth(holydays, '06')
    elif month == 'июль':
        response = 'Список выходных дней в июле:\n'
        response += getHolydaysByMonth(holydays, '07')
    elif month == 'август':
        response = 'Список выходных дней в августе:\n'
        response += getHolydaysByMonth(holydays, '08')
    elif month == 'сентябрь':
        response = 'Список выходных дней в сентябре:\n'
        response += getHolydaysByMonth(holydays, '09')
    elif month == 'октябрь':
        response = 'Список выходных дней в октябре:\n'
        response += getHolydaysByMonth(holydays, '10')
    elif month == 'ноябрь':
        response = 'Список выходных дней в ноябре:\n'
        response += getHolydaysByMonth(holydays, '11')
    elif month == 'декабрь':
        response = 'Список выходных дней в декабре:\n'
        response += getHolydaysByMonth(holydays, '12')
    else:
        response = 'Простите, я не понимаю. Введите, пожалуйста, корректный месяц'

    return response


def getHolydaysByMonth(holydays, month):
    response = ''

    for i in range(0, len(holydays[0])):
        if holydays[0][i].split('.')[1] == month:
            if holydays[1][i] == None:
                response += holydays[0][i] + '\n'
            else:
                response += holydays[0][i] + ' - ' + holydays[1][i] + '\n'

    if not response:
        response = 'Выходных в данном месяце нет'
    
    return response
