import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, AdamW, BertConfig
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from tqdm import tqdm
import os

# Cihaz kontrolü
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Veriyi oku
df = pd.read_excel("toplamyorumlar.xlsx")
df = df[df["duygu"].notna()]
df["duygu"] = df["duygu"].astype(str).str.strip().str.lower()

# Etiketleri sayıya çevir
etiket_map = {"negative": 0, "positive": 1}
filtered_df = df[df["duygu"].isin(etiket_map.keys())]
filtered_df["label"] = filtered_df["duygu"].map(etiket_map)

if filtered_df.empty:
    raise ValueError("Filtrelenmiş veri boş! 'positive' ve 'negative' değerlerini içeren etiketler bulunamadı.")

# Metin ve etiketleri al
texts = filtered_df["Tweet"].astype(str).tolist()
labels = filtered_df["label"].astype(int).tolist()

# Tokenizer ve model
model_name = "dbmdz/bert-base-turkish-cased"
tokenizer = BertTokenizer.from_pretrained(model_name)
config = BertConfig.from_pretrained(model_name)
config.num_hidden_layers = 14
model = BertForSequenceClassification.from_pretrained(model_name, config=config)
model.to(device)

# Dataset sınıfı
class TweetDataset(Dataset):
    def __init__(self, texts, labels):
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=128, return_tensors="pt")
        self.labels = torch.tensor(labels)

    def __getitem__(self, idx):
        item = {k: v[idx] for k, v in self.encodings.items()}
        item["labels"] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)

# Train/test ayrımı
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)
train_dataset = TweetDataset(train_texts, train_labels)
val_dataset = TweetDataset(val_texts, val_labels)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)

# Optimizer
optimizer = AdamW(model.parameters(), lr=2e-5)

# Eğitim
epochs = 5
train_losses = []
val_accuracies = []

for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}"):
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        total_loss += loss.item()
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    avg_loss = total_loss / len(train_loader)
    train_losses.append(avg_loss)
    print(f"Epoch {epoch+1} Loss: {avg_loss:.4f}")

    # Doğrulama
    model.eval()
    predictions, true_labels = [], []
    with torch.no_grad():
        for batch in val_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()
            labels = batch["labels"].cpu().numpy()
            predictions.extend(preds)
            true_labels.extend(labels)
    acc = accuracy_score(true_labels, predictions)
    val_accuracies.append(acc)
    print(f"Validation Accuracy: {acc:.4f}")

# Son klasör yolu ve isim ayarı
final_accuracy = val_accuracies[-1] if val_accuracies else 0.0
acc_str = f"{final_accuracy:.2f}".replace(".", "_")
epoch_info = f"{epochs}epoch_{config.num_hidden_layers}katman"
output_dir = f"C:/Users/hrnbo/Desktop/python/borsa tahmini/dil modeli eğitimş/eğitim sonuçları/{epoch_info}_acc_{acc_str}"
os.makedirs(output_dir, exist_ok=True)

# Grafikler ve kayıt
plt.figure(figsize=(10, 4))
plt.plot(range(1, epochs+1), train_losses, label="Train Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Eğitim Kaybı (Loss)")
plt.legend()
plt.grid()
plt.savefig(os.path.join(output_dir, "loss_grafik.png"))
plt.close()

plt.figure(figsize=(10, 4))
plt.plot(range(1, epochs+1), val_accuracies, label="Validation Accuracy", color='green')
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Doğruluk (Validation Accuracy)")
plt.legend()
plt.grid()
plt.savefig(os.path.join(output_dir, "accuracy_grafik.png"))
plt.close()

# Modeli kaydet
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print(f"Eğitim tamamlandı ve model ile grafikler '{output_dir}' klasörüne kaydedildi.")
