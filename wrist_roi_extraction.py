import time

import cv2
import numpy as np

def line_intersection(p1, p2, p3, p4):
    """
    Calculate the intersection point of two lines (p1-p2) and (p3-p4)
    using the determinant method.
    """
    A1 = p2[1] - p1[1]
    B1 = p1[0] - p2[0]
    C1 = A1 * p1[0] + B1 * p1[1]
    
    A2 = p4[1] - p3[1]
    B2 = p3[0] - p4[0]
    C2 = A2 * p3[0] + B2 * p3[1]

    det = A1 * B2 - A2 * B1
    x = (B2 * C1 - B1 * C2) / det
    y = (A1 * C2 - A2 * C1) / det

    return (x.astype(int), y.astype(int))

def scale_point(p, center, scale):
    """
    Scale a point `p` with respect to `center` by a scaling factor `scale`.
    """
    return (p - center) * scale + center

# Image loading and preparation
start_time = time.time()

captured_img = cv2.imread("001_L_M_S1_01.png", cv2.IMREAD_GRAYSCALE)
h, w = captured_img.shape

# Add padding
img = np.zeros((h + 160, w + 160), dtype=np.uint8)
img[80:-80, 80:-80] = captured_img
cv2.imwrite("padded_image.png", img)

# Otsu binarization
_, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imwrite("thresholded_image.png", thresh)

# Extract contours and fill largest one
contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
max_contour = max(contours, key=cv2.contourArea)
mask = np.zeros_like(thresh)
cv2.drawContours(mask, [max_contour], -1, 255, thickness=cv2.FILLED)

# Compute centroid of the contour
cnt, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cnt = cnt[0]

img_c = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
img_cnt = cv2.drawContours(img_c, [cnt], 0, (0, 255, 0), 2)
cv2.imwrite("contour_image.png", img_cnt)

M = cv2.moments(cnt)
if M["m00"] != 0:
    x_c = int(M["m10"] / M["m00"])
    y_c = int(M["m01"] / M["m00"])
else:
    print("[Warning] Zero division in moments calculation")

# Find convexity defects
hull = cv2.convexHull(cnt, returnPoints=False)
defects = cv2.convexityDefects(cnt, hull)
sorted_defects = sorted(defects, key=lambda x: x[0][3], reverse=True)

# Draw convex hull, save the image
hull_points = cv2.convexHull(cnt, returnPoints=True)
img_hull = cv2.drawContours(img_c.copy(), [hull_points], 0, (255, 0, 0), 2)
cv2.imwrite("hull_image.png", img_hull)

# Extract the first and second maximum defects (P1, P2)
first_defect = sorted_defects[0][0]
s, e, f, _ = first_defect
P1, P3, P4 = tuple(cnt[f][0]), tuple(cnt[s][0]), tuple(cnt[e][0])
if P4[1] < P1[1]: P4, P3 = P3, P4
is_right = P1[0] > x_c

second_defect = None
for defect in sorted_defects[1:]:
    s, e, f, _ = defect[0]
    far_point = tuple(cnt[f][0])
    if (far_point[0] > x_c) != is_right:
        second_defect = defect
        break

s, e, f, _ = second_defect[0]
P2, P5, P6 = tuple(cnt[f][0]), tuple(cnt[s][0]), tuple(cnt[e][0])
if P5[1] < P2[1]: 
    P6, P5 = P5, P6

