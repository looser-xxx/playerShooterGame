# Vampire Shooter (Survivor)

## Project Overview
This is a 2D top-down shooter/survivor game built using Python and **Pygame Community Edition (pygame-ce)**. The project is structured with the main source code in the root directory and assets organized into specific folders.

**Key Technologies:**
*   **Language:** Python 3.14 (inferred from venv)
*   **Library:** Pygame CE (imported as `pygame`)

## Project Structure

*   **`main.py`**: The entry point of the application. Contains the `Game` class and the main game loop.
*   **`player.py`**: Contains the `Player` class, handling player input, movement, and sprite management.
*   **`settings.py`**: Configuration file containing global variables like window dimensions and tile size.
*   **`code/`**: Contains alternative or backup source files (`main.py`, `settings.py`). *Note: The active development seems to be in the root directory.*
*   **`venv/`**: Python virtual environment.
*   **Assets:**
    *   `audio/`: Sound effects and music.
    *   `data/`: Map data (Tiled `.tmx`) and tilesets.
    *   `images/`: Sprites for enemies, gun, and player animations.

## Building and Running

1.  **Activate Virtual Environment:**
    ```bash
    source venv/bin/activate
    ```
2.  **Run the Game:**
    ```bash
    python main.py
    ```

## Development Conventions

*   **Entry Point:** The game is initialized via `if __name__ == "__main__":` in `main.py`.
*   **Classes:** Game entities (like `Player`) inherit from `pygame.sprite.Sprite`.
*   **State Management:** The `Game` class manages the display surface, clock, and sprite groups.
*   **Settings:** Constants are imported from `settings.py` using `from settings import *`.
*   **Input Handling:** Player input is handled within the `Player` class's `input` method.
*   **Typing:** Basic type hinting is used (e.g., `-> None`).
