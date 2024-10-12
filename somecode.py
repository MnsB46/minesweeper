import random
import itertools
import ast

squares = []
rows = 6
columns = 6
gameOver = False

def cartesian_product(r, c):###Returns a list containing the tuplets (1,1), (1,2), ... (1,2), (2, 2), ... (r,c)
    range1 = range(1, r+1)
    range2 = range(1, c+1)
    
    return list(itertools.product(range1, range2))

def randomMinePlacer(dict1):###Changes the value of each key to randomly be true or false
    for e in dict1:
        dict1[e] = random.choices([True, False], weights=[20, 80], k=1)[0]

def nonRandomMinePlacer(dict1, tup):
    dict1[tup] = 0
    list1 = [(tup[0]-1, tup[1]-1), (tup[0], tup[1]-1), (tup[0]+1, tup[1]-1), (tup[0]+1, tup[1]), (tup[0]+1, tup[1]+1), (tup[0], tup[1]+1), (tup[0]-1, tup[1]+1), (tup[0]-1, tup[1])]
    for e in list1:
        dict1[e] = 0
    for e in squares:
        if e in list1:
            print()
        else:
            dict1[e] = random.choices([True, False], weights=[20, 80], k=1)[0]

def adjacentCounter(dict1, dict2):###Changes the value of each key to how many adjacent bombs there are.
    for e in dict1:
        list1 = [(e[0]-1, e[1]-1), (e[0], e[1]-1), (e[0]+1, e[1]-1), (e[0]+1, e[1]), (e[0]+1, e[1]+1), (e[0], e[1]+1), (e[0]-1, e[1]+1), (e[0]-1, e[1])]
        for f in list1:
            if f in dict1:
                if dict1[f] == True:
                    dict2[e] += 1

def adjacentFogCounter(dict1, dict2):###Changes the value of each key to how many adjacent bombs there are.
    for e in dict1:
        list1 = [(e[0]-1, e[1]-1), (e[0], e[1]-1), (e[0]+1, e[1]-1), (e[0]+1, e[1]), (e[0]+1, e[1]+1), (e[0], e[1]+1), (e[0]-1, e[1]+1), (e[0]-1, e[1])]
        for f in list1:
            if f in dict1:
                if dict1[f] == 0 or dict1[f] == 2:
                    dict2[e] += 1
                    
def draw_squares(list1, adjacentMines):###Draws the squares
    global gameOver
    for i in range(rows):
        for e in list1[i*columns:i*columns+columns]:
            if fog[e] == 1:
                if mines[e] == True:
                    print("|*", end="")
                    gameOver = True
                else:
                    print("|"+str(adjacentMines[e]), end="")
            elif fog[e] == 2:
                print("|?", end="")
            else:
                print("| ", end="")
        print()
    if gameOver == True:
        print("BOOM")
    if checkWinCondition(fog):
        gameOver == True
        print("You won")

def checkWinCondition(dict1):
    sum = 0
    for e in dict1:
        if dict1[e] == 1:
            sum += 1
        elif dict1[e] == 2 and mines[e] == True:
            sum += 1
    if sum == len(squares):
        return True
    else:
        return False

def placeBombMarks(e):
    global fog
    if adjacentMines[e] != 0:
        if adjacentFog[e] == adjacentMines[e]:
            list1 = [(e[0]-1, e[1]-1), (e[0], e[1]-1), (e[0]+1, e[1]-1), (e[0]+1, e[1]), (e[0]+1, e[1]+1), (e[0], e[1]+1), (e[0]-1, e[1]+1), (e[0]-1, e[1])]
            for f in list1:
                if f in squares:
                    if fog[f] == 0:
                        fog[f] = 2
    else:
        list1 = [(e[0]-1, e[1]-1), (e[0], e[1]-1), (e[0]+1, e[1]-1), (e[0]+1, e[1]), (e[0]+1, e[1]+1), (e[0], e[1]+1), (e[0]-1, e[1]+1), (e[0]-1, e[1])]
        for f in list1:
            if f in squares:
                if fog[f] == 0:
                    fog[f] = 1
    

squares = cartesian_product(rows, columns) #list containing the coordinates of all squares
mines = {key: None for key in squares} #dictionary containing if a squares is a bomb or not
adjacentMines = {key: 0 for key in squares} #dictionary containing how many adjacent bombs there is to a squares
fog = {key: 0 for key in squares} #dictionary containing if a square is hidden, shown or has a bomb mark
adjacentFog = {key: 0 for key in squares} #dictionary containing how many adjacent squares are hidden, or has a bomb mark
randomMinePlacer(mines)
adjacentCounter(mines, adjacentMines)
draw_squares(squares, adjacentMines)

while gameOver == False:
    user_input = input() #ask for user input
    user_input = "("+user_input+")" #adds paranthesis to user input
    user_input = ast.literal_eval(user_input) #converts the user input string to a tuplet
    fog[user_input] = 1 #changes the square to shown
    adjacentFog = {key: 0 for key in adjacentFog}
    adjacentFogCounter(fog, adjacentFog)
    #print(adjacentFog)
    
    placeBombMarks(user_input)
    #Should show hidden squares if they are known to be safe
    #ie there are as many bomb marks as there are adjacent mines
    
    draw_squares(squares, adjacentMines) #draws the squares showing the newly revealed squares
    


