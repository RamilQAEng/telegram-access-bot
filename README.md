
## Установка на VPS (Ubuntu)

### 1. Подготовка системы
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv -y
```

### 2. Клонирование репозитория
```bash
git clone https://github.com/RamilQAEng/telegram-access-bot.git
cd telegram-access-bot
```

### 3. Настройка окружения
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Конфигурация
Создайте файл `.env` в папке `config`:
```bash
nano config/.env
```

Пример содержимого:
```env
TOKEN=your_bot_token
CHANNELS=-100123456789,-100987654321
```

### 5. Настройка systemd сервиса
Создайте файл сервиса:
```bash
sudo nano /etc/systemd/system/tg_sub_bot.service
```

Добавьте конфигурацию:
```ini
[Unit]
Description=Telegram Subscription Bot
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/tg_sub_checker_bot
ExecStart=/path/to/tg_sub_checker_bot/venv/bin/python3 src/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 6. Запуск бота
```bash
sudo systemctl daemon-reload
sudo systemctl start tg_sub_bot
sudo systemctl enable tg_sub_bot
```

### 7. Проверка работы
```bash
sudo systemctl status tg_sub_bot
```

## Примечания
1. Замените `your_bot_token` на токен от @BotFather
2. ID каналов должны начинаться с `-100` (для супергрупп/каналов)
3. Бот должен быть администратором в проверяемых каналах
4. Для приватных каналов используйте username в кнопках (если доступно)


tg_sub_checker_bot/
├── config/
│ └── .env # Конфигурационный файл
├── src/
│ └── bot.py # Основной код бота
├── venv/ # Виртуальное окружение
├── requirements.txt # Зависимости
├── README.md # Документация
└── .gitignore # Игнорируемые файлы