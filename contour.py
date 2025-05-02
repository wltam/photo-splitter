import cv2
import numpy as np
import os

def process_folder(input_folder, output_folder):
    # ===== 可調整參數 =====
    # 最小區域面積 (像素數): 小於此面積的區域將被忽略
    MIN_AREA = 20000
    
    # 最小面積比例: 檢測區域面積與整個圖像面積的最小比例 (0.05 = 5%)
    MIN_AREA_RATIO = 0.01
    
    # 最大面積比例: 檢測區域面積與整個圖像面積的最大比例 (0.95 = 95%)
    # 用於避免檢測到整個圖像
    MAX_AREA_RATIO = 0.99
    
    # 最小尺寸 (像素): 檢測區域的寬度和高度必須大於此值
    MIN_DIMENSION = 100
    
    # 長寬比最大差異: 長邊與短邊的最大比例
    # 例如: 設為5.0表示長邊最多為短邊的5倍
    # 常見照片比例參考:
    # - 4:3 比例的照片，長寬比差異為 4/3 = 1.33
    # - 16:9 比例的照片，長寬比差異為 16/9 = 1.78
    # 設定較大的值如5.0可以容納大多數照片和文件
    MAX_ASPECT_RATIO_DIFF = 5.0
    
    # 提取照片時添加的邊緣像素
    MARGIN = 5
    
    # 邊緣檢測參數
    CANNY_LOW_THRESHOLD = 20
    CANNY_HIGH_THRESHOLD = 80
    
    # CLAHE 參數 (對比度增強)
    CLAHE_CLIP_LIMIT = 4.0
    CLAHE_TILE_SIZE = (8, 8)
    
    # 雙邊濾波參數 (降噪)
    BILATERAL_D = 9
    BILATERAL_SIGMA_COLOR = 75
    BILATERAL_SIGMA_SPACE = 75
    
    # 高斯模糊參數 (降噪)
    GAUSSIAN_KERNEL_SIZE = (5, 5)
    
    # 膨脹參數 (閉合邊緣)
    DILATION_KERNEL_SIZE = (5, 5)
    DILATION_ITERATIONS = 3
    
    # 輸出控制 - 設定是否保存各類圖像
    SAVE_DETECTED_REGIONS = True     # 保存標記出檢測區域的圖像
    SAVE_INTERMEDIATE_IMAGES = False  # 保存中間處理過程的圖像 (邊緣檢測等)
    # ===================

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all image files in the input folder
    image_files = [f for f in os.listdir(input_folder) 
                  if f.lower().endswith(('jpg', 'jpeg', 'png'))]
    
    total_photos = 0
    
    for image_file in image_files:
        # Read the input image
        input_image_path = os.path.join(input_folder, image_file)
        img = cv2.imread(input_image_path)
        
        # Skip if image couldn't be read
        if img is None:
            print(f"Could not read image: {image_file}")
            continue
            
        original = img.copy()
        
        # Get image dimensions
        img_height, img_width = img.shape[:2]
        img_area = img_height * img_width

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply CLAHE for enhanced contrast
        clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP_LIMIT, tileGridSize=CLAHE_TILE_SIZE)
        enhanced_gray = clahe.apply(gray)

        # Apply bilateral filter to reduce noise while preserving edges
        smooth = cv2.bilateralFilter(enhanced_gray, BILATERAL_D, 
                                    BILATERAL_SIGMA_COLOR, BILATERAL_SIGMA_SPACE)

        # Apply Gaussian blur to further reduce noise
        blurred = cv2.GaussianBlur(smooth, GAUSSIAN_KERNEL_SIZE, 0)

        # Apply Canny edge detection with appropriate thresholds
        edges = cv2.Canny(blurred, CANNY_LOW_THRESHOLD, CANNY_HIGH_THRESHOLD)

        # Dilate edges to close gaps
        kernel = np.ones(DILATION_KERNEL_SIZE, np.uint8)
        dilated_edges = cv2.dilate(edges, kernel, iterations=DILATION_ITERATIONS)

        # Find contours in the edge image
        contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, 
                                      cv2.CHAIN_APPROX_SIMPLE)

        # Filter and extract rectangular regions (photos)
        count = 0

        # Debug image to show detected regions
        debug_img = original.copy() if SAVE_DETECTED_REGIONS else None

        for contour in contours:
            area = cv2.contourArea(contour)
            area_ratio = area / img_area
            
            # Filter by both absolute area and relative area
            if area > MIN_AREA and area_ratio > MIN_AREA_RATIO and area_ratio < MAX_AREA_RATIO:
                # Get a bounding rectangle around the contour
                x, y, w, h = cv2.boundingRect(contour)
                
                # Additional check for minimum dimensions
                if w < MIN_DIMENSION or h < MIN_DIMENSION:
                    continue
                
                # Check aspect ratio to filter out very narrow or wide regions
                long_side = max(w, h)
                short_side = min(w, h)
                aspect_ratio_diff = long_side / short_side if short_side > 0 else float('inf')
                
                if aspect_ratio_diff > MAX_ASPECT_RATIO_DIFF:
                    continue

                # Add a small margin to ensure we capture the full photo
                x_with_margin = max(0, x - MARGIN)
                y_with_margin = max(0, y - MARGIN)
                w_with_margin = min(img.shape[1] - x_with_margin, w + 2 * MARGIN)
                h_with_margin = min(img.shape[0] - y_with_margin, h + 2 * MARGIN)

                # Extract the region of interest (photo)
                photo = original[y_with_margin:y_with_margin + h_with_margin, 
                               x_with_margin:x_with_margin + w_with_margin]

                # Save the extracted photo
                base_name = os.path.splitext(image_file)[0]
                output_path = os.path.join(output_folder, 
                                         f'{base_name}_photo_{count + 1}.jpg')
                cv2.imwrite(output_path, photo)
                count += 1

                # Draw rectangle on debug image if enabled
                if SAVE_DETECTED_REGIONS:
                    cv2.rectangle(debug_img, (x_with_margin, y_with_margin),
                                (x_with_margin + w_with_margin, y_with_margin + h_with_margin),
                                (0, 255, 0), 3)
                    
                    # Add area and aspect ratio info to the debug image
                    cv2.putText(debug_img, f"Area: {area:.0f} ({area_ratio:.2%})", 
                              (x_with_margin, y_with_margin - 10),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    cv2.putText(debug_img, f"Ratio: {aspect_ratio_diff:.1f}", 
                              (x_with_margin, y_with_margin - 30),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save the visualization with detected regions if enabled
        if SAVE_DETECTED_REGIONS:
            debug_path = os.path.join(output_folder, 
                                    f'{os.path.splitext(image_file)[0]}_detected_regions.jpg')
            cv2.imwrite(debug_path, debug_img)

        # Save intermediate processing images for debugging if enabled
        if SAVE_INTERMEDIATE_IMAGES:
            cv2.imwrite(os.path.join(output_folder, 
                                   f'{os.path.splitext(image_file)[0]}_enhanced_gray.jpg'), 
                       enhanced_gray)
            cv2.imwrite(os.path.join(output_folder, 
                                   f'{os.path.splitext(image_file)[0]}_edges.jpg'), 
                       edges)
            cv2.imwrite(os.path.join(output_folder, 
                                   f'{os.path.splitext(image_file)[0]}_dilated_edges.jpg'), 
                       dilated_edges)
        
        total_photos += count
        print(f"Processed '{image_file}': Found {count} photos")

    print(f"Processed {len(image_files)} images from '{input_folder}'")
    print(f"Total {total_photos} photos extracted and saved to '{output_folder}'")

# 使用範例 - 指定輸入和輸出資料夾
process_folder('C:/Users/WLTAM/Documents/Scanner/', 'C:/Users/WLTAM/Documents/Scanner/extracted')
