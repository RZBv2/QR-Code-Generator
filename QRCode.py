import qrcode
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw
import os
from pathlib import Path


class QRCodeGenerator:
    
    def __init__(self, data, image_path=None, output_path="qr_code.png", 
                 box_size=10, border=4, fill_color="black", back_color="white"):
        self.data = data
        self.image_path = image_path
        self.output_path = output_path
        self.box_size = box_size
        self.border = border
        self.fill_color = fill_color
        self.back_color = back_color
    
    def generate(self):
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=self.box_size,
                border=self.border,
            )
            qr.add_data(self.data)
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color=self.fill_color, back_color=self.back_color)
            
            if self.image_path and os.path.exists(self.image_path):
                qr_img = self._embed_image(qr_img, self.image_path)
            
            qr_img.save(self.output_path)
            return True, f"QR code saved to {self.output_path}"
        
        except Exception as e:
            return False, f"Error generating QR code: {str(e)}"
    
    def _embed_image(self, qr_img, image_path):
        try:
            logo = Image.open(image_path).convert("RGBA")
            
            qr_width, qr_height = qr_img.size
            logo_size = min(qr_width, qr_height) // 5
            
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            logo_bg = Image.new("RGB", (logo_size + 20, logo_size + 20), self.back_color)
            
            logo_bg.paste(logo, (10, 10), logo)
            
            logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo_bg, (logo_pos[0] - 10, logo_pos[1] - 10))
            
            return qr_img
        
        except Exception as e:
            messagebox.showwarning("Warning", f"Could not embed image: {str(e)}")
            return qr_img


class QRCodeGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.image_path = tk.StringVar()
        self.file_label = None
        
        self.setup_ui()
    
    def setup_ui(self):
        title = ttk.Label(self.root, text="High-Quality QR Code Generator", 
                         font=("Helvetica", 14, "bold"))
        title.pack(pady=10)
        
        ttk.Label(self.root, text="Enter Text or URL:").pack(anchor="w", padx=20, pady=(10, 0))
        self.data_entry = tk.Text(self.root, height=4, width=50)
        self.data_entry.pack(padx=20, pady=5)
        
        ttk.Label(self.root, text="Optional: Select Image to Embed:", 
                 font=("Helvetica", 10)).pack(anchor="w", padx=20, pady=(15, 0))
        
        img_frame = ttk.Frame(self.root)
        img_frame.pack(padx=20, pady=5, fill="x")
        
        ttk.Button(img_frame, text="Browse Image", 
                  command=self.browse_image).pack(side="left")
        self.file_label = ttk.Label(img_frame, text="No image selected", 
                                    foreground="gray")
        self.file_label.pack(side="left", padx=10)
        
        settings_frame = ttk.LabelFrame(self.root, text="Settings", padding=10)
        settings_frame.pack(padx=20, pady=10, fill="x")
        
        ttk.Label(settings_frame, text="Box Size:").grid(row=0, column=0, sticky="w")
        self.box_size = tk.IntVar(value=10)
        box_spinbox = ttk.Spinbox(settings_frame, from_=5, to=20, textvariable=self.box_size, width=10)
        box_spinbox.grid(row=0, column=1, sticky="w", padx=10)
        
        ttk.Label(settings_frame, text="Border:").grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.border = tk.IntVar(value=4)
        border_spinbox = ttk.Spinbox(settings_frame, from_=1, to=10, textvariable=self.border, width=10)
        border_spinbox.grid(row=0, column=3, sticky="w", padx=10)
        
        ttk.Label(settings_frame, text="QR Color:").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.fill_color = tk.StringVar(value="black")
        ttk.Combobox(settings_frame, textvariable=self.fill_color, 
                    values=["black", "blue", "red", "green"], state="readonly", 
                    width=10).grid(row=1, column=1, sticky="w", padx=10, pady=(10, 0))
        
        ttk.Label(settings_frame, text="Background Color:").grid(row=1, column=2, sticky="w", 
                                                                 padx=(20, 0), pady=(10, 0))
        self.back_color = tk.StringVar(value="white")
        ttk.Combobox(settings_frame, textvariable=self.back_color, 
                    values=["white", "black", "lightgray"], state="readonly", 
                    width=10).grid(row=1, column=3, sticky="w", padx=10, pady=(10, 0))
        
        ttk.Label(self.root, text="Save Location:").pack(anchor="w", padx=20, pady=(15, 0))
        
        output_frame = ttk.Frame(self.root)
        output_frame.pack(padx=20, pady=5, fill="x")
        
        self.output_path = tk.StringVar(value=str(Path.home() / "QR_Code.png"))
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).pack(side="left", fill="x", expand=True)
        ttk.Button(output_frame, text="Browse", 
                  command=self.browse_output).pack(side="left", padx=5)
        
        ttk.Button(self.root, text="Generate QR Code", 
                  command=self.generate_qr).pack(pady=(20, 10))
    
    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        if file_path:
            self.image_path.set(file_path)
            filename = os.path.basename(file_path)
            self.file_label.config(text=filename, foreground="black")
    
    def browse_output(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            self.output_path.set(file_path)
    
    def generate_qr(self):
        data = self.data_entry.get("1.0", "end-1c").strip()
        
        if not data:
            messagebox.showerror("Error", "Please enter text or URL")
            return
        
        generator = QRCodeGenerator(
            data=data,
            image_path=self.image_path.get() if self.image_path.get() else None,
            output_path=self.output_path.get(),
            box_size=self.box_size.get(),
            border=self.border.get(),
            fill_color=self.fill_color.get(),
            back_color=self.back_color.get()
        )
        
        success, message = generator.generate()
        
        if success:
            messagebox.showinfo("Success", message)
            self.data_entry.delete("1.0", "end")
            self.image_path.set("")
            self.file_label.config(text="No image selected", foreground="gray")
        else:
            messagebox.showerror("Error", message)


def main_gui():
    root = tk.Tk()
    app = QRCodeGUI(root)
    root.mainloop()


def main_cli():
    print("=" * 50)
    print("High-Quality QR Code Generator")
    print("=" * 50)
    
    data = input("\nEnter text or URL: ").strip()
    if not data:
        print("Error: Text/URL cannot be empty")
        return
    
    embed_image = input("Embed image in QR code? (y/n): ").lower() == 'y'
    image_path = None
    
    if embed_image:
        image_path = input("Enter image path: ").strip()
        if not os.path.exists(image_path):
            print("Warning: Image file not found. Generating QR code without image.")
            image_path = None
    
    output_path = input(f"Output path [{Path.home() / 'QR_Code.png'}]: ").strip()
    if not output_path:
        output_path = str(Path.home() / "QR_Code.png")
    
    generator = QRCodeGenerator(
        data=data,
        image_path=image_path,
        output_path=output_path,
        box_size=10,
        border=4
    )
    
    success, message = generator.generate()
    print(f"\n{message}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        main_cli()
    else:
        main_gui()
