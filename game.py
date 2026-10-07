import pygame
import sys
import random
import math

pygame.init()

# Kolory
BG = (252, 237, 198)
BLUE = (0, 100, 255)
DARK_BLUE = (0, 80, 200)
BLACK = (0, 0, 0)
PLAY_BUTTON_COLOR=(114, 150, 255)

# Czcionka
font = pygame.font.SysFont(None, 60)
fontEnd = pygame.font.SysFont(None, 30)

# Ustawienia ekranu
WIDTH, HEIGHT = 1500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cactus Cards")


play_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 150, 200, 80)
logo_image = pygame.image.load("cards/logo.png").convert_alpha()
logo_image = pygame.transform.scale(logo_image, (400, 400))

cards_dealt = 6

def draw_menu():
    screen.fill(BG)
    screen.blit(logo_image, (WIDTH // 2 - 200, 100)) 
    pygame.draw.rect(screen, BLUE, play_button)
    text = font.render("Play", True, BG)
    screen.blit(text, (play_button.x + 50, play_button.y + 20))

play_again_button = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 50, 180, 80)
exit_button = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 50, 180, 80)

def draw_end_screen():
    screen.fill(BG)
    big_font = pygame.font.SysFont(None, 80)
    medium_font = pygame.font.SysFont(None, 60)
    
    
    header = big_font.render("Koniec gry!", True, DARK_BLUE)
    screen.blit(header, (WIDTH // 2 - header.get_width() // 2, HEIGHT // 4))
    
    
    score_text = medium_font.render(f"Wynik końcowy: Gracz 1: {player1_score}, Gracz 2: {player2_score}", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3))
    
    if player1_score > player2_score:
        winner_text = medium_font.render("Wygrywa AI!", True, DARK_BLUE)
    elif player2_score > player1_score:
        winner_text = medium_font.render("Wygrywasz!", True, DARK_BLUE)
    else:
        winner_text = medium_font.render("Remis!", True, DARK_BLUE)
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 30))
    
    pygame.draw.rect(screen, PLAY_BUTTON_COLOR, play_again_button)
    pygame.draw.rect(screen, (200, 50, 50), exit_button)
    
    play_text = fontEnd.render("Jeszcze raz", True, BG)
    exit_text = fontEnd.render("Wyjdź", True, BG)
    
    screen.blit(play_text, (play_again_button.x + 10, play_again_button.y + 20))
    screen.blit(exit_text, (exit_button.x + 50, exit_button.y + 20))


CARD_POOL = [
    ("monsteraX2", 14),
    ("kaktusyX3", 14),
    ("sukulent", 14),
    ("kaktus2", 10),
    ("kaktus3", 5),
    ("kaktus1", 5)
]

def calculate_score(cards):
    score = 0
    card_counts = {
        "monsteraX2": cards.count("monsteraX2"),
        "kaktusyX3": cards.count("kaktusyX3"),
        "sukulent": cards.count("sukulent"),
        "kaktus1": cards.count("kaktus1"),
        "kaktus2": cards.count("kaktus2"),
        "kaktus3": cards.count("kaktus3"),
    }

    # monsteraX2: Zestaw 2 kart = 5 pkt, w innym razie 0 pkt
    if card_counts["monsteraX2"] >=2:
        couples2=card_counts["monsteraX2"] //2
        score += couples2*5

    # kaktusyX3: 3 karty = 10 pkt, w innym razie 0 pkt
    if card_counts["kaktusyX3"] >= 3:
        couples3=card_counts["kaktusyX3"] //3
        score += couples3*10
        

    # sukulent: 1 karta = 1 pkt, 2 karty = 3 pkt, 3 karty = 6 pkt, 4 karty = 10 pkt, 5 kart = 15 pkt
    if card_counts["sukulent"] == 1:
        score += 1
    elif card_counts["sukulent"] == 2:
        score += 3
    elif card_counts["sukulent"] == 3:
        score += 6
    elif card_counts["sukulent"] == 4:
        score += 10
    elif card_counts["sukulent"] == 5:
        score += 15

    # kaktus1, kaktus2, kaktus3: proste punkty
    score += card_counts["kaktus1"]*1
    score += card_counts["kaktus2"]*2
    score += card_counts["kaktus3"]*3

    return score


