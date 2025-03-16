# Telegram Subscription Checker Bot

Бот проверяет подписку на каналы перед выдачей доступа к контенту.

## Установка на VPS (Ubuntu)

1. **Обновите систему:**
   ```bash
   sudo apt update && sudo apt upgrade -y
Установите Python и зависимости:

bash
Copy
sudo apt install python3-pip python3-venv -y
Клонируйте репозиторий:

bash
Copy
git clone https://github.com/yourusername/tg_sub_checker_bot.git
cd tg_sub_checker_bot
Создайте виртуальное окружение:

bash
Copy
python3 -m venv venv
source venv/bin/activate
Установите зависимости:

bash
Copy
pip install -r requirements.txt
Настройте .env файл:

bash
Copy
nano config/.env
Заполните:

env
Copy
TOKEN=your_bot_token
CHANNELS=-100123456789,-100987654321 (ID каналов через (,))
Создайте systemd сервис:

bash
Copy
sudo nano /etc/systemd/system/tg_sub_bot.service
Добавьте:

ini
Copy
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
Запустите бота:

bash
Copy
sudo systemctl daemon-reload
sudo systemctl start tg_sub_bot
sudo systemctl enable tg_sub_bot
Проверка работы
bash
Copy
sudo systemctl status tg_sub_bot
Copy

---

### Примечания:
1. Замените `YOUR_BOT_TOKEN` на токен от @BotFather.
2. ID каналов должны начинаться с `-100` (для супергрупп/каналов).
3. Бот должен быть администратором в проверяемых каналах.
4. Для приватных каналов используйте username в кнопках (если доступно).