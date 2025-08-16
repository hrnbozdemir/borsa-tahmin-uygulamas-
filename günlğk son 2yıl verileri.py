from yahooquery import Ticker
import pandas as pd

# Hisse senedi belirleme
ticker = Ticker("ASELS.IS")

# Son 5 günün 1 dakikalık verilerini al
data = ticker.history(period="5d", interval="1m")

# DataFrame olarak düzenleme
df = pd.DataFrame(data)

# CSV dosya yolu
dosya_yolu = r"C:\Users\hrnbo\Desktop\python\borsa tahmini\dakikalık veri\aselsan_5gun.csv"

# CSV olarak kaydet
df.to_csv(dosya_yolu, index=True)

print(f"Veriler başarıyla kaydedildi: {dosya_yolu}")
