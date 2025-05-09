#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from urllib.parse import urlparse
import requests
import socket
import whois
import pyfiglet
import csv

# --- Global Variables ---
result_data = []

# --- Utility Functions ---
def resolve_ip(url):
    try:
        parsed = urlparse(url)
        return socket.gethostbyname(parsed.netloc)
    except Exception:
        return "N/A"


def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return {
            "registrar": w.registrar or "N/A",
            "creation_date": w.creation_date or "N/A",
            "expiration_date": w.expiration_date or "N/A",
            "updated_date": w.updated_date or "N/A",
            "name_servers": ', '.join(w.name_servers) if isinstance(w.name_servers, list) else w.name_servers or "N/A"
        }
    except Exception as e:
        return {"error": str(e)}


def check_redirects(url):
    redirects = []
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)

        if not response.history:
            ip = resolve_ip(response.url)
            whois_data = get_whois_info(urlparse(response.url).netloc)
            redirects.append({"type": "final", "url": response.url, "ip": ip, "whois": whois_data})
        else:
            for r in response.history:
                ip = resolve_ip(r.url)
                whois_data = get_whois_info(urlparse(r.url).netloc)
                redirects.append({"type": "redirect", "url": r.url, "ip": ip, "whois": whois_data})

            ip = resolve_ip(response.url)
            whois_data = get_whois_info(urlparse(response.url).netloc)
            redirects.append({"type": "final", "url": response.url, "ip": ip, "whois": whois_data})

    except Exception as e:
        return [{"error": str(e)}]
    return redirects


def analyze():
    global result_data

    user_input = url_entry.get().strip()
    if not user_input:
        messagebox.showwarning("Invalid URL", "Please enter a valid URL.")
        return

    # Try HTTPS first, then HTTP if needed
    if not user_input.startswith(('http://', 'https://')):
        url_https = "https://" + user_input
        result = check_redirects(url_https)
        if result and result[0].get("url"):
            result_data = result
            show_results(result)
            return

        url_http = "http://" + user_input
        result = check_redirects(url_http)
        if result and result[0].get("url"):
            result_data = result
            show_results(result)
            return

        messagebox.showerror("Connection Error", "Could not reach the domain using http:// or https://")
    else:
        result = check_redirects(user_input)
        result_data = result
        show_results(result)


def show_results(result):
    output_text.delete(1.0, tk.END)

    if result[0].get("error"):
        output_text.insert(tk.END, f"❌ Error: {result[0]['error']}\n")
        return

    for idx, step in enumerate(result):
        color_tag = step["type"]
        arrow = "🚧" if step["type"] == "redirect" else "🏁"

        output_text.insert(tk.END, f"{arrow} Step {idx + 1} - {step['type'].capitalize()}\n", color_tag)
        output_text.insert(tk.END, f"🌐 URL: {step['url']}\n")
        output_text.insert(tk.END, f"📶 IP Address: {step['ip']}\n")

        whois_data = step.get("whois", {})
        if "error" in whois_data:
            output_text.insert(tk.END, f"📋 WHOIS: ❌ {whois_data['error']}\n")
        else:
            output_text.insert(tk.END, f"📋 WHOIS Info:\n")
            output_text.insert(tk.END, f"   Registrar: {whois_data.get('registrar', 'N/A')}\n")
            output_text.insert(tk.END, f"   Creation Date: {whois_data.get('creation_date', 'N/A')}\n")
            output_text.insert(tk.END, f"   Expiry Date: {whois_data.get('expiration_date', 'N/A')}\n")
            output_text.insert(tk.END, f"   Name Servers: {whois_data.get('name_servers', 'N/A')}\n")

        output_text.insert(tk.END, "-" * 60 + "\n")


