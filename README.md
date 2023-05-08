# checkersAI-ISTA450-final

![visual representation of the genetic algorithm at work](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjIzOTllZGFjNzA5YTc2MmVhM2M0Y2RkMTA3ZmRmMTJlNjhlYmY3NCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/MNiJgUZPXgTl0dSNhR/giphy.gif)


Francisco Figueroa

Professor Millhouse

ISTA 450 – Artificial Intelligence

May 7, 2023
 

For my final project I opted for an attempt to integrate a genetic agent applied to a scaled-down game of checkers. This decision for genetic algorithm arose out of simple curiosity given the work we had already done with Pacman agent and the Q-learning models of the last homework assignment. As for the idea of using checkers as a scenario for my proposed agent I needed a classic example that I more or less knew how to assess on an “eye-test” level basis. This comes as a response to something such as Pacman, which can be viewed initially as simple but within a single game state there could be multiple other agents working towards their respective goals. I needed something where I could assess static pieces acting towards the same goal. Initially I had thought chess or poker as potential implementations, but the number of permutations coupled with the combination of rulings and moves (for chess), that proved to be too time consuming both in implementation and in the time any visibly successful learning model can be created. Thus, I opted for checkers which has a significantly simpler move pool than chess but still allows for somewhat complex behaviors that would make a model interesting.