# --------------------------------------------------------------MINIMAX------------------------------------------
def minimax(p1_hand, p2_hand, p1_collected, p2_collected, depth):

    if depth == 0 or not p1_hand or not p2_hand:
        p1_score = calculate_score(p1_collected)
        p2_score = calculate_score(p2_collected)
        return p1_score - p2_score, None

    best_card = None
    best_avg_score = -math.inf

    for p1_card in set(p1_hand):
        total_score = 0
        valid_opponent_responses = 0

        for p2_card in set(p2_hand):
        
            temp_p1_hand = p1_hand.copy()
            temp_p2_hand = p2_hand.copy()
            temp_p1_collected = p1_collected.copy()
            temp_p2_collected = p2_collected.copy()

            temp_p1_hand.remove(p1_card)
            temp_p2_hand.remove(p2_card)
            temp_p1_collected.append(p1_card)
            temp_p2_collected.append(p2_card)

            #switch
            temp_p1_hand, temp_p2_hand = temp_p2_hand, temp_p1_hand

            eval_score, _ = minimax(
                temp_p1_hand,
                temp_p2_hand,
                temp_p1_collected,
                temp_p2_collected,
                depth - 1
            )
            total_score += eval_score
            valid_opponent_responses += 1

        if valid_opponent_responses > 0:
            #uśrednic wyniki
            avg_score = total_score / valid_opponent_responses
            if avg_score > best_avg_score:
                best_avg_score = avg_score
                best_card = p1_card

#zwrot mozliwie najlepszego wyniku:
    return best_avg_score, best_card


# --------------------------------------------------------------------------------------------------------




# obrazki kart
card_images = {
    "monsteraX2": pygame.image.load("cards/monstera.png").convert_alpha(),
    "kaktusyX3": pygame.image.load("cards/kaktusy trio.png").convert_alpha(),
    "sukulent": pygame.image.load("cards/sukulent.png").convert_alpha(),
    "kaktus1": pygame.image.load("cards/mini kaktus.png").convert_alpha(),
    "kaktus2": pygame.image.load("cards/kaktus_2.png").convert_alpha(),
    "kaktus3": pygame.image.load("cards/kaktus_3.png").convert_alpha(),
    "back": pygame.image.load("cards/back.png").convert_alpha()
}

for key in card_images:
    card_images[key] = pygame.transform.scale(card_images[key], (100, 150))


 

# FUNKCJA GRY

# Stan gry
current_state = "menu"
current_round = 1
max_rounds = 3
player1_score = 0
player2_score = 0
selected_card = None
round_in_progress = False
result_message = ""

player1_hand = []
player2_hand = []
player1_collected = []
player2_collected = []


def initialize_deck():
    global full_deck
    full_deck = []
    for name, count in CARD_POOL:
        full_deck.extend([name] * count)
    random.shuffle(full_deck)
    return full_deck


def update_card_distribution():
    global card_distribution
    card_distribution = {}
    for card_name, _ in CARD_POOL:
        card_distribution[card_name] = full_deck.count(card_name)
    
    # Dodaj karty w rękach i zebrane
    for card in player1_hand + player2_hand + player1_collected + player2_collected:
        if card in card_distribution:
            card_distribution[card] += 1

def deal_cards(cards_per_player=10):
    global player1_hand, player2_hand, full_deck
    
    # Sprawdź, czy w talii jest wystarczająco kart
    if len(full_deck) < cards_per_player * 2:
        # Jeśli nie, zresetuj talię
        initialize_deck()
        
    # Rozdaj karty
    player1_hand = []
    player2_hand = []
    for _ in range(cards_per_player):
        if full_deck:
            player1_hand.append(full_deck.pop())
        if full_deck:
            player2_hand.append(full_deck.pop())




