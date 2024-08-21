# Ice Bath Calculator

A picture is worth a thousand words:

<img width="450" alt="image" src="https://github.com/user-attachments/assets/140a9538-80fb-4be8-999d-5d63ac10f7bd">

## Features

- **Unit Conversion:** Toggle between Metric and Imperial units.
- **How much water and ice you need**.
- **Standalone Executable:** No need for Python installation.


## Installation

### Run the Executable

- Download the latest release from the [Releases](https://github.com/yourusername/cold-bath-ice-calculator/releases) page.

Or

### Build from Source:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cold-bath-ice-calculator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd cold-bath-ice-calculator
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python IceBath_calc.py
   ```


#### To create an Executable for your OS:

To create a standalone executable:

```bash
pyinstaller --onefile --windowed IceBath_calc.py
```

The executable will be located in the `dist` directory.

## License

Free for personal human use and modification.

## Acknowledgements

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/intro) and [PyInstaller](https://www.pyinstaller.org/).
- HackerNews user [imthewatcher](https://news.ycombinator.com/item?id=35875673) who posted the code.
