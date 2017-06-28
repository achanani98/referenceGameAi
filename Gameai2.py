import tensorflow as tf
import numpy as np
import copy
import random
import math


input_nodes=100
hidden_nodes=100
output_nodes=100
gamma=0.5

def computer_place_ships(board,ships):
    for ship in ships.keys():
        valid=False
        while(not valid):
            x=random.randint(0,9)
            y=random.randint(0,9)
            o=random.randint(0,1)
            if(o==0):
                ori="v"
            else:
                ori="h"
            valid=validate(board,ships[ship],x,y,ori)
        board=place_ship(board,ships[ship],ship[0],ori,x,y)
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

def findships(board):
    ship_pos=[]
    for i in range(0,10):
        for j in range(0,10):
            if(board[i][j]!=-1):
                ship_pos.append(10*(i)+j)
    return ship_pos


def rewards_calculator(hitlog):
    hit_log_weighted = [(item -float(17 - sum(hitlog[:index])) / float(100 - index)) * (gamma ** index) for index, item in enumerate(hitlog)]
    return [((gamma) ** (-i)) * sum(hit_log_weighted[i:]) for i in range(len(hitlog))]

#value function approximator(neural network)
input_layer=tf.placeholder(tf.float32,[1,input_nodes])
labels=tf.placeholder(tf.int64)
learning_rate=tf.placeholder(tf.float32,shape=[])

weights1=tf.Variable(tf.truncated_normal([input_nodes,hidden_nodes],stddev=0.1/np.sqrt(100.0)))
baises1=tf.Variable(tf.zeros(shape=(1,hidden_nodes)))
weights2=tf.Variable(tf.truncated_normal([hidden_nodes,output_nodes],stddev=0.1/np.sqrt(100.0)))
baises2 =tf.Variable(tf.zeros(shape=(1,output_nodes)))

a1=tf.tanh(tf.matmul(input_layer,weights1)+baises1)

z2=tf.matmul(a1,weights2)+baises2
probabilities=tf.nn.softmax(z2)

cost=(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels,logits=z2))
optimizer=tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)

game_progress=[]
init=tf.global_variables_initializer()
with tf.Session() as session:
    session.run(init)

    game_lengths = []

    for game in range(1,10000):
        print game

        states=[]
        actions=[]
        current_state=np.zeros(shape=(1,100),dtype=np.float32)
        current_state[0,:]=-1.0
        hitlog=[]
        ships = {"Aircraft Carrier":5, "Battleship":4, "Submarine":3,"Destroyer":3,"Patrol Boat":2}
        board = []
        for i in range(10):
            board_row = []
            for j in range(10):
                board_row.append(-1)
            board.append(board_row)
        board.append(copy.deepcopy(ships))
        board = computer_place_ships(board,ships)
        ship_positions=findships(board)
        flag=0
        while(sum(hitlog)<17):
            states.append(copy.deepcopy(current_state))
            probs = session.run(probabilities,feed_dict={input_layer:current_state})
            if flag==0:
                print probs
                flag=1
            prob = [p * (index not in actions) for index, p in enumerate(probs[0])]
            prob = [p / sum(prob) for p in prob]


            current_action = np.random.choice(100,p=prob)
            hitlog.append(1*(current_action in ship_positions))

            current_state[0,current_action]= 1*(current_action in ship_positions)
            actions.append(current_action)


        game_lengths.append(len(actions))
        reward_log = rewards_calculator(hitlog)

        for reward ,current_state, action in zip(reward_log,states,actions):
            session.run(optimizer,feed_dict={input_layer:current_state,labels:[action],learning_rate:0.01* reward})
        print 'game_length--',len(actions),'  avg--',1.0*sum(game_lengths)/len(game_lengths)

    dict={}
    dict['weights1']=session.run(weights1)
    dict['weights2']=session.run(weights2)
    dict['baises1']=session.run(baises1)
    dict['baises2']=session.run(baises2)
with open('gameaiweights.pickle','wb') as f:
    pickle.dump(dict,f)    
