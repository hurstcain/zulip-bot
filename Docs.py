from docxtpl import DocxTemplate
from petrovich.main import Petrovich
from petrovich.enums import Case, Gender
from datetime import datetime
import sqlite3


db = sqlite3.connect("mydb.db")

# Функция, атоматически заполняющая заявление на отпуск на примере готового шаблона 
# Переменная path - путь к нужному шаблону, берется из БД 
# userId - это электронная почта пользователя, является идентификатором каждого из пользователей
# beginDate - дата начала отпуска, вводится пользователем
# endDate - дата окончания отпуска, вводится пользователем 
# period - количество отпускных дней
def vacationRequest(path, userId, beginDate, endDate, period):
    # Переменная, в которую записывается название организации
    # Функция getOrganization() извлекает из таблицы CompanyInfo базы данных содержание
    # столбца с названием организации и возвращает его
    organization = getOrganization()
    # Переменная, в которую записывается полное имя директора организации в дательном падеже
    # Функция getDirectorName() извлекает из таблицы CompanyInfo содержание
    # четырех столбцов с именем, фамилией, отчеством и полом; преобразовывает имена из именительного в 
    # дательный падеж; а затем соединяет три имени в одну текстовую переменую и возвращает ее значение
    directorFullName = getDirectorName()
    # Переменная, содержащая полное имя сотрудника в родительном падеже
    # Функция getEmployeeName() извлекает из таблицы User фамилию, имя, отчество и пол
    # сотрудника с идентификатором userId; преобразовывает имена из именительного в 
    # родительный падеж; а затем соединяет три имени в одну текстовую переменую и возвращает ее значение
    employeeFullName = getEmployeeName(userId)
    # Переменная с текущей датой
    # Функуия getTodayDate() преобразовывает текущую дату в формат "ЧЧ.ММ.ГГГГ", записывает 
    # значение в текстовую переменную и возвращает ее
    todayDate = getTodayDate()
    # Переменная, в которой хранится имя пользователя в именительном падеже, 
    # записанное по шаблону “Фамилия И.О.”
    # Функция getEmployeeFIO() работает по такому же принципу, что и функция getEmployeeName()
    # Достает данные из таблицы БД и преобразовывает имя в надлежащий вид, затем 
    # записывает в текстовую переменную и возвращает ее
    employeeFIO = getEmployeeFIO(userId)

    # Переменная с названием документа. Документ располагается в папке user_docs, а в качестве имени 
    # используется идентификатор пользователя
    finalDocName = "user_docs/" + userId + ".docx"

    # Открытие шаблона 
    doc = DocxTemplate(path)
    # Словарь с тегами шаблона, которым присваиваются соответствующие значения
    context = { 'organization' : organization,
                'directorFullName' : directorFullName,
                'employeeFullName' : employeeFullName,
                'beginDate' : beginDate,
                'endDate' : endDate,
                'period' : period,
                'todayDate' : todayDate,
                'employeeFIO' : employeeFIO}
    # Преобразование шаблона в заполненное заявление
    doc.render(context)
    # Сохранение заявления
    doc.save(finalDocName)

    # Функция возвращает полное название документа, чтобы впоследствии отправить его пользователю
    return finalDocName

def zayavlenieNaOtpusk(path, userId, beginDate, endDate, period):
    organization = getOrganization()
    directorFullName = getDirectorName()
    employeeFullName = getEmployeeName(userId)
    todayDate = getTodayDate()
    employeeFIO = getEmployeeFIO(userId)
    finalDocName = "user_docs/" + userId + ".docx"

    doc = DocxTemplate(path)
    context = { 'organization' : organization,
                'directorFullName' : directorFullName,
                'employeeFullName' : employeeFullName,
                'beginDate' : beginDate,
                'endDate' : endDate,
                'period' : period,
                'todayDate' : todayDate,
                'employeeFIO' : employeeFIO}
    doc.render(context)
    doc.save(finalDocName)

    return finalDocName


