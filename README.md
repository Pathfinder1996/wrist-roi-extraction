## 📝 Wrist ROI(Region of Interest) Extraction
Python implementation of the wrist ROI(Region of Interest) extraction algorithm

### 📁 Contents
- `wrist_roi_extraction.py` - primary execution script.
- `requirements.txt` - lists environment dependencies.
 
## 📊 Sample Result
| Input Image | 1. Padded Image | 2. Thresholded Image |
|-------------|--------------|-------------------|
| <img src="image/001_L_M_S1_01.png" width="250"/> | <img src="image/padded_image.png" width="250"/> | <img src="image/thresholded_image.png" width="250"/> |

| 3. Contour Image | 4. Hull Image | 5. Defects Image |
|---------------|------------|----------------|
| <img src="image/contour_image.png" width="250"/> | <img src="image/hull_image.png" width="250"/> | <img src="image/defects_image.png" width="250"/> |

| 6. Line Image | 7. P7 Image | 8. P8 Image |
|---------------|------------|----------------|
| <img src="image/lines_image.png" width="250"/> | <img src="image/P7_image.png" width="250"/> | <img src="image/P8_image.png" width="250"/> |

| 9. P9 Image | 10. Angle Direction Image | 11. Scaled ROI Image |
|---------------|------------|----------------|
| <img src="image/P9_image.png" width="250"/> | <img src="image/angle_direction_image.png" width="250"/> | <img src="image/scaled_ROI_image.png" width="250"/> |

| 9. ROI Image |
|---------------|
| <img src="image/ROI.png" width="250"/> |

## 🚀 Getting Started
To set up the environment (optional if already installed), run:
```
pip install -r .\requirements.txt
```
Replace the image_path in vein_enhance.py with your input image path, then run:
```
python .\wrist_roi_extraction.py
```
