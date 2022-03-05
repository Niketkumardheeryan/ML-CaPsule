#import randint from random module
from random import randint
#moves of the game
moves = ["r", "p", "s"]
player_score = 0
computer_score = 0

#start the game
x = int(input("(1)Start. (2)End the game. \n"))

if x != 1 and x != 2:
    x = int(input("Invalid input! Please enter '1' or '2': \n"))


if x == 1:
            while True:
                #randomly selects option for computer
                computer_moves = moves[randint(0, 2)]
                #ask for player move
                player_moves = input("(r)Rock. (p)Paper. (s)Scissors. (e)End the game. \n")
                #if player and computer moves are equal it's a tie
                if player_moves == computer_moves:
                    print("Computer chose the same move. It's a tie! Please play again!")
                    continue

                elif player_moves == "r":
                    if computer_moves == "p":
                        computer_score+=1
                        print("Computer chose paper. You lose! your score:",player_score, "computer score:",computer_score)
                        continue
                    elif computer_moves == "s":
                        player_score+=1
                        print("Computer chose scissors. You win! your score:",player_score, "computer score:",computer_score)
                        continue

                elif player_moves == "p":
                    if computer_moves == "s":
                        computer_score+=1
                        print("Computer chose scissors. You lose! your score:",player_score, "computer score:",computer_score)
                        continue
                    elif computer_moves == "r":
                        player_score+=1
                        print("Computer chose rock. You win! your score:",player_score, "computer score:",computer_score)
                        continue

                elif player_moves == "s":
                    if computer_moves == "r":
                        computer_score+=1
                        print("Computer chose rock. You lose! your score:",player_score, "computer score:",computer_score)
                        continue
                    elif computer_moves == "p":
                        player_score+=1
                        print("Computer chose paper. You win! your score:",player_score, "computer score:",computer_score)
                        continue
                #quit the game
                elif player_moves == "e":
                    exit()
                #if the player entered a wrong letter raise an error
                else:
                    print("Invalid input! Please enter 'r','p','s' or 'e': ")
                    continue



#quit the game
elif x == 2:
        exit()
