from copy import deepcopy
import random
import sys
import math



def create_board():
	f = open(infile,"r")
	file_lines = f.readlines()
	f1 = [[int(char) for char in line[0:7]] for line in file_lines[0:-1]]
	turn = int(file_lines[-1][0])
	f.close()
	#g = [[0 for i in range(7)]for j in range(6)]
	return f1,turn
	
	

def printGameBoardToFile(turn):
	f1 = open(outfile,"w")
	for row in grid:
		f1.write(''.join(str(col) for col in row)+'\r\n')
	if(turn==2):
		turn=1
	else:
		turn=2
	f1.write('%s\r\n' % str(turn))
	f1.close()

def printGameBoardToFile1(turn):
	f1 = open("human.txt","w")
	for row in grid:
		f1.write(''.join(str(col) for col in row)+'\r\n')
	if(turn==2):
		turn=1
	else:
		turn=2
	f1.write('%s\r\n' % str(turn))
	f1.close()

def printGameBoardToFile2(turn):
	f1 = open("computer.txt","w")
	for row in grid:
		f1.write(''.join(str(col) for col in row)+'\r\n')
	if(turn==2):
		turn=1
	else:
		turn=2
	f1.write('%s\r\n' % str(turn))
	f1.close()

	




def print_grid():
	for x in grid:
		print(" ".join(map(str,x)))
def playpiece(col,grid,type):
	if(grid[0][col]==0):
		for i in range(5,-1,-1):
			if(grid[i][col]==0):
				grid[i][col]=type
				return 1
def checkPieceCount():
	pieceCount = int(sum(1 for row in grid for piece in row if piece)) 
	#print("piececount"+str(pieceCount))
	return pieceCount

def avilable_columns(grid):
	avilable_list = []
	for i in range(7):
		if(grid[0][i]==0):
			avilable_list.append(i)
	return avilable_list
		
def terminal_node():
	return len(avilable_columns(grid))

def current_score(grid,type):
	score = 0
	if(type==1):
		opp = 2
	elif(type==2):
		opp = 1
	for r in range(6):
		row_array = [int(i) for i in list(grid[r])]
		for c in range(4):
			a = row_array[c:c+4]
			if(a.count(type)==4):
				score+=100
			elif(a.count(type)==3 and a.count(0)==1):
				score +=5
			elif(a.count(type)==2 and a.count(0)==2):
				score+=2
			elif(a.count(opp)==3 and a.count(0)==0):
				score-=40
			if(a.count(opp)==4 and a.count(0)==0):
				score-=80
	for c in range(7):
		col_array = []
		for r in range(6):
			col_array.append(grid[r][c])
		for r in range(4):
			a = col_array[r:r+4]
			if(a.count(type)==4):
				score+=100
			elif(a.count(type)==3 and a.count(0)==1):
				score +=5
			elif(a.count(type)==2 and a.count(0)==2):
				score+=2
			elif(a.count(opp)==3 and a.count(0)==0):
				score-=-40
			if(a.count(opp)==4 and a.count(0)==0):
				score-=80

	for r in range(6-3):
		for c in range(7-3):
			a = [grid[r+i][c+i] for i in range(4)]
			#score += evaluate_a(a, piece)
			if(a.count(type)==4):
				score+=100
			elif(a.count(type)==3 and a.count(0)==1):
				score+=5
			elif(a.count(type)==2 and a.count(0)==2):
				score+=2
			elif(a.count(opp)==3 and a.count(0)==0):
				score-=40
			if(a.count(opp)==4 and a.count(0)==0):
				score-=80

	for r in range(6-3):
		for c in range(7-3):
			a = [grid[r+3-i][c+i] for i in range(4)]
			#score += evaluate_a(a, piece)
			if(a.count(type)==4):
				score+=100
			elif(a.count(type)==3 and a.count(0)==1):
				score+=5
			elif(a.count(type)==2 and a.count(0)==2):
				score+=2
			elif(a.count(opp)==3 and a.count(0)==0):
				score-=40
			if(a.count(opp)==4 and a.count(0)==0):
				score-=80
	#print("score"+str(score)) 
	return score
	
	
	


	
