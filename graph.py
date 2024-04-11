# n1 = 3
# n2 = 2
# n3 = 1
# n4 = 3

import turtle
from turtle import *
import random
import math
from copy import deepcopy

turtle.speed(0)

VERTEX_AMOUNT = 11
VERTEX_RADIUS = 15
FONT_SIZE = 12
FONT = ("Arial", FONT_SIZE, "normal")
SQUARE_SIZE = 300
BREAK_GAP = 10
EXTRA_GAP = 50


def drawVertex(x, y, text):
    up()
    goto(x, y - VERTEX_RADIUS)
    down()
    circle(VERTEX_RADIUS)
    turtle.up()
    turtle.goto(x, y - VERTEX_RADIUS + FONT_SIZE / 2)
    turtle.write(text, align="center", font=FONT)
    down()


def getVertexCoords(vertexAmount, squareSize):
    vertexCoords = []

    squareStartX = -squareSize / 2
    squareStartY = squareSize / 2

    xPos = squareStartX
    yPos = squareStartY

    isXMove = 1
    isYMove = 0

    xDirection = 1
    yDirection = -1

    vertexModulus = vertexAmount % 4
    vertexStep = vertexAmount // 4

    for i in range(4):

        vertexPerSide = vertexStep

        if (vertexModulus > 0):
            vertexPerSide += 1
            vertexModulus -= 1

        vertexGap = squareSize / vertexPerSide

        for j in range(vertexPerSide):
            vertexCoords.append({"x": round(xPos), "y": round(yPos)})
            xPos += isXMove * xDirection * vertexGap
            yPos += isYMove * yDirection * vertexGap

        xPos = round(xPos)
        yPos = round(yPos)

        if (isXMove):
            isXMove = 0
            isYMove = 1
            xDirection *= -1
        elif (isYMove):
            isYMove = 0
            isXMove = 1
            yDirection *= -1

    return vertexCoords


def generateDirMatrix(vertexAmount):
    random.seed(3213)
    k = 1.0 - 1 * 0.02 - 3 * 0.005 - 0.25

    dirMatrix = []

    for i in range(vertexAmount):
        row = []

        for j in range(vertexAmount):
            randomNumber = random.uniform(0, 2.0)
            row.append(math.floor(randomNumber * k))

        dirMatrix.append(row)

    return dirMatrix


def dirIntoUndirMatrix(dirMatrix):
    undirMatrix = deepcopy(dirMatrix)

    for i in range(len(undirMatrix)):
        for j in range(len(undirMatrix)):
            if (undirMatrix[i][j] == 1):
                undirMatrix[j][i] = 1

    return undirMatrix


def getFi(vector):
    cosFi = vector[0] / math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    fi = 180 + math.degrees(math.acos(cosFi))
    if (vector[1] < 0): fi = 360 - fi
    return fi

def arrow(startX, startY, endX, endY, fi=None):
    vector = [endX - startX, endY - startY]
    if (fi == None):
        fi = getFi(vector)
    fi = math.pi * fi / 180
    lx = endX + 15 * math.cos(fi + 0.3)
    rx = endX + 15 * math.cos(fi - 0.3)
    ly = endY + 15 * math.sin(fi + 0.3)
    ry = endY + 15 * math.sin(fi - 0.3)

    drawLine(endX, endY, lx, ly)
    drawLine(endX, endY, rx, ry)


def drawLine(startX, startY, endX, endY, withArrow=False):
    up()
    goto(startX, startY)
    down()
    goto(endX, endY)

    if (withArrow == True):
        arrow(startX, startY, endX, endY)


def getOrtVector(startX, startY, endX, endY):
    vector = [endX - startX, endY - startY]
    vectorLenght = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    ortVector = [vector[0] / vectorLenght, vector[1] / vectorLenght]
    return ortVector


def normVector(ortVector):
    nVector = [-ortVector[1], ortVector[0]]
    return nVector


