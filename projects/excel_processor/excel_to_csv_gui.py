import pandas as pd
import os
import subprocess
import datetime
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk


# === Utility functions ===

def install_package(pkg_name):
    try:
        subprocess.check_call([os.sys.executable, "-m", "pip", "install", pkg_name])
    except Exception as e:
        raise RuntimeError(f"Failed to install {pkg_name}: {e}")


def copy_csv_file_with_suffix(csv_file_path, suffix="_1"):
    folder_path, file_name = os.path.split(csv_file_path)
    name, ext = os.path.splitext(file_name)
    new_file_name = f"{name}{suffix}{ext}"
    new_file_path = os.path.join(folder_path, new_file_name)

    with open(csv_file_path, 'rb') as file_in, open(new_file_path, 'wb') as file_out:
        file_out.write(file_in.read())

    return new_file_path


def move_excel_file(source_file_path, destination_folder_path):
    os.makedirs(destination_folder_path, exist_ok=True)
    t = time.localtime()
    current_time = str(datetime.date.today()) + str(time.strftime(" %H-%M-%S", t))
    _, ext = os.path.splitext(source_file_path)
    file_name = f"{current_time}{ext}"
    destination_path = os.path.join(destination_folder_path, file_name)
    os.rename(source_file_path, destination_path)
    return destination_path


def clean_column(series, rule):
    series = series.astype(str)
    if rule == "Remove 11th character":
        return series.str.slice(0, 10) + series.str.slice(11)
    elif rule == "Trim spaces":
        return series.str.strip()
    elif rule == "Uppercase":
        return series.str.upper()
    elif rule == "Lowercase":
        return series.str.lower()
    elif rule == "Keep only digits":
        return series.str.replace(r"\D", "", regex=True)
    else:
        return series


def apply_rules_to_dataframe(df, column_rules, log_callback=None):
    df_copy = df.copy()
    for col, rule in column_rules.items():
        if col not in df_copy.columns:
            raise ValueError(f"Column '{col}' not found in file.")
        if rule != "No change":
            if log_callback:
                log_callback(f"Applying rule '{rule}' to column '{col}'")
            df_copy[col] = clean_column(df_copy[col], rule)
    return df_copy


def save_csv(df, file_path, log_callback):
    df.to_csv(file_path, index=False)
    log_callback(f"CSV saved: {file_path}")
    csv_copy = copy_csv_file_with_suffix(file_path)
    log_callback(f"CSV copy saved: {csv_copy}")


def archive_excel(file_path, output_dir, log_callback):
    history_dir = os.path.join(output_dir, "History")
    moved_excel = move_excel_file(file_path, history_dir)
    log_callback(f"Excel archived to: {moved_excel}")


# === GUI ===

