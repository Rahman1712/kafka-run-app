from tkinter import *
from PIL import Image, ImageTk
import sqlite3
import os
from db_utils import resource_path

class ProducerFrame:
    def __init__(self, parent):
        self.parent = parent
        self.bg_colour_2 = "#03C7C7"  # "#F7DC6F"
        self.create_widgets()

    def create_widgets(self):
        global kafka_img
        top = Toplevel()
        top.title('Producer Run')
        top.iconbitmap(resource_path('assets\\kafka.ico'))
        top.geometry('500x400')
        top.grab_set()
        top.resizable(False, False)

        frameTop = Frame(top, width=500, height=500, bg=self.bg_colour_2)
        frameTop.grid(row=0, column=0)
        frameTop.pack_propagate(False)

        img = Image.open(resource_path("assets\\kafka_blue.jpeg"))
        img = img.resize((img.size[0]//4, img.size[1]//4), Image.LANCZOS)
        kafka_img = ImageTk.PhotoImage(img)
        logo_widget = Label(frameTop, image=kafka_img, borderwidth=0.5)
        logo_widget.pack(pady=10)

        Label(frameTop, text="Port number",
              bg=self.bg_colour_2, fg="#283938").pack()
        port = IntVar(value=9092)
        portEntry = Entry(frameTop, textvariable=port)
        portEntry.pack(padx=60)

        Label(frameTop, text="Topic name", bg=self.bg_colour_2, fg="#283938").pack()
        topicName = StringVar(value='topic-name')
        topicNameEntry = Entry(frameTop, textvariable=topicName)
        topicNameEntry.pack(padx=60)

        connection = sqlite3.connect(resource_path("data\\kafka.db"))
        cursor = connection.cursor()
        KAFKA_HOME = cursor.execute(
            "SELECT VALUE FROM KAFKA WHERE KEY='KAFKA_HOME'").fetchone()[0]
        connection.close()

        Label(frameTop,
              text="Eg:- "+KAFKA_HOME +
              "\\bin\windows\kafka-console-producer.bat --broker-list  localhost:9092 --topic topic-name",
              bg=self.bg_colour_2, fg="#012970", wraplength=400).pack()

        Button(
            frameTop,
            width=15,
            text="producer run",
            font=("TkHeadingfont", 12),
            bg="#283938",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: self.producer_create(port.get(), topicName.get())
        ).pack(pady=10, padx=50)

        Button(
            frameTop,
            width=15,
            text="Back",
            font=("TkHeadingfont", 12),
            bg="#283945",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=top.destroy).pack()

    def producer_create(self, port=9092, topic_name=''):
        connection = sqlite3.connect(resource_path("data\\kafka.db"))
        
        cursor = connection.cursor()
        
        PRODUCER_PRE = cursor.execute(
            "SELECT VALUE FROM KAFKA WHERE KEY='KAFKA_PRODUCER_PRE'").fetchone()[0]
        
        PRODUCER_RUN = PRODUCER_PRE+"localhost:" + \
            str(port)+" --topic "+str(topic_name)
        
        os.system('start cmd /k '+PRODUCER_RUN)

        connection.close()
