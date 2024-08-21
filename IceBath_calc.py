import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from switch_button import SwitchButton  # Import the custom switch

class ColdBathCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.use_metric = False
        self.initUI()

    def initUI(self):
        # Set the dark mode palette
        self.setDarkMode()

        # Create the layout
        layout = QVBoxLayout()

        # Horizontal layout for the switch and labels
        switch_layout = QHBoxLayout()

        self.metric_label = QLabel("Metric")
        self.imperial_label = QLabel("Imperial")

        # Adjust label alignment
        self.metric_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.imperial_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Unit switcher using custom SwitchButton
        self.unit_switch = SwitchButton()
        self.unit_switch.setChecked(False)
        self.unit_switch.clicked.connect(self.toggle_units)

        # Add labels and switch to the layout
        switch_layout.addWidget(self.metric_label)
        switch_layout.addWidget(self.unit_switch)
        switch_layout.addWidget(self.imperial_label)

        layout.addLayout(switch_layout)

        # Form layout for inputs
        self.form_layout = QFormLayout()

        self.tankVolumeInput = QLineEdit()
        self.startTempInput = QLineEdit()
        self.desiredTempInput = QLineEdit()
        self.personWeightInput = QLineEdit()

        self.update_labels()
        layout.addLayout(self.form_layout)

        # Calculate button
        self.calculateButton = QPushButton("Calculate Ice Requirements")
        self.calculateButton.clicked.connect(self.calculate_ice)
        layout.addWidget(self.calculateButton)

        # Result label
        self.resultLabel = QLabel("Results will appear here")
        layout.addWidget(self.resultLabel)

        # Set layout and window title
        self.setLayout(layout)
        self.setWindowTitle('Cold Bath Ice Calculator')

    def setDarkMode(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        self.setPalette(palette)

    def update_labels(self):
        # Clear existing widgets
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Recreate input fields
        self.tankVolumeInput = QLineEdit()
        self.startTempInput = QLineEdit()
        self.desiredTempInput = QLineEdit()
        self.personWeightInput = QLineEdit()

        # Update labels based on the selected unit system
        if self.use_metric:
            self.form_layout.addRow("Max Tank Capacity (liters):", self.tankVolumeInput)
            self.form_layout.addRow("Starting Water Temperature (°C):", self.startTempInput)
            self.form_layout.addRow("Desired Water Temperature (°C):", self.desiredTempInput)
            self.form_layout.addRow("Person's Weight (kg):", self.personWeightInput)
        else:
            self.form_layout.addRow("Max Tank Capacity (gallons):", self.tankVolumeInput)
            self.form_layout.addRow("Starting Water Temperature (°F):", self.startTempInput)
            self.form_layout.addRow("Desired Water Temperature (°F):", self.desiredTempInput)
            self.form_layout.addRow("Person's Weight (lbs):", self.personWeightInput)

    def toggle_units(self, checked):
        self.use_metric = checked
        self.update_labels()

    def calculate_ice(self):
        try:
            # Gather inputs
            if self.use_metric:
                tank_volume = float(self.tankVolumeInput.text())  # liters
                start_temp = float(self.startTempInput.text())  # Celsius
                desired_temp = float(self.desiredTempInput.text())  # Celsius
                person_weight = float(self.personWeightInput.text())  # kg

                vol_tank_net_liters = tank_volume
                T_hot_C = start_temp
                T_cold_C = desired_temp
                T_ice_C = 0.0
                den_water_kg_per_m3 = 997.0  # Density of water in kg/m^3
                cp_water_J_per_kg_C = 4.1955 * 1000.0  # Specific heat capacity of water in J/kg/°C
                hf_water_J_per_kg = 333.55 * 1000  # Latent heat of fusion for water in J/kg

                # Calculate volumes and mass
                den_human_kg_per_m3 = 0.985 * den_water_kg_per_m3  # Density of the human body
                vol_human_liters = person_weight / den_human_kg_per_m3  # Calculate volume displaced by person
                vol_tank_net_liters -= vol_human_liters
                m_tank_net_kg = vol_tank_net_liters / 1000 * den_water_kg_per_m3  # Convert liters to cubic meters for mass

                # Energy calculations
                m_ice_kg = m_tank_net_kg * cp_water_J_per_kg_C * (T_hot_C - T_cold_C) / (hf_water_J_per_kg + cp_water_J_per_kg_C * (T_cold_C - T_ice_C))

                ice_required = m_ice_kg  # in kg

                # Display results in metric units
                self.resultLabel.setText(f"Ice required: {ice_required:.2f} kg\n" +
                                         f"How much volume you should use given user's weight + tank's capacity: {vol_tank_net_liters:.2f} liters\n" +
                                         f"Total Weight of water AND user: {m_tank_net_kg:.2f} kg")
            else:
                tank_volume_gallons = float(self.tankVolumeInput.text())
                start_temp_f = float(self.startTempInput.text())
                desired_temp_f = float(self.desiredTempInput.text())
                person_weight_lbs = float(self.personWeightInput.text())

                # Convert inputs to metric units
                vol_tank_total_liters = tank_volume_gallons * 3.78541  # Gallons to liters
                T_hot_C = (start_temp_f - 32) * 5/9  # Fahrenheit to Celsius
                T_cold_C = (desired_temp_f - 32) * 5/9  # Fahrenheit to Celsius
                T_ice_C = 0.0
                den_water_kg_per_m3 = 997.0  # Density of water in kg/m^3
                cp_water_J_per_kg_C = 4.1955 * 1000.0  # Specific heat capacity of water in J/kg/°C
                hf_water_J_per_kg = 333.55 * 1000  # Latent heat of fusion for water in J/kg
                den_human_kg_per_m3 = 0.985 * den_water_kg_per_m3  # Density of the human body

                # Calculate volumes and mass
                vol_human_liters = person_weight_lbs * 0.45359237 / den_human_kg_per_m3  # Convert lbs to kg and then calculate volume
                vol_tank_net_liters = vol_tank_total_liters - vol_human_liters
                m_tank_net_kg = vol_tank_net_liters / 1000 * den_water_kg_per_m3  # Convert liters to cubic meters for mass

                # Energy calculations
                m_ice_kg = m_tank_net_kg * cp_water_J_per_kg_C * (T_hot_C - T_cold_C) / (hf_water_J_per_kg + cp_water_J_per_kg_C * (T_cold_C - T_ice_C))

                # Convert the result to lbs and gallons
                ice_required_lbs = m_ice_kg * 2.20462  # Convert kg to lbs
                vol_tank_net_gallons = vol_tank_net_liters / 3.78541  # Convert liters to gallons
                m_tank_net_lbs = m_tank_net_kg * 2.20462  # Convert kg to lbs

                # Display results in Imperial units
                self.resultLabel.setText(f"Ice required: {ice_required_lbs:.2f} lbs\n" +
                                         f"How much volume you should use given user's weight + tank's capacity: {vol_tank_net_gallons:.2f} gallons\n" +
                                         f"Total Weight of water + user: {m_tank_net_lbs:.2f} lbs")

        except Exception as e:
            QMessageBox.warning(self, "Input Error", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ex = ColdBathCalculator()
    ex.show()
    sys.exit(app.exec())
