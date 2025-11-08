# Chess Bot

AI-powered chess assistant using computer vision and Stockfish.

This project combines computer vision, deep learning (Keras), and the Stockfish chess engine to detect a chess position from your screen and suggest or execute the best move. It’s built for research, experimentation, and self-play — not for online cheating.

## Features

- Simple UI (Tkinter) for calibration, detection, and engine control
- AI model predicts which piece is on each square using a trained Keras model
- Automatic FEN generation from detected board positions
- Stockfish integration for move suggestions and engine tuning
- Auto-click execution of moves on your local board using `pyautogui`
- Calibration system to match screen coordinates
- Minimal tests and research scripts included

![ezgif-567c6f3fc1cb40d2](https://github.com/user-attachments/assets/0baecec4-85d2-41ff-b309-c0884d32799c)


## How it works

1. Calibrate the board using the UI to mark the on-screen board region. Calibration data saved to `codes/calib.json`.
2. Capture a screenshot of the calibrated region and slice it into 8×8 tiles.
3. Predict pieces on each tile using the Keras model (`model4.0.h5`).
4. Convert the prediction matrix into a FEN string.
5. Ask Stockfish for the best move given the FEN and the selected side.
6. Optionally execute the move via automated clicks (flipped if running as Black when calibrated for White).

## Model details

- Model type: square-wise classifier (one prediction per board square)
- Classes:
  - `.` (empty)
  - `p r n b q k` (black pieces)
  - `P R N B Q K` (white pieces)
- Model file: `model4.0.h5` (root directory)
- For customization or retraining see `codes/model_wrapper.py`.

## Engine integration

- Uses Stockfish 15.1 (binary included)
- Default binary path: `stockfish_15.1_win_x64_avx2/sk.exe`
- Engine settings adjustable at runtime via UI: hash (MB), threads
- Change the binary path in `codes/engine.py` if needed.

## Orientation & side selection

- Choose your side (White / Black) in the UI before asking for moves.
- Calibration assumes White is at the bottom. If you play as Black, clicks need flipping.
- Planned improvements:
  - Automatic click flipping when “Black” is selected
  - Automatic orientation detection via image analysis

## Calibration

- Calibration data saved to `codes/calib.json`.
- Re-run calibration if you change screen resolution or move the app window.

## How to run (Windows PowerShell)

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Launch the app:

   ```powershell
   python -m codes.app
   ```

## Tests & quick checks

- Run unit tests:

  ```powershell
  pytest tests/
  ```

- Import check:

  ```powershell
  python -c "import importlib; importlib.import_module('codes.app'); print('OK')"
  ```

## Troubleshooting

- Missing `python-chess`: `pip install python-chess`
- Stockfish not found: update path in `codes/engine.py`
- Clicks go to wrong squares: flip orientation manually or enable flip logic
- TensorFlow warnings are usually informational

## License & credits

- Stockfish distributed under its own license (`stockfish_15.1_win_x64_avx2/COPYING.txt`)
- Rest of the project intended for educational and research use only
