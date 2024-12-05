# Instrukcja uruchomienia gry Dino Chrome kontrolowanej gestami na systemach Linux korzystając z gry dostępnej w przeglądarce

W tym repozytorium znajduje się projekt, który umożliwia sterowanie grą Dino Chrome za pomocą gestów rąk przy użyciu modelu MediaPipe. Poniżej znajduje się szczegółowa instrukcja krok po kroku, jak uruchomić grę i sterować nią za pomocą gestów.

### 1. Sklonowanie repozytorium
Pierwszym krokiem jest sklonowanie repozytorium na swoje urządzenie:

`git https://github.com/marpom03/hand_gesture_game.git`
`cd hand_gesture_game`

### 2. Instalacja zależności

Upewnij się, że masz zainstalowanego Pythona oraz wszystkie potrzebne biblioteki, jeżeli nie zainstaluj je:

`pip install opencv-python mediapipe pyautogui `

### 3. Przygotowanie uprawnień do symulacji klawiszy

Aby program mógł symulować naciśnięcia klawiszy w systemie Linux, należy zmienić odpowiednie uprawnienia. Wykonaj poniższą komendę w terminalu:

`xhost +`

Ta komenda zezwoli na dostęp do urządzenia wejściowego (klawiatury) dla aplikacji działających na Twoim systemie. Możesz równie łatwo cofnąć to pozwolenie komendą: 

`xhost -`

### 4. Uruchomienie gry Dino Chrome

Otwórz grę Dino Chrome w przeglądarce. Możesz to zrobić, wpisując w pasku adresu przeglądarki:

`chrome://dino`

Gra powinna wyświetlić się na ekranie. Będziesz sterować nią za pomocą gestów rąk.

### 5. Uruchomienie programu

W terminalu, w folderze projektu, uruchom plik `gameplay.py`, który obsługuje rozpoznawanie gestów i sterowanie grą:

`python3 gameplay.py`

Program uruchomi kamerę i rozpocznie rozpoznawanie gestów. Kamera musi być włączona, aby system mógł rozpoznać gesty.

### 6. Sterowanie grą za pomocą gestów

Gest **"open_hand"** (otwarta dłoń) powoduje skok w grze. Aby skoczyć, wystarczy pokazać gest otwartej dłoni przed kamerą.
Gest **"pointer"** (wskazujący palec) spowoduje unik (schylenie się) w grze.

Program automatycznie rozpozna te gesty i wyśle odpowiednie polecenia do systemu, symulując naciśnięcie klawisza (**spacji dla skoku i strzałki w dół dla uniku**).

### 7. Zakończenie gry
Aby zakończyć program, naciśnij klawisz **q**. Program wtedy zamknie kamerę i zakończy działanie.


