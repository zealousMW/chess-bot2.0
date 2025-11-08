# Chess Bot — Educational, Research & Demo

Important: This project is an educational demonstration of vision + ML + chess-engine integration. It is NOT intended or supported for cheating on live game platforms (e.g., chess.com, lichess). Use responsibly and only where allowed (local practice, research, self-play, learning).

## What this project is

A small research/demo codebase that shows how to combine computer vision (a Keras model) with a chess engine (Stockfish) and a simple UI to detect board state from screen captures and suggest/execute moves.

Key components
- `codes/capture.py` — calibration UI to select the board region and helpers to grab screenshots.
- `codes/model_wrapper.py` — loads a Keras model (default `model4.0.h5`) and predicts the piece on each 8x8 square.
- `codes/engine.py` — Stockfish wrapper with runtime-configurable engine parameters (Hash, Threads) and a simple click executor.
- `codes/chessbot_core.py` — orchestration layer that ties capture → model → engine together.
- `codes/app.py` — a Tkinter GUI to calibrate, detect, ask for suggestions and (optionally) execute the move.
- `codes/chess_bot_need.py` and `codes/utils.py` — small helpers (board→FEN conversion, etc.).

Files moved to `research/` are legacy scripts, experiments, and training notebooks preserved for reference.

## How AI is used here (proposals and ideas)

This project uses a per-square image classification model (Keras) to detect which piece occupies each square. Here are ways AI can be used and improved:

- Per-square classification (current): small CNN predicts one of {., r, n, b, k, q, p, R, N, B, K, Q, P} per tile.
- End-to-end board detection: use a segmentation or object-detection model to detect board corners and piece bounding boxes (more robust to perspective).
- Orientation / side-to-move detection: train a small classifier to determine whether the board in the image is aligned with White at bottom or Black at bottom.
- Confidence / uncertainty: expose per-square softmax/confidence values to flag low-confidence boards for human review.
- Post-processing with chess rules: combine ML output with a chess rules model (legal move checks) to correct improbable classifications.
- Training & augmentation: use the `dataset/` (labeled folders) to retrain/finetune the model, add synthetic augmentations (lighting, rotation, occlusion) to improve robustness.

Possible research directions
- Replace per-square classifier with a transformer-based image model for better contextual predictions.
- Use an OCR-style pipeline to recognize coordinates and board edges automatically.
- Create a self-play evaluation loop: detect board → propose move → execute on another UI → capture next state → use as weak supervision.

## Quick start (Windows PowerShell)

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Launch the GUI (calibrate first):

```powershell
python -m codes.app
```

3. Recommended workflow in the UI
- Click `Calibrate (select board)` and draw a rectangle around the chessboard when the translucent screen appears. Coordinates are saved to `codes/calib.json`.
- Click `Detect board` to capture the board image and run the model. The UI log shows the 8×8 matrix and a generated FEN string.
- Click `Suggest move` to ask Stockfish for a recommended move.
- If you understand and trust the suggestion, click `Execute move` to have the app click the start/end squares on-screen. There is also an Engine settings row (Hash / Threads) so you can tune Stockfish performance.

Notes
- The default Stockfish binary path is `stockfish_15.1_win_x64_avx2/sk.exe` within the repository. Change the path in `codes/engine.py` or pass a custom path when instantiating the engine in code.
- Model files (e.g. `model4.0.h5`) are large; loading the model may take a few seconds and requires sufficient memory.

## Safety, ethics & legal

This repository is intended for personal learning, research, and offline analysis. Do not use it to gain unfair advantage in online play or to violate the terms of service of other platforms. Respect the rules and fair-play policies of any service.

## Development & testing

- Unit tests live in `tests/` (simple checks such as board→FEN conversion). Run `pytest` for tests.
- Training data is stored in `dataset/` (structured by classes) — use it to train or fine-tune models. Legacy/exports are in `research/`.

## Where to add images (placeholders)

Add example images/screenshots into `docs/images/` (create the folder) then replace these placeholders in README with real images:

![Calibration placeholder](docs/images/calibration-placeholder.png)

![Detect board placeholder](docs/images/detect-placeholder.png)

![Suggest move placeholder](docs/images/suggest-placeholder.png)

## Next steps & contributions

- I can add a persisted engine config, safety confirmation before clicking, automatic orientation detection, or a small evaluation harness that runs model predictions on a set of saved screenshots and produces accuracy/precision reports. Tell me which feature you want next and I'll implement it.

## License & credits

Check the included Stockfish license in the `stockfish_15.1_win_x64_avx2` folder. The remaining code is provided as-is for educational use.
