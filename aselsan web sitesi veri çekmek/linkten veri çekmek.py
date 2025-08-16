import requests
import os

def download_latest_financial_report():
    # En güncel finansal raporun tahmini URL yapısı
    base_url = "https://wwwcdn.aselsan.com/api/file/"
    latest_pdf_name = "12_2024_TR.pdf"  # Her ay güncelleyerek en son raporu takip edebilirsin

    # Tam URL oluştur
    latest_pdf_url = base_url + latest_pdf_name

    # PDF dosyasını indir
    pdf_response = requests.get(latest_pdf_url)
    if pdf_response.status_code == 200:
        # PDF dosyasını kaydet
        pdf_filename = os.path.basename(latest_pdf_url)
        with open(pdf_filename, "wb") as pdf_file:
            pdf_file.write(pdf_response.content)
        print(f"{pdf_filename} başarıyla indirildi.")
        return pdf_filename
    else:
        print("PDF dosyası indirilemedi. Linki ve dosya adını kontrol et.")
        return None

# En güncel finansal raporu indir
download_latest_financial_report()
