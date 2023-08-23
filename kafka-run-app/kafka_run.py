import tkinter as tk
from main_frame import MainFrame
from db_utils import initialize_database, resource_path

class KafkaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kafka GUI")
        self.root.geometry('500x500')
        self.root.resizable(False, False)
        self.root.iconbitmap(resource_path('assets\\kafka.ico'))
        x = root.winfo_screenwidth() // 2 - 250
        y = int(root.winfo_screenheight() * 0.1)
        self.root.geometry('500x500+' + str(x) + '+' + str(y))

        initialize_database()
        
        self.main_frame = MainFrame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = KafkaApp(root)
    root.mainloop()
