/** 
 * @file   main.cpp
 * 
 * @author Morgan Chumbley
 * 
 * @date   May 29th, 2020
 */

#include <QApplication>

#include "main_window.hpp"

int main(int argc, char **argv)
{
	QApplication::setStyle("plastique");
	QApplication app(argc, argv);

	MainWindow *main = new MainWindow();
	main->setMinimumSize(850, 500);
	main->showMaximized();
	main->show();

	app.exec();

	// After the app is closed, shutdown
	delete main;
}