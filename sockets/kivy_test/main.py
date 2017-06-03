#!/usr/bin/env python2
import socket
import my_rsa

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

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
        self.keys_path = TextInput(multiline=False)
        self.add_widget(self.keys_path)
        self.send = Button(text="send")
        self.send.bind(on_press=self.send_data)
        self.add_widget(self.send)

    def send_data(self, obj):
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

class MyApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
