import os
import socket
import threading
import time
import tkinter as tk
import tkinter.messagebox
from io import BytesIO

import customtkinter
import pafy
import pyperclip
import vlc
from PIL import ImageTk, Image
from pyngrok import ngrok
from pytube import Playlist
from pytube import YouTube
from requests import get

# test

global Video_info
Video_info = ["None", "False", "Video_time_sek"]
global sock
global Hoster
global vra
Hoster = 0


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("sallify.json")
print(os.path.dirname(os.path.abspath(__file__)))

global False_Call
def play_song(url, volume):
    global Video_info
    Video_info[0] = url
    global player
    global video
    video = pafy.new(url)
    best = video.getbestaudio()
    play_url = best.url
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(play_url)
    media.get_mrl()
    player.set_media(media)
    player.play()
    player.audio_set_volume(int(volume))



def start_server():
    global sock
    ngrok.set_auth_token("2AYWrd8D7u9WAhpit1cRzCclzt4_47YboKYHbaAFqx2VvbQbU")
    host = socket.gethostname()
    port = 1509

    # Create a TCP socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind a local socket to the port
    server_address = ("", port)
    sock.bind(server_address)
    sock.listen(1)

    # Open a ngrok tunnel to the socket
    public_url = ngrok.connect(port, "tcp", options={"remote_addr": "{}:{}".format(host, port)})
    print("ngrok tunnel \"{}\" -> \"tcp://127.0.0.1:{}/\"".format(public_url, port))
    global code
    code = str(public_url)[20] + str(public_url)[34:40]

    global Video_info

    while True:
        connection = None
        try:
            # Wait for a connection
            print("\nWaiting for a connection ...")
            connection, client_address = sock.accept()

            print("... connection established from {}".format(client_address))

            # Receive the message, send a response
            while True:
                data = connection.recv(1024)
                if data:
                    Request = data.decode("utf-8")
                    print("Sending: {}".format(str(Video_info)))
                    connection.sendall(str(Video_info).encode("utf-8"))
                else:
                    break
        except KeyboardInterrupt:
            print(" Shutting down server.")

            if connection:
                connection.close()
            break

    sock.close()

"""with open('Playlists.txt', 'rb') as f:
    Songs = load(f)"""
Songs_Full = []
Songs = []
url = "https://youtu.be/1VD17MgCMhM"
video = YouTube(url)
Songs_Half = video.description
for i in Songs_Half.split(","):
    Songs.append(i.split("¦"))

root = customtkinter.CTk()
root.title('Sallify')
root.geometry("1000x500+50+50")
root.iconbitmap("Assets/Sqaure.ico")
Icon = ImageTk.PhotoImage(Image.open("Assets/Green.png"))
panel = tk.Label(root, image=Icon, bg="black")
Ican = ImageTk.PhotoImage(Image.open("Assets/Reload_white.png"))
img = []




def load_songs():
    try:
        for i in Songs:
            p = Playlist(i[1])
            y = YouTube(p.video_urls[0])
            url = y.thumbnail_url
            response = get(url)
            img_data = response.content
            img.append(ImageTk.PhotoImage(Image.open(BytesIO(img_data))))
    except:
        tkinter.messagebox.showerror(root, title="Conection error",message="Please make wifi good and restart")

load_s = threading.Thread(target=load_songs)
load_s.start()

def showimg(e):
    a = lst.curselection()
    fname = lst.get(a)
    for i in range(len(Songs)):
        if Songs[i][0] == fname:
            try:
                panel.configure(image=img[i])
                panel.pack(side="bottom", fill="both", expand="yes")
                panel.update()
            except:
                panel.configure(image=Ican)
                panel.pack(side="bottom", fill="both", expand="yes")
                panel.update()

