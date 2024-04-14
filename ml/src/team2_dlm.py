from src.team2_read_data import read_csv_with_tab_separator
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()

# Example DataFrame
data_path = 'data\\characters.csv'
df = read_csv_with_tab_separator(data_path)
#X = df[['Keywords', 'Description']]
#y = df['Class']
df['text'] = df['Keywords'] + ' ' + df['Description']
df['labels'] = df['Class']
df['labels'] = label_encoder.fit_transform(df['labels'])
df.drop(columns=['Keywords', 'Description', 'Class'], inplace=True)
print(df.head())
print(df.shape)


tokenizer = get_tokenizer('basic_english')
vocab = build_vocab_from_iterator(map(tokenizer, df['text']), specials=['<unk>', '<pad>'])
vocab.set_default_index(vocab['<unk>'])


class TextClassificationDataset(Dataset):
    def __init__(self, df, vocab, tokenizer):
        self.texts = df['text'].tolist()
        self.labels = df['labels'].tolist()
        self.vocab = vocab
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        tokens = self.vocab(self.tokenizer(text))
        return torch.tensor(tokens, dtype=torch.long), torch.tensor(label, dtype=torch.long)

def collate_batch(batch):
    label_list, text_list = [], []
    for (_text, _label) in batch:
        label_list.append(_label)
        processed_text = torch.tensor(_text, dtype=torch.int64)
        text_list.append(processed_text)
    return pad_sequence(text_list, padding_value=vocab['<pad>']), torch.tensor(label_list, dtype=torch.int64)


dataset = TextClassificationDataset(df, vocab, tokenizer)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True, collate_fn=collate_batch)

class TextCNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_classes):
        super(TextCNN, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.conv1 = nn.Conv1d(in_channels=embed_dim, out_channels=16, kernel_size=3)
        self.pool = nn.MaxPool1d(kernel_size=2)
        self.fc = nn.Linear(16, num_classes)

    def forward(self, text):
        embedded = self.embedding(text)
        embedded = embedded.permute(1, 2, 0) # Needed to adjust dimensions for Conv1d
        conv_out = F.relu(self.conv1(embedded))
        pooled = self.pool(conv_out)
        pooled = pooled.permute(2, 0, 1) # Adjust dimensions back for linear layer
        pooled = torch.flatten(pooled, 1)
        return self.fc(pooled)

# Instantiate the model
num_classes = df['labels'].tolist()
vocab_size = len(vocab)
embed_dim = 64
model = TextCNN(vocab_size, embed_dim, num_classes)

optimizer = Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# Training Loop
for epoch in range(1, 6):  # 5 epochs
    for batch, (text, labels) in enumerate(dataloader):
        optimizer.zero_grad()
        output = model(text)
        loss = criterion(output, labels)
        loss.backward()
        optimizer.step()
    print(f'Epoch: {epoch}, Loss: {loss.item()}')

def evaluate_model(model, dataloader):
    model.eval()  # Set model to evaluation mode
    true_labels = []
    predictions = []

    with torch.no_grad():  # Do not calculate gradients
        for batch, (text, labels) in enumerate(dataloader):
            outputs = model(text)
            _, predicted = torch.max(outputs, 1)
            
            true_labels.extend(labels.tolist())
            predictions.extend(predicted.tolist())

    accuracy = accuracy_score(true_labels, predictions)
    precision, recall, fscore, _ = precision_recall_fscore_support(true_labels, predictions, average='weighted')

    return accuracy, precision, recall, fscore

train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
test_dataset = TextClassificationDataset(test_df, vocab, tokenizer)
test_dataloader = DataLoader(test_dataset, batch_size=16, shuffle=False, collate_fn=collate_batch)
# Assuming the DataFrame df and the classes TextClassificationDataset and collate_batch are defined

# Split DataFrame into training and test sets
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Create training and test datasets
train_dataset = TextClassificationDataset(train_df, vocab, tokenizer)
test_dataset = TextClassificationDataset(test_df, vocab, tokenizer)

# Create DataLoaders for training and test sets
train_dataloader = DataLoader(train_dataset, batch_size=16, shuffle=True, collate_fn=collate_batch)
test_dataloader = DataLoader(test_dataset, batch_size=16, shuffle=False, collate_fn=collate_batch)

# Assume test_dataloader is defined and loaded with the test dataset
accuracy, precision, recall, fscore = evaluate_model(model, test_dataloader)
print(f'Accuracy: {accuracy:.4f}')
print(f'Precision: {precision:.4f}')
print(f'Recall: {recall:.4f}')
print(f'F1 Score: {fscore:.4f}')

