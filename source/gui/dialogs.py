import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
from typing import Optional

from gui.components import LoadingDialog, ValueInputDialog


class FileSelectionDialog:
    
    @staticmethod
    def prompt_for_file(parent, current_game_id: str = None) -> Optional[str]:
        from config.settings import MESSAGES, FILE_SETTINGS, get_current_game_settings
        
        if current_game_id is None:
            if hasattr(parent, 'main_window') and hasattr(parent.main_window, 'current_game_id'):
                current_game_id = parent.main_window.current_game_id
            elif hasattr(parent, 'current_game_id'):
                current_game_id = parent.current_game_id
        
        game_settings = get_current_game_settings(current_game_id)
        executable_name = game_settings.get('executable_name', 'game.exe')
        
        file_not_found_msg = MESSAGES['file_not_found'].format(game_exe=executable_name)
        select_file_title = MESSAGES['select_file_title'].format(game_exe=executable_name)
        wrong_file_error = MESSAGES['wrong_file_error'].format(game_exe=executable_name)
        
        result = messagebox.askyesno("File Not Found", 
                                   f"{file_not_found_msg}\n\n"
                                   f"{MESSAGES['select_file_prompt']}")
        if result:
            filename = filedialog.askopenfilename(
                title=select_file_title,
                filetypes=FILE_SETTINGS['file_type_filters']
            )
            if filename:
                if filename.lower().endswith(executable_name.lower()):
                    return filename
                else:
                    messagebox.showerror("Error", wrong_file_error)
        
        return None


class NexusDialog:
    
    @staticmethod
    def open_nexus_page(game_id: str = None):
        from config.settings import get_current_game_settings
        game_settings = get_current_game_settings(game_id)
        nexus_url = game_settings.get('nexus_mods_url', '')
        
        if nexus_url:
            try:
                webbrowser.open(nexus_url)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open browser: {str(e)}")
        else:
            messagebox.showinfo("Info", "No Nexus Mods URL configured for this game.")


class ConfirmationDialog:
    
    @staticmethod
    def confirm_backup_with_active_tweaks() -> bool:
        from config.settings import MESSAGES
        return messagebox.showwarning("Warning", MESSAGES['backup_with_active_warning']) == 'ok'
    
    @staticmethod
    def confirm_disable_all_tweaks(count: int) -> bool:
        from config.settings import MESSAGES
        return messagebox.askyesno("Confirm", MESSAGES['confirm_disable_all'].format(count=count))
    
    @staticmethod
    def confirm_restore_backup() -> bool:
        from config.settings import MESSAGES
        return messagebox.askyesno("Confirm", MESSAGES['confirm_restore_backup'])


class ErrorDialog:
    
    @staticmethod
    def show_file_not_found(game_id: str = None):
        from config.settings import MESSAGES, get_current_game_settings
        
        game_settings = get_current_game_settings(game_id)
        executable_name = game_settings.get('executable_name', 'game.exe')
        file_not_found_error = MESSAGES['file_not_found_error'].format(game_exe=executable_name)
        messagebox.showerror("Error", file_not_found_error)
    
    @staticmethod
    def show_no_backup():
        from config.settings import MESSAGES
        messagebox.showerror("Error", MESSAGES['no_backup_error'])
    
    @staticmethod
    def show_no_active_tweaks():
        from config.settings import MESSAGES
        messagebox.showinfo("Info", MESSAGES['no_active_tweaks'])
    
    @staticmethod
    def show_operation_failed(operation: str, error: str):
        from config.settings import MESSAGES
        messagebox.showerror("Error", MESSAGES['operation_failed'].format(operation=operation, error=error))
    
    @staticmethod
    def show_success(operation: str):
        from config.settings import MESSAGES
        messagebox.showinfo("Success", MESSAGES['success'].format(operation=operation))
    
    @staticmethod
    def show_info(title: str, message: str):
        root = tk.Tk()
        root.withdraw()
        
        from config.settings import DIALOG_DIMENSIONS, FONT_CONFIG
        
        dialog = tk.Toplevel(root)
        dialog.title(title)
        dialog.geometry(DIALOG_DIMENSIONS['info_dialog'])
        dialog.resizable(True, True)
        dialog.transient(root)
        
        try:
            dialog.grab_set()
        except tk.TclError:
            pass
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400)
        y = (dialog.winfo_screenheight() // 2) - (300)
        dialog.geometry(f"{DIALOG_DIMENSIONS['info_dialog']}+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=FONT_CONFIG['text'], 
                             bg="white", fg="black", relief=tk.SUNKEN, borderwidth=1)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget.insert(tk.END, message)
        text_widget.config(state=tk.DISABLED)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        from config.settings import UI_TEXT
        ttk.Button(button_frame, text=UI_TEXT['close_button'], command=lambda: [dialog.destroy(), root.destroy()]).pack(side=tk.RIGHT)
        
        dialog.focus_set()
        dialog.wait_window()
        
        root.destroy()


class SimpleLoadingDialog:
    
    def __init__(self, parent, operation: str, tweak_name: str):
        self.parent = parent
        from config.settings import DIALOG_DIMENSIONS, FONT_CONFIG
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Applying Tweak")
        self.dialog.geometry(DIALOG_DIMENSIONS['simple_loading'])
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.center_dialog()
        
        message = f"{operation} {tweak_name}..."
        message_label = ttk.Label(self.dialog, text=message, font=FONT_CONFIG['subtitle'])
        message_label.pack(pady=20)
        
        progress = ttk.Progressbar(self.dialog, mode='indeterminate')
        progress.pack(pady=10, padx=20, fill=tk.X)
        progress.start()
        
        self.dialog.update()
    
    def center_dialog(self):
        self.dialog.update_idletasks()
        main_x = self.parent.winfo_rootx()
        main_y = self.parent.winfo_rooty()
        main_width = self.parent.winfo_width()
        main_height = self.parent.winfo_height()
        
        from config.settings import DIALOG_DIMENSIONS
        
        x = main_x + (main_width // 2) - (150)
        y = main_y + (main_height // 2) - (50)
        
        self.dialog.geometry(f"{DIALOG_DIMENSIONS['simple_loading']}+{x}+{y}")
    
    def close(self):
        self.dialog.destroy()
