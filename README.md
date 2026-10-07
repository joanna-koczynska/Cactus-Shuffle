# 🌵 Cactus Cards
<img width="1024" height="1024" alt="logo" src="https://github.com/user-attachments/assets/a98ef556-c994-45d1-a802-cbfe51e4144b" />

A two-player card drafting game inspired by *Sushi Go*, with a cactus theme. Built in Python with Pygame. You play against an AI opponent that uses a minimax-based algorithm to choose its cards.

This was a university project. The in-game interface is in Polish.

## How to play

The game lasts **3 rounds**. At the start of each round, both players get 6 cards. Each turn you pick one card from your hand to keep, and the AI does the same. Then the players **swap hands** and pick again from the cards the other player left. The round ends when the hands are empty, and the points from collected cards are added to your total score. The player with more points after 3 rounds wins.

## Scoring

| Card | Points |
|------|--------|
| **Monstera Duo** | Every pair = 5 pts (a single card = 0) |
| **Cactus Trio** | Every set of 3 = 10 pts (fewer = 0) |
| **Succulent** | 1 → 1 pt, 2 → 3 pts, 3 → 6 pts, 4 → 10 pts, 5 → 15 pts |
| **Mini Cactus** | 1 pt each |
| **Blooming Cactus** | 2 pts each |
| **Royal Cactus** | 3 pts each |

## AI opponent

The computer player uses a minimax-style search (similar to expectimax). For every card it could play, it simulates all possible responses from the human player, looks up to 6 moves ahead, averages the results, and picks the card with the best expected score difference.

## Running the game

Requirements: Python 3 and Pygame.

```bash
pip install pygame
python game.py
```

Run the game from the project folder, because the card images are loaded from the `cards/` directory.

<img width="1501" height="735" alt="image" src="https://github.com/user-attachments/assets/829c3059-d47a-43c8-93be-5c50d0a2da38" />
