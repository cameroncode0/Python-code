import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import socket
import re
import threading
import os
from datetime import datetime
import webbrowser
from tkinter import font as tkfont

class ModernNetworkScanner:
    def __init__(self, root):
        self.root = root
        self.setup_colors()
        self.setup_window()
        self.create_widgets()
        self.setup_styles()
        self.last_scan_time = None

    def setup_colors(self):
        """Modern color palette"""
        self.primary_color = "#3498db"
        self.secondary_color = "#2ecc71"
        self.danger_color = "#e74c3c"
        self.dark_color = "#2c3e50"
        self.light_color = "#ecf0f1"
        self.bg_color = "#f9f9f9"

    def setup_window(self):
        """Window configuration"""
        self.root.title("Network Ninja Pro")
        self.root.geometry("1100x750")
        self.root.minsize(900, 650)
        self.root.configure(bg=self.bg_color)
        
        # Set window icon if available
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass

    def setup_styles(self):
        """Custom styling for widgets"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, 
                           font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', 
                           background=self.dark_color, 
                           foreground='white',
                           font=('Segoe UI', 14, 'bold'),
                           padding=10)
        self.style.configure('Primary.TButton',
                           background=self.primary_color,
                           foreground='white',
                           font=('Segoe UI', 10, 'bold'),
                           borderwidth=0)
        self.style.map('Primary.TButton',
                      background=[('active', '#2980b9')])
        
        # Custom treeview style
        self.style.configure('Treeview',
                           font=('Segoe UI', 9),
                           rowheight=28,
                           background=self.light_color,
                           fieldbackground=self.light_color)
        self.style.configure('Treeview.Heading',
                           font=('Segoe UI', 10, 'bold'),
                           background=self.dark_color,
                           foreground='white')
        self.style.map('Treeview',
                      background=[('selected', self.primary_color)])

    def create_widgets(self):
        """Create all GUI components"""
        self.create_header()
        self.create_control_panel()
        self.create_results_panel()
        self.create_status_bar()

    def create_header(self):
        """Application header"""
        header_frame = ttk.Frame(self.root, style='Header.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title with icon
        title_font = tkfont.Font(family='Segoe UI', size=16, weight='bold')
        title_label = tk.Label(header_frame,
                             text="⚡ Network Ninja Pro",
                             font=title_font,
                             bg=self.dark_color,
                             fg='white')
        title_label.pack(side=tk.LEFT, padx=15)
        
        # Version label
        version_label = ttk.Label(header_frame,
                                text="v2.0",
                                style='Header.TLabel')
        version_label.pack(side=tk.RIGHT, padx=15)

    def create_control_panel(self):
        """Scan control panel"""
        control_frame = ttk.Frame(self.root, padding=(15, 10))
        control_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # IP Range Entry
        ip_frame = ttk.Frame(control_frame)
        ip_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(ip_frame, text="Network Range:").pack(side=tk.LEFT)
        self.ip_range = tk.StringVar(value=self.get_default_ip_range())
        ip_entry = ttk.Entry(ip_frame,
                            textvariable=self.ip_range,
                            font=('Segoe UI', 10),
                            width=25)
        ip_entry.pack(side=tk.LEFT, padx=10)
        
        # Action Buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        self.scan_btn = ttk.Button(btn_frame,
                                  text="Start Scan",
                                  style='Primary.TButton',
                                  command=self.start_scan_thread)
        self.scan_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = ttk.Button(btn_frame,
                               text="Export CSV",
                               command=self.export_results)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # Stats Panel
        stats_frame = ttk.LabelFrame(control_frame,
                                   text=" Network Stats ",
                                   padding=10)
        stats_frame.pack(side=tk.RIGHT, padx=20)
        
        stats = [
            ("Devices", "total", None),
            ("Online", "online", self.secondary_color),
            ("Offline", "offline", self.danger_color)
        ]
        
        for text, key, color in stats:
            frame = ttk.Frame(stats_frame)
            frame.pack(side=tk.LEFT, padx=10)
            
            ttk.Label(frame, text=text+":", font=('Segoe UI', 9)).pack()
            self.stats_labels[key] = ttk.Label(frame,
                                             text="0",
                                             font=('Segoe UI', 10, 'bold'),
                                             foreground=color)
            self.stats_labels[key].pack()

    def create_results_panel(self):
        """Results display area"""
        results_frame = ttk.Frame(self.root)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Treeview with scrollbars
        tree_scroll_y = ttk.Scrollbar(results_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree = ttk.Treeview(
            results_frame,
            columns=("ip", "mac", "vendor", "hostname", "status", "last_seen"),
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            selectmode="extended",
            style='Treeview'
        )
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Configure columns
        columns = [
            ("IP Address", 150),
            ("MAC Address", 150),
            ("Vendor", 200),
            ("Hostname", 200),
            ("Status", 100),
            ("Last Seen", 150)
        ]
        
        for col, width in columns:
            self.tree.heading(col.lower().replace(" ", "_"), text=col)
            self.tree.column(col.lower().replace(" ", "_"), 
                            width=width, 
                            anchor=tk.CENTER)
        
        # Add right-click menu
        self.setup_context_menu()

    def create_status_bar(self):
        """Status bar at bottom"""
        self.status_frame = ttk.Frame(self.root, relief=tk.SUNKEN)
        self.status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.status_var = tk.StringVar(value="Ready to scan network...")
        status_label = ttk.Label(self.status_frame,
                               textvariable=self.status_var,
                               anchor=tk.W,
                               font=('Segoe UI', 9))
        status_label.pack(fill=tk.X, padx=5)
        
        # Add scan time indicator
        self.scan_time_var = tk.StringVar()
        ttk.Label(self.status_frame,
                 textvariable=self.scan_time_var,
                 anchor=tk.E,
                 font=('Segoe UI', 9)).pack(side=tk.RIGHT, padx=5)

    def setup_context_menu(self):
        """Right-click context menu"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(
            label="Copy IP",
            command=self.copy_selected_ip
        )
        self.context_menu.add_command(
            label="Ping Device",
            command=self.ping_selected
        )
        self.context_menu.add_command(
            label="Open in Browser",
            command=self.open_in_browser
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="Refresh Scan",
            command=self.start_scan_thread
        )
        
        self.tree.bind("<Button-3>", self.show_context_menu)

    # ... [Include all your existing network scanning methods here] ...

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernNetworkScanner(root)
    root.mainloop()
