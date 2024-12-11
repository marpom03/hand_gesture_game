# Instrukcja uruchomienia lokalnej gry Dino Chrome kontrolowanej gestami

Poniżej znajduje się instrukcja, jak uruchomić lokalną wersję gry **Dino** w Pythonie, sterowaną gestami. Gra jest oparta na bibliotece **Pygame** i wykorzystuje model **MediaPipe** do rozpoznawania gestów rąk.

### 1. Sklonowanie repozytorium

Najpierw musisz sklonować repozytorium na swoje urządzenie:


`git clone https://github.com/marpom03/hand_gesture_game.git`
`cd hand_gesture_game/dino_gameplay_local`



### 2. Instalacja zależności

Upewnij się, że masz zainstalowanego Pythona oraz wszystkie niezbędne biblioteki. Jeżeli nie masz ich zainstalowanych, użyj poniższej komendy:


`pip install pygame opencv-python mediapipe`

**UWAGA!**
Ważna jest odpowiednia wersja Pythona, którą obsługuje MediaPipe. Musisz używać wersji **Pythona 3.7** lub nowszej w wersji **64 bitowej**.

### 3. Dla użytkowników Linuxa

Gra jest napisana pod Windowsa - jest jedna funkcja, która działa tylko na Windowsie. Jeśli korzystasz z Linuxa przed uruchomieniem gry wyświetl kod i zakomentuj linię 350 i odkomentuj linię pod nią. Dzięki temu gra będzie miała dostęp do kamery. 

Zakomentuj to:

` cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) `

Odkomentuj to:

` cap = cv2.VideoCapture(0, cv2.CAP_V4L2) `

### 4. Uruchomienie gry

Aby uruchomić grę, wykonaj poniższą komendę w terminalu:

`python3 main.py`


Gra uruchomi okno Pygame i zacznie rozpoznawać gesty rąk, które będą kontrolować postać dinozaura. Kamera musi być włączona, aby system mógł rozpoznać gesty.

### 5. Sterowanie grą za pomocą gestów

Dostępne gesty:

-   **Gest "open_hand"** (otwarta dłoń) — powoduje skok dinozaura.
-   **Gest "pointer"** (wskazujący palec) — powoduje, że dinozaur schyla się (unika przeszkód).

System rozpozna te gesty i wyśle odpowiednie polecenia do gry:

-   Gest otwartej dłoni (`open_hand`) spowoduje, że dinozaur wykona skok.
-   Gest wskazującego palca (`pointer`) spowoduje, że dinozaur zacznie kucać.

### 6. Zakończenie gry

Aby zakończyć grę, wystarczy zamknąć okno Pygame lub nacisnąć `Ctrl+C` w terminalu.

----------

### Dodatkowe informacje:

-   Gra wyświetla kamerę w lewym górnym rogu, co pozwala śledzić rozpoznawane gesty na bieżąco.
-   Możesz przejść do menu gry po zakończeniu każdej rozgrywki, w którym możesz ponownie uruchomić grę.

