from tkinter import Toplevel, Frame, Label, Entry, Button, StringVar, IntVar
from PIL import Image, ImageTk
import sqlite3
import os
from db_utils import resource_path


class TopicFrame:
    def __init__(self, parent):
        self.parent = parent
        self.bg_colour_2 = "#03C7C7" #"#F7DC6F"
        self.create_widgets()

    def create_widgets(self):
        top = Toplevel(self.parent)
        top.title('Create Topic')
        top.iconbitmap(resource_path('assets\\kafka.ico'))
        top.resizable(False, False)
        top.geometry('500x400')
        top.grab_set()

        frameTop = Frame(top, width=500, height=500, bg=self.bg_colour_2)
        frameTop.grid(row=0, column=0)
        frameTop.pack_propagate(False)

        global kafka_img
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

        Label(frameTop, text="Topic name",
              bg=self.bg_colour_2, fg="#283938").pack()
        topicName = StringVar(value='topic-name')
        topicNameEntry = Entry(frameTop, textvariable=topicName)
        topicNameEntry.pack(padx=60)

        Label(frameTop, text="Partition Count",
              bg=self.bg_colour_2, fg="#283938").pack()
        partition = IntVar(value=3)
        partitionEntry = Entry(frameTop, textvariable=partition)
        partitionEntry.pack(padx=60)

        Label(frameTop, text="Replication count",
              bg=self.bg_colour_2, fg="#283938").pack()
        replication = IntVar(value=1)
        replicationEntry = Entry(frameTop, textvariable=replication)
        replicationEntry.pack(padx=60)

        connection = sqlite3.connect(resource_path("data\\kafka.db"))
        cursor = connection.cursor()
        KAFKA_HOME = cursor.execute(
            "SELECT VALUE FROM KAFKA WHERE KEY='KAFKA_HOME'").fetchone()[0]
        connection.close()

        Label(frameTop,
              text="Eg:- "+KAFKA_HOME+"\\bin\windows\kafka-topics.bat --bootstrap-server localhost:9092 --create --topic topic-name --partitions 3 --replication-factor 1",
              bg=self.bg_colour_2, fg="#012970", wraplength=400).pack()

        Button(
            frameTop,
            width=15,
            text="create",
            font=("TkHeadingfont", 12),
            bg="#283938",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: self.topic_create(
                port.get(), topicName.get(), partition.get(), replication.get())
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

    def topic_create(self, port=9092, topic_name="topic-1", partition_count=1, replication_factor_count=1):
        connection = sqlite3.connect(resource_path("data\\kafka.db"))
        cursor = connection.cursor()
        topicCmdPre = cursor.execute(
            "SELECT VALUE FROM KAFKA WHERE KEY='TOPIC_CREATE_PRE'").fetchone()[0]
        topicCmd = topicCmdPre+"localhost:"+str(port)+" --create --topic "+str(topic_name)+" --partitions "+str(
            partition_count)+" --replication-factor "+str(replication_factor_count)
        os.system('start cmd /k '+topicCmd)

        connection.close()
