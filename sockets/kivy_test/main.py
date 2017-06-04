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
        self.add_widget(Label(text='message'))
        self.message = TextInput(multiline=False)
        self.add_widget(self.message)
        self.add_widget(Label(text='server ip'))
        self.ipaddr = TextInput(multiline=False)
        self.add_widget(self.ipaddr)
        self.add_widget(Label(text='path to keys'))
        self.keys_path = Button(text="../../numbers.txt",
                on_press=self.show_load)
        self.add_widget(self.keys_path)
        self.send = Button(text="send")
        self.send.bind(on_press=self.send_data)
        self.add_widget(self.send)
        self.add_widget(Label(text="Output"))
        self.output = Label(text="")
        self.add_widget(self.output)
        self.load_strings()

    def show_load(self, obj):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Choose file", content=content,
                size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self, path):
        # self.key_path.text = os.path.join(path, filename[0])
        self.keys_path.text = path
        self.dismiss_popup()

    def save_strings(self, homedir):
        if not os.path.isdir(os.path.join(homedir, ".diplom")):
            try:
                os.mkdir(os.path.join(homedir, ".diplom"))
            except:
                print ("error creating folder" +
                        os.path.join(homedir, ".diplom"))
                pass
        with open(os.path.join(homedir, ".diplom", "fields.json"), "w+") as f:
            f.write(json.dumps({
                "ip" : self.ipaddr.text,
                "keys_path" : self.keys_path.text
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

    def send_data(self, obj):
        try:
            self.output.text = (os.environ['HOME'])
            homedir = self.output.text
        except:
            self.output.text = "Android detected"
            homedir = "/storage/sdcard0/"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ipaddr.text, 50012))
        encoded_int = (my_rsa.encode(self.message.text,
            self.keys_path.text));
        encoded_bytes = my_rsa.pack(encoded_int)
        send_data1 = encoded_bytes 
        send_data1 += (b'\x00')
        # print(send_data)
        s.sendall(send_data1)
        # data = s.recv(1024)
        s.close()
        # print ('Received ', (data.decode())) 
        self.save_strings(homedir)

class MyApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