def minimax(depth,grid,alpha,beta,maximizingPlayer):
	if(depth==0):
		#print(grid)
		#leprint("scoreeeeeeeeeeeee"+str(current_score(grid,2)))
		return(None,current_score(grid,2)) 
	if(maximizingPlayer==True):
		column = 0
		#type = 2
		value = float("-inf")
		avilable_column = []
		avilable_column = avilable_columns(grid)
		#print("avilable_column"+str(avilable_column))
		for i in avilable_column:
			#print("iiiii"+str(i))
			#print(grid)
			dummy_grid = deepcopy(grid)
			playpiece(i,dummy_grid,2)
			new_value = minimax(depth-1,dummy_grid,alpha,beta,False)[1]
			if(new_value>value):
				value = new_value
				column = i
			alpha = max(alpha,value)
			if(alpha>=beta):
				break
			
		return column,value
		
		
	elif(maximizingPlayer==False):
		column = 0
		value = float("inf")
		avilable_column = []
		avilable_column = avilable_columns(grid)
		for i in avilable_column:
			dummy_grid = deepcopy(grid)
			playpiece(i,dummy_grid,1)
			new_value = minimax(depth-1,dummy_grid,alpha,beta,True)[1]
			if(new_value<value):
				value = new_value
				column = i
			beta = min(beta,value)
			if(alpha<=beta):
				break
			
		return column,value

	