def draw_game():
    screen.fill(BG)
    fontt = pygame.font.SysFont(None, 30)

    round_text = fontt.render(f"Runda: {current_round}/{max_rounds}", True, BLACK)
    score_text1 = fontt.render(f"Gracz 1: {player1_score}", True, BLACK)
    score_text2 = fontt.render(f"Gracz 2: {player2_score}", True, BLACK)

    rules_font = pygame.font.SysFont(None, 20)
    rules = [
        "Zasady punktacji:",
        "MONSTEROWY DUET: ",
        "   Zestaw 2 kart = 5 pkt, w innym razie 0 pkt",
        "KAKTUSOWE TRIO: ",
        "   3 karty = 10 pkt, w innym razie 0 pkt",
        "SUKULENT: ",
        "   1=1 pkt ",
        "   2=3 pkt ",
        "   3=6 pkt, ",
        "   4=10 pkt ",
        "   5=15 pkt",
        "MINI KAKTUS: ",
        "   1 karta = 1 pkt",
        "ROZKWITAJĄCY KAKTUS: ",
        "   1 karta = 2 pkt",
        "KAKTUS KRÓLEWSKI: ",
        "   1 karta = 3 pkt",
    ]
    
    x_pos = WIDTH - 360
    y_pos = 30
    padding = 10
    line_height = 30
    box_width = 440
    box_height = line_height * len(rules) + 2 * padding

    # Tło
    pygame.draw.rect(screen, (255, 255, 255), (x_pos, y_pos, box_width, box_height))
    # Obwódka
    pygame.draw.rect(screen, (0, 0, 0), (x_pos, y_pos, box_width, box_height), 2)

    # Tekst
    for i, line in enumerate(rules):
        text = rules_font.render(line, True, (0, 0, 0))
        screen.blit(text, (x_pos + padding, y_pos + padding + i * line_height))
    screen.blit(round_text, (50, 30))
    screen.blit(score_text1, (50, 100))
    screen.blit(score_text2, (50, 550))


    if result_message:
        msg = fontt.render(result_message, True, DARK_BLUE)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 100))

    # WYSWIWETLANIE KART GRACZY
    spacing = 110
    start_x = WIDTH // 2 - (len(player1_hand) * spacing // 2)
    y = HEIGHT // 50
    # for i in range(len(player1_hand)):
    for i, card_name in enumerate(player1_hand):
        x = start_x + i * spacing
        #screen.blit(card_images["back"], (x, y))
        screen.blit(card_images[card_name], (x, y))


    start_x = WIDTH // 2 - (len(player1_collected) * spacing // 2)
    y_collected = HEIGHT // 3.5
    for i, card_name in enumerate(player1_collected):
        x = start_x + i * spacing
        screen.blit(card_images[card_name], (x, y_collected))    

    mouse_x, mouse_y = pygame.mouse.get_pos()
    start_x = WIDTH // 2 - (len(player2_hand) * spacing // 2)
    y2 = HEIGHT // 1.3
    for i, card_name in enumerate(player2_hand):
        x = start_x + i * spacing
        rect = pygame.Rect(x, y2, 100, 150)
        if rect.collidepoint(mouse_x, mouse_y):
            screen.blit(pygame.transform.scale(card_images[card_name], (150, 220)), (x - 50, y2 - 50))
        else:
            screen.blit(card_images[card_name], (x, y2))

    start_x = WIDTH // 2 - (len(player2_collected) * spacing // 2)
    y_collected2 = HEIGHT // 1.9
    for i, card_name in enumerate(player2_collected):
        x = start_x + i * spacing
        screen.blit(card_images[card_name], (x, y_collected2))


def pass_cards():
    global player1_hand, player2_hand
    player1_hand, player2_hand = player2_hand, player1_hand


