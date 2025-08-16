import fitz  # PyMuPDF
import re
import pandas as pd
import os
from datetime import datetime

# Başlangıç ve bitiş tarihleri
start_date = datetime.strptime("03-2023", "%m-%Y")
end_date = datetime.strptime("09-2024", "%m-%Y")

# Hisse sayısı (örnek)
hisse_sayisi = 456_000_000

# Metinden veri çekme fonksiyonu
def extract_value(pattern, text, default="Bulunamadı"):
    match = re.search(pattern, text)
    return match.group(1) if match else default

# Ay ay ilerleyerek her biri için dosya işle
current_date = start_date
while current_date <= end_date:
    ay = current_date.strftime("%m")
    yil = current_date.strftime("%Y")

    # 3 farklı isim formatı denenecek
    possible_filenames = [
        f"{ay}-{yil}_tr.pdf",
        f"{ay}_{yil}_tr.pdf",
        f"{ay}.{yil}_tr.pdf",
    ]

    pdf_path = None
    for filename in possible_filenames:
        if os.path.exists(filename):
            pdf_path = filename
            break

    if not pdf_path:
        print(f"❌ Dosya bulunamadı: {ay}-{yil} için hiçbir varyasyon yok.")
        current_date = current_date.replace(day=1)
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
        continue

    print(f"🔍 İşleniyor: {pdf_path}")
    try:
        pdf_document = fitz.open(pdf_path)
        text = ""
        for page in pdf_document:
            text += page.get_text("text") + "\n"
        pdf_document.close()
    except Exception as e:
        print(f"❌ Hata oluştu ({pdf_path}): {e}")
        current_date = current_date.replace(day=1)
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
        continue

    # Finansal verileri çıkart
    financial_data = {
        "Toplam Varlıklar": extract_value(r"TOPLAM VARLIKLAR\s+([\d,.]+)", text),
        "Kısa Vadeli Borçlar": extract_value(r"Kısa Vadeli Yükümlülükler\s+([\d,.]+)", text),
        "Uzun Vadeli Borçlar": extract_value(r"Uzun Vadeli Yükümlülükler\s+([\d,.]+)", text),
        "Toplam Özkaynaklar": extract_value(r"TOPLAM ÖZKAYNAKLAR\s+([\d,.]+)", text),
        "Net Kâr": extract_value(r"NET DÖNEM KÂRI\s+([\d,.]+)", text),
        "Brüt Kâr": extract_value(r"BRÜT KÂR\s+([\d,.]+)", text),
        "FAVÖK": extract_value(r"ESAS FAALİYET KÂRI\s+([\d,.]+)", text),
        "Nakit Akışları": extract_value(r"NAKİT VE NAKİT BENZERLERİ\s+([\d,.]+)", text),
    }

    # Borç/Özkaynak Oranı
    try:
        financial_data["Borç/Özkaynak Oranı"] = float(financial_data["Kısa Vadeli Borçlar"].replace(",", "")) / float(financial_data["Toplam Özkaynaklar"].replace(",", ""))
    except:
        financial_data["Borç/Özkaynak Oranı"] = "Hesaplanamadı"

    # EPS
    try:
        financial_data["Hisse Başına Kâr (EPS)"] = float(financial_data["Net Kâr"].replace(",", "")) / hisse_sayisi
    except:
        financial_data["Hisse Başına Kâr (EPS)"] = "Hesaplanamadı"

    # Kaydet
    df_financial = pd.DataFrame(financial_data.items(), columns=["Finansal Göstergeler", "Değerler"])
    csv_filename = f"finansal_veriler_{ay}-{yil}.csv"
    df_financial.to_csv(csv_filename, index=False)
    print(f"✅ Kaydedildi: {csv_filename}")

    # Bir sonraki aya geç
    if current_date.month == 12:
        current_date = current_date.replace(year=current_date.year + 1, month=1)
    else:
        current_date = current_date.replace(month=current_date.month + 1)
