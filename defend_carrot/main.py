"""Entry point for the Defend the Carrot MVP.

    python main.py

Keys: Enter starts/continues, 1-3 or a card selects a fruit, left click
builds, right click cancels, I opens the guide, P pauses, Esc goes back.
"""

import sys


def self_test(report_path: str) -> int:
    """Exercise executable startup, building and rendering without a display."""
    import json
    import os
    import traceback
    from pathlib import Path

    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    report = {"game": "DefendCarrot", "frozen": bool(getattr(sys, "frozen", False))}
    try:
        import pygame
        import config as C
        from game import Game
        game = Game()
        assert game.state == "menu"
        game.draw()
        game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        game.coins = 1000
        for kind in C.SHOP_ORDER:
            col, row = next((col, row) for row in range(C.GRID_ROWS)
                            for col in range(C.GRID_COLS) if game.can_build(col, row))
            game.selected = kind
            game._on_click((col * C.TILE + C.TILE // 2,
                            C.HUD_H + row * C.TILE + C.TILE // 2))
        assert len(game.fruits) == len(C.SHOP_ORDER)
        for _ in range(180):
            game.update(1 / C.FPS)
            game.draw()
        pygame.quit()
        report.update(ok=True, fruits_built=len(game.fruits), frames_rendered=180)
    except Exception:
        report.update(ok=False, error=traceback.format_exc())
    Path(report_path).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if report["ok"] else 1


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] == "--self-test":
        sys.exit(self_test(sys.argv[2]))
    from game import Game
    Game().run()


if __name__ == "__main__":
    main()
