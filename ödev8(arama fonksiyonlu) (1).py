import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from plyer import notification
import threading
import time

class HatirlatmaQueue:
    def __init__(self):
        self.elements = []

    def hatirlatma_ekle(self, hatirlatma):
        self.elements.append(hatirlatma)
        self.elements = sorted(self.elements, key=lambda x: x["tarih"])

    def hatirlatma_goruntule(self):
        for hatirlatma in self.elements:
            metin = hatirlatma["metin"]
            tarih = hatirlatma["tarih"]
            print(f"Hatırlatma: {metin}, Tarih: {tarih}")

    def hatirlatma_sil(self, index):
        if 0 <= index < len(self.elements):
            del self.elements[index]

    def hatirlatma_ara(self, anahtar_kelime):
        bulunan_hatirlatmalar = []
        for hatirlatma in self.elements:
            metin = hatirlatma["metin"]
            if anahtar_kelime.lower() in metin.lower():
                bulunan_hatirlatmalar.append(hatirlatma)
        return bulunan_hatirlatmalar

hatirlatma_kuyrugu = HatirlatmaQueue()

def hatirlatma_ekle():
    pencere = tk.Toplevel(ana_pencere, bg="#a0a0a0")
    pencere.title("Hatırlatma Ekle")

    metin_etiket = tk.Label(pencere, text="Hatırlatma Metni:")
    metin_etiket.pack(padx=10, pady=10)
    metin_giris = tk.Entry(pencere, width=100)
    metin_giris.pack(padx=10, pady=10)

    saat_etiket = tk.Label(pencere, text="Saat:")
    saat_etiket.pack(padx=10, pady=10)
    saat_giris = ttk.Combobox(pencere, values=list(range(24)), width=5)
    saat_giris.pack(padx=10, pady=10)

    dakika_etiket = tk.Label(pencere, text="Dakika:")
    dakika_etiket.pack(padx=10, pady=10)
    dakika_giris = ttk.Combobox(pencere, values=list(range(60)), width=5)
    dakika_giris.pack(padx=10, pady=10)

    gun_etiket = tk.Label(pencere, text="Gün:")
    gun_etiket.pack(padx=10, pady=10)
    gun_giris = ttk.Combobox(pencere, values=list(range(32)), width=5)
    gun_giris.pack(padx=10, pady=10)

    ay_etiket = tk.Label(pencere, text="Ay:")
    ay_etiket.pack(padx=10, pady=10)
    ay_giris = ttk.Combobox(pencere, values=list(range(13)), width=5)
    ay_giris.pack(padx=10, pady=10)

    yil_etiket = tk.Label(pencere, text="Yıl:")
    yil_etiket.pack(padx=10, pady=10)
    yil_giris = tk.Entry(pencere, width=10)
    yil_giris.pack(padx=10, pady=10)

    def hatirlatma_kaydet():
        metin = metin_giris.get()
        saat = int(saat_giris.get())
        dakika = int(dakika_giris.get())
        gun = int(gun_giris.get())
        ay = int(ay_giris.get())
        yil = int(yil_giris.get())

        if 0 <= saat < 24 and 0 <= dakika < 60 and 1 <= gun <= 31 and 1 <= ay <= 12:
            tarih = datetime(yil, ay, gun, saat, dakika)
            hatirlatma = {"metin": metin, "tarih": tarih}
            hatirlatma_kuyrugu.hatirlatma_ekle(hatirlatma)
            pencere.destroy()

            simdi = datetime.now()
            fark = tarih - simdi
            bekleme_suresi = fark.total_seconds()

            if bekleme_suresi > 0:
                def show_notification():
                    notification.notify(
                        title="Hatırlatma",
                        message=f"{metin} - Zamanı geldi.",
                        timeout=10
                    )
                    bildirim_pencere = tk.Toplevel(ana_pencere)
                    bildirim_pencere.title("Hatırlatma Bildirimi")
                    label = tk.Label(bildirim_pencere, text=f"{metin} - Zamanı geldi!")
                    bildirim_pencere.geometry("200x50+650+350")
                    label.pack(padx=10, pady=10)
                
                threading.Timer(bekleme_suresi, show_notification).start()

        else:
            messagebox.showerror("Hata", "Geçersiz tarih veya saat")

    kaydet_buton = tk.Button(pencere, text="Kaydet", command=hatirlatma_kaydet)
    kaydet_buton.pack(pady=10)

