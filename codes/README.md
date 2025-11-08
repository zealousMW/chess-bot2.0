# Chess Bot (refactored)

This folder contains a refactored, modular version of the original chess bot.

Files of interest

- `capture.py` - calibration UI and screen capture helper
- `model_wrapper.py` - loads the Keras model and predicts an 8x8 matrix of pieces
- `engine.py` - Stockfish wrapper and pyautogui-based executor
- `chessbot_core.py` - high-level orchestration
- `app.py` - simple Tkinter UI (entrypoint)

How to use (Windows)

1. Install dependencies: TensorFlow, OpenCV (optional), pyautogui, stockfish Python wrapper, Pillow, python-chess.
2. Run `python -m codes.app` to start the UI.
3. Click "Calibrate" and draw a rectangle around the chessboard; coordinates are saved.
4. Click "Detect board" to run the model and show the board and FEN.
5. Click "Suggest move" to ask Stockfish for a move.
6. Click "Execute move" to perform the clicks on the screen (be ready to allow the bot to click).

Notes

- This keeps the existing model (`model4.0.h5`) and Stockfish binary path. Adjust paths if your files are elsewhere.
- The code re-uses `chess_bot_need.board_to_fen` for FEN conversion.
