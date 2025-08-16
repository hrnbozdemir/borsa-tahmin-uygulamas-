import pandas as pd
import os

def clean_and_filter_tweets(file_path, financial_keywords, output_dir, output_file_name):
    # Veriyi yükleme
    df = pd.read_excel(file_path)
    
    # Tweetlerin olduğu sütun ismini tahmin etmeye çalışıyoruz
    tweet_column = 'tweet' if 'tweet' in df.columns else df.columns[0]
    
    # Tüm metinleri küçük harfe çevirerek anahtar kelimeye göre filtreleme
    df[tweet_column] = df[tweet_column].astype(str).str.lower()
    
    # Finansal anahtar kelimeleri içerenleri filtreleme
    financial_tweets = df[df[tweet_column].apply(lambda x: any(keyword in x for keyword in financial_keywords))]
    
    # İstenmeyen kelimeleri veya linkleri içerenleri çıkartma
    unwanted_keywords = ["telegram", "ücretsiz", "bitcoin", "youtube", "http"]
    financial_tweets = financial_tweets[~financial_tweets[tweet_column].apply(lambda x: any(keyword in x for keyword in unwanted_keywords))]
    
    # Aselsan veya asels içermeyenleri kaldırma
    financial_tweets = financial_tweets[financial_tweets[tweet_column].apply(lambda x: "aselsan" in x or "asels" in x)]
    
    # Tekrar eden tweetleri kaldırma
    financial_tweets = financial_tweets.drop_duplicates(subset=[tweet_column])
    
    # Çıkış dosyasının tam yolunu oluşturma
    output_file = os.path.join(output_dir, output_file_name)
    
    # Temizlenmiş veriyi farklı bir dosyaya kaydetme
    financial_tweets.to_excel(output_file, index=False)
    print(f"Temizlenmiş veri kaydedildi: {output_file}")
    
# Finansal içerik belirlemek için anahtar kelimeler
financial_keywords = ["borsa", "hisse", "yatırım", "kazanç", "zarar", "dolar", "euro", "borsa", "kripto", "finans", "faiz", "bilanço", "kar", "borsa istanbul", "yatırımcı", "piyasa", "mali", "temettü", "ekonomi", "para", "altın", "bankacılık", "borsa endeksi", "kredi", "tahvil", "döviz", "sermaye"]

# Dosya yolları
input_file = "C:/Users/hrnbo/Desktop/python/borsa tahmini/dakikalık veri/tweets.xlsx"
output_dir = "C:/Users/hrnbo/Desktop/python/borsa tahmini/dakikalık veri"
output_file_name = "cleaned_tweets.xlsx"

# Fonksiyonu çağırma
clean_and_filter_tweets(input_file, financial_keywords, output_dir, output_file_name)

