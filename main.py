import time

class Possible_Place:
    #class for box location, contains x position (horizontal), y position (vertical)
    #, its length and its orientation
    def __init__(self, x_in, y_in, length_in, horizontal):
        self.x = x_in
        self.y = y_in
        self.length = length_in
        self.isHorizontal = horizontal

def print_possible_places(list_possible_places):
    #prints the list of possible places
    for x in list_possible_places:
        print(x.x, end =' ')
        print(x.y,end =' ')
        print(x.length, end = ' ')
        print(x.isHorizontal)

def find_possible_places(crossword_matrix, matrix_size):
    # list the possible place for the words
    # returns list of possible places
    list_possible_places = []
    # horizontal
    first_y = 0
    first_x = 0
    for i in range(0, matrix_size):
        found = False
        length = 0
        for j in range(0, matrix_size):
            if (crossword_matrix[i][j] == '-'):
                if (not (found)):
                    first_x = j
                    first_y = i
                    found = True
                length = length + 1
                if (j == matrix_size - 1 and length > 1):  # handling for edges
                    list_possible_places.append(Possible_Place(first_x, first_y, length, True))
            elif (crossword_matrix[i][j] == '#'):
                if (length > 1):
                    list_possible_places.append(Possible_Place(first_x, first_y, length, True))
                found = False
                length = 0
    # vertical
    for j in range(0, matrix_size):
        found = False
        length = 0
        for i in range(0, matrix_size):
            if (crossword_matrix[i][j] == '-'):
                if (not (found)):
                    first_x = j
                    first_y = i
                    found = True
                length = length + 1
                if (i == matrix_size - 1 and length > 1):
                    list_possible_places.append(Possible_Place(first_x, first_y, length, False))
            elif (crossword_matrix[i][j] == '#'):
                if (length > 1):
                    list_possible_places.append(Possible_Place(first_x, first_y, length, False))
                found = False
                length = 0
    return list_possible_places


def insert_to_crossword(crossword, place, string):
    #insert a string to a place in crossword
    #string ALWAYS fits to the possible place in crossword
    if place.isHorizontal :
        for i in range(0, len(string)):
            #crossword[place.y][place.x+i] = string[i]
            crossword[place.y][place.x:place.x+len(string)] = list(string)
    else :
        for i in range (0,len(string)):
            crossword[place.y+i][place.x] = string[i]

def possible_to_fill(crossword, place, string):
    #check whether a string fits to a place in crossword
    #checks by its length and whether any char is different with the string that wanted to be inputed
    if(place.length != len(string)):
        return False
    if place.isHorizontal:
        for i in range (0,place.length):
            crossword_char = crossword[place.y][place.x+i]
            if crossword_char != '-' and crossword_char != string[i]:
                return False
    else: #if vertical
        for i in range (0,place.length):
            crossword_char =  crossword[place.y+i][place.x]
            if crossword_char != '-' and crossword_char != string[i]:
                return False
    return True

def solve_crossword(crossword, possible_places, string_list):
    #solve the crossword by brute force method
    #continue searching if it is possible to fill the string
    #if its impossible, go to the next string in the string list
    if possible_places:
        place = possible_places[0]
        temp_crossword = list(map(list,crossword))
        for i in range(0,len(string_list)):
            '''print_crossword(crossword)
            print(place.x, end=' ')
            print(place.y, end=' ')
            print(place.length, end=' ')
            print(place.isHorizontal)
            print('String = ', string_list[i])'''
            temp_string_list = string_list[:]
            if(possible_to_fill(temp_crossword,place,string_list[i])):
                insert_to_crossword(temp_crossword, place, string_list[i])
                temp_string_list.remove(temp_string_list[i])
                result, filled = solve_crossword(temp_crossword, possible_places[1:],temp_string_list)
                if filled:
                    crossword = result
                    return crossword, True
                else:
                    temp_crossword = list(map(list,crossword))
        return [], False
    else:
        return crossword,True

def print_crossword(crossword):
    #print all the crossword elements
    for x in crossword:
        for i in range (0,len(x)):
            print(x[i],end='')
        print()

#MAIN PROGRAM

# read the crossword file
print("(  ____ \(  ____ )(  ___  )(  ____ \(  ____ \|\     /|(  ___  )(  ____ )(  __  \   (  ____ \(  ___  )( \    |\     /|(  ____ \(  ____ )")
print("| (    \/| (    )|| (   ) || (    \/| (    \/| )   ( || (   ) || (    )|| (  \  )  | (    \/| (   ) || (    | )   ( || (    \/| (    )|")
print("| |      | (____)|| |   | || (_____ | (_____ | | _ | || |   | || (____)|| |   ) |  | (_____ | |   | || |    | |   | || (__    | (____)|")
print("| |      |     __)| |   | |(_____  )(_____  )| |( )| || |   | ||     __)| |   | |  (_____  )| |   | || |    ( (   ) )|  __)   |     __)")
print("| |      | (\ (   | |   | |      ) |      ) || || || || |   | || (\ (   | |   ) |        ) || |   | || |     \ \_/ / | (      | (\ (   ")
print("| (____/\| ) \ \__| (___) |/\____) |/\____) || () () || (___) || ) \ \__| (__/  )  /\____) || (___) || (____/\\   /  | (____/\| ) \ \__")
print("(_______/|/   \__/(_______)\_______)\_______)(_______)(_______)|/   \__/(______/   \_______)(_______)(_______/ \_/   (_______/|/   \__/")
crossword_file_name = input("Input the file name ")
start_time = time.time()
crossword_file = open(crossword_file_name, 'r')
testcase_file = crossword_file.readlines()
#read the size
matrix_size = int(testcase_file[0])
#read the crossword
crossword_matrix = []
for x in range(1, matrix_size + 1):
    temp_string = testcase_file[x]
    crossword_matrix.append(list(temp_string[0:matrix_size]))
#read the strings that wanted to be inputted to the crossword
string_list = testcase_file[-1].split(';')
# file have read in crossword_matrix

#find the places that will be filled with strings
list_possible_places = find_possible_places(crossword_matrix, matrix_size)

#sort by the length for optimization
list_possible_places.sort(key = lambda l:l.length, reverse=True)
string_list.sort(key = len, reverse=True)

#solve the crossword
result, bool = solve_crossword(crossword_matrix,list_possible_places, string_list)
print_crossword(result)

#print the execution time
print("time elapsed: {:.8f}s".format(time.time() - start_time))



