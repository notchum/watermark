/** 
 * @file   image_viewer.cpp
 * 
 * @brief  Contains the implementation of the ImageViewer class.
 * 
 * @author Morgan Chumbley
 * 
 * @date   May 29th, 2020
 */

#include "image_viewer.hpp"

ImageViewer::ImageViewer(QWidget *parent, QString topic) : QWidget(parent)
{
    // Create our image (using a QLabel)
    image_lbl = new QLabel;

    // Setting our layout
    QVBoxLayout *layout = new QVBoxLayout;
    layout->addWidget(image_lbl);
    setLayout(layout);
}

void ImageViewer::streamCallback(const sensor_msgs::ImageConstPtr& msg)
{
    // Create our cv image
    cv::Mat img;

    // Convert the color encoding to the RGB for Qt
    cv::cvtColor(img, img, CV_BGR2RGB);

    // Resize the OpenCV image to fit the window but keep aspect ratio
    img = resizeImage(img);

    // Set the pixmap for the QLabel which displays the image recieved
    image_lbl->setPixmap(QPixmap::fromImage(QImage(img.data, img.cols, img.rows, img.step, QImage::Format_RGB888)));
}

cv::Mat ImageViewer::resizeImage(const cv::Mat& img, int target_width)
{
    int width = img.cols, height = img.rows;

    // Create a new square image using zeros (black)
    cv::Mat out_img = cv::Mat::zeros(target_width, target_width, img.type());

    // Set new image to a color that matches the background
    out_img.setTo(cv::Scalar(246, 246, 246));

    // Obtain ROI while keeping aspect ratio from orig image
    int max_dim = (width >= height) ? width : height;
    float scale = ((float)target_width) / max_dim;
    cv::Rect roi;
    if (width >= height)
    {
        roi.width = target_width;
        roi.x = 0;
        roi.height = height * scale;
        roi.y = (target_width - roi.height) / 2;
    }
    else
    {
        roi.y = 0;
        roi.height = target_width;
        roi.width = width * scale;
        roi.x = (target_width - roi.width) / 2;
    }

    // Use OpenCV's resize function
    cv::resize(img, out_img(roi), roi.size());

    // Return the newly resized image
    return out_img;
}