def zayavlenieNaOtpuskPoUhoduZaRebenkomDoTrehLet(path, userId, childFullName, date):
    organization = getOrganization()
    directorFullName = getDirectorName()
    employeeFullName = getEmployeeName(userId)
    todayDate = getTodayDate()
    employeeFIO = getEmployeeFIO(userId)
    finalDocName = "user_docs/" + userId + ".docx"

    doc = DocxTemplate(path)
    context = { 'organization' : organization,
                'directorFullName' : directorFullName,
                'employeeFullName' : employeeFullName,
                'childFullName' : childFullName,
                'date' : date,
                'todayDate' : todayDate,
                'employeeFIO' : employeeFIO}
    doc.render(context)
    doc.save(finalDocName)

    return finalDocName


def zayavlenieNaUvolneniePoSobstvennomuZhelaniyu(path, userId, date):
    organization = getOrganization()
    directorFullName = getDirectorName()
    employeeFullName = getEmployeeName(userId)
    todayDate = getTodayDate()
    employeeFIO = getEmployeeFIO(userId)
    finalDocName = "user_docs/" + userId + ".docx"

    doc = DocxTemplate(path)
    context = { 'organization' : organization,
                'directorFullName' : directorFullName,
                'employeeFullName' : employeeFullName,
                'dismissalDate' : date,
                'todayDate' : todayDate,
                'employeeFIO' : employeeFIO}
    doc.render(context)
    doc.save(finalDocName)

    return finalDocName


def zayavlenieObOtziveZayavleniyaObUvolnenii(path, userId, date):
    organization = getOrganization()
    directorFullName = getDirectorName()
    employeeFullName = getEmployeeName(userId)
    employeeFullFIO = getEmployeeFullFIO(userId)
    todayDate = getTodayDate()
    employeeFIO = getEmployeeFIO(userId)
    finalDocName = "user_docs/" + userId + ".docx"

    doc = DocxTemplate(path)
    context = { 'organization' : organization,
                'directorFullName' : directorFullName,
                'employeeFullName' : employeeFullName,
                'employeeFullFIO' : employeeFullFIO,
                'dismissalDate' : date,
                'todayDate' : todayDate,
                'employeeFIO' : employeeFIO}
    doc.render(context)
    doc.save(finalDocName)

    return finalDocName


def zayavlenieOPerevodeNaNepolnoeRabocheeVremya(path, userId, date):
    organization = getOrganization()
    directorFullName = getDirectorName()
    employeeFullName = getEmployeeName(userId)
    todayDate = getTodayDate()
    employeeFIO = getEmployeeFIO(userId)
    finalDocName = "user_docs/" + userId + ".docx"

    doc = DocxTemplate(path)
    context = { 'organization' : organization,
                'directorFullName' : directorFullName,
                'employeeFullName' : employeeFullName,
                'date' : date,
                'todayDate' : todayDate,
                'employeeFIO' : employeeFIO}
    doc.render(context)
    doc.save(finalDocName)

    return finalDocName


def zayavlenieOPredostavleniiOtpuskaZaSvoiChetVSvyaziSRegistracieiBraka(path, userId, beginDate, endDate):
    organization = getOrganization()
    directorFullName = getDirectorName()
    employeeFullName = getEmployeeName(userId)
    todayDate = getTodayDate()
    employeeFIO = getEmployeeFIO(userId)
    finalDocName = "user_docs/" + userId + ".docx"

    doc = DocxTemplate(path)
    context = { 'organization' : organization,
                'directorFullName' : directorFullName,
                'employeeFullName' : employeeFullName,
                'beginDate' : beginDate,
                'endDate' : endDate,
                'todayDate' : todayDate,
                'employeeFIO' : employeeFIO}
    doc.render(context)
    doc.save(finalDocName)

    return finalDocName


def zayavlenieOPredostavleniiOtpuskaZaSvoiChetVSvyaziSRoshdeniemRebenka(path, userId, beginDate, endDate):
    organization = getOrganization()
    directorFullName = getDirectorName()
    employeeFullName = getEmployeeName(userId)
    todayDate = getTodayDate()
    employeeFIO = getEmployeeFIO(userId)
    finalDocName = "user_docs/" + userId + ".docx"

    doc = DocxTemplate(path)
    context = { 'organization' : organization,
                'directorFullName' : directorFullName,
                'employeeFullName' : employeeFullName,
                'beginDate' : beginDate,
                'endDate' : endDate,
                'todayDate' : todayDate,
                'employeeFIO' : employeeFIO}
    doc.render(context)
    doc.save(finalDocName)

    return finalDocName


