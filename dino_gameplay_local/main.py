import pygame
import cv2
import time
import threading
import random
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions
import os
import queue
import sys  # Dodano import sys

# Inicjalizacja Pygame
pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100

# Ustal poziom ziemi
GROUND = 380  # Y-position dla ziemi

# Okno gry
GAME_SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game with Gesture Recognition")

# Funkcja do ładowania obrazów z obsługą błędów
def load_image(path):
    try:
        image = pygame.image.load(path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Nie można załadować obrazu {path}: {e}")
        pygame.quit()
        sys.exit()  # Zakończ program, jeśli obraz się nie załaduje

# Załaduj wszystkie obrazy
RUNNING = [
    load_image(os.path.join("Assets", "Dino", "DinoRun1.png")),
    load_image(os.path.join("Assets", "Dino", "DinoRun2.png"))
]
JUMPING = load_image(os.path.join("Assets", "Dino", "DinoJump.png"))
DUCKING = [
    load_image(os.path.join("Assets", "Dino", "DinoDuck1.png")),
    load_image(os.path.join("Assets", "Dino", "DinoDuck2.png"))
]

SMALL_CACTUS = [
    load_image(os.path.join("Assets", "Cactus", "SmallCactus1.png")),
    load_image(os.path.join("Assets", "Cactus", "SmallCactus2.png")),
    load_image(os.path.join("Assets", "Cactus", "SmallCactus3.png"))
]
LARGE_CACTUS = [
    load_image(os.path.join("Assets", "Cactus", "LargeCactus1.png")),
    load_image(os.path.join("Assets", "Cactus", "LargeCactus2.png")),
    load_image(os.path.join("Assets", "Cactus", "LargeCactus3.png"))
]

BIRD = [
    load_image(os.path.join("Assets", "Bird", "Bird1.png")),
    load_image(os.path.join("Assets", "Bird", "Bird2.png"))
]

CLOUD = load_image(os.path.join("Assets", "Other", "Cloud.png"))
BG = load_image(os.path.join("Assets", "Other", "Track.png"))

# Klasa Dinozaura
class Dinosaur:
    X_POS = 80
    JUMP_VEL = 15  # Zwiększona prędkość skoku
    GRAVITY = 1    # Grawitacja
    DUCK_DURATION = 200  # Czas trwania uniku w milisekundach

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.bottom = GROUND  # Ustawienie dolnej krawędzi na poziom ziemi

        self.last_duck_gesture_time = 0  # Czas ostatniego gestu kucania

    def update(self, user_input):
        current_time = pygame.time.get_ticks()

        # Obsługa wejścia gestów i klawiatury
        if isinstance(user_input, str):
            # Obsługa gestów
            if user_input == "open_hand" and not self.dino_jump:
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
                self.last_duck_gesture_time = 0  # Reset kucania
                print("Rozpoczęto skok przez gest 'open_hand'")
            elif user_input == "pointer" and not self.dino_jump:
                self.dino_duck = True
                self.dino_run = False
                self.dino_jump = False
                self.last_duck_gesture_time = current_time  # Zapisz czas gestu
                print("Rozpoczęto kucanie przez gest 'pointer'")
            else:
                if not self.dino_jump and (current_time - self.last_duck_gesture_time) > self.DUCK_DURATION:
                    self.dino_duck = False
                    self.dino_run = True
        elif isinstance(user_input, pygame.key.ScancodeWrapper):
            # Obsługa klawiatury
            if user_input[pygame.K_UP] and not self.dino_jump:
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
                self.last_duck_gesture_time = 0  # Reset kucania
                print("Rozpoczęto skok przez klawisz 'UP'")
            elif user_input[pygame.K_DOWN] and not self.dino_jump:
                self.dino_duck = True
                self.dino_run = False
                self.dino_jump = False
                print("Rozpoczęto kucanie przez klawisz 'DOWN'")
            else:
                if not self.dino_jump and not user_input[pygame.K_DOWN] and (current_time - self.last_duck_gesture_time) > self.DUCK_DURATION:
                    self.dino_duck = False
                    self.dino_run = True

        # Obsługa gestu kucania
        if self.dino_duck and not self.dino_jump:
            if isinstance(user_input, str) and user_input == "pointer":
                # Gest jest aktywny, kontynuuj kucanie
                self.last_duck_gesture_time = current_time
            elif isinstance(user_input, pygame.key.ScancodeWrapper) and user_input[pygame.K_DOWN]:
                # Klawisz jest przytrzymany, kontynuuj kucanie
                pass
            else:
                # Sprawdź, czy gest minął
                if (current_time - self.last_duck_gesture_time) > self.DUCK_DURATION:
                    self.dino_duck = False
                    self.dino_run = True
                    print("Kucanie zakończone")

        # Resetowanie kroków animacji
        if self.step_index >= 10:
            self.step_index = 0

        # Aktualizacja animacji i ruchu
        if self.dino_duck and not self.dino_jump:
            self.duck()
        elif self.dino_run and not self.dino_jump:
            self.run()
        elif self.dino_jump:
            self.jump()

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        # Ustawienie nowego rect i wyrównanie do poziomu ziemi
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.bottom = GROUND  # Ustawienie dolnej krawędzi na poziom ziemi
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        # Ustawienie nowego rect i wyrównanie do poziomu ziemi
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.bottom = GROUND  # Ustawienie dolnej krawędzi na poziom ziemi
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        self.dino_rect.y -= self.jump_vel
        self.jump_vel -= self.GRAVITY

        if self.dino_rect.bottom >= GROUND:
            self.dino_rect.bottom = GROUND
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            print("Dino zakończył skok i wrócił na ziemię")

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

# Klasa Przeszkód
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self, game_speed):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            if self in obstacles:
                obstacles.remove(self)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
        # Tymczasowo dodaj prostokąt do debugowania
        # pygame.draw.rect(SCREEN, (0, 255, 0), self.rect, 2)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325  # Dostosuj w zależności od grafiki

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300  # Dostosuj w zależności od grafiki

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250  # Dostosuj w zależności od grafiki
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 10:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        # Tymczasowo dodaj prostokąt do debugowania
        # pygame.draw.rect(SCREEN, (0, 255, 0), self.rect, 2)
        self.index += 1