def createGraph(VERTEX_AMOUNT, VERTEX_RADIUS, SQUARE_SIZE, BREAK_GAP, EXTRA_GAP, graphType):
    vertexCoords = getVertexCoords(VERTEX_AMOUNT, SQUARE_SIZE)

    dirMatrix = generateDirMatrix(VERTEX_AMOUNT)

    for row in dirMatrix:
        print(row)

    matrix = dirMatrix
    withArrow = True

    if (graphType == "undir"):
        undirMatrix = dirIntoUndirMatrix(dirMatrix)

        for row in undirMatrix:
            print(row)

        matrix = undirMatrix
        withArrow = False

    for i in range(len(vertexCoords)):
        x = vertexCoords[i]["x"]
        y = vertexCoords[i]["y"]
        drawVertex(x, y, str(i + 1))

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if (matrix[i][j] == 1):
                startX = vertexCoords[i]["x"]
                startY = vertexCoords[i]["y"]
                if (i == j):
                    fi = 360 - getFi([startX, startY])
                    if (((0 < fi) and (fi < 45)) or ((315 < fi) and (fi < 360))):
                        ortVector = [1, 0]
                        setheading(270)
                    elif (((45 < fi) and (fi < 135))):
                        ortVector = [0, 1]
                        setheading(0)
                    elif (((135 < fi) and (fi < 225))):
                        ortVector = [-1, 0]
                        setheading(90)
                    elif (((225 < fi) and (fi < 315))):
                        ortVector = [0, -1]
                        setheading(180)
                    elif (fi == 45):
                        ortVector = [1, 1]
                        setheading(315)
                    elif (fi == 135):
                        ortVector = [-1, 1]
                        setheading(45)
                    elif (fi == 225):
                        ortVector = [-1, -1]
                        setheading(135)
                    elif (fi == 315):
                        ortVector = [1, -1]
                        setheading(225)

                    up()
                    goto(startX + ortVector[0] * VERTEX_RADIUS, startY + ortVector[1] * VERTEX_RADIUS)
                    down()
                    turtle.circle(10)
                    if (graphType == "dir"):
                        arrow(turtle.pos()[0], turtle.pos()[1], turtle.pos()[0], turtle.pos()[1], 150 + turtle.heading())

                else:
                    extraGapVector = [0, 0]
                    endX = vertexCoords[j]["x"]
                    endY = vertexCoords[j]["y"]
                    midX = (startX + endX) / 2
                    midY = (startY + endY) / 2
                    ortVector = getOrtVector(startX, startY, endX, endY)

                    if (((startX == endX) or (startY == endY)) and abs(i-j) <= (VERTEX_AMOUNT // 4 + 1)):
                        k = abs(i-j) - 1
                        extraGapOrtVector = getOrtVector(0, 0, midX, midY)
                        extraGapVector = [extraGapOrtVector[0] * EXTRA_GAP * k, extraGapOrtVector[1] * EXTRA_GAP * k]


                    if (matrix[j][i] == 1 and graphType == "dir"):
                        nVector = normVector(ortVector)
                        nVector[0] = nVector[0] * BREAK_GAP
                        nVector[1] = nVector[1] * BREAK_GAP
                        drawLine(startX + ortVector[0] * 15, startY + ortVector[1] * 15, midX + nVector[0] + extraGapVector[0],
                                 midY + nVector[1] + extraGapVector[1], False)
                        drawLine(midX + nVector[0] + extraGapVector[0], midY + nVector[1] + extraGapVector[1], endX - ortVector[0] * 15,
                                 endY - ortVector[1] * 15, True)

                    else:
                        drawLine(startX + ortVector[0] * 15, startY + ortVector[1] * 15,
                                 midX + extraGapVector[0],
                                 midY + extraGapVector[1], False)
                        drawLine(midX + extraGapVector[0], midY + extraGapVector[1],
                                 endX - ortVector[0] * 15,
                                 endY - ortVector[1] * 15, withArrow)

        if (graphType == "undir" and i == j):
            break

createGraph(VERTEX_AMOUNT, VERTEX_RADIUS, SQUARE_SIZE, BREAK_GAP, EXTRA_GAP, "dir")

turtle.done()
