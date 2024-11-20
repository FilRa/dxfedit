import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ezdxf

class AnalyzeTab:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        self.doc = None  # Store the loaded DXF document

        # UI Elements
        self.load_button = ttk.Button(self.frame, text="Load DXF File", command=self.load_dxf)
        self.load_button.pack(pady=10)

        self.output_label = tk.Text(self.frame, height=10, width=50)
        self.output_label.pack(pady=10)

    def load_dxf(self):
        file_path = filedialog.askopenfilename(filetypes=[("DXF Files", "*.dxf")])
        if not file_path:
            return

        try:
            self.doc = ezdxf.readfile(file_path)
            msp = self.doc.modelspace()

            # Analyze DXF
            entity_counts = {"POLYFACEMESH": 0, "LINE": 0, "LWPOLYLINE": 0, "TEXT": 0, "3DFACE": 0}
            for entity in msp:
                entity_type = entity.dxftype()

                # Ensure POLYFACEMESH is explicitly counted
                if entity_type == "POLYLINE" and entity.is_poly_face_mesh:
                    entity_type = "POLYFACEMESH"

                entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1

            # Display analysis results
            self.output_label.delete(1.0, tk.END)
            for entity_type, count in entity_counts.items():
                self.output_label.insert(tk.END, f"{entity_type}: {count}\n")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load DXF file: {e}")