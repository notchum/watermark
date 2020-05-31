/** 
 * @file   main_window.cpp
 * 
 * @brief  Contains the implementation of the MainWindow class.
 * 
 * @author Morgan Chumbley
 * 
 * @date   May 29th, 2020
 */

#include "main_window.hpp"

MainWindow::MainWindow(QWidget *parent) : QWidget(parent)
{
	/************************************************************************************************
	*
	*                             HEALTH MONITORING
	* 
	************************************************************************************************/

	// Create group box for health monitoring
	QGroupBox *healthGroupBox = new QGroupBox(tr("Health Monitor"));
	healthGroupBox->setMaximumWidth(300);
	healthGroupBox->setMinimumSize(450, 300);

	// Create layout for health monitoring
	QVBoxLayout *rightLayout = new QVBoxLayout();
	rightLayout->setAlignment(Qt::AlignVCenter);

	// Create indicator lines
	line1 = new QFrame();
	line2 = new QFrame();
	line3 = new QFrame();
	line1->setFrameShape(QFrame::HLine);
	line2->setFrameShape(QFrame::HLine);
	line3->setFrameShape(QFrame::HLine);
	line1->setFixedHeight(5);
	line2->setFixedHeight(5);
	line3->setFixedHeight(5);
	line1->setStyleSheet(QString("background-color: #80FF80;"));
	line2->setStyleSheet(QString("background-color: #80FF80;"));
	line3->setStyleSheet(QString("background-color: #80FF80;"));

	// Create layout for the indicator lights
	QHBoxLayout *upperLayout = new QHBoxLayout();
	upperLayout->addWidget(line1);
	upperLayout->addWidget(line2);
	upperLayout->addWidget(line3);
	upperLayout->addSpacing(30);
	rightLayout->addLayout(upperLayout);

	// Create & add tabs for health monitoring
	QTabWidget *healthTabs = new QTabWidget();
	healthTabs->setStyleSheet("QTabBar::tab { height: 70px; width: 130px; font-size: 20pt; }");
	rightLayout->addWidget(healthTabs);

	// Create & add modules
	Modules *modules = new Modules();
	healthTabs->addTab(modules, "Modules");

	// Create & add fault string
	FaultString *stringF = new FaultString();
	healthTabs->addTab(stringF, "RTC");

	// Create & add sensor string
	SensorString *stringS = new SensorString();
	healthTabs->addTab(stringS, "Sensors");

	// Set the layout in the group box
	healthGroupBox->setLayout(rightLayout);

	// Connect the indicator lights to the signals from string classes
	//QObject::connect(modules, &Modules::disabled, 
	//				 [=]() { this->disableIndLight(line1); });
	QObject::connect(stringF, &FaultString::disabled, 
					 [=]() { this->disableIndLight(line2); });
	QObject::connect(stringS, &SensorString::disabled, 
					 [=]() { this->disableIndLight(line3); });
	//QObject::connect(modules, &Modules::enabled, 
	//				 [=]() { this->enableIndLight(line1); });
	QObject::connect(stringF, &FaultString::enabled, 
					 [=]() { this->enableIndLight(line2); });
	QObject::connect(stringS, &SensorString::enabled, 
					 [=]() { this->enableIndLight(line3); });

	/************************************************************************************************
	*
	*                             COMMANDS
	* 
	************************************************************************************************/

	// Create group box for visuals
	QGroupBox *commandGroupBox = new QGroupBox(tr("Commands"));

	// Create layout for commands
	QVBoxLayout *topLayout = new QVBoxLayout;
	topLayout->setAlignment(Qt::AlignVCenter);

	// Create & add commands
	Commands *commands = new Commands();
	topLayout->addWidget(commands);
	commandGroupBox->setLayout(topLayout);
	commandGroupBox->setMaximumHeight(300);

	// Connect the commander state change with the machine that updates csm request buttons
	QObject::connect(modules, &Modules::cmdStateChanged, 
					 [=]() { commands->updateButtons(modules->getCurrentCmdState()); });

	/************************************************************************************************
	*
	*                            LAYOUTS
	* 
	************************************************************************************************/

	//Left side
	QVBoxLayout *leftLayout = new QVBoxLayout;
	leftLayout->addWidget(commandGroupBox);
	leftLayout->addWidget(visualGroupBox);

	QHBoxLayout *mainLayout = new QHBoxLayout;
	mainLayout->addLayout(leftLayout);
	mainLayout->addWidget(healthGroupBox);
	setLayout(mainLayout);
}

void MainWindow::disableIndLight(QFrame *frame)
{
	frame->setStyleSheet(QString("background-color: #FF8080;"));
}