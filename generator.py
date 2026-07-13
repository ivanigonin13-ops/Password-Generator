import string
import secrets

def check_password_strength(password):
    """Оценивает надежность пароля по 5-балльной шкале."""
    score = 0
    feedback = []

    # 1. Проверка длины
    if len(password) >= 12:
        score += 1
    else:
        feedback.append("• Слишком короткий (рекомендуется от 12 символов)")

    # 2. Проверка строчных букв
    if any(char in string.ascii_lowercase for char in password):
        score += 1
    else:
        feedback.append("• Добавьте строчные буквы (a-z)")

    # 3. Проверка прописных букв
    if any(char in string.ascii_uppercase for char in password):
        score += 1
    else:
        feedback.append("• Добавьте заглавные буквы (A-Z)")

    # 4. Проверка цифр
    if any(char in string.digits for char in password):
        score += 1
    else:
        feedback.append("• Добавьте цифры (0-9)")

    # 5. Проверка спецсимволов
    if any(char in string.punctuation for char in password):
        score += 1
    else:
        feedback.append("• Добавьте специальные знаки (например, @, #, $)")

    return score, feedback

def generate_password():
    print("--- Настройка генератора паролей ---")
    
    # Запрашиваем длину
    while True:
        try:
            length = int(input("Введите желаемую длину пароля: "))
            if length < 4:
                print("Пароль должен быть не менее 4 символов.")
                continue
            break
        except ValueError:
            print("Ошибка! Введите целое число.")
    
    # Настройки состава
    include_digits = input("Включать цифры? (да/нет): ").strip().lower() == 'да'
    include_special = input("Включать спецсимволы? (да/нет): ").strip().lower() == 'да'
    
    all_characters = string.ascii_letters
    if include_digits:
        all_characters += string.digits
    if include_special:
        all_characters += string.punctuation
        
    # Генерация
    password_list = [secrets.choice(all_characters) for _ in range(length)]
    final_password = "".join(password_list)
    
    return final_password

# Запуск программы
if __name__ == "__main__":
    password = generate_password()
    
    print("\n" + "="*30)
    print(f"Ваш пароль: {password}")
    print("="*30)
    
    # Запускаем проверку безопасности
    score, tips = check_password_strength(password)
    
    # Выводим вердикт
    print(f"Надежность пароля: {score}/5")
    
    if score == 5:
        print("🟢 Отличный и очень надежный пароль!")
    elif score >= 3:
        print("🟡 Средняя надежность. Можно использовать, но лучше улучшить.")
    else:
        print("🔴 Слабый пароль! Использовать небезопасно.")
        
    # Выводим советы, если они есть
    if tips:
        print("\nРекомендации по улучшению:")
        for tip in tips:
            print(tip)
