import random
# Global
INDEX = NAME = 0
WEAPON = PERCENTAGE = 1
ARMOR = NOMBREIDEAL = 2
KNIGHTORDER = 3
WOUNDS = 4
IDEAL = 5
DAYACTION = 6
CS = 7
DS = 8

today = ''


def getBonus(name):
    # ===============================================================
    # Desc: Calcula el bonus de combate de un participante
    # Input:    name: Nombre del participante
    # Ouptut:   total: Suma total del bonus del participante
    # ===============================================================
    total = 50
    linea = getLine("Vivos", getLineNumber(name, "Vivos"))
    linea = linea.split(":")
    for value in linea:
        add = getValue(value, "Combate", PERCENTAGE)
        try:
            add = int(add)
            total += add
        except:
            add = 0

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
# Desc: Comprueva si un numero esta por debajo de otro
# Input:
# Ouptut:
# ===============================================================


def checkPercentageResult(num, result):
    return result < int(num)

# ===============================================================
# Desc: Devuelve el indice de una linea
# Input:    line: Linea de la que sacaremos el indice
# Ouptut:   indice de la linea
# ===============================================================


def getName(line):
    return line.split(":")[0]
# ===============================================================
# Desc: Modifica el valor de Accion diaria
# Input:    name: Nombre de la persona a la que se le aumentara el valor
# Ouptut:
# ===============================================================


def doDayAction(name):
    modifyLine("1", DAYACTION, name)

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
# Desc: Escoge un jugador aleatorio
# Input:
# Ouptut:   Nombre de un jugador
# ===============================================================


def randomPlayer():
    line = getLine("Vivos", random.randint(2, fileLengthy("Vivos")))
    return line.split(":")[0]


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
# Desc: Calcula si dos personajes luchan entre si.
# Input:    player1: Nombre del primer participante
#           player2: Nombre del segudno participante
# Ouptut:
# ===============================================================


def fight(player1, player2):
    day = open(today, "a+")
    if(getAndCheckPercentage("combatir", "Porcentajes")):
        day.write(player1 + " pelea contra " + player2 + "\n")
        day.close()
        attack(player1, player2)


# ===============================================================
# Desc: Modifica el valor de Accion diaria a 0 de todos lo personajes
# Input:
# Ouptut:
# ===============================================================


def clearDayAction():
    files = open("Vivos", "r")
    next(files)
    for lines in files:
        modifyLine("0", DAYACTION, lines.split(":")[0])


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
# Desc: Modifica un valor de una linea
# Input:    text: Texto que añadiremos
#           position: Posicion en la que añadiriamos el texto
#           name: Nombre de la persona a la que añadiremos ese valor
# Ouptut:
# ===============================================================


def modifyLine(text, position, name):
    modify = getLine("Vivos", getLineNumber(
        name, "Vivos"))  # Buscamos la linea de la persona
    modify = modify.split(":")  # La separamos
    modify[position] = text  # Escribimos en el arma
    separator = ":"
    modify = separator.join(modify)  # Juntamos el vector
    # Modificamos la linea
    replaceLine("Vivos", getLineNumber(name, "Vivos"), modify)

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
# Desc: Un personaje busca un arma y se le añade al inventario
# Input: name: Nombre de la persona que busca un arma
# Ouptut:
# ===============================================================


def findWeapon(name):
    file = open('Vivos', 'a')
    day = open(today, "a+")
    betterWeapon = True
    if(getAndCheckPercentage("conseguirArma", "Porcentajes")):  # LLamar a aplicarPorcentaje
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
                        modifyLine(getName(line), WEAPON, name)
                        day.write(name + " ha encontrado " +
                                  line.split(":")[2] + "\n")
                        getWeapon = True
            armas.close()
    file.close()
    day.close()

# ===============================================================
# Desc: Genera un encuentro entre dos personas
# Input:    name: Nombre de la persona que busca a otra
# Ouptut:
# ===============================================================


def findPlayer(name):
    day = open(today, "a+")
    while(not(allDayActions()) and getAndCheckPercentage("encontrarPersona", "Porcentajes")):
        player = randomPlayer()
        if(not(checkDayAction(player))):
            while(player == name):
                player = randomPlayer()
            # Arma? DailyAction?
            doDayAction(player)
            day.write(name + " se ha encontrado con " + player + "\n")
            day.close()
            return player
    day.write(name + " no ha encontrado a nadie \n")

