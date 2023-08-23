from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import clipboard
import os
from db_utils import resource_path
import tkinter.messagebox as messagebox
from update_doc import UpdateDocPopup

class SettingsFrame:
    def __init__(self, parent):
        self.parent = parent
        self.bg_colour_2 = "#03C7C7"  # "#F7DC6F"
        self.bg_colour_3 = "#7AEDF8"
        self.create_widgets()

    def create_widgets(self):
        global kafka_img
        top = Toplevel()
        top.title('Settings')
        top.iconbitmap(resource_path('assets\\kafka.ico'))
        top.geometry('500x400')
        top.grab_set()
        top.resizable(False, False)

        frameTop = Frame(top, width=500, height=500, bg=self.bg_colour_2)
        frameTop.pack()
        frameTop.pack_propagate(False)

        img = Image.open(resource_path("assets\\kafka_blue.jpeg"))
        img = img.resize((img.size[0]//4, img.size[1]//4), Image.LANCZOS)
        kafka_img = ImageTk.PhotoImage(img)
        logo_widget = Label(frameTop, image=kafka_img, borderwidth=0.5)
        logo_widget.pack(pady=5)

        style = ttk.Style()
        if not custom_style_exists("custom_style"):
            style.theme_create("custom_style", parent="alt", settings={
                "TNotebook": {
                    "configure": {
                        "tabmargins": [2,5,2,0],
                        "background": "lightgray",
                        
                    },
                    "tab": {
                        "configure": {
                            "padding": [10,5],
                            "borderwidth": 2,
                            "background": "gray",
                            "foreground": "white",
                        }
                    },
                    "TNotebook.Tab": {
                        "configure": {
                            "padding": [10,5],
                            
                        }
                    },
                }
            })
        style.theme_use("custom_style")
        style.layout("Tab",
                     [("Notebook.tab", 
                       {
                           'sticky': 'nswe', 
                           'children': [('Notebook.label', {'side':'top', 'sticky': ''})]              
                        }
                    )])
        style.map("TNotebook.Tab", 
                  background=[("selected", self.bg_colour_3)], 
                  foreground=[("selected", "#001B4A")], 
                  font=[("selected",  ("Arial", 10, 'bold'))],
                )

        notebook = ttk.Notebook(frameTop, width=480)

        tab1 = Tab1(notebook)
        tab2 = Tab2(notebook, top)
        tab3 = Tab3(notebook, top)
        tab4 = Tab4(notebook, top, self.parent)

        tab1.pack(fill="both", expand=1)
        tab2.pack(fill="both", expand=1)
        tab3.pack(fill="both", expand=1)
        tab4.pack(fill="both", expand=1)

        notebook.add(tab1, text="Documentation")
        notebook.add(tab2, text="Add Doc")
        notebook.add(tab3, text="Manage Docs")
        notebook.add(tab4, text="Edit Settings")

        notebook.pack(pady=15)


# ================ Common functions =======================

#=====open cmd======
def open_cmd(path):
    cmd_command = 'start cmd /k "cd /d {}"'.format(path)
    os.system(cmd_command)

#=====copy======
def copy_text(label_text):
    clipboard.copy(label_text)   
            
#=====custom style check======
def custom_style_exists(style_name):
    existing_styles = ttk.Style().theme_names()
    return style_name in existing_styles


#-------------------------------------------------------
class Tab1(tk.Frame):

    def __init__(self, parent):

        self.bg_colour_2 = "#03C7C7"
        self.bg_colour_3 = "#7AEDF8"
        super().__init__(parent, bg=self.bg_colour_3)
        self.parent = parent

        # ===========TAB1===============================
        tab1_content = ttk.Frame(self)

        connection = sqlite3.connect(resource_path("data\\kafka.db"))
        cursor = connection.cursor()

        KAFKA_HOME = cursor.execute("SELECT VALUE FROM KAFKA WHERE KEY='KAFKA_HOME'").fetchone()[0]

        canvas = tk.Canvas(tab1_content, width=440, height=300)
        scrollbar = ttk.Scrollbar(
            tab1_content, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container = Frame(scrollable_frame)
        # ==========CMD KAFKA HOME============================
        content_box = Frame(container, borderwidth=1,
                         bg=self.bg_colour_2, padx=10, pady=10)
        content_box.grid(row=0, column=0, padx=10, pady=10)

        Label(content_box, text="Open Cmd KafKa Home", bg=self.bg_colour_3, fg="#000000", font=(
            "TkMenuFont", 10, 'bold'), justify="center").grid(row=0, column=0, pady=(0, 5))

        Button(
            content_box,
            text="open cmd",
            font=("TkHeadingfont", 12),
            bg="#283938",
            fg="white",
            activebackground="#badee2",
            activeforeground="black",
            cursor="hand2",
            borderwidth=0,
            command=lambda: open_cmd(KAFKA_HOME)
        ).grid(row=1, column=0, pady=2)

        # ===============IMG COPY=======================
        global copy_icon
        copy_img = Image.open(resource_path("assets\\copy.png"))
        copy_img = copy_img.resize(
            (copy_img.size[0] // 2, copy_img.size[1] // 2), Image.LANCZOS)
        copy_icon = ImageTk.PhotoImage(copy_img)
        # ===============DOCS============================
        kafka_docs_datas = cursor.execute("SELECT title,command FROM KAFKA_DOCS WHERE enabled = true").fetchall()

        for row, (title, command) in enumerate(kafka_docs_datas, start=1):
            content_box = tk.Frame(container, bg="#DEDEDE",
                                highlightbackground=self.bg_colour_2, highlightthickness=1, padx=10, pady=5)
            content_box.grid(row=row, column=0, padx=10, pady=10, sticky="we")

            # label_width = content_box.winfo_width()
            Label(content_box, text=title, bg="#DEDEDE", fg="#001B4A", 
                #   width=label_width,
                  font=("TkMenuFont", 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 2), padx=(20,0), sticky="w")

            copy_button = Button(content_box, image=copy_icon, cursor="hand2", borderwidth=0,
                                 command=lambda text=command: copy_text(text))
            copy_button.grid(row=1, column=0, pady=2)

            # Label(content_box, text=command, wraplength=370, bg="#DEDEDE", fg="#000000", anchor="w", font=("Arial", 10, 'bold')).grid(row=1, column=1, padx=10, pady=2, sticky="w")
            command_frame = tk.Frame(content_box, bg="#DEDEDE")
            command_frame.grid(row=1, column=1, padx=10, pady=2)
            if "Get Started" in title:
                num_lines = len(command.split('\n'))
                command_text_widget = tk.Text(command_frame, bg="#DEDEDE", fg="#000000", wrap="none", font=("Arial", 10, 'bold'), height=num_lines, width=50)
                command_text_widget.insert("1.0", command)
                command_text_widget.config(state="disabled")
                command_text_widget.pack(side="left", fill="both", expand=True)
            else:
                Label(command_frame, text=command, bg="#DEDEDE", fg="#000000",
                    wraplength=370, anchor="w", font=("Arial", 10, 'bold')).pack(side="left", fill="x", expand=True)

        tab1_content.pack()
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        container.pack()

        connection.close()


#-------------------------------------------------------
class Tab2(tk.Frame):
    def __init__(self, parent, top):

        self.bg_colour_3 = "#7AEDF8"
        super().__init__(parent, bg=self.bg_colour_3)
        self.parent = parent
        self.top = top

        # =============================TAB2=======================================
        tab2_content = ttk.Frame(self)

        box = Frame(tab2_content, borderwidth=1)
        Label(box, text="KAFKA DOCUMENTATION ADD", bg=self.bg_colour_3, fg="#000000", font=(
            "TkMenuFont", 10, 'bold'), justify="center").pack(pady=(5, 10))

        Label(box, text="Title and Command", fg="#283938").pack()
        docTitle = StringVar(value='')
        docTitleEntry = Entry(box, textvariable=docTitle, width=100)
        docTitleEntry.pack(pady=10, padx=10)

        docCommand_widget = Text(box, height=4, width=100)
        docCommand_widget.insert("1.0", "")
        docCommand_widget.pack(padx=10, pady=5)
        Button(
            box,
            text="ADD",
            bg="#283938",
            fg="white",
            cursor="hand2",
            font=("TkHeadingfont", 12),
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: self.add_kafka(
                docTitle.get(), docCommand_widget.get("1.0", "end-1c"), self.top)
        ).pack()

        tab2_content.pack(padx=10, pady=(10, 0))
        box.pack(padx=10, pady=5)

    #=====ADD======
    def add_kafka(self, docTitle, docCommand, top: Toplevel):
        if docTitle.strip() == "" or docCommand.strip() == "":
            print("Please Fill the Fields")
        else:
            connection = sqlite3.connect(resource_path("data\\kafka.db"))
            cursor = connection.cursor()
            
            cursor.execute("insert into KAFKA_DOCS(title, command, enabled) values (?,?,?)", (docTitle, docCommand, True))
            connection.commit()
            connection.close()
            top.destroy()


#-------------------------------------------------------
class Tab3(tk.Frame):
    def __init__(self, parent, top):
        
        self.bg_colour_3 = "#7AEDF8"
        self.bg_colour_2 = "#03C7C7" 
        super().__init__(parent, bg=self.bg_colour_3)
        self.parent = parent
        self.top = top

        # ===========TAB3===============================
        tab3_content = ttk.Frame(self)

        connection = sqlite3.connect(resource_path("data\\kafka.db"))
        cursor = connection.cursor()
        kafka_docs_datas = cursor.execute("SELECT * FROM KAFKA_DOCS").fetchall()  # [(id, title, command, enabled),...]
        self.kafka_docs_datas = kafka_docs_datas

        canvas = tk.Canvas(tab3_content, width=440, height=300)
        scrollbar = ttk.Scrollbar(
            tab3_content, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container = Frame(scrollable_frame)
 
        Label(container, text="Manage Documentaion Details", fg="#001B4A", bg= self.bg_colour_2, anchor="w", font=(
                "TkMenuFont", 10, 'bold')).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # ===============DOCS============================

        for row, (id, title, command, enabled) in enumerate(self.kafka_docs_datas, start=1):
            content_box = tk.Frame(container, bg="#DEDEDE", highlightthickness=1,highlightbackground=self.bg_colour_2,  padx=10, pady=3)
            content_box.grid(row=row, column=0, padx=10, pady=3, sticky="we")
            content_box.configure(highlightbackground=self.bg_colour_2)

            left_box = tk.Frame(content_box, bg="#DEDEDE")
            left_box.grid(row=0, column=0, pady=(0, 2), padx=(2, 0), sticky="w")
            
            left_inner_box = tk.Frame(left_box, bg="#DEDEDE")
            left_inner_box.pack(anchor="w")
            title_label = Label(left_inner_box, text=title, bg="#DEDEDE", fg="#001B4A", font=("TkMenuFont", 8, 'bold'))
            title_label.grid(row=0, column=0)
            if enabled == 1:
                enabled_text = "Enabled"
                label_bg_color = "#7EBC9F"
                label_fg_color = "#2A3E35"
            else:
                enabled_text = "Disabled"
                label_bg_color = "#F0ACB3"
                label_fg_color = "#491117"
            status_label = Label(left_inner_box, text=enabled_text, bg=label_bg_color, fg=label_fg_color, font=("TkMenuFont", 8, 'bold'))
            status_label.grid(row=0, column=1, padx=10)

            # cmd_label = Label(left_box, text=command, wraplength=340, bg="#DEDEDE", fg="#000000", anchor="w", font=("Arial", 8, 'bold'))
            # cmd_label.pack(anchor="w")
            if "Get Started" in title:
                num_lines = len(command.split('\n'))
                cmd_label = tk.Text(left_box, bg="#DEDEDE", fg="#000000", wrap="none", font=("Arial", 8, 'bold'), height=num_lines, width=50)
                cmd_label.insert("1.0", command)
                cmd_label.config(state="disabled")
                cmd_label.pack(anchor="w", pady=(2,0))
                is_get_started = True
            else:
                cmd_label = Label(left_box, text=command, wraplength=330, bg="#DEDEDE", fg="#000000", anchor="w", font=("Arial", 8, 'bold'))
                cmd_label.pack(anchor="w", padx=(0,5))
                is_get_started = False

            right_box = tk.Frame(content_box, bg="#DEDEDE")
            right_box.grid(row=0, column=1, pady=2, sticky="e")

            btn_update_doc = Button(right_box, text="Update", width=8, cursor="hand2", borderwidth=0,bg="#03C7C7",  fg="white")
            update_doc_command = lambda id=id, title=title, command=command,enabled=enabled, title_label=title_label, doc_label=cmd_label, is_get_started=is_get_started: self.update_doc_value(id, title, command, enabled,title_label ,doc_label, is_get_started)
            btn_update_doc.config(command= update_doc_command)
            btn_update_doc.pack(side="top", anchor="e",pady=1)
            
            btn_update = Button(right_box, text="Visible", width=8, cursor="hand2", borderwidth=0, 
            bg="#696767", fg="white")
            update_command = lambda id=id, enabled=enabled, status_label=status_label, row=row, btn_update=btn_update:self.update_enabled(id, enabled, status_label, row, btn_update)
            btn_update.config(command=update_command)
            btn_update.pack(side="top", anchor="e", pady=1)

            Button(right_box, text="Delete", width=8, cursor="hand2", borderwidth=0,
                   bg="#BA3049",  fg="white",
                   command=lambda id=id, content_box=content_box: self.confirm_delete(id, content_box, self.top)).pack(side="top", anchor="e",pady=1)

            content_box.grid_columnconfigure(0, weight=1)
            content_box.grid_columnconfigure(1, weight=1)


        tab3_content.pack()
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        container.pack()

        connection.close()


    #=====Update Enabled======
    def update_enabled(self, id, enabled, status_label: Label ,row, btn_update: Button):
        connection = sqlite3.connect(resource_path("data\\kafka.db"))
        cursor = connection.cursor()
        updated_enabled = not enabled
        cursor.execute("UPDATE KAFKA_DOCS SET enabled = ? WHERE id = ?", (updated_enabled, id))
        connection.commit()
        connection.close()
        
        if updated_enabled:
            status_label.config(text="Enabled", bg="#7EBC9F", fg="#2A3E35")
        else:
            status_label.config(text="Disabled", bg="#F0ACB3", fg="#491117")

        new_update_command = lambda id=id, enabled=updated_enabled, status_label=status_label, row=row, btn_update=btn_update:self.update_enabled(id, enabled, status_label, row, btn_update)
        btn_update.config(command=new_update_command)
    
    #=====Delete By id======
    def delete_doc(self, id, content_frame: Frame):
        connection = sqlite3.connect(resource_path("data\\kafka.db"))
        cursor = connection.cursor()
        cursor.execute("DELETE FROM KAFKA_DOCS WHERE id = ?", (id,))
        connection.commit()
        connection.close()
        content_frame.destroy()

    #====Message Confirm=====
    def confirm_delete(self, id, content_box, parent):
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this document?", parent=parent)

        if confirm:
            self.delete_doc(id, content_box)

    #====Update Doc Values=====
    def update_doc_value(self, id, title, command, enabled, title_label, doc_label, is_get_started):
        doc_popup = UpdateDocPopup(self, self.top, id, title, command, enabled , title_label, doc_label, is_get_started)
        doc_popup.pack(fill=tk.BOTH, expand=True)

    def changeTitleDocValues(self, title, title_label, docVal, doc_label, is_get_started):
        title_label.config(text = title)
        if is_get_started:
            doc_label.config(state="normal")
            doc_label.delete("1.0", "end")  
            doc_label.insert("1.0", docVal)  
            doc_label.config(state="disabled")
        else:
            doc_label.config(text = docVal)

#-------------------------------------------------------
class Tab4(tk.Frame):
    def __init__(self, parent, top, main_frame):
        
        self.bg_colour_3 = "#7AEDF8"
        super().__init__(parent, bg=self.bg_colour_3)
        self.parent = parent
        self.top = top

        # =============================TAB3=======================================
        tab4_content = ttk.Frame(self)

        connection = sqlite3.connect(resource_path("data\\kafka.db"))
        cursor = connection.cursor()
        KAFKA_HOME = cursor.execute("SELECT VALUE FROM KAFKA WHERE KEY='KAFKA_HOME'").fetchone()[0]

        box = Frame(tab4_content, borderwidth=1)
        Label(box, text="KAFKA HOME", bg=self.bg_colour_3, fg="#000000", font=(
            "TkMenuFont", 10, 'bold'), justify="center").grid(row=0, column=0, columnspan=3, pady=(5, 10))
        text_widget = Text(box, height=4, width=40)
        text_widget.insert("1.0", KAFKA_HOME)
        text_widget.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
        Button(
            box,
            text="Update",
            bg="#283938",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: self.update_kafka(
                text_widget.get("1.0", "end-1c"), self.top, main_frame)
        ).grid(row=1, column=4)

        kafka_env = "C:\kafka\kafka_folder_path"  # "C:\kafka\kafka_2.13-2.8.0"
        try:
            kafka_env = os.environ['KAFKA_HOME']
        except KeyError:
            print("Environment variable 'KAFKA_HOME' not found.")

        Label(box, text="Environment Value:", wraplength=400).grid(
            row=2, column=0, pady=(10, 0))
        Label(box, text=kafka_env, wraplength=400, fg="#012970").grid(
            row=3, column=0, pady=(0, 10))
        Button(box, text="copy", cursor="hand2", bg="#283938",
                fg="white", borderwidth=0, activebackground="#badee2", activeforeground="black",
                command=lambda: copy_text(kafka_env)).grid(row=3, column=1, pady=(0, 10))

        tab4_content.pack(padx=10, pady=(10, 0))
        box.pack(padx=10, pady=5)

        connection.close()

    #=====Update======
    def update_kafka(self, new_kafka_home, top: Toplevel, main_frame):
        if new_kafka_home.strip() == "":
            print("Please Fill the Field")
        else:
            connection = sqlite3.connect(resource_path("data\\kafka.db"))
            cursor = connection.cursor()

            kafka_values = [
                ("KAFKA_HOME", new_kafka_home),
                ("ZOOKEEPER", new_kafka_home + "\\bin\\windows\\zookeeper-server-start.bat " +
                    new_kafka_home + "\\config\\zookeeper.properties"),
                ("KAFKA_SERVER", new_kafka_home + "\\bin\\windows\\kafka-server-start.bat " +
                    new_kafka_home + "\\config\\server.properties"),
                ("TOPIC_CREATE_PRE", new_kafka_home +
                    "\\bin\\windows\\kafka-topics.bat --bootstrap-server "),
                ("KAFKA_PRODUCER_PRE", new_kafka_home +
                    "\\bin\\windows\\kafka-console-producer.bat --broker-list "),
                ("KAFKA_CONSUMER_PRE", new_kafka_home +
                    "\\bin\\windows\\kafka-console-consumer.bat --bootstrap-server ")
            ]

            for key, value in kafka_values:
                cursor.execute(
                    "UPDATE KAFKA SET VALUE = ? WHERE KEY = ?", (value, key))

            main_frame.changeLabelTexts(kafka_values[1][1], kafka_values[2][1])

            connection.commit()
            connection.close()
            top.destroy()       


#-------------------------------------------------------