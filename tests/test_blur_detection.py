import pytest
import numpy as np
from app.utils.blur_detection import blur_score

def test_blur_score_clear_image(sample_image_array):
    """Test blur score on a clear image."""
    score = blur_score(sample_image_array)
    assert isinstance(score, (int, float))
    assert score >= 0

def test_blur_score_blurry_image():
    """Test blur score on a blurry image."""
    # Create a blurry image by averaging
    blurry_img = np.ones((100, 100, 3), dtype=np.uint8) * 128
    score = blur_score(blurry_img)
    assert isinstance(score, (int, float))
    assert score >= 0

def test_blur_score_none_image():
    """Test blur score with None input."""
    score = blur_score(None)
    assert score == 0.0