import os
import numpy as np
from tensorflow.keras.models import load_model
from typing import List


class ModelWrapper:
    """Load Keras model and predict piece per square.

    Usage:
        mw = ModelWrapper(model_path)
        matrix = mw.predict_board(img)  # returns list[list[str]] 8x8
    """

    def __init__(self, model_path: str = None):
        if model_path is None:
            # default to project root model4.0.h5
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            model_path = os.path.join(base, 'model4.0.h5')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")
        self.model = load_model(model_path)
        # mapping index -> piece symbol used in original project
        self.cp = ['.', 'r', 'n', 'b', 'k', 'q', 'p', 'R', 'N', 'B', 'K', 'Q', 'P']

    def _slice_board(self, img: np.ndarray) -> np.ndarray:
        # img expected shape (H, W, 3), square board (e.g. 800x800)
        h, w = img.shape[:2]
        assert h == w, "Input image must be square"
        sq = h // 8
        squares = []
        # row-major: top row -> rank 8
        for row in range(8):
            for col in range(8):
                y0 = row * sq
                x0 = col * sq
                tile = img[y0:y0 + sq, x0:x0 + sq]
                squares.append(tile)
        arr = np.stack(squares, axis=0).astype('float32') / 255.0
        return arr

    def predict_board(self, img: np.ndarray) -> List[List[str]]:
        """Return 8x8 matrix of piece symbols (rows top->bottom).
        """
        arr = self._slice_board(img)
        preds = self.model.predict(arr, verbose=0)
        idx = np.argmax(preds, axis=1)
        pieces = [self.cp[i] for i in idx]
        # group into 8 rows
        matrix = [pieces[i:i + 8] for i in range(0, 64, 8)]
        return matrix
