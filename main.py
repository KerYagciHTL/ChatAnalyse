import re
from collections import Counter
import matplotlib.pyplot as plt

file_path = "_chat.txt"
with open(file_path, "r", encoding="utf-8") as file:
    chat_lines = file.readlines()

user_last_message = {}
def parse_chat(lines):
    user_messages = {}
    for line in lines:
        match = re.match(r"\[(\d{2}\.\d{2}\.\d{2}), \d{2}:\d{2}:\d{2}\] (.*?): (.+)", line)
        if match:
            date = match.group(1).strip()
            user = match.group(2).strip()
            message = match.group(3).strip()
            user_last_message[user] = date
            if user not in user_messages:
                user_messages[user] = []
            user_messages[user].append(message)
    return user_messages

user_messages = parse_chat(chat_lines)

user_word_counts = {}
user_top_words = {}
for user, messages in user_messages.items():
    all_words = []
    for message in messages:
        words = re.findall(r"\w+", message.lower())
        all_words.extend(words)
    word_counter = Counter(all_words)
    user_word_counts[user] = sum(word_counter.values())
    user_top_words[user] = word_counter.most_common(5)

def create_pie_chart(data, title):
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
    labels = [f"{user} ({count})" for user, count in sorted_data.items()]
    sizes = list(sorted_data.values())
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')
    plt.show()

create_pie_chart(user_word_counts, "Anzahl der Wörter pro Benutzer (absteigend)")
ranked_users = sorted(user_word_counts.items(), key=lambda x: x[1], reverse=True)

print("Ranking der Benutzer:")
for idx, (user, count) in enumerate(ranked_users, start=1):
    last_message_date = user_last_message.get(user, "Keine Daten")
    print(f"Nr{idx}: {user} ({count} Wörter, zuletzt geschrieben: {last_message_date})")
    print("Top 5 Wörter:")
    for word, freq in user_top_words[user]:
        print(f"{word} : {freq}")
    print()
