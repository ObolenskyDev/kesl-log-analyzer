# 🛡️ KESL Log Analyzer

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python)
![Bash](https://img.shields.io/badge/Shell-Bash-4EAA25?style=flat&logo=gnu-bash)
![Linux](https://img.shields.io/badge/Platform-Linux-FCC624?style=flat&logo=linux&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

Набор скриптов для автоматизации анализа трассировок Kaspersky Endpoint Security for Linux (KESL). Разработан для ускорения поиска корневых причин (RCA) в тяжелых логах (1GB+).

---

## 📸 Пример анализа
*(Автоматический поиск ошибок и вывод окружающего контекста)*

![Log Analysis Demo](analyzer_demo.png)

---

## 🛠️ Инструментарий
1. **trace_analyzer.py**: Построчный парсер. Ищет ошибки (Error, Fail, Critical) и выводит контекст (строки до/после). Оптимизирован для работы при дефиците RAM.
2. **log_rotate.sh**: Скрипт обслуживания. Сжимает старые трассировки в gzip и чистит архивы по политике хранения (Retention Policy).

---

## 🚀 Использование
Анализ конкретного лога:
sudo python3 trace_analyzer.py /var/log/kaspersky/kesl/kesl_launcher.log

Ротация логов (запуск вручную или через cron):
sudo ./log_rotate.sh
