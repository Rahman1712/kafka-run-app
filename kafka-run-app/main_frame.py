# from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import os

from topic_frame import TopicFrame
from producer_frame import ProducerFrame
from consumer_frame import ConsumerFrame
from settings_frame import SettingsFrame
from db_utils import resource_path

bg_colour = "#00B6D8"


class MainFrame(tk.Frame):
    def __init__(self, parent):
        self.bg_colour = bg_colour

        super().__init__(parent, width=500, height=600, bg=self.bg_colour)

        self.parent = parent

        self.pack_propagate(False)
        self.create_widgets()

    def create_widgets(self):
        connection = sqlite3.connect(resource_path("data\\kafka.db"))
        cursor = connection.cursor()
        ZOOKEEPER = cursor.execute(
            "SELECT VALUE FROM KAFKA WHERE KEY='ZOOKEEPER'").fetchone()[0]
        KAFKA_SERVER = cursor.execute(
            "SELECT VALUE FROM KAFKA WHERE KEY='KAFKA_SERVER'").fetchone()[0]
        connection.close()

        global logo_img
        global zookeeper_label
        global kafka_server_label

        self.pack_propagate(False)
        img = Image.open(resource_path("assets\\kafka_blue.jpeg"))
        img = img.resize((img.size[0]//2, img.size[1]//2), Image.LANCZOS)
        logo_img = ImageTk.PhotoImage(img)
        logo_widget = tk.Label(self, image=logo_img, borderwidth=0.5)
        logo_widget.pack(pady=10)

        tk.Label(
            self,
            text="Kafka Operations",
            bg=self.bg_colour,
            fg="white",
            font="Verdana 15 underline",
        ).pack()

        tk.Button(
            self,
            width=15,
            text="start zookeeper",
            font=("TkHeadingfont", 12),
            bg="#283938",
            fg="red",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda:self.run_server('ZOOKEEPER')
        ).pack(pady=(5, 0), padx=50)
        zookeeper_label = tk.Label(
            self,
            text=ZOOKEEPER,
            bg=self.bg_colour,
            fg="#001B4A",
            wraplength=450,
            font=("TkMenuFont", 8)
        )
        zookeeper_label.pack()

        tk.Button(
            self,
            width=15,
            text="start kafka server",
            font=("TkHeadingfont", 12),
            bg="#283938",
            fg="red",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda:self.run_server('KAFKA_SERVER')
        ).pack(pady=(10, 0), padx=50)
        kafka_server_label = tk.Label(
            self,
            text=KAFKA_SERVER,
            bg=self.bg_colour,
            fg="#001B4A",
            wraplength=450,
            font=("TkMenuFont", 8)
        )
        kafka_server_label.pack()

        tk.Button(
            self,
            width=15,
            text="topic create",
            font=("TkHeadingfont", 12),
            bg="#283938",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda:self.topic_creation()
        ).pack(pady=(10, 5), padx=50)

        tk.Button(
            self,
            width=15,
            text="start producer",
            font=("TkHeadingfont", 12),
            bg="#283938",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: self.run_producer()
        ).pack(pady=5, padx=50)

        tk.Button(
            self,
            width=15,
            text="start consumer",
            font=("TkHeadingfont", 12),
            bg="#283938",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: self.run_consumer()
        ).pack(pady=5, padx=50)

        tk.Button(
            self,
            width=15,
            text="settings",
            font=("TkHeadingfont", 12),
            bg="#283938",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: self.settings()
        ).pack(pady=5, padx=50)

    #=======ZOOKEEPER, KAFKA SEVER===============
    def run_server(self,key):
        connection = sqlite3.connect(resource_path("data\\kafka.db"))
        cursor = connection.cursor()
        keyVal = cursor.execute("SELECT VALUE FROM KAFKA WHERE KEY=:k", {"k": key}).fetchone()

        os.system('start cmd /k '+keyVal[0])

        connection.close()

    def topic_creation(self):
        TopicFrame(self)
    
    def run_producer(self):
        ProducerFrame(self)
    
    def run_consumer(self):
        ConsumerFrame(self)

    def settings(self):
        SettingsFrame(self)

    def changeLabelTexts(self, zookeeper_text, kafka_server_text):
        zookeeper_label.config(text=zookeeper_text)
        kafka_server_label.config(text=kafka_server_text)