def run_gui():
    root = tk.Tk()
    root.title("Excel to CSV Processor")
    root.geometry("1200x900")

    selected_file = tk.StringVar()
    output_folder = tk.StringVar()

    rules = [
        "Remove 11th character",
        "Trim spaces",
        "Uppercase",
        "Lowercase",
        "Keep only digits",
        "No change"
    ]

    column_rules_widgets = {}
    df_original = None
    df_cleaned = None
    df_preview = None
    tree = None
    page_size = 20
    current_page = tk.IntVar(value=0)

    log_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=120, state="disabled")
    log_box.pack(padx=10, pady=10)

    preview_frame = tk.Frame(root)
    preview_frame.pack(pady=10, fill="both", expand=True)

    search_var = tk.StringVar()

    def log_callback(message):
        log_box.configure(state="normal")
        log_box.insert(tk.END, message + "\n")
        log_box.configure(state="disabled")
        log_box.see(tk.END)
        root.update()

    def choose_file():
        nonlocal df_original
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            selected_file.set(file_path)
            log_callback(f"Selected Excel file: {file_path}")
            try:
                df_original = pd.read_excel(file_path)
                cols = list(df_original.columns)

                for widget in column_rules_widgets.values():
                    widget.destroy()
                column_rules_widgets.clear()

                frame = tk.Frame(root)
                frame.pack(pady=10)
                tk.Label(frame, text="Assign a rule to each column:").grid(row=0, column=0, columnspan=2)

                for i, col in enumerate(cols, start=1):
                    tk.Label(frame, text=col, width=40, anchor="w").grid(row=i, column=0, padx=5, pady=2)
                    combo = ttk.Combobox(frame, values=rules, state="readonly", width=30)
                    combo.set("No change")
                    combo.grid(row=i, column=1, padx=5, pady=2)
                    column_rules_widgets[col] = combo

                log_callback("Column rules setup ready.")

            except Exception as e:
                log_callback(f"❌ Failed to load columns: {e}")
                messagebox.showerror("Error", f"Could not read Excel columns:\n{e}")

    def choose_output_folder():
        folder_path = filedialog.askdirectory()
        if folder_path:
            output_folder.set(folder_path)
            log_callback(f"Selected output folder: {folder_path}")

    def render_page():
        nonlocal tree, df_preview
        if df_preview is None:
            return
        page = current_page.get()
        start = page * page_size
        end = start + page_size
        df_page = df_preview.iloc[start:end]

        for widget in preview_frame.winfo_children():
            widget.destroy()

        search_frame = tk.Frame(preview_frame)
        search_frame.pack(pady=5)
        tk.Entry(search_frame, textvariable=search_var, width=40).pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=apply_search).pack(side="left", padx=5)
        tk.Button(search_frame, text="Clear Search", command=clear_search).pack(side="left", padx=5)

        tree = ttk.Treeview(preview_frame, columns=list(df_preview.columns), show="headings", height=20)
        for col in df_preview.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        for i, row in df_page.iterrows():
            tree.insert("", "end", iid=i, values=list(row))

        tree.pack(fill="both", expand=True)

        def on_double_click(event):
            item = tree.selection()[0]
            col = tree.identify_column(event.x)
            col_index = int(col.replace("#", "")) - 1
            old_value = tree.set(item, column=df_preview.columns[col_index])

            entry = tk.Entry(preview_frame)
            entry.insert(0, old_value)
            entry.focus()

            def save_edit(event):
                new_value = entry.get()
                tree.set(item, column=df_preview.columns[col_index], value=new_value)
                df_preview.at[int(item), df_preview.columns[col_index]] = new_value
                entry.destroy()

            entry.bind("<Return>", save_edit)
            entry.place(x=event.x_root - root.winfo_rootx(),
                        y=event.y_root - root.winfo_rooty())

        tree.bind("<Double-1>", on_double_click)

        nav_frame = tk.Frame(preview_frame)
        nav_frame.pack(pady=5)

        tk.Button(nav_frame, text="⬅ Previous", command=lambda: change_page(-1)).pack(side="left", padx=5)
        tk.Label(nav_frame, text=f"Page {page+1} of {len(df_preview)//page_size + 1}").pack(side="left", padx=10)
        tk.Button(nav_frame, text="Next ➡", command=lambda: change_page(1)).pack(side="left", padx=5)

    def change_page(delta):
        page = current_page.get() + delta
        max_page = len(df_preview) // page_size
        if 0 <= page <= max_page:
            current_page.set(page)
            render_page()

    def apply_search():
        nonlocal df_preview
        if df_cleaned is None:
            return
        query = search_var.get().strip().lower()
        if not query:
            return
        df_preview = df_cleaned[df_cleaned.astype(str).apply(lambda row: row.str.lower().str.contains(query).any(), axis=1)]
        current_page.set(0)
        render_page()
        log_callback(f"Search applied: '{query}'")

    def clear_search():
        nonlocal df_preview
        if df_cleaned is None:
            return
        df_preview = df_cleaned.copy()
        current_page.set(0)
        render_page()
        log_callback("Search cleared.")

    def preview_data():
        nonlocal df_cleaned, df_preview
        file_path = selected_file.get()
        if not file_path:
            messagebox.showwarning("Missing file", "Please select an Excel file first.")
            return
        if not column_rules_widgets:
            messagebox.showwarning("Missing columns", "Please load columns first.")
            return

        try:
            column_rules = {col: combo.get() for col, combo in column_rules_widgets.items()}
            df_cleaned = apply_rules_to_dataframe(df_original, column_rules, log_callback)
            df_preview = df_cleaned.copy()
            current_page.set(0)
            render_page()
            log_callback("Preview generated with pagination, editing, and search.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview data:\n{e}")
            log_callback(f"❌ Preview error: {e}")

    def export_full_data():
        file_path = selected_file.get()
        folder_path = output_folder.get()
        if not df_cleaned is None:
            try:
                save_csv(df_cleaned, os.path.join(folder_path, "tms_shipments.csv"), log_callback)
                archive_excel(file_path, folder_path, log_callback)
                messagebox.showinfo("Success", "Full dataset exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def export_filtered_data():
        file_path = selected_file.get()
        folder_path = output_folder.get()
        if not df_preview is None:
            try:
                save_csv(df_preview, os.path.join(folder_path, "tms_shipments_filtered.csv"), log_callback)
                archive_excel(file_path, folder_path, log_callback)
                messagebox.showinfo("Success", "Filtered dataset exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    tk.Button(root, text="Select Excel File", command=choose_file, height=2, width=25).pack(pady=5)
    tk.Button(root, text="Select Output Folder", command=choose_output_folder, height=2, width=25).pack(pady=5)
    tk.Button(root, text="Preview & Edit Data", command=preview_data, height=2, width=25).pack(pady=5)

    tk.Button(root, text="Export Full Data", command=export_full_data, height=2, width=25, bg="lightblue").pack(pady=10)
    tk.Button(root, text="Export Filtered Data", command=export_filtered_data, height=2, width=25, bg="lightgreen").pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    run_gui()
