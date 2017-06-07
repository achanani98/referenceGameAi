import copy, random
import numpy as np
import matplotlib.pyplot as plt
import time



def print_board(s,board):

	# WARNING: This function was crafted with a lot of attention. Please be aware that any
	#          modifications to this function will result in a poor output of the board 
	#          layout. You have been warn. 

	#find out if you are printing the computer or user board
	player = "Computer"
	if s == "u":
		player = "User"
	
	print "The " + player + "'s board look like this: \n"

	#print the horizontal numbers
	print " ",
	for i in range(10):
		print "  " + str(i+1) + "  ",
	print "\n"

	for i in range(10):
	
		#print the vertical line number
		if i != 9: 
			print str(i+1) + "  ",
		else:
			print str(i+1) + " ",

		#print the board values, and cell dividers
		for j in range(10):
			if board[i][j] == -1:
				print ' ',	
			elif s == "u":
				print board[i][j],
			elif s == "c":
				if board[i][j] == "*" or board[i][j] == "$":
					print board[i][j],
				else:
					print " ",
			
			if j != 9:
				print " | ",
		print
		
		#print a horizontal line
		if i != 9:
			print "   ----------------------------------------------------------"
		else: 
			print 


def computer_place_ships(board,ships):

	for ship in ships.keys():
	
		#genreate random coordinates and vlidate the postion
		valid = False
		while(not valid):

			x = random.randint(1,10)-1
			y = random.randint(1,10)-1
			o = random.randint(0,1)
			if o == 0: 
				ori = "v"
			else:
				ori = "h"
			valid = validate(board,ships[ship],x,y,ori)

		#place the ship
		#print "Computer placing a/an " + ship
		board = place_ship(board,ships[ship],ship[0],ori,x,y)
	
	return board



def validate(board,ship,x,y,ori):

	#validate the ship can be placed at given coordinates
	if ori == "v" and x+ship > 10:
		return False
	elif ori == "h" and y+ship > 10:
		return False
	else:
		if ori == "v":
			for i in range(ship):
				if board[x+i][y] != -1:
					return False
		elif ori == "h":
			for i in range(ship):
				if board[x][y+i] != -1:
					return False
		
	return True



def place_ship(board,ship,s,ori,x,y):

	#place ship based on orientation
	if ori == "v":
		for i in range(ship):
			board[x+i][y] = s
	elif ori == "h":
		for i in range(ship):
			board[x][y+i] = s

	return board


def make_move(board,x,y):
	
	#make a move on the board and return the result, hit, miss or try again for repeat hit
	if board[x][y] == -1:
		return "miss"
	elif board[x][y] == '*' or board[x][y] == '$':
		return "try again"
	else:
		return "hit"


def computer_move(board):
	
	#generate user coordinates from the user and try to make move
	#if move is a hit, check ship sunk and win condition
	while(True):
		x = random.randint(1,10)-1
		y = random.randint(1,10)-1
		res = make_move(board,x,y)
		if res == "hit":
			#print "Hit at " + str(x+1) + "," + str(y+1)
			check_sink(board,x,y)
			board[x][y] = '$'
			if check_win(board):
				return "WIN"
		elif res == "miss":
			#print "Sorry, " + str(x+1) + "," + str(y+1) + " is a miss."
			board[x][y] = "*"

		if res != "try again":
			
			return board


def check_sink(board,x,y):

	#figure out what ship was hit
	if board[x][y] == "A":
		ship = "Aircraft Carrier"
	elif board[x][y] == "B":
		ship = "Battleship"
	elif board[x][y] == "S":
		ship = "Submarine" 
	elif board[x][y] == "D":
		ship = "Destroyer"
	elif board[x][y] == "P": 
		ship = "Patrol Boat"
	
	#mark cell as hit and check if sunk
	board[-1][ship] -= 1
	#if board[-1][ship] == 0:
		#print ship + " Sunk"
		

def check_win(board):
	
	#simple for loop to check all cells in 2d board
	#if any cell contains a char that is not a hit or a miss return false
	for i in range(10):
		for j in range(10):
			if board[i][j] != -1 and board[i][j] != '*' and board[i][j] != '$':
				return False
	return True





start_time = time.time()
arr = []
for i in range(100):
	arr.append(0)


Time = []	

#types of ships
ships = {"Aircraft Carrier":5,
	     "Battleship":4,
    	 "Submarine":3,
    	 "Destroyer":3,
    	 "Patrol Boat":2}


for i in range(10001):
	#initialising with an empty board
	if (i%1000==0): print str(i/100.00)+"% complete........"

	board = []
	for i in range(10):
		board_row = []
		for j in range(10):
			board_row.append(-1)
		board.append(board_row)

	board.append(copy.deepcopy(ships))

	board = computer_place_ships(board,ships)

	#print_board("c",board)

	num_moves=0

	while(1):

		board = computer_move(board)
		num_moves=num_moves+1
		#check if computer move
		if board == "WIN":
			#print "Computer WON! :("
			break
			
	#print num_moves
	arr[num_moves-1]=arr[num_moves-1]+1
	#print("--- %s ---"%(time.time()-start_time))
	Time.append((time.time()-start_time))



x = []
for i in range(10001):
	x.append(i+1)

y = []
for i in range(100):
	y.append(i+1)


#print x
#print arr

plt.subplot(2,1,1)
plt.plot(x,Time)

plt.subplot(2,1,2)
plt.plot(y,arr)
plt.show()



#print_board("c",board)

