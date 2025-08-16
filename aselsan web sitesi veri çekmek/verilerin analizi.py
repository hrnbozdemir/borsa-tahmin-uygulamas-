import fitz  # PyMuPDF
import re
import pandas as pd

# 📂 PDF dosyasının adı (Aynı dizinde olduğundan emin ol!)
pdf_path = "12_2024_TR.pdf"

# 📌 PDF'yi aç ve metni oku
pdf_document = fitz.open(pdf_path)
text = ""
for page in pdf_document:
    text += page.get_text("text") + "\n"
pdf_document.close()

# 📌 Önemli finansal verileri çıkarma (Regex ile)
financial_data = {}

def extract_value(pattern, text, default="Bulunamadı"):
    match = re.search(pattern, text)
    return match.group(1) if match else default

financial_data["Toplam Varlıklar"] = extract_value(r"TOPLAM VARLIKLAR\s+([\d,.]+)", text)
financial_data["Kısa Vadeli Borçlar"] = extract_value(r"Kısa Vadeli Yükümlülükler\s+([\d,.]+)", text)
financial_data["Uzun Vadeli Borçlar"] = extract_value(r"Uzun Vadeli Yükümlülükler\s+([\d,.]+)", text)
financial_data["Toplam Özkaynaklar"] = extract_value(r"TOPLAM ÖZKAYNAKLAR\s+([\d,.]+)", text)
financial_data["Net Kâr"] = extract_value(r"NET DÖNEM KÂRI\s+([\d,.]+)", text)
financial_data["Brüt Kâr"] = extract_value(r"BRÜT KÂR\s+([\d,.]+)", text)
financial_data["FAVÖK"] = extract_value(r"ESAS FAALİYET KÂRI\s+([\d,.]+)", text)
financial_data["Nakit Akışları"] = extract_value(r"NAKİT VE NAKİT BENZERLERİ\s+([\d,.]+)", text)

# 📌 Borç/Özkaynak Oranı Hesaplama
try:
    financial_data["Borç/Özkaynak Oranı"] = float(financial_data["Kısa Vadeli Borçlar"].replace(",", "")) / float(financial_data["Toplam Özkaynaklar"].replace(",", ""))
except:
    financial_data["Borç/Özkaynak Oranı"] = "Hesaplanamadı"

# 📌 Hisse Başına Kâr (EPS) - (Örnek hisse sayısı: 456M)
hisse_sayisi = 456000000  
try:
    financial_data["Hisse Başına Kâr (EPS)"] = float(financial_data["Net Kâr"].replace(",", "")) / hisse_sayisi
except:
    financial_data["Hisse Başına Kâr (EPS)"] = "Hesaplanamadı"

# 📌 Verileri DataFrame'e dönüştür
df_financial = pd.DataFrame(financial_data.items(), columns=["Finansal Göstergeler", "Değerler"])

# 📌 CSV olarak kaydet
csv_filename = "aselsan_finansal_veriler.csv"
df_financial.to_csv(csv_filename, index=False)

# 📌 Sonuçları göster
print(f"✅ Finansal veriler '{csv_filename}' dosyasına kaydedildi! İçeriği görmek için açabilirsin.\n")
print(df_financial)
