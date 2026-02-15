import tkinter as tk
from tkinter.filedialog import *

def encrypt(text: str, key: str) -> str:
    newText = ""
    key = key.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65 # 65 is based on ASCII values

            if char.isupper():
                newText += chr((ord(char) + shift - 65) % 26 + 65) # wrapping around 26, then convert to ASCII values
            else:
                newText += chr((ord(char) + shift - 97) % 26 + 97) # ASCII value for "a" is 97

            key_index += 1
        else:
            newText += char

    return newText


def decrypt(text: str, key: str) -> str:
    originalText = ""
    key = key.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65

            if char.isupper():
                originalText += chr((ord(char) - shift - 65) % 26 + 65)
            else:
                originalText += chr((ord(char) - shift - 97) % 26 + 97)

            key_index += 1
        else:
            originalText += char

    return originalText


def save_file(window, text_edit, key_edit):
    key = key_edit.get()
    if key is None or key == "enter your key here":
        message = tk.Label(window, text="Enter your encryption key here")
        message.grid(column=0, row=0, )
        return
    file = asksaveasfilename(filetypes=[("Text Files", "*.txt")])

    if file is None:
        return

    with open(file, 'w') as f:
        content = text_edit.get("1.0", tk.END)
        encrypted = encrypt(content, key)
        f.write(encrypted)

    window.title(f"Saved to {file}")


def open_file(window, text_edit, key_edit):
    file = askopenfile(filetypes=[("Text Files", "*.txt")])
    key = key_edit.get()

    if key is None or key == "enter your key here":
        print("No key provided")
        return

    if file is None:
        return

    text_edit.delete(1.0, tk.END)
    with open(file.name, 'r') as f:
        content = f.read()
        decrypted = decrypt(content, key)
        text_edit.insert(tk.END, decrypted)

    window.title(f"Open file:{file}")


def clear_placeholder(entry):
    if entry.get() == "enter your key here":
        entry.delete(0, tk.END)

def add_placeholder(entry):
    if entry.get() == "":
        entry.insert(0, "enter your key here")


def main():
    # windows setup
    window = tk.Tk()
    window.title("Cipher")
    window.rowconfigure(0, minsize = 400)
    window.columnconfigure(1, minsize = 300)

    text_edit = tk.Text(window, font=("Helvetica", 20))
    text_edit.grid(row=0, column=1)
    frame = tk.Frame(window, relief = tk.FLAT, bd = 5)

    # save and open buttons setup
    save_button = tk.Button(frame, text = "Save", command = lambda: save_file(window, text_edit, encryption_key))
    open_button = tk.Button(frame, text = "Open", command = lambda: open_file(window, text_edit, encryption_key))

    save_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
    open_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

    # encryption key field setup
    encryption_key = tk.Entry(frame, width = 20)
    encryption_key.insert(0, "enter your key here")
    encryption_key.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
    encryption_key.bind("<FocusIn>", lambda e: clear_placeholder(encryption_key))
    encryption_key.bind("<FocusOut>", lambda e: add_placeholder(encryption_key))

    frame.grid(row=0, column=0, sticky="ns")

    window.bind("<Command-s>", lambda e: save_file(window, text_edit))
    window.bind("<Command-o>", lambda e: open_file(window, text_edit))

    window.mainloop()




if __name__ == "__main__":
    main()