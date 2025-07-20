## 📝 手腕感興趣區域(Region of Interest, ROI)提取演算法
此專題為我的碩士論文中靜脈辨識系統的手腕感興趣區域提取程式碼。

使用 Python 實現的手腕感興趣區域(Region of Interest, ROI)提取演算法。

演算法設計細節與流程在我的論文第 27–44 頁。[請點此到我的論文連結並到電子全文下載論文](https://etheses.lib.ntust.edu.tw/thesis/detail/2b733280676d7c87e0445313c40a9b74/?seq=2#)

### 📁 壓縮檔內容
- `wrist_roi_extraction.py` - 主程式
- `requirements.txt` - Python3.9.2 用到的函式庫及其版本
 
## 📊 測試結果(左手為例) (點擊縮圖可放大)
| 輸入影像(左手為例) | 1. 填充影像周圍 80 像素 | 2. Otsu's 將手腕與背景分離 |
|-------------|--------------|-------------------|
| <img src="image/001_L_M_S1_01.png" width="250"/> | <img src="image/padded_image.png" width="250"/> | <img src="image/thresholded_image.png" width="250"/> |

| 3. 找到手腕最大輪廓 | 4. 輪廓凸包 | 5. 第一大與第二大凸缺陷(P1 與 P2) |
|---------------|------------|----------------|
| <img src="image/contour_image.png" width="250"/> | <img src="image/hull_image.png" width="250"/> | <img src="image/defects_image.png" width="250"/> |

| 6. 計算關鍵向量與垂直線 | 7. 計算 P7 | 8. 計算 P8 |
|---------------|------------|----------------|
| <img src="image/lines_image.png" width="250"/> | <img src="image/P7_image.png" width="250"/> | <img src="image/P8_image.png" width="250"/> |

| 9. 計算 P9 | 10. 計算向量叉積 | 11. 縮放 ROI |
|---------------|------------|----------------|
| <img src="image/P9_image.png" width="250"/> | <img src="image/angle_direction_image.png" width="250"/> | <img src="image/scaled_ROI_image.png" width="250"/> |

| 12. ROI 影像(128×128) |
|---------------|
| <img src="image/ROI.png" width="250"/> |

## 🚀 如何使用
請輸入以下指令建置 Python3.9.2 環境用到的函式庫及其版本:
```
pip install -r .\requirements.txt
```
請將 `wrist_roi_extraction.py` 中的變數 `captured_img` 替換為您想測試的手腕影像，並輸入以下指令執行程式:
```
python .\wrist_roi_extraction.py
```

## 🐛 演算法缺陷
1. 手腕影像(或拍攝畫面)只能從ㄇ字型缺口的方向進入。演算法有些地方寫得很死，目前還沒辦法在鏡頭中從不同方向伸入手腕來提取手腕ROI影像。
2. 手腕影像(或拍攝畫面)背景必須為全黑。演算法寫的沒有很好，目前還沒辦法在複雜背景下將手腕與背景區域分離開來，因此加入此限制條件。
