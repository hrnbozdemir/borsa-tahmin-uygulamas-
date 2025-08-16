import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def get_and_save_daily_data(ticker, save_path):
    """Mümkün olan en eski tarihten bugüne kadar günlük verileri çeker ve kaydeder."""
    start_date = "2000-01-01"
    end_date = datetime.today().strftime("%Y-%m-%d")

    print(f"{ticker} için {start_date} - {end_date} arasındaki günlük veriler çekiliyor...")

    try:
        data = yf.download(
            tickers=ticker,
            start=start_date,
            end=end_date,
            interval="1d"
        )

        if data.empty:
            print("Veri bulunamadı.")
            return

        data.index = data.index.tz_localize(None)

        directory = os.path.dirname(save_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
                data.to_excel(writer, sheet_name=ticker.replace(".IS", ""))
            print(f"Veriler başarıyla kaydedildi: {save_path}")
        except Exception as save_error:
            print(f"Dosya kaydedilirken hata oluştu: {save_error}")

    except Exception as e:
        print(f"Veri çekme sırasında hata oluştu: {e}")

# 📌 Parametreler
ticker = "XU100.IS"  # İlgili hisse senedi ya da endeks
save_path = "C:/Users/hrnbo/Desktop/aralıklıveri/bist_gunluk_veriler2.xlsx"

# 📌 Fonksiyonu çalıştır
get_and_save_daily_data(ticker, save_path)
