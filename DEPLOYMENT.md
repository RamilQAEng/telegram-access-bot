# Руководство по развертыванию Telegram-бота

Это руководство описывает процесс развертывания Telegram-бота на сервере с использованием `systemd`.

## 1. Подготовка сервера

Убедитесь, что на сервере установлены:
- Python 3.8+
- `pip`
- `git`

## 2. Клонирование репозитория

Склонируйте репозиторий с ботом на сервер:
```bash
git clone https://github.com/RamilQAEng/telegram-access-bot.git /opt/tg_sub_checker_bot
```

## 3. Установка зависимостей

Перейдите в директорию проекта и установите зависимости:
```bash
cd /opt/tg_sub_checker_bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Настройка переменных окружения

Создайте файл `.env` в директории `config/`:
```bash
nano config/.env
```

Пример содержимого:
```env
TOKEN=ваш_токен_бота
CHANNELS=-1001234567890,-1000987654321
```

## 5. Создание systemd сервиса

Создайте файл сервиса:
```bash
sudo nano /etc/systemd/system/tg_sub_bot.service
```

Добавьте следующий контент:
```ini
[Unit]
Description=Telegram Subscription Bot
After=network.target

[Service]
User=ubuntu  # Замените на вашего пользователя
WorkingDirectory=/opt/tg_sub_checker_bot
ExecStart=/opt/tg_sub_checker_bot/venv/bin/python3 /opt/tg_sub_checker_bot/src/bot.py
Restart=always
Environment="PATH=/opt/tg_sub_checker_bot/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

[Install]
WantedBy=multi-user.target
```

## 6. Запуск и настройка сервиса

Перезагрузите systemd для применения изменений:
```bash
sudo systemctl daemon-reload
```

Запустите сервис:
```bash
sudo systemctl start tg_sub_bot
```

Включите автозапуск при старте системы:
```bash
sudo systemctl enable tg_sub_bot
```

## 7. Проверка работы сервиса

Проверьте статус сервиса:
```bash
sudo systemctl status tg_sub_bot
```

Просмотрите логи:
```bash
journalctl -u tg_sub_bot -f
```

## 8. Управление сервисом

Перезапуск сервиса:
```bash
sudo systemctl restart tg_sub_bot
```

Остановка сервиса:
```bash
sudo systemctl stop tg_sub_bot
```

Просмотр логов:
```bash
journalctl -u tg_sub_bot -f
```

## 9. Дополнительные настройки

Для перенаправления логов в файл добавьте в секцию `[Service]`:
```ini
StandardOutput=append:/var/log/tg_sub_bot.log
StandardError=append:/var/log/tg_sub_bot_error.log
```

## 10. Завершение

Теперь ваш бот будет работать на сервере постоянно, автоматически перезапускаться в случае сбоев и запускаться при старте системы.