import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import GameTweakPackGUI


def main():
    try:
        root = tk.Tk()
        
        app = GameTweakPackGUI(root)
        
        root.mainloop()
        
    except Exception as e:
        import traceback
        error_msg = f"An unexpected error occurred:\n{str(e)}\n\n{traceback.format_exc()}"
        
        try:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", error_msg)
        except:
            print(error_msg, file=sys.stderr)
        
        sys.exit(1)


if __name__ == "__main__":
    main()
