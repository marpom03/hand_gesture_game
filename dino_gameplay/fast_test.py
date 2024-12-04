import cv2
import mediapipe as mp
import time

# Importowanie Gesture Recognizer
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Ścieżka do modelu
model_path = "/home/martusia/PycharmProjects/dino_gameplay/gesture_recognizer _final_version2.task"

# Liczniki dla gestów
pointer_count = 0
pointer_processing_time = 0

open_hand_count = 0
open_hand_processing_time = 0

# Globalne zmienne do wyświetlania
last_gesture = "Brak gestu"
last_processing_time = 0.0

# Funkcja callback do obsługi wyników
def gesture_callback(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global pointer_count, pointer_processing_time
    global open_hand_count, open_hand_processing_time
    global last_gesture, last_processing_time

    # Pobranie aktualnego czasu
    current_time = time.time()

    if result.gestures:
        gesture_name = result.gestures[0][0].category_name
        processing_time = current_time - start_time

        # Obsługa gestów
        if gesture_name == "pointer":
            pointer_count += 1
            pointer_processing_time += processing_time

        elif gesture_name == "open_hand":
            open_hand_count += 1
            open_hand_processing_time += processing_time

        # Zapis do wyświetlania
        last_gesture = gesture_name
        last_processing_time = processing_time

        # Wyświetlenie w terminalu
        print(f"Gest: {gesture_name}, Czas przetwarzania: {processing_time * 1000:.2f} ms")

# Konfiguracja modelu
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=gesture_callback,
)

# Inicjalizacja Gesture Recognizer
recognizer = GestureRecognizer.create_from_options(options)

# Kamera
cap = cv2.VideoCapture(0)

print("Rozpoczynam pomiar szybkości...")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Konwersja obrazu na RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Tworzenie obiektu MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Zmierz czas rozpoczęcia dla tej klatki
        start_time = time.time()

        # Przesyłanie obrazu do modelu
        timestamp_ms = int(time.time() * 1000)
        recognizer.recognize_async(mp_image, timestamp_ms)

        # Wyświetlanie rozpoznanego gestu i czasu na obrazie
        cv2.putText(
            frame,
            f"Gest: {last_gesture}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        cv2.putText(
            frame,
            f"Czas: {last_processing_time * 1000:.2f} ms",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Wyświetlanie obrazu
        cv2.imshow("Gesture Recognition", frame)

        # Przerwij po naciśnięciu 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()

    # Obliczanie średniej latencji i FPS dla każdego gestu
    if pointer_count > 0:
        avg_pointer_time = (pointer_processing_time / pointer_count) * 1000  # w ms
        pointer_fps = pointer_count / pointer_processing_time
        print(f"Pointer - Średni czas przetwarzania: {avg_pointer_time:.2f} ms")
        print(f"Pointer - Średnia liczba FPS: {pointer_fps:.2f}")
    else:
        print("Pointer - Brak danych do obliczenia.")

    if open_hand_count > 0:
        avg_open_hand_time = (open_hand_processing_time / open_hand_count) * 1000  # w ms
        open_hand_fps = open_hand_count / open_hand_processing_time
        print(f"Open Hand - Średni czas przetwarzania: {avg_open_hand_time:.2f} ms")
        print(f"Open Hand - Średnia liczba FPS: {open_hand_fps:.2f}")
    else:
        print("Open Hand - Brak danych do obliczenia.")
