# 🍓 Fruit OCR Automation

This project uses [EasyOCR](https://github.com/JaidedAI/EasyOCR) and Python automation to detect fruit names on screen and automatically send them into another program via AutoHotkey.  

This is only useful for the current fairy event when submitting to the fountain, however the workflow is generic enough to be used for other events in future.

It works on both **GPU (CUDA)** and **CPU-only** systems.  

---

## 🚀 Features
- OCR text recognition using EasyOCR  
- Fuzzy matching against a target word list  
- Hotkey-based workflow with queue processing  
- AutoHotkey integration for sending recognized names  

---

## 📦 Setup Instructions (Windows)

### 1. Install Python 3
1. Download Python 3 from [python.org](https://www.python.org/downloads/).  
2. Run the installer:  
   - ✅ Check **“Add Python to PATH”**  
   - Click *Install Now*
Verify installation:
  python --version

### 2. Clone the repository
    git clone https://github.com/thennak3/gagfairyocr.git
    cd gagfairyocr

### 3. Create a virtual environment (recommended)
    python -m venv venv

Activate it:
- **Windows**:  
    venv\Scripts\activate  
- **Linux/macOS**:  
    source venv/bin/activate  

### 4. Install dependencies
    pip install -r requirements.txt
This will install all necessary libraries for the project.  
On a machine **without a GPU**, PyTorch will fall back to CPU automatically.

### 5. Install Autohotkeyv2
1. Download Autohotkeyv2 from [Autohotkey](https://www.autohotkey.com/v2/)
2. Run the installer

---

## 🖼️ Configuration

You’ll need to define screen coordinates for four areas:

1. **Fruit capture area**  
   - Use `imagecheck.jpg` as an example capture area.  
   - Uncomment line 94 in `ocr_fsm.py`:  
     ```python
     # img.save(f"raw_{timestamp}.png")
     ```  
     This will output test captures.  

2. **Adjust capture region**  
   - Edit line 38 in `ocr_fsm.py`:  
     ```python
     large_region = {"top": 308, "left": 1320, "width": 1100, "height": 650}
     ```  
   - Use **AutoHotkey Window Spy** (installed with AutoHotkey) to find coordinates.  
   - Remember: `left` = X position, `top` = Y position.  

3. **Update AutoHotkey script**  
   Edit `SendNameListener.ahk` to match your screen:  
   ```ahk
   SendName(name) {
       MouseClick "L", 2227, 1183 ; Clear filter button
       Sleep 100
       MouseClick "L", 2163, 1192 ; Search textbox
       Sleep 100
       Send "{Blind}" name
       Sleep 100
       MouseClick "L", 1569, 1288 ; Fruit filter button
   }
  Replace coordinates with values from Window Spy.

## ▶️ Usage
Run the OCR script:
    python ocr_fsm.py
Run the AutoHotkey listener by double-clicking SendNameListener.ahk or opening it with AutoHotkey v2.

Check CUDA support with:
    python cudacheck.py


### Workflow
1. Press `]` → Start the script (global hotkeys work even with Roblox active).  
2. OCR scans text and matches fruit names.  
3. Script presses **E** to open the chat window, then **N** to enter the fruit filter.  
4. You must manually click **Submit Fruit**.  
5. Press **N** to search for the next fruit.  
6. When finished, press **Q** (and `Ctrl+C` in the terminal if needed).  

---

## 🎮 Hotkeys
- `]` → Start OCR scanning  
- `n` → Process next item in queue  
- `q` → Quit the script  

---

## 📝 Notes
- If running on a machine with CUDA-capable GPU and the correct PyTorch + CUDA installed, the program will automatically use GPU acceleration.  
- If running on a machine **without GPU/CUDA**, the program will still run, but slower.  
