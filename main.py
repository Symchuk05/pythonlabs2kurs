# Точка входу в гру

import sys
from snake_game import SnakeGame
from snake_game.exceptions import GameError


def main() -> None:
    """Головна функція запуску гри"""
    try:
        game = SnakeGame()
        game.start()
    except GameError as e:
        print(f"\n❌ Game error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted by user!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
