import tkinter as tk
from tkinter import messagebox, ttk


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)
        return item

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from an empty stack")
        return self.items[-1]

    def size(self):
        return len(self.items)

    def get_items(self):
        return self.items.copy()


class StackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Stack Operations")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Configure style
        self.root.configure(bg='#2c3e50')
        
        # Create stack object
        self.stack = Stack()
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="📚 Stack Operations",
            font=("Arial", 24, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=10)
        
        # Input Frame
        input_frame = tk.Frame(self.root, bg='#2c3e50')
        input_frame.pack(pady=10)
        
        tk.Label(
            input_frame,
            text="Enter value:",
            font=("Arial", 12),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(side=tk.LEFT, padx=5)
        
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            input_frame,
            textvariable=self.entry_var,
            font=("Arial", 12),
            width=20,
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#ecf0f1'
        )
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind('<Return>', lambda e: self.push_operation())
        
        # Buttons Frame
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        # Create buttons with different colors
        buttons = [
            ("Push", self.push_operation, '#27ae60'),
            ("Pop", self.pop_operation, '#e74c3c'),
            ("Peek", self.peek_operation, '#3498db'),
            ("Check Empty", self.check_empty, '#f39c12'),
            ("Get Size", self.get_size, '#9b59b6'),
            ("Clear All", self.clear_all, '#e67e22')
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 11, "bold"),
                bg=color,
                fg='white',
                padx=15,
                pady=8,
                relief=tk.RAISED,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Display Frame for Stack Visualization
        display_frame = tk.Frame(self.root, bg='#34495e', relief=tk.GROOVE, bd=3)
        display_frame.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)
        
        # Stack display label
        self.stack_label = tk.Label(
            display_frame,
            text="Stack is empty",
            font=("Courier New", 14),
            bg='#34495e',
            fg='#ecf0f1',
            wraplength=500
        )
        self.stack_label.pack(pady=30, padx=20)
        
        # Status Bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 10, "italic"),
            bg='#2c3e50',
            fg='#95a5a6',
            relief=tk.SUNKEN,
            anchor=tk.W,
            padx=10
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Info Frame
        info_frame = tk.Frame(self.root, bg='#2c3e50')
        info_frame.pack(pady=5)
        
        self.info_label = tk.Label(
            info_frame,
            text="",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        self.info_label.pack()
        
        # Update display
        self.update_display()
    
    def update_display(self):
        """Update the stack visualization"""
        if self.stack.is_empty():
            self.stack_label.config(text="📭 Stack is empty")
        else:
            items = self.stack.get_items()
            # Display with arrows showing LIFO order
            display_text = " ↓ ".join(reversed([str(item) for item in items]))
            self.stack_label.config(
                text=f"Top → {display_text}",
                font=("Courier New", 14, "bold")
            )
        
        # Update info
        self.info_label.config(text=f"Size: {self.stack.size()}")
    
    def set_status(self, message, color='#95a5a6'):
        """Update status bar with colored message"""
        self.status_bar.config(text=message, fg=color)
        self.root.after(3000, lambda: self.status_bar.config(text="Ready", fg='#95a5a6'))
    
    def push_operation(self):
        """Push item onto stack"""
        value = self.entry_var.get().strip()
        if not value:
            messagebox.showwarning("Input Error", "Please enter a value to push!")
            return
        
        try:
            # Try to convert to number if possible for display
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                # Keep as string if not a number
                pass
            
            self.stack.push(value)
            self.update_display()
            self.set_status(f"✅ Pushed '{value}' onto the stack", '#27ae60')
            self.entry_var.set("")
            self.entry.focus()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def pop_operation(self):
        """Pop item from stack"""
        try:
            item = self.stack.pop()
            self.update_display()
            self.set_status(f"🗑️ Popped '{item}' from the stack", '#e74c3c')
        except IndexError as e:
            messagebox.showwarning("Empty Stack", str(e))
    
    def peek_operation(self):
        """Peek at top item"""
        try:
            item = self.stack.peek()
            messagebox.showinfo("Peek", f"Top item: {item}")
            self.set_status(f"👀 Peeked at '{item}'", '#3498db')
        except IndexError as e:
            messagebox.showwarning("Empty Stack", str(e))
    
    def check_empty(self):
        """Check if stack is empty"""
        is_empty = self.stack.is_empty()
        if is_empty:
            messagebox.showinfo("Empty Check", "✅ Stack is empty")
            self.set_status("Stack is empty", '#f39c12')
        else:
            messagebox.showinfo("Empty Check", f"❌ Stack is not empty (Size: {self.stack.size()})")
            self.set_status(f"Stack is not empty (Size: {self.stack.size()})", '#f39c12')
    
    def get_size(self):
        """Get stack size"""
        size = self.stack.size()
        messagebox.showinfo("Stack Size", f"Stack size: {size}")
        self.set_status(f"Stack size: {size}", '#9b59b6')
    
    def clear_all(self):
        """Clear all items from stack"""
        if self.stack.is_empty():
            messagebox.showwarning("Empty Stack", "Stack is already empty!")
            return
        
        if messagebox.askyesno("Clear Stack", "Are you sure you want to clear the entire stack?"):
            self.stack.items.clear()
            self.update_display()
            self.set_status("🗑️ Stack cleared", '#e67e22')


def main():
    root = tk.Tk()
    app = StackGUI(root)
    
    # Set focus to entry
    app.entry.focus()
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
