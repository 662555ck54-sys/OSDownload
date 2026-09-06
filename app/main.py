import hashlib
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

from catalog import OS_CATALOG


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OS Downloader — Core")
        self.geometry("1040x680")
        self.minsize(860, 560)

        self.search = tk.StringVar()
        self.category = tk.StringVar(value="All")
        self.status = tk.StringVar(value="Ready")

        self._build()
        self.refresh()

    def _build(self):
        header = ttk.Frame(self, padding=16)
        header.pack(fill="x")

        ttk.Label(header, text="OS Downloader", font=("TkDefaultFont", 22, "bold")).pack(anchor="w")
        ttk.Label(
            header,
            text="Core • Free • Python-first • Official, legacy, and experimental OS catalog",
        ).pack(anchor="w", pady=(3, 12))

        controls = ttk.Frame(header)
        controls.pack(fill="x")

        ttk.Label(controls, text="Search").pack(side="left")
        search = ttk.Entry(controls, textvariable=self.search)
        search.pack(side="left", fill="x", expand=True, padx=(8, 14))
        search.bind("<KeyRelease>", lambda _: self.refresh())

        ttk.Label(controls, text="Section").pack(side="left")
        sections = ["All"] + sorted({x["category"] for x in OS_CATALOG})
        combo = ttk.Combobox(controls, textvariable=self.category, values=sections, state="readonly", width=24)
        combo.pack(side="left", padx=8)
        combo.bind("<<ComboboxSelected>>", lambda _: self.refresh())

        main = ttk.Frame(self, padding=(16, 0, 16, 12))
        main.pack(fill="both", expand=True)

        cols = ("name", "category", "type", "versions", "editions", "arch")
        self.tree = ttk.Treeview(main, columns=cols, show="headings")
        labels = {
            "name": "Operating System",
            "category": "Section",
            "type": "Type",
            "versions": "Version",
            "editions": "Editions",
            "arch": "Architecture",
        }
        widths = {"name": 150, "category": 170, "type": 175, "versions": 145, "editions": 250, "arch": 180}
        for c in cols:
            self.tree.heading(c, text=labels[c])
            self.tree.column(c, width=widths[c], anchor="w")

        y = ttk.Scrollbar(main, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        y.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", lambda _: self.open_source())

        bar = ttk.Frame(self, padding=(16, 0, 16, 16))
        bar.pack(fill="x")
        ttk.Button(bar, text="Open Source / Download", command=self.open_source).pack(side="left")
        ttk.Button(bar, text="Details", command=self.details).pack(side="left", padx=8)
        ttk.Button(bar, text="SHA-256 Verify", command=self.verify_hash).pack(side="left")
        ttk.Label(bar, textvariable=self.status).pack(side="right")

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        term = self.search.get().strip().lower()
        section = self.category.get()
        shown = 0

        for item in OS_CATALOG:
            haystack = " ".join(str(v) for v in item.values()).lower()
            if term and term not in haystack:
                continue
            if section != "All" and item["category"] != section:
                continue

            self.tree.insert(
                "", "end", iid=item["name"],
                values=(item["name"], item["category"], item["type"],
                        item["versions"], item["editions"], item["arch"])
            )
            shown += 1

        self.status.set(f"{shown} OS entries")

    def selected(self):
        ids = self.tree.selection()
        if not ids:
            messagebox.showinfo("Choose an OS", "Select an operating system first.")
            return None
        name = ids[0]
        return next((x for x in OS_CATALOG if x["name"] == name), None)

    def open_source(self):
        item = self.selected()
        if not item:
            return
        webbrowser.open(item["url"])
        self.status.set(f"Opened source for {item['name']}")

    def details(self):
        item = self.selected()
        if not item:
            return
        
        messagebox.showinfo(
            item["name"],
            f"Section: {item['category']}\n"
            f"Type: {item['type']}\n"
            f"Versions: {item['versions']}\n"
            f"Editions: {item['editions']}\n"
            f"Architecture: {item['arch']}\n\n"
            f"Source: {item['url']}"
        )

    def verify_hash(self):
        path = filedialog.askopenfilename(
            title="Choose an ISO/image to hash",
            filetypes=[("Disk images", "*.iso *.img *.zip *.xz *.gz"), ("All files", "*.*")]
        )
        if not path:
            return

        self.status.set("Calculating SHA-256 checksum...")

        def _compute():
            digest = hashlib.sha256()
            try:
                with open(path, "rb") as f:
                    while chunk := f.read(1024 * 1024):
                        digest.update(chunk)
            except OSError as exc:
                self.after(0, lambda: messagebox.showerror("Verification error", str(exc)))
                self.after(0, lambda: self.status.set("Ready"))
                return

            value = digest.hexdigest()
            
            def _done():
                self.clipboard_clear()
                self.clipboard_append(value)
                self.status.set("SHA-256 complete (copied to clipboard)")
                messagebox.showinfo(
                    "SHA-256",
                    f"SHA-256 for:\n{os.path.basename(path)}\n\n{value}\n\n"
                    "The hash was copied to your clipboard. Compare it with the publisher's official checksum."
                )

            self.after(0, _done)

        threading.Thread(target=_compute, daemon=True).start()


if __name__ == "__main__":
    App().mainloop()