def zayavlenieOPredostavleniiRabotnikuDonoruDvuhDneiOtdiha(path, userId, beginDate, endDate, cerDate):
    organization = getOrganization()
    directorFullName = getDirectorName()
    employeeFullName = getEmployeeName(userId)
    todayDate = getTodayDate()
    employeeFIO = getEmployeeFIO(userId)
    finalDocName = "user_docs/" + userId + ".docx"

    doc = DocxTemplate(path)
    context = { 'organization' : organization,
                'directorFullName' : directorFullName,
                'employeeFullName' : employeeFullName,
                'beginDate' : beginDate,
                'endDate' : endDate,
                'certificateDate' : cerDate,
                'todayDate' : todayDate,
                'employeeFIO' : employeeFIO}
    doc.render(context)
    doc.save(finalDocName)

    return finalDocName


def zayavlenieOSoglasiiNaRabotuVVihodnoiDen(path, userId, date):
    organization = getOrganization()
    directorFullName = getDirectorName()
    employeeFullName = getEmployeeName(userId)
    todayDate = getTodayDate()
    employeeFIO = getEmployeeFIO(userId)
    finalDocName = "user_docs/" + userId + ".docx"

    doc = DocxTemplate(path)
    context = { 'organization' : organization,
                'directorFullName' : directorFullName,
                'employeeFullName' : employeeFullName,
                'date' : date,
                'todayDate' : todayDate,
                'employeeFIO' : employeeFIO}
    doc.render(context)
    doc.save(finalDocName)

    return finalDocName