def hatirlatmaları_listele():
    hatirlatma_kuyrugu.hatirlatma_goruntule()
    liste_pencere = tk.Toplevel(ana_pencere, bg="#a0a0a0")
    liste_pencere.title("Hatırlatmalar")

    current_index = 1
    for hatirlatma in hatirlatma_kuyrugu.elements:
        metin = hatirlatma["metin"]
        tarih = hatirlatma["tarih"]
        hatirlatma_str = f"{current_index}. Hatırlatma: {metin}, Tarih: {tarih}"
        hatirlatma_etiket = tk.Label(liste_pencere, text=hatirlatma_str)
        hatirlatma_etiket.pack(padx=10, pady=10)
        current_index += 1

def hatirlatma_sil():
    sil_pencere = tk.Toplevel(ana_pencere, bg="#a0a0a0")
    sil_pencere.title("Hatırlatma Sil")

    sil_etiket = tk.Label(sil_pencere, text="Silinecek hatırlatmanın numarasını girin:")
    sil_etiket.pack(padx=10, pady=10)
    sil_giris = ttk.Combobox(sil_pencere, values=list(range(100)), width=5)
    sil_giris.pack(padx=10, pady=10)

    def sil():
        try:
            index = int(sil_giris.get()) - 1
            hatirlatma_kuyrugu.hatirlatma_sil(index)
            sil_pencere.destroy()
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz hatırlatma numarası")

    sil_buton = tk.Button(sil_pencere, text="Sil", command=sil)
    sil_buton.pack(padx=10, pady=10)

def arama_yap():
    anahtar_kelime = entry_arama.get()
    if anahtar_kelime:
        bulunan_hatirlatmalar = hatirlatma_kuyrugu.hatirlatma_ara(anahtar_kelime)
        
        if bulunan_hatirlatmalar:
            liste_pencere = tk.Toplevel(ana_pencere, bg="#a0a0a0")
            liste_pencere.title("Arama Sonuçları")

            current_index = 1
            for hatirlatma in bulunan_hatirlatmalar:
                metin = hatirlatma["metin"]
                tarih = hatirlatma["tarih"]
                hatirlatma_str = f"{current_index}. Hatırlatma: {metin}, Tarih: {tarih}"
                hatirlatma_etiket = tk.Label(liste_pencere, text=hatirlatma_str)
                hatirlatma_etiket.pack(padx=10, pady=10)
                current_index += 1
        else:
            messagebox.showinfo("Arama Sonuçları", "Eşleşen hatırlatma bulunamadı.")
    else:
        messagebox.showwarning("Arama Hatası", "Lütfen bir anahtar kelime girin.")

# Ana pencere oluştur
ana_pencere = tk.Tk()
ana_pencere.title("Hatırlatıcı Uygulaması")
icon_path = 'galatasaray.png'
icon = tk.PhotoImage(file=icon_path)
ana_pencere.iconphoto(True, icon)
ana_pencere.configure(bg="#313131")
ana_pencere.geometry("750x650+385+75")

entry_arama = tk.Entry(ana_pencere, font=("Arial", 12), fg='white', bg='#11119c', width=30)
entry_arama.pack(pady=10)
button_arama = tk.Button(ana_pencere, text="Ara", font=("Arial", 12), fg='white', bg='#11119c', command=arama_yap)
button_arama.pack(pady=10)

ekle_buton = tk.Button(ana_pencere, text="Hatırlatma Ekle", font=("Arial", 12), fg='white', bg='#11119c', command=hatirlatma_ekle)
ekle_buton.pack(pady=20)
listele_buton = tk.Button(ana_pencere, text="Hatırlatmaları Listele", font=("Arial", 12), fg='white', bg='#11119c', command=hatirlatmaları_listele)
listele_buton.pack(pady=20)
sil_buton = tk.Button(ana_pencere, text="Hatırlatma Sil", font=("Arial", 12), fg='white', bg='#11119c', command=hatirlatma_sil)
sil_buton.pack(pady=20)
cikis_buton = tk.Button(ana_pencere, text="Çıkış", font=("Arial", 12), fg='white', bg='#11119c', command=ana_pencere.destroy)
cikis_buton.pack(pady=20)

class DijitalSaat:
    def __init__(self, master):
        self.master = master

        self.label = tk.Label(self.master, font=('Arial', 60, 'bold'), bg='#11119c', fg='white')
        self.label.pack(pady=50)

        self.update_time()

    def update_time(self):
        current_time = time.strftime('%H:%M:%S')
        self.label.config(text=current_time)
        self.master.after(1000, self.update_time)

saat = DijitalSaat(ana_pencere)

ana_pencere.mainloop()
