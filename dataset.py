import copy, random

hits_user = 0
hits_comp = 0
State_flag = 0
State_x = 0
State_y = 0


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

def user_place_ships(board,ships):

	for ship in ships.keys():

		#get coordinates from user and vlidate the postion
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
		board = place_ship(board,ships[ship],ship[0],ori,x,y)
		#print_board("u",board)
		
	#raw_input("Done placing user ships. Hit ENTER to continue")
	return board


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


def place_ship(board,ship,s,ori,x,y):

	#place ship based on orientation
	if ori == "v":
		for i in range(ship):
			board[x+i][y] = s
	elif ori == "h":
		for i in range(ship):
			board[x][y+i] = s

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



def make_move(board,x,y):
	
	#make a move on the board and return the result, hit, miss or try again for repeat hit
	if board[x][y] == -1:
		return "miss"
	elif board[x][y] == '*' or board[x][y] == '$':
		return "try again"
	else:
		return "hit"

def user_move(board):
	
	#get coordinates from the user and try to make move
	#if move is a hit, check ship sunk and win condition
	while(True):
		global State_flag,State_x,State_y

		x = random.randint(1,10)-1
		y = random.randint(1,10)-1
		if State_flag==0:
			State_x = x
			State_y = y
			State_flag = 1
		res = make_move(board,x,y)
		if res == "hit":
			#print "Hit at " + str(x+1) + "," + str(y+1)
			check_sink(board,x,y)
			board[x][y] = '$'
			global hits_user
			hits_user = hits_user + 1
			#print_board("c",board)
			
			if check_win(board):
				return "WIN"

			board=user_move(board)
			
				
		elif res == "miss":
			#print "Sorry, " + str(x+1) + "," + str(y+1) + " is a miss."
			board[x][y] = "*"
		#elif res == "try again":
			#print "Sorry, that coordinate was already hit. Please try again"

		#if res == "hit":

			#board=user_move(board)	

				

		if res != "try again":
			return board

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
			global hits_comp
			hits_comp = hits_comp + 1


			if check_win(board):
				return "WIN"

			board=computer_move(board)
			

		elif res == "miss":
			#print "Sorry, " + str(x+1) + "," + str(y+1) + " is a miss."
			board[x][y] = "*"

		#if res == "hit":
			#board=computer_move(board)
				

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
	#	print ship + " Sunk"
		

def check_win(board):
	
	#simple for loop to check all cells in 2d board
	#if any cell contains a char that is not a hit or a miss return false
	for i in range(10):
		for j in range(10):
			if board[i][j] != -1 and board[i][j] != '*' and board[i][j] != '$':
				return False
	return True

def main():

	#types of ships
	ships = {"Aircraft Carrier":5,
		     "Battleship":4,
 		     "Submarine":3,
		     "Destroyer":3,
		     "Patrol Boat":2}

	#setup blank 10x10 board
	
	l = 10000
	while (l):

		global State_flag,State_y,State_x
		State_flag = 0


		l = l-1
		board = []
		for i in range(10):
			board_row = []
			for j in range(10):
				board_row.append(-1)
			board.append(board_row)

		#setup user and computer boards
		user_board = copy.deepcopy(board)
		comp_board = copy.deepcopy(board)

		#add ships as last element in the array
		user_board.append(copy.deepcopy(ships))
		comp_board.append(copy.deepcopy(ships))

		#ship placement
		user_board = user_place_ships(user_board,ships)
		comp_board = computer_place_ships(comp_board,ships)


		flag = 0
		moves_before = random.randint(1,100)
		for j in range(moves_before):
			comp_board = user_move(comp_board)
			if comp_board == "WIN":
				flag = 1
				break

			user_board = computer_move(user_board)
		
			if user_board == "WIN":
				flag = 1
				break		



		if flag == 1:
			l = l+1
			continue

		#print user_board
		#print comp_board	

		moves_after = 0
		global hits_comp
		hits_comp = 0
		global hits_user
		hits_user = 0
		

		while(1):

			comp_board = user_move(comp_board)
			moves_after = moves_after+1

			#check if user won
			if comp_board == "WIN":
				print "Reward = " + (str)((float)(hits_user-hits_comp)/(moves_after))+"    if hit at :  "+str(State_x+1)+","+str(State_y+1)
		#		print hits_comp,hits_user,moves_after,moves_before
				break
				
			user_board = computer_move(user_board)
		
			
			if user_board == "WIN":
				print "Reward = " + (str)((float)(hits_user-hits_comp)/(moves_after))+"    if hit at:  "+str(State_x+1)+","+str(State_y+1)
		#		print hits_comp,hits_user,moves_after,moves_before
				break


		#global hits_comp
		hits_comp = 0
		#global hits_user
		hits_user = 0
		State_flag = 0
		State_x = 0
		State_y = 0
		


			
if __name__=="__main__":
	main()