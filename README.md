This project is a desktop-based home automation system prototype developed to demonstrate the control and monitoring of home appliances using the TM4C123GH6PM microcontroller. The system includes the following features:

Lamp Control: Toggle a 220V lamp on/off while retaining manual switch functionality.
Plug Control: Turn a plug on/off; when off, the plug is disabled for use.
Door Status Display: Real-time monitoring of door status using a magnetic switch.
Room Temperature Display: Continuous display of the current room temperature.
Temperature Alarm: Trigger both software and physical alarms if the temperature exceeds a set threshold.
Door Activity Logs: Record and display the timestamps for door opening and closing events.
The GUI for this project is implemented as a desktop application using Python's Tkinter library. Communication between the TM4C123 board and the desktop app is achieved via UART.

All hardware components are neatly mounted, and wiring is concealed to ensure a clean presentation
