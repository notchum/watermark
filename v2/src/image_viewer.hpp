/** 
 * @file   image_viewer.hpp
 * 
 * @brief  Contains the definitions of the ImageViewer class.
 * 
 * @author Morgan Chumbley
 * 
 * @date   May 29th, 2020
 */

#ifndef IMAGE_VIEWER_HPP
#define IMAGE_VIEWER_HPP

#include <QWidget>
#include <QLabel>
#include <QVBoxLayout>

/** 
 * @class   ImageViewer
 * 
 * @brief   A class to create a widget to display an image.
 * 
 * @details A more detailed class description.
 * 			Class description continued
 */
class ImageViewer : public QWidget
{
	Q_OBJECT

public:
	/** 
	 * @brief Constructor 
	 */
	ImageViewer(QWidget *parent = nullptr) : QWidget(parent), it(n) {}

	/** 
	 * @brief Destructor 
	 */
	virtual ~ImageViewer() {}

private:
	/** 
	 * @brief Callback for stream subscriber
	 * 
	 * @param msg the sensor_msg image recieved from the subscriber
	 */
	void streamCallback(const sensor_msgs::ImageConstPtr& msg);

	/** 
	 * @brief  Helper function to resize an OpenCV Mat image
	 * 
	 * @param  img the input OpenCV image
	 * 
	 * @param  target_width the target width of the output image
	 * 
	 * @return the resized image
	 */
	cv::Mat resizeImage(const cv::Mat& img, int target_width = 500);

	/** A QLabel can be used to diplay an image */
	QLabel *image_lbl;

}; // end class ImageViewer

#endif // IMAGE_VIEWER_HPP