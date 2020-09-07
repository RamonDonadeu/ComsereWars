import random
import os
# Global
INDEX = NAME = 0
WEAPON = PERCENTAGE = NUMBER = 1
NOMBREIDEAL = KNIGHTORDER = 2
WOUNDS = 3
IDEAL = 4
DAYACTION = 5
HABILITY = 6
KILLS = 7

today = ''

# ===============================================================
# Desc: Mira si quedan personajes que no han hecho su accion
# Input:
# Ouptut:
# ===============================================================


def allDayActions():
    files = open("Vivos", "r")
    next(files)
    for line in files:
        if(not(int(getValue(line.split(":")[0], "Vivos", DAYACTION)))):
            return False
    return True


# ===============================================================
# Desc: Comprueba si se puede hacer una accion
# Input:    Accion que se va a comprobar
# Ouptut:   True si se puede hacer la accion False si no.
# ===============================================================


def checkAction(actionNumber):
    line = getLine("ActionsCounter", int(actionNumber+3))
    name = line.split(":")[0]
    remaining = int(getValue(name, "ActionsCounter", PERCENTAGE))
    if(remaining):
        modifyLine(str(remaining-1), NUMBER, name, "ActionsCounter")
        modifyLine(str(int(getValue("Actions", "ActionsCounter", NUMBER))-1),
                   NUMBER, "Actions", "ActionsCounter")
    else:
        return False
    return True


# ===============================================================
# Desc: Comprueva si un numero esta por debajo de otro
# Input:
# Ouptut:
# ===============================================================


def checkPercentageResult(num, result):
    return result < int(num)


# ===============================================================
# Desc: Calcula un Porcentage y comprueba si es menor que el numero pasado por parametro
# Input:    num: Numero a superar
# Ouptut:   True or False
# ===============================================================


def checkPercentage(num):
    return random.randint(0, 99) < int(num)


# ===============================================================
# Desc: Mira si la persona pasada por parametro ha hecho su accion diaria
# Input:    name: Nombre de la persona
# Ouptut:   Valor del DAYACTION
# ===============================================================


def checkDayAction(name):
    return int(getValue(name, "Vivos", DAYACTION))


# ===============================================================
# Desc: Modifica el valor de Accion diaria a 0 de todos lo personajes
# Input:
# Ouptut:
# ===============================================================


def clearDayAction():
    files = open("Vivos", "r")
    next(files)
    for lines in files:
        modifyLine("0", DAYACTION, lines.split(":")[0], "Vivos")


# ===============================================================
# Desc: Prepara el archivo de Vivos
# Input:
# Ouptut:
# ===============================================================


def cleanDays():
    lineas = fileLengthy("Dias")
    while(lineas-1):
        lineas -= 1
        namefile = "Dia " + str(lineas)
        os.remove(namefile)

    file = open("Dias", "w")
    file.write("Dia 0")


# ===============================================================
# Desc: Modifica el valor de Accion diaria
# Input:    name: Nombre de la persona a la que se le aumentara el valor
# Ouptut:
# ===============================================================


def doDayAction(name):
    modifyLine("1", DAYACTION, name, "Vivos")


def daybackup():
    with open("Vivos") as f:
        with open("VivosBackup", "w") as f1:
            for line in f:
                f1.write(line)


def dailysetup():
    clearDayAction()
    with open("ActionsPerDay") as f:
        with open("ActionsCounter", "w") as f1:
            for line in f:
                f1.write(line)


# ===============================================================
# Desc: Calcula las acciones de cada personaje
# Input:
# Ouptut:
# ===============================================================


