/** 
 * @file   main_window.hpp
 * 
 * @brief  Contains the definitions of the MainWindow class.
 * 
 * @author Morgan Chumbley
 * 
 * @date   May 29th, 2020
 */

#ifndef MAIN_WINDOW_HPP
#define MAIN_WINDOW_HPP

#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QGroupBox>

/** 
 * @class   MainWindow
 * 
 * @brief   A class to create the main Qt window.
 * 
 * @details This class is used to add all custom
 * 			widgets to a single window. This class
 * 			constructor is then called in main.cpp
 * 			to execute the entire application.
 */
class MainWindow: public QWidget
{
	Q_OBJECT

public:
	/** 
	 * @brief Constructor 
	 */
	MainWindow(QWidget * parent = nullptr);

	/** 
	 * @brief Destructor 
	 */
	virtual ~MainWindow() {}

public slots:
	/** 
	 * @brief Qt slot for disabling (changing to red) a QFrame
     * 
     * @param frame pointer to the QFrame to be altered
	 */
	void disableIndLight(QFrame *frame);

}; // end class MainWindow

#endif // MAIN_WINDOW_HPP