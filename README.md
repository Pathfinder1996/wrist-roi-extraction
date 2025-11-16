## Region of Interest (ROI) Extraction for Wrist Vein Imaging

This repository provides a Python implementation of the wrist Region of Interest (ROI) extraction algorithm used in our wrist vein verification system.

## Contents
- `wrist_roi_extraction.py` - Main ROI extraction script.
- `requirements.txt` - Python 3.9.2 dependency list.
 
## Sample Results (Left Wrist Example) (Click the thumbnails to enlarge)
| Input Image | 1. Padding (80 px) | 2. Otsu Thresholding |
|-------------|--------------|-------------------|
| <img src="image/001_L_M_S1_01.png" width="250"/> | <img src="image/padded_image.png" width="250"/> | <img src="image/thresholded_image.png" width="250"/> |

| 3. Largest Contour| 4. Convex Hull | 5. Major Defects (P1 & P2) |
|---------------|------------|----------------|
| <img src="image/contour_image.png" width="250"/> | <img src="image/hull_image.png" width="250"/> | <img src="image/defects_image.png" width="250"/> |

| 6. Key Vectors & Perpendicular Line | 7. Compute P7 | 8. Compute P8 |
|---------------|------------|----------------|
| <img src="image/lines_image.png" width="250"/> | <img src="image/P7_image.png" width="250"/> | <img src="image/P8_image.png" width="250"/> |

| 9. Compute P9 | 10. Cross-Product Direction | 11. Scaled ROI |
|---------------|------------|----------------|
| <img src="image/P9_image.png" width="250"/> | <img src="image/angle_direction_image.png" width="250"/> | <img src="image/scaled_ROI_image.png" width="250"/> |

| 12. Final ROI (64×64) |
|---------------|
| <img src="image/ROI.png" width="250"/> |

## How to Use
Install required Python 3.9.2 packages:
```
pip install -r .\requirements.txt
```
Set the `captured_img` variable in `wrist_roi_extraction.py` to your test image, then run:
```
python .\wrist_roi_extraction.py
```

## Limitations
1. Fixed wrist insertion direction
   - The algorithm currently assumes the wrist enters from the opening side of the imaging device (‵ㄇ‵-shaped structure). It does not support arbitrary wrist orientations.
2. Requires a completely black background
   - The algorithm relies on background–foreground separation using Otsu’s thresholding. Complex or non-uniform backgrounds may cause segmentation failure.