def dayActions():

    files = open("Vivos", "r")
    lineas = fileLengthy("Vivos")
    while(not(allDayActions()) and int(getValue("Actions", "ActionsCounter", NUMBER))):
        player = randomPlayer()
        if(not(checkDayAction(player))):
            doDayAction(player)
            day = open(today, "a+")
            day.write("\n========================== " +
                      player + " ==========================\n")
            actionDone = False
            while(not(actionDone) and not(allDayActions())):
                day = open(today, "a+")
                if(fileLengthy("Vivos")<4):
                    action=2
                else:
                    action = random.randint(0, 4)
                if action == 0:  # Arma
                    available = checkAction(action)
                    if(available):
                        day.write("----------- ACCION ARMA ----------- \n")
                        day.close()
                        findWeapon(player)
                        actionDone = True
                elif action == 1:  # Encuentro
                    available = checkAction(action)
                    if(available):
                        day.write("----------- ACCION ENCUENTRO -----------\n")
                        day.close()
                        player2 = findPlayer(player)
                        if(player2):
                            actionDone = True
                elif action == 2:  # Combate
                    available = checkAction(action)
                    if(available):
                        day.write("----------- ACCION COMBATE -----------\n")
                        day.close()
                        player2 = findPlayer(player)
                        if(player2):
                            if(not(getValue(player, "Vivos", KNIGHTORDER) == getValue(player2, "Vivos", KNIGHTORDER)) or fileLengthy("Vivos") < 17):
                                fight(player, player2)
                                actionDone = True
                elif action == 3:  # Huida
                    available = checkAction(action)
                    if(available):
                        day.write("----------- ACCION HUIR -----------\n")
                        day.close()
                        player2 = findPlayer(player)
                        if(player2):
                            if(not(getValue(player, "Vivos", KNIGHTORDER) == getValue(player2, "Vivos", KNIGHTORDER))):
                                scape(player, player2)
                                actionDone = True
                elif action == 4:  # Herido
                    available = checkAction(action)
                    if(available):
                        day.write("----------- ACCION HERIR -----------\n")
                        day.close()
                        player2 = findPlayer(player)
                        if(player2):
                            if(not(getValue(player, "Vivos", KNIGHTORDER) == getValue(player2, "Vivos", KNIGHTORDER))):
                                wound(player, player2)
                                actionDone = True
                if(not(actionDone)):
                    check=getLine("ActionsCounter", 2)
                    if(int(check.split(":")[1])==0):
                        actionDone=True

                day.close()


# ===============================================================
# Desc: Dos personajes luchan entre si y uno sale victorioso mientras otro muere
# Input:    player1: Nombre del primer participante
#           player2: Nombre del segudno participante
# Ouptut:
# ===============================================================


