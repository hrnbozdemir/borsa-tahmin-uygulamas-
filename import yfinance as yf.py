import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

def get_and_save_combined_data(ticker, interval, iterations, days_to_subtract, save_path):
    combined_data = pd.DataFrame()
    current_end_date = datetime.now()
    current_start_date = current_end_date - timedelta(days=days_to_subtract)

    for i in range(iterations):
        try:
            print(f"\n{i+1}. iterasyon: {current_start_date.date()} - {current_end_date.date()}")

            data = yf.download(
                tickers=ticker,
                start=current_start_date.strftime("%Y-%m-%d"),
                end=current_end_date.strftime("%Y-%m-%d"),
                interval=interval
            )

            if data.empty:
                print("Veri alınamadı, atlanıyor.")
            else:
                data.index = data.index.tz_localize(None)
                combined_data = pd.concat([data, combined_data])
                print("Veri başarıyla eklendi.")

        except Exception as e:
            print(f"Hata oluştu: {e}")

        current_end_date -= timedelta(days=days_to_subtract)
        current_start_date -= timedelta(days=days_to_subtract)

    try:
        if not combined_data.empty:
            if not os.path.exists(os.path.dirname(save_path)):
                os.makedirs(os.path.dirname(save_path))

            combined_data.to_excel(save_path)
            print(f"Tüm veriler başarıyla kaydedildi: {save_path}")
        else:
            print("Hiç veri alınamadı.")
    except Exception as e:
        print(f"Kaydetme sırasında hata: {e}")

# Parametreler
ticker = "XU100.IS"
interval = "15m"
iterations = 6            # Toplam 30 günlük veri için 5 günlük 6 parça
days_to_subtract = 5
save_path = "C:/Users/hrnbo/Desktop/aralıklıveri/aselsan_15dk_veri.xlsx"

get_and_save_combined_data(
    ticker=ticker,
    interval=interval,
    iterations=iterations,
    days_to_subtract=days_to_subtract,
    save_path=save_path
)
