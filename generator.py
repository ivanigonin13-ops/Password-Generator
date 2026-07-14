import string
import secrets
# 1. Импортируем библиотеку для буфера обмена
import pyperclip 
from zxcvbn import zxcvbn

def format_exact_time(seconds):
    """Преобразует секунды в детальный формат."""
    if seconds < 1:
        ms = round(seconds * 1000, 2)
        return f"{ms} мс (мгновенно)"
    
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    YEAR = 31536000
    CENTURY = 3153600000

    if seconds >= CENTURY:
        val = seconds / CENTURY
        return f"{val:,.1f} веков"
    elif seconds >= YEAR:
        val = seconds / YEAR
        return f"{val:,.1f} лет"
        
    days = int(seconds // DAY)
    seconds %= DAY
    hours = int(seconds // HOUR)
    seconds %= HOUR
    minutes = int(seconds // MINUTE)
    seconds %= MINUTE
    rem_seconds = round(seconds, 2)

    parts = []
    if days > 0: parts.append(f"{days} дн.")
    if hours > 0: parts.append(f"{hours} ч.")
    if minutes > 0: parts.append(f"{minutes} мин.")
    if rem_seconds > 0 or not parts: parts.append(f"{rem_seconds} сек.")

    return " ".join(parts)

def check_password_strength(password):
    """Возвращает оценку и словарь с временем взлома."""
    result = zxcvbn(password)
    score = result["score"] + 1 
    
    scenarios_map = {
        "online_throttling_100_per_hour": "Онлайн-атака (есть лимит попыток)",
        "online_no_throttling_10_per_second": "Онлайн-атака (без защиты)",
        "offline_slow_hashing_1e4_per_second": "Оффлайн (Локальный ПК хакера)",
        "offline_fast_hashing_1e10_per_second": "Оффлайн (Суперкомпьютер / GPU)"
    }
    
    crack_times_formatted = {}
    for key, seconds in result["crack_times_seconds"].items():
        if key in scenarios_map:
            crack_times_formatted[scenarios_map[key]] = format_exact_time(seconds)
            
    feedback = []
    if result["feedback"]["warning"]:
        feedback.append(f"• Предупреждение: {result['feedback']['warning']}")
    if result["feedback"]["suggestions"]:
        for suggestion in result["feedback"]["suggestions"]:
            feedback.append(f"• Совет: {suggestion}")
            
    return score, crack_times_formatted, feedback

def generate_password():
    print("--- Настройка генератора паролей ---")
    while True:
        try:
            length = int(input("Введите длину пароля: "))
            if length < 4: print("Минимум 4 символа."); continue
            break
        except ValueError: print("Введите число.")
    
    include_digits = input("Включать цифры? (да/нет): ").strip().lower() == 'да'
    include_special = input("Включать спецсимволы? (да/нет): ").strip().lower() == 'да'
    
    chars = string.ascii_letters
    if include_digits: chars += string.digits
    if include_special: chars += string.punctuation
        
    return "".join(secrets.choice(chars) for _ in range(length))

if __name__ == "__main__":
    password = generate_password()
    
    print("\n" + "="*50)
    print(f"ПАРОЛЬ: {password}")
    print("="*50)
    
    # --- БЛОК АВТОМАТИЧЕСКОГО КОПИРОВАНИЯ ---
    try:
        pyperclip.copy(password)
        print("✅ Пароль успешно скопирован в буфер обмена!")
    except Exception as e:
        print(f"⚠️ Не удалось скопировать пароль: {e}")
        print("(На Linux убедитесь, что установлен пакет xclip: sudo apt install xclip)")
    # ----------------------------------------
    
    score, times_dict, tips = check_password_strength(password)
    
    print(f"\nНадежность: {score}/5")
    
    print("\n--- ВРЕМЯ ВЗЛОМА В РАЗНЫХ УСЛОВИЯХ ---")
    for scenario, time_val in times_dict.items():
        print(f"{scenario:<40} : {time_val}")
        
    print("-" * 50)
    if score == 5: print("🟢 Отличный пароль!")
    elif score >= 3: print("🟡 Средняя надежность.")
    else: print("🔴 Слабый пароль!")
        
    if tips:
        print("\nРекомендации:")
        for tip in tips: print(tip)