def fight(player1, player2):
    saved = False
    day = open(today, "a+")
    day.write(player1 + " pelea contra " + player2 + "\n")
    day.close()
    if (getValue(player2, "Vivos", KNIGHTORDER) == "Windrunner"):
        day = open(today, "a+")
        aux = player2
        player2 = findWindrunner(player2)
        if (not(aux == player2)):
            day.write("Cuando " + aux+" iba a ser atacado, aparece " +
                      player2 + " para proteger a su compañero Corredor del Viento\n")
            day.close()

    if (getValue(player1, "Vivos", KNIGHTORDER) == "Elsecaller"):
        day = open(today, "a+")
        if(getValue(player1, "Vivos", WEAPON) == ""):
            day.write(player1 + " va a moldear una espada:\n")
            day.close()
            modifyLine("Espada", WEAPON, player1, "Vivos")

    if (getValue(player2, "Vivos", KNIGHTORDER) == "Elsecaller"):
        day = open(today, "a+")
        if(getValue(player2, "Vivos", WEAPON) == ""):
            day.write(player2 + " va a moldear una espada:\n")
            day.close()
            modifyLine("Espada", WEAPON, player2, "Vivos")

    if (getValue(player1, "Vivos", KNIGHTORDER) == "Stoneward"):
        if(not(getValue(player2, "Vivos", WEAPON) == "Espada Esquirlada")):
            day = open(today, "a+")
            modifyLine("", WEAPON, player2, "Vivos")
            day.write(player1+" ha destruido el arma a "+player2+"\n")
            day.close()

    if (getValue(player2, "Vivos", KNIGHTORDER) == "Stoneward"):
        if(not(getValue(player1, "Vivos", WEAPON) == "Espada Esquirlada")):
            day = open(today, "a+")
            modifyLine("", WEAPON, player1, "Vivos")
            day.write(player2+" ha destruido el arma a "+player1+"\n")
            day.close()

    if (getValue(player1, "Vivos", KNIGHTORDER) == "Bondsmith"):
        if(not(getValue(player2, "Vivos", WEAPON) == "Espada Esquirlada")):
            day = open(today, "a+")
            arma = getValue(player2, "Vivos", WEAPON)
            if(not(arma == "")):
                if(getLineNumber(arma, "PorcentajesArmas") < getLineNumber(getValue(player1, "Vivos", WEAPON), "PorcentajesArmas") or getValue(player1, "Vivos", WEAPON) == ""):
                    modifyLine(arma, WEAPON, player1, "Vivos")
                modifyLine("", WEAPON, player2, "Vivos")
                day.write(player1+" ha robado el arma (" +
                          arma+") a "+player2+"\n")
            day.close()

    if (getValue(player2, "Vivos", KNIGHTORDER) == "Bondsmith"):
        if(not(getValue(player1, "Vivos", WEAPON) == "Espada Esquirlada")):
            day = open(today, "a+")
            arma = getValue(player1, "Vivos", WEAPON)
            if(not(arma == "")):
                if(getLineNumber(arma, "PorcentajesArmas") < getLineNumber(getValue(player2, "Vivos", WEAPON), "PorcentajesArmas") or getValue(player2, "Vivos", WEAPON) == ""):
                    modifyLine(arma, WEAPON, player2, "Vivos")
                modifyLine("", WEAPON, player1, "Vivos")
                day.write(player2+" ha robado el arma (" +
                          arma+") a "+player1+"\n")
            day.close()

    winner = getWinner(player1, player2, "Kill")
    day = open(today, "a+")
    if(winner == player1):
        if ((getValue(player2, "Vivos", KNIGHTORDER) == "Edgedancer" and not(int(getValue(player2, "Vivos", HABILITY)))) or (getValue(player2, "Vivos", KNIGHTORDER) == "Dustbringer" and not(int(getValue(player2, "Vivos", HABILITY))))):
            if (checkPercentage(30)):
                day.write("Antes de morir, "+player2 +
                          " escapa con la habilidad de friccion")
                modifyLine("1", HABILITY, player2, "Vivos")
                saved = True
        if(not(saved)):
            day.write(player1 + " ha matado a " + player2 + "\n")
            loot = lootPlayer(player1, player2)
            if(loot):
                day.write(player1 + " ha cogido el arma ( " + getValue(player1,
                                                                       "Vivos", WEAPON) + " ) a " + player2 + "\n")
            printDead(player2)
            killPlayer(player2)
            day.close()
            sayIdeal(player1)
            modifyLine(str(int(getValue(player1, "Vivos", KILLS))+1),
                       KILLS, player1, "Vivos")
        if(fileLengthy("Vivos") > 2):
            if (getValue(player1, "Vivos", KNIGHTORDER) == "Dustbringer"):
                if(checkPercentage(10)):
                    day = open(today, "a+")
                    day.write("Debido al poder de abrasion, " +
                              player1+" se ha matado a si mismo\n")
                    printDead(player1)
                    killPlayer(player1)
                    
            if (getValue(player1, "Vivos", KNIGHTORDER) == "Skybreaker"):
                if(checkPercentage(5)):
                    day = open(today, "a+")
                    day.write("Debido al poder de abrasion, " +
                              player1+" se ha matado a si mismo\n")
                    printDead(player1)
                    killPlayer(player1)

    if(winner == player2):
        if ((getValue(player1, "Vivos", KNIGHTORDER) == "Edgedancer" and not(int(getValue(player1, "Vivos", HABILITY)))) or (getValue(player1, "Vivos", KNIGHTORDER) == "Dustbringer" and not(int(getValue(player1, "Vivos", HABILITY))))):
            if (checkPercentage(30)):
                day.write("Antes de morir, "+player1 +
                          " escapa con la habilidad de friccion")
                modifyLine("1", HABILITY, player1, "Vivos")
                saved = True
        if(not(saved)):
            day.write(player2 + " ha matado a " + player1 + "\n")
            loot = lootPlayer(player2, player1)
            if(loot):
                day.write(player2 + " ha cogido el arma ( " + getValue(player2,
                                                                       "Vivos", WEAPON) + " ) a " + player1 + "\n")
            printDead(player1)
            killPlayer(player1)
            day.close()
            sayIdeal(player2)
            modifyLine(str(int(getValue(player2, "Vivos", KILLS))+1),
                       KILLS, player2, "Vivos")
        if(fileLengthy("Vivos") > 2):
            if (getValue(player2, "Vivos", KNIGHTORDER) == "Dustbringer"):
                if(checkPercentage(10)):
                    day = open(today, "a+")
                    day.write("Debido al poder de abrasion, " +
                              player2+" se ha matado a si mismo\n")
                    killPlayer(player2)
            if (getValue(player2, "Vivos", KNIGHTORDER) == "Skybreaker"):
                if(checkPercentage(5)):
                    day = open(today, "a+")
                    day.write("Debido al poder de abrasion, " +
                              player2+" se ha matado a si mismo\n")
                    killPlayer(player2)