def save_results():
    global result_data

    if not result_data:
        messagebox.showwarning("Empty Output", "There is no data to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("CSV File", "*.csv"), ("All Files", "*.*")])
    if not file_path:
        return

    if file_path.endswith(".csv"):
        with open(file_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Step Type", "URL", "IP", "Registrar", "Creation Date", "Expiry Date", "Name Servers"])

            for step in result_data:
                if isinstance(step, dict) and "url" in step:
                    step_type = step.get("type", "").capitalize()
                    url = step.get("url", "")
                    ip = step.get("ip", "")
                    whois_info = step.get("whois", {})
                    registrar = whois_info.get("registrar", "N/A")
                    creation_date = whois_info.get("creation_date", "N/A")
                    expiry_date = whois_info.get("expiration_date", "N/A")
                    name_servers = whois_info.get("name_servers", "N/A")

                    writer.writerow([step_type, url, ip, registrar, creation_date, expiry_date, name_servers])

        messagebox.showinfo("Saved", "Results saved as CSV successfully!")
    else:
        content = output_text.get(1.0, tk.END)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Saved", "Results saved successfully!")


def copy_output():
    root.clipboard_clear()
    root.clipboard_append(output_text.get(1.0, tk.END))
    messagebox.showinfo("Copy", "Output copied to clipboard!")


def paste_url():
    try:
        url_entry.delete(0, tk.END)
        url_entry.insert(tk.END, root.clipboard_get())
    except:
        messagebox.showwarning("Paste", "Nothing to paste from clipboard.")


def clear_all():
    url_entry.delete(0, tk.END)
    output_text.delete(1.0, tk.END)


def bind_copy_paste(widget):
    widget.bind("<Control-c>", lambda e: widget.event_generate("<<Copy>>"))
    widget.bind("<Control-v>", lambda e: widget.event_generate("<<Paste>>"))
    widget.bind("<Control-a>", lambda e: widget.tag_add("sel", "1.0", "end-1c") or widget.mark_set("insert", "end") or widget.see("insert"))


# --- GUI Setup ---
root = tk.Tk()
root.title("Redirect Analyzer")
root.geometry("920x780")
root.configure(bg="#1e1e1e")

# ASCII Banner
ascii_banner = pyfiglet.figlet_format("TASHI", font="big")
ascii_label = tk.Label(root, text=ascii_banner, font=("Courier", 12, "bold"), fg="lime", bg="#1e1e1e", justify="left")
ascii_label.pack(pady=0)

# Powered by label (placed right after banner)
footer_text = tk.Label(root, text="Powered by Roy Merlo 2025", font=("Helvetica", 9, "italic"), fg="#cccccc", bg="#1e1e1e")
footer_text.pack(pady=(2, 10))

# Input Frame
input_frame = ttk.Frame(root)
input_frame.pack(pady=5)

ttk.Label(input_frame, text="Enter URL to analyze:").pack(side=tk.LEFT)

# Paste Button
ttk.Button(input_frame, text="📎 Paste", width=8, command=paste_url).pack(side=tk.RIGHT, padx=(5, 0))

# Clear Button
ttk.Button(input_frame, text="🗑 Clear", width=8, command=clear_all).pack(side=tk.RIGHT, padx=(5, 0))

# URL Entry Field
url_entry = ttk.Entry(input_frame, width=68)
url_entry.pack(side=tk.LEFT, padx=(5, 0))
bind_copy_paste(url_entry)

# Analyze Button
ttk.Button(root, text="🔍 Analyze", command=analyze).pack(pady=5)

# Output Text Area
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 10), bg="#121212", fg="white", insertbackground="white")
output_text.pack(expand=True, fill='both', padx=10, pady=10)
bind_copy_paste(output_text)

# Configure colors for redirect/final
output_text.tag_configure("redirect", foreground="red")
output_text.tag_configure("final", foreground="lime")

# Action Buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=5)

ttk.Button(button_frame, text="📋 Copy", width=10, command=copy_output).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="💾 Save Results", width=12, command=save_results).pack(side=tk.LEFT, padx=5)

# Start GUI
root.mainloop()