def messageProcessing(userId, content):
    pathToFile = ''

    if ("заявление на отпуск" in content.lower()):
        message = content.split()

        if len(message) !=  6:
            response = "Чтобы заполнить " + getDocName(1) + ", \n"
            response += "введите дату начала отпуска, дату конца отпуска и период отпуска через пробел.\n"
            response += "Например, 'заявление на отпуск 30.07.2021 8.08.2021 10'\n"

            return [False, response]
        else:
            beginDate = message[3]
            endDate = message[4]
            period = message[5]
            path = getDocPath(1)

            pathToFile = zayavlenieNaOtpusk(path, userId, beginDate, endDate, period)

    elif (content.split()[0] == '1'):
        message = content.split()

        if len(message) !=  4:
            response = "Чтобы заполнить " + getDocName(1) + ", \n"
            response += "введите дату начала отпуска, дату конца отпуска и период отпуска через пробел.\n"
            response += "Например, '1 30.07.2021 8.08.2021 10'\n"

            return [False, response]
        else:
            beginDate = message[1]
            endDate = message[2]
            period = message[3]
            path = getDocPath(1)

            pathToFile = zayavlenieNaOtpusk(path, userId, beginDate, endDate, period)

    elif ("заявление на отпуск по уходу за ребенком до трех лет" in content.lower()):
        message = content.split()

        if len(message) !=  14:
            response = "Чтобы заполнить " + getDocName(3) + ", \n"
            response += "введите ФИО ребенка в творительном падеже и дату начала отпуска через пробел.\n"
            response += "Например, 'заявление на отпуск по уходу за ребенком до трех лет Ивановым Иваном Ивановичем 8.08.2021'\n"

            return [False, response]
        else:
            childFullName = message[10] + ' ' + message[11] + ' ' + message[12]
            date = message[13]
            path = getDocPath(3)

            pathToFile = zayavlenieNaOtpuskPoUhoduZaRebenkomDoTrehLet(path, userId, childFullName, date)

    elif (content.split()[0] == '3'):
        message = content.split()

        if len(message) !=  5:
            response = "Чтобы заполнить " + getDocName(3) + ", \n"
            response += "введите ФИО ребенка в творительном падеже и дату начала отпуска через пробел.\n"
            response += "Например, '3 Ивановым Иваном Ивановичем 8.08.2021'\n"

            return [False, response]
        else:
            childFullName = message[1] + ' ' + message[2] + ' ' + message[3]
            date = message[4]
            path = getDocPath(3)

            pathToFile = zayavlenieNaOtpuskPoUhoduZaRebenkomDoTrehLet(path, userId, childFullName, date)

    elif ("заявление об увольнении по собственному желанию" in content.lower()):
        message = content.split()

        if len(message) !=  7:
            response = "Чтобы заполнить " + getDocName(2) + ", \n"
            response += "введите дату увольнения.\n"
            response += "Например, 'заявление об увольнении по собственному желанию 8.08.2021'\n"

            return [False, response]
        else:
            date = message[6]
            path = getDocPath(2)

            pathToFile = zayavlenieNaUvolneniePoSobstvennomuZhelaniyu(path, userId, date)
    
    elif (content.split()[0] == '2'):
        message = content.split()

        if len(message) !=  2:
            response = "Чтобы заполнить " + getDocName(2) + ", \n"
            response += "введите дату увольнения.\n"
            response += "Например, '2 8.08.2021'\n"

            return [False, response]
        else:
            date = message[1]
            path = getDocPath(2)

            pathToFile = zayavlenieNaUvolneniePoSobstvennomuZhelaniyu(path, userId, date)

    elif ("заявление об отзыве заявления об увольнении по собственному желанию" in content.lower()):
        message = content.split()

        if len(message) !=  10:
            response = "Чтобы заполнить " + getDocName(8) + ", \n"
            response += "введите дату, когда было написано заявление об увольнении.\n"
            response += "Например, 'заявление об отзыве заявления об увольнении по собственному желанию 6.06.2021'\n"

            return [False, response]
        else:
            date = message[9]
            path = getDocPath(8)

            pathToFile = zayavlenieObOtziveZayavleniyaObUvolnenii(path, userId, date)

    elif (content.split()[0] == '8'):
        message = content.split()

        if len(message) !=  2:
            response = "Чтобы заполнить " + getDocName(8) + ", \n"
            response += "введите дату, когда было написано заявление об увольнении.\n"
            response += "Например, '8 6.06.2021'\n"

            return [False, response]
        else:
            date = message[1]
            path = getDocPath(8)

            pathToFile = zayavlenieObOtziveZayavleniyaObUvolnenii(path, userId, date)

    elif ("заявление о переводе на неполное рабочее время" in content.lower()):
        message = content.split()

        if len(message) !=  8:
            response = "Чтобы заполнить " + getDocName(4) + ", \n"
            response += "введите дату, с которой будет осуществлен перевод на неполное рабочее время.\n"
            response += "Например, 'заявление о переводе на неполное рабочее время 6.06.2021'\n"

            return [False, response]
        else:
            date = message[7]
            path = getDocPath(4)

            pathToFile = zayavlenieOPerevodeNaNepolnoeRabocheeVremya(path, userId, date)

    elif (content.split()[0] == '4'):
        message = content.split()

        if len(message) !=  2:
            response = "Чтобы заполнить " + getDocName(4) + ", \n"
            response += "введите дату, с которой будет осуществлен перевод на неполное рабочее время.\n"
            response += "Например, '4 6.06.2021'\n"

            return [False, response]
        else:
            date = message[1]
            path = getDocPath(4)

            pathToFile = zayavlenieOPerevodeNaNepolnoeRabocheeVremya(path, userId, date)

    elif ("заявление о предоставлении отпуска за свой счет продолжительностью 5 календарных дней работнику в связи с регистрацией брака" in content.lower()):
        message = content.split()

        if len(message) !=  19:
            response = "Чтобы заполнить " + getDocName(7) + ", \n"
            response += "введите дату начала отпуска и дату окончания отпуска через пробел.\n"
            response += "Например, 'заявление о предоставлении отпуска за свой счет продолжительностью 5 календарных дней работнику в связи с регистрацией брака 02.06.2021 6.06.2021'\n"

            return [False, response]
        else:
            beginDate = message[17]
            endDate = message[18]
            path = getDocPath(7)

            pathToFile = zayavlenieOPredostavleniiOtpuskaZaSvoiChetVSvyaziSRegistracieiBraka(path, userId, beginDate, endDate)

    elif (content.split()[0] == '7'):
        message = content.split()

        if len(message) !=  3:
            response = "Чтобы заполнить " + getDocName(7) + ", \n"
            response += "введите дату начала отпуска и дату окончания отпуска через пробел.\n"
            response += "Например, '7 02.06.2021 6.06.2021'\n"

            return [False, response]
        else:
            beginDate = message[1]
            endDate = message[2]
            path = getDocPath(7)

            pathToFile = zayavlenieOPredostavleniiOtpuskaZaSvoiChetVSvyaziSRegistracieiBraka(path, userId, beginDate, endDate)

    elif ("заявление о предоставлении отпуска за свой счет продолжительностью 5 календарных дней работнику в связи с рождением у него ребенка" in content.lower()):
        message = content.split()

        if len(message) !=  21:
            response = "Чтобы заполнить " + getDocName(6) + ", \n"
            response += "введите дату начала отпуска и дату окончания отпуска через пробел.\n"
            response += "Например, 'заявление о предоставлении отпуска за свой счет продолжительностью 5 календарных дней работнику в связи с рождением у него ребенка 02.06.2021 6.06.2021'\n"

            return [False, response]
        else:
            beginDate = message[19]
            endDate = message[20]
            path = getDocPath(6)

            pathToFile = zayavlenieOPredostavleniiOtpuskaZaSvoiChetVSvyaziSRoshdeniemRebenka(path, userId, beginDate, endDate)

    elif (content.split()[0] == '6'):
        message = content.split()

        if len(message) !=  3:
            response = "Чтобы заполнить " + getDocName(6) + ", \n"
            response += "введите дату начала отпуска и дату окончания отпуска через пробел.\n"
            response += "Например, '6 02.06.2021 6.06.2021'\n"

            return [False, response]
        else:
            beginDate = message[1]
            endDate = message[2]
            path = getDocPath(6)

            pathToFile = zayavlenieOPredostavleniiOtpuskaZaSvoiChetVSvyaziSRoshdeniemRebenka(path, userId, beginDate, endDate)

    elif ("заявление о предоставлении работнику-донору двух дополнительных дней отдыха" in content.lower()):
        message = content.split()

        if len(message) !=  11:
            response = "Чтобы заполнить " + getDocName(5) + ", \n"
            response += "введите дату начала отпуска, дату окончания отпуска и дату выдачи справки о донорстве через пробел.\n"
            response += "Например, 'заявление о предоставлении работнику-донору двух дополнительных дней отдыха 05.06.2021 6.06.2021 04.06.2021'\n"

            return [False, response]
        else:
            beginDate = message[8]
            endDate = message[9]
            cerDate = message[10]
            path = getDocPath(5)

            pathToFile = zayavlenieOPredostavleniiRabotnikuDonoruDvuhDneiOtdiha(path, userId, beginDate, endDate, cerDate)

    elif (content.split()[0] == '5'):
        message = content.split()

        if len(message) !=  4:
            response = "Чтобы заполнить " + getDocName(5) + ", \n"
            response += "введите дату начала отпуска, дату окончания отпуска и дату выдачи справки о донорстве через пробел.\n"
            response += "Например, '5 05.06.2021 6.06.2021 04.06.2021'\n"

            return [False, response]
        else:
            beginDate = message[1]
            endDate = message[2]
            cerDate = message[3]
            path = getDocPath(5)

            pathToFile = zayavlenieOPredostavleniiRabotnikuDonoruDvuhDneiOtdiha(path, userId, beginDate, endDate, cerDate)

    elif ("заявление о согласии на работу в выходной день" in content.lower()):
        message = content.split()

        if len(message) !=  9:
            response = "Чтобы заполнить " + getDocName(9) + ", \n"
            response += "введите дату выходного дня.\n"
            response += "Например, 'заявление о согласии на работу в выходной день 6.06.2021'\n"

            return [False, response]
        else:
            date = message[8]
            path = getDocPath(9)

            pathToFile = zayavlenieOSoglasiiNaRabotuVVihodnoiDen(path, userId, date)

    elif (content.split()[0] == '9'):
        message = content.split()

        if len(message) !=  2:
            response = "Чтобы заполнить " + getDocName(9) + ", \n"
            response += "введите дату выходного дня.\n"
            response += "Например, '9 6.06.2021'\n"

            return [False, response]
        else:
            date = message[1]
            path = getDocPath(9)

            pathToFile = zayavlenieOSoglasiiNaRabotuVVihodnoiDen(path, userId, date)

    return [True, pathToFile]