def countScore():
	player1Score = 0;
	player2Score = 0;

	# Check horizontally
	for row in grid:
		# Check player 1
		if row[0:4] == [1]*4:
			player1Score += 1
		if row[1:5] == [1]*4:
			player1Score += 1
		if row[2:6] == [1]*4:
			player1Score += 1
		if row[3:7] == [1]*4:
			player1Score += 1
		# Check player 2
		if row[0:4] == [2]*4:
			player2Score += 1
		if row[1:5] == [2]*4:
			player2Score += 1
		if row[2:6] == [2]*4:
			player2Score += 1
		if row[3:7] == [2]*4:
			player2Score += 1

	# Check vertically
	for j in range(7):
		# Check player 1
		if (grid[0][j] == 1 and grid[1][j] == 1 and
			   grid[2][j] == 1 and grid[3][j] == 1):
			player1Score += 1
		if (grid[1][j] == 1 and grid[2][j] == 1 and
			   grid[3][j] == 1 and grid[4][j] == 1):
			player1Score += 1
		if (grid[2][j] == 1 and grid[3][j] == 1 and
			   grid[4][j] == 1 and grid[5][j] == 1):
			player1Score += 1
		# Check player 2
		if (grid[0][j] == 2 and grid[1][j] == 2 and
			   grid[2][j] == 2 and grid[3][j] == 2):
			player2Score += 1
		if (grid[1][j] == 2 and grid[2][j] == 2 and
			   grid[3][j] == 2 and grid[4][j] == 2):
			player2Score += 1
		if (grid[2][j] == 2 and grid[3][j] == 2 and
			   grid[4][j] == 2 and grid[5][j] == 2):
			player2Score += 1

	# Check diagonally

	# Check player 1
	if (grid[2][0] == 1 and grid[3][1] == 1 and
		   grid[4][2] == 1 and grid[5][3] == 1):
		player1Score += 1
	if (grid[1][0] == 1 and grid[2][1] == 1 and
		   grid[3][2] == 1 and grid[4][3] == 1):
		player1Score += 1
	if (grid[2][1] == 1 and grid[3][2] == 1 and
		   grid[4][3] == 1 and grid[5][4] == 1):
		player1Score += 1
	if (grid[0][0] == 1 and grid[1][1] == 1 and
		   grid[2][2] == 1 and grid[3][3] == 1):
		player1Score += 1
	if (grid[1][1] == 1 and grid[2][2] == 1 and
		   grid[3][3] == 1 and grid[4][4] == 1):
		player1Score += 1
	if (grid[2][2] == 1 and grid[3][3] == 1 and
		   grid[4][4] == 1 and grid[5][5] == 1):
		player1Score += 1
	if (grid[0][1] == 1 and grid[1][2] == 1 and
		   grid[2][3] == 1 and grid[3][4] == 1):
		player1Score += 1
	if (grid[1][2] == 1 and grid[2][3] == 1 and
		   grid[3][4] == 1 and grid[4][5] == 1):
		player1Score += 1
	if (grid[2][3] == 1 and grid[3][4] == 1 and
		   grid[4][5] == 1 and grid[5][6] == 1):
		player1Score += 1
	if (grid[0][2] == 1 and grid[1][3] == 1 and
		   grid[2][4] == 1 and grid[3][5] == 1):
		player1Score += 1
	if (grid[1][3] == 1 and grid[2][4] == 1 and
		   grid[3][5] == 1 and grid[4][6] == 1):
		player1Score += 1
	if (grid[0][3] == 1 and grid[1][4] == 1 and
		   grid[2][5] == 1 and grid[3][6] == 1):
		player1Score += 1

	if (grid[0][3] == 1 and grid[1][2] == 1 and
		   grid[2][1] == 1 and grid[3][0] == 1):
		player1Score += 1
	if (grid[0][4] == 1 and grid[1][3] == 1 and
		   grid[2][2] == 1 and grid[3][1] == 1):
		player1Score += 1
	if (grid[1][3] == 1 and grid[2][2] == 1 and
		   grid[3][1] == 1 and grid[4][0] == 1):
		player1Score += 1
	if (grid[0][5] == 1 and grid[1][4] == 1 and
		   grid[2][3] == 1 and grid[3][2] == 1):
		player1Score += 1
	if (grid[1][4] == 1 and grid[2][3] == 1 and
		   grid[3][2] == 1 and grid[4][1] == 1):
		player1Score += 1
	if (grid[2][3] == 1 and grid[3][2] == 1 and
		   grid[4][1] == 1 and grid[5][0] == 1):
		player1Score += 1
	if (grid[0][6] == 1 and grid[1][5] == 1 and
		   grid[2][4] == 1 and grid[3][3] == 1):
		player1Score += 1
	if (grid[1][5] == 1 and grid[2][4] == 1 and
		   grid[3][3] == 1 and grid[4][2] == 1):
		player1Score += 1
	if (grid[2][4] == 1 and grid[3][3] == 1 and
		   grid[4][2] == 1 and grid[5][1] == 1):
		player1Score += 1
	if (grid[1][6] == 1 and grid[2][5] == 1 and
		   grid[3][4] == 1 and grid[4][3] == 1):
		player1Score += 1
	if (grid[2][5] == 1 and grid[3][4] == 1 and
		   grid[4][3] == 1 and grid[5][2] == 1):
		player1Score += 1
	if (grid[2][6] == 1 and grid[3][5] == 1 and
		   grid[4][4] == 1 and grid[5][3] == 1):
		player1Score += 1

	# Check player 2
	if (grid[2][0] == 2 and grid[3][1] == 2 and
		   grid[4][2] == 2 and grid[5][3] == 2):
		player2Score += 1
	if (grid[1][0] == 2 and grid[2][1] == 2 and
		   grid[3][2] == 2 and grid[4][3] == 2):
		player2Score += 1
	if (grid[2][1] == 2 and grid[3][2] == 2 and
		   grid[4][3] == 2 and grid[5][4] == 2):
		player2Score += 1
	if (grid[0][0] == 2 and grid[1][1] == 2 and
		   grid[2][2] == 2 and grid[3][3] == 2):
		player2Score += 1
	if (grid[1][1] == 2 and grid[2][2] == 2 and
		   grid[3][3] == 2 and grid[4][4] == 2):
		player2Score += 1
	if (grid[2][2] == 2 and grid[3][3] == 2 and
		   grid[4][4] == 2 and grid[5][5] == 2):
		player2Score += 1
	if (grid[0][1] == 2 and grid[1][2] == 2 and
		   grid[2][3] == 2 and grid[3][4] == 2):
		player2Score += 1
	if (grid[1][2] == 2 and grid[2][3] == 2 and
		   grid[3][4] == 2 and grid[4][5] == 2):
		player2Score += 1
	if (grid[2][3] == 2 and grid[3][4] == 2 and
		   grid[4][5] == 2 and grid[5][6] == 2):
		player2Score += 1
	if (grid[0][2] == 2 and grid[1][3] == 2 and
		   grid[2][4] == 2 and grid[3][5] == 2):
		player2Score += 1
	if (grid[1][3] == 2 and grid[2][4] == 2 and
		   grid[3][5] == 2 and grid[4][6] == 2):
		player2Score += 1
	if (grid[0][3] == 2 and grid[1][4] == 2 and
		   grid[2][5] == 2 and grid[3][6] == 2):
		player2Score += 1

	if (grid[0][3] == 2 and grid[1][2] == 2 and
		   grid[2][1] == 2 and grid[3][0] == 2):
		player2Score += 1
	if (grid[0][4] == 2 and grid[1][3] == 2 and
		   grid[2][2] == 2 and grid[3][1] == 2):
		player2Score += 1
	if (grid[1][3] == 2 and grid[2][2] == 2 and
		   grid[3][1] == 2 and grid[4][0] == 2):
		player2Score += 1
	if (grid[0][5] == 2 and grid[1][4] == 2 and
		   grid[2][3] == 2 and grid[3][2] == 2):
		player2Score += 1
	if (grid[1][4] == 2 and grid[2][3] == 2 and
		   grid[3][2] == 2 and grid[4][1] == 2):
		player2Score += 1
	if (grid[2][3] == 2 and grid[3][2] == 2 and
		   grid[4][1] == 2 and grid[5][0] == 2):
		player2Score += 1
	if (grid[0][6] == 2 and grid[1][5] == 2 and
		   grid[2][4] == 2 and grid[3][3] == 2):
		player2Score += 1
	if (grid[1][5] == 2 and grid[2][4] == 2 and
		   grid[3][3] == 2 and grid[4][2] == 2):
		player2Score += 1
	if (grid[2][4] == 2 and grid[3][3] == 2 and
		   grid[4][2] == 2 and grid[5][1] == 2):
		player2Score += 1
	if (grid[1][6] == 2 and grid[2][5] == 2 and
		   grid[3][4] == 2 and grid[4][3] == 2):
		player2Score += 1
	if (grid[2][5] == 2 and grid[3][4] == 2 and
		   grid[4][3] == 2 and grid[5][2] == 2):
		player2Score += 1
	if (grid[2][6] == 2 and grid[3][5] == 2 and
		   grid[4][4] == 2 and grid[5][3] == 2):
		player2Score += 1
	print("human------score ------->"+str(player1Score))
	print("AI----------socre ------->"+str(player2Score))
	
	if(player1Score>player2Score):
		print("WINNER IS .............HUMAN")
		print("HURRAYYYYYYY HUMAN IS MORE INTELLIGENT THAN AI")
	elif(player1Score<player2Score):
		print("WINNER IS .............AI")
		print("WOAHHHH AI BEAT HUMANN")
	else:
		print("DRAW MATCH")
	