def Start_playlist():
    subroot =  customtkinter.CTk()
    subroot.geometry("490x340")
    subroot.grid_columnconfigure(0, weight=1)
    subroot.grid_rowconfigure(0, weight=1)
    playlist = tk.Listbox(subroot, selectmode=tk.SINGLE, bg="black", fg="white", width=40)
    playlist.config(font=('Roboto', 15))
    playlist.grid(columnspan=10, sticky="news")
    Z = lst.curselection()
    Aname = lst.get(Z)
    def threaded_Loading():
        for e in range(len(Songs)):
            if Songs[e][0] == Aname:
                p = Playlist(Songs[e][1])
                print(p.title)
                for Url in p.video_urls:
                    Name = YouTube(Url).title
                    playlist.insert(tk.END, Name+" "*1000+","+Url)

    a = threading.Thread(target=threaded_Loading)
    a.start()

    def test(e):
        print("select")
    playlist.bind("<<ListboxSelect>>", test)

    def Load_Song(Link):
        global Video_info
        Video_info[0] = Link
        try:
            player.stop()
        except:
            pass
        play_song(Link, Volumeslider.get())
        Timeslider.config(from_=0, to=video.length)
        Timeslider.set(0)
        z = threading.Thread(target=Has_ended)
        z.start()

    def Has_ended():
        global Video_info
        global False_Call
        while True:
            False_Call = True
            global Video_info
            Timeslider.set(video.length*(player.get_position()))
            Video_info[2] = round(video.length*(player.get_position()))
            time.sleep(5)
            try:
                if str(player.get_state()) == "State.Ended":
                    Next_int = -1
                    print(player.get_state())
                    while True:
                        Next_int += 1
                        if video.title in str(playlist.get(Next_int)):
                            try:
                                print((playlist.get(Next_int+1)).split(",")[0])
                                Load_Song((playlist.get(Next_int+1)).split(",")[1])
                                break
                            except:
                                Load_Song((playlist.get(0)).split(",")[1])
                                break
                                print("First song")
                    break
                else:

                    print(str(player.get_state()))
            except NameError as e:
                print(e)

    def playSong():
        try:
            player.stop()
        except:
            pass
        Puase_Resumebtn.config(text="  ⏸ ")
        pay = playlist.curselection()
        gayname = playlist.get(pay)
        play_song(gayname.split(",")[1], Volumeslider.get())
        Timeslider.config(from_=0, to=video.length)
        Timeslider.set(0)
        z = threading.Thread(target=Has_ended)
        z.start()
        Volumeslider.set(player.audio_get_volume())

    def Puase_ResumeSong():
        print(player.is_playing())
        if player.is_playing() == 1:
            player.pause()
            Video_info[1] = "True"
            Puase_Resumebtn.config(text="  ▶ ")
        elif player.is_playing() == 0:
            Video_info[1] = "False"
            Puase_Resumebtn.config(text="  ⏸ ")
            player.pause()

    def Change_volume(e):
        try:
            text = ("Volume : "+str(round(e)))
            player.audio_set_volume(int(e)*5)
            VolumeEntry.delete(0,tk.END)
            VolumeEntry.insert(0,text)
        except:
            pass

    def Change_Loacation(e):
        global False_Call
        try:
            if False_Call:
                Video_info[2] = e
                False_Call = False
            elif not False_Call:
                Video_info[2] = e
                player.set_time(int(e)*1000)
                False_Call = False
        except:
            pass

    def Enterred(e):
        try:
            Text = int(VolumeEntry.get())
            if Text > 0 and Text < 200:
                Volumeslider.set(Text)
        except:
            text = ("Volume : " + str(round(player.audio_get_volume()/5)))
            VolumeEntry.delete(0, tk.END)
            VolumeEntry.insert(0, text)

    def CLicked(e):
        VolumeEntry.configure(state=tk.NORMAL)
        VolumeEntry.delete(0, tk.END)

    subroot.title('Sallify')
    subroot.iconbitmap("Assets/Sqaure.ico")
    songstatus = tk.StringVar()
    songstatus.set("choosing")
    # playlist---------------

    playbtn = customtkinter.CTkButton(subroot, text="play", command=playSong, text_font=('Roboto', 20))
    # playbtn.config(font=('arial', 20), bg="black", fg="white", padx=70, pady=6)
    playbtn.grid(row=1, rowspan=2, column=0, sticky="news")
    Puase_Resumebtn = customtkinter.CTkButton(subroot, text="  ⏸ ", command=Puase_ResumeSong)
    # Puase_Resumebtn.config(font=('arial', 20), bg="black", fg="white", padx=7, pady=6)
    Puase_Resumebtn.grid(row=1, rowspan=2, column=1, sticky="NSEW")
    # Canvy = customtkinter.CTkFrame(subroot)
    # Canvy.grid(row=1, column=2, sticky="ew", )
    VolumeEntry = customtkinter.CTkEntry(subroot,placeholder_text="Volume")
    VolumeEntry.config()
    # Volumeslider.config(font=('arial', 20), bg="black", fg="white",length=150)
    VolumeEntry.grid(row=1, column=2)
    Volumeslider = customtkinter.CTkSlider(subroot, from_=1,to=100, orient='horizontal',command=Change_volume)
    Volumeslider.set(20)
    # Volumeslider.config(font=('arial', 20), bg="black", fg="white",length=150)
    Volumeslider.grid(row=2, column=2)
    Timeslider = customtkinter.CTkSlider(subroot, from_=0,to=100, orient='horizontal',command=Change_Loacation)
    # Timeslider.config(font=('arial', 20), bg="gray", fg="white",length=450)
    Timeslider.grid(row=3, column=0,columnspan=4, sticky="NSEW")
    VolumeEntry.bind('<Button-1>', CLicked)
    VolumeEntry.bind('<Return>', Enterred)
    subroot.mainloop()

def start_threaded_playlist():
    # x =threading.Thread(target=Start_playlist)
    # x.start()
    Start_playlist()
def client_listen_along(Code):
    while True:
        time.sleep(1)
        Full_info = Code.split(":")
        host = f"{Full_info[0]}.tcp.ngrok.io"
        port = str(Full_info[1])

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = (host, port)
        sock.connect(server_address)
        print("Connected to {}:{}".format(host, port))

        message = "Video"
        print("Sending: {}".format(message))
        sock.sendall(message.encode("utf-8"))

        data_received = 0
        data_expected = len(message)

        while data_received < data_expected:
            data = sock.recv(1024)
            data_received += len(data)
            print(data.decode("utf-8"))
            sock.close()
        sock.close()