# ===============================================================
# Desc: Prepara el archivo de Vivos
# Input:
# Ouptut:
# ===============================================================


def setup():
    file = open('Vivos', 'w')
    file.write(
        "Name:Weapon:Armor:KnighOrder:Wounds:Ideal:DayAction:ChargedSpheres:DischargedSpheres:\n")

    participantes = open("participantes", "r")
    for line in participantes:
        file.write(line.split(":")[0]+":::::"+str(0)+":"+str(0)+":" + str(random.randint(1, 2)) +
                   ":"+str(random.randint(1, 3))+":\n")
    participantes.close()
    file.close()
    file = open("Muertos", "w")
    file.write(
        "========================= Participantes Muertos =========================\n")
    file.close()
    removeLastLine("Vivos")

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
            days.close()
            modifyLine(getValue(ideal, "Ideales", NOMBREIDEAL), IDEAL, name)

# ===============================================================
# Desc: Genera un archivo para un dia
# Input:
# Ouptut: Nombre del archivo
# ===============================================================


def generateDay():
    # Limpiar dayActions?
    days = open("Dias", "r")
    dayNumber = 0
    print(days)
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
            modifyLine(arma2, WEAPON, alive)
    add = int(getValue(alive, "Vivos", CS)) + int(getValue(dead, "Vivos", CS))
    modifyLine(str(add), CS, alive)
    add = int(getValue(alive, "Vivos", DS)) + int(getValue(dead, "Vivos", DS))
    modifyLine(str(add), DS, alive)

    return newWeapon

# ===============================================================
# Desc: Dos participantes luchan, solo uno puede quedar vivo.
# Input:    player1: Nombre del primer participante
#           player2: Nombre del segudno participante
# Ouptut:
# ===============================================================


def attack(player1, player2):
    # Ataque sigiloso
    day = open(today, "a+")
    deadPlayer = False
    while(not(deadPlayer)):
        player1Bonus = getBonus(player1)
        player2Bonus = getBonus(player2)
        result1 = checkPercentage(player1Bonus)
        result2 = checkPercentage(player2Bonus)
        day.write(player1 + ": " + str(player1Bonus) +
                  "% Success: "+str(result1) + "\n")
        day.write(player2 + ": " + str(player2Bonus) +
                  "% Success: "+str(result2)+"\n")
        if (result1 and not(result2)):
            day.write(player1 + " ha matado a " + player2 + "\n")
            loot = lootPlayer(player1, player2)
            if(loot):
                day.write(player1 + " ha cogido el arma ( " + getValue(player1,
                                                                       "Vivos", WEAPON) + " ) y las esferas a " + player2 + "\n")
            printDead(player2)
            killPlayer(player2)
            deadPlayer = True
        if (result2 and not(result1)):
            day.write(player2 + " ha matado a " + player1 + "\n")
            loot = lootPlayer(player2, player1)
            if(loot):
                day.write(player2 + " ha cogido el arma ( " + getValue(player2,
                                                                       "Vivos", WEAPON) + " ) y las esferas a " + player1 + "\n")
            printDead(player1)
            killPlayer(player1)
            deadPlayer = True
    day.close()


# ===============================================================
# Desc: Calcula las acciones de cada personaje
# Input:
# Ouptut:
# ===============================================================


def dayActions():
    files = open("Vivos", "r")
    lineas = fileLengthy("Vivos")
    while(not(allDayActions())):
        player = randomPlayer()
        if(not(checkDayAction(player))):
            doDayAction(player)
            day = open(today, "a+")
            day.write("\n========================== " +
                      player + " ==========================\n")
            day.close()
            sayIdeal(player)
            findWeapon(player)
            player2 = findPlayer(player)
            if(player2):
                fight(player, player2)

# def combate(nombre1, nombre2):
    # if(atack & atack):
    #   if (Armaesquirlada)
    #      if(ArmaduraEsquirlada)
    #         Nada
    #    probBajaDeVivir
    # else(atack & fail)
    #   if(espadaEsquirlada):
    #      Muerto
    # else:
    #    herida grave o leve


if __name__ == '__main__':
    setup()
    clearDayAction()
    today = generateDay()
    dayActions()
