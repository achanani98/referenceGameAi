import tensorflow as tf
import numpy as np
import copy
import random
import math


input_nodes=102
hidden_nodes=150
output_nodes=1
alpha=0.1
lmbda=0.5
gamma=0.5

def TDlambda(list_rewards):
    length=len(list_rewards)
    for i in range(0,length):
        if(i!=length-1):
            list_rewards[i]=(1-lmbda)*list_rewards[i]
        list_rewards[i]=list_rewards[i]*math.pow(lmbda,i)
    a=sum(list_rewards)

    return a
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

#value function approximator(neural network)
input_layer=tf.placeholder(tf.float32,[None,input_nodes])
Q_s_a=tf.placeholder(tf.float32,[None,output_nodes])

weights1=tf.Variable(tf.random_normal(shape=(input_nodes,hidden_nodes)))
baises1=tf.Variable(tf.zeros(shape=(hidden_nodes)))
weights2=tf.Variable(tf.random_normal(shape=(hidden_nodes,output_nodes)))
baises2 =tf.Variable(tf.zeros(shape=(output_nodes)))

z1=tf.matmul(input_layer,weights1)+baises1
a1=tf.nn.relu(z1)

pQ_s_a=tf.matmul(a1,weights2)+baises2

cost=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Q_s_a,logits=pQ_s_a))
optimizer=tf.train.GradientDescentOptimizer(alpha).minimize(cost)

game_progress=[]
init=tf.initialize_all_variables()
with tf.Session() as session:
    session.run(init)
    for game in range(1,10001):
        print game
        k=0
        states=[]

        actions=[]
        state=np.zeros(shape=(102),dtype=np.float32)
        hitlog=[]
        pQ_s_alist=[]
        #types of ships
        ships = {"Aircraft Carrier":5, "Battleship":4, "Submarine":3,"Destroyer":3,"Patrol Boat":2}
        board = []
        for i in range(10):
            board_row = []
            for j in range(10):
                board_row.append(-1)
            board.append(board_row)
        board.append(copy.deepcopy(ships))
        board = computer_place_ships(board,ships)

        counter=0
        while(counter<17):
            flag=1
            maxQ=0
            actionindex=[1,1]
            for i in range(1,11):
                for j in range(1,11):
                    if((state[(10*(i-1)+j)-1]==1) or (state[(10*(i-1)+j)-1]==-1)):    #1 for hit and -1 for miss
                        continue
                    state[100]=i
                    state[101]=j
                    stte=np.zeros(shape=(1,102),dtype=np.float32)
                    stte[0,:]=copy.deepcopy(state)
                    dict={}
                    dict[input_layer]=stte
                    pQsa=session.run(pQ_s_a,feed_dict=dict)

                    if(flag==1):
                        maxQ=pQsa
                        actionindex[0]=i
                        actionindex[1]=j
                        flag=0
                    if(maxQ<pQsa):
                        maxQ=pQsa
                        actionindex[0]=i
                        actionindex[1]=j
            pQ_s_alist.extend(maxQ)
            state[100:102]=copy.deepcopy(actionindex)
            states.append(copy.deepcopy(state))
            actions.append(actionindex)
            if(board[actionindex[0]-1][actionindex[1]-1]==-1):
                h=-1
            else:
                h=1
            if(h==1):
                counter+=1
            hitlog.append(h)
            state[(10*((actionindex[0])-1)+(actionindex[1]))-1]=h


        aQ_s_a=[]
        for timestep in range(0,len(states)):
            list_rewards=[]
            stp=timestep+1

            while(stp<=len(states)):
                p=0
                t=timestep
                longreward=0
                while(t<=stp):
                    if(t==stp and stp<len(states)):
                        longreward+=math.pow(gamma,p)*pQ_s_alist[t][0]
                    elif(t<len(states)):
                        longreward+=math.pow(gamma,p)*hitlog[t]
                    p+=1
                    t+=1
                list_rewards.append(longreward)
                stp+=1
            aQ_s_a.append(TDlambda(list_rewards))

        state_action=np.zeros((len(states),102),dtype=np.float32)
        Q=np.zeros((len(states),1),dtype=np.float32)
        for i in range(0,len(states)):
            state_action[i,:]=copy.deepcopy(states[i])
            Q[i,0]=aQ_s_a[i]

        game_progress.append(len(states))

        per=np.random.permutation(len(states))
        state_action=state_action[per,:]
        Q=Q[per,:]

        steps=10
        for step in range(1,steps+1):
            for i in range(0,len(states)):
                inpt=np.zeros((1,102),dtype=np.float32)
                outpt=np.zeros((1,1),dtype=np.float32)
                inpt[0,:]=state_action[i,:]
                outpt[0,0]=Q[i,0]
                feed_dict={}
                feed_dict[input_layer]=inpt
                feed_dict[Q_s_a]=outpt
                _,l=session.run([optimizer,cost],feed_dict=feed_dict)
    
        print '-----',game_progress[game-1],'-----',sum(game_progress)*1.0/len(game_progress)
    w1=session.run(weights1)
    b1=session.run(baises1)
    w2=session.run(weights2)
    b2=session.run(baises2)
    dict={}
    dict['weights1']=w1
    dict['baises1']=b1
    dict['weights2']=w2
    dict['baises2']=b2

with open('gameai.pickle','wb') as f:
    pickle.dump(dict,f)