def Client_setup():
    Host_b.pack_forget()
    Join_b.pack_forget()
    Ask_code.pack(side="right", fill=tk.X)
    start.pack(side="right", fill=tk.X)
    Filan_audio_bar.pack(side="right", fill=tk.X)
def start_threaded_listen_along():
    if stream_Buton.get():
        tkinter.messagebox.showinfo(message="Please full screen window to see full gui")
        Host_b.pack(side="right", fill=tk.X)
        Join_b.pack(side="right", fill=tk.X)
    else:
        vra = False
        Filan_audio_bar.pack_forget()
        Host_b.pack_forget()
        Join_b.pack_forget()
        stop.pack_forget()
        Ask_code.pack_forget()
        copyCode.pack_forget()
        start.pack_forget()
        ngrok.kill()
def start_server_setup():
    server = threading.Thread(target=start_server)
    server.start()
    Host_b.pack_forget()
    Join_b.pack_forget()
    stop.pack(side="right", fill=tk.X)
    copyCode.pack(side="right", fill=tk.X)
def stop_server():
    ngrok.kill()
    global vra
    vra = False
    stream_Buton.toggle()

global old_hoho
old_hoho = Video_info
old_hoho[1] == "False"
global vra
vra = False
def vra_serber_vir_informasie():
    global old_hoho
    while vra:
        print(vra)
        time.sleep(1)
        gagagagaag = Ask_code.get().split(":")
        host = f"{gagagagaag[0]}.tcp.ngrok.io"
        port = int(gagagagaag[1])
        pock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host, port)
        pock.connect(server_address)
        message = "Video"
        pock.sendall(message.encode("utf-8"))
        data_received = 0
        data_expected = len(message)
        while data_received < data_expected:
            data = pock.recv(1024)
            data_received += len(data)
            time.sleep(2)
            hohoho = data.decode("utf-8")
            hohoho = hohoho.replace(" ", "").replace("'", "").replace("[", "").replace("]", "")
            hohoho = hohoho.split(",")
            if hohoho != old_hoho:
                if hohoho[0] != old_hoho[0]:
                    try:
                        player.stop()
                    except:
                        pass
                    play_song(hohoho[0], Filan_audio_bar.get())
                    old_hoho = hohoho
                if hohoho[1] != old_hoho[1]:
                    print(str(hohoho) + " Recieved")
                    print(str(old_hoho) + " had")
                    old_hoho = hohoho
                    if hohoho[1] == "True":
                        print("pausing")
                        if player.is_playing() == 1:
                            player.pause()
                    elif hohoho[1] == "False":
                        if player.is_playing() == 0:
                            print("playing")
                            player.pause()
                if hohoho[2] != old_hoho[2]:
                    if int(hohoho[2]) - 5 > round(video.length*(player.get_position())):
                        try:
                            player.set_time(int(hohoho[2])*1000)
                        except:
                            pass
                    elif int(hohoho[2]) + 5 < round(video.length*(player.get_position())):
                        try:
                            player.set_time(int(hohoho[2]) * 1000)
                        except:
                            pass
                    old_hoho = hohoho
            pock.close()
        pock.close()

def join_server():
    global vra
    print("Joining")
    vra = True
    client = threading.Thread(target=vra_serber_vir_informasie)
    client.start()
def Copy_code():
    global code
    pyperclip.copy(code)
def Final_audio_slider(e):
    try:
        player.audio_set_volume(int(e))
    except:
        pass

def on_closing():
    print("closing")
    ngrok.kill()
    try:
        player.stop()
    except:
        pass
    root.destroy()
    quit()
    quit()

root.protocol("WM_DELETE_WINDOW", on_closing)

Filan_audio_bar = customtkinter.CTkSlider(from_=1,to=100, orient='horizontal', command=Final_audio_slider)
subbie = customtkinter.CTk()
copyCode = customtkinter.CTkButton(text="Copy code", command=Copy_code)
stop = customtkinter.CTkButton(text="Stop", command=stop_server)
start = customtkinter.CTkButton(text="Join", command=join_server)
Ask_code = customtkinter.CTkEntry(placeholder_text="Paste Code here")
Host_b = customtkinter.CTkButton(text="Host listen along", command=start_server_setup)
Join_b = customtkinter.CTkButton(text="Join listen along", command=Client_setup)
stream_Buton = customtkinter.CTkSwitch(text="Listen along",command=start_threaded_listen_along )
stream_Buton.pack(side="top",fill=tk.X)
b1 = customtkinter.CTkButton(text="Play",command=start_threaded_playlist)
b1.pack(side="bottom",fill=tk.X)
lst = tk.Listbox(root, bg="black", fg="white")
lst.pack(side="left",fill="both", ipadx=20)

for fname in Songs:
    lst.insert(tk.END, fname[0])
lst.config(font=('Roboto', 12))
lst.bind("<<ListboxSelect>>", showimg)
panel.pack(side="bottom", fill="both", expand="yes", ipadx=10)
# panel.pack(side="bottom", fill="both", expand="yes")
print("done")

root.mainloop()