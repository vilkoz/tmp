#!/usr/bin/env python2
import socket
import my_rsa
import json

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import ScreenManager, Screen

import os

class MyFileChooser(FileChooserListView):
    load = ObjectProperty(None)

    def on_submit(self, selected, touch):
        # print(args[1][0])
        self.load((selected[0].encode()))

class LoadDialog(BoxLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LoadDialog, self).__init__(**kwargs)
        self.fclv = MyFileChooser(filters=
                [lambda folder, filename: not filename.endswith('.sys')],
                load = self.load)
        self.add_widget(self.fclv)

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="Output"))
        self.output = Label(text="")
        self.add_widget(self.output)
        self.add_widget(Label(text='message'))
        self.message = TextInput(multiline=False)
        self.add_widget(self.message)
        self.send = Button(text="send")
        self.send.bind(on_press=self.send_data)
        self.add_widget(self.send)
        self.add_widget(Button(text="settings",
            on_press = self.open_settings))
        # self.load_strings()

    def open_settings(self, obj):
        sm.transition.direction = "left"
        sm.current = "settings"

    def load_strings(self):
        try:
            homedir = os.environ['HOME']
        except:
            homedir = "/storage/sdcard0/"
        if os.path.exists(os.path.join(homedir, ".diplom", "fields.json")):
            f = open(os.path.join(homedir, ".diplom", "fields.json"), "r")
            contents = json.loads(f.read())
            # self.ipaddr.text = contents['ip'].encode()
            # self.keys_path.text = contents['keys_path'].encode()
            return (contents['ip'].encode(), contents['keys_path'].encode(),
                    contents['phone_number'].encode())

    def send_data(self, obj):
        (ipaddr, keys_path, phone_number) = self.load_strings()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ipaddr, 50012))
        encoded_int = (my_rsa.encode(self.message.text, keys_path));
        encoded_bytes = my_rsa.pack(encoded_int)
        send_data1 = encoded_bytes 
        send_data1 += (b'\x00')
        # print(send_data)
        s.sendall(send_data1)
        # data = s.recv(1024)
        s.close()
        # print ('Received ', (data.decode())) 

class SettingsLayout(GridLayout):
    def __init__(self, **kwargs):
        super(SettingsLayout, self).__init__(**kwargs)
        self.cols = 2
        # self.add_widget(Label(text="Settings"))
        self.add_widget(Button(text="Save", on_press=self.save_strings))
        self.add_widget(Button(text="<< Back", on_press=self.back))
        self.add_widget(Label(text="server ip"))
        self.ipaddr = TextInput()
        self.add_widget(self.ipaddr)
        self.add_widget(Label(text="Phone number"))
        self.phone_number = TextInput()
        self.add_widget(self.phone_number)
        self.add_widget(Label(text="keys file"))
        self.keys_path = Button(text="../../numbers.txt",
                on_press=self.show_load)
        self.add_widget(self.keys_path)
        self.load_strings()

    def back(self, obj):
        sm.transition.direction = "right"
        sm.current = "main"

    def save_strings(self, obj):
        try:
            homedir = os.environ['HOME']
        except:
            homedir = "/storage/sdcard0/"
        if not os.path.isdir(os.path.join(homedir, ".diplom")):
            try:
                os.mkdir(os.path.join(homedir, ".diplom"))
            except:
                print ("error creating folder" +
                        os.path.join(homedir, ".diplom"))
        with open(os.path.join(homedir, ".diplom", "fields.json"), "w+") as f:
            f.write(json.dumps({
                "ip" : self.ipaddr.text,
                "keys_path" : self.keys_path.text,
                "phone_number" : self.phone_number.text
                }))

    def load_strings(self):
        try:
            homedir = os.environ['HOME']
        except:
            homedir = "/storage/sdcard0/"
        if os.path.exists(os.path.join(homedir, ".diplom", "fields.json")):
            f = open(os.path.join(homedir, ".diplom", "fields.json"), "r")
            contents = json.loads(f.read())
            self.ipaddr.text = contents['ip'].encode()
            self.keys_path.text = contents['keys_path'].encode()
            self.phone_number.text = contents['phone_number'].encode()

    def show_load(self, obj):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Choose file", content=content,
                size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self, path):
        self.keys_path.text = path
        self.dismiss_popup()



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        mainlayout = LoginScreen()
        self.add_widget(mainlayout)

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.add_widget(SettingsLayout())

sm = ScreenManager()
sm.add_widget(MainScreen(name="main"))
sm.add_widget(SettingsScreen(name="settings"))


class MyApp(App):

    def build(self):
        # return LoginScreen()
        return sm


if __name__ == '__main__':
    MyApp().run()
