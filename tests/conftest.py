import pytest
import os
import tempfile
from PIL import Image
import numpy as np

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    return img

@pytest.fixture
def sample_image_array():
    """Create a sample image as numpy array."""
    # Create a simple RGB image array
    img_array = np.zeros((100, 100, 3), dtype=np.uint8)
    img_array[:, :, 0] = 255  # Red channel
    return img_array