# Draw points and labels on the image
img_defects = img_c.copy()
cv2.circle(img_defects, P1, 5, (0, 0, 255), -1)
cv2.putText(img_defects, "P1", (P1[0] + 10, P1[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.circle(img_defects, P3, 5, (0, 0, 255), -1)
cv2.putText(img_defects, "P3", (P3[0] + 10, P3[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.circle(img_defects, P4, 5, (0, 0, 255), -1)
cv2.putText(img_defects, "P4", (P4[0] + 10, P4[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.circle(img_defects, P2, 5, (0, 0, 255), -1)
cv2.putText(img_defects, "P2", (P2[0] + 10, P2[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.circle(img_defects, P5, 5, (0, 0, 255), -1)
cv2.putText(img_defects, "P5", (P5[0] + 10, P5[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.circle(img_defects, P6, 5, (0, 0, 255), -1)
cv2.putText(img_defects, "P6", (P6[0] + 10, P6[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.imwrite("defects_image.png", img_defects)

# Convert points to np.array for calculations
P1 = np.array(P1)
P2 = np.array(P2)
P3 = np.array(P3)
P4 = np.array(P4)
P5 = np.array(P5)
P6 = np.array(P6)

# Compute perpendicular vector
vec_P1_P4 = P4 - P1
vec_P1_P4_perp = np.array([-vec_P1_P4[1], vec_P1_P4[0]])
unit_perp = vec_P1_P4_perp / np.linalg.norm(vec_P1_P4_perp)
start_line = (P1 - unit_perp * max(h, w)).astype(int)
end_line = (P1 + unit_perp * max(h, w)).astype(int)

# Draw lines and points on the image
cv2.arrowedLine(img_defects, tuple(P1), tuple(P4), (255, 0, 0), 2, tipLength=0.05)
cv2.arrowedLine(img_defects, tuple(P2), tuple(P5), (255, 0, 0), 2, tipLength=0.05)
cv2.arrowedLine(img_defects, tuple(start_line), tuple(end_line), (255, 0, 0), 2, tipLength=0.05)
cv2.imwrite("lines_image.png", img_defects)

# Compute P7
unit_vec_P1_P4 = vec_P1_P4 / np.linalg.norm(vec_P1_P4)
P7 = (P1 + unit_vec_P1_P4 * 200).astype(int)

# Draw P7 on the image
cv2.circle(img_defects, P7, 5, (0, 0, 255), -1)
cv2.putText(img_defects, "P7", (P7[0] + 10, P7[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.imwrite("P7_image.png", img_defects)

# Compute intersection point(P8)
P8 = np.array(line_intersection(start_line, end_line, P2, P5))

# Draw P8 on the image
cv2.circle(img_defects, P8, 5, (0, 0, 255), -1)
cv2.putText(img_defects, "P8", (P8[0] + 10, P8[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.imwrite("P8_image.png", img_defects)

# Compute P9
vec_P8_P5 = P5 - P8
unit_vec_P8_P5 = vec_P8_P5 / np.linalg.norm(vec_P8_P5)
P9 = (P8 + unit_vec_P8_P5 * 200).astype(int)

# Draw P9 on the image
cv2.circle(img_defects, P9, 5, (0, 0, 255), -1)
cv2.putText(img_defects, "P9", (P9[0] + 10, P9[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.imwrite("P9_image.png", img_defects)

# Compute angle direction
cross_z = np.cross(P8 - P1, P3 - P1)
sin_theta = cross_z / (np.linalg.norm(P8 - P1) * np.linalg.norm(P3 - P1))

# Save the angle direction
cv2.arrowedLine(img_defects, tuple(P1), tuple(P3), (255, 255, 255), 5, tipLength=0.05)
cv2.arrowedLine(img_defects, tuple(P1), tuple(P8), (255, 255, 255), 5, tipLength=0.05)
cv2.imwrite("angle_direction_image.png", img_defects)

# Scale points around ROI center
ROI_center = (P1 + P7 + P8 + P9) / 4
scale = 0.8
P1_s = scale_point(P1, ROI_center, scale)
P7_s = scale_point(P7, ROI_center, scale)
P8_s = scale_point(P8, ROI_center, scale)
P9_s = scale_point(P9, ROI_center, scale)

# Draw scaled points and lines on the image
img_roi = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
cv2.line(img_roi, tuple(P8_s.astype(int)), tuple(P1_s.astype(int)), (0, 255, 0), 2)
cv2.line(img_roi, tuple(P1_s.astype(int)), tuple(P7_s.astype(int)), (0, 255, 0), 2)
cv2.line(img_roi, tuple(P7_s.astype(int)), tuple(P9_s.astype(int)), (0, 255, 0), 2)
cv2.line(img_roi, tuple(P9_s.astype(int)), tuple(P8_s.astype(int)), (0, 255, 0), 2)
cv2.circle(img_roi, P1, 5, (0, 0, 255), -1)
cv2.putText(img_roi, "P1", (P1[0] + 10, P1[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.circle(img_roi, P7, 5, (0, 0, 255), -1)
cv2.putText(img_roi, "P7", (P7[0] + 10, P7[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.circle(img_roi, P8, 5, (0, 0, 255), -1)
cv2.putText(img_roi, "P8", (P8[0] + 10, P8[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.circle(img_roi, P9, 5, (0, 0, 255), -1)
cv2.putText(img_roi, "P9", (P9[0] + 10, P9[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.imwrite("scaled_ROI_image.png", img_roi)

# Define ROI order (based on angle)
if sin_theta < 0:
    ROI_points = np.float32([P1_s, P8_s, P9_s, P7_s])
else:
    ROI_points = np.float32([P8_s, P1_s, P7_s, P9_s])

# Perspective transformation
ROI_w = int(max(np.linalg.norm(P8_s - P1_s), np.linalg.norm(P9_s - P7_s)))
ROI_h = int(max(np.linalg.norm(P8_s - P9_s), np.linalg.norm(P1_s - P7_s)))
dst_points = np.float32([[0, 0], [ROI_w, 0], [ROI_w, ROI_h], [0, ROI_h]])

m_persp = cv2.getPerspectiveTransform(ROI_points, dst_points)
warped = cv2.warpPerspective(img, m_persp, (ROI_w, ROI_h))

# Resize and save result
resized_roi = cv2.resize(warped, (128, 128))
cv2.imwrite("ROI.png", resized_roi)

elapsed_time = time.time() - start_time
print(f"Processing time: {elapsed_time:.2f} seconds")
