from bs4 import BeautifulSoup
import requests,webbrowser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from tkinter import *
from tkinter import messagebox
import json
import re

def buka_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup
def skip_link(url):
    driver = webdriver.Chrome()
    driver.get(url)
    tombol = driver.find_element_by_class_name('sorasubmit')
    tombol.submit()
    driver.execute_script("changeLink();");
def ambilLink(s):
    soup = buka_link(s)
    temp = soup.findAll('a')
    linkBagiLagi = []
    for a in temp:
        if ('http://bagilagi.com/?id=U3Z' in a.get('href')) :
            linkBagiLagi.append((a.get_text(),a.get('href')))
    return linkBagiLagi

def loadLink(link_):
    soup = buka_link('https://drivenime.com/daftar-anime/')
    temp = soup.findAll('a')
    link = {}
    now = 'misc'
    linknama_temp = []
    num = 0
    for a in temp:
        if(now=='misc'):
            if(a.get('href')=='#azindex-1'):
                now = a.get_text()
        else:
            if((a.get('href')=='#azindex-1')):
                link.update({now : linknama_temp})
                saveLink(link)
                now = a.get_text()
                linknama_temp = []
                num = 0
            else:
                namaAnime = a.get_text()
                #Cari apakah anime sudah di load sebelumnya
                ketemu = False
                try:
                    for i in link_[namaAnime[0].upper()]:
                        if(namaAnime in i[2]):
                            linknama_temp.append(i)
                            ketemu = True
                            break
                except:
                    ketemu = False
                if(ketemu != True):
                    linknama_temp.append((num,a.get('href'),namaAnime,ambilLink(a.get('href'))))
                    print('Done load baru',namaAnime)
                else:
                    print('    Skip',namaAnime)
                if(namaAnime == 'Action'):
                    break
                num += 1
    return link

def saveLink(link):
    with open('data.json', 'w') as outfile:
        json.dump(link, outfile)

def reload(link_):
    link = loadLink(link_)
    saveLink(link)
    tmp = 0
    for lin in link:
        for li in link[lin]:
            list1.insert(tmp,li[2])
            tmp += 1
    messagebox.showinfo("Reload", "Reload selesai")
    return link

def openLink(link):
    tmp = 0
    for lin in link:
        for li in link[lin]:
            list1.insert(tmp,li[2])
            tmp += 1
    return link

def onselect(event,pilihan,listEps,idxEps,download):
    wid = event.widget
    nama = str(wid)
    #print(nama)
    liCur = wid.curselection()
    if(liCur):
        if('list1' in nama):
            index = int(liCur[0])
            value = wid.get(index)
            pilihan.clear()
            pilihan.append(value)
            #print( 'You selected item %d: "%s"' % (index, value))
            lin = link[value[0].upper()]
            for li in lin:
                if(li[2]==value):
                    list2.delete(0,END)
                    listEps.clear()
                    idxEps.clear()
                    tmp = 1
                    for i in li[3]:
                        list2.insert(tmp,i[0])
                        listEps.append((i[0],i[1]))
                        #print(listEps)
                        tmp += 1
        elif('list2' in nama):
            index = int(liCur[0])
            value = wid.get(index)
            #print(index)
            idxEps.clear()
            idxEps.append(index)
            idxHapus.clear()
        elif('list3' in nama):
            index = int(liCur[0])
            idxHapus.clear()
            idxHapus.append(index)

def tambah(listEps,idxEps,download):
    if(idxEps):
        eps = listEps[idxEps[0]]
        list3.insert(END,eps[0])
        download.append(eps)
    else:
        messagebox.showwarning('Error','Pilih episode terlebih dahulu')

def hapus(idxHapus):
    if(idxHapus):
        list3.delete(idxHapus[0])
        download.pop(idxHapus[0])
    else:
        messagebox.showwarning('Error','Pilih item yang mau dihapus terlebih dahulu')
def gas(download):
    for i in download:
        skip_link(i[1])

#Variable Global
pilihan,listEps,idxEps= [],[],[]
download = []
idxHapus = []


if __name__ == "__main__":
    #Kode Utama
    root = Tk()
    root.title('Anime Downloader')
    frame2 = Frame(root)
    frame2.pack(side = TOP)
    frame1 = Frame(root)
    frame1.pack(side = LEFT)
    frame3 = Frame(root)
    frame3.pack(side = LEFT)
    frame4 = Frame(root)
    frame4.pack(side = LEFT)

    with open('data.json') as data_file:
        link = json.load(data_file)

    #Label
    label1 = Label(frame1, text = 'List Anime')
    label1.pack(side = TOP)

    label2 = Label(frame3, text = 'List Episode')
    label2.pack(side = TOP)

    label3 = Label(frame4, text = 'List Download')
    label3.pack(side = TOP)
    #Scrollbar
    scrollbar = Scrollbar(frame1)
    scrollbar.pack( side = RIGHT, fill = Y )
    list1 = Listbox(frame1,name = 'list1',width=70, height = 20,yscrollcommand = scrollbar.set, relief = FLAT)
    list1.bind('<<ListboxSelect>>',lambda event : onselect(event,pilihan,listEps,idxEps,download))
    list1.pack(side = TOP)
    scrollbar.config( command = list1.yview )

    scrollbar2 = Scrollbar(frame3)
    scrollbar2.pack(side = RIGHT,fill = Y)
    list2 = Listbox(frame3,name = 'list2',width = 70,height = 20,yscrollcommand = scrollbar2.set,relief=FLAT)
    list2.pack(side = TOP)
    scrollbar2.config( command = list2.yview )
    list2.bind('<<ListboxSelect>>',lambda event : onselect(event,pilihan,listEps,idxEps,idxHapus))

    scrollbar3 = Scrollbar(frame4)
    scrollbar3.pack(side = RIGHT,fill= Y)
    list3 = Listbox(frame4,name = 'list3',width = 70, height = 20,yscrollcommand = scrollbar3.set,relief=FLAT)
    list3.pack(side = TOP)
    scrollbar3.config(command = list3.yview)
    list3.bind('<<ListboxSelect>>',lambda event : onselect(event,pilihan,listEps,idxEps,idxHapus))

    #Button
    but1 = Button(frame2,text = 'Load Database',command = lambda : openLink(link))
    but1.pack(side = LEFT)
    but2 = Button(frame2,text = 'Reload dari server',command =  lambda : reload(link))
    but2.pack(side = LEFT)
    but3 = Button(frame2,text = 'Tambah ke list Download', command = lambda : tambah(listEps,idxEps,download))
    but3.pack(side = LEFT)
    but4 = Button(frame2,text = 'Hapus dari list',command = lambda : hapus(idxHapus))
    but4.pack(side = LEFT)
    but5 = Button(frame2, text = 'Download',command = lambda : gas(download))#lol
    but5.pack(side = RIGHT)
    root.mainloop()