def end_round():
    #global player1_score, player2_score, player1_collected, player2_collected, current_round, current_state, result_message
    global player1_score, player2_score, player1_collected, player2_collected
    global current_round, current_state, result_message, final_message
  
  # Oblicz i dodaj punkty za tę rundę
    round_player1_score = calculate_score(player1_collected)
    round_player2_score = calculate_score(player2_collected)

    # Oblicz i dodaj punkty za tę rundę
    player1_score += round_player1_score
    player2_score += round_player2_score
    
    # Przejdź do następnej rundy
    current_round += 1
    
    # Wyczyść zebrane karty
    player1_collected = []
    player2_collected = []
    
    # Rozdaj karty dla następnej rundy, jeśli gra trwa dalej
    if current_round <= max_rounds:
        deal_cards(cards_dealt)  
    else:
        # Koniec gry
        final_message = f"Koniec gry! Wynik końcowy: Gracz 1: {player1_score}, Gracz 2: {player2_score}"
        if player1_score > player2_score:
            final_message += " - Wygrywa AI!"
        elif player2_score > player1_score:
            final_message += " - Wygrywasz!"
        else:
            final_message += " - Remis!"
        current_state = "end_screen"


# Główna pętla gry
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_state == "menu" and play_button.collidepoint(event.pos):
                current_state = "game"
                current_round = 1
                player1_score = 0
                player2_score = 0
                player1_collected = []
                player2_collected = []
                result_message = ""
                
                # Inicjalizacja talii i rozdanie kart
                initialize_deck()
                deal_cards(cards_dealt)


            elif current_state == "end_screen":
                if play_again_button.collidepoint(event.pos):
                    # Rozpocznij nową grę
                    current_state = "game"
                    current_round = 1
                    player1_score = 0
                    player2_score = 0
                    player1_collected = []
                    player2_collected = []
                    result_message = ""
                    
                    # Inicjalizacja talii i rozdanie kart
                    initialize_deck()
                    deal_cards(cards_dealt)
                    
                elif exit_button.collidepoint(event.pos):
                    # Wyjdź z gry
                    pygame.quit()
                    sys.exit()    

            elif current_state == "game" and player2_hand:
                mouse_x, mouse_y = event.pos
                spacing2 = 110
                start_x = WIDTH // 2 - (len(player2_hand) * spacing2 // 2)
                y2 = HEIGHT // 1.25

                for i, card_name in enumerate(player2_hand):
                    x = start_x + i * spacing2
                    rect = pygame.Rect(x, y2, 100, 150)
                    if rect.collidepoint(mouse_x, mouse_y):
                        last_card_in_round = (len(player2_hand) == 1)

                        # Zapisz ruch gracza tymczasowo
                        selected_card = card_name

                        # Stwórz kopie stanu gry zanim gracz zagra
                        temp_p2_hand = player2_hand.copy()
                        temp_p2_collected = player2_collected.copy()

                        # AI podejmuje decyzję przy pełnej ręce gracza
                        if len(player1_hand) == 1:
                            p1_card = player1_hand[0]
                        else:
                            _, p1_card = minimax(player1_hand, temp_p2_hand, player1_collected, temp_p2_collected, 6)

                        # Teraz wykonaj rzeczywiste zagrania obu graczy
                        if p1_card and p1_card in player1_hand:
                            player1_hand.remove(p1_card)
                            player1_collected.append(p1_card)

                        player2_hand.remove(selected_card)
                        player2_collected.append(selected_card)

                        # Sprawdzenie końca rundy
                        if not player1_hand or not player2_hand:
                            end_round()
                        else:
                            pass_cards()

                        break



    # Rysowanie aktualnego stanu gry
    if current_state == "menu":
        draw_menu()
    elif current_state == "end_screen":
        draw_end_screen()
    else:
        draw_game()
        
    pygame.display.flip()
    clock.tick(60)