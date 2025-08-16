import pandas as pd
from transformers import pipeline

# CSV dosyasını oku
df_cleaned = pd.read_csv("C:/Users/hrnbo/Downloads/D_zenlenmi__Ek_i_S_zl_k_Verileri.csv")

# Yorumları listeye çevir (NaN varsa string yapar, hata engellenir)
yorumlar = df_cleaned["content"].astype(str).tolist()

# Türkçe BERT ile Duygu Analizi (Sadece PyTorch kullanarak)
sentiment_analysis = pipeline(
    "sentiment-analysis",
    model="savasy/bert-base-turkish-sentiment-cased",
    framework="pt"  # <-- Bu satır hatayı çözüyor
)

# Yorumları toplu analiz et (batch kullanarak)
results = []
batch_size = 32

for i in range(0, len(yorumlar), batch_size):
    batch = yorumlar[i:i + batch_size]
    results.extend(sentiment_analysis(batch))

# Sonuçları DataFrame'e ekle
df_cleaned["duygu"] = [r['label'] for r in results]
df_cleaned["duygu_skoru"] = [r['score'] for r in results]

# İlk birkaç sonucu göster
print(df_cleaned.head())

# Yeni CSV olarak kaydet
df_cleaned.to_csv("C:/Users/hrnbo/Downloads/analizli_duygu_verisi.csv", index=False)
