#!/usr/bin/env python2
import socket
import my_rsa
import my_sign
import json
import base64
import time

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

class DecodeError(Exception):
    pass
class SignatureError(Exception):
    pass

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
        self.output = TextInput(readonly=True, background_color=[0, 0, 0, 0],
                foreground_color=[1, 1, 1, 1])
        self.add_widget(self.output)
        self.add_widget(Label(text='message'))
        self.message = TextInput(multiline=False)
        self.add_widget(self.message)
        self.add_widget(Button(text="guard on",
            on_press = self.send_button_test))
        self.add_widget(Button(text="guard off",
            on_press = self.send_button_test))
        self.add_widget(Label(text='call help'))
        self.add_widget(Button(text="SOS",
            on_press = self.send_button_test))
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
            return (contents['ip'].encode(),
                    contents['keys_path'].encode(),
                    contents['own_keys_path'].encode(),
                    contents['phone_number'].encode())

    def receive(self, server):
        chunks = []
        bytes_recv = 0
        while bytes_recv < 4096:
            chunk = server.recv(2048)
            if (chunk == 0):
                # raise RuntimeError("socket connection broken")
                print("socket connection broken")
            chunks.append(chunk)
            bytes_recv += len(chunk)
            if (len(chunk) == 0 or chunk[-1] == '\x00'):
                break
        ret = b""
        for chunk in chunks:
            ret += chunk
        return ret[:-1]

    def decode_message(self, data_id_json, own_keys_path):
        try:
            data_id = json.loads(data_id_json)
            exp_time = int(data_id['exp_time'])
        except Exception as e:
            print("[ERROR] exception: ", (e.message))
            print("[ERROR] wrong data_id format from")
            raise DecodeError
        if (int(time.time()) > exp_time):
            print("[ERROR] expired message from")
            raise DecodeError
        b64_data = bytes(base64.b64decode(data_id['data']))
        data = my_rsa.unpack(b64_data)
        return my_rsa.decode(data, own_keys_path)

    def verify_sign(self, received_data, keys_path):
        try:
            json_msg = json.loads(received_data)
            signature = json_msg['sign'].encode()
            data_id_json = json_msg['data_id'].encode()
        except Exception as e:
            print("received_data: ", received_data)
            print("exception: ", (e.message))
            print("[ERROR] wrong message format! from")
            raise SignatureError
        if not (my_sign.verify_sign(signature, data_id_json,
        keys_path)):
            print("[ERROR] wrong signature from")
            raise SignatureError
        return data_id_json

    def get_response(self, s, keys_path, own_keys_path):
        resp = self.receive(s)
        try:
            data_id_json = self.verify_sign(resp, keys_path)
        except SignatureError:
            return "INTERNAL SIGNATURE ERROR"
        try:
            decoded_data = self.decode_message(data_id_json, own_keys_path)
        except DecodeError:
            return "INTERNAL DECODE ERROR"
        return decoded_data
    
    def send_button_test(self, obj):
        self.message.text = obj.text
        self.send_data(obj)

    def send_data(self, obj):
        print(obj)
        (ipaddr, keys_path, own_keys_path, phone_number) = self.load_strings()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ipaddr, 50012))
        except socket.error as s_err:
            if s_err.errno != 111:
                raise s_err
            tryes = 5
            print "Connection refused, retrying.."
            for i in range(0, tryes + 1):
                print "Try number ", str(i)
                try:
                    s.connect((ipaddr, 50012))
                except socket.error as try_err:
                    if try_err.errno != 111:
                        raise try_err
                time.sleep(1)
            print "Connection error"
            self.output.text = "Connection error"
            return
        encoded_int = (my_rsa.encode(self.message.text, keys_path));
        encoded_bytes = base64.b64encode(my_rsa.pack(encoded_int))
        json_data_id = json.dumps({
            "data": encoded_bytes,
            "id" : phone_number,
            "type" : "phone_number",
            "exp_time" : int(time.time()) + 10
            })
        sign = my_sign.sign_data(json_data_id, own_keys_path)
        json_send = json.dumps({
            "sign" : sign,
            "data_id" : json_data_id,
            })
        send_data1 = json_send 
        send_data1 += (b'\x00')
        s.sendall(send_data1)
        self.output.text = self.get_response(s, keys_path, own_keys_path)
        s.close()

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
        self.keys_path = TextInput(text="../../numbers.txt", readonly=True)
        # self.keys_path.bind(on_press=self.show_load)
        self.keys_path.bind(focus=self.input_focus)
        self.add_widget(self.keys_path)
        self.add_widget(Label(text="own keys file"))
        self.own_keys_path = TextInput(text="../../numbers.txt", readonly=True)
        # self.own_keys_path.bind(on_press=self.show_load)
        self.own_keys_path.bind(focus=self.input_focus)
        self.add_widget(self.own_keys_path)
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
                "own_keys_path" : self.own_keys_path.text,
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
            self.own_keys_path.text = contents['own_keys_path'].encode()
            self.phone_number.text = contents['phone_number'].encode()

    def input_focus(self, instance, value):
        if value:
            print "focused"
            print instance
            self.show_load(instance)
        else:
            print "unfocused"
            print instance


    def show_load(self, obj):
        if obj == self.keys_path:
            content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        elif obj == self.own_keys_path:
            content = LoadDialog(load=self.load_own, cancel=self.dismiss_popup)
        self._popup = Popup(title="Choose file", content=content,
                size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self, path):
        self.keys_path.text = path
        self.dismiss_popup()

    def load_own(self, path):
        self.own_keys_path.text = path
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
        return sm


if __name__ == '__main__':
    MyApp().run()
