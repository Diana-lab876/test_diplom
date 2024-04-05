import pandas as pd
import numpy as np
import chainer
import chainer.links as L
import chainer.functions as F
from chainer import iterators, optimizers, training
from chainer.training import extensions

# Загрузка данных из CSV-файла
df = pd.read_csv('error_correction_dataset.csv')

# Преобразование данных в списки
errors = df['error'].tolist()
corrections = df['correction'].tolist()

# Создание токенизатора
tokenizer = chainer.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(errors)

# Преобразование текста в последовательности чисел
error_sequences = tokenizer.texts_to_sequences(errors)
correction_sequences = tokenizer.texts_to_sequences(corrections)

# Подготовка данных для обучения
max_len = max([len(seq) for seq in error_sequences])
padded_error_sequences = chainer.preprocessing.sequence.pad_sequence(error_sequences, maxlen=max_len, padding='post')
padded_correction_sequences = chainer.preprocessing.sequence.pad_sequence(correction_sequences, maxlen=max_len, padding='post')

# Разделение данных на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(padded_error_sequences, padded_correction_sequences, test_size=0.2, random_state=42)

# Преобразование формата y_train
y_train = chainer.Variable(y_train)

# Создание модели нейронной сети
class MyModel(chainer.Chain):
    def __init__(self, vocab_size, hidden_dim):
        super(MyModel, self).__init__()
        with self.init_scope():
            self.embed = L.EmbedID(vocab_size, hidden_dim)
            self.lstm = L.LSTM(hidden_dim, hidden_dim)
            self.fc = L.Linear(hidden_dim, vocab_size)

    def __call__(self, x):
        x = self.embed(x)
        x = self.lstm(x)
        return self.fc(x)

model = MyModel(vocab_size=len(tokenizer.word_index)+1, hidden_dim=64)

# Определение функции потерь и оптимизатора
optimizer = optimizers.Adam()
optimizer.setup(model)

# Создание итераторов
train_iter = iterators.SerialIterator(dataset=list(zip(X_train, y_train)), batch_size=32, shuffle=True)
updater = training.StandardUpdater(train_iter, optimizer)
trainer = training.Trainer(updater, (20, 'epoch'))

# Запуск обучения
trainer.run()

# Оценка модели на тестовых данных
# loss, accuracy = model.evaluate(X_test, y_test)
# print(f'Test Accuracy: {accuracy}')

# Сохранение модели
chainer.serializers.save_npz('error_correction_model.npz', model)