# Klasa Chmury
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self, game_speed):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))
        # Tymczasowo dodaj prostokąt do debugowania
        # pygame.draw.rect(SCREEN, (0, 0, 255), self.image.get_rect(topleft=(self.x, self.y)), 2)

# Klasa do Rozpoznawania Gestów
class GestureRecognizerThread(threading.Thread):
    def __init__(self, gesture_callback, frame_queue):
        threading.Thread.__init__(self)
        self.gesture_callback = gesture_callback
        self.running = True
        self.frame_queue = frame_queue

        # Ścieżka do modelu
        model_path = 'gesture_recognizer_final_version.task'

        # Ustawienia dla rozpoznawacza gestów
        options = vision.GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=self.process_result
        )

        # Tworzymy obiekt rozpoznawacza gestów
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def process_result(self, result, output_image, timestamp_ms):
        try:
            if result.gestures:
                for gesture_list in result.gestures:
                    for gesture in gesture_list:
                        gesture_input = None
                        if gesture.category_name == 'open_hand':
                            gesture_input = 'open_hand'
                        elif gesture.category_name == 'pointer':
                            gesture_input = 'pointer'

                        if gesture_input:
                            print(f"Odebrano gest: {gesture_input}")
                            self.gesture_callback(gesture_input)
        except AttributeError as e:
            print(f"Nieprawidłowy atrybut gestu: {e}")
        except Exception as e:
            print(f"Nieoczekiwany błąd w process_result: {e}")

    def run(self):
        while self.running:
            try:
                frame = self.frame_queue.get(timeout=1)
            except queue.Empty:
                continue

            # Konwersja obrazu z OpenCV (BGR) na format RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            timestamp_ms = int(time.time() * 1000)

            # Rozpoznawanie gestów
            self.recognizer.recognize_async(mp_image, timestamp_ms)

    def stop(self):
        self.running = False
        self.recognizer.close()