def interactiveGame(turn):
	# human = 1
	# machine = 2 
	# grid,turn = create_board()
	#print("turn",turn)
	turn = turn % 2
	while(checkPieceCount()<42):
		if(turn==0):  #human part
			#print_grid()
			col = int(input("enter the value of player 1:")) 
			col = col-1
			flag=False
			if(col>6 or col<0 or grid[0][col]):
				flag=True
			while(flag==True):
				col = int(input("enter a valid value:"))
				col = col-1   
				if(col>6 or col<0 or grid[0][col]):
					flag=True
				else:
					flag=False
				
				
			type = human
			playpiece(col,grid,type)
			print("HUMAN MOVE")
			print_grid()
			turn +=1
			printGameBoardToFile1(turn)
			turn = turn%2
		else:
			type = machine
			depth = int(sys.argv[4])
			a=float("-inf")
			b=float("inf")
			col,value = minimax(depth,grid,a,b,True)
			#print("col"+str(col))
			#print("value"+str(value))
			playpiece(col,grid,type)
			print("AI MOVE")
			print_grid()
			turn +=1
			printGameBoardToFile2(turn)
			turn = turn%2

	if(checkPieceCount()>=42):
		countScore()

def oneMoveGame():
	# human = 1
	# machine = 2 
	# grid,turn = create_board()
	# if(checkPieceCount() == 42):    # Is the board full already?
	# 	print 'BOARD FULL\n\nGame Over!\n'
 #        sys.exit(0)
	print "BOARD BEFORE MOVE"
	print_grid()
	#print("turn",turn)
	type = turn
	depth = int(sys.argv[4])
	a=float("-inf")
	b=float("inf")
	col,value = minimax(depth,grid,a,b,True)
	#print("col"+str(col))
	#print("value"+str(value))
	playpiece(col,grid,type)
	print("AI MOVE")
	print_grid()
	printGameBoardToFile(2)
	#countScore()

		


#driver code

if len(sys.argv) != 5:
	print 'Four command-line arguments are needed:'
	print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % sys.argv[0])
	print('or: %s one-move [input_file] [output_file] [depth]' % sys.argv[0])
	sys.exit(2)

game_mode = sys.argv[1]
infile = sys.argv[2]


human = 1
machine = 2 

grid,turn = create_board()
if not game_mode == 'interactive' and not game_mode == 'one-move':
	print('%s is an unrecognized game mode' % game_mode)
	sys.exit(2)	

if(game_mode == 'interactive'):
	chance = sys.argv[3]
	if(chance=="computer-next"):
		turn=1
	elif(chance=="human-next"):
		turn=2
	else:
		print("enter computer-next or human-next")
		sys.exit(0)
	interactiveGame(turn) # Be sure to pass whatever else you need from the command line
else: # game_mode == 'one-move'
	# Set up the output file
	outfile = sys.argv[3]
	oneMoveGame() # Be sure to pass any other arguments from the command line you might need.



	
