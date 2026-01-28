import customtkinter as ctk
import threading
from tkinter import messagebox, filedialog
from .crawler import RobustCrawler

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ecommerce Product Crawler V2")
        self.geometry("900x600")
        
        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header
        self.header = ctk.CTkLabel(self, text="🛍️ Product Crawler Pro", font=ctk.CTkFont(size=20, weight="bold"))
        self.header.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        # Controls Frame
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        # URL Input
        self.url_label = ctk.CTkLabel(self.controls_frame, text="Start URL:")
        self.url_label.grid(row=0, column=0, padx=10, pady=10)
        self.url_entry = ctk.CTkEntry(self.controls_frame, width=400, placeholder_text="https://example.com/shop")
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        # Depth
        self.depth_label = ctk.CTkLabel(self.controls_frame, text="Max Depth:")
        self.depth_label.grid(row=0, column=2, padx=10, pady=10)
        self.depth_var = ctk.StringVar(value="2")
        self.depth_entry = ctk.CTkEntry(self.controls_frame, width=50, textvariable=self.depth_var)
        self.depth_entry.grid(row=0, column=3, padx=10, pady=10)

        # Buttons
        self.start_btn = ctk.CTkButton(self.controls_frame, text="Start Crawling", command=self.start_crawling, fg_color="green")
        self.start_btn.grid(row=0, column=4, padx=10, pady=10)
        
        self.stop_btn = ctk.CTkButton(self.controls_frame, text="Stop", command=self.stop_crawling, state="disabled", fg_color="red")
        self.stop_btn.grid(row=0, column=5, padx=10, pady=10)

        self.export_btn = ctk.CTkButton(self.controls_frame, text="Export Data", command=self.export_data, state="disabled")
        self.export_btn.grid(row=0, column=6, padx=10, pady=10)

        # Console/Log
        self.console = ctk.CTkTextbox(self, width=880, height=350)
        self.console.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.console.insert("0.0", "--- Ready to Crawl ---\n")

        # Status Bar
        self.status = ctk.CTkLabel(self, text="Status: Idle | Products Found: 0", anchor="w")
        self.status.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.crawler = None
        self.crawl_thread = None

    def log(self, message):
        self.console.insert("end", message + "\n")
        self.console.see("end")

    def update_callback(self, type, data):
        if type == 'status':
            self.status.configure(text=f"Status: {data} | Products: {self.crawler.stats['products_found']}")
        elif type == 'data':
            self.log(f"[FOUND] {data.get('product_name', 'Unknown')} - {data.get('price', 'N/A')}")
        elif type == 'done':
            self.stop_crawling_ui()
            self.log(f"\n--- DONE ---\nItems: {data['products_found']} | Scanned: {data['scanned']} | Errors: {data['errors']}")
            messagebox.showinfo("Finished", f"Crawl finished. Found {data['products_found']} products.")

    def start_crawling(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a valid URL")
            return

        try:
            depth = int(self.depth_entry.get())
        except ValueError:
            messagebox.showwarning("Input Error", "Depth must be a number")
            return

        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.export_btn.configure(state="disabled")
        self.console.delete("1.0", "end")
        self.log(f"Starting crawl on {url} (Depth: {depth})...")

        self.crawler = RobustCrawler(url, depth, callback=self.update_callback)
        self.crawl_thread = threading.Thread(target=self.crawler.start, daemon=True)
        self.crawl_thread.start()

    def stop_crawling(self):
        if self.crawler:
            self.crawler.stop()
            self.log("Stopping...")

    def stop_crawling_ui(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        if self.crawler and self.crawler.results:
            self.export_btn.configure(state="normal")

    def export_data(self):
        if not self.crawler or not self.crawler.results:
            return

        format_choice = ctk.CTkInputDialog(text="Format (csv/json/xlsx):", title="Export").get_input()
        if format_choice and format_choice.lower() in ['csv', 'json', 'xlsx']:
            success, msg = self.crawler.export_data(format_choice.lower())
            if success:
                messagebox.showinfo("Export Success", f"Saved to {msg}")
                self.log(f"Data exported to {msg}")
            else:
                messagebox.showerror("Export Failed", msg)
        else:
            messagebox.showwarning("Invalid Format", "Please type csv, json, or xlsx")

def run_app():
    app = App()
    app.mainloop()
