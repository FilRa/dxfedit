import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ezdxf

class ContourTab:
    def __init__(self, notebook, analyze_tab):
        self.frame = ttk.Frame(notebook)
        self.analyze_tab = analyze_tab  # Reference to AnalyzeTab for the loaded document

        # UI Elements
        self.interval_label = ttk.Label(self.frame, text="Contour Interval:")
        self.interval_label.pack(pady=5)

        self.interval_var = tk.StringVar(value="0.2")
        self.interval_entry = ttk.Entry(self.frame, textvariable=self.interval_var)
        self.interval_entry.pack(pady=5)

        self.threshold_label = ttk.Label(self.frame, text="Simplification Threshold:")
        self.threshold_label.pack(pady=5)

        self.threshold_var = tk.StringVar(value="1.0")
        self.threshold_entry = ttk.Entry(self.frame, textvariable=self.threshold_var)
        self.threshold_entry.pack(pady=5)

        self.generate_button = ttk.Button(self.frame, text="Generate Contour Lines", command=self.generate_contours)
        self.generate_button.pack(pady=10)

    def generate_contours(self):
        if not self.analyze_tab.doc:
            messagebox.showerror("Error", "No DXF file loaded. Please load a file in the Analyze DXF tab first.")
            return

        try:
            doc = self.analyze_tab.doc
            msp = doc.modelspace()

            # Read parameters from GUI
            interval = float(self.interval_var.get())
            threshold = float(self.threshold_var.get())

            # Find POLYFACEMESH entities (as POLYLINE with is_poly_face_mesh = True)
            polyfacemeshes = [entity for entity in msp if entity.dxftype() == "POLYLINE" and entity.is_poly_face_mesh]
            if not polyfacemeshes:
                messagebox.showinfo("No PolyFaceMesh", "No POLYFACEMESH entities found in the DXF file.")
                return

            # Collect Z values from POLYFACEMESH vertices
            z_values = []
            for mesh in polyfacemeshes:
                for vertex in mesh.vertices:
                    location = vertex.dxf.location  # Access location as a `Vec3` object
                    z_values.append(location.z)

            if not z_values:
                messagebox.showerror("Error", "No vertices with valid Z coordinates found in POLYFACEMESH entities.")
                return

            min_z, max_z = min(z_values), max(z_values)

            # Placeholder for contour generation logic
            current_z = min_z
            contours = []
            while current_z <= max_z:
                # Generate contour polyline (simplified placeholder logic)
                polyline = msp.add_lwpolyline([(0, current_z), (1, current_z)])  # Dummy polyline example
                contours.append(polyline)
                current_z += interval

            # Save contours to a new DXF file
            output_path = filedialog.asksaveasfilename(defaultextension=".dxf", filetypes=[("DXF Files", "*.dxf")])
            if not output_path:
                return
            doc.saveas(output_path)
            messagebox.showinfo("Success", f"Contours saved to {output_path}.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process DXF file: {e}")

    def process_contourlines(self):
        if not self.analyze_tab.doc:
            messagebox.showerror("Error", "No DXF file loaded. Please load a file in the Analyze tab first.")
            return

        try:
            # Access the DXF document from AnalyzeTab
            doc = self.analyze_tab.doc
            msp = doc.modelspace()

            # Find POLYFACEMESH entities
            polyfacemeshes = [entity for entity in msp if entity.dxftype() == "POLYLINE" and entity.is_poly_face_mesh]

            if not polyfacemeshes:
                messagebox.showerror("Error", "No POLYFACEMESH entities found in the DXF file.")
                return

            # Get parameters from the GUI
            try:
                interval = float(self.interval_entry.get())
                threshold = float(self.threshold_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for the interval and threshold.")
                return

            # Process contour lines (placeholder for actual logic)
            # This will involve processing the vertices of each POLYFACEMESH
            for polyfacemesh in polyfacemeshes:
                vertices = list(polyfacemesh.vertices)  # Extract vertices from POLYFACEMESH
                # Implement contour line generation logic here

            # Save the updated DXF
            output_file = filedialog.asksaveasfilename(defaultextension=".dxf", filetypes=[("DXF Files", "*.dxf")])
            if output_file:
                doc.saveas(output_file)
                messagebox.showinfo("Success", "Contour lines generated and saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process DXF file: {e}")