def getOrganization():
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from CompanyInfo")
    companyInfo = dbCursor.fetchall()
    db.commit()
    dbCursor.close()
    
    organizationName = companyInfo[0][0]
    
    return organizationName


def getDirectorName():
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from CompanyInfo")
    companyInfo = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    lastName = companyInfo[0][1]
    firstName = companyInfo[0][2]
    middleName = companyInfo[0][3]
    gender = companyInfo[0][4]

    p = Petrovich()

    lastNameDative = ''
    firstNameDative = ''
    middleNameDative = ''

    if gender == 'male':
        lastNameDative = p.lastname(lastName, Case.DATIVE, Gender.MALE)
        firstNameDative = p.firstname(firstName, Case.DATIVE, Gender.MALE)
        middleNameDative = p.middlename(middleName, Case.DATIVE, Gender.MALE)
    elif gender == 'female':
        lastNameDative = p.lastname(lastName, Case.DATIVE, Gender.FEMALE)
        firstNameDative = p.firstname(firstName, Case.DATIVE, Gender.FEMALE)
        middleNameDative = p.middlename(middleName, Case.DATIVE, Gender.FEMALE)

    directorName = lastNameDative + ' ' + firstNameDative + ' ' + middleNameDative

    return directorName


def getEmployeeName(userId):
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from User WHERE UserId = '%s'" % userId)
    userInfo = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    lastName = userInfo[0][1]
    firstName = userInfo[0][2]
    middleName = userInfo[0][3]
    gender = userInfo[0][4]

    lastNameDative = ''
    firstNameDative = ''
    middleNameDative = ''

    # Создание экземпляра класса
    p = Petrovich()

    # Преобразование ФИО сотрудника в родительный падеж
    # Если пол сотрудника мужской
    if gender == 'male':
        # Склонение фамилии
        lastNameDative = p.lastname(lastName, Case.GENITIVE, Gender.MALE)
        # Склонение имени
        firstNameDative = p.firstname(firstName, Case.GENITIVE, Gender.MALE)
        # Склонение отчества
        middleNameDative = p.middlename(middleName, Case.GENITIVE, Gender.MALE)
    # Если пол сотрудника женский
    elif gender == 'female':
        lastNameDative = p.lastname(lastName, Case.GENITIVE, Gender.FEMALE)
        firstNameDative = p.firstname(firstName, Case.GENITIVE, Gender.FEMALE)
        middleNameDative = p.middlename(middleName, Case.GENITIVE, Gender.FEMALE)

    employeeName = lastNameDative + ' ' + firstNameDative + ' ' + middleNameDative

    return employeeName


