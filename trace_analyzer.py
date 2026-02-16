import sys
import re
import os

# Утилита для анализа трассировок KESL / KSC Agent.
# Ищет ключевые слова (Error, Fail) и выводит контекст события.

# Цвета для вывода (работают в большинстве Linux-терминалов)
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def analyze_trace(filepath):
    if not os.path.exists(filepath):
        print(f"{RED}[Ошибка] Файл {filepath} не найден.{RESET}")
        return

    print(f"{GREEN}--- Запуск анализа: {filepath} ---{RESET}")
    
    # Регулярка для поиска ошибок (игнорируем регистр)
    error_pattern = re.compile(r"(error|fail|critical|exception|denied)", re.IGNORECASE)
    
    found_count = 0
    context_size = 2  # Количество строк контекста (до и после)
    
    try:
        # errors='ignore' спасает от крашей на битых символах в логах
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        total_lines = len(lines)
        print(f"Всего строк: {total_lines}. Сканирование...")

        for i, line in enumerate(lines):
            if error_pattern.search(line):
                found_count += 1
                print(f"\n{YELLOW}[Событие #{found_count} | Строка {i+1}]{RESET}")
                
                # Выводим контекст ДО
                start = max(0, i - context_size)
                for ctx_line in lines[start:i]:
                    print(f"  {ctx_line.strip()}")
                
                # Выводим САМУ ошибку (Жирным/Красным)
                print(f"{RED}>> {line.strip()}{RESET}")
                
                # Выводим контекст ПОСЛЕ
                end = min(total_lines, i + 1 + context_size)
                for ctx_line in lines[i+1:end]:
                    print(f"  {ctx_line.strip()}")
                print("-" * 40)

        if found_count == 0:
            print(f"{GREEN}✅ Ошибок и критических событий не найдено.{RESET}")
        else:
            print(f"{RED}⚠️  Найдено подозрительных событий: {found_count}{RESET}")

    except Exception as e:
        print(f"Ошибка обработки: {e}")

if __name__ == "__main__":
    # Логика создания демо-лога в папке logs/
    if len(sys.argv) < 2:
        log_dir = "logs"
        demo_log = os.path.join(log_dir, "kesl_trace.log")

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        print(f"Файл не указан. Создаю демо-лог '{demo_log}'...")
        with open(demo_log, "w") as f:
            f.write("2026-02-16 10:00:00.123 \tInfo \tStarting KESL service...\n")
            f.write("2026-02-16 10:00:00.125 \tInfo \tLoading modules...\n")
            f.write("2026-02-16 10:00:00.500 \tError \tConnection refused: KSC server (192.168.1.10) is unreachable.\n")
            f.write("2026-02-16 10:00:00.505 \tInfo \tRetrying connection in 10 seconds...\n")
            f.write("2026-02-16 10:00:10.000 \tInfo \tConnection attempt #2...\n")
            f.write("2026-02-16 10:00:10.050 \tCritical \tLicense validation FAILED. Key is blacklisted.\n")
            f.write("2026-02-16 10:00:10.100 \tInfo \tStopping tasks...\n")
        
        analyze_trace(demo_log)
    else:
        analyze_trace(sys.argv[1])