# ===============================================================
# Desc: Devuelve el numero de lineas de un archivo
# Input:    fname: Nombre del archivo
# Ouptut:   Numero de lineas
# ===============================================================


def fileLengthy(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


# ===============================================================
# Desc: Un personaje busca un arma y se le añade al inventario
# Input: name: Nombre de la persona que busca un arma
# Ouptut:
# ===============================================================


def findWeapon(name):
    file = open('Vivos', 'a')
    if(today):
        day = open(today, "a+")
    betterWeapon = True
    getWeapon = False
    while(not(getWeapon)):  # Mientras no se consiga un arma
        armas = open('PorcentajesArmas', 'r')  # Abrir fichero de Armas
        next(armas)
        for line in armas:
            if(getValue(name, "Vivos", WEAPON) == getName(line)):
                betterWeapon = False
                getWeapon = True
            if (betterWeapon):
                value = random.randint(0, 99)
                # Si conseguimos el porcentaje del arma
                if((value < int(line.split(':')[1])) and not(getWeapon)):
                    modifyLine(getName(line), WEAPON, name, "Vivos")
                    if(today):
                        day.write(name + " ha encontrado " +
                                  line.split(":")[2] + "\n")
                    getWeapon = True

        armas.close()
    if(not(betterWeapon)):
        day.write(name + " no ha encontrado un arma mejor que la suya\n")
    file.close()
    if(today):
        day.close()


# ===============================================================
# Desc: Genera un encuentro entre dos personas
# Input:    name: Nombre de la persona que busca a otra
# Ouptut:
# ===============================================================


def findPlayer(name):
    day = open(today, "a+")
    while(not(allDayActions())):
        player = randomPlayer()
        if(not(checkDayAction(player))):
            while(player == name):
                player = randomPlayer()
            doDayAction(player)
            day.write(name + " se ha encontrado con " + player + "\n")
            day.close()
            return player


def findWindrunner(name):
    files = open("Vivos", "r")
    next(files)
    for lines in files:
        line = lines.split(":")
        if(line[KNIGHTORDER] == "Windrunner" and not(int(line[DAYACTION]))):
            modifyLine("1", DAYACTION, line[NAME], "Vivos")
            return line[NAME]
    return name

# ===============================================================
# Desc: Genera un archivo para un dia
# Input:
# Ouptut: Nombre del archivo
# ===============================================================


def generateDay():
    # Limpiar dayActions?
    days = open("Dias", "r")
    dayNumber = 0
    for line in days:
        dayNumber = line.split(' ')[1]
    if(not(int(dayNumber))):
        dayNumber = 1
    else:
        dayNumber = int(dayNumber)+1
    newDayName = "Dia " + str(dayNumber)
    newDayName
    days.close()
    days = open("Dias", "a")
    days.write("\n"+newDayName)
    days.close()
    days = open(newDayName, "w")
    days.write("========================== Inicio " +
               newDayName + " ==========================\n")
    days.close()
    return newDayName


# ===============================================================
# Desc: Dos participantes luchan, solo uno puede quedar vivo.
# Input:    player1: Nombre del primer participante
#           player2: Nombre del segudno participante
# Ouptut:
# ===============================================================


def getWinner(player1, player2, action):
    # Ataque sigiloso
    day = open(today, "a+")
    deadPlayer = False
    while(not(deadPlayer)):
        player1Bonus = getBonus(player1, action)
        player2Bonus = getBonus(player2, action)
        result1 = checkPercentage(player1Bonus)
        result2 = checkPercentage(player2Bonus)
        day.write(player1 + ": " + str(player1Bonus) +
                  "% Success: "+str(result1) + "\n")
        day.write(player2 + ": " + str(player2Bonus) +
                  "% Success: "+str(result2)+"\n")
        if (result1 and not(result2)):
            return(player1)
            deadPlayer = True
        if (result2 and not(result1)):
            return(player2)
            deadPlayer = True
    day.close()


# ===============================================================
# Desc: Calcula el bonus de combate de un participante
# Input:    name: Nombre del participante
# Ouptut:   total: Suma total del bonus del participante
# ===============================================================


def getBonus(name, action):
    total = 50
    linea = getLine("Vivos", getLineNumber(name, "Vivos"))
    linea = linea.split(":")
    order = getValue(name, "Vivos", KNIGHTORDER)
    if (action == "Kill" or action == "Wound"):
        for value in linea:
            add = getValue(value, "Combate", PERCENTAGE)
            try:
                add = int(add)
                total += add
            except:
                add = 0
        if (order == "Windrunner"):
            total += 10
        elif (order == "Stoneward"):
            total += 5
        elif(order == "Willshaper"):
            total += 10
        elif(order == "Skybreaker"):
            total += 10
        elif (order == "Dustbringer"):
            total += 7
        elif (order == "Lightweaver"):
            total += 5
    elif (action == "Scape"):
        if (order == "Lightweaver"):
            total += 20
        if (order == "Truthwatcher"):
            total += 10
    return total


# ===============================================================
# Desc: Da el un valor concreto de una linea
# Input:    index: indice de la linea
#           filename: Nombre del archivo
#           value: Valor que queremos obtener
# Ouptut:   Valor que queremos obtener
# ===============================================================


def getValue(index, fileName, value):
    files = open(fileName, "r")
    next(files)
    for line in files:
        if(line.split(":")[INDEX] == index):
            return line.split(":")[value]


# ===============================================================
# Desc: Busca el porcentaje necesario para X accion y nos indica si es superado
# Input:    index: Valor del porcentage que buscaremos
#           archivo: Archivo en el que buscaremos
# Ouptut: Boolean
# ===============================================================


def getAndCheckPercentage(index, file_name):
    files = open(file_name, "r")  # Abrimos el archivo
    porcentaje = 0
    next(files)  # Saltamos la linea de descripcion
    for line in files:  # Buscamos el indice en el archivo
        if((line.split(':')[0]) == index):  # Si es igual
            porcentaje = line.split(':')[1]  # Cogemos el percentaje
            files.close()
            return random.uniform(0, 99) < int(porcentaje)
    # Cerramos el archivo
    # Calculamos si se consigue el porcentaje


# ===============================================================
# Desc: Busca el porcentaje necesario para X accion y lo devuelve
# Input:    index: Valor del porcentage que buscaremos
#           archivo: Archivo en el que buscaremos
# Ouptut: Valor del porcentaje que queremos
# ===============================================================


def getPorcentaje(index, file_name):
    files = open(file_name, "r")  # Abrimos el archivo
    porcentaje = 0
    next(files)  # Saltamos la linea de descripcion
    for line in files:  # Buscamos el indice en el archivo
        if((line.split(':')[0]) == index):  # Si es igual
            porcentaje = line.split(':')[1]  # Cogemos el percentaje
    files.close()  # Cerramos el archivo
    return porcentaje  # Devolvemos el Porcentaje


# ===============================================================
# Desc: Busca el numero de linia que contiene el indice indicado
# Input:    index: Valor que buscaremos
#           archivo: Archivo en el que buscaremos
# Ouptut: Numero de linia
# ===============================================================


def getLineNumber(index, file_name):
    files = open(file_name, "r")  # Abrimos el archivo
    aux = 1
    linea = 0
    next(files)  # Saltamos la linea de descripcion
    for line in files:  # Buscamos el indice en el archivo
        aux += 1
        if((line.split(':')[0]) == index):  # Si es igual
            linea = aux  # Cogemos el percentaje
    files.close()  # Cerramos el archivo
    return int(linea)  # Devolvemos la linea


# ===============================================================
# Desc: Busca el porcentaje necesario para X accion y nos devuelve si se cumple o no
# Input:    file_name: Nombre del fichero que modificaremos
#           line_num: Linea que modificaremos
# Ouptut: Texto de la linia especifica
# ===============================================================


def getLine(file_name, line_num):
    lines = open(file_name, 'r').readlines()
    return lines[line_num-1]


# ===============================================================
# Desc: Calcula un numero del 0 al 99
# Input:    Numero del 0 al 99
# Ouptut:
# ===============================================================


def getPercentageResult():
    return random.randint(0, 99)


# ===============================================================
# Desc: Devuelve el indice de una linea
# Input:    line: Linea de la que sacaremos el indice
# Ouptut:   indice de la linea
# ===============================================================


def getName(line):
    return line.split(":")[0]


# ===============================================================
# Desc: Borra un jugador del archivo "Vivos", lo añade a "Muertos"
# Input:    player: Nombre del jugador
# Ouptut:
# ===============================================================


def killPlayer(player):
    files = open("Vivos", "a")
    files.close()
    files = open("Vivos", "r")
    dead = False
    for lines in files:
        line = getLineNumber(getName(lines), "Vivos")
        if(line != fileLengthy("Vivos")):
            if(player == getName(lines)):
                dead = True
            if(dead):
                newline = getLine("Vivos", line+1)
                if(line == fileLengthy("Vivos")-1):
                    newline = newline+"\n"
                replaceLine("Vivos", line, newline)
    removeLastLine("Vivos")


# ===============================================================
# Desc: Despues de una pelea, un personaje lootea al muerto
# Input:    alive: Personaje vivo
#           dead: Personaje Muerto
# Ouptut:   Boolean que indica si el vivo le ha cogido el arma al muerto
# ===============================================================


def lootPlayer(alive, dead):
    armas = open("PorcentajesArmas", "r")
    arma1 = getValue(alive, "Vivos", WEAPON)
    arma2 = getValue(dead, "Vivos", WEAPON)
    betterWeapon = False
    newWeapon = False
    for lines in armas:
        if(getName(lines) == arma1):
            betterWeapon = True
        if (getName(lines) == arma2 and not(betterWeapon)):
            arma1 = arma2
            newWeapon = True
            modifyLine(arma2, WEAPON, alive, "Vivos")

    return newWeapon


# ===============================================================
# Desc: Modifica un valor de una linea
# Input:    text: Texto que añadiremos
#           position: Posicion en la que añadiriamos el texto
#           name: Nombre de la persona a la que añadiremos ese valor
# Ouptut:
# ===============================================================


def modifyLine(text, position, name, file_name):
    modify = getLine(file_name, getLineNumber(
        name, file_name))  # Buscamos la linea de la persona
    modify = modify.split(":")  # La separamos
    modify[position] = text  # Escribimos en el arma
    separator = ":"
    modify = separator.join(modify)  # Juntamos el vector
    # Modificamos la linea
    replaceLine(file_name, getLineNumber(name, file_name), modify)


# ===============================================================
# Desc: Imprime el nombre de algun participante que ha muerto en el archivo "Muertos"
# Input:    name: Nombre del participante muerto
# Ouptut:
# ===============================================================


def printDead(name):
    file = open("Muertos", "a")
    file.write(getLine("Vivos", getLineNumber(name, "Vivos")))
    file.close()


# ===============================================================
# Desc: Elimina la ultima linea de un archivo
# Input:    fileName: nombre del archivo
# Ouptut:
# ===============================================================


def removeLastLine(fileName):
    fd = open(fileName, "r")
    d = fd.read()
    fd.close()
    m = d.split("\n")
    s = "\n".join(m[:-1])
    fd = open(fileName, "w+")
    for i in range(len(s)):
        fd.write(s[i])
    fd.close()


# ===============================================================
# Desc: Reemplaza una linea concreta con el texto pasado por parametro
# Input:    file_name: Nombre del fichero que modificaremos
#           line_num: Linea que modificaremos
#           text: Texto que añadiremos
# Ouptut:
# ===============================================================


def replaceLine(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num-1] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


# ===============================================================
# Desc: Escoge un jugador aleatorio
# Input:
# Ouptut:   Nombre de un jugador
# ===============================================================


def randomPlayer():
    line = getLine("Vivos", random.randint(2, fileLengthy("Vivos")))
    return line.split(":")[0]


# ===============================================================
# Desc: Dos personajes luchan entre si y uno huye
# Input:    player1: Nombre del primer participante
#           player2: Nombre del segudno participante
# Ouptut:
# ===============================================================


def scape(player1, player2):
    day = open(today, "a+")
    day.write(player1 + " pelea contra " + player2 + "\n")
    day.close()
    winner = getWinner(player1, player2, "Scape")
    day = open(today, "a+")
    if(winner == player1):
        day.write(player2 + " ha huido de " + player1 + "\n")
        if(not(getValue(player2, "Vivos", WEAPON) == "")):
            day.write(player2 + " pierde el arma " +
                      getValue(player2, "Vivos", WEAPON)+"\n")
            new = lootPlayer(player1, player2)
            if(new):
                day.write(" y " + player1+" la coje\n")
            modifyLine("", WEAPON, player2, "Vivos")
        day.close()

    if(winner == player2):
        day.write(player1 + " ha huido de " + player2 + "\n")
        if(not(getValue(player1, "Vivos", WEAPON) == "")):
            day.write(player1 + "pierde el arma " +
                      getValue(player1, "Vivos", WEAPON))
            new = lootPlayer(player2, player1)
            if(new):
                day.write(" y " + player2+" la coje\n")
            modifyLine("", WEAPON, player1, "Vivos")
        day.close()


def setup():
    file = open('Vivos', 'w')
    file.write(
        "Name:Weapon:KnighOrder:Wounds:Ideal:DayAction:Hability:Kills:\n")
    participantes = open("participantes", "r")
    for line in participantes:
        file.write(line.split(",")[0]+"::" + line.split(",")
                   [1]+"::Primer Ideal:"+str(0)+":"+str(0)+":"+str(0)+":\n")
    participantes.close()
    file.close()
    file = open("Muertos", "w")
    file.write(
        "========================= Participantes Muertos =========================\n")
    file.close()
    removeLastLine("Vivos")
    file = open("vivos", "r")
    for lines in file:
        if(lines.split(":")[KNIGHTORDER] == "Lightweaver"):
            findWeapon(lines.split(":")[NAME])
    file.close()


# ===============================================================
# Desc: Genera un archivo para un dia
# Input:
# Ouptut: Nombre del archivo
# ===============================================================


def sayIdeal(name):
    ideal = getValue(name, "Vivos", IDEAL)
    if(ideal != "Quinto Ideal"):
        ideal = getLineNumber(str(ideal), "Ideales")
        ideal = getName(getLine("Ideales", int(ideal+1)))
        if (getAndCheckPercentage(ideal, "Ideales")):
            days = open(today, "a")
            days.write(name + " ha pronunciado " +
                       getValue(ideal, "Ideales", NOMBREIDEAL) + "\n")
            if (ideal == "Tercer Ideal"):
                days.write(
                    "Al llegar al Tercer Ideal ha conseguido una Espada Esquirlada")
                modifyLine("Espada Esquirlada", WEAPON, name, "Vivos")
            days.close()
            modifyLine(getValue(ideal, "Ideales", NOMBREIDEAL),
                       IDEAL, name, "Vivos")


# ===============================================================
# Desc: Dos personajes luchan entre si y uno sale herido
# Input:    player1: Nombre del primer participante
#           player2: Nombre del segudno participante
# Ouptut:
# ===============================================================


def wound(player1, player2):
    day = open(today, "a+")
    day.write(player1 + " pelea contra " + player2 + "\n")
    day.close()
    winner = getWinner(player1, player2, "Wound")
    day = open(today, "a+")

    if(winner == player1):
        if (getValue(player2, "Vivos", KNIGHTORDER) == "Edgedancer" or getValue(player2, "Vivos", KNIGHTORDER) == "Trutwatcher"):
            if(checkPercentage(50)):
                day.write(player1 + " ha sido levemente heirdo por " + player2 +
                          " pero se ha curado gracias a la potencia de Progresion\n")
            else:
                modifyLine("leves", WOUNDS, player2, "Vivos")
                day.write(player1 + " ha sido gravemente heirdo por " + player2 +
                          " pero se ha curado a leve gracias a la potencia de Progresion\n")
        else:
            if(checkPercentage(50)):
                modifyLine("leves", WOUNDS, player2, "Vivos")
            else:
                modifyLine("graves", WOUNDS, player2, "Vivos")
            day.write(player2 + " ha sido heirdo por " + player1 + "\n")
        day.close()

    if(winner == player2):
        if (getValue(player1, "Vivos", KNIGHTORDER) == "Edgedancer" or getValue(player1, "Vivos", KNIGHTORDER) == "Trutwatcher"):
            if(checkPercentage(50)):
                day.write(player1 + " ha sido levemente heirdo por " + player2 +
                          " pero se ha curado gracias a la potencia de Progresion\n")
            else:
                modifyLine("leves", WOUNDS, player1, "Vivos")
                day.write(player1 + " ha sido gravemente heirdo por " + player2 +
                          " pero se ha curado a leve gracias a la potencia de Progresion\n")
        else:
            if(checkPercentage(50)):
                modifyLine("leves", WOUNDS, player1, "Vivos")
            else:
                modifyLine("graves", WOUNDS, player1, "Vivos")
            day.write(player1 + " ha sido heirdo por " + player2 + "\n")
        day.close()


if __name__ == '__main__':
    option = 1
    while(option):
        print("------------ Selecciona una opcion ------------\n 1.- Setup inicial \n 2.- Ejecutar dia \n 3.- Restablecer dia anterior\n 4.- Modificar datos\n 5.- Simulaciuon\n 0.- Salir")
        option = int(input())
        if(option == 1):
            seguro = 0
            while(not(seguro == ("S")) and not(seguro == ("N"))):
                print(
                    "Seleccionar esta opcion borrara todos los dias y el progreso actual\nEstas seguro que quieres eliminarlo (S/N)")
                seguro = input()
                if(seguro == "S"):
                    setup()
                    cleanDays()
                else:
                    if(not(seguro == "N")):
                        print("Opcion incorrecta\n")
        elif (option == 2):
            daybackup()
            dailysetup()
            today = generateDay()
            dayActions()
        elif (option == 3):
            fd = open("Dias", "r")
            d = fd.read()
            fd.close()
            m = d.split("\n")
            lastday = m[len(m)-1]
            os.remove(lastday)
            removeLastLine("Dias")
            with open("VivosBackup") as f:
                with open("Vivos", "w") as f1:
                    for line in f:
                        f1.write(line)
        elif (option == 4):
            print("Hola")

        elif (option == 5):
            WR = 0
            SB = 0
            DB = 0
            ED = 0
            TW = 0
            LW = 0
            EC = 0
            WS = 0
            SW = 0
            BS = 0
            winners = open("Winners", "a")
            stats = open("stats", "w")
            print("Cuantas simulaciones quieres hacer?\n")
            sim = int(input())
            while (sim):
                sim -= 1
                setup()
                cleanDays()
                while(fileLengthy("Vivos") > 2):
                    dailysetup()
                    today = generateDay()
                    dayActions()
                winner = getLine("Vivos", 2)
                winner = winner.split(":")
                winners.write(getLine("Vivos", 2)+"\n")
                if(winner[KNIGHTORDER] == "Windrunner"):
                    WR += 1
                    print("Windrunners: "+str(WR)+"\n")
                if(winner[KNIGHTORDER] == "Skybreaker"):
                    SB += 1
                    print("Skybreakers: "+str(SB)+"\n")
                if(winner[KNIGHTORDER] == "Dustbringer"):
                    DB += 1
                    print("Dustbringers: "+str(DB)+"\n")
                if(winner[KNIGHTORDER] == "Edgedancer"):
                    ED += 1
                    print("Edgedancers: "+str(ED)+"\n")
                if(winner[KNIGHTORDER] == "Truthwatcher"):
                    TW += 1
                    print("Truthwatchers: "+str(TW)+"\n")
                if(winner[KNIGHTORDER] == "Lightweaver"):
                    LW += 1
                    print("Lightweavers: "+str(LW)+"\n")
                if(winner[KNIGHTORDER] == "Elsecaller"):
                    EC += 1
                    print("Elsecallers: "+str(EC)+"\n")
                if(winner[KNIGHTORDER] == "Willshaper"):
                    WS += 1
                    print("Willshapers: "+str(WS)+"\n")
                if(winner[KNIGHTORDER] == "Stoneward"):
                    SW += 1
                    print("Stonewards: "+str(SW)+"\n")
                if(winner[KNIGHTORDER] == "Bondsmith"):
                    BS += 1
                    print("Bondsmiths: "+str(BS)+"\n")

                print(sim)

            print("================= RESULTS =================\n")
            print("Windrunners: "+str(WR)+"\n")
            print("Skybreakers: "+str(SB)+"\n")
            print("Dustbringers: "+str(DB)+"\n")
            print("Edgedancers: "+str(ED)+"\n")
            print("Truthwatchers: "+str(TW)+"\n")
            print("Lightweavers: "+str(LW)+"\n")
            print("Elsecallers: "+str(EC)+"\n")
            print("Willshapers: "+str(WS)+"\n")
            print("Stonewards: "+str(SW)+"\n")
            print("Bondsmiths: "+str(BS)+"\n")

            winners.close()
