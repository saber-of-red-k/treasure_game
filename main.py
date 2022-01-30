import random       #for random initialization
import os           #to if file exists

'''Treasure map file creation + initialization'''
def file_init():

    with open('treasure.txt', 'w+') as f:
        for i in range(0,10,1):
            f.write(str(i)*random.randint(1,20))        #writing in for loop 1,2,3... *random times
        f.write('TREASURE')                             #treasure plant
    with open('treasure.txt', 'a+') as f:
        for i in range(9,-1,-1):
            f.write(str(i) * random.randint(1, 20))     #closing sequence with reversed for: 9,8,7...

'''File read & main game function'''
def file_read():

    hitword = ['T', 'R', 'E', 'A', 'S', 'U', 'E']       #list of winning symbols(TREASURE)
    counter = 0                                         #counter for number of tries

    with open('treasure.txt', 'r') as f:
        length_of_file = len(f.read())                  #length of file for further check for errors
        f.seek(0)                                       #return to start of file after reading

        while True:                                     #while loop inside with statement
            step = input('Which way we are moving? B for back, F for forward: ')
            if step.lower() != 'b' and step.lower() !='f':
                continue                                #continue until we receive proper choice
            elif step.lower() == 'f':
                try:
                    navigate = int(input('How many characters? '))
                except: continue                        #try for possible negative number

                if navigate > length_of_file:
                    print('You moved too far away! Try again. ')
                    continue                            #check if the player exited the treasure "map"

                f.seek(f.tell()+navigate)               #move to initial position + player input
                check = f.read(1)                       #read one char
                f.seek(f.tell()-1)                      #return one char back after reading

                if check not in hitword:
                    print(f' We are now on position {f.tell()}')
                    print(f' We hit : {check}')
                    counter += 1                        #counter increments for one try
                    continue
                else:
                    counter += 1                        #final try increment
                    return counter                      #return counter if we hit one of the TREASURE words

            elif step.lower() == 'b':

                try:
                    navigate = int(input('How many characters? '))+1        #+1 because we are moving before the symbol
                except: continue                                            #ex. player choosing 20, we need to move 21 back
                                                                            # 19 20 21 - we are moving to end of 19 to read 20
                try:
                    f.seek(f.tell()-navigate)
                except:
                    print('You can\'t go there! Try again. ')               #in case seek is moving below 0 (to the negative) due to player choice
                    continue

                check = f.read(1)
                f.seek(f.tell() - 1)

                if check not in hitword:
                    f.seek(f.tell()+1)                                      #+1 for previous:
                    print(f' We are now on position {f.tell()}')            #ex. 19 20 21 - we are moving to the end of 20
                    print(f' We hit : {check}')
                    counter += 1                                            #one try counter increment
                    continue
                else:
                    counter +=1                                             #final try increment
                    return counter                                          #return counter in case we hit TREASURE

'''Function for leaderboard managmanet'''
def leaderboard(player_score):
    global score_board
    score_board = []                                                        #empty list initialization to use as a local leaderboard

    '''Internal function for leaderboard file reading and passing it to the list'''
    def score_board_init():
        global score_board
        with open('leaders.txt', 'r+') as f:
            for line in f:
                score_board.append([int(line.split()[0]), line.split()[1]])     #for every line we read we append list to list, slicing the strings, consisting of score[0],name[1]

        print('Current leaderboard for the game: \n')

        score_board.sort()                                                      #sort the list by the first value(score)

        try:
            score_board.pop(10)                                                 #delete item index 10 (11th element) if it exist
        except: pass                                                            #do nothing if we didn't save new record last time (so no 11th list item)

        for i in range(0, len(score_board)):
            print(f' Name: {score_board[i][1]}, score: {score_board[i][0]}')    #printing current leaderboard we extracted at the end of the game
        print('\n')                                                             #for graphical purpose

    '''Internal function for score check and writing it to the list'''
    def score_check():

        global score_board
        if len(score_board) < 10:                                               #if there are < 10 entries we enter the score directly to the file without checks
            new_leader = input('Congratulations! There is a new score record! Your name? (enter in one word or use _): ')

            with open('leaders.txt', 'a+') as f:                                #open file for append + write score in format
                f.write(str(player_score))
                f.write(' ')
                f.write(str(new_leader))
                f.write('\n')
            score_board.append([player_score, new_leader])                      #append to the list so no errors down when overwrite the file with the new list

            print('Thank you for playing! Your name will be saved in the leaderboard and you will see it after the next game!')

        else:                                                                   #in case there are already 10 positions we check to see if score is higher or not

            change = 0                                                      #counter for proper closing message

            for i in range(0,len(score_board)):
                if player_score < score_board[i][0]:                        #check if current score is under scores in list (smaller)

                    new_leader = input('Congratulations! You beat the score in the leaderboard! Your name? (enter in one word or use _): ')
                    score_board.append([player_score, new_leader])          #append new score in the end of the list

                    change += 1                                             #increment the change counter for message and break the loop so no further changes will be made
                    break

            if change: print('Thank you for playing! Your name will be saved in the leaderboard and you will see it after the next game!')
            else: print('Thank you for playing! No record for this game, try harder next time. ')

    '''Internal function to write the modified list to file'''
    def score_close():

        global score_board
        with open('leaders.txt', 'w+') as f:
            for i in range(0, len(score_board)):
                f.write(str(score_board[i][0]))                     #just writing the modified list (with additions or sorted after previous game
                f.write(' ')                                        #format is {score} {name} \n for next line
                f.write(str(score_board[i][1]))
                f.write('\n')

    score_board_init()
    score_check()                                                   #internal functions calling
    score_close()

file_init()                                                         #file init function calling

print('Welcome to the TREASURE HUNT game! There is a treasure somewhere there... You can move only forward and backwards in steps. Good luck! \n')

attempts = file_read()                                              #file_read() returns number of attempts it took the player to win
print(f' Congratulations! You found the treasure in {attempts} attempts \n')

if os.path.isfile('leaders.txt') == False:                          #check if leaders.txt exists - if not, then create
    f = open('leaders.txt', 'w')
    f.close()

leaderboard(attempts)                                               #pass attempts variable to leaderboard function for processing