
import tkinter as tk
from tkinter import messagebox
import urllib.request
import json
from pathlib import Path

SAVE_FOLDER = Path("saved_objects")


def get_object():
    object_id = entry_id.get().strip()

    if not object_id.isdigit() or not 1 <= int(object_id) <= 100:
        messagebox.showerror("Ошибка", "Введите ID от 1 до 100.")
        return

    url = f"https://jsonplaceholder.typicode.com/posts/{object_id}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        result_text.delete("1.0", tk.END)
        result_text.insert(
            tk.END,
            json.dumps(data, indent=4, ensure_ascii=False)
        )

    except Exception as error:
        messagebox.showerror("Ошибка запроса", str(error))


def save_object():
    content = result_text.get("1.0", tk.END).strip()

    if not content:
        messagebox.showwarning("Внимание", "Сначала получите объект.")
        return

    try:
        data = json.loads(content)
        SAVE_FOLDER.mkdir(parents=True, exist_ok=True)
        file_path = SAVE_FOLDER / f"post_{data['id']}.json"

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        messagebox.showinfo(
            "Успешно",
            f"Файл сохранён:\n{file_path.resolve()}"
        )

    except Exception as error:
        messagebox.showerror("Ошибка сохранения", str(error))


root = tk.Tk()
root.title("JSONPlaceholder Viewer")
root.geometry("650x520")
root.minsize(500, 400)
root.configure(bg="#202938")

title = tk.Label(
    root,
    text="JSONPlaceholder Viewer",
    font=("Arial", 20, "bold"),
    bg="#202938",
    fg="white"
)
title.pack(pady=(20, 5))

subtitle = tk.Label(
    root,
    text="Получение объектов через REST API",
    bg="#202938",
    fg="#cbd5e1"
)
subtitle.pack(pady=(0, 20))

input_frame = tk.Frame(root, bg="#202938")
input_frame.pack(fill="x", padx=25)

tk.Label(
    input_frame,
    text="ID объекта (1–100):",
    font=("Arial", 11),
    bg="#202938",
    fg="white"
).pack(side="left", padx=(0, 10))

entry_id = tk.Entry(input_frame, font=("Arial", 12), width=10)
entry_id.pack(side="left", padx=(0, 10))
entry_id.insert(0, "1")

tk.Button(
    input_frame,
    text="Получить",
    command=get_object,
    bg="#2563eb",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=12,
    pady=6
).pack(side="left")

tk.Label(
    root,
    text="Результат запроса:",
    font=("Arial", 12, "bold"),
    bg="#202938",
    fg="white"
).pack(anchor="w", padx=25, pady=(20, 8))

result_text = tk.Text(
    root,
    font=("Consolas", 11),
    bg="#111827",
    fg="#86efac",
    insertbackground="white",
    relief="flat",
    wrap="word",
    padx=12,
    pady=12
)
result_text.pack(fill="both", expand=True, padx=25, pady=(0, 15))

tk.Button(
    root,
    text="Сохранить в файл",
    command=save_object,
    bg="#16a34a",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    padx=15,
    pady=8
).pack(pady=(0, 20))

root.mainloop()
