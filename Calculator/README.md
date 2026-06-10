# Scientific Calculator GUI

A modern, desktop-based Scientific Calculator built with Python and Tkinter. This application features a sleek dark mode user interface, full keyboard bindings, dynamic display scaling for error handling, and robust parsing for advanced mathematical expressions.

## 🚀 Features

- **Modern Dark Theme**: Styled cleanly using Tkinter's `clam` theme engine with a custom color palette.
- **Comprehensive Math Suite**: 
  - Standard arithmetic operations (`+`, `−`, `×`, `÷`, `mod`).
  - Trigonometric functions (`sin`, `cos`, `tan`) supporting both **Degree (DEG)** and **Radian (RAD)** modes.
  - Powers, roots, and inverses (`x²`, `x³`, `xʸ`, `√`, `³√`, `2ˣ`).
  - Advanced operations like absolute values (`|x|`) and factorials (`n!`).
- **Physical Keyboard Support**: Map standard keyboard inputs seamlessly (e.g., typing `*` or `x` automatically appends the clean `×` visual operator).
- **Smart Expression Parser**: Handles implicit multiplication automatically (e.g., parsing `2(3)` as `2*3` or `2π` as `2*3.14159...`).
- **Dynamic Display Scaling**: Automatically shrinks the display font size down to a legible format whenever a syntax error or a division-by-zero error is encountered.

---

## 🛠️ Prerequisites

To run this project, you only need Python installed on your system. Tkinter comes bundled with standard Python installations.

- **Python**: 3.10 or higher recommended.

---

## 📦 Installation & Usage

1. **Clone or download this repository** to your local machine:
   ```bash
   git clone [https://github.com/your-username/scientific-calculator.git](https://github.com/your-username/scientific-calculator.git)
   cd scientific-calculator