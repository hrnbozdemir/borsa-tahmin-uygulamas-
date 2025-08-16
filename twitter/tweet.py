import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
import threading
import subprocess
from datetime import datetime

# Veri yolları
veri_yolu = r"C:\\Users\\hrnbo\\Desktop\\python\\borsa tahmini\\dakikalık veri"
aselsan_dosya_adi = "aselsan_gunluk_veri.xlsx"
bist_dosya_adi = "bist100_gunluk_veri.xlsx"

veri_yolu_15dk = r"C:\\Users\\hrnbo\\Desktop\\python\\borsa tahmini\\dakikalık veri"
aselsan_15dk_dosya = "aselsan_15dk_veri.xlsx"

veri_guncelleme_dosyasi = r"C:\\Users\\hrnbo\\Desktop\\python\\borsa tahmini\\model eğitimi ana kod\\veri güncellemeleri yfinance.py"
tweet_py_dosyasi = r"C:\\Users\\hrnbo\\Desktop\\python\\borsa tahmini\\twitter\\tweet.py"
tweet_excel_path = os.path.join(veri_yolu, "tweets.xlsx")

# CustomTkinter ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Aselsan Tahmin ve Analiz")
app.state("zoomed")  # Tam ekran başlat

# Başlık
title_label = ctk.CTkLabel(app, text="📊 ASELSAN Tahmin Uygulaması", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

# Veri güncelleme işlemi
veri_proses = None

def arka_planda_guncelle():
    global veri_proses
    try:
        veri_proses = subprocess.Popen(['python', veri_guncelleme_dosyasi])
    except Exception as e:
        print("Arka plan güncelleme hatası:", e)

def veri_guncelle():
    global veri_proses
    try:
        if veri_proses and veri_proses.poll() is None:
            veri_proses.terminate()
        veri_proses = subprocess.Popen(['python', veri_guncelleme_dosyasi])
        status_label.configure(text="Durum: Veriler yeniden güncelleniyor...")
    except Exception as e:
        status_label.configure(text=f"Durum: Güncelleme hatası ❌ {e}")

def tweet_cek_kontrol():
    bugun = datetime.today().date()

    try:
        df = pd.read_excel(tweet_excel_path)
        df['Tarih'] = pd.to_datetime(df['Tarih'], errors='coerce')
        en_son_tweet = df['Tarih'].max().date()

        if en_son_tweet >= bugun:
            status_label.configure(text=f"Bugüne ait tweetler zaten var 🟢")
            tweet_goster(df[df['Tarih'].dt.date == bugun])
            return
    except Exception as e:
        print("Tweet verisi okunamadı, yine de devam ediliyor:", e)

    try:
        subprocess.Popen(['python', tweet_py_dosyasi])
        status_label.configure(text="Tweet çekme işlemi başladı 🐦")
        app.after(15000, tweet_cek_kontrol)  # 15 saniye sonra tekrar dene
    except Exception as e:
        status_label.configure(text=f"Tweet çekme hatası ❌ {e}")

def tweet_goster(df):
    if df.empty:
        status_label.configure(text="Bugüne ait tweet bulunamadı.")
        return

    # Eğer daha önce oluşturulmuş bir frame varsa kaldır
    for widget in tweet_frame.winfo_children():
        widget.destroy()

    tweet_label = ctk.CTkLabel(tweet_frame, text="Bugünkü Tweetler", font=("Arial", 16, "bold"))
    tweet_label.pack(pady=5)

    tweet_box = ctk.CTkTextbox(tweet_frame, wrap="word", height=200)
    tweet_box.pack(fill="both", expand=True, padx=10, pady=5)

    for _, row in df.iterrows():
        tweet_box.insert("end", f"{row['Tarih']}\n{row['Tweet']}\n\n")

# Grafik alanı
chart_frame = ctk.CTkFrame(app)
chart_frame.pack(pady=10, fill="both", expand=True)

# Tweet kutusu
tweet_frame = ctk.CTkFrame(app)
tweet_frame.pack(pady=5, fill="both", expand=False)

# Grafik çizim fonksiyonu
def grafik_goster():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # ASELSAN günlük veri
    try:
        path_aselsan = os.path.join(veri_yolu, aselsan_dosya_adi)
        aselsan_df = pd.read_excel(path_aselsan, engine='openpyxl')
        aselsan_df.columns = ['datetime', 'close', 'high', 'low', 'open', 'volume']
        aselsan_df['datetime'] = pd.to_datetime(aselsan_df['datetime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        aselsan_df.sort_values('datetime', inplace=True)
        axes[0].plot(aselsan_df['datetime'], aselsan_df['close'], label="ASELSAN")
        axes[0].set_title("ASELSAN Günlük")
        axes[0].tick_params(axis='x', labelrotation=45)
    except Exception as e:
        print("ASELSAN günlük grafik hatası:", e)
        axes[0].text(0.5, 0.5, f"Hata: {e}", ha='center')

    # BIST veri
    try:
        path_bist = os.path.join(veri_yolu, bist_dosya_adi)
        bist_df = pd.read_excel(path_bist, engine='openpyxl')
        bist_df.columns = ['datetime', 'close', 'high', 'low', 'open', 'volume']
        bist_df['datetime'] = pd.to_datetime(bist_df['datetime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        bist_df.sort_values('datetime', inplace=True)
        axes[1].plot(bist_df['datetime'], bist_df['close'], color="orange", label="BIST100")
        axes[1].set_title("BIST100 Günlük")
        axes[1].tick_params(axis='x', labelrotation=45)
    except Exception as e:
        print("BIST grafik hatası:", e)
        axes[1].text(0.5, 0.5, f"Hata: {e}", ha='center')

    # ASELSAN 15dk veri
    try:
        path_15dk = os.path.join(veri_yolu_15dk, aselsan_15dk_dosya)
        a15_df = pd.read_excel(path_15dk, engine='openpyxl')
        a15_df.columns = ['datetime', 'close', 'high', 'low', 'open', 'volume']
        a15_df['datetime'] = pd.to_datetime(a15_df['datetime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        a15_df.sort_values('datetime', inplace=True)
        axes[2].plot(a15_df['datetime'], a15_df['close'], color="green", label="15dk")
        axes[2].set_title("ASELSAN 15dk")
        axes[2].tick_params(axis='x', labelrotation=45)
    except Exception as e:
        print("ASELSAN 15dk grafik hatası:", e)
        axes[2].text(0.5, 0.5, f"Hata: {e}", ha='center')

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# Uygulama açıldığında grafikleri göster
app.after(100, grafik_goster)


# Güncelleme butonları
guncelle_btn = ctk.CTkButton(app, text="🔄 Verileri Güncelle", command=veri_guncelle)
guncelle_btn.pack(pady=10)

tweet_btn = ctk.CTkButton(app, text="🐦 Tweetleri Güncelle", command=tweet_cek_kontrol)
tweet_btn.pack(pady=10)

# Durum etiketi
status_label = ctk.CTkLabel(app, text="Durum: Grafikler Yüklendi", font=("Arial", 14))
status_label.pack(pady=20)

# Ana döngü
app.mainloop()
