# QR Code Generator

A simple yet powerful Python app that lets you create awesome QR codes with the ability to embed your logo or image right in the center. Perfect for branding, marketing, or just fun projects!

## Features

- **Easy-to-Use GUI**: Click buttons, fill in fields, and generate QR codes in seconds
- **CLI Mode**: Want to automate? Just use the command line version
- **Logo Embedding**: Drop your logo right into the center of the QR code
- **Tweak Everything**: Adjust size, borders, and colors to match your style
- **Smart Error Correction**: Handles embedded images without breaking the QR scan
- **PNG Output**: Saves as high-quality PNG files
- **Pick Your Colors**: Black/blue/red/green for QR codes, white/black/gray for backgrounds

## What You'll Need

- Python 3.7 or newer
- qrcode library with PIL support
- Pillow (the image library)
- tkinter (comes with Python, so you probably already have it)

## Installation

Quick and simple:

1. Grab the code (clone or download)

2. Set up a virtual environment (I recommend it):
   ```bash
   python -m venv .venv
   ```

3. Activate it:
   - **Windows**: `.venv\Scripts\activate`
   - **Mac/Linux**: `source .venv/bin/activate`

4. Install what you need:
   ```bash
   pip install qrcode[pil] Pillow
   ```

That's it! You're ready to go.

## How to Use It

### GUI Version (The Easy Way)

Just run it:
```bash
python QRCode.py
```

Then:
1. Type or paste your text/URL
2. Optionally pick an image to embed
3. Tweak the settings if you want (size, colors, etc.)
4. Pick where to save it
5. Hit the button and boom—your QR code is ready!

### Command Line Version (For Power Users)

Want to do it without the GUI?
```bash
python QRCode.py --cli
```

Just answer the prompts:
1. What text/URL do you want to encode?
2. Add a logo? (yes/no)
3. Where's the image? (if yes)
4. Where should I save the QR code?

## For Developers

### QRCodeGenerator Class

This is where the magic happens. Here's how to use it in your own code:

```python
generator = QRCodeGenerator(
    data="https://example.com",           # What to encode
    image_path="logo.png",               # Your logo (optional)
    output_path="my_qr.png",             # Where to save
    box_size=10,                          # Size of each square
    border=4,                             # Border thickness
    fill_color="black",                  # QR code color
    back_color="white"                   # Background color
)

success, message = generator.generate()
```

### QRCodeGUI Class

Handles all the GUI stuff. It's built with tkinter and includes:
- `setup_ui()`: Creates all the buttons and fields
- `browse_image()`: Opens a file picker for images
- `browse_output()`: Lets you choose where to save
- `generate_qr()`: Does the actual QR generation

## Color Options

**For the QR code itself:** black, blue, red, green

**For the background:** white, black, lightgray

## Output

- **Default spot:** Your home folder as `QR_Code.png`
- **Format:** PNG (works everywhere)
- **Quality:** Crisp and clear, tweakable size

## Quick Examples

### Basic QR Code
1. Run: `python QRCode.py`
2. Type: "Hello World"
3. Click the button
4. Done!

### QR with Your Logo
1. Run: `python QRCode.py`
2. Type: "https://example.com"
3. Click "Browse Image" and pick your logo
4. Hit generate
5. Your branded QR is ready!

### Using the Command Line
```bash
python QRCode.py --cli
# Answer a few questions and you're set
```

## Good to Know

- The app automatically uses extra error correction when you add a logo (so it still scans fine)
- Your logo gets shrunk down to about 20% of the QR code size (looks sharp!)
- There's a white border around embedded images to keep them crisp and readable

## License

MIT License - Do whatever you want with it. Use it, fork it, modify it, sell it. No strings attached!

## Author

Md. Razab Ali
