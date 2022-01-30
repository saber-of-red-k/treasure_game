import random

#name = input(('Enter your name '))
#score = random.randint(1,20)

score_board = []
with open('test.txt', 'r+') as f:
    for line in f:
        score_board.append([int(line.split()[0]),line.split()[1]])
for i in range(0,len(score_board)):
    print(score_board[i])

test_score = int(input('Enter score for example: '))

new_leader = input('Your name? (enter in one word or use _): ')
if len(score_board) < 10:
    with open('test.txt', 'a+') as f:
        f.write('\n')
        f.write(str(random.randint(1,20)))
        f.write(' ')
        f.write(str(new_leader))
else:
    score_board.sort()
    score_board.reverse()
    change = 0
    for i in range(len(score_board)-1,0,-1):
        if change == 1: break
        else:
            if test_score > score_board[i][0]:
                score_board[i][0] = test_score
                score_board[i][1] = new_leader
                change +=1
    score_board.sort()
    score_board.reverse()

with open('test.txt', 'w+') as f:
    for i in range(0,10):
        f.write(str(score_board[i][0]))
        f.write(' ')
        f.write(str(score_board[i][1]))
        f.write('\n')
