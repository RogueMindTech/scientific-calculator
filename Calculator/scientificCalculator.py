import math
import re
import tkinter as tk
from tkinter import ttk


class ScientificCalculator:
    """Advanced GUI scientific calculator with history and memory functions."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.resizable(False, False)
        self.root.configure(bg="#121212")

        # State
        self.expression = ""
        self.history: list[str] = []
        self.memory = 0.0
        self.last_answer = 0.0
        self.angle_mode = "DEG"  # DEG or RAD

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configure_styles()

        # Build UI
        self._create_display()
        self._create_buttons()
        self._bind_keyboard()

    def _configure_styles(self):
        """Configure ttk styles for buttons with a modern dark theme."""
        # Numbers
        self.style.configure(
            "Num.TButton",
            font=("Segoe UI", 13),
            padding=10,
            background="#2a2a2a",
            foreground="#ffffff",
            borderwidth=0,
        )
        self.style.map("Num.TButton", background=[("active", "#3a3a3a")])

        # Core Operators (+, -, x, ÷, =)
        self.style.configure(
            "Op.TButton",
            font=("Segoe UI", 13, "bold"),
            padding=10,
            background="#6366f1",
            foreground="#ffffff",
            borderwidth=0,
        )
        self.style.map("Op.TButton", background=[("active", "#4f46e5")])

        # Functions (Trig, logs, powers)
        self.style.configure(
            "Func.TButton",
            font=("Segoe UI", 11),
            padding=10,
            background="#1e1e1e",
            foreground="#9ca3af",
            borderwidth=0,
        )
        self.style.map("Func.TButton", background=[("active", "#2d2d2d")])

        # Clear operations (C, CE)
        self.style.configure(
            "Clear.TButton",
            font=("Segoe UI", 13, "bold"),
            padding=10,
            background="#ef4444",
            foreground="#ffffff",
            borderwidth=0,
        )
        self.style.map("Clear.TButton", background=[("active", "#dc2626")])

    def _create_display(self):
        """Create the display area with expression and result fields."""
        display_frame = tk.Frame(self.root, bg="#121212")
        display_frame.pack(fill=tk.X, padx=12, pady=(12, 6))

        # Mode indicator
        self.mode_label = tk.Label(
            display_frame,
            text=f"Mode: {self.angle_mode}",
            font=("Segoe UI", 10, "bold"),
            bg="#121212",
            fg="#6366f1",
            anchor="w",
        )
        self.mode_label.pack(fill=tk.X)

        # Expression display
        self.expr_var = tk.StringVar(value="")
        self.expr_display = tk.Entry(
            display_frame,
            textvariable=self.expr_var,
            font=("Consolas", 14),
            bg="#1e1e1e",
            fg="#9ca3af",
            relief=tk.FLAT,
            justify=tk.RIGHT,
            state="readonly",
            readonlybackground="#1e1e1e",
        )
        self.expr_display.pack(fill=tk.X, pady=(6, 0), ipady=4)

        # Result display
        self.result_var = tk.StringVar(value="0")
        self.result_display = tk.Entry(
            display_frame,
            textvariable=self.result_var,
            bg="#1e1e1e",
            fg="#ffffff",
            relief=tk.FLAT,
            justify=tk.RIGHT,
            state="readonly",
            readonlybackground="#1e1e1e",
        )
        self.result_display.pack(fill=tk.X, pady=(2, 6), ipady=4)

        # Explicit initialization of display layout defaults
        self.result_display.config(font=("Consolas", 26, "bold"))

    def _set_result(self, text: str):
        """Set the result variable text and dynamically scale font size if it's an error."""
        self.result_var.set(text)

        if "Error" in text:
            # Scale down to a readable size for long exception text
            self.result_display.config(
                font=("Consolas", 12, "bold"), fg="#ef4444"
            )
        else:
            # Restore normal large sizing and white color
            self.result_display.config(
                font=("Consolas", 26, "bold"), fg="#ffffff"
            )

    def _create_buttons(self):
        """Create all calculator buttons layout."""
        button_frame = tk.Frame(self.root, bg="#121212")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Button layout: (text, style, command/value, colspan)
        buttons = [
            # Row 1: Scientific functions
            ("log", "Func", lambda: self._append("log("), 1),
            ("exp", "Func", lambda: self._append("exp("), 1),
            ("sin", "Func", lambda: self._append("sin("), 1),
            ("cos", "Func", lambda: self._append("cos("), 1),
            ("tan", "Func", lambda: self._append("tan("), 1),
            # Row 2: Powers and roots
            ("x²", "Func", lambda: self._append("²"), 1),
            ("x³", "Func", lambda: self._append("³"), 1),
            ("xʸ", "Func", lambda: self._append("^"), 1),
            ("√", "Func", lambda: self._append("√("), 1),
            ("³√", "Func", lambda: self._append("³√("), 1),
            # Row 3: Utility
            ("(", "Func", lambda: self._append("("), 1),
            (")", "Func", lambda: self._append(")"), 1),
            ("n!", "Func", lambda: self._append("!"), 1),
            ("π", "Func", lambda: self._append("π"), 1),
            ("ANS", "Func", lambda: self._append("ANS"), 1),
            # Row 4: Clear and basic ops
            ("mod", "Func", lambda: self._append(" mod "), 1),
            ("2ˣ", "Func", lambda: self._append("2^"), 1),
            ("C", "Clear", self._clear, 1),
            ("CE", "Clear", self._clear_entry, 1),
            ("⌫", "Clear", self._backspace, 1),
            # Row 5: Utility Functions + Upper Numbers
            ("DEG/RAD", "Func", self._toggle_angle_mode, 1),
            ("|x|", "Func", lambda: self._append("abs("), 1),
            ("7", "Num", lambda: self._append("7"), 1),
            ("8", "Num", lambda: self._append("8"), 1),
            ("9", "Num", lambda: self._append("9"), 1),
            # Row 6: Operators & Mid Numbers
            ("−", "Op", lambda: self._append("−"), 1),
            ("÷", "Op", lambda: self._append("÷"), 1),
            ("4", "Num", lambda: self._append("4"), 1),
            ("5", "Num", lambda: self._append("5"), 1),
            ("6", "Num", lambda: self._append("6"), 1),
            # Row 7: Operators & Lower Numbers
            ("+", "Op", lambda: self._append("+"), 1),
            ("×", "Op", lambda: self._append("×"), 1),
            ("1", "Num", lambda: self._append("1"), 1),
            ("2", "Num", lambda: self._append("2"), 1),
            ("3", "Num", lambda: self._append("3"), 1),
            # Row 8: Zero and equals
            ("00", "Num", lambda: self._append("00"), 1),
            (".", "Num", lambda: self._append("."), 1),
            ("0", "Num", lambda: self._append("0"), 1),
            ("=", "Op", self._calculate, 2),
        ]

        row, col = 0, 0
        cols_per_row = 5

        for text, style, command, colspan in buttons:
            btn = ttk.Button(
                button_frame,
                text=text,
                style=f"{style}.TButton",
                command=command,
                width=5 * colspan,
            )
            btn.grid(
                row=row,
                column=col,
                columnspan=colspan,
                padx=3,
                pady=3,
                sticky="nsew",
            )
            col += colspan
            if col >= cols_per_row:
                col = 0
                row += 1

        # Configure grid system weights
        for i in range(cols_per_row):
            button_frame.columnconfigure(i, weight=1)
        for i in range(row + 1):
            button_frame.rowconfigure(i, weight=1)

    def _bind_keyboard(self):
        """Bind keyboard events for input processing."""
        self.root.bind("<Key>", self._handle_keypress)
        self.root.bind("<Return>", lambda e: self._calculate())
        self.root.bind("<BackSpace>", lambda e: self._backspace())
        self.root.bind("<Escape>", lambda e: self._clear())

    def _handle_keypress(self, event):
        """Handle physical keyboard inputs cleanly."""
        char = event.char
        if char.isdigit() or char in ".+-*/()x":
            mapping = {"*": "×", "x": "×", "/": "÷", "-": "−"}
            self._append(mapping.get(char, char))
        elif char == "^":
            self._append("^")

    def _append(self, value: str):
        """Append value to input expression buffer."""
        self.expression += value
        self.expr_var.set(self.expression)

    def _clear(self):
        """Reset total state layout."""
        self.expression = ""
        self.expr_var.set("")
        self._set_result("0")

    def _clear_entry(self):
        """Clear current tail entry token."""
        self.expression = re.sub(
            r"(\d+\.?\d*|[+\-×÷^]|[a-z]+\(?)$", "", self.expression
        )
        self.expr_var.set(self.expression)

    def _backspace(self):
        """Pop the last character out of calculation queue."""
        self.expression = self.expression[:-1]
        self.expr_var.set(self.expression)

    def _toggle_angle_mode(self):
        """Toggle computational angle states."""
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        self.mode_label.config(text=f"Mode: {self.angle_mode}")

    def _calculate(self):
        """Evaluate calculation string and stream result formatting logic."""
        if not self.expression:
            return

        try:
            result = self._evaluate(self.expression)
            self.last_answer = result

            # Format result dynamically
            if isinstance(result, float):
                if result.is_integer():
                    result_str = str(int(result))
                elif abs(result) > 1e10 or (
                    abs(result) < 1e-10 and result != 0
                ):
                    result_str = f"{result:.10e}"
                else:
                    result_str = f"{result:.10g}"
            else:
                result_str = str(result)

            self._set_result(result_str)
            self.history.append(f"{self.expression} = {result_str}")
            self.expression = result_str
            self.expr_var.set("")

        except ZeroDivisionError:
            self._set_result("Error: Division by zero")
        except ValueError as e:
            self._set_result(f"Error: {e}")
        except Exception as e:
            self._set_result("Error: Invalid Syntax")
            print(f"Calculation error: {e}")

    def _evaluate(self, expr: str) -> float:
        """Safely parse strings into system execution operations."""
        # Clean down visual markers to native operators
        expr = expr.replace("×", "*")
        expr = expr.replace("÷", "/")
        expr = expr.replace("−", "-")
        expr = expr.replace("x", "*")  # Keyboard safety net
        expr = expr.replace("π", str(math.pi))
        expr = expr.replace("e", str(math.e))
        expr = expr.replace("ANS", str(self.last_answer))
        expr = expr.replace(" mod ", " % ")

        # Superscript evaluations
        expr = expr.replace("²", "**2")
        expr = expr.replace("³", "**3")
        expr = expr.replace("^", "**")

        # Process function names mapping definitions
        expr = self._replace_functions(expr)

        # Implicit Multiplications fixes (e.g. 2(3) or 2π or (4)π)
        expr = re.sub(r"(\d)(\()", r"\1*\2", expr)
        expr = re.sub(r"(\))(\d)", r"\1*\2", expr)
        expr = re.sub(r"(\))(\()", r"\1*\2", expr)

        # Constants Implicit checking
        expr = re.sub(r"(\d)(" + str(math.pi) + ")", r"\1*\2", expr)
        expr = re.sub(r"(\d)(" + str(math.e) + ")", r"\1*\2", expr)

        allowed_names = {
            "sin": self._sin,
            "cos": self._cos,
            "tan": self._tan,
            "log": math.log10,
            "exp": math.exp,
            "sqrt": math.sqrt,
            "cbrt": lambda x: math.copysign(abs(x) ** (1 / 3), x),
            "abs": abs,
            "factorial": math.factorial,
            "pow": pow,
        }

        # Safe parsing block check compilation
        code = compile(expr, "<string>", "eval")
        for name in code.co_names:
            if name not in allowed_names:
                raise ValueError(f"Unknown function: {name}")

        return eval(code, {"__builtins__": {}}, allowed_names)

    def _replace_functions(self, expr: str) -> str:
        """Map human visual UI configurations into programmatic keys."""
        expr = expr.replace("√(", "sqrt(")
        expr = expr.replace("³√(", "cbrt(")
        expr = re.sub(r"(\d+)!", r"factorial(\1)", expr)
        return expr

    def _sin(self, x: float) -> float:
        return math.sin(math.radians(x) if self.angle_mode == "DEG" else x)

    def _cos(self, x: float) -> float:
        return math.cos(math.radians(x) if self.angle_mode == "DEG" else x)

    def _tan(self, x: float) -> float:
        return math.tan(math.radians(x) if self.angle_mode == "DEG" else x)


def main():
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()