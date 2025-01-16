from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

# Initialize console
console = Console()

# Create the root layout
layout = Layout()

# Define sub-layouts with fixed sizes
layout.split_column(
    Layout(name="header", size=3),  # Fixed height of 3 rows
    Layout(name="content", size=2),  # Takes up remaining space
    Layout(name="footer", size=5)  # Fixed height of 5 rows
)

# Add content to each layout
layout["header"].update(Panel("Header Section", style="bold white on blue"))
layout["content"].update(Panel("Main Content", style="bold white on green"))
layout["footer"].update(Panel("Footer Section", style="bold white on red"))

# Render the layout
console.print(layout)

console.print("hello")
