c++融合

测试图尺寸为512x512大小。

- mask值为0或255

```c++
// 通过mask将 foreground 和background融合。 运行时间约1ms
cv::Mat compose(cv::Mat& fg, cv::Mat& bg, cv::Mat& mask){
    cv::Mat dst;
    dst = bg.clone();

    int rows = fg.rows;
    int cols = fg.cols;
    for (int i = 0; i < rows; i++){
        cv::Vec3b* fg_rows_ptr = fg.ptr<cv::Vec3b>(i);
        cv::Vec3b* dst_row_ptr = dst.ptr<cv::Vec3b>(i);
        uchar* mask_rows_ptr = mask.ptr<uchar >(i);
        for (int j = 0; j < cols; j++){
            if(mask_rows_ptr[j] == 255){
                dst_row_ptr[j][0]= fg_rows_ptr[j][0];
                dst_row_ptr[j][1] = fg_rows_ptr[j][1];
                dst_row_ptr[j][2] = fg_rows_ptr[j][2];
            }
        }
    }
    return dst;
}
```



- matting的方式融合，mask值在0-255之间。

```c++
//  这个脚本运行 约5ms - 6ms
cv::Mat compose(cv::Mat& fg, cv::Mat& bg, cv::Mat& mask){
	cv::Mat dst;
    dst = bg.clone();
    int rows = fg.rows;
    int cols = fg.cols;
	for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            cv::Vec3b fgPixel = fg.at<cv::Vec3b>(i, j);
            cv::Vec3b bgPixel = bg.at<cv::Vec3b>(i, j);
            uchar alphaValue = mask.at<uchar>(i, j);
            cv::Vec3b blendedPixel;
			// use if cost 5ms-6ms
			if (alphaValue != 0) {
				float av = alphaValue / 255.0 ;
				for (int c = 0; c < 3; ++c) {
					blendedPixel[c] = av* fgPixel[c] + (1 - av)* bgPixel[c];
				}
				dst.at<cv::Vec3b>(i, j) = blendedPixel;
			}
        }
    }
    return dst;
}
```

运行效果同上。

```c++
// 这个脚本运行 约3ms 全部使用了opencv的方法
cv::Mat compose(cv::Mat& foreground, cv::Mat& background, cv::Mat& alpha){
    foreground.convertTo(foreground, CV_32FC3); // convert to float type
    background.convertTo(background, CV_32FC3);
	cv::cvtColor(alpha, alpha, cv::COLOR_GRAY2BGR);
    alpha.convertTo(alpha, CV_32FC3, 1.0/255); // alpha to 0 and 1
    cv::Mat ouImage = cv::Mat::zeros(foreground.size(), foreground.type());
    cv::multiply(alpha, foreground, foreground); 
    cv::multiply(cv::Scalar::all(1.0)-alpha, background, background); 
    cv::add(foreground, background, ouImage); 
	ouImage = ouImage/255;
	ouImage.convertTo(ouImage, CV_8U, 255.0);
    return ouImage;
}
```

