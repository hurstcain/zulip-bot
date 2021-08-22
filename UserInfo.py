import sqlite3


db = sqlite3.connect("mydb.db")


def checkUserExistence(content):
    newContent = []

    for word in content:
        newContent.append(capitalizeTheFirstLetter(word))

    varCount = len(content)
    rightVarCount = 0
    surname = None
    firstName = None
    middleName = None

    for word in newContent:
        if checkSurname(word):
            rightVarCount += 1
            surname = word
        elif checkFirstName(word):
            rightVarCount += 1
            firstName = word
        elif checkMiddleName(word):
            rightVarCount += 1
            middleName = word

    if varCount == rightVarCount:
        return [surname, firstName, middleName]
    else:
        return None


def capitalizeTheFirstLetter(word):
    newWord = word[0].upper()
    newWord += word[1:]

    return newWord


def checkSurname(surname):
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from User WHERE Surname=:surname", 
                    {"surname": surname})
    userWithThisSurname = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    if not userWithThisSurname:
        return False
    else:
        return True


def checkFirstName(firstName):
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from User WHERE FirstName=:firstName", 
                    {"firstName": firstName})
    userWithThisFirstName = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    if not userWithThisFirstName:
        return False
    else:
        return True


def checkMiddleName(middleName):
    dbCursor = db.cursor()
    dbCursor.execute("SELECT * from User WHERE MiddleName=:middleName", 
                    {"middleName": middleName})
    userWithThisMiddleName = dbCursor.fetchall()
    db.commit()
    dbCursor.close()

    if not userWithThisMiddleName:
        return False
    else:
        return True


def getUserInfo(content):
    nameForSearch = checkUserExistence(content)

    message = ''

    if nameForSearch is not None:
        dbCursor = db.cursor()

        if nameForSearch[1] is None and nameForSearch[2] is None:
            dbCursor.execute("SELECT * from User WHERE Surname=:surname", 
            {"surname": nameForSearch[0]})
        elif nameForSearch[0] is None and nameForSearch[2] is None:
            dbCursor.execute("SELECT * from User WHERE FirstName=:firstName", 
            {"firstName": nameForSearch[1]})
        elif nameForSearch[0] is None and nameForSearch[1] is None:
            dbCursor.execute("SELECT * from User WHERE MiddleName=:middleName", 
            {"middleName": nameForSearch[2]})
        elif nameForSearch[2] is None:
            dbCursor.execute("SELECT * from User WHERE Surname=:surname and FirstName=:firstName", 
            {"surname": nameForSearch[0], "firstName": nameForSearch[1]})
        elif nameForSearch[1] is None:
            dbCursor.execute("SELECT * from User WHERE Surname=:surname and MiddleName=:middleName", 
            {"surname": nameForSearch[0], "middleName": nameForSearch[2]})
        elif nameForSearch[0] is None:
            dbCursor.execute("SELECT * from User WHERE FirstName=:firstName and MiddleName=:middleName", 
            {"firstName": nameForSearch[1], "middleName": nameForSearch[2]})
        else:
            dbCursor.execute("SELECT * from User WHERE WHERE Surname=:surname and FirstName=:firstName and MiddleName=:middleName", 
            {"surname": nameForSearch[0], "firstName": nameForSearch[1], "middleName": nameForSearch[2]})
        
        findUsers = dbCursor.fetchall()

        db.commit()
        dbCursor.close()

        message = 'Список найденных пользователей: \n'
        for user in findUsers:
            message += '```spoiler ' + user[1] + ' ' + user[2] + ' ' + user[3] + '\n'
            message += 'День рождения: ' + dateForm(user[7], user[8]) + '\n'
            message += 'Телефон: ' + user[6] + '\n'
            message += 'Email: ' + user[5] + '\n```\n'

    return message


def dateForm(day, month):
    date = ''
    
    if day < 9:
        date += '0' + str(day)
    else:
        date += str(day)
    
    date += '.'

    if month < 9:
        date += '0' + str(month)
    else:
        date += str(month)

    return date