# Funkcja callback do obsługi gestów
def handle_gesture(gesture):
    global gesture_input
    gesture_input = gesture

# Globalna zmienna do przechowywania aktualnego gestu
gesture_input = None

# Create frame_queue
frame_queue = queue.Queue(maxsize=1)

# Initialize GestureRecognizerThread with frame_queue
gesture_thread = GestureRecognizerThread(handle_gesture, frame_queue)
gesture_thread.start()

# Funkcja gry
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, gesture_input

    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = GROUND
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    cloud = Cloud()

    # Surface do wyświetlania kamery
    camera_width, camera_height = 160, 120  # Mniejszy rozmiar
    camera_position = (10, 10)  # Lewy Górny Róg

    # Initialize camera capture
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    # If you are using Linux uncomment line below  
    #cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("Nie udało się otworzyć kamery.")
        gesture_thread.stop()
        pygame.quit()
        sys.exit()

    def score_function():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        GAME_SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        GAME_SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        GAME_SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            GAME_SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Capture frame for gesture recognition
        ret, frame = cap.read()
        if ret:
            if not frame_queue.full():
                frame_queue.put(frame)
            latest_frame = frame  # Keep the latest frame for display

        # Aktualizacja dinozaura na podstawie gestu
        if gesture_input:
            player.update(gesture_input)
            gesture_input = None  # Reset po obsłużeniu gestu
        else:
            # Jeśli nie ma gestu, użyj domyślnego sterowania klawiaturą
            userInput = pygame.key.get_pressed()
            player.update(userInput)

        # Czyszczenie ekranu
        GAME_SCREEN.fill((255, 255, 255))

        # Rysowanie tła
        background()

        # Rysowanie chmur
        cloud.draw(GAME_SCREEN)
        cloud.update(game_speed)

        # Rysowanie gracza
        player.draw(GAME_SCREEN)

        # Rysowanie i aktualizacja przeszkód
        if len(obstacles) == 0:
            obstacle_type = random.randint(0, 2)
            if obstacle_type == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
                print("Dodano SmallCactus")
            elif obstacle_type == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
                print("Dodano LargeCactus")
            elif obstacle_type == 2:
                obstacles.append(Bird(BIRD))
                print("Dodano Bird")

        for obstacle in obstacles[:]:  # Iteruj po kopii listy
            obstacle.draw(GAME_SCREEN)
            obstacle.update(game_speed)
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        # Aktualizacja wyniku
        score_function()

        # Wyświetlanie podglądu kamery w lewym górnym rogu
        if 'latest_frame' in locals():
            # Konwersja obrazu z OpenCV (BGR) na Pygame (RGB)
            frame_rgb = cv2.cvtColor(latest_frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (camera_width, camera_height))
            frame_surface = pygame.surfarray.make_surface(frame_resized)
            # Rotacja i flip, aby pasowały do Pygame
            frame_surface = pygame.transform.rotate(frame_surface, -90)
            frame_surface = pygame.transform.flip(frame_surface, True, False)
            # Blit do ekranu
            GAME_SCREEN.blit(frame_surface, camera_position)

        # Aktualizacja ekranu
        pygame.display.update()

        # Kontrola szybkości gry
        clock.tick(30)

    # Czyszczenie po zakończeniu głównego loopa
    pygame.quit()
    cap.release()
    gesture_thread.stop()
    sys.exit()  # Zakończ program

# Funkcja menu
def menu(death_count):
    global points, gesture_input
    run = True
    while run:
        GAME_SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score_text = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score_text.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            GAME_SCREEN.blit(score_text, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        GAME_SCREEN.blit(text, textRect)
        GAME_SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gesture_thread.stop()  # Zatrzymaj wątek rozpoznawania gestów
                pygame.quit()
                sys.exit()  # Zakończ program
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.USEREVENT:
                gesture_input = None  # Resetowanie gestu przed nową grą
                main()

if __name__ == "__main__":
    menu(death_count=0)
