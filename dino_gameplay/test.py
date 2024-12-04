import cv2
import mediapipe as mp
import time

# Importowanie wymaganych klas z MediaPipe
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Przechowywanie ostatniego rozpoznanego gestu
recognized_gesture = "Brak gestu"

# Funkcja callback do wyświetlania wyników rozpoznawania gestów
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global recognized_gesture
    if result.gestures:
        gesture = result.gestures[0][0]  # Najbardziej prawdopodobny gest
        recognized_gesture = f"{gesture.category_name} ({gesture.score:.2f})"
    else:
        recognized_gesture = "Brak rozpoznanych gestow"

# Funkcja główna
def main():
    global recognized_gesture

    # Ścieżka do pliku modelu MediaPipe Gesture Recognizer
    model_path = '/home/martusia/PycharmProjects/dino_gameplay/gesture_recognizer_final_version.task'  # Podmień na faktyczną ścieżkę do modelu

    # Konfiguracja GestureRecognizer
    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result
    )

    # Inicjalizacja GestureRecognizer w bloku with
    with GestureRecognizer.create_from_options(options) as recognizer:
        # Uruchomienie kamery przy użyciu OpenCV
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # 0 to indeks pierwszej kamery (domyślnej)

        # Ustawienia kamery
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Sprawdzenie, czy kamera została otwarta poprawnie
        if not cap.isOpened():
            print("Nie można otworzyć kamery.")
            return

        print("Nacisnij 'q', aby zakonczyć program.")

        while True:
            # Odczyt klatki z kamery
            ret, frame = cap.read()
            if not ret:
                print("Nie udalo sie odczytac klatki z kamery.")
                break

            # Konwersja obrazu OpenCV (BGR) na format RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Tworzenie obiektu MediaPipe Image
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # Obliczanie znacznika czasu w milisekundach
            timestamp_ms = int(time.time() * 1000)

            # Rozpoznawanie gestów w czasie rzeczywistym
            recognizer.recognize_async(mp_image, timestamp_ms)

            # Wyświetlanie wyniku na obrazie
            cv2.putText(
                frame,
                recognized_gesture,
                (10, 50),  # Pozycja tekstu na obrazie
                cv2.FONT_HERSHEY_SIMPLEX,
                1,  # Rozmiar czcionki
                (0, 255, 0),  # Kolor tekstu (zielony)
                2,  # Grubość tekstu
                cv2.LINE_AA
            )

            # Wyświetlanie obrazu w oknie OpenCV
            cv2.imshow('Gesture Recognition', frame)

            # Wyjście z pętli po naciśnięciu klawisza 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Zwolnienie zasobów
        cap.release()
        cv2.destroyAllWindows()

# Wywołanie funkcji głównej
if __name__ == "__main__":
    main()