def getEmployeeFIO(userId):
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from User WHERE UserId = '%s'" % userId)
    userInfo = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    lastName = userInfo[0][1]
    firstName = userInfo[0][2]
    middleName = userInfo[0][3]

    employeeFIO = lastName + ' ' + firstName[0] + '.' + middleName[0] + '.'

    return employeeFIO


def getEmployeeFullFIO(userId):
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from User WHERE UserId = '%s'" % userId)
    userInfo = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    lastName = userInfo[0][1]
    firstName = userInfo[0][2]
    middleName = userInfo[0][3]

    employeeFullFIO = lastName + ' ' + firstName + '.' + middleName

    return employeeFullFIO


def getTodayDate():
    day = str(datetime.now().day)
    month = str(datetime.now().month)
    year = str(datetime.now().year)

    date = day + '.' + month + '.' + year

    return date


def getDocPath(id):
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from Documents WHERE Id = '%s'" % id)
    docInfo = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    path = docInfo[0][2]

    return path


def getDocName(id):
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from Documents WHERE Id = '%s'" % id)
    docInfo = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    name = docInfo[0][1]

    return name


def getDocsListStr():
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from Documents")
    docs = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    docsStr = ''

    for doc in docs:
        docsStr += str(doc[0]) + '. ' + doc[1] + '\n'

    return docsStr


def getDocsList():
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from Documents")
    docs = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    return docs