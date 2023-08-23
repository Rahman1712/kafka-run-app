from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from db_utils import resource_path

bg_colour = "#00B6D8"

class UpdateDocPopup(tk.Frame):
    def __init__(self, parent, top, id, title, command, enabled, title_label, doc_label, is_get_started):
        self.bg_colour = bg_colour
        self.bg_colour_2 = "#03C7C7"
        super().__init__(parent, width=500, height=600, bg=self.bg_colour)

        self.parent = parent  # tab3
        self.top = top
        self.id = id
        self.title = title
        self.command = command
        self.enabled = enabled
        self.title_label = title_label
        self.doc_label = doc_label
        self.is_get_started = is_get_started

        self.create_widgets()

    def create_widgets(self):
        popup = Toplevel(self)
        popup.title("Update Kafka Doc")
        popup.resizable(False, False)
        popup.iconbitmap(resource_path('assets\\kafka.ico'))
        x = self.top.winfo_rootx() + 50
        y = self.top.winfo_rooty() + 50
        popup.geometry('400x270+' + str(x) + '+' + str(y))
        popup.overrideredirect(1)
        popup.grab_set()

        content_box = tk.Frame(popup, bg="#DEDEDE", highlightthickness=3,
                               highlightbackground=self.bg_colour_2,  padx=10, pady=1)
        content_box.pack(padx=5, pady=5)
        content_box.configure(highlightbackground=self.bg_colour_2)

        label_head = Label(content_box, text="Update Documentation", fg="#001B4A", bg=self.bg_colour_2, anchor="w", font=(
            "TkMenuFont", 10, 'bold'))
        label_head.pack(padx=10, pady=10)

        id_box = tk.Frame(content_box, bg="#DEDEDE")
        id_box.pack(anchor="w")
        Label(id_box, text="ID : ", bg="#DEDEDE", fg="#001B4A",
              font=("TkMenuFont", 12, 'bold')).grid(row=0, column=0)
        Label(id_box, text=self.id, bg="#DEDEDE", fg="#001B4A", font=(
            "TkMenuFont", 15, 'bold')).grid(row=0, column=1, padx=10)

        Label(content_box, text="Title and Command").pack()
        docTitle = StringVar(value=self.title)
        docTitleEntry = Entry(content_box, textvariable=docTitle, width=100)
        docTitleEntry.pack(pady=10, padx=10)

        docCommand_widget = Text(content_box, height=4, width=100)
        docCommand_widget.insert("1.0", self.command)
        docCommand_widget.pack(padx=10, pady=5)

        btn_box = tk.Frame(content_box, bg="#DEDEDE")
        btn_box.pack(anchor="center")
        update_button = Button(
            btn_box,
            text="UPDATE",
            bg="#283938",
            fg="white",
            cursor="hand2",
            width=10,
            font=("TkHeadingfont", 10),
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: self.update_kafka_doc(
                docTitle.get(), docCommand_widget.get("1.0", "end-1c"), popup)
        )
        update_button.grid(row=0, column=0, padx=10, pady=10)

        back_btn = Button(
            btn_box,
            width=10,
            text="Back",
            font=("TkHeadingfont", 10),
            bg="#283945",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=popup.destroy)
        back_btn.grid(row=0, column=1, padx=10, pady=10)

    def update_kafka_doc(self, docTitle, docCommand, popup):
        if docTitle.strip() == "" or docCommand.strip() == "":
            print("Please Fill the Fields")
        else:
            connection = sqlite3.connect(resource_path("data\\kafka.db"))
            cursor = connection.cursor()

            cursor.execute("UPDATE KAFKA_DOCS SET title = :title, command = :command, enabled = :enabled  WHERE id = :id", {
                        "id": self.id, "title": docTitle, "command": docCommand, "enabled": self.enabled})
            connection.commit()
            connection.close()

            self.parent.changeTitleDocValues(docTitle, self.title_label, docCommand, self.doc_label, self.is_get_started)
            
            popup.destroy()
