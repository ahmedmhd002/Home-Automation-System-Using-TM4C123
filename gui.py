import tkinter as tk
from tkinter import messagebox, ttk
import serial  # Ensure you have pyserial installed: pip install pyserial
import winsound

class HomeControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Appliances Control")

        # Initialize UART communication first
        self.ser = None
        self.init_uart()

        # Initialize GUI components
        self.setup_gui()

        # Alarm threshold for temperature
        self.alarm_threshold = 30.0

        # Start checking the temperature periodically
        self.check_temperature()

    def init_uart(self):
        """Initialize UART communication."""
        try:
            # Change 'COM13' to the correct COM port on your system
            self.ser = serial.Serial('COM13', baudrate=9600, timeout=1)
            print("UART initialized successfully")
        except Exception as e:
            messagebox.showerror("UART Error", f"Failed to open UART: {e}")
            self.ser = None

    def setup_gui(self):
        """Set up the GUI components."""

        # Dropdown menu for choosing what to control/view
        self.option_var = tk.StringVar()
        self.option_var.set("Lamp")  # Default option

        self.option_menu = ttk.Combobox(self.root, textvariable=self.option_var, values=["Lamp", "Plug", "Door", "Temperature"])
        self.option_menu.pack(pady=10)

        # Control panel
        self.control_panel = tk.Frame(self.root)
        self.control_panel.pack(pady=10)

        self.lamp_status = tk.StringVar(value="Off")
        self.plug_status = tk.StringVar(value="Off")
        self.door_status = tk.StringVar(value="Closed")
        self.temperature = tk.DoubleVar(value=25.0)

        # Set up the control buttons and labels
        self.lamp_button = tk.Button(self.control_panel, text="Toggle Lamp", command=self.toggle_lamp)
        self.plug_button = tk.Button(self.control_panel, text="Toggle Plug", command=self.toggle_plug)
        self.door_label = tk.Label(self.control_panel, text="Door Status:")
        self.temp_label = tk.Label(self.control_panel, text="Room Temperature:")

        self.lamp_label = tk.Label(self.control_panel, textvariable=self.lamp_status)
        self.plug_label = tk.Label(self.control_panel, textvariable=self.plug_status)
        self.door_status_label = tk.Label(self.control_panel, textvariable=self.door_status)
        self.temp_value_label = tk.Label(self.control_panel, textvariable=self.temperature)

        self.update_gui()

        # Bind the option change to update the displayed controls
        self.option_menu.bind("<<ComboboxSelected>>", self.update_gui)

    def update_gui(self, event=None):
        """Update the GUI based on the selected option."""
        selected_option = self.option_var.get()

        # Hide all widgets first
        for widget in self.control_panel.winfo_children():
            widget.pack_forget()

        if selected_option == "Lamp":
            self.lamp_button.pack(pady=5)
            self.lamp_label.pack(pady=5)
            self.send_uart_command("L")  # Send command to turn on/off the lamp

        elif selected_option == "Plug":
            self.plug_button.pack(pady=5)
            self.plug_label.pack(pady=5)
            self.send_uart_command("P")  # Send command to control the plug

        elif selected_option == "Door":
            self.door_label.pack(pady=5)
            self.door_status_label.pack(pady=5)
            self.send_uart_command("D")  # Send command to control the door

        elif selected_option == "Temperature":
            self.temp_label.pack(pady=5)
            self.temp_value_label.pack(pady=5)
            self.send_uart_command("T")  # Send command to check temperature

    def send_uart_command(self, command):
        """Send UART command to the microcontroller."""
        if self.ser:
            try:
                print(f"Sending command: {command}")  # Debug print
                self.ser.write(command.encode())  # Send the command
            except Exception as e:
                print(f"Error sending UART command: {e}")
        else:
            print("Error: UART not initialized")  # Debug message if UART is not initialized

    def toggle_lamp(self):
        """Toggle the lamp status between On and Off."""
        if self.lamp_status.get() == "Off":
            self.lamp_status.set("On")  # Update GUI to On
            self.send_uart_command("C")  # Command to turn lamp ON
        else:
            self.lamp_status.set("Off")  # Update GUI to Off
            self.send_uart_command("E")  # Command to turn lamp OFF

    def toggle_plug(self):
        """Toggle the plug status between On and Off."""
        if self.plug_status.get() == "Off":
            self.plug_status.set("On")
            self.send_uart_command("A")  # Command to turn plug ON
        else:
            self.plug_status.set("Off")
            self.send_uart_command("B")  # Command to turn plug OFF

    def check_temperature(self):
        """Check the room temperature and trigger an alarm if it exceeds the threshold."""
        try:
            selected_option = self.option_var.get()

            # Only process temperature if the "Temperature" option is selected
            if selected_option == "Temperature" and self.ser and self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                print(f"Temperature received: {line}")  # Debug print
                self.temperature.set(line)  # Update GUI with the received temperature

                if self.temperature.get() > self.alarm_threshold:
                    self.sound_alarm()  # Trigger the alarm sound
        except Exception as e:
            print(f"Error reading UART: {e}")

        self.root.after(1000, self.check_temperature)  # Check temperature every second

    def sound_alarm(self):
        """Play an alarm sound."""
        winsound.Beep(1000, 1000)

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeControlApp(root)
    root.mainloop()
