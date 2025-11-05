"""
Data Masking & Anonymization Tool
A comprehensive tool for applying anonymization and masking to sensitive data
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from faker import Faker
from cryptography.fernet import Fernet
import re
import hashlib
import base64

class DataMaskingTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Masking & Anonymization Tool")
        self.root.geometry("1200x800")
        
        # Initialize Faker
        self.faker = Faker()
        
        # Data storage
        self.df = None
        self.masked_df = None
        self.masking_rules = {}
        self.encryption_key = None
        self.reverse_mapping = {}  # For reversible masking
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Menu Bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load CSV", command=self.load_csv)
        file_menu.add_command(label="Load Excel", command=self.load_excel)
        file_menu.add_separator()
        file_menu.add_command(label="Save Masked Data", command=self.save_masked_data)
        file_menu.add_command(label="Export Rules", command=self.export_rules)
        file_menu.add_command(label="Import Rules", command=self.import_rules)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Main container with notebook tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Data Preview
        self.preview_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.preview_tab, text="Data Preview")
        self.setup_preview_tab()
        
        # Tab 2: Masking Rules
        self.rules_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.rules_tab, text="Masking Rules")
        self.setup_rules_tab()
        
        # Tab 3: Processing
        self.process_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.process_tab, text="Processing")
        self.setup_process_tab()
        
        # Tab 4: Results
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text="Results")
        self.setup_results_tab()
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_preview_tab(self):
        """Setup data preview tab"""
        # Control frame
        control_frame = ttk.Frame(self.preview_tab)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Load CSV File", command=self.load_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Load Excel File", command=self.load_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Generate Sample Data", command=self.generate_sample_data).pack(side=tk.LEFT, padx=5)
        
        # Data info frame
        info_frame = ttk.LabelFrame(self.preview_tab, text="Data Information")
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=5, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, padx=5, pady=5)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(self.preview_tab, text="Data Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, wrap=tk.NONE)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def setup_rules_tab(self):
        """Setup masking rules configuration tab"""
        # Left panel - Field selection
        left_frame = ttk.Frame(self.rules_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Select Fields to Mask:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=5)
        
        # Scrollable listbox for fields
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.fields_listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
        self.fields_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.fields_listbox.yview)
        
        # Right panel - Masking options
        right_frame = ttk.LabelFrame(self.rules_tab, text="Masking Configuration")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Masking type selection
        ttk.Label(right_frame, text="Masking Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.masking_type = ttk.Combobox(right_frame, state='readonly', width=30)
        self.masking_type.grid(row=0, column=1, padx=5, pady=5)
        self.masking_type['values'] = [
            'Full Masking (****)',
            'Partial Masking',
            'Format-Preserving Encryption',
            'Fake Data Replacement',
            'Hash (One-way)',
            'Reversible (with key)',
            'Email Masking',
            'Phone Masking',
            'SSN Masking',
            'Date Shifting',
            'Number Randomization'
        ]
        self.masking_type.current(0)
        self.masking_type.bind('<<ComboboxSelected>>', self.on_masking_type_change)
        
        # Additional options frame
        self.options_frame = ttk.Frame(right_frame)
        self.options_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Partial masking options
        self.partial_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.partial_frame, text="Keep first:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.keep_first = ttk.Spinbox(self.partial_frame, from_=0, to=10, width=10)
        self.keep_first.grid(row=0, column=1, padx=5, pady=2)
        self.keep_first.set(0)
        
        ttk.Label(self.partial_frame, text="Keep last:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.keep_last = ttk.Spinbox(self.partial_frame, from_=0, to=10, width=10)
        self.keep_last.grid(row=1, column=1, padx=5, pady=2)
        self.keep_last.set(4)
        
        # Reversible masking key
        self.reversible_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.reversible_frame, text="Encryption Key:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.key_entry = ttk.Entry(self.reversible_frame, width=40, show='*')
        self.key_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(self.reversible_frame, text="Generate Key", command=self.generate_key).grid(row=0, column=2, padx=5, pady=2)
        
        # Date shifting options
        self.date_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.date_frame, text="Shift by days:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.date_shift = ttk.Spinbox(self.date_frame, from_=-365, to=365, width=10)
        self.date_frame.grid_remove()
        self.date_shift.grid(row=0, column=1, padx=5, pady=2)
        self.date_shift.set(30)
        
        # Buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add Rule", command=self.add_masking_rule).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Rule", command=self.remove_masking_rule).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All Rules", command=self.clear_rules).pack(side=tk.LEFT, padx=5)
        
        # Current rules display
        rules_display_frame = ttk.LabelFrame(right_frame, text="Active Masking Rules")
        rules_display_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        
        self.rules_text = scrolledtext.ScrolledText(rules_display_frame, height=15, wrap=tk.WORD)
        self.rules_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def setup_process_tab(self):
        """Setup processing tab"""
        # Processing options
        options_frame = ttk.LabelFrame(self.process_tab, text="Processing Options")
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.batch_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Batch Processing (for large files)", variable=self.batch_var).pack(anchor=tk.W, padx=5, pady=5)
        
        ttk.Label(options_frame, text="Batch Size:").pack(anchor=tk.W, padx=5)
        self.batch_size = ttk.Spinbox(options_frame, from_=100, to=10000, increment=100, width=15)
        self.batch_size.pack(anchor=tk.W, padx=5, pady=5)
        self.batch_size.set(1000)
        
        # Processing button
        ttk.Button(options_frame, text="Apply Masking Rules", command=self.apply_masking, 
                  style='Accent.TButton').pack(pady=10)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(self.process_tab, text="Processing Status")
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        self.process_log = scrolledtext.ScrolledText(progress_frame, height=20, wrap=tk.WORD)
        self.process_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def setup_results_tab(self):
        """Setup results tab"""
        # Control buttons
        control_frame = ttk.Frame(self.results_tab)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Save Masked Data", command=self.save_masked_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Export Reverse Mapping", command=self.export_reverse_mapping).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Compare Original vs Masked", command=self.show_comparison).pack(side=tk.LEFT, padx=5)
        
        # Results display
        results_frame = ttk.LabelFrame(self.results_tab, text="Masked Data Preview")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.NONE)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def log(self, message):
        """Add message to process log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.process_log.insert(tk.END, f"[{timestamp}] {message}\n")
        self.process_log.see(tk.END)
        self.root.update()
        
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.root.update()
        
    def load_csv(self):
        """Load CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.update_data_view()
                self.update_status(f"Loaded: {Path(file_path).name} ({len(self.df)} rows)")
                messagebox.showinfo("Success", f"Loaded {len(self.df)} rows successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV: {str(e)}")
                
    def load_excel(self):
        """Load Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.df = pd.read_excel(file_path)
                self.update_data_view()
                self.update_status(f"Loaded: {Path(file_path).name} ({len(self.df)} rows)")
                messagebox.showinfo("Success", f"Loaded {len(self.df)} rows successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load Excel: {str(e)}")
                
    def generate_sample_data(self):
        """Generate sample data for testing"""
        sample_data = {
            'employee_id': [f'EMP{i:04d}' for i in range(1, 51)],
            'first_name': [self.faker.first_name() for _ in range(50)],
            'last_name': [self.faker.last_name() for _ in range(50)],
            'email': [self.faker.email() for _ in range(50)],
            'phone': [self.faker.phone_number() for _ in range(50)],
            'ssn': [self.faker.ssn() for _ in range(50)],
            'salary': [self.faker.random_int(30000, 150000) for _ in range(50)],
            'date_of_birth': [self.faker.date_of_birth(minimum_age=25, maximum_age=65) for _ in range(50)],
            'address': [self.faker.address() for _ in range(50)]
        }
        self.df = pd.DataFrame(sample_data)
        self.update_data_view()
        self.update_status("Generated 50 rows of sample data")
        messagebox.showinfo("Success", "Sample data generated successfully!")
        
    def update_data_view(self):
        """Update data preview and field list"""
        if self.df is not None:
            # Update info
            info = f"Rows: {len(self.df)}\n"
            info += f"Columns: {len(self.df.columns)}\n"
            info += f"Fields: {', '.join(self.df.columns)}\n"
            info += f"Memory Usage: {self.df.memory_usage(deep=True).sum() / 1024:.2f} KB"
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info)
            
            # Update preview
            preview = self.df.head(20).to_string()
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, preview)
            
            # Update fields listbox
            self.fields_listbox.delete(0, tk.END)
            for col in self.df.columns:
                self.fields_listbox.insert(tk.END, col)
                
    def on_masking_type_change(self, event=None):
        """Handle masking type change"""
        # Hide all option frames
        self.partial_frame.grid_remove()
        self.reversible_frame.grid_remove()
        self.date_frame.grid_remove()
        
        # Show relevant frame
        masking_type = self.masking_type.get()
        if masking_type == 'Partial Masking':
            self.partial_frame.grid(row=0, column=0, sticky=tk.W)
        elif masking_type == 'Reversible (with key)' or masking_type == 'Format-Preserving Encryption':
            self.reversible_frame.grid(row=0, column=0, sticky=tk.W)
        elif masking_type == 'Date Shifting':
            self.date_frame.grid(row=0, column=0, sticky=tk.W)
            
    def generate_key(self):
        """Generate encryption key"""
        key = Fernet.generate_key()
        self.encryption_key = key
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, key.decode())
        messagebox.showinfo("Key Generated", "Encryption key generated. Please save it securely!")
        
    def add_masking_rule(self):
        """Add masking rule for selected fields"""
        selected_indices = self.fields_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one field")
            return
            
        masking_type = self.masking_type.get()
        
        for idx in selected_indices:
            field = self.fields_listbox.get(idx)
            
            rule = {
                'type': masking_type,
                'options': {}
            }
            
            # Add type-specific options
            if masking_type == 'Partial Masking':
                rule['options']['keep_first'] = int(self.keep_first.get())
                rule['options']['keep_last'] = int(self.keep_last.get())
            elif masking_type in ['Reversible (with key)', 'Format-Preserving Encryption']:
                key = self.key_entry.get()
                if not key:
                    messagebox.showwarning("Warning", "Please generate or enter an encryption key")
                    return
                rule['options']['key'] = key
            elif masking_type == 'Date Shifting':
                rule['options']['shift_days'] = int(self.date_shift.get())
                
            self.masking_rules[field] = rule
            
        self.update_rules_display()
        messagebox.showinfo("Success", f"Added masking rules for {len(selected_indices)} field(s)")
        
    def remove_masking_rule(self):
        """Remove masking rule for selected fields"""
        selected_indices = self.fields_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one field")
            return
            
        for idx in selected_indices:
            field = self.fields_listbox.get(idx)
            if field in self.masking_rules:
                del self.masking_rules[field]
                
        self.update_rules_display()
        messagebox.showinfo("Success", "Removed selected masking rules")
        
    def clear_rules(self):
        """Clear all masking rules"""
        if messagebox.askyesno("Confirm", "Clear all masking rules?"):
            self.masking_rules = {}
            self.update_rules_display()
            
    def update_rules_display(self):
        """Update rules display"""
        self.rules_text.delete(1.0, tk.END)
        if not self.masking_rules:
            self.rules_text.insert(1.0, "No masking rules defined")
        else:
            for field, rule in self.masking_rules.items():
                rule_str = f"Field: {field}\n"
                rule_str += f"  Type: {rule['type']}\n"
                if rule['options']:
                    rule_str += f"  Options: {rule['options']}\n"
                rule_str += "\n"
                self.rules_text.insert(tk.END, rule_str)
                
    def apply_masking(self):
        """Apply masking rules to data"""
        if self.df is None:
            messagebox.showwarning("Warning", "Please load data first")
            return
            
        if not self.masking_rules:
            messagebox.showwarning("Warning", "Please define masking rules first")
            return
            
        try:
            self.log("Starting masking process...")
            self.masked_df = self.df.copy()
            total_fields = len(self.masking_rules)
            
            for idx, (field, rule) in enumerate(self.masking_rules.items()):
                self.log(f"Processing field: {field}")
                self.masked_df[field] = self.masked_df[field].apply(
                    lambda x: self.mask_value(x, rule, field)
                )
                self.progress_var.set((idx + 1) / total_fields * 100)
                
            self.log("Masking completed successfully!")
            self.update_results_view()
            self.notebook.select(self.results_tab)
            messagebox.showinfo("Success", "Data masking completed!")
            
        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            messagebox.showerror("Error", f"Masking failed: {str(e)}")
            
    def mask_value(self, value, rule, field_name):
        """Apply masking to a single value"""
        if pd.isna(value):
            return value
            
        masking_type = rule['type']
        options = rule['options']
        value_str = str(value)
        
        if masking_type == 'Full Masking (****)':
            return '*' * len(value_str)
            
        elif masking_type == 'Partial Masking':
            keep_first = options.get('keep_first', 0)
            keep_last = options.get('keep_last', 4)
            if len(value_str) <= keep_first + keep_last:
                return '*' * len(value_str)
            masked = value_str[:keep_first] + '*' * (len(value_str) - keep_first - keep_last) + value_str[-keep_last:]
            return masked
            
        elif masking_type == 'Format-Preserving Encryption':
            key = options.get('key', '').encode()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(value_str.encode())
            # Store reverse mapping
            if field_name not in self.reverse_mapping:
                self.reverse_mapping[field_name] = {}
            encoded = base64.urlsafe_b64encode(encrypted).decode()
            self.reverse_mapping[field_name][encoded] = value_str
            return encoded
            
        elif masking_type == 'Fake Data Replacement':
            # Intelligent fake data based on field name
            lower_field = field_name.lower()
            if 'email' in lower_field:
                return self.faker.email()
            elif 'phone' in lower_field:
                return self.faker.phone_number()
            elif 'name' in lower_field:
                if 'first' in lower_field:
                    return self.faker.first_name()
                elif 'last' in lower_field:
                    return self.faker.last_name()
                return self.faker.name()
            elif 'address' in lower_field:
                return self.faker.address()
            elif 'ssn' in lower_field:
                return self.faker.ssn()
            elif 'company' in lower_field:
                return self.faker.company()
            else:
                return self.faker.word()
                
        elif masking_type == 'Hash (One-way)':
            return hashlib.sha256(value_str.encode()).hexdigest()[:16]
            
        elif masking_type == 'Reversible (with key)':
            key = options.get('key', '').encode()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(value_str.encode())
            # Store reverse mapping
            if field_name not in self.reverse_mapping:
                self.reverse_mapping[field_name] = {}
            encoded = encrypted.decode()
            self.reverse_mapping[field_name][encoded] = value_str
            return encoded
            
        elif masking_type == 'Email Masking':
            if '@' in value_str:
                local, domain = value_str.split('@', 1)
                if len(local) > 2:
                    masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
                else:
                    masked_local = '*' * len(local)
                return f"{masked_local}@{domain}"
            return '*' * len(value_str)
            
        elif masking_type == 'Phone Masking':
            # Keep last 4 digits
            digits = re.sub(r'\D', '', value_str)
            if len(digits) >= 4:
                return '*' * (len(value_str) - 4) + value_str[-4:]
            return '*' * len(value_str)
            
        elif masking_type == 'SSN Masking':
            # Keep last 4 digits
            digits = re.sub(r'\D', '', value_str)
            if len(digits) >= 4:
                return '***-**-' + digits[-4:]
            return '*' * len(value_str)
            
        elif masking_type == 'Date Shifting':
            try:
                shift_days = options.get('shift_days', 30)
                date_value = pd.to_datetime(value)
                shifted = date_value + pd.Timedelta(days=shift_days)
                return shifted.strftime('%Y-%m-%d')
            except:
                return value
                
        elif masking_type == 'Number Randomization':
            try:
                num = float(value)
                # Add random noise (±10%)
                noise = num * 0.1 * (2 * self.faker.random.random() - 1)
                return round(num + noise, 2)
            except:
                return value
                
        return value
        
    def update_results_view(self):
        """Update results display"""
        if self.masked_df is not None:
            preview = self.masked_df.head(20).to_string()
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, preview)
            
    def save_masked_data(self):
        """Save masked data to file"""
        if self.masked_df is None:
            messagebox.showwarning("Warning", "No masked data to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Masked Data",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.masked_df.to_csv(file_path, index=False)
                elif file_path.endswith('.xlsx'):
                    self.masked_df.to_excel(file_path, index=False)
                else:
                    self.masked_df.to_csv(file_path, index=False)
                    
                messagebox.showinfo("Success", f"Masked data saved to {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
                
    def export_rules(self):
        """Export masking rules to JSON"""
        if not self.masking_rules:
            messagebox.showwarning("Warning", "No rules to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Masking Rules",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.masking_rules, f, indent=2)
                messagebox.showinfo("Success", "Rules exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
                
    def import_rules(self):
        """Import masking rules from JSON"""
        file_path = filedialog.askopenfilename(
            title="Import Masking Rules",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    self.masking_rules = json.load(f)
                self.update_rules_display()
                messagebox.showinfo("Success", "Rules imported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {str(e)}")
                
    def export_reverse_mapping(self):
        """Export reverse mapping for reversible masking"""
        if not self.reverse_mapping:
            messagebox.showwarning("Warning", "No reverse mapping available")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Reverse Mapping",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.reverse_mapping, f, indent=2)
                messagebox.showinfo("Success", "Reverse mapping exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
                
    def show_comparison(self):
        """Show side-by-side comparison"""
        if self.df is None or self.masked_df is None:
            messagebox.showwarning("Warning", "Need both original and masked data")
            return
            
        # Create comparison window
        comp_window = tk.Toplevel(self.root)
        comp_window.title("Data Comparison")
        comp_window.geometry("1200x600")
        
        # Original data frame
        orig_frame = ttk.LabelFrame(comp_window, text="Original Data")
        orig_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        orig_text = scrolledtext.ScrolledText(orig_frame, wrap=tk.NONE)
        orig_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        orig_text.insert(1.0, self.df.head(20).to_string())
        
        # Masked data frame
        masked_frame = ttk.LabelFrame(comp_window, text="Masked Data")
        masked_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        masked_text = scrolledtext.ScrolledText(masked_frame, wrap=tk.NONE)
        masked_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        masked_text.insert(1.0, self.masked_df.head(20).to_string())


def main():
    root = tk.Tk()
    app = DataMaskingTool(root)
    root.mainloop()


if __name__ == "__main__":
    main()