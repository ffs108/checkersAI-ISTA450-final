# checkersAI-ISTA450-final

![visual representation of the genetic algorithm at work](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjIzOTllZGFjNzA5YTc2MmVhM2M0Y2RkMTA3ZmRmMTJlNjhlYmY3NCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/MNiJgUZPXgTl0dSNhR/giphy.gif)


Francisco Figueroa
Professor Millhouse
ISTA 450 – Artificial Intelligence
May 7, 2023
                                                                    Checkers Genetic Learning
    For my final project I opted for an attempt to integrate a genetic agent applied to a scaled-down game of checkers. This decision for genetic algorithm arose out of simple curiosity given the work we had already done with Pacman agent and the Q-learning models of the last homework assignment. As for the idea of using checkers as a scenario for my proposed agent I needed a classic example that I more or less knew how to assess on an “eye-test” level basis. This comes as a response to something such as Pacman, which can be viewed initially as simple but within a single game state there could be multiple other agents working towards their respective goals. I needed something where I could assess static pieces acting towards the same goal. Initially I had thought chess or poker as potential implementations, but the number of permutations coupled with the combination of rulings and moves (for chess), that proved to be too time consuming both in implementation and in the time any visibly successful learning model can be created. Thus, I opted for checkers which has a significantly simpler move pool than chess but still allows for somewhat complex behaviors that would make a model interesting.
    While researching what I would need to successfully implement this, I needed to find a way to provide a proper visualization for this checkers agent. I opted to use the pygame library and referenced a quick tutorial series on creating a checkers pygame visual by “TechbyTim” since I was not too familiar with pygame personally. I will note that while this tutorial does provide the basis for the actual chess visual and structure, all actual algorithms relevant to class (detailed later) are openly built upon this checkers representation. The contribution is noted within the code and in my works cited for this paper. The result is a proper visualization that exists outside of console, and I think helps in presentation overall. That being said there is also my own personal visual implementation that is output to the terminal. This visual is a simple ASCII character-based grid that updates and presents the “score” which is the number of pieces alive per color. The win message is displayed solely on the terminal as the pygame window closes upon game completion.
Visuals aside, and before I couple apply any sort of genetic algorithms, first I had to construct an opponent. This did not prove to be too much of a decision as I had already thought of a particular algorithm I had in mind: Alpha-Beta pruning minimax. This would prove to be a good choice, the implementation, other than a few bugs here and there was smooth. I decided to work on Alpha-Beta exclusively as the white player. Alpha-Beta also reliably was fairly simple to create an evaluation function for. I developed a few Game controller object level functions to help remedy two glaring issues that eventually the genetic agent would have to face: Alpha-Beta stalling indefinitely with the last piece and Alpha-Beta getting stuck without any valid moves available. The former was relatively simple, I prioritized Alpha-Beta wanting to gain mid control as well as seeing the enemy holding mid control as unacceptable. This proved to be a successful evaluation. For the ladder issue, I actually consulted the internet on the real rules for American style checkers: a player without any available moves loses the game. I applied this as a check for the white agent, were if there was no valid moves left the agent will concede by dropping the white_piece alive value to 0 and calling the winner() function responsible for check the live pieces and determining a winner that way. Other than those cases the Alpha-Beta followed the same recursive logic as the Pacman homework assignment, with a few things modified to fir the architecture of the checkers implementation. The two utility functions getSuccessors() and proposedTransitions() would both become relevant later as they were modified and adapted to also fit the genetic algorithm agent.
    Finally at the genetic algorithm agent I approached this from a completely object-oriented design approach in contrast to the implementation of Alpha-Beta. For my GeneticAgent, I decided to have a static population size as well as a static mutation rate. The constructor only takes in two arguments, one being the player controlling the instance of the object denoted by their color, and the other being the depth. My population array is also made up of objects, denoted as Individuals as I felt it was appropriate nomenclature. After the less than conventional constructor, the rest of the algorithm is somewhat pretty standard to what I found outside of
class. My class includes a method for obtaining the optimal action, a general policy to start with, a fitness evaluation function, a training function, and a population selector. In what seemed like a bit of an unorthodox approach, I also delegated the “breeding” and “mutating” methods to the Individual objects since they already hold the information for their weight and fitness for the given problem.
    In a possible short-sighted decision, I performed the fitness evaluation tests with the Alpha-Beta AI as the opponent, making the match that is displayed after the training lean in the already experienced Individual’s favor and therefore trivial. In retrospect, creating a very simple agent, like a random move agent would have provided a good training opportunity, but also not completely have given the edge to the GeneticAgent. I think if I were reimplementing this again, and in general had a bit more time I would try to rethink the learning process and refine the way to reimplement inheritance. I saw some very interesting implementations of the genetic algorithm that incorporate Q-learning with a SARSA update rule. Though that would also be part of an added complexity to this problem. Another issue I found was that although there were a variety of possible states in checkers, the number of opening moves and how they could be preformed optimally, means that a lot of the time the games feel a bit repetitive, even with the chance of a random move appearing through mutation. This is partly due to the nature of checkers, there would be at most 4 valid moves if you are a king, but since every piece starts as a pawn the number of choices quickly boils down to just left or right. Typically, the genetic algorithm learned that “smothering” the Alpha-Beta player was a quick way to a win. It would play aggressively to gain a king piece on one side and hold the back line of pawns still in order to block white from gaining kings themselves, effectively leaving the white pieces with no valid moves and forcing them to concede.
    I also attempted a third type of agent, a deep Q learning agent, but I quickly ran into a brick wall when attempting to set it up. Firstly, it required the use of a Python library I am not too familiar with: pyTorch. NumPy also apparently has the capability to create a neural network but all to most of the functions I saw recommend were through pyTorch. I actually did manage to calculate a single move but attempting to incorporate this type of agent with its very particular architecture provided a challenge that I did not have the skill (yet) or time to tackle. The remnants of the class are still on the Git repository in the off chance I would like to revisit this sometime.
    As far as running this, on my windows machine, I had to be in the directory of the checkers.py file within terminal/powershell and use the ‘&’ operator leading to the conda virtual environment’s python.exe directory and then call checkers.py. You will need NumPy, and pygame installed other than Python’s standard library. Quick note because I also forgot to test for
this but if the deepQLearning.py file for some reason is not uncooperative feel free to delete it or install torch to your environment.


Works Cited TechbyTim. (2020, September 5). Python/Pygame Checkers tutorial (part 1) - drawing the Board. YouTube. Retrieved May 7, 2023, from https://youtu.be/vnd3RfeG3NM
