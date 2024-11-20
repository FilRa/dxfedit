import tkinter as tk
from tkinter import ttk
from analyze import AnalyzeTab
from contour import ContourTab

class DXFAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DXF Analyzer")

        # Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Analyze DXF Tab
        self.analyze_tab = AnalyzeTab(self.notebook)
        self.notebook.add(self.analyze_tab.frame, text="Analyze DXF")

        # Generate Contour Lines Tab
        self.contour_tab = ContourTab(self.notebook, self.analyze_tab)
        self.notebook.add(self.contour_tab.frame, text="Generate Contours")

if __name__ == "__main__":
    root = tk.Tk()
    app = DXFAnalyzerApp(root)
    root.mainloop()