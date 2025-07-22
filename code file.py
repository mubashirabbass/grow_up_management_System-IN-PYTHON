import tkinter as tk
from tkinter import CENTER, SOLID, Frame, Label, ttk, messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import hashlib
from PIL import Image, ImageTk
from tkinter import ttk, filedialog
import logging
import os
import pandas as pd
from PIL import Image, ImageDraw, ImageTk
import os
from datetime import timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import letter, landscape
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side
import logging
import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import win32api
import tempfile
import win32print
import win32ui
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class HospitalManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Grow-Up Hospital Management System")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Email configuration
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'Mubashirabbasedu4@gmail.com',  # Replace with your email
            'sender_password': 'rlzfzjdquhfiifsg',  # Replace with your app-specific password
            'admin_email': 'mubashirabbasedu4@gmail.com'  # Replace with the admin's email address
        }
        
        # Initialize the loading screen only once
        self.show_modern_loading_screen()

    def send_email_notification(self, recipient_email, subject, body):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = recipient_email
            msg['Subject'] = subject

            html_message = f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333; background-color: #f4f4f9; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <div style="background-color: #007bff; padding: 20px; text-align: center; border-top-left-radius: 10px; border-top-right-radius: 10px;">
                            <h1 style="color: white; margin: 0;">Grow Up Hospital</h1>
                        </div>
                        <div style="padding: 20px;">
                            <h2 style="color: #007bff;">{subject}</h2>
                            <p style="font-size: 16px; line-height: 1.6;">{body}</p>
                            <hr style="border: 1px solid #e6f0fa;">
                            <p style="font-size: 14px; color: #495057; text-align: center;">
                                Developed by: Mubashir Abbas<br>
                                Contact: support@growuphospital.com
                            </p>
                        </div>
                    </div>
                </body>
            </html>
            """
            msg.attach(MIMEText(html_message, 'html'))

            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['sender_email'], self.email_config['sender_password'])
                server.sendmail(self.email_config['sender_email'], recipient_email, msg.as_string())
            self.logger.info(f"Email sent to {recipient_email}")
        except Exception as e:
            self.logger.error(f"Failed to send email to {recipient_email}: {e}")
            messagebox.showerror("Email Error", f"Failed to send email notification: {e}")


    def show_modern_loading_screen(self):
        # Create loading overlay on main window
        self.loading_frame = tk.Frame(self.root, bg="#2c3e50")
        self.loading_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        try:
            # Load and display heart GIF
            self.heartbeat_frames = []
            heartbeat_gif = Image.open("heart2.gif")
            try:
                while True:
                    frame = heartbeat_gif.copy()
                    frame = frame.resize((120, 120), Image.LANCZOS)  # Slightly smaller heart
                    self.heartbeat_frames.append(ImageTk.PhotoImage(frame))
                    heartbeat_gif.seek(len(self.heartbeat_frames))
            except EOFError:
                pass
            
            self.heartbeat_label = tk.Label(
                self.loading_frame, 
                image=self.heartbeat_frames[0], 
                bg="#2c3e50"
            )
            self.heartbeat_label.pack(pady=(100, 10))  # Reduced top padding
            
            # Loading percentage with modern font
            self.loading_percent = tk.Label(
                self.loading_frame, 
                text="0%", 
                font=("Arial", 24, "bold"), 
                fg="#ecf0f1", 
                bg="#2c3e50"
            )
            self.loading_percent.pack(pady=5)  # Reduced padding
            
            # Add space between percentage and progress bar
            tk.Frame(self.loading_frame, height=10, bg="#2c3e50").pack()
            
            # Stylish loading bar
            style = ttk.Style()
            style.theme_use('clam')
            style.configure("Custom.Horizontal.TProgressbar", 
                        troughcolor='#34495e',
                        background='#3498db',
                        thickness=15)  # Thinner progress bar
            
            self.loading_bar = ttk.Progressbar(
                self.loading_frame, 
                orient="horizontal", 
                length=450,  # Slightly shorter
                mode="determinate",
                style="Custom.Horizontal.TProgressbar"
            )
            self.loading_bar.pack(pady=5)
            
            # Add space between progress bar and message
            tk.Frame(self.loading_frame, height=15, bg="#2c3e50").pack()
            
            # Loading message with more specific status updates
            self.loading_message = tk.Label(
                self.loading_frame, 
                text="Starting system...", 
                font=("Arial", 12), 
                fg="#bdc3c7", 
                bg="#2c3e50"
            )
            self.loading_message.pack(pady=5)
            
            # Secondary loading message for more detail
            self.loading_detail = tk.Label(
                self.loading_frame,
                text="",
                font=("Arial", 10),
                fg="#95a5a6",
                bg="#2c3e50"
            )
            self.loading_detail.pack(pady=5)
            
            # Start the loading animation
            self.loading_progress = 0
            self.animate_loading()
            
        except Exception as e:
            self.logger.error(f"Error loading loading screen assets: {e}")
            # Fallback to simple loading if there's an error
            tk.Label(
                self.loading_frame, 
                text="Loading...", 
                font=("Arial", 24), 
                fg="white", 
                bg="#2c3e50"
            ).pack(expand=True)
            self.root.after(2000, self.show_welcome_animation)

    def animate_loading(self):
        if self.loading_progress < 100:
            self.loading_progress += 1
            self.loading_bar['value'] = self.loading_progress
            self.loading_percent.config(text=f"{self.loading_progress}%")
            
            # Update messages based on progress with more specific tasks
            if self.loading_progress < 15:
                self.loading_message.config(text="Initializing core systems")
                self.loading_detail.config(text="Loading configuration...")
            elif self.loading_progress < 30:
                self.loading_message.config(text="Connecting to database")
                self.loading_detail.config(text="Establishing connection...")
            elif self.loading_progress < 50:
                self.loading_message.config(text="Loading resources")
                self.loading_detail.config(text="Loading interface assets...")
            elif self.loading_progress < 70:
                self.loading_message.config(text="Setting up security")
                self.loading_detail.config(text="Initializing encryption...")
            elif self.loading_progress < 85:
                self.loading_message.config(text="Preparing interface")
                self.loading_detail.config(text="Loading components...")
            else:
                self.loading_message.config(text="Finalizing setup")
                self.loading_detail.config(text="Almost ready...")
            
            # Animate heart at a slightly slower pace
            if self.loading_progress % 2 == 0:  # Only update every 2% progress
                frame_index = (self.loading_progress // 2) % len(self.heartbeat_frames)
                self.heartbeat_label.config(image=self.heartbeat_frames[frame_index])
            
            # Variable speed - slower at start and end, faster in middle
            if self.loading_progress < 20 or self.loading_progress > 80:
                speed = 80  # Slower
            else:
                speed = 40  # Faster
            
            self.root.after(speed, self.animate_loading)
        else:
            self.show_welcome_animation()
        
        def animate_loading(self):
            if self.loading_progress < 100:
                self.loading_progress += 1
                self.loading_bar['value'] = self.loading_progress
                self.loading_percent.config(text=f"{self.loading_progress}%")
                
                # Animate dots in loading message
                self.dot_count = (self.dot_count + 1) % 4
                dots = "." * self.dot_count
                base_text = self.loading_message.cget("text").split(".")[0]
                self.loading_message.config(text=f"{base_text}{dots}")
                
                # Update loading message based on progress
                if self.loading_progress < 30:
                    base_text = "Initializing system"
                elif self.loading_progress < 60:
                    base_text = "Loading database"
                elif self.loading_progress < 90:
                    base_text = "Preparing interface"
                else:
                    base_text = "Finalizing setup"
                
                # Animate heart
                frame_index = (self.loading_progress % len(self.heartbeat_frames))
                self.heartbeat_label.config(image=self.heartbeat_frames[frame_index])
                
                # Variable speed for more natural feel
                speed = 30 + (self.loading_progress % 40)
                self.root.after(speed, self.animate_loading)
            else:
                self.show_welcome_animation()
    
    def show_welcome_animation(self):
        # Clear the loading elements but keep the background
        for widget in self.loading_frame.winfo_children():
            widget.destroy()
        
        # Welcome text that will be animated
        self.welcome_text = ""
        self.welcome_label = tk.Label(
            self.loading_frame,
            text="",
            font=("Arial", 36, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        self.welcome_label.place(relx=0.5, rely=0.4, anchor="center")
        
        # Subtitle label
        self.subtitle_label = tk.Label(
            self.loading_frame,
            text="Hospital Management Portal",
            font=("Arial", 18),
            fg="#bdc3c7",
            bg="#2c3e50"
        )
        self.subtitle_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Full welcome message
        self.full_welcome_message = "Welcome to Grow-Up"
        
        # Start the typing animation
        self.typing_index = 0
        self.animate_welcome_text()
    
    def animate_welcome_text(self):
        if self.typing_index < len(self.full_welcome_message):
            self.welcome_text += self.full_welcome_message[self.typing_index]
            self.welcome_label.config(text=self.welcome_text)
            self.typing_index += 1
            
            # Variable typing speed for more natural feel
            speed = 50 + (self.typing_index % 30)
            self.root.after(speed, self.animate_welcome_text)
        else:
            # After animation completes, transition to main interface
            self.root.after(1000, self.finish_loading)
    
    def finish_loading(self):
        # Remove the loading frame
        self.loading_frame.destroy()
        
        # Initialize the rest of the system
        try:
            self.bg_image = Image.open("Downpic.cc-2378101665.jpg")
            self.bg_image = self.bg_image.resize((1200, 700), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()
        except Exception as e:
            logging.error(f"Error loading background image: {e}")
            self.root.config(bg="#f0f8ff")

        self.main_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        self.db_connection = self.connect_to_database()
        self.current_user_id = None
        self.current_user_type = None
        self.navigation_stack = []
        self.role_photos = {}
        
        # Load hospital GIF but do not animate yet
        try:
            self.gif_frames = []
            self.gif_index = 0
            gif = Image.open("hospital.gif")
            try:
                while True:
                    frame = gif.copy()
                    frame = frame.resize((50, 50), Image.LANCZOS)
                    self.gif_frames.append(ImageTk.PhotoImage(frame))
                    gif.seek(len(self.gif_frames))
            except EOFError:
                pass
            self.gif_label = tk.Label(self.root, image=self.gif_frames[0])
            self.gif_label.place(x=10, y=10)
            self.is_animating = False
        except Exception as e:
            logging.error(f"Error loading hospital GIF: {e}")
            self.gif_label = tk.Label(self.root, text="GIF Error", bg="red", fg="white")
        
        self.show_landing_screen()

    # [Rest of your existing methods remain unchanged...]
    def animate_gif(self):
        if self.is_animating and self.gif_frames:
            self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
            self.gif_label.configure(image=self.gif_frames[self.gif_index])
            self.root.after(100, self.animate_gif)
            
    def show_loading_screen(self, callback):
        # Create a frame with white background
        self.loading_frame = tk.Frame(self.root, bg="white")
        self.loading_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.loading_frame.lift() 
        self.gif_label.lift()  

        self.is_heartbeat_animating = True

        try:
            # Load and animate heartbeat GIF
            self.heartbeat_frames = []
            self.heartbeat_index = 0
            heartbeat_gif = Image.open("heart2.gif")  
            try:
                while True:
                    frame = heartbeat_gif.copy()
                    frame = frame.resize((100, 100), Image.LANCZOS)
                    self.heartbeat_frames.append(ImageTk.PhotoImage(frame))
                    heartbeat_gif.seek(len(self.heartbeat_frames))
            except EOFError:
                pass
            self.heartbeat_label = tk.Label(self.loading_frame, image=self.heartbeat_frames[0], bg="white")
            self.heartbeat_label.place(relx=0.5, rely=0.5, anchor="center")

            def animate_heartbeat():
                if self.is_heartbeat_animating and self.heartbeat_frames:
                    try:
                        self.heartbeat_index = (self.heartbeat_index + 1) % len(self.heartbeat_frames)
                        self.heartbeat_label.configure(image=self.heartbeat_frames[self.heartbeat_index])
                        self.root.update()
                        self.root.after(50, animate_heartbeat)
                        logging.debug(f"Heartbeat GIF frame: {self.heartbeat_index}")
                    except tk.TclError:
                        self.is_heartbeat_animating = False
                        logging.debug("Heartbeat animation stopped due to widget destruction")

            animate_heartbeat()

            def cleanup_and_proceed():
                self.is_heartbeat_animating = False
                self.heartbeat_label.destroy()  
                self.loading_frame.destroy()
                callback()

            self.root.after(1000, cleanup_and_proceed)

        except Exception as e:
            logging.error(f"Error loading heartbeat GIF: {e}")
            self.is_heartbeat_animating = False
            self.root.after(1000, lambda: [self.loading_frame.destroy(), callback()])

  
            
    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Mubashirhec@4",
                database="hospital_management_system",
            )
            return connection
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            return None

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    def show_landing_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        self.gif_label.place_forget()  # Hide GIF
        self.is_animating = True     # Stop GIF animation

        self.current_user_id = None
        self.current_user_type = None
        self.gif_label.lift()

        landing_frame = tk.Frame(self.main_frame, bg="#f0f8ff", padx=50, pady=50)
        landing_frame.pack(expand=True)

        tk.Label(
            landing_frame,
            text="      Login As            ",
            font=("Arial", 24, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        ).pack(pady=(0, 40))

        roles_frame = tk.Frame(landing_frame, bg="#f0f8ff")
        roles_frame.pack()

        roles = [
            ("admin", "admin_logo.png", lambda: self.show_loading_screen(lambda: self.show_login_screen("admin"))),
            ("doctor", "doctor_logo.png", lambda: self.show_loading_screen(lambda: self.show_login_screen("doctor"))),
            ("patient", "patient_logo.png", lambda: self.show_loading_screen(lambda: self.show_login_screen("patient"))),
            ("staff", "staff_logo.png", lambda: self.show_loading_screen(lambda: self.show_login_screen("staff"))),
        ]

        for idx, (role, image_path, command) in enumerate(roles):
            try:
                if not os.path.exists(image_path):
                    logging.error(f"Image file not found: {image_path}")
                    raise FileNotFoundError(f"Image {image_path} not found")
                
                logging.debug(f"Loading image for {role}: {image_path}")
                img = Image.open(image_path)
                img = img.resize((100, 100), Image.LANCZOS)
                img_scaled = img.resize((110, 110), Image.LANCZOS)
                
                self.role_photos[role] = {
                    'normal': ImageTk.PhotoImage(img),
                    'hover': ImageTk.PhotoImage(img_scaled)
                }
                
            except Exception as e:
                logging.error(f"Failed to load image for {role}: {e}")
                self.role_photos[role] = {
                    'normal': ImageTk.PhotoImage(Image.new("RGB", (100, 100), "#cccccc")),
                    'hover': ImageTk.PhotoImage(Image.new("RGB", (110, 110), "#cccccc"))
                }
                tk.Label(
                    landing_frame,
                    text=f"{role.capitalize()} Image Missing",
                    font=("Arial", 10),
                    bg="#f0f8ff",
                    fg="#ff4500"
                ).place(x=150 * idx + 100, y=300)

            img_button = tk.Button(
                roles_frame,
                image=self.role_photos[role]['normal'],
                bg="#f0f8ff",
                borderwidth=0,
                command=command
            )
            img_button.grid(row=0, column=idx, padx=20)

            img_button.bind("<Enter>", lambda event, r=role: self.on_role_hover_enter(event, r))
            img_button.bind("<Leave>", lambda event, r=role: self.on_role_hover_leave(event, r))

            tk.Label(
                roles_frame,
                text=role.capitalize(),
                font=("Arial", 12, "bold"),
                bg="#f0f8ff",
                fg="#34495e"
            ).grid(row=1, column=idx, pady=10)

    def on_role_hover_enter(self, event, role):
        event.widget.config(image=self.role_photos[role]['hover'])

    def on_role_hover_leave(self, event, role):
        event.widget.config(image=self.role_photos[role]['normal'])

    def show_login_screen(self, user_type=""):
        self.gif_label.place_forget()  # Hide GIF
        self.is_animating = False      # Stop GIF animation

        logging.debug(f"Entering show_login_screen with user_type: {user_type}")
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.gif_label.lift()

        login_frame = tk.Frame(self.main_frame, bg="#f0f8ff", padx=50, pady=50)
        login_frame.pack(expand=True)

        tk.Label(
            login_frame,
            text="Login to Your Account",
            font=("Noto Nastaliq Urdu", 20, "bold"),
            bg="#f0f8ff",
        ).grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(login_frame, text="Username:", font=("Arial", 12), bg="#f0f8ff").grid(
            row=1, column=0, pady=5, sticky="e"
        )
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12))
        self.username_entry.grid(row=1, column=1, pady=5, ipadx=20)

        tk.Label(login_frame, text="Password:", font=("Arial", 12), bg="#f0f8ff").grid(
            row=2, column=0, pady=5, sticky="e"
        )
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), show="*")
        self.password_entry.grid(row=2, column=1, pady=5, ipadx=20)

        tk.Label(login_frame, text="User Type:", font=("Arial", 12), bg="#f0f8ff").grid(
            row=3, column=0, pady=5, sticky="e"
        )
        user_types = ["admin", "doctor", "patient", "staff"]
        self.user_type_var = tk.StringVar(value=user_type)
        logging.debug(f"Set user_type_var to: {user_type}")
        self.user_type_dropdown = ttk.Combobox(
            login_frame,
            textvariable=self.user_type_var,
            values=user_types,
            font=("Arial", 12),
            state="readonly"
        )
        self.user_type_dropdown.set(user_type)
        self.user_type_dropdown.grid(row=3, column=1, pady=5, ipadx=20)

        login_btn = tk.Button(
            login_frame,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            command=lambda: self.show_loading_screen(lambda:self.authenticate_user()),
        )
        login_btn.grid(row=4, column=0, columnspan=2, pady=20, ipadx=20)

        register_btn = tk.Button(
            login_frame,
            text="Register as Patient",
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            command=lambda:self.show_loading_screen(lambda:self.show_patient_registration()),
        )
        register_btn.grid(row=5, column=0, columnspan=2, pady=10, ipadx=10)

        back_btn = tk.Button(
            login_frame,
            text="Back to Home",
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
            command=self.show_landing_screen,
        )
        back_btn.grid(row=6, column=0, columnspan=2, pady=10, ipadx=10)

    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        hashed_password = self.hash_password(password)

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT user_id, password FROM users WHERE username = %s AND user_type = %s",
                (username, user_type),
            )
            user_data = cursor.fetchone()

            if user_data and user_data[1] == hashed_password:
                self.current_user_id = user_data[0]
                self.current_user_type = user_type
                
                # Start hospital GIF animation
                self.gif_label.place(x=10, y=10)
                self.is_animating = True
                self.animate_gif()
                
                # Show appropriate dashboard directly
                if user_type == "admin":
                    self.show_admin_dashboard(user_data[0])
                elif user_type == "doctor":
                    self.show_doctor_dashboard(user_data[0])
                elif user_type == "patient":
                    self.show_patient_dashboard(user_data[0])
                elif user_type == "staff":
                    self.show_staff_dashboard(user_data[0])
            else:
                messagebox.showerror("Error", "Invalid username or password")
                self.show_login_screen(user_type)  # Stay on login screen with user type preserved

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to authenticate user: {e}")
            self.show_login_screen(user_type)
            

    def show_patient_registration(self, edit_mode=False, user_id=None):
            # Clear main frame
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            # Create scrollable canvas for form
            canvas = tk.Canvas(self.main_frame, bg="#e6f0fa")
            scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#e6f0fa", padx=20, pady=20)

            # Configure canvas scrolling
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Style for combobox and buttons
            style = ttk.Style()
            style.configure("TCombobox", fieldbackground="#ffffff", background="#ffffff", font=("Arial", 14))
            style.configure("TButton", padding=10, font=("Arial", 12, "bold"))

            # Header
            header_frame = tk.Frame(scrollable_frame, bg="#007bff")
            header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
            tk.Label(
                header_frame,
                text="Edit Patient Profile" if edit_mode else "Patient Registration",
                font=("Arial", 26, "bold"),
                bg="#007bff",
                fg="white"
            ).pack(pady=15)

            # Personal information section
            tk.Label(
                scrollable_frame,
                text="Personal Information",
                font=("Arial", 18, "bold"),
                bg="#e6f0fa",
                fg="#495057"
            ).grid(row=1, column=0, columnspan=2, pady=(20, 15), sticky="w")

            # Define form fields
            fields = [
                ("First Name:", 2),
                ("Last Name:", 3),
                ("Email:", 4),
                ("Date of Birth (YYYY-MM-DD):", 5),
                ("Gender:", 6),
                ("Blood Type:", 7),
                ("Phone:", 8),
                ("Address:", 9)
            ]

            # Create labels and entries for fields
            self.reg_first_name = tk.Entry(scrollable_frame, font=("Arial", 14), relief="flat", borderwidth=1, bg="#ffffff")
            self.reg_last_name = tk.Entry(scrollable_frame, font=("Arial", 14), relief="flat", borderwidth=1, bg="#ffffff")
            self.reg_email = tk.Entry(scrollable_frame, font=("Arial", 14), relief="flat", borderwidth=1, bg="#ffffff")
            self.reg_dob = tk.Entry(scrollable_frame, font=("Arial", 14), relief="flat", borderwidth=1, bg="#ffffff")
            self.reg_gender = ttk.Combobox(scrollable_frame, values=["Male", "Female", "Other"], state="readonly")
            self.reg_blood_type = ttk.Combobox(scrollable_frame, 
                                            values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], 
                                            state="readonly")
            self.reg_phone = tk.Entry(scrollable_frame, font=("Arial", 14), relief="flat", borderwidth=1, bg="#ffffff")
            self.reg_address = tk.Text(scrollable_frame, font=("Arial", 14), height=3, width=30)

            # Grid layout for fields
            for label_text, row in fields:
                tk.Label(
                    scrollable_frame,
                    text=label_text,
                    font=("Arial", 14),
                    bg="#e6f0fa",
                    fg="#495057"
                ).grid(row=row, column=0, pady=10, padx=15, sticky="e")
            
            self.reg_first_name.grid(row=2, column=1, pady=10, padx=15, sticky="w")
            self.reg_last_name.grid(row=3, column=1, pady=10, padx=15, sticky="w")
            self.reg_email.grid(row=4, column=1, pady=10, padx=15, sticky="w")
            self.reg_dob.grid(row=5, column=1, pady=10, padx=15, sticky="w")
            self.reg_gender.grid(row=6, column=1, pady=10, padx=15, sticky="w")
            self.reg_blood_type.grid(row=7, column=1, pady=10, padx=15, sticky="w")
            self.reg_phone.grid(row=8, column=1, pady=10, padx=15, sticky="w")
            self.reg_address.grid(row=9, column=1, pady=10, padx=15, sticky="w")

            # Profile photo section
            photo_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief="groove", borderwidth=2)
            photo_frame.grid(row=10, column=0, columnspan=2, pady=(20, 15), padx=10, sticky="ew")
            tk.Label(
                photo_frame,
                text="Profile Photo",
                font=("Arial", 18, "bold"),
                bg="#f8f9fa",
                fg="#495057"
            ).pack(pady=(10, 5))

            tk.Label(
                photo_frame,
                text="Upload Photo:",
                font=("Arial", 14),
                bg="#f8f9fa",
                fg="#495057"
            ).pack(side="left", padx=15, pady=5)

            self.photo_path = tk.StringVar()
            photo_button = ttk.Button(
                photo_frame,
                text="Choose Image",
                command=lambda: self.upload_photo(scrollable_frame)
            )
            photo_button.pack(side="left", padx=15, pady=5)

            # Photo display label
            self.photo_label = tk.Label(scrollable_frame, bg="#e6f0fa")
            self.photo_label.grid(row=11, column=0, columnspan=2, pady=10)

            # Login credentials section (only for new registration)
            if not edit_mode:
                credentials_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief="groove", borderwidth=2)
                credentials_frame.grid(row=12, column=0, columnspan=2, pady=(20, 15), padx=10, sticky="ew")
                tk.Label(
                    credentials_frame,
                    text="Login Credentials",
                    font=("Arial", 18, "bold"),
                    bg="#f8f9fa",
                    fg="#495057"
                ).pack(pady=(10, 5))

                tk.Label(
                    credentials_frame,
                    text="Username:",
                    font=("Arial", 14),
                    bg="#f8f9fa",
                    fg="#495057"
                ).pack(side="left", padx=15, pady=10)
                self.reg_username = tk.Entry(credentials_frame, font=("Arial", 14), relief="flat", borderwidth=1, bg="#ffffff")
                self.reg_username.pack(side="left", padx=15, pady=10)

                tk.Label(
                    credentials_frame,
                    text="Password:",
                    font=("Arial", 14),
                    bg="#f8f9fa",
                    fg="#495057"
                ).pack(side="left", padx=15, pady=10)
                self.reg_password = tk.Entry(credentials_frame, font=("Arial", 14), show="*", relief="flat", borderwidth=1, bg="#ffffff")
                self.reg_password.pack(side="left", padx=15, pady=10)

                tk.Label(
                    credentials_frame,
                    text="Confirm Password:",
                    font=("Arial", 14),
                    bg="#f8f9fa",
                    fg="#495057"
                ).pack(side="left", padx=15, pady=10)
                self.reg_confirm_password = tk.Entry(credentials_frame, font=("Arial", 14), show="*", relief="flat", borderwidth=1, bg="#ffffff")
                self.reg_confirm_password.pack(side="left", padx=15, pady=10)

            # Buttons
            button_frame = tk.Frame(scrollable_frame, bg="#e6f0fa")
            button_frame.grid(row=13 if not edit_mode else 12, column=0, columnspan=2, pady=20)

            if edit_mode:
                # Load existing patient data
                try:
                    cursor = self.db_connection.cursor()
                    cursor.execute(
                        """SELECT p.first_name, p.last_name, p.email, p.date_of_birth, p.gender, 
                                p.blood_type, p.phone, p.address, p.photo_path, u.username
                        FROM patients p
                        JOIN users u ON p.user_id = u.user_id
                        WHERE p.user_id = %s""",
                        (user_id,)
                    )
                    patient_data = cursor.fetchone()

                    if patient_data:
                        self.reg_first_name.insert(0, patient_data[0])
                        self.reg_last_name.insert(0, patient_data[1])
                        self.reg_email.insert(0, patient_data[2] if patient_data[2] else '')
                        self.reg_dob.insert(0, patient_data[3].strftime('%Y-%m-%d') if patient_data[3] else '')
                        self.reg_gender.set(patient_data[4])
                        self.reg_blood_type.set(patient_data[5])
                        self.reg_phone.insert(0, patient_data[6])
                        self.reg_address.insert("1.0", patient_data[7] or '')
                        self.photo_path.set(patient_data[8] or '')
                        
                        # Display photo if exists
                        if patient_data[8] and os.path.exists(patient_data[8]):
                            self.display_photo(patient_data[8])

                except Error as e:
                    messagebox.showerror("Database Error", f"Failed to load patient data: {e}")

            register_btn = ttk.Button(
                button_frame,
                text="Update Profile" if edit_mode else "Register",
                command=lambda: self.register_patient(edit_mode, user_id),
                style="TButton"
            )
            register_btn.pack(side="left", padx=15)
            back_btn = ttk.Button(
                button_frame,
                text="Cancel",
                command=lambda: self.show_patient_profile(user_id) if edit_mode else self.show_login_screen(),
                style="TButton"
            )
            back_btn.pack(side="left", padx=15)

    def register_patient(self, edit_mode=False, user_id=None):
        first_name = self.reg_first_name.get()
        last_name = self.reg_last_name.get()
        email = self.reg_email.get()
        dob = self.reg_dob.get()
        gender = self.reg_gender.get()
        blood_type = self.reg_blood_type.get()
        phone = self.reg_phone.get()
        address = self.reg_address.get("1.0", tk.END).strip()
        photo_path = self.photo_path.get() if self.photo_path.get() else None

        if not edit_mode:
            username = self.reg_username.get()
            password = self.reg_password.get()
            confirm_password = self.reg_confirm_password.get()

        if not all([first_name, last_name, email, dob, gender, phone, address]):
            messagebox.showerror("Error", "All fields except blood type are required")
            return
        if not "@" in email or not "." in email:
            messagebox.showerror("Error", "Invalid email format")
            return

        if not edit_mode and (not username or not password or not confirm_password):
            messagebox.showerror("Error", "All fields are required")
            return
        if not edit_mode and password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()

            if edit_mode:
                cursor.execute(
                    """UPDATE patients 
                    SET first_name = %s, last_name = %s, email = %s, date_of_birth = %s, 
                        gender = %s, blood_type = %s, phone = %s, address = %s, photo_path = %s
                    WHERE user_id = %s""",
                    (first_name, last_name, email, dob, gender, blood_type, phone, address, photo_path, user_id)
                )
                if hasattr(self, 'reg_password') and self.reg_password.get():
                    hashed_password = self.hash_password(self.reg_password.get())
                    cursor.execute(
                        "UPDATE users SET password = %s WHERE user_id = %s",
                        (hashed_password, user_id)
                    )
                self.db_connection.commit()
                messagebox.showinfo("Success", "Patient profile updated successfully!")
                self.show_patient_profile(user_id)
            else:
                cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Username already exists")
                    return
                hashed_password = self.hash_password(password)
                cursor.execute(
                    "INSERT INTO users (username, password, user_type) VALUES (%s, %s, 'patient')",
                    (username, hashed_password)
                )
                user_id = cursor.lastrowid
                cursor.execute(
                    """INSERT INTO patients 
                    (user_id, first_name, last_name, email, date_of_birth, gender, 
                     blood_type, phone, address, photo_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (user_id, first_name, last_name, email, dob, gender, blood_type, phone, address, photo_path)
                )
                self.db_connection.commit()
                subject = "Welcome to Grow Up Hospital"
                body = (
                    f"Dear {first_name} {last_name},\n\n"
                    f"Congratulations! Your registration with Grow Up Hospital has been successful.\n"
                    f"Username: {username}\n"
                    f"You can now log in to manage your appointments and medical records.\n\n"
                    f"Thank you for choosing Grow Up Hospital."
                )
                self.send_email_notification(email, subject, body)
                messagebox.showinfo("Success", "Patient registered successfully!")
                self.show_login_screen()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to {'update' if edit_mode else 'register'} patient: {e}")
        finally:
            if cursor:
                cursor.close()


    def upload_photo(self, frame):
            # Open file dialog to select image
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
            )
            if file_path:
                self.photo_path.set(file_path)  # Store file path
                # Load and display image
                image = Image.open(file_path)
                image = image.resize((150, 150), Image.LANCZOS)  # Resize to 150x150
                photo = ImageTk.PhotoImage(image)
                self.photo_label.configure(image=photo)
                self.photo_label.image = photo  # Keep reference to avoid garbage collection

    def show_patient_profile(self, user_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT p.first_name, p.last_name, p.email, p.phone, p.address, 
                        p.date_of_birth, p.gender, p.blood_type, p.photo_path, u.username
                FROM patients p
                JOIN users u ON p.user_id = u.user_id
                WHERE p.user_id = %s""",
                (user_id,)
            )
            patient = cursor.fetchone()
            if not patient:
                messagebox.showerror("Error", "Patient not found")
                return

            profile_window = tk.Toplevel(self.root)
            profile_window.title("Patient Profile")
            profile_window.geometry("600x600")
            profile_window.resizable(False, False)
            profile_window.configure(bg="#f0f8ff")

            # Header
            header_frame = tk.Frame(profile_window, bg="#3498db", height=60)
            header_frame.pack(fill=tk.X)
            tk.Label(
                header_frame,
                text=f"Profile: {patient[0]} {patient[1]}",
                font=("Arial", 18, "bold"),
                bg="#3498db",
                fg="white"
            ).pack(pady=15)

            # Profile details
            details_frame = tk.Frame(profile_window, bg="#f0f8ff", padx=20, pady=20)
            details_frame.pack(fill=tk.BOTH, expand=True)

            fields = ["First Name:", "Last Name:", "Email:", "Phone:", "Address:", 
                      "Date of Birth:", "Gender:", "Blood Type:", "Username:"]
            for i, (field, value) in enumerate(zip(fields, patient[:-1])):
                tk.Label(
                    details_frame,
                    text=field,
                    font=("Arial", 12, "bold"),
                    bg="#f0f8ff"
                ).grid(row=i, column=0, pady=5, sticky="e")
                tk.Label(
                    details_frame,
                    text=value if value else "N/A",
                    font=("Arial", 12),
                    bg="#f0f8ff"
                ).grid(row=i, column=1, pady=5, sticky="w")

            # Photo display
            if patient[8] and os.path.exists(patient[8]):
                photo_frame = tk.Frame(details_frame, bg="#f0f8ff")
                photo_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
                image = Image.open(patient[8])
                image = image.resize((150, 150), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                tk.Label(photo_frame, image=photo, bg="#f0f8ff").pack()
                profile_window.photo = photo  # Keep reference

            # Buttons
            button_frame = tk.Frame(details_frame, bg="#f0f8ff")
            button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
            tk.Button(
                button_frame,
                text="Edit Profile",
                font=("Arial", 12, "bold"),
                bg="#3498db",
                fg="white",
                command=lambda: self.edit_patient_profile(user_id, profile_window)
            ).pack(side=tk.LEFT, padx=10)
            tk.Button(
                button_frame,
                text="Close",
                font=("Arial", 12),
                bg="#e74c3c",
                fg="white",
                command=profile_window.destroy
            ).pack(side=tk.LEFT, padx=10)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load profile: {e}")
            self.logger.error(f"Database error in show_patient_profile: {e}")
        finally:
            if cursor:
                cursor.close()

    def edit_patient_profile(self, user_id, profile_window):
            profile_window.destroy()
            self.show_patient_registration(edit_mode=True, user_id=user_id)

    def save_patient_profile(self, user_id, edit_window):
            first_name = self.reg_first_name.get()
            last_name = self.reg_last_name.get()
            email = self.reg_email.get()
            phone = self.reg_phone.get()
            address = self.reg_address.get("1.0", tk.END).strip()
            dob = self.reg_dob.get()
            gender = self.reg_gender.get()
            blood_type = self.reg_blood_type.get()
            photo_path = self.photo_path.get() if self.photo_path.get() else None

            # Validate inputs
            if not all([first_name, last_name, email, phone, address, dob, gender]):
                messagebox.showerror("Error", "All fields except blood type are required")
                return
            if not "@" in email or not "." in email:
                messagebox.showerror("Error", "Invalid email format")
                return

            try:
                datetime.strptime(dob, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
                return

            try:
                cursor = self.db_connection.cursor()
                cursor.execute(
                    """UPDATE patients 
                    SET first_name = %s, last_name = %s, email = %s, phone = %s, 
                        address = %s, date_of_birth = %s, gender = %s, blood_type = %s, 
                        photo_path = %s 
                    WHERE user_id = %s""",
                    (first_name, last_name, email, phone, address, dob, gender, blood_type, photo_path, user_id)
                )
                self.db_connection.commit()
                messagebox.showinfo("Success", "Profile updated successfully!")
                edit_window.destroy()
                self.show_patient_profile(user_id)
            except Error as e:
                self.db_connection.rollback()
                messagebox.showerror("Database Error", f"Failed to update profile: {e}")
                self.logger.error(f"Database error in save_patient_profile: {e}")
            finally:
                if cursor:
                     cursor.close()
            
# Placeholder methods for dashboards (unchanged)
    def show_admin_dashboard(self, user_id):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Dashboard frame with light background
        dashboard_frame = tk.Frame(self.main_frame, bg="#f8fafc")
        dashboard_frame.pack(fill=tk.BOTH, expand=True)

        # Compact header
        header_frame = tk.Frame(dashboard_frame, bg="#4f46e5", height=75)
        header_frame.pack(fill=tk.X, pady=(0, 5))

        tk.Label(
            header_frame,
            text="Admin Dashboard",
            font=("Segoe UI", 20, "bold"),
            bg="#4f46e5",
            fg="white",
            padx=20
        ).pack(side=tk.LEFT)

        # Smaller logout button
        logout_btn = tk.Button(
            header_frame,
            text="Logout",
            font=("Segoe UI", 10, "bold"),
            bg="#ef4444",
            fg="white",
            activebackground="#dc2626",
            bd=0,
            padx=20,
            pady=5,
            relief=tk.FLAT,
            command=lambda: self.show_loading_screen(lambda: self.show_login_screen()),
        )
        logout_btn.pack(side=tk.RIGHT, padx=20)
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg="#dc2626"))
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg="#ef4444"))

        # Compact navigation panel
        nav_frame = tk.Frame(dashboard_frame, bg="#ffffff", width=200)
        nav_frame.pack(fill=tk.Y, side=tk.LEFT, ipady=10, padx=8, pady=8)

        # Button configuration for smaller size
        button_config = {
            "font": ("Segoe UI", 10),
            "bd": 0,
            "padx": 15,  # Reduced padding
            "pady": 8,   # Reduced padding
            "activebackground": "#e0e7ff",
            "activeforeground": "#4f46e5",
            "relief": tk.FLAT,
            "anchor": "w",
            "cursor": "hand2",
            "highlightthickness": 0,
            "borderwidth": 0
        }

        # Compact buttons with icons
        buttons = [
            ("📊 Dashboard", "#e0e7ff", "#4f46e5", lambda: self.show_admin_welcome()),
            ("👨‍⚕️ Doctors", "#ecfdf5", "#10b981", lambda: self.show_manage_doctors()),
            ("👥 Patients", "#f0f9ff", "#0ea5e9", lambda: self.show_manage_patients()),
            ("🛠️ Staff", "#f5f3ff", "#8b5cf6", lambda: self.show_manage_staff()),
            ("📅 Appoints", "#fef2f2", "#ef4444", lambda: self.show_admin_appointments()),
            ("📊 Reports", "#fffbeb", "#f59e0b", lambda: self.show_reports()),
            ("⚙️ Settings", "#ecfdf5", "#10b981", lambda: self.show_system_settings()),
        ]

        for text, bg_color, fg_color, command in buttons:
            btn = tk.Button(
                nav_frame,
                text=text,
                bg=bg_color,
                fg=fg_color,
                **button_config
            )
            btn.pack(fill=tk.X, padx=5, pady=3, ipady=5)  # Smaller spacing
            btn.config(command=command)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn, c=fg_color: b.config(bg=self.lighten_color(c, 0.8)))
            btn.bind("<Leave>", lambda e, b=btn, c=bg_color: b.config(bg=c))

        # Compact content area
        self.admin_content_frame = tk.Frame(
            dashboard_frame, 
            bg="#ffffff",
            highlightbackground="#e2e8f0",
            highlightthickness=1,
            padx=15,
            pady=15
        )
        self.admin_content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT, padx=5, pady=5)

        # Show default view
        self.show_admin_welcome()

    def lighten_color(self, hex_color, factor=0.1):
        """Lighten color by a given factor (0-1)"""
        rgb = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        lightened = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
        return f'#{lightened[0]:02x}{lightened[1]:02x}{lightened[2]:02x}'
  
    def show_admin_welcome(self):
        # Clear content frame
        for widget in self.admin_content_frame.winfo_children():
            widget.destroy()

        # Main container
        main_container = tk.Frame(self.admin_content_frame, bg="#f5f7fa", padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = tk.Frame(main_container, bg="#f5f7fa")
        header_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(
            header_frame,
            text="Admin Dashboard Overview",
            font=("Arial", 22, "bold"),
            bg="#f5f7fa",
            fg="#2c3e50"
        ).pack(side=tk.LEFT)

        current_date = datetime.now().strftime("%A, %B %d, %Y")
        tk.Label(
            header_frame,
            text=current_date,
            font=("Arial", 12),
            bg="#f5f7fa",
            fg="#7f8c8d"
        ).pack(side=tk.RIGHT)

        # Stats grid
        stats_frame = tk.Frame(main_container, bg="#f5f7fa")
        stats_frame.pack(fill=tk.X, pady=(0, 20))

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM patients")
            total_patients = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM doctors")
            total_doctors = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM staff")
            total_staff = cursor.fetchone()[0]

            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = %s", (today,))
            today_appointments = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM billing WHERE payment_status = 'Pending'")
            pending_bills = cursor.fetchone()[0]

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch statistics: {e}")
            return

        card_colors = {
            "patients": "#3498db",
            "doctors": "#2ecc71",
            "staff": "#e74c3c",
            "appointments": "#9b59b6",
            "bills": "#f39c12"
        }

        stats = [
            ("Total Patients", total_patients, "patients", lambda: self.show_manage_patients()),
            ("Total Doctors", total_doctors, "doctors", lambda: self.show_manage_doctors()),
            ("Total Staff", total_staff, "staff", lambda: self.show_manage_staff()),
            ("Today's Appointments", today_appointments, "appointments", lambda: self.show_admin_appointments()),
            ("Pending Bills", pending_bills, "bills", lambda: self.show_reports())
        ]

        for i, (title, value, card_type, command) in enumerate(stats):
            card = tk.Frame(
                stats_frame,
                bg=card_colors[card_type],
                bd=0,
                highlightthickness=0,
                width=200,
                height=100,
                relief=tk.RAISED
            )
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            card.grid_propagate(False)

            tk.Label(
                card,
                text=title,
                font=("Arial", 11, "bold"),
                bg=card_colors[card_type],
                fg="white",
                anchor="w"
            ).pack(fill=tk.X, padx=10, pady=(10, 0))

            tk.Label(
                card,
                text=str(value),
                font=("Arial", 24, "bold"),
                bg=card_colors[card_type],
                fg="white"
            ).pack(expand=True)

            # ✅ Fixed hover effect
            card.bind("<Enter>", lambda e, c=card: c.config(highlightbackground="#bdc3c7", highlightthickness=1))
            card.bind("<Leave>", lambda e, c=card: c.config(highlightbackground=c["bg"], highlightthickness=0))

            card.bind("<Button-1>", lambda e, cmd=command: cmd())
            for child in card.winfo_children():
                child.bind("<Button-1>", lambda e, cmd=command: cmd())

        # Responsive grid config
        for i in range(3):
            stats_frame.columnconfigure(i, weight=1)
        stats_frame.rowconfigure(0, weight=1)
        stats_frame.rowconfigure(1, weight=1)

        # Quick Actions
        actions_frame = tk.Frame(main_container, bg="#f5f7fa")
        actions_frame.pack(fill=tk.X, pady=(10, 20))

        tk.Label(
            actions_frame,
            text="Quick Actions",
            font=("Arial", 16, "bold"),
            bg="#f5f7fa",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 10))

        action_buttons = [
            ("Add New Doctor", "#2ecc71", lambda: self.show_add_doctor_form()),
            ("Add New Staff", "#3498db", lambda: self.show_add_staff_form()),
            ("Generate Report", "#9b59b6", lambda: self.show_reports()),
            ("System Settings", "#e67e22", lambda: self.show_system_settings())
        ]

        button_frame = tk.Frame(actions_frame, bg="#f5f7fa")
        button_frame.pack(fill=tk.X)

        for text, color, command in action_buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 11),
                bg=color,
                fg="white",
                bd=0,
                padx=15,
                pady=8,
                activebackground=color,
                activeforeground="white",
                command=command
            )
            btn.pack(side=tk.LEFT, padx=5, ipadx=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(relief=tk.SUNKEN))
            btn.bind("<Leave>", lambda e, b=btn: b.config(relief=tk.RAISED))


    def update_additional_filters(self, event=None):
        for widget in self.additional_filters_frame.winfo_children():
            widget.destroy()

        report_type = self.report_type_var.get()

        if report_type == "Appointments":
            tk.Label(self.additional_filters_frame, text="Status:", bg="#2a3d4e", fg="#e0f7fa").pack(side=tk.LEFT, padx=5)
            self.appt_status_var = tk.StringVar(value="All")
            ttk.Combobox(
                self.additional_filters_frame,
                textvariable=self.appt_status_var,
                values=["All", "Scheduled", "Confirmed", "Completed", "Cancelled"],
                state="readonly",
                width=12,
                style="Custom.TCombobox"
            ).pack(side=tk.LEFT, padx=5)

        elif report_type == "Financial":
            tk.Label(self.additional_filters_frame, text="Payment Status:", bg="#2a3d4e", fg="#e0f7fa").pack(side=tk.LEFT, padx=5)
            self.payment_status_var = tk.StringVar(value="All")
            ttk.Combobox(
                self.additional_filters_frame,
                textvariable=self.payment_status_var,
                values=["All", "Paid", "Pending"],
                state="readonly",
                width=10,
                style="Custom.TCombobox"
            ).pack(side=tk.LEFT, padx=5)

        elif report_type == "Patient Payments":
            tk.Label(self.additional_filters_frame, text="Payment Status:", bg="#2a3d4e", fg="#e0f7fa").pack(side=tk.LEFT, padx=5)
            self.patient_payment_var = tk.StringVar(value="All")
            ttk.Combobox(
                self.additional_filters_frame,
                textvariable=self.patient_payment_var,
                values=["All", "Paid", "Unpaid"],
                state="readonly",
                width=10,
                style="Custom.TCombobox"
            ).pack(side=tk.LEFT, padx=5)

    def load_doctors_data(self):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT d.doctor_id, CONCAT(d.first_name, ' ', d.last_name), d.specialization, d.phone, d.email
                FROM doctors d
                JOIN users u ON d.user_id = u.user_id
            """
            cursor.execute(query)
            doctors = cursor.fetchall()

            # Clear existing data
            for item in self.doctors_tree.get_children():
                self.doctors_tree.delete(item)

            # Insert new data
            for doctor in doctors:
                self.doctors_tree.insert("", tk.END, values=doctor)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load doctors data: {e}")

    def show_add_doctor_form(self):
        # Create a new top-level window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Doctor")
        add_window.geometry("500x600")

        tk.Label(add_window, text="Add New Doctor", font=("Arial", 18, "bold")).pack(
            pady=10
        )

        # Form fields
        fields = [
            ("First Name:", "entry"),
            ("Last Name:", "entry"),
            ("Specialization:", "entry"),
            ("Phone:", "entry"),
            ("Email:", "entry"),
            ("Username:", "entry"),
            ("Password:", "entry", True),
            ("Confirm Password:", "entry", True),
        ]

        self.doctor_form_entries = {}

        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(add_window, text=label, font=("Arial", 12)).pack(pady=5)

            if field_type == "entry":
                show = "*" if options and options[0] else ""
                entry = tk.Entry(add_window, font=("Arial", 12), show=show)
                entry.pack(pady=5, ipadx=20)
                self.doctor_form_entries[
                    label.split(":")[0].lower().replace(" ", "_")
                ] = entry

        # Submit button
        submit_btn = tk.Button(
            add_window,
            text="Add Doctor",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.add_doctor(add_window),
        )
        submit_btn.pack(pady=20)

    def add_doctor(self, window):
        # Get all form data
        first_name = self.doctor_form_entries["first_name"].get()
        last_name = self.doctor_form_entries["last_name"].get()
        specialization = self.doctor_form_entries["specialization"].get()
        phone = self.doctor_form_entries["phone"].get()
        email = self.doctor_form_entries["email"].get()
        username = self.doctor_form_entries["username"].get()
        password = self.doctor_form_entries["password"].get()
        confirm_password = self.doctor_form_entries["confirm_password"].get()

        # Validate inputs
        if not all([first_name, last_name, specialization, username, password, confirm_password]):
            messagebox.showerror("Error", "All fields except phone and email are required")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Check if username exists
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return

            # Insert user
            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)",
                (username, hashed_password, "doctor"),
            )
            user_id = cursor.lastrowid

            # Insert doctor
            cursor.execute(
                """INSERT INTO doctors 
                (user_id, first_name, last_name, specialization, phone, email) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (user_id, first_name, last_name, specialization, phone, email),
            )

            self.db_connection.commit()
            messagebox.showinfo("Success", "Doctor added successfully!")
            window.destroy()
            self.load_doctors_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to add doctor: {e}")
        finally:
            if cursor:
                cursor.close()

    def edit_doctor(self):
        selected_item = self.doctors_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a doctor to edit")
            return

        doctor_id = self.doctors_tree.item(selected_item)["values"][0]

        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT d.doctor_id, d.first_name, d.last_name, d.specialization, 
                    d.phone, d.email, u.username
                FROM doctors d
                JOIN users u ON d.user_id = u.user_id
                WHERE d.doctor_id = %s
            """
            cursor.execute(query, (doctor_id,))
            doctor_data = cursor.fetchone()

            if not doctor_data:
                messagebox.showerror("Error", "Doctor not found")
                return

            # Create edit window with scrollable frame
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Doctor")
            edit_window.geometry("700x700")
            edit_window.resizable(True, True)
            
            # Modern styling
            bg_color = "#f8f9fa"
            label_color = "#343a40"
            entry_bg = "#ffffff"
            button_color = "#007bff"
            edit_window.configure(bg=bg_color)

            # Create main container with scrollbar
            container = tk.Frame(edit_window, bg=bg_color)
            container.pack(fill="both", expand=True)

            # Create a canvas
            canvas = tk.Canvas(container, bg=bg_color)
            scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=bg_color, padx=20, pady=20)

            # Configure canvas scrolling
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Title
            tk.Label(
                scrollable_frame,
                text="Edit Doctor Information",
                font=("Arial", 18, "bold"),
                bg=bg_color,
                fg=label_color
            ).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

            # Form fields - using consistent keys that match database fields
            fields = [
                ("first_name", "First Name:", doctor_data[1], "entry"),
                ("last_name", "Last Name:", doctor_data[2], "entry"),
                ("specialization", "Specialization:", doctor_data[3], "entry"),
                ("phone", "Phone:", doctor_data[4], "entry"),
                ("email", "Email:", doctor_data[5], "entry"),
                ("username", "Username:", doctor_data[6], "entry"),
            ]

            self.edit_doctor_entries = {}
            row_num = 1

            for field_name, label_text, value, field_type in fields:
                # Label
                tk.Label(
                    scrollable_frame,
                    text=label_text,
                    font=("Arial", 12),
                    bg=bg_color,
                    fg=label_color
                ).grid(row=row_num, column=0, pady=8, padx=10, sticky="e")

                # Field
                if field_type == "entry":
                    entry = tk.Entry(
                        scrollable_frame,
                        font=("Arial", 12),
                        bg=entry_bg,
                        bd=1,
                        relief="solid"
                    )
                    entry.insert(0, value)
                    entry.grid(row=row_num, column=1, pady=8, padx=10, sticky="we")
                    
                self.edit_doctor_entries[field_name] = entry
                row_num += 1

            # Password fields (optional)
            tk.Label(
                scrollable_frame,
                text="New Password (leave blank to keep current):",
                font=("Arial", 12),
                bg=bg_color,
                fg=label_color
            ).grid(row=row_num, column=0, pady=8, padx=10, sticky="e")
            
            self.edit_doctor_password = tk.Entry(
                scrollable_frame,
                font=("Arial", 12),
                show="*",
                bg=entry_bg,
                bd=1,
                relief="solid"
            )
            self.edit_doctor_password.grid(row=row_num, column=1, pady=8, padx=10, sticky="we")
            row_num += 1

            tk.Label(
                scrollable_frame,
                text="Confirm New Password:",
                font=("Arial", 12),
                bg=bg_color,
                fg=label_color
            ).grid(row=row_num, column=0, pady=8, padx=10, sticky="e")
            
            self.edit_doctor_confirm_password = tk.Entry(
                scrollable_frame,
                font=("Arial", 12),
                show="*",
                bg=entry_bg,
                bd=1,
                relief="solid"
            )
            self.edit_doctor_confirm_password.grid(row=row_num, column=1, pady=8, padx=10, sticky="we")
            row_num += 1

            # Button frame
            button_frame = tk.Frame(scrollable_frame, bg=bg_color)
            button_frame.grid(row=row_num, column=0, columnspan=2, pady=20)

            # Update button
            update_btn = tk.Button(
                button_frame,
                text="Update Doctor",
                font=("Arial", 12, "bold"),
                bg=button_color,
                fg="white",
                activebackground="#0069d9",
                bd=0,
                padx=20,
                pady=10,
                command=lambda: self.update_doctor(doctor_id, edit_window)
            )
            update_btn.pack(side="left", padx=10)

            # Cancel button
            cancel_btn = tk.Button(
                button_frame,
                text="Cancel",
                font=("Arial", 12),
                bg="#6c757d",
                fg="white",
                activebackground="#5a6268",
                bd=0,
                padx=20,
                pady=10,
                command=edit_window.destroy
            )
            cancel_btn.pack(side="left", padx=10)

            # Configure grid weights to make form responsive
            scrollable_frame.grid_columnconfigure(1, weight=1)

            # Bind mouse wheel scrolling for Windows
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            edit_window.bind("<MouseWheel>", _on_mousewheel)
            scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch doctor data: {e}")

    def update_doctor(self, doctor_id, window):
        # Get all form data
        first_name = self.edit_doctor_entries["first_name"].get()
        last_name = self.edit_doctor_entries["last_name"].get()
        specialization = self.edit_doctor_entries["specialization"].get()
        phone = self.edit_doctor_entries["phone"].get()
        email = self.edit_doctor_entries["email"].get()
        username = self.edit_doctor_entries["username"].get()
        password = self.edit_doctor_password.get()
        confirm_password = self.edit_doctor_confirm_password.get()

        # Validate inputs
        if not all([first_name, last_name, specialization, username]):
            messagebox.showerror("Error", "First Name, Last Name, Specialization, and Username are required")
            return

        if password and password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Get user_id for this doctor
            cursor.execute("SELECT user_id FROM doctors WHERE doctor_id = %s", (doctor_id,))
            user_id = cursor.fetchone()[0]

            # Check if username exists (excluding current doctor)
            cursor.execute(
                "SELECT username FROM users WHERE username = %s AND user_id != %s",
                (username, user_id)
            )
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return

            # Update doctors table
            cursor.execute(
                """UPDATE doctors 
                SET first_name = %s, last_name = %s, specialization = %s, 
                    phone = %s, email = %s
                WHERE doctor_id = %s""",
                (first_name, last_name, specialization, phone, email, doctor_id),
            )

            # Update users table
            if password:
                hashed_password = self.hash_password(password)
                cursor.execute(
                    "UPDATE users SET username = %s, password = %s WHERE user_id = %s",
                    (username, hashed_password, user_id)
                )
            else:
                cursor.execute(
                    "UPDATE users SET username = %s WHERE user_id = %s",
                    (username, user_id)
                )

            self.db_connection.commit()
            messagebox.showinfo("Success", "Doctor updated successfully!")
            window.destroy()
            self.load_doctors_data()  # Refresh the doctors list

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to update doctor: {e}")
        finally:
            if cursor:
                cursor.close()
                
    def delete_doctor(self):
        selected_item = self.doctors_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a doctor to delete")
            return

        doctor_id = self.doctors_tree.item(selected_item)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm", "Are you sure you want to delete this doctor?"
        )
        if not confirm:
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Get user_id for this doctor
            cursor.execute("SELECT user_id FROM doctors WHERE doctor_id = %s", (doctor_id,))
            user_id = cursor.fetchone()[0]

            # Delete from doctors table
            cursor.execute("DELETE FROM doctors WHERE doctor_id = %s", (doctor_id,))

            # Delete from users table
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

            self.db_connection.commit()
            messagebox.showinfo("Success", "Doctor deleted successfully!")
            self.load_doctors_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to delete doctor: {e}")
        finally:
            if cursor:
                cursor.close()
                
    def show_manage_doctors(self):
        # Clear content frame
        for widget in self.admin_content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.admin_content_frame,
            text="Manage Doctors",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=10)

        # Add doctor button
        add_btn = tk.Button(
            self.admin_content_frame,
            text="Add New Doctor",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.show_add_doctor_form,
        )
        add_btn.pack(pady=10)

        # Doctors table
        columns = ("ID", "Name", "Specialization", "Phone", "Email")
        self.doctors_tree = ttk.Treeview(
            self.admin_content_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.doctors_tree.heading(col, text=col)
            self.doctors_tree.column(col, width=150, anchor=tk.CENTER)

        self.doctors_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Load doctors data
        self.load_doctors_data()

        # Action buttons frame
        action_frame = tk.Frame(self.admin_content_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)

        edit_btn = tk.Button(
            action_frame,
            text="Edit Doctor",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=self.edit_doctor,
        )
        edit_btn.grid(row=0, column=0, padx=10)

        delete_btn = tk.Button(
            action_frame,
            text="Delete Doctor",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=self.delete_doctor,
        )
        delete_btn.grid(row=0, column=1, padx=10)

    def load_doctors_data(self):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT d.doctor_id, CONCAT(d.first_name, ' ', d.last_name), d.specialization, d.phone, d.email
                FROM doctors d
                JOIN users u ON d.user_id = u.user_id
            """
            cursor.execute(query)
            doctors = cursor.fetchall()

            # Clear existing data
            for item in self.doctors_tree.get_children():
                self.doctors_tree.delete(item)

            # Insert new data
            for doctor in doctors:
                self.doctors_tree.insert("", tk.END, values=doctor)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load doctors data: {e}")

    def show_add_doctor_form(self):
        # Create a new top-level window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Doctor")
        add_window.geometry("500x600")

        tk.Label(add_window, text="Add New Doctor", font=("Arial", 18, "bold")).pack(
            pady=10
        )

        # Form fields
        fields = [
            ("First Name:", "entry"),
            ("Last Name:", "entry"),
            ("Specialization:", "entry"),
            ("Phone:", "entry"),
            ("Email:", "entry"),
            ("Username:", "entry"),
            ("Password:", "entry", True),
            ("Confirm Password:", "entry", True),
        ]

        self.doctor_form_entries = {}

        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(add_window, text=label, font=("Arial", 12)).pack(pady=5)

            if field_type == "entry":
                show = "*" if options and options[0] else ""
                entry = tk.Entry(add_window, font=("Arial", 12), show=show)
                entry.pack(pady=5, ipadx=20)
                self.doctor_form_entries[
                    label.split(":")[0].lower().replace(" ", "_")
                ] = entry

        # Submit button
        submit_btn = tk.Button(
            add_window,
            text="Add Doctor",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.add_doctor(add_window),
        )
        submit_btn.pack(pady=20)

    def add_doctor(self, window):
        # Get all form data
        first_name = self.doctor_form_entries["first_name"].get()
        last_name = self.doctor_form_entries["last_name"].get()
        specialization = self.doctor_form_entries["specialization"].get()
        phone = self.doctor_form_entries["phone"].get()
        email = self.doctor_form_entries["email"].get()
        username = self.doctor_form_entries["username"].get()
        password = self.doctor_form_entries["password"].get()
        confirm_password = self.doctor_form_entries["confirm_password"].get()

        # Validate inputs
        if not all([first_name, last_name, specialization, username, password, confirm_password]):
            messagebox.showerror("Error", "All fields except phone and email are required")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Check if username exists
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return

            # Insert user
            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)",
                (username, hashed_password, "doctor"),
            )
            user_id = cursor.lastrowid

            # Insert doctor
            cursor.execute(
                """INSERT INTO doctors 
                (user_id, first_name, last_name, specialization, phone, email) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (user_id, first_name, last_name, specialization, phone, email),
            )

            self.db_connection.commit()
            messagebox.showinfo("Success", "Doctor added successfully!")
            window.destroy()
            self.load_doctors_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to add doctor: {e}")
        finally:
            if cursor:
                cursor.close()

    def edit_doctor(self):
        selected_item = self.doctors_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a doctor to edit")
            return

        doctor_id = self.doctors_tree.item(selected_item)["values"][0]

        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT d.doctor_id, d.first_name, d.last_name, d.specialization, d.phone, d.email, u.username
                FROM doctors d
                JOIN users u ON d.user_id = u.user_id
                WHERE d.doctor_id = %s
            """
            cursor.execute(query, (doctor_id,))
            doctor_data = cursor.fetchone()

            if not doctor_data:
                messagebox.showerror("Error", "Doctor not found")
                return

            # Create edit window
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Doctor")
            edit_window.geometry("500x600")

            tk.Label(edit_window, text="Edit Doctor", font=("Arial", 18, "bold")).pack(pady=10)

            # Form fields
            fields = [
                ("First Name:", doctor_data[1]),
                ("Last Name:", doctor_data[2]),
                ("Specialization:", doctor_data[3]),
                ("Phone:", doctor_data[4]),
                ("Email:", doctor_data[5]),
                ("Username:", doctor_data[6]),
            ]

            self.edit_doctor_entries = {}

            for i, (label, value) in enumerate(fields):
                tk.Label(edit_window, text=label, font=("Arial", 12)).pack(pady=5)

                entry = tk.Entry(edit_window, font=("Arial", 12))
                entry.insert(0, value)
                entry.pack(pady=5, ipadx=20)

                self.edit_doctor_entries[
                    label.split(":")[0].lower().replace(" ", "_")
                ] = entry

            # Add password fields (optional)
            tk.Label(edit_window, text="New Password (leave blank to keep current):", font=("Arial", 12)).pack(pady=5)
            self.edit_doctor_password = tk.Entry(edit_window, font=("Arial", 12), show="*")
            self.edit_doctor_password.pack(pady=5, ipadx=20)

            tk.Label(edit_window, text="Confirm New Password:", font=("Arial", 12)).pack(pady=5)
            self.edit_doctor_confirm_password = tk.Entry(edit_window, font=("Arial", 12), show="*")
            self.edit_doctor_confirm_password.pack(pady=5, ipadx=20)

            # Submit button
            submit_btn = tk.Button(
                edit_window,
                text="Update Doctor",
                font=("Arial", 12, "bold"),
                bg="#4CAF50",
                fg="white",
                command=lambda: self.update_doctor(doctor_id, edit_window),
            )
            submit_btn.pack(pady=20)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch doctor data: {e}")

    def update_doctor(self, doctor_id, window):
        # Get all form data
        first_name = self.edit_doctor_entries["first_name"].get()
        last_name = self.edit_doctor_entries["last_name"].get()
        specialization = self.edit_doctor_entries["specialization"].get()
        phone = self.edit_doctor_entries["phone"].get()
        email = self.edit_doctor_entries["email"].get()
        username = self.edit_doctor_entries["username"].get()
        password = self.edit_doctor_password.get()
        confirm_password = self.edit_doctor_confirm_password.get()

        # Validate inputs
        if not all([first_name, last_name, specialization, username]):
            messagebox.showerror("Error", "First Name, Last Name, Specialization, and Username are required")
            return

        if password and password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Get user_id for this doctor
            cursor.execute("SELECT user_id FROM doctors WHERE doctor_id = %s", (doctor_id,))
            user_id = cursor.fetchone()[0]

            # Check if username exists (excluding current doctor)
            cursor.execute(
                "SELECT username FROM users WHERE username = %s AND user_id != %s",
                (username, user_id)
            )
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return

            # Update doctors table
            cursor.execute(
                """UPDATE doctors 
                SET first_name = %s, last_name = %s, specialization = %s, phone = %s, email = %s
                WHERE doctor_id = %s""",
                (first_name, last_name, specialization, phone, email, doctor_id),
            )

            # Update users table
            if password:
                hashed_password = self.hash_password(password)
                cursor.execute(
                    "UPDATE users SET username = %s, password = %s WHERE user_id = %s",
                    (username, hashed_password, user_id)
                )
            else:
                cursor.execute(
                    "UPDATE users SET username = %s WHERE user_id = %s",
                    (username, user_id)
                )

            self.db_connection.commit()
            messagebox.showinfo("Success", "Doctor updated successfully!")
            window.destroy()
            self.show_loading_screen(lambda: self.load_doctors_data())

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to update doctor: {e}")
        finally:
            if cursor:
                cursor.close()
                
    def delete_doctor(self):
        selected_item = self.doctors_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a doctor to delete")
            return

        doctor_id = self.doctors_tree.item(selected_item)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm", "Are you sure you want to delete this doctor?"
        )
        if not confirm:
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Get user_id for this doctor
            cursor.execute("SELECT user_id FROM doctors WHERE doctor_id = %s", (doctor_id,))
            user_id = cursor.fetchone()[0]

            # Delete from doctors table
            cursor.execute("DELETE FROM doctors WHERE doctor_id = %s", (doctor_id,))

            # Delete from users table
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

            self.db_connection.commit()
            messagebox.showinfo("Success", "Doctor deleted successfully!")
            self.load_doctors_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to delete doctor: {e}")
        finally:
            if cursor:
                cursor.close()

    def show_manage_staff(self):
        # Clear content frame
        for widget in self.admin_content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.admin_content_frame,
            text="Manage Staff",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=10)

        # Add staff button
        add_btn = tk.Button(
            self.admin_content_frame,
            text="Add New Staff Member",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.show_add_staff_form,
        )
        add_btn.pack(pady=10)

        # Staff table
        columns = ("ID", "Name", "Role", "Phone", "Email")
        self.staff_tree = ttk.Treeview(
            self.admin_content_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.staff_tree.heading(col, text=col)
            self.staff_tree.column(col, width=150, anchor=tk.CENTER)

        self.staff_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Load staff data
        self.load_staff_data()

        # Action buttons frame
        action_frame = tk.Frame(self.admin_content_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)

        edit_btn = tk.Button(
            action_frame,
            text="Edit Staff",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=self.edit_staff,
           
        )
        edit_btn.grid(row=0, column=0, padx=10)

        delete_btn = tk.Button(
            action_frame,
            text="Delete Staff",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=lambda:self.show_loading_screen(lambda:self.delete_staff()),
        )
        delete_btn.grid(row=0, column=1, padx=10)

    def load_staff_data(self):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT s.staff_id, CONCAT(s.first_name, ' ', s.last_name), s.role, s.phone, s.email
                FROM staff s
                JOIN users u ON s.user_id = u.user_id
            """
            cursor.execute(query)
            staff_members = cursor.fetchall()

            # Clear existing data
            for item in self.staff_tree.get_children():
                self.staff_tree.delete(item)

            # Insert new data
            for staff in staff_members:
                self.staff_tree.insert("", tk.END, values=staff)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load staff data: {e}")

    def show_manage_doctors(self):
        # Clear content frame
        for widget in self.admin_content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.admin_content_frame,
            text="Manage Doctors",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=10)

        # Add doctor button
        add_btn = tk.Button(
            self.admin_content_frame,
            text="Add New Doctor",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.show_add_doctor_form,
        )
        add_btn.pack(pady=10)

        # Doctors table
        columns = ("ID", "Name", "Specialization", "Phone", "Email")
        self.doctors_tree = ttk.Treeview(
            self.admin_content_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.doctors_tree.heading(col, text=col)
            self.doctors_tree.column(col, width=150, anchor=tk.CENTER)

        self.doctors_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Load doctors data
        self.load_doctors_data()

        # Action buttons frame
        action_frame = tk.Frame(self.admin_content_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)

        edit_btn = tk.Button(
            action_frame,
            text="Edit Doctor",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=self.edit_doctor,
        )
        edit_btn.grid(row=0, column=0, padx=10)

        delete_btn = tk.Button(
            action_frame,
            text="Delete Doctor",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=self.delete_doctor,
        )
        delete_btn.grid(row=0, column=1, padx=10)

    def load_doctors_data(self):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT d.doctor_id, CONCAT(d.first_name, ' ', d.last_name), d.specialization, d.phone, d.email
                FROM doctors d
                JOIN users u ON d.user_id = u.user_id
            """
            cursor.execute(query)
            doctors = cursor.fetchall()

            # Clear existing data
            for item in self.doctors_tree.get_children():
                self.doctors_tree.delete(item)

            # Insert new data
            for doctor in doctors:
                self.doctors_tree.insert("", tk.END, values=doctor)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load doctors data: {e}")

    def show_add_doctor_form(self):
        # Create a new top-level window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Doctor")
        add_window.geometry("500x600")

        tk.Label(add_window, text="Add New Doctor", font=("Arial", 18, "bold")).pack(
            pady=10
        )

        # Form fields
        fields = [
            ("First Name:", "entry"),
            ("Last Name:", "entry"),
            ("Specialization:", "entry"),
            ("Phone:", "entry"),
            ("Email:", "entry"),
            ("Username:", "entry"),
            ("Password:", "entry", True),
            ("Confirm Password:", "entry", True),
        ]

        self.doctor_form_entries = {}

        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(add_window, text=label, font=("Arial", 12)).pack(pady=5)

            if field_type == "entry":
                show = "*" if options and options[0] else ""
                entry = tk.Entry(add_window, font=("Arial", 12), show=show)
                entry.pack(pady=5, ipadx=20)
                self.doctor_form_entries[
                    label.split(":")[0].lower().replace(" ", "_")
                ] = entry

        # Submit button
        submit_btn = tk.Button(
            add_window,
            text="Add Doctor",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.add_doctor(add_window),
        )
        submit_btn.pack(pady=20)

    def add_doctor(self, window):
        # Get all form data
        first_name = self.doctor_form_entries["first_name"].get()
        last_name = self.doctor_form_entries["last_name"].get()
        specialization = self.doctor_form_entries["specialization"].get()
        phone = self.doctor_form_entries["phone"].get()
        email = self.doctor_form_entries["email"].get()
        username = self.doctor_form_entries["username"].get()
        password = self.doctor_form_entries["password"].get()
        confirm_password = self.doctor_form_entries["confirm_password"].get()

        # Validate inputs
        if not all([first_name, last_name, specialization, username, password, confirm_password]):
            messagebox.showerror("Error", "All fields except phone and email are required")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Check if username exists
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return

            # Insert user
            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)",
                (username, hashed_password, "doctor"),
            )
            user_id = cursor.lastrowid

            # Insert doctor
            cursor.execute(
                """INSERT INTO doctors 
                (user_id, first_name, last_name, specialization, phone, email) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (user_id, first_name, last_name, specialization, phone, email),
            )

            self.db_connection.commit()
            messagebox.showinfo("Success", "Doctor added successfully!")
            window.destroy()
            self.load_doctors_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to add doctor: {e}")
        finally:
            if cursor:
                cursor.close()

    def edit_doctor(self):
        selected_item = self.doctors_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a doctor to edit")
            return

        doctor_id = self.doctors_tree.item(selected_item)["values"][0]

        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT d.doctor_id, d.first_name, d.last_name, d.specialization, d.phone, d.email, u.username
                FROM doctors d
                JOIN users u ON d.user_id = u.user_id
                WHERE d.doctor_id = %s
            """
            cursor.execute(query, (doctor_id,))
            doctor_data = cursor.fetchone()

            if not doctor_data:
                messagebox.showerror("Error", "Doctor not found")
                return

            # Create edit window
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Doctor")
            edit_window.geometry("500x600")

            tk.Label(edit_window, text="Edit Doctor", font=("Arial", 18, "bold")).pack(pady=10)

            # Form fields
            fields = [
                ("First Name:", doctor_data[1]),
                ("Last Name:", doctor_data[2]),
                ("Specialization:", doctor_data[3]),
                ("Phone:", doctor_data[4]),
                ("Email:", doctor_data[5]),
                ("Username:", doctor_data[6]),
            ]

            self.edit_doctor_entries = {}

            for i, (label, value) in enumerate(fields):
                tk.Label(edit_window, text=label, font=("Arial", 12)).pack(pady=5)

                entry = tk.Entry(edit_window, font=("Arial", 12))
                entry.insert(0, value)
                entry.pack(pady=5, ipadx=20)

                self.edit_doctor_entries[
                    label.split(":")[0].lower().replace(" ", "_")
                ] = entry

            # Add password fields (optional)
            tk.Label(edit_window, text="New Password (leave blank to keep current):", font=("Arial", 12)).pack(pady=5)
            self.edit_doctor_password = tk.Entry(edit_window, font=("Arial", 12), show="*")
            self.edit_doctor_password.pack(pady=5, ipadx=20)

            tk.Label(edit_window, text="Confirm New Password:", font=("Arial", 12)).pack(pady=5)
            self.edit_doctor_confirm_password = tk.Entry(edit_window, font=("Arial", 12), show="*")
            self.edit_doctor_confirm_password.pack(pady=5, ipadx=20)

            # Submit button
            submit_btn = tk.Button(
                edit_window,
                text="Update Doctor",
                font=("Arial", 12, "bold"),
                bg="#4CAF50",
                fg="white",
                command=lambda: self.update_doctor(doctor_id, edit_window),
            )
            submit_btn.pack(pady=20)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch doctor data: {e}")

    def update_doctor(self, doctor_id, window):
        # Get all form data
        first_name = self.edit_doctor_entries["first_name"].get()
        last_name = self.edit_doctor_entries["last_name"].get()
        specialization = self.edit_doctor_entries["specialization"].get()
        phone = self.edit_doctor_entries["phone"].get()
        email = self.edit_doctor_entries["email"].get()
        username = self.edit_doctor_entries["username"].get()
        password = self.edit_doctor_password.get()
        confirm_password = self.edit_doctor_confirm_password.get()

        # Validate inputs
        if not all([first_name, last_name, specialization, username]):
            messagebox.showerror("Error", "First Name, Last Name, Specialization, and Username are required")
            return

        if password and password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Get user_id for this doctor
            cursor.execute("SELECT user_id FROM doctors WHERE doctor_id = %s", (doctor_id,))
            user_id = cursor.fetchone()[0]

            # Check if username exists (excluding current doctor)
            cursor.execute(
                "SELECT username FROM users WHERE username = %s AND user_id != %s",
                (username, user_id)
            )
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return

            # Update doctors table
            cursor.execute(
                """UPDATE doctors 
                SET first_name = %s, last_name = %s, specialization = %s, phone = %s, email = %s
                WHERE doctor_id = %s""",
                (first_name, last_name, specialization, phone, email, doctor_id),
            )

            # Update users table
            if password:
                hashed_password = self.hash_password(password)
                cursor.execute(
                    "UPDATE users SET username = %s, password = %s WHERE user_id = %s",
                    (username, hashed_password, user_id)
                )
            else:
                cursor.execute(
                    "UPDATE users SET username = %s WHERE user_id = %s",
                    (username, user_id)
                )

            self.db_connection.commit()
            messagebox.showinfo("Success", "Doctor updated successfully!")
            window.destroy()
            self.show_loading_screen(lambda: self.load_doctors_data())

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to update doctor: {e}")
        finally:
            if cursor:
                cursor.close()
                
    def delete_doctor(self):
        selected_item = self.doctors_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a doctor to delete")
            return

        doctor_id = self.doctors_tree.item(selected_item)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm", "Are you sure you want to delete this doctor?"
        )
        if not confirm:
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Get user_id for this doctor
            cursor.execute("SELECT user_id FROM doctors WHERE doctor_id = %s", (doctor_id,))
            user_id = cursor.fetchone()[0]

            # Delete from doctors table
            cursor.execute("DELETE FROM doctors WHERE doctor_id = %s", (doctor_id,))

            # Delete from users table
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

            self.db_connection.commit()
            messagebox.showinfo("Success", "Doctor deleted successfully!")
            self.load_doctors_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to delete doctor: {e}")
        finally:
            if cursor:
                cursor.close()
                
    def show_system_settings(self):
                    # Clear content frame
                    for widget in self.admin_content_frame.winfo_children():
                        widget.destroy()

                    tk.Label(
                        self.admin_content_frame,
                        text="System Settings",
                        font=("Arial", 20, "bold"),
                        bg="#f0f8ff",
                    ).pack(pady=10)

                    # Settings frame
                    settings_frame = tk.Frame(self.admin_content_frame, bg="#f0f8ff")
                    settings_frame.pack(pady=20)

                    # Business hours setting
                    tk.Label(
                        settings_frame,
                        text="Business Hours:",
                        font=("Arial", 12, "bold"),
                        bg="#f0f8ff"
                    ).grid(row=0, column=0, pady=5, sticky="w")

                    # Start time
                    tk.Label(settings_frame, text="Opening Time:", font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, pady=5)
                    self.opening_time = tk.Entry(settings_frame, font=("Arial", 12))
                    self.opening_time.grid(row=1, column=1, pady=5)
                    self.opening_time.insert(0, "08:00")

                    # End time
                    tk.Label(settings_frame, text="Closing Time:", font=("Arial", 12), bg="#f0f8ff").grid(row=2, column=0, pady=5)
                    self.closing_time = tk.Entry(settings_frame, font=("Arial", 12))
                    self.closing_time.grid(row=2, column=1, pady=5)
                    self.closing_time.insert(0, "17:00")

                    # Appointment duration
                    tk.Label(
                        settings_frame,
                        text="Default Appointment Duration (minutes):",
                        font=("Arial", 12),
                        bg="#f0f8ff"
                    ).grid(row=3, column=0, pady=5)
                    self.appointment_duration = tk.Entry(settings_frame, font=("Arial", 12))
                    self.appointment_duration.grid(row=3, column=1, pady=5)
                    self.appointment_duration.insert(0, "30")

                    # Save button
                    save_btn = tk.Button(
                        settings_frame,
                        text="Save Settings",
                        font=("Arial", 12, "bold"),
                        bg="#4CAF50",
                        fg="white",
                        command=self.save_system_settings,
                    )
                    save_btn.grid(row=4, column=0, columnspan=2, pady=20)

    def save_system_settings(self):
                    opening_time = self.opening_time.get()
                    closing_time = self.closing_time.get()
                    duration = self.appointment_duration.get()

                    # Validate inputs
                    try:
                        datetime.strptime(opening_time, "%H:%M")
                        datetime.strptime(closing_time, "%H:%M")
                        int(duration)
                    except ValueError:
                        messagebox.showerror("Error", "Invalid input format. Time should be HH:MM and duration should be a number")
                        return

                    # In a real application, you would save these settings to a database or config file
                    messagebox.showinfo("Success", "Settings saved successfully (not persisted in this demo)")
            
    

    def show_manage_staff(self):
        # Clear content frame
        for widget in self.admin_content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.admin_content_frame,
            text="Manage Staff",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=10)

        # Add staff button
        add_btn = tk.Button(
            self.admin_content_frame,
            text="Add New Staff Member",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.show_add_staff_form,
        )
        add_btn.pack(pady=10)

        # Staff table
        columns = ("ID", "Name", "Role", "Phone", "Email")
        self.staff_tree = ttk.Treeview(
            self.admin_content_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.staff_tree.heading(col, text=col)
            self.staff_tree.column(col, width=150, anchor=tk.CENTER)

        self.staff_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Load staff data
        self.load_staff_data()

        # Action buttons frame
        action_frame = tk.Frame(self.admin_content_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)

        edit_btn = tk.Button(
            action_frame,
            text="Edit Staff",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=self.edit_staff,
           
        )
        edit_btn.grid(row=0, column=0, padx=10)

        delete_btn = tk.Button(
            action_frame,
            text="Delete Staff",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=lambda:self.show_loading_screen(lambda:self.delete_staff()),
        )
        delete_btn.grid(row=0, column=1, padx=10)

    def load_staff_data(self):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT s.staff_id, CONCAT(s.first_name, ' ', s.last_name), s.role, s.phone, s.email
                FROM staff s
                JOIN users u ON s.user_id = u.user_id
            """
            cursor.execute(query)
            staff_members = cursor.fetchall()

            # Clear existing data
            for item in self.staff_tree.get_children():
                self.staff_tree.delete(item)

            # Insert new data
            for staff in staff_members:
                self.staff_tree.insert("", tk.END, values=staff)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load staff data: {e}")

    def show_manage_doctors(self):
        # Clear content frame
        for widget in self.admin_content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.admin_content_frame,
            text="Manage Doctors",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=10)

        # Add doctor button
        add_btn = tk.Button(
            self.admin_content_frame,
            text="Add New Doctor",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.show_add_doctor_form,
        )
        add_btn.pack(pady=10)

        # Doctors table
        columns = ("ID", "Name", "Specialization", "Phone", "Email")
        self.doctors_tree = ttk.Treeview(
            self.admin_content_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.doctors_tree.heading(col, text=col)
            self.doctors_tree.column(col, width=150, anchor=tk.CENTER)

        self.doctors_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Load doctors data
        self.load_doctors_data()

        # Action buttons frame
        action_frame = tk.Frame(self.admin_content_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)

        edit_btn = tk.Button(
            action_frame,
            text="Edit Doctor",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=self.edit_doctor,
        )
        edit_btn.grid(row=0, column=0, padx=10)

        delete_btn = tk.Button(
            action_frame,
            text="Delete Doctor",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=self.delete_doctor,
        )
        delete_btn.grid(row=0, column=1, padx=10)

    def load_doctors_data(self):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT d.doctor_id, CONCAT(d.first_name, ' ', d.last_name), d.specialization, d.phone, d.email
                FROM doctors d
                JOIN users u ON d.user_id = u.user_id
            """
            cursor.execute(query)
            doctors = cursor.fetchall()

            # Clear existing data
            for item in self.doctors_tree.get_children():
                self.doctors_tree.delete(item)

            # Insert new data
            for doctor in doctors:
                self.doctors_tree.insert("", tk.END, values=doctor)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load doctors data: {e}")

    def show_add_doctor_form(self):
        # Create a new top-level window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Doctor")
        add_window.geometry("500x600")

        tk.Label(add_window, text="Add New Doctor", font=("Arial", 18, "bold")).pack(
            pady=10
        )

        # Form fields
        fields = [
            ("First Name:", "entry"),
            ("Last Name:", "entry"),
            ("Specialization:", "entry"),
            ("Phone:", "entry"),
            ("Email:", "entry"),
            ("Username:", "entry"),
            ("Password:", "entry", True),
            ("Confirm Password:", "entry", True),
        ]

        self.doctor_form_entries = {}

        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(add_window, text=label, font=("Arial", 12)).pack(pady=5)

            if field_type == "entry":
                show = "*" if options and options[0] else ""
                entry = tk.Entry(add_window, font=("Arial", 12), show=show)
                entry.pack(pady=5, ipadx=20)
                self.doctor_form_entries[
                    label.split(":")[0].lower().replace(" ", "_")
                ] = entry

        # Submit button
        submit_btn = tk.Button(
            add_window,
            text="Add Doctor",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.add_doctor(add_window),
        )
        submit_btn.pack(pady=20)

    def add_doctor(self, window):
        # Get all form data
        first_name = self.doctor_form_entries["first_name"].get()
        last_name = self.doctor_form_entries["last_name"].get()
        specialization = self.doctor_form_entries["specialization"].get()
        phone = self.doctor_form_entries["phone"].get()
        email = self.doctor_form_entries["email"].get()
        username = self.doctor_form_entries["username"].get()
        password = self.doctor_form_entries["password"].get()
        confirm_password = self.doctor_form_entries["confirm_password"].get()

        # Validate inputs
        if not all([first_name, last_name, specialization, username, password, confirm_password]):
            messagebox.showerror("Error", "All fields except phone and email are required")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Check if username exists
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return

            # Insert user
            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)",
                (username, hashed_password, "doctor"),
            )
            user_id = cursor.lastrowid

            # Insert doctor
            cursor.execute(
                """INSERT INTO doctors 
                (user_id, first_name, last_name, specialization, phone, email) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (user_id, first_name, last_name, specialization, phone, email),
            )

            self.db_connection.commit()
            messagebox.showinfo("Success", "Doctor added successfully!")
            window.destroy()
            self.load_doctors_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to add doctor: {e}")
        finally:
            if cursor:
                cursor.close()

    def edit_doctor(self):
        selected_item = self.doctors_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a doctor to edit")
            return

        doctor_id = self.doctors_tree.item(selected_item)["values"][0]

        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT d.doctor_id, d.first_name, d.last_name, d.specialization, d.phone, d.email, u.username
                FROM doctors d
                JOIN users u ON d.user_id = u.user_id
                WHERE d.doctor_id = %s
            """
            cursor.execute(query, (doctor_id,))
            doctor_data = cursor.fetchone()

            if not doctor_data:
                messagebox.showerror("Error", "Doctor not found")
                return

            # Create edit window
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Doctor")
            edit_window.geometry("500x600")

            tk.Label(edit_window, text="Edit Doctor", font=("Arial", 18, "bold")).pack(pady=10)

            # Form fields
            fields = [
                ("First Name:", doctor_data[1]),
                ("Last Name:", doctor_data[2]),
                ("Specialization:", doctor_data[3]),
                ("Phone:", doctor_data[4]),
                ("Email:", doctor_data[5]),
                ("Username:", doctor_data[6]),
            ]

            self.edit_doctor_entries = {}

            for i, (label, value) in enumerate(fields):
                tk.Label(edit_window, text=label, font=("Arial", 12)).pack(pady=5)

                entry = tk.Entry(edit_window, font=("Arial", 12))
                entry.insert(0, value)
                entry.pack(pady=5, ipadx=20)

                self.edit_doctor_entries[
                    label.split(":")[0].lower().replace(" ", "_")
                ] = entry

            # Add password fields (optional)
            tk.Label(edit_window, text="New Password (leave blank to keep current):", font=("Arial", 12)).pack(pady=5)
            self.edit_doctor_password = tk.Entry(edit_window, font=("Arial", 12), show="*")
            self.edit_doctor_password.pack(pady=5, ipadx=20)

            tk.Label(edit_window, text="Confirm New Password:", font=("Arial", 12)).pack(pady=5)
            self.edit_doctor_confirm_password = tk.Entry(edit_window, font=("Arial", 12), show="*")
            self.edit_doctor_confirm_password.pack(pady=5, ipadx=20)

            # Submit button
            submit_btn = tk.Button(
                edit_window,
                text="Update Doctor",
                font=("Arial", 12, "bold"),
                bg="#4CAF50",
                fg="white",
                command=lambda: self.update_doctor(doctor_id, edit_window),
            )
            submit_btn.pack(pady=20)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch doctor data: {e}")

    def update_doctor(self, doctor_id, window):
        # Get all form data
        first_name = self.edit_doctor_entries["first_name"].get()
        last_name = self.edit_doctor_entries["last_name"].get()
        specialization = self.edit_doctor_entries["specialization"].get()
        phone = self.edit_doctor_entries["phone"].get()
        email = self.edit_doctor_entries["email"].get()
        username = self.edit_doctor_entries["username"].get()
        password = self.edit_doctor_password.get()
        confirm_password = self.edit_doctor_confirm_password.get()

        # Validate inputs
        if not all([first_name, last_name, specialization, username]):
            messagebox.showerror("Error", "First Name, Last Name, Specialization, and Username are required")
            return

        if password and password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Get user_id for this doctor
            cursor.execute("SELECT user_id FROM doctors WHERE doctor_id = %s", (doctor_id,))
            user_id = cursor.fetchone()[0]

            # Check if username exists (excluding current doctor)
            cursor.execute(
                "SELECT username FROM users WHERE username = %s AND user_id != %s",
                (username, user_id)
            )
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return

            # Update doctors table
            cursor.execute(
                """UPDATE doctors 
                SET first_name = %s, last_name = %s, specialization = %s, phone = %s, email = %s
                WHERE doctor_id = %s""",
                (first_name, last_name, specialization, phone, email, doctor_id),
            )

            # Update users table
            if password:
                hashed_password = self.hash_password(password)
                cursor.execute(
                    "UPDATE users SET username = %s, password = %s WHERE user_id = %s",
                    (username, hashed_password, user_id)
                )
            else:
                cursor.execute(
                    "UPDATE users SET username = %s WHERE user_id = %s",
                    (username, user_id)
                )

            self.db_connection.commit()
            messagebox.showinfo("Success", "Doctor updated successfully!")
            window.destroy()
            self.show_loading_screen(lambda: self.load_doctors_data())

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to update doctor: {e}")
        finally:
            if cursor:
                cursor.close()
                
    def delete_doctor(self):
        selected_item = self.doctors_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a doctor to delete")
            return

        doctor_id = self.doctors_tree.item(selected_item)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm", "Are you sure you want to delete this doctor?"
        )
        if not confirm:
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Get user_id for this doctor
            cursor.execute("SELECT user_id FROM doctors WHERE doctor_id = %s", (doctor_id,))
            user_id = cursor.fetchone()[0]

            # Delete from doctors table
            cursor.execute("DELETE FROM doctors WHERE doctor_id = %s", (doctor_id,))

            # Delete from users table
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

            self.db_connection.commit()
            messagebox.showinfo("Success", "Doctor deleted successfully!")
            self.load_doctors_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to delete doctor: {e}")
        finally:
            if cursor:
                cursor.close()


    def show_admin_appointments(self):
        # Clear content frame
        for widget in self.admin_content_frame.winfo_children():
            widget.destroy()

        # Header
        tk.Label(
            self.admin_content_frame,
            text="Manage Appointments",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=10)

        # Filter frame
        filter_frame = tk.Frame(self.admin_content_frame, bg="#f0f8ff")
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Filter by:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, padx=5)

        # Date filter
        self.appointment_date_filter = tk.StringVar()
        tk.Label(filter_frame, text="Date:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=1, padx=5)
        date_entry = tk.Entry(filter_frame, textvariable=self.appointment_date_filter, font=("Arial", 12))
        date_entry.grid(row=0, column=2, padx=5)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Doctor filter
        self.appointment_doctor_filter = tk.StringVar()
        tk.Label(filter_frame, text="Doctor:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=3, padx=5)
        doctor_combobox = ttk.Combobox(
            filter_frame, 
            textvariable=self.appointment_doctor_filter,
            font=("Arial", 12),
            state="readonly"
        )
        doctor_combobox.grid(row=0, column=4, padx=5)
        
        # Load doctors for filter
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT doctor_id, CONCAT(first_name, ' ', last_name) FROM doctors")
            doctors = cursor.fetchall()
            doctor_combobox['values'] = ["All"] + [f"{name} (ID: {id})" for id, name in doctors]
            doctor_combobox.set("All")
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load doctors: {e}")

        # Filter button
        filter_btn = tk.Button(
            filter_frame,
            text="Apply Filter",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=self.load_appointments_data,
        )
        filter_btn.grid(row=0, column=5, padx=10)

        # Container for treeview and scrollbars
        tree_container = tk.Frame(self.admin_content_frame)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create vertical scrollbar
        y_scrollbar = ttk.Scrollbar(tree_container)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the treeview
        columns = ("ID", "Patient", "Doctor", "Date", "Time", "Status", "Reason")
        self.appointments_tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            height=15,
            xscrollcommand=x_scrollbar.set,
            yscrollcommand=y_scrollbar.set
        )

        # Configure scrollbars
        x_scrollbar.config(command=self.appointments_tree.xview)
        y_scrollbar.config(command=self.appointments_tree.yview)

        # Configure columns
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=120, anchor=tk.CENTER, stretch=False)

        # Allow column resizing and horizontal scrolling
        for col in columns:
            self.appointments_tree.column(col, stretch=True)

        self.appointments_tree.pack(fill=tk.BOTH, expand=True)

        # Pagination controls
        self.current_page = 1
        self.appointments_per_page = 20
        
        pagination_frame = tk.Frame(self.admin_content_frame, bg="#f0f8ff")
        pagination_frame.pack(pady=10)
        
        self.page_label = tk.Label(
            pagination_frame, 
            text="Page 1 of 1", 
            font=("Arial", 10),
            bg="#f0f8ff"
        )
        self.page_label.pack(side=tk.LEFT, padx=5)
        
        self.prev_btn = tk.Button(
            pagination_frame,
            text="◀ Previous",
            font=("Arial", 10),
            command=lambda: self.change_page(-1),
            state=tk.DISABLED
        )
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = tk.Button(
            pagination_frame,
            text="Next ▶",
            font=("Arial", 10),
            command=lambda: self.change_page(1),
            state=tk.DISABLED
        )
        self.next_btn.pack(side=tk.LEFT, padx=5)

        # Action buttons frame
        action_frame = tk.Frame(self.admin_content_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)

        add_btn = tk.Button(
            action_frame,
            text="Add Appointment",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.show_add_appointment_form,
        )
        add_btn.grid(row=0, column=0, padx=10)

        edit_btn = tk.Button(
            action_frame,
            text="Edit Appointment",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=self.edit_appointment,
        )
        edit_btn.grid(row=0, column=1, padx=10)

        delete_btn = tk.Button(
            action_frame,
            text="Delete Appointment",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=self.delete_appointment,
        )
        delete_btn.grid(row=0, column=2, padx=10)

        # Load initial data
        self.load_appointments_data()

    def load_appointments_data(self):
        try:
            cursor = self.db_connection.cursor()
            
            # Base query
            query = """
                SELECT a.appointment_id, 
                    CONCAT(p.first_name, ' ', p.last_name),
                    CONCAT(d.first_name, ' ', d.last_name),
                    a.appointment_date,
                    a.appointment_time,
                    a.status,
                    a.reason
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
            """
            
            # Apply filters
            conditions = []
            params = []
            
            # Date filter
            date_filter = self.appointment_date_filter.get()
            if date_filter:
                try:
                    datetime.strptime(date_filter, "%Y-%m-%d")
                    conditions.append("a.appointment_date = %s")
                    params.append(date_filter)
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
                    return
            
            # Doctor filter
            doctor_filter = self.appointment_doctor_filter.get()
            if doctor_filter and doctor_filter != "All":
                doctor_id = doctor_filter.split("(ID: ")[1].replace(")", "")
                conditions.append("a.doctor_id = %s")
                params.append(doctor_id)
            
            # Build final query
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY a.appointment_date, a.appointment_time"
            
            # First get total count for pagination
            count_query = "SELECT COUNT(*) FROM (" + query + ") AS total"
            cursor.execute(count_query, tuple(params))
            total_appointments = cursor.fetchone()[0]
            
            # Calculate total pages
            self.total_pages = max(1, (total_appointments + self.appointments_per_page - 1) // self.appointments_per_page)
            
            # Add pagination to the query
            query += f" LIMIT {self.appointments_per_page} OFFSET {(self.current_page - 1) * self.appointments_per_page}"
            
            cursor.execute(query, tuple(params))
            appointments = cursor.fetchall()

            # Clear existing data
            for item in self.appointments_tree.get_children():
                self.appointments_tree.delete(item)

            # Insert new data
            for appointment in appointments:
                self.appointments_tree.insert("", tk.END, values=appointment)

            # Update pagination controls
            self.page_label.config(text=f"Page {self.current_page} of {self.total_pages}")
            self.prev_btn.config(state=tk.DISABLED if self.current_page == 1 else tk.NORMAL)
            self.next_btn.config(state=tk.DISABLED if self.current_page >= self.total_pages else tk.NORMAL)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load appointments: {e}")

    def change_page(self, direction):
        new_page = self.current_page + direction
        
        # Validate page bounds
        if 1 <= new_page <= self.total_pages:
            self.current_page = new_page
            self.load_appointments_data()

    # def show_add_appointment_form(self):
    #     # Create the appointment window
    #     self.add_appt_window = tk.Toplevel(self.root)
    #     self.add_appt_window.title("Admin: Add New Appointment")
    #     self.add_appt_window.geometry("650x650")
    #     self.add_appt_window.resizable(False, False)
        
    #     # Configure window styling
    #     bg_color = "#f0f8ff"
    #     self.add_appt_window.configure(bg=bg_color)
        
    #     # Header frame
    #     header_frame = tk.Frame(self.add_appt_window, bg="#3498db", height=70)
    #     header_frame.pack(fill=tk.X)
    #     tk.Label(
    #         header_frame,
    #         text="Create New Appointment",
    #         font=("Arial", 18, "bold"),
    #         bg="#3498db",
    #         fg="white"
    #     ).pack(pady=20)

    #     # Main form container
    #     form_frame = tk.Frame(self.add_appt_window, bg=bg_color, padx=25, pady=25)
    #     form_frame.pack(fill=tk.BOTH, expand=True)

    #     # Patient Selection
    #     tk.Label(
    #         form_frame,
    #         text="Select Patient:",
    #         font=("Arial", 12, "bold"),
    #         bg=bg_color
    #     ).grid(row=0, column=0, pady=10, sticky="e")

    #     self.patient_var = tk.StringVar()
    #     patient_cb = ttk.Combobox(
    #         form_frame,
    #         textvariable=self.patient_var,
    #         font=("Arial", 12),
    #         state="readonly",
    #         width=35
    #     )
    #     patient_cb.grid(row=0, column=1, pady=10, padx=10, sticky="w")

    #     # Doctor Selection
    #     tk.Label(
    #         form_frame,
    #         text="Select Doctor:",
    #         font=("Arial", 12, "bold"),
    #         bg=bg_color
    #     ).grid(row=1, column=0, pady=10, sticky="e")

    #     self.doctor_var = tk.StringVar()
    #     doctor_cb = ttk.Combobox(
    #         form_frame,
    #         textvariable=self.doctor_var,
    #         font=("Arial", 12),
    #         state="readonly",
    #         width=35
    #     )
    #     doctor_cb.grid(row=1, column=1, pady=10, padx=10, sticky="w")

    #     # Load patients and doctors
    #     try:
    #         cursor = self.db_connection.cursor()
            
    #         # Load patients in format: "John Doe (ID: 1) - Phone: 1234567890"
    #         cursor.execute("""
    #             SELECT p.patient_id, p.first_name, p.last_name, p.phone 
    #             FROM patients p
    #             JOIN users u ON p.user_id = u.user_id
    #             ORDER BY p.last_name, p.first_name
    #         """)
    #         patients = [
    #             f"{first_name} {last_name} (ID: {id}) - Phone: {phone}" 
    #             for id, first_name, last_name, phone in cursor.fetchall()
    #         ]
    #         patient_cb['values'] = patients
            
    #         # Load doctors in format: "Dr. Smith (ID: 1) - Cardiology"
    #         cursor.execute("""
    #             SELECT doctor_id, first_name, last_name, specialization 
    #             FROM doctors 
    #             ORDER BY last_name, first_name
    #         """)
    #         doctors = [
    #             f"Dr. {first_name} {last_name} (ID: {id}) - {specialization}" 
    #             for id, first_name, last_name, specialization in cursor.fetchall()
    #         ]
    #         doctor_cb['values'] = doctors
            
    #         if not patients:
    #             messagebox.showwarning("Warning", "No patients found in database")
    #         if not doctors:
    #             messagebox.showwarning("Warning", "No doctors found in database")
                
    #         if patients:
    #             patient_cb.current(0)
    #         if doctors:
    #             doctor_cb.current(0)
                
    #     except Error as e:
    #         messagebox.showerror("Database Error", f"Failed to load data: {str(e)}")
    #         self.add_appt_window.destroy()
    #         return

    #     # Date Selection
    #     tk.Label(
    #         form_frame,
    #         text="Appointment Date:",
    #         font=("Arial", 12, "bold"),
    #         bg=bg_color
    #     ).grid(row=2, column=0, pady=10, sticky="e")

    #     self.date_var = tk.StringVar()
    #     date_entry = tk.Entry(
    #         form_frame,
    #         textvariable=self.date_var,
    #         font=("Arial", 12),
    #         width=35
    #     )
    #     date_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")
    #     date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Default to today

    #     # Time Selection
    #     tk.Label(
    #         form_frame,
    #         text="Appointment Time:",
    #         font=("Arial", 12, "bold"),
    #         bg=bg_color
    #     ).grid(row=3, column=0, pady=10, sticky="e")

    #     self.time_var = tk.StringVar()
    #     time_cb = ttk.Combobox(
    #         form_frame,
    #         textvariable=self.time_var,
    #         font=("Arial", 12),
    #         values=[f"{h:02d}:{m:02d}" for h in range(8, 18) for m in [0, 30]],
    #         state="readonly",
    #         width=35
    #     )
    #     time_cb.grid(row=3, column=1, pady=10, padx=10, sticky="w")
    #     time_cb.current(0)  # Default to first time slot

    #     # Status Selection (Admin only)
    #     tk.Label(
    #         form_frame,
    #         text="Appointment Status:",
    #         font=("Arial", 12, "bold"),
    #         bg=bg_color
    #     ).grid(row=4, column=0, pady=10, sticky="e")

    #     self.status_var = tk.StringVar(value="Scheduled")
    #     status_cb = ttk.Combobox(
    #         form_frame,
    #         textvariable=self.status_var,
    #         font=("Arial", 12),
    #         values=["Scheduled", "Confirmed", "Completed", "Cancelled"],
    #         state="readonly",
    #         width=35
    #     )
    #     status_cb.grid(row=4, column=1, pady=10, padx=10, sticky="w")

    #     # Reason for Visit
    #     tk.Label(
    #         form_frame,
    #         text="Reason:",
    #         font=("Arial", 12, "bold"),
    #         bg=bg_color
    #     ).grid(row=5, column=0, pady=10, sticky="ne")

    #     self.reason_text = tk.Text(
    #         form_frame,
    #         font=("Arial", 12),
    #         height=5,
    #         width=35,
    #         wrap=tk.WORD
    #     )
    #     self.reason_text.grid(row=5, column=1, pady=10, padx=10, sticky="w")

    #     # Button Frame
    #     button_frame = tk.Frame(form_frame, bg=bg_color)
    #     button_frame.grid(row=6, column=0, columnspan=2, pady=20)

    #     # Submit Button
    #     submit_btn = tk.Button(
    #         button_frame,
    #         text="CREATE APPOINTMENT",
    #         font=("Arial", 12, "bold"),
    #         bg="#4CAF50",
    #         fg="white",
    #         width=25,
    #         height=2,
    #         command=self.admin_create_appointment
    #     )
    #     submit_btn.pack(side=tk.RIGHT, padx=10)

    #     # Cancel Button
    #     cancel_btn = tk.Button(
    #         button_frame,
    #         text="CANCEL",
    #         font=("Arial", 12),
    #         bg="#f44336",
    #         fg="white",
    #         width=15,
    #         height=2,
    #         command=self.add_appt_window.destroy
    #     )
    #     cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def show_add_appointment_form(self):
        # Create a new top-level window
        add_appt_window = tk.Toplevel(self.root)
        add_appt_window.title("Add New Appointment")
        add_appt_window.geometry("500x500")
        add_appt_window.configure(bg="#f0f8ff")

        # Header
        header_frame = tk.Frame(add_appt_window, bg="#3498db", height=60)
        header_frame.pack(fill=tk.X)
        tk.Label(
            header_frame,
            text="Add New Appointment",
            font=("Arial", 18, "bold"),
            bg="#3498db",
            fg="white"
        ).pack(pady=15)

        # Form frame
        form_frame = tk.Frame(add_appt_window, bg="#f0f8ff", padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Patient selection
        tk.Label(form_frame, text="Patient:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, pady=10, sticky="e")
        self.patient_var = tk.StringVar()
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT patient_id, CONCAT(first_name, ' ', last_name) FROM patients")
        patients = [f"{name} (ID: {id})" for id, name in cursor.fetchall()]
        self.patient_combobox = ttk.Combobox(
            form_frame,
            textvariable=self.patient_var,
            values=patients,
            font=("Arial", 12),
            state="readonly"
        )
        self.patient_combobox.grid(row=0, column=1, pady=10, sticky="w")
        if patients:
            self.patient_combobox.current(0)

        # Doctor selection
        tk.Label(form_frame, text="Doctor:", font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, pady=10, sticky="e")
        self.doctor_var = tk.StringVar()
        cursor.execute("SELECT doctor_id, CONCAT(first_name, ' ', last_name) FROM doctors")
        doctors = [f"{name} (ID: {id})" for id, name in cursor.fetchall()]
        self.doctor_combobox = ttk.Combobox(
            form_frame,
            textvariable=self.doctor_var,
            values=doctors,
            font=("Arial", 12),
            state="readonly"
        )
        self.doctor_combobox.grid(row=1, column=1, pady=10, sticky="w")
        if doctors:
            self.doctor_combobox.current(0)

        # Date
        tk.Label(form_frame, text="Date:", font=("Arial", 12), bg="#f0f8ff").grid(row=2, column=0, pady=10, sticky="e")
        self.date_var = tk.StringVar()
        date_entry = DateEntry(
            form_frame,
            textvariable=self.date_var,
            font=("Arial", 12),
            date_pattern='yyyy-mm-dd',
            width=12
        )
        date_entry.grid(row=2, column=1, pady=10, sticky="w")

        # Time
        tk.Label(form_frame, text="Time:", font=("Arial", 12), bg="#f0f8ff").grid(row=3, column=0, pady=10, sticky="e")
        self.time_var = tk.StringVar()
        time_combobox = ttk.Combobox(
            form_frame,
            textvariable=self.time_var,
            values=[f"{h:02d}:{m:02d}" for h in range(8, 18) for m in [0, 30]],
            font=("Arial", 12),
            state="readonly"
        )
        time_combobox.grid(row=3, column=1, pady=10, sticky="w")
        if time_combobox['values']:
            time_combobox.current(0)

        # Status
        tk.Label(form_frame, text="Status:", font=("Arial", 12), bg="#f0f8ff").grid(row=4, column=0, pady=10, sticky="e")
        self.status_var = tk.StringVar(value="Scheduled")
        status_combobox = ttk.Combobox(
            form_frame,
            textvariable=self.status_var,
            values=["Scheduled", "Confirmed", "Completed", "Cancelled"],
            font=("Arial", 12),
            state="readonly"
        )
        status_combobox.grid(row=4, column=1, pady=10, sticky="w")

        # Reason
        tk.Label(form_frame, text="Reason:", font=("Arial", 12), bg="#f0f8ff").grid(row=5, column=0, pady=10, sticky="ne")
        self.reason_text = tk.Text(form_frame, font=("Arial", 12), height=5, width=40, wrap=tk.WORD)
        self.reason_text.grid(row=5, column=1, pady=10, sticky="w")

        # Button frame
        button_frame = tk.Frame(form_frame, bg="#f0f8ff")
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        # Submit button
        submit_btn = tk.Button(
            button_frame,
            text="Add Appointment",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            command=lambda: self.admin_create_appointment()
        )
        submit_btn.pack(side=tk.LEFT, padx=10)

        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            command=add_appt_window.destroy
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)

        # Ensure cursor is closed
        cursor.close()
    # def show_add_appointment_form(self, is_admin=False):
    #     self.add_appt_window = tk.Toplevel(self.root)
    #     self.add_appt_window.title("Admin: Add New Appointment" if is_admin else "Book Appointment")
    #     self.add_appt_window.geometry("650x650")
    #     self.add_appt_window.resizable(False, False)
        
    #     # Configure window styling
    #     bg_color = "#f0f8ff"
    #     self.add_appt_window.configure(bg=bg_color)
        
    #     # Header frame
    #     header_frame = tk.Frame(self.add_appt_window, bg="#3498db", height=70)
    #     header_frame.pack(fill=tk.X)
    #     tk.Label(
    #         header_frame,
    #         text="Create New Appointment",
    #         font=("Arial", 18, "bold"),
    #         bg="#3498db",
    #         fg="white"
    #     ).pack(pady=20)

    #     # Main form container
    #     form_frame = tk.Frame(self.add_appt_window, bg=bg_color, padx=25, pady=25)
    #     form_frame.pack(fill=tk.BOTH, expand=True)

    #     # Patient Selection
    #     tk.Label(
    #         form_frame,
    #         text="Select Patient:",
    #         font=("Arial", 12, "bold"),
    #         bg=bg_color
    #     ).grid(row=0, column=0, pady=10, sticky="e")

    #     self.patient_var = tk.StringVar()
    #     patient_cb = ttk.Combobox(
    #         form_frame,
    #         textvariable=self.patient_var,
    #         font=("Arial", 12),
    #         state="readonly",
    #         width=35
    #     )
    #     patient_cb.grid(row=0, column=1, pady=10, padx=10, sticky="w")

    #     # Doctor Selection
    #     tk.Label(
    #         form_frame,
    #         text="Select Doctor:",
    #         font=("Arial", 12, "bold"),
    #         bg=bg_color
    #     ).grid(row=1, column=0, pady=10, sticky="e")

    #     self.doctor_var = tk.StringVar()
    #     doctor_cb = ttk.Combobox(
    #         form_frame,
    #         textvariable=self.doctor_var,
    #         font=("Arial", 12),
    #         state="readonly",
    #         width=35
    #     )
    #     doctor_cb.grid(row=1, column=1, pady=10, padx=10, sticky="w")

    #     # Load patients and doctors
    #     try:
    #         cursor = self.db_connection.cursor()
            
    #         if is_admin:
    #             # Load all patients for admin
    #             cursor.execute("""
    #                 SELECT p.patient_id, p.first_name, p.last_name, p.phone 
    #                 FROM patients p
    #                 JOIN users u ON p.user_id = u.user_id
    #                 ORDER BY p.last_name, p.first_name
    #             """)
    #             patients = [
    #                 f"{first_name} {last_name} (ID: {id}) - Phone: {phone}" 
    #                 for id, first_name, last_name, phone in cursor.fetchall()
    #             ]
    #         else:
    #             # Load only current patient for patient view
    #             cursor.execute("""
    #                 SELECT p.patient_id, p.first_name, p.last_name, p.phone 
    #                 FROM patients p
    #                 WHERE p.user_id = %s
    #             """, (self.current_user_id,))
    #             patient_data = cursor.fetchone()
    #             if patient_data:
    #                 patients = [f"{patient_data[1]} {patient_data[2]} (ID: {patient_data[0]}) - Phone: {patient_data[3]}"]
    #             else:
    #                 patients = []
            
    #         patient_cb['values'] = patients
            
    #         # Load doctors
    #         cursor.execute("""
    #             SELECT doctor_id, first_name, last_name, specialization 
    #             FROM doctors 
    #             ORDER BY last_name, first_name
    #         """)
    #         doctors = [
    #             f"Dr. {first_name} {last_name} (ID: {id}) - {specialization}" 
    #             for id, first_name, last_name, specialization in cursor.fetchall()
    #         ]
    #         doctor_cb['values'] = doctors
            
    #         if not patients:
    #             messagebox.showwarning("Warning", "No patients found")
    #         if not doctors:
    #             messagebox.showwarning("Warning", "No doctors found")
                
    #         if patients:
    #             patient_cb.current(0)
    #         if doctors:
    #             doctor_cb.current(0)
                
    #     except Error as e:
    #         messagebox.showerror("Database Error", f"Failed to load data: {str(e)}")
    #         self.add_appt_window.destroy()
    #         return

    #     # Date Selection
    #     tk.Label(
    #         form_frame,
    #         text="Appointment Date:",
    #         font=("Arial", 12, "bold"),
    #         bg=bg_color
    #     ).grid(row=2, column=0, pady=10, sticky="e")

    #     self.date_var = DateEntry(
    #         form_frame,
    #         font=("Arial", 12),
    #         date_pattern='yyyy-mm-dd',
    #         width=12
    #     )
    #     self.date_var.grid(row=2, column=1, pady=10, padx=10, sticky="w")
    #     self.date_var.set_date(datetime.now())  # Default to today

    #     # Time Selection
    #     tk.Label(
    #         form_frame,
    #         text="Appointment Time:",
    #         font=("Arial", 12, "bold"),
    #         bg=bg_color
    #     ).grid(row=3, column=0, pady=10, sticky="e")

    #     self.time_var = ttk.Combobox(
    #         form_frame,
    #         textvariable=self.time_var,
    #         font=("Arial", 12),
    #         values=[f"{h:02d}:{m:02d}" for h in range(8, 18) for m in [0, 30]],
    #         state="readonly",
    #         width=35
    #     )
    #     self.time_var.grid(row=3, column=1, pady=10, padx=10, sticky="w")
    #     self.time_var.current(0)  # Default to first time slot

    #     # Status Selection (only for admin)
    #     if is_admin:
    #         tk.Label(
    #             form_frame,
    #             text="Appointment Status:",
    #             font=("Arial", 12, "bold"),
    #             bg=bg_color
    #         ).grid(row=4, column=0, pady=10, sticky="e")

    #         self.status_var = tk.StringVar(value="Scheduled")
    #         status_cb = ttk.Combobox(
    #             form_frame,
    #             textvariable=self.status_var,
    #             font=("Arial", 12),
    #             values=["Scheduled", "Confirmed", "Completed", "Cancelled"],
    #             state="readonly",
    #             width=35
    #         )
    #         status_cb.grid(row=4, column=1, pady=10, padx=10, sticky="w")

    #     # Reason for Visit
    #     tk.Label(
    #         form_frame,
    #         text="Reason:",
    #         font=("Arial", 12, "bold"),
    #         bg=bg_color
    #     ).grid(row=5 if is_admin else 4, column=0, pady=10, sticky="ne")

    #     self.reason_text = tk.Text(
    #         form_frame,
    #         font=("Arial", 12),
    #         height=5,
    #         width=35,
    #         wrap=tk.WORD
    #     )
    #     self.reason_text.grid(row=5 if is_admin else 4, column=1, pady=10, padx=10, sticky="w")

    #     # Button Frame
    #     button_frame = tk.Frame(form_frame, bg=bg_color)
    #     button_frame.grid(row=6 if is_admin else 5, column=0, columnspan=2, pady=20)

    #     # Submit Button
    #     submit_btn = tk.Button(
    #         button_frame,
    #         text="CREATE APPOINTMENT",
    #         font=("Arial", 12, "bold"),
    #         bg="#4CAF50",
    #         fg="white",
    #         width=25,
    #         height=2,
    #         command=lambda: self.create_appointment(is_admin)
    #     )
    #     submit_btn.pack(side=tk.RIGHT, padx=10)

    #     # Cancel Button
    #     cancel_btn = tk.Button(
    #         button_frame,
    #         text="CANCEL",
    #         font=("Arial", 12),
    #         bg="#f44336",
    #         fg="white",
    #         width=15,
    #         height=2,
    #         command=self.add_appt_window.destroy
    #     )
    #     cancel_btn.pack(side=tk.LEFT, padx=10)
        
    def create_appointment(self, is_admin=False):
        try:
            # Get values from form
            patient_str = self.patient_var.get()
            doctor_str = self.doctor_var.get()
            date = self.date_var.get_date().strftime("%Y-%m-%d")
            time = self.time_var.get()
            reason = self.reason_text.get("1.0", tk.END).strip()
            status = self.status_var.get() if is_admin else "Scheduled"

            # Validate required fields
            if not all([patient_str, doctor_str, date, time]):
                messagebox.showerror("Error", "Please fill all required fields")
                return

            # Extract IDs from strings
            try:
                patient_id = int(patient_str.split("(ID: ")[1].split(")")[0])
                doctor_id = int(doctor_str.split("(ID: ")[1].split(")")[0])
            except (IndexError, ValueError):
                messagebox.showerror("Error", "Invalid patient or doctor selection")
                return

            # Validate date and time
            try:
                datetime.strptime(date, "%Y-%m-%d")
                datetime.strptime(time, "%H:%M")
            except ValueError:
                messagebox.showerror("Error", "Invalid date or time format")
                return

            # Insert into database
            cursor = self.db_connection.cursor()
            cursor.execute(
                """INSERT INTO appointments 
                (patient_id, doctor_id, appointment_date, appointment_time, status, reason) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (patient_id, doctor_id, date, time, status, reason if reason else None)
            )
            
            # Get the new appointment ID
            appointment_id = cursor.lastrowid
            
            # Get patient and doctor names for notification
            cursor.execute(
                "SELECT CONCAT(first_name, ' ', last_name) FROM patients WHERE patient_id = %s",
                (patient_id,)
            )
            patient_name = cursor.fetchone()[0]
            
            cursor.execute(
                "SELECT CONCAT(first_name, ' ', last_name) FROM doctors WHERE doctor_id = %s",
                (doctor_id,)
            )
            doctor_name = cursor.fetchone()[0]
            
            # Get patient email
            cursor.execute(
                "SELECT email FROM patients WHERE patient_id = %s",
                (patient_id,)
            )
            patient_email = cursor.fetchone()[0]

            self.db_connection.commit()
            
            # Send confirmation email
            subject = "Appointment Confirmation"
            body = (
                f"Dear {patient_name},\n\n"
                f"Your appointment has been successfully booked.\n"
                f"Appointment ID: {appointment_id}\n"
                f"Date: {date}\n"
                f"Time: {time}\n"
                f"Doctor: {doctor_name}\n"
                f"Status: {status}\n"
                f"Reason: {reason if reason else 'Not specified'}\n\n"
                f"Thank you for choosing our hospital."
            )
            self.send_email_notification(patient_email, subject, body)
            
            messagebox.showinfo("Success", "Appointment booked successfully!")
            self.add_appt_window.destroy()
            
            # Refresh appointments view
            if is_admin:
                self.load_appointments_data()
            else:
                self.load_patient_appointments(self.current_user_id)

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to create appointment: {e}")
        finally:
            cursor.close()
        
    def submit_appointment(self, user_id, window):
        doctor_str = self.doctor_var.get()
        date = self.date_var.get_date()
        time = self.time_var.get()
        reason = self.reason_text.get("1.0", tk.END).strip()

        if not all([doctor_str, date, time]):
            messagebox.showerror("Error", "All fields except reason are required")
            return

        try:
            doctor_id = int(doctor_str.split("(ID: ")[1].replace(")", ""))
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT patient_id, email, CONCAT(first_name, ' ', last_name) FROM patients WHERE user_id = %s", (user_id,))
            patient_data = cursor.fetchone()
            if not patient_data:
                messagebox.showerror("Error", "Patient not found")
                return
            patient_id, patient_email, patient_name = patient_data

            cursor.execute("SELECT CONCAT(first_name, ' ', last_name) FROM doctors WHERE doctor_id = %s", (doctor_id,))
            doctor_name = cursor.fetchone()[0]

            cursor.execute(
                """INSERT INTO appointments 
                (patient_id, doctor_id, appointment_date, appointment_time, status, reason) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (patient_id, doctor_id, date, time, "Scheduled", reason if reason else None)
            )
            appointment_id = cursor.lastrowid
            self.db_connection.commit()

            subject = "Appointment Confirmation - Grow Up Hospital"
            body = (
                f"Dear {patient_name},\n\n"
                f"Your appointment has been successfully booked.\n"
                f"Appointment ID: {appointment_id}\n"
                f"Date: {date}\n"
                f"Time: {time}\n"
                f"Doctor: {doctor_name}\n"
                f"Status: Scheduled\n"
                f"Reason: {reason if reason else 'Not specified'}\n\n"
                f"Thank you for choosing Grow Up Hospital."
            )
            self.send_email_notification(patient_email, subject, body)
            messagebox.showinfo("Success", "Appointment booked successfully!")
            window.destroy()
            if hasattr(self, 'load_patient_appointments'):
                self.load_patient_appointments(user_id)

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to book appointment: {e}")
        finally:
            cursor.close()
        
    def add_appointment(self, user_id):
        add_window = tk.Toplevel(self.root)
        add_window.title("Book Appointment")
        add_window.geometry("500x500")
        add_window.configure(bg="#f0f8ff")

        tk.Label(add_window, text="Book Appointment", font=("Arial", 18, "bold"), bg="#f0f8ff").pack(pady=10)

        tk.Label(add_window, text="Doctor:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT doctor_id, CONCAT(first_name, ' ', last_name) FROM doctors")
        doctors = [f"{name} (ID: {id})" for id, name in cursor.fetchall()]
        self.doctor_var = tk.StringVar()
        doctor_combobox = ttk.Combobox(add_window, textvariable=self.doctor_var, values=doctors, state="readonly")
        doctor_combobox.pack(pady=5)
        if doctors:
            doctor_combobox.current(0)

        tk.Label(add_window, text="Date:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
        self.date_var = DateEntry(add_window, date_pattern='yyyy-mm-dd', width=12)
        self.date_var.pack(pady=5)

        tk.Label(add_window, text="Time:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
        self.time_var = ttk.Combobox(add_window, values=[f"{h:02d}:{m:02d}" for h in range(8, 18) for m in [0, 30]], state="readonly")
        self.time_var.pack(pady=5)
        self.time_var.current(0)

        tk.Label(add_window, text="Reason:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
        self.reason_text = tk.Text(add_window, height=5, width=40)
        self.reason_text.pack(pady=5)

        submit_btn = tk.Button(
            add_window,
            text="Book Appointment",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.submit_appointment(user_id, add_window)
        )
        submit_btn.pack(pady=20)

        
    def edit_appointment(self):
        selected_item = self.appointments_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an appointment to edit")
            return

        appointment_id = self.appointments_tree.item(selected_item)["values"][0]

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT a.appointment_id, 
                        CONCAT(p.first_name, ' ', p.last_name, ' (ID: ', p.patient_id, ')'),
                        CONCAT(d.first_name, ' ', d.last_name, ' (ID: ', d.doctor_id, ')'),
                        a.appointment_date,
                        a.appointment_time,
                        a.status,
                        a.reason
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE a.appointment_id = %s""",
                (appointment_id,)
            )
            appointment_data = cursor.fetchone()

            if not appointment_data:
                messagebox.showerror("Error", "Appointment not found")
                return

            # Create edit window with scrollable frame
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Appointment")
            edit_window.geometry("600x500")
            edit_window.resizable(True, True)

            # Create main container frame
            main_frame = tk.Frame(edit_window)
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Create canvas and scrollbar
            canvas = tk.Canvas(main_frame)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            # Configure the canvas
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Pack the canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Title
            tk.Label(
                scrollable_frame,
                text="Edit Appointment",
                font=("Arial", 18, "bold")
            ).pack(pady=10)

            # Form fields
            fields = [
                ("Patient:", appointment_data[1], False),
                ("Doctor:", appointment_data[2], False),
                ("Date (YYYY-MM-DD):", appointment_data[3], True),
                ("Time (HH:MM):", appointment_data[4], True),
                ("Status:", appointment_data[5], True),
                ("Reason:", appointment_data[6], True),
            ]

            self.edit_appointment_entries = {}

            for label, value, editable in fields:
                frame = tk.Frame(scrollable_frame)
                frame.pack(fill=tk.X, padx=10, pady=5)
                
                tk.Label(frame, text=label, font=("Arial", 12)).pack(side=tk.LEFT)

                if not editable:
                    tk.Label(frame, text=value, font=("Arial", 12)).pack(side=tk.LEFT)
                    continue

                if label == "Status:":
                    entry = ttk.Combobox(
                        frame,
                        values=["Scheduled", "Completed", "Cancelled", "No Show"],
                        font=("Arial", 12),
                        state="readonly"
                    )
                    entry.set(value)
                elif label == "Reason:":
                    entry = tk.Text(
                        frame,
                        font=("Arial", 12),
                        height=4,
                        width=40
                    )
                    entry.insert("1.0", value)
                else:
                    entry = tk.Entry(frame, font=("Arial", 12))
                    entry.insert(0, value)

                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                # Create consistent key
                key = label.split(":")[0].lower().replace(" ", "_")
                self.edit_appointment_entries[key] = entry

            # Button frame
            button_frame = tk.Frame(scrollable_frame)
            button_frame.pack(pady=20)

            # Submit button
            submit_btn = tk.Button(
                button_frame,
                text="Update Appointment",
                font=("Arial", 12, "bold"),
                bg="#4CAF50",
                fg="white",
                command=lambda: self.update_appointment(appointment_id, edit_window),
            )
            submit_btn.pack(side=tk.LEFT, padx=10)

            # Cancel button
            cancel_btn = tk.Button(
                button_frame,
                text="Cancel",
                font=("Arial", 12),
                bg="#f44336",
                fg="white",
                command=edit_window.destroy,
            )
            cancel_btn.pack(side=tk.LEFT, padx=10)

            # Add mousewheel scrolling support
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            edit_window.bind("<MouseWheel>", _on_mousewheel)
            scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch appointment data: {e}")

    def update_appointment(self, appointment_id, edit_window):
        try:
            # Get values from form fields
            date = self.edit_appointment_entries["date_(yyyy-mm-dd)"].get()
            time = self.edit_appointment_entries["time_(hh"].get()
            
            # Handle status (Combobox)
            status = self.edit_appointment_entries["status"].get()
            
            # Handle reason (Text widget)
            reason = self.edit_appointment_entries["reason"].get("1.0", "end-1c")

            # Validate inputs
            if not all([date, time, status]):
                messagebox.showerror("Error", "Required fields are missing")
                return

            # Update database - USE CONSISTENT db_connection
            cursor = self.db_connection.cursor()
            query = """UPDATE appointments 
                    SET appointment_date = %s, 
                        appointment_time = %s, 
                        status = %s, 
                        reason = %s
                    WHERE appointment_id = %s"""
            cursor.execute(query, (date, time, status, reason, appointment_id))
            self.db_connection.commit()

            # Refresh UI and close window
            self.load_appointments_data()  # Use consistent refresh method name
            edit_window.destroy()
            messagebox.showinfo("Success", "Appointment updated successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {str(e)}")
            if self.db_connection:
                self.db_connection.rollback()
            
    def delete_appointment(self):
        selected_item = self.appointments_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an appointment to delete")
            return

        appointment_id = self.appointments_tree.item(selected_item)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm", "Are you sure you want to delete this appointment?"
        )
        if not confirm:
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            cursor.execute(
                "DELETE FROM appointments WHERE appointment_id = %s",
                (appointment_id,)
            )

            self.db_connection.commit()
            messagebox.showinfo("Success", "Appointment deleted successfully!")
            self.load_appointments_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to delete appointment: {e}")
        finally:
            if cursor:
                cursor.close()
                
    def create_edit_appointment_form(self, appointment_data):
            self.edit_appointment_entries = {}
            # Date entry
            ttk.Label(edit_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5) # type: ignore
            self.edit_appointment_entries["date_(yyyy-mm-dd)"] = ttk.Entry(edit_frame)
            self.edit_appointment_entries["date_(yyyy-mm-dd)"].grid(row=0, column=1, padx=5, pady=5)
            self.edit_appointment_entries["date_(yyyy-mm-dd)"].insert(0, appointment_data['date'])
            
            # Time entry
            ttk.Label(edit_frame, text="Time (HH:MM):").grid(row=1, column=0, padx=5, pady=5) # type: ignore
            self.edit_appointment_entries["time_(hh"] = ttk.Entry(edit_frame)  # Note: Fix key naming
            self.edit_appointment_entries["time_(hh"].grid(row=1, column=1, padx=5, pady=5)
            self.edit_appointment_entries["time_(hh"].insert(0, appointment_data['time'])
            
            # Status dropdown
            ttk.Label(edit_frame, text="Status:").grid(row=2, column=0, padx=5, pady=5)
            self.edit_appointment_entries["status"] = ttk.Combobox(edit_frame, 
                                                                values=["Scheduled", "Completed", "Cancelled"])
            self.edit_appointment_entries["status"].grid(row=2, column=1, padx=5, pady=5)
            self.edit_appointment_entries["status"].set(appointment_data['status'])
            
            # Reason entry
            ttk.Label(edit_frame, text="Reason:").grid(row=3, column=0, padx=5, pady=5)
            self.edit_appointment_entries["reason"] = ttk.Entry(edit_frame)
            self.edit_appointment_entries["reason"].grid(row=3, column=1, padx=5, pady=5)
            self.edit_appointment_entries["reason"].insert(0, appointment_data.get('reason', ''))


    def show_reports(self):
        for widget in self.admin_content_frame.winfo_children():
            widget.destroy()

        scrolled_frame = tk.Frame(self.admin_content_frame)
        scrolled_frame.pack(fill=tk.BOTH, expand=True)

        y_scrollbar = ttk.Scrollbar(scrolled_frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas = tk.Canvas(scrolled_frame, yscrollcommand=y_scrollbar.set, bg="#e0f7fa")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.config(command=canvas.yview)

        inner_frame = tk.Frame(canvas, bg="#e0f7fa")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner_frame.bind("<Configure>", configure_scroll_region)

        title_label = tk.Label(
            inner_frame,
            text="Hospital Analytics Dashboard",
            font=("Helvetica", 22, "bold"),
            bg="#1a252f",
            fg="#e0f7fa",
            pady=15,
            relief="flat"
        )
        title_label.pack(fill=tk.X)

        filter_frame = tk.Frame(inner_frame, bg="#2a3d4e")
        filter_frame.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(filter_frame, text="From Date:", font=("Helvetica", 12), bg="#2a3d4e", fg="#e0f7fa").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.from_date_entry = DateEntry(
            filter_frame,
            font=("Helvetica", 12),
            date_pattern='yyyy-mm-dd',
            width=12,
            background='#e0f7fa',
            foreground='#1a252f',
            bordercolor='#4dd0e1',
            selectbackground='#4dd0e1',
            selectforeground='#1a252f'
        )
        self.from_date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.from_date_entry.set_date(datetime.now().replace(day=1))

        tk.Label(filter_frame, text="To Date:", font=("Helvetica", 12), bg="#2a3d4e", fg="#e0f7fa").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.to_date_entry = DateEntry(
            filter_frame,
            font=("Helvetica", 12),
            date_pattern='yyyy-mm-dd',
            width=12,
            background='#e0f7fa',
            foreground='#1a252f',
            bordercolor='#4dd0e1',
            selectbackground='#4dd0e1',
            selectforeground='#1a252f'
        )
        self.to_date_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.to_date_entry.set_date(datetime.now())

        tk.Label(filter_frame, text="Report Type:", font=("Helvetica", 12), bg="#2a3d4e", fg="#e0f7fa").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.report_type_var = tk.StringVar(value="Summary")
        report_types = ttk.Combobox(
            filter_frame,
            textvariable=self.report_type_var,
            values=["Summary", "Patients", "Appointments", "Financial", "Staff", "Patient Payments"],
            font=("Helvetica", 12),
            state="readonly",
            width=15,
            style="Custom.TCombobox"
        )
        report_types.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        report_types.bind("<<ComboboxSelected>>", self.update_additional_filters)

        generate_btn = tk.Button(
            filter_frame,
            text="Generate Report",
            font=("Helvetica", 12, "bold"),
            bg="#ff6f61",
            fg="white",
            activebackground="#e55b4d",
            relief="flat",
            padx=10,
            pady=5,
            command=self.generate_report_data
        )
        generate_btn.grid(row=0, column=6, padx=10, pady=5)

        self.additional_filters_frame = tk.Frame(inner_frame, bg="#2a3d4e")
        self.additional_filters_frame.pack(pady=5, fill=tk.X)

        tree_container = tk.Frame(inner_frame, bg="#e0f7fa")
        tree_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview",
                        background="#ffffff",
                        foreground="#1a252f",
                        fieldbackground="#e0f7fa",
                        borderwidth=0,
                        relief="flat")
        style.map("Custom.Treeview",
                 background=[('selected', '#4dd0e1')],
                 foreground=[('selected', '#ffffff')])
        style.configure("Custom.Treeview.Heading",
                        background="#4dd0e1",
                        foreground="#ffffff",
                        font=('Helvetica', 11, 'bold'),
                        borderwidth=0,
                        relief="flat")
        style.configure("Custom.TCombobox",
                        fieldbackground="#e0f7fa",
                        background="#4dd0e1",
                        foreground="#1a252f")

        x_scrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, style="TScrollbar")
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        y_scrollbar = ttk.Scrollbar(tree_container, style="TScrollbar")
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.report_tree = ttk.Treeview(
            tree_container,
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set,
            height=15,
            style="Custom.Treeview",
            show='tree headings'
        )
        self.report_tree.pack(fill=tk.BOTH, expand=True)
        y_scrollbar.config(command=self.report_tree.yview)
        x_scrollbar.config(command=self.report_tree.xview)

        button_frame = tk.Frame(inner_frame, bg="#2a3d4e")
        button_frame.pack(pady=10, fill=tk.X)
        
        tk.Button(
            button_frame,
            text="Export to PDF",
            font=("Helvetica", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            relief="flat",
            padx=10,
            pady=5,
            command=self.export_report_to_pdf
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="Export to Excel",
            font=("Helvetica", 12, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            relief="flat",
            padx=10,
            pady=5,
            command=self.export_report_to_excel
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="Print Report",
            font=("Helvetica", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            relief="flat",
            padx=10,
            pady=5,
            command=self.print_report
        ).pack(side=tk.LEFT, padx=10)

        self.report_status = tk.Label(
            inner_frame,
            text="Ready to generate report",
            font=("Helvetica", 10),
            bg="#2a3d4e",
            fg="#e0f7fa",
            anchor='w'
        )
        self.report_status.pack(fill=tk.X, padx=20, pady=(0, 10))

        self.update_additional_filters()
        self.generate_report_data()

    def update_additional_filters(self, event=None):
        for widget in self.additional_filters_frame.winfo_children():
            widget.destroy()

        report_type = self.report_type_var.get()
        if report_type == "Appointments":
            tk.Label(self.additional_filters_frame, text="Status:", bg="#2a3d4e", fg="#e0f7fa").pack(side=tk.LEFT, padx=5)
            self.appt_status_var = tk.StringVar(value="All")
            ttk.Combobox(
                self.additional_filters_frame,
                textvariable=self.appt_status_var,
                values=["All", "Scheduled", "Confirmed", "Completed", "Cancelled"],
                state="readonly",
                width=12,
                style="Custom.TCombobox"
            ).pack(side=tk.LEFT, padx=5)
        elif report_type == "Financial":
            tk.Label(self.additional_filters_frame, text="Payment Status:", bg="#2a3d4e", fg="#e0f7fa").pack(side=tk.LEFT, padx=5)
            self.payment_status_var = tk.StringVar(value="All")
            ttk.Combobox(
                self.additional_filters_frame,
                textvariable=self.payment_status_var,
                values=["All", "Paid", "Pending", "Partially Paid"],
                state="readonly",
                width=12,
                style="Custom.TCombobox"
            ).pack(side=tk.LEFT, padx=5)
        elif report_type == "Patient Payments":
            tk.Label(self.additional_filters_frame, text="Payment Status:", bg="#2a3d4e", fg="#e0f7fa").pack(side=tk.LEFT, padx=5)
            self.patient_payment_var = tk.StringVar(value="All")
            ttk.Combobox(
                self.additional_filters_frame,
                textvariable=self.patient_payment_var,
                values=["All", "Paid", "Pending", "Partially Paid"],
                state="readonly",
                width=12,
                style="Custom.TCombobox"
            ).pack(side=tk.LEFT, padx=5)

    def generate_report_data(self):
        from_date = self.from_date_entry.get_date().strftime('%Y-%m-%d')
        to_date = self.to_date_entry.get_date().strftime('%Y-%m-%d')
        report_type = self.report_type_var.get()
        cursor = None

        try:
            cursor = self.db_connection.cursor(dictionary=True)
            self.report_tree.delete(*self.report_tree.get_children())
            self.report_tree["columns"] = ()

            column_widths = {
                "Summary": {"Metric": 250, "Value": 150},
                "Patients": {col: 120 for col in ("Patient ID", "Name", "Gender", "DOB", "Blood Type", "Phone")},
                "Appointments": {col: 120 for col in ("Appointment ID", "Date", "Time", "Patient", "Doctor", "Status", "Reason")},
                "Financial": {col: 120 for col in ("Bill ID", "Date", "Patient", "Amount", "Description", "Status")},
                "Staff": {col: 120 for col in ("Staff ID", "Name", "Role", "Phone", "Email")},
                "Patient Payments": {col: 120 for col in ("Patient ID", "Name", "Total Amount", "Paid Amount", "Unpaid Amount", "Status")}
            }

            if report_type == "Summary":
                self.report_tree["columns"] = ("Metric", "Value")
                for col in self.report_tree["columns"]:
                    self.report_tree.heading(col, text=col, anchor=tk.W)
                    self.report_tree.column(col, width=column_widths["Summary"][col], anchor=tk.W, stretch=True)

                summary_data = []
                cursor.execute("SELECT COUNT(DISTINCT patient_id) as count FROM appointments WHERE created_at BETWEEN %s AND %s", (from_date, to_date))
                patient_count = cursor.fetchone()['count'] or 0
                summary_data.append(("Patients with Appointments", patient_count))

                cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE appointment_date BETWEEN %s AND %s", (from_date, to_date))
                appointments_count = cursor.fetchone()['count']
                summary_data.append(("Appointments Booked", appointments_count))

                cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE status = 'Completed' AND appointment_date BETWEEN %s AND %s", (from_date, to_date))
                completed_count = cursor.fetchone()['count']
                summary_data.append(("Appointments Completed", completed_count))

                cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE status = 'Cancelled' AND appointment_date BETWEEN %s AND %s", (from_date, to_date))
                cancelled_count = cursor.fetchone()['count']
                summary_data.append(("Appointments Cancelled", cancelled_count))

                cursor.execute("SELECT SUM(amount) as total FROM billing WHERE payment_status = 'Paid' AND bill_date BETWEEN %s AND %s", (from_date, to_date))
                revenue = cursor.fetchone()['total'] or 0
                summary_data.append(("Total Revenue", f"${revenue:.2f}"))

                cursor.execute("SELECT COUNT(*) as count FROM doctors")
                doctor_count = cursor.fetchone()['count']
                summary_data.append(("Total Doctors", doctor_count))

                cursor.execute("SELECT COUNT(*) as count FROM staff")
                staff_count = cursor.fetchone()['count']
                summary_data.append(("Total Staff", staff_count))

                parent = self.report_tree.insert("", tk.END, text="Summary Metrics")
                for metric, value in summary_data:
                    self.report_tree.insert(parent, tk.END, values=(metric, value))
                self.report_status.config(text=f"Generated summary report from {from_date} to {to_date}")

            elif report_type == "Patients":
                columns = ("Patient ID", "Name", "Gender", "DOB", "Blood Type", "Phone")
                self.report_tree["columns"] = columns
                for col in columns:
                    self.report_tree.heading(col, text=col, anchor=tk.W)
                    self.report_tree.column(col, width=column_widths["Patients"][col], anchor=tk.W, stretch=True)

                query = """
                    SELECT p.patient_id, CONCAT(p.first_name, ' ', COALESCE(p.last_name, '')) as name, 
                           p.gender, p.date_of_birth, p.blood_type, p.phone 
                    FROM patients p 
                    ORDER BY p.patient_id
                """
                cursor.execute(query)
                results = cursor.fetchall()

                parent = self.report_tree.insert("", tk.END, text="Patients")
                for row in results:
                    values = (
                        row['patient_id'],
                        row['name'] or 'Unknown',
                        row['gender'],
                        row['date_of_birth'].strftime('%Y-%m-%d') if row['date_of_birth'] else 'N/A',
                        row['blood_type'] or 'N/A',
                        row['phone'] or 'N/A'
                    )
                    self.report_tree.insert(parent, tk.END, values=values)
                self.report_status.config(text=f"Total Patients: {len(results)}")

            elif report_type == "Appointments":
                columns = ("Appointment ID", "Date", "Time", "Patient", "Doctor", "Status", "Reason")
                self.report_tree["columns"] = columns
                for col in columns:
                    self.report_tree.heading(col, text=col, anchor=tk.W)
                    self.report_tree.column(col, width=column_widths["Appointments"][col], anchor=tk.W, stretch=True)

                status = getattr(self, 'appt_status_var', tk.StringVar(value="All")).get()
                query = """
                    SELECT a.appointment_id, a.appointment_date, a.appointment_time,
                          CONCAT(p.first_name, ' ', COALESCE(p.last_name, '')) as patient_name,
                          CONCAT(d.first_name, ' ', COALESCE(d.last_name, '')) as doctor_name,
                          a.status, a.reason
                    FROM appointments a
                    LEFT JOIN patients p ON a.patient_id = p.patient_id
                    LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
                    WHERE a.appointment_date BETWEEN %s AND %s
                """
                params = [from_date, to_date]
                if status != "All":
                    query += " AND a.status = %s"
                    params.append(status)
                cursor.execute(query, tuple(params))
                results = cursor.fetchall()

                parent = self.report_tree.insert("", tk.END, text="Appointments")
                for row in results:
                    time_str = 'N/A'
                    if row['appointment_time']:
                        if isinstance(row['appointment_time'], timedelta):
                            total_seconds = int(row['appointment_time'].total_seconds())
                            hours = total_seconds // 3600
                            minutes = (total_seconds % 3600) // 60
                            time_str = f"{hours:02d}:{minutes:02d}"
                        elif hasattr(row['appointment_time'], 'strftime'):
                            time_str = row['appointment_time'].strftime('%H:%M')
                    values = (
                        row['appointment_id'] or 'N/A',
                        row['appointment_date'].strftime('%Y-%m-%d') if row['appointment_date'] else 'N/A',
                        time_str,
                        row['patient_name'] or 'Unknown',
                        row['doctor_name'] or 'Unknown',
                        row['status'] or 'N/A',
                        row['reason'] or 'N/A'
                    )
                    self.report_tree.insert(parent, tk.END, values=values)
                self.report_status.config(text=f"Total Appointments: {len(results)}")

            elif report_type == "Financial":
                columns = ("Bill ID", "Date", "Patient", "Amount", "Description", "Status")
                self.report_tree["columns"] = columns
                for col in columns:
                    self.report_tree.heading(col, text=col, anchor=tk.W)
                    self.report_tree.column(col, width=column_widths["Financial"][col], anchor=tk.W, stretch=True)

                payment_status = getattr(self, 'payment_status_var', tk.StringVar(value="All")).get()
                query = """
                    SELECT b.bill_id, b.bill_date, CONCAT(p.first_name, ' ', COALESCE(p.last_name, '')) as patient_name,
                           b.amount, b.description, b.payment_status
                    FROM billing b
                    LEFT JOIN patients p ON b.patient_id = p.patient_id
                    WHERE b.bill_date BETWEEN %s AND %s
                """
                params = [from_date, to_date]
                if payment_status != "All":
                    query += " AND b.payment_status = %s"
                    params.append(payment_status)
                cursor.execute(query, tuple(params))
                results = cursor.fetchall()

                parent = self.report_tree.insert("", tk.END, text="Financial Records")
                total_amount = sum(row['amount'] for row in results)
                paid_amount = sum(row['amount'] for row in results if row['payment_status'] == "Paid")
                for row in results:
                    values = (
                        row['bill_id'],
                        row['bill_date'].strftime('%Y-%m-%d') if row['bill_date'] else 'N/A',
                        row['patient_name'] or 'Unknown',
                        f"${row['amount']:.2f}",
                        row['description'] or 'N/A',
                        row['payment_status']
                    )
                    self.report_tree.insert(parent, tk.END, values=values)
                self.report_status.config(
                    text=f"Total Amount: ${total_amount:.2f} | Paid: ${paid_amount:.2f} | Pending: ${total_amount-paid_amount:.2f}"
                )

            elif report_type == "Staff":
                columns = ("Staff ID", "Name", "Role", "Phone", "Email")
                self.report_tree["columns"] = columns
                for col in columns:
                    self.report_tree.heading(col, text=col, anchor=tk.W)
                    self.report_tree.column(col, width=column_widths["Staff"][col], anchor=tk.W, stretch=True)

                query = """
                    SELECT s.staff_id, CONCAT(s.first_name, ' ', s.last_name) as name, s.role, s.phone, s.email 
                    FROM staff s 
                    ORDER BY s.staff_id
                """
                cursor.execute(query)
                results = cursor.fetchall()

                parent = self.report_tree.insert("", tk.END, text="Staff")
                for row in results:
                    values = (
                        row['staff_id'],
                        row['name'],
                        row['role'],
                        row['phone'] or 'N/A',
                        row['email'] or 'N/A'
                    )
                    self.report_tree.insert(parent, tk.END, values=values)
                self.report_status.config(text=f"Total Staff: {len(results)}")

            elif report_type == "Patient Payments":
                columns = ("Patient ID", "Name", "Total Amount", "Paid Amount", "Unpaid Amount", "Status")
                self.report_tree["columns"] = columns
                for col in columns:
                    self.report_tree.heading(col, text=col, anchor=tk.W)
                    self.report_tree.column(col, width=column_widths["Patient Payments"][col], anchor=tk.W, stretch=True)

                payment_status = getattr(self, 'patient_payment_var', tk.StringVar(value="All")).get()
                query = """
                    SELECT p.patient_id, CONCAT(p.first_name, ' ', COALESCE(p.last_name, '')) as name,
                           SUM(b.amount) as total_amount,
                           SUM(CASE WHEN b.payment_status = 'Paid' THEN b.amount ELSE 0 END) as paid_amount,
                           SUM(CASE WHEN b.payment_status IN ('Pending', 'Partially Paid') THEN b.amount ELSE 0 END) as unpaid_amount,
                           CASE
                               WHEN SUM(CASE WHEN b.payment_status IN ('Pending', 'Partially Paid') THEN b.amount ELSE 0 END) > 0 THEN 'Unpaid'
                               ELSE 'Paid'
                           END as status
                    FROM patients p
                    LEFT JOIN billing b ON p.patient_id = b.patient_id
                    WHERE b.bill_date BETWEEN %s AND %s
                    GROUP BY p.patient_id, p.first_name, p.last_name
                """
                params = [from_date, to_date]
                if payment_status != "All":
                    query += " HAVING status = %s"
                    params.append(payment_status)
                cursor.execute(query, tuple(params))
                results = cursor.fetchall()

                parent = self.report_tree.insert("", tk.END, text="Patient Payments")
                for row in results:
                    values = (
                        row['patient_id'],
                        row['name'] or 'Unknown',
                        f"${row['total_amount'] or 0:.2f}",
                        f"${row['paid_amount'] or 0:.2f}",
                        f"${row['unpaid_amount'] or 0:.2f}",
                        row['status']
                    )
                    self.report_tree.insert(parent, tk.END, values=values)
                self.report_status.config(text=f"Total Patients with Payments: {len(results)}")

            self.on_resize(None)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to generate report: {e}")
            logger.error(f"Database error: {e}")
        finally:
            if cursor:
                cursor.close()

    def export_report_to_pdf(self):
        from_date = self.from_date_entry.get_date().strftime('%Y-%m-%d')
        to_date = self.to_date_entry.get_date().strftime('%Y-%m-%d')
        report_type = self.report_type_var.get()

        try:
            if not self.report_tree.get_children():
                messagebox.showwarning("No Data", "No data to export. Generate a report first.")
                return

            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=f"hospital_report_{report_type.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            if not filename:
                return

            doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
            # Extract headers
            headers = [self.report_tree.heading(col)["text"] for col in self.report_tree["columns"]]
            data = [headers]
            # Extract data rows
            for item in self.report_tree.get_children():
                values = self.report_tree.item(item)["values"]
                if not values:  # Skip empty rows (e.g., parent nodes)
                    continue
                data.append([str(val) if val is not None else "N/A" for val in values])

            logger.debug(f"Exporting to PDF: Headers={headers}, Data rows={len(data)-1}")
            if not data[1:]:  # Check if there are any data rows
                messagebox.showwarning("No Data", "No data rows to export.")
                return

            col_widths = [100] * len(self.report_tree["columns"])
            table = Table(data, colWidths=col_widths)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ])
            table.setStyle(style)

            styles = getSampleStyleSheet()
            title = Paragraph(f"Hospital {report_type} Report", styles['Title'])
            subtitle = Paragraph(f"Date Range: {from_date} to {to_date}", styles['Normal'])
            elements = [title, subtitle, Spacer(1, 12), table]
            doc.build(elements)

            messagebox.showinfo("Success", f"Report exported to {filename}")
            if os.name == 'nt':
                os.startfile(filename)
            else:
                os.system(f"open {filename}" if os.name == 'posix' else f"xdg-open {filename}")

        except Exception as e:
            messagebox.showerror("PDF Export Error", f"Failed to export PDF: {e}")
            logger.error(f"PDF export error: {e}")

    def export_report_to_excel(self):
        from_date = self.from_date_entry.get_date().strftime('%Y-%m-%d')
        to_date = self.to_date_entry.get_date().strftime('%Y-%m-%d')
        report_type = self.report_type_var.get()

        try:
            if not self.report_tree.get_children():
                messagebox.showwarning("No Data", "No data to export. Generate a report first.")
                return

            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=f"hospital_report_{report_type.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            if not filename:
                return

            # Extract headers
            headers = [self.report_tree.heading(col)["text"] for col in self.report_tree["columns"]]
            data = [headers]
            # Extract data rows
            for item in self.report_tree.get_children():
                values = self.report_tree.item(item)["values"]
                if not values:  # Skip empty rows (e.g., parent nodes)
                    continue
                data.append([str(val) if val is not None else "N/A" for val in values])

            logger.debug(f"Exporting to Excel: Headers={headers}, Data rows={len(data)-1}")
            if not data[1:]:  # Check if there are any data rows
                messagebox.showwarning("No Data", "No data rows to export.")
                return

            df = pd.DataFrame(data[1:], columns=data[0])
            writer = pd.ExcelWriter(filename, engine='openpyxl')
            df.to_excel(writer, index=False, sheet_name=report_type)
            
            worksheet = writer.sheets[report_type]
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).map(len).max(), len(col))
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
            
            writer.close()
            messagebox.showinfo("Success", f"Report exported to {filename}")
            if os.name == 'nt':
                os.startfile(filename)
            else:
                os.system(f"open {filename}" if os.name == 'posix' else f"xdg-open {filename}")

        except Exception as e:
            messagebox.showerror("Excel Export Error", f"Failed to export Excel: {e}")
            logger.error(f"Excel export error: {e}")

    def print_report(self):
        from_date = self.from_date_entry.get_date().strftime('%Y-%m-%d')
        to_date = self.to_date_entry.get_date().strftime('%Y-%m-%d')
        report_type = self.report_type_var.get()

        try:
            if not self.report_tree.get_children():
                messagebox.showwarning("No Data", "No data to print. Generate a report first.")
                return

            temp_filename = f"temp_hospital_report_{report_type.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(temp_filename, pagesize=landscape(letter))
            # Extract headers
            headers = [self.report_tree.heading(col)["text"] for col in self.report_tree["columns"]]
            data = [headers]
            # Extract data rows
            for item in self.report_tree.get_children():
                values = self.report_tree.item(item)["values"]
                if not values:  # Skip empty rows (e.g., parent nodes)
                    continue
                data.append([str(val) if val is not None else "N/A" for val in values])

            logger.debug(f"Printing: Headers={headers}, Data rows={len(data)-1}")
            if not data[1:]:  # Check if there are any data rows
                messagebox.showwarning("No Data", "No data rows to print.")
                return

            col_widths = [100] * len(self.report_tree["columns"])
            table = Table(data, colWidths=col_widths)
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ])
            table.setStyle(style)

            styles = getSampleStyleSheet()
            title = Paragraph(f"Hospital {report_type} Report", styles['Title'])
            subtitle = Paragraph(f"Date Range: {from_date} to {to_date}", styles['Normal'])
            elements = [title, subtitle, Spacer(1, 12), table]
            doc.build(elements)

            if os.name == 'nt':
                # Use os.startfile with 'print' verb to open the print dialog
                os.startfile(temp_filename, "print")
                messagebox.showinfo("Print", "Please select a printer and confirm to print.")
                # Delay removal to allow printing
                self.root.after(5000, lambda: os.remove(temp_filename) if os.path.exists(temp_filename) else None)
            else:
                messagebox.showwarning("Print Warning", "Direct printing is only supported on Windows.")

        except Exception as e:
            messagebox.showerror("Print Error", f"Failed to print report: {e}")
            logger.error(f"Print error: {e}")
            if os.path.exists(temp_filename):
                os.remove(temp_filename)





    # def show_reports(self):
    #     # Clear content frame
    #     for widget in self.admin_content_frame.winfo_children():
    #         widget.destroy()

    #     # Create a scrolled frame for the main content
    #     scrolled_frame = tk.Frame(self.admin_content_frame)
    #     scrolled_frame.pack(fill=tk.BOTH, expand=True)

    #     # Add scrollbar to the scrolled frame
    #     y_scrollbar = ttk.Scrollbar(scrolled_frame, orient=tk.VERTICAL)
    #     y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    #     canvas = tk.Canvas(scrolled_frame, yscrollcommand=y_scrollbar.set, bg="#e0f7fa")
    #     canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    #     y_scrollbar.config(command=canvas.yview)

    #     # Create inner frame for content
    #     inner_frame = tk.Frame(canvas, bg="#e0f7fa")
    #     canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    #     # Update scroll region when inner frame changes size
    #     def configure_scroll_region(event):
    #         canvas.configure(scrollregion=canvas.bbox("all"))
    #     inner_frame.bind("<Configure>", configure_scroll_region)

    #     # Main title with modern styling
    #     title_label = tk.Label(
    #         inner_frame,
    #         text="Hospital Analytics Dashboard",
    #         font=("Helvetica", 22, "bold"),
    #         bg="#1a252f",
    #         fg="#e0f7fa",
    #         pady=15,
    #         relief="flat"
    #     )
    #     title_label.pack()

    #     # Filter frame with gradient-like background
    #     filter_frame = tk.Frame(inner_frame, bg="#2a3d4e")
    #     filter_frame.pack(fill=tk.X, padx=20, pady=15)

    #     # Date range selection
    #     tk.Label(filter_frame, text="From Date:", font=("Helvetica", 12), bg="#2a3d4e", fg="#e0f7fa").grid(row=0, column=0, padx=5, pady=5)
    #     self.from_date_entry = DateEntry(
    #         filter_frame,
    #         font=("Helvetica", 12),
    #         date_pattern='yyyy-mm-dd',
    #         width=12,
    #         background='#e0f7fa',
    #         foreground='#1a252f',
    #         bordercolor='#4dd0e1',
    #         selectbackground='#4dd0e1',
    #         selectforeground='#1a252f'
    #     )
    #     self.from_date_entry.grid(row=0, column=1, padx=5, pady=5)
    #     self.from_date_entry.set_date(datetime.now().replace(day=1))

    #     tk.Label(filter_frame, text="To Date:", font=("Helvetica", 12), bg="#2a3d4e", fg="#e0f7fa").grid(row=0, column=2, padx=5, pady=5)
    #     self.to_date_entry = DateEntry(
    #         filter_frame,
    #         font=("Helvetica", 12),
    #         date_pattern='yyyy-mm-dd',
    #         width=12,
    #         background='#e0f7fa',
    #         foreground='#1a252f',
    #         bordercolor='#4dd0e1',
    #         selectbackground='#4dd0e1',
    #         selectforeground='#1a252f'
    #     )
    #     self.to_date_entry.grid(row=0, column=3, padx=5, pady=5)
    #     self.to_date_entry.set_date(datetime.now())

    #     # Report type selection
    #     tk.Label(filter_frame, text="Report Type:", font=("Helvetica", 12), bg="#2a3d4e", fg="#e0f7fa").grid(row=0, column=4, padx=5, pady=5)
    #     self.report_type_var = tk.StringVar(value="Summary")
    #     report_types = ttk.Combobox(
    #         filter_frame,
    #         textvariable=self.report_type_var,
    #         values=["Summary", "Patients", "Appointments", "Financial", "Staff", "Patient Payments"],
    #         font=("Helvetica", 12),
    #         state="readonly",
    #         width=15,
    #         style="Custom.TCombobox"
    #     )
    #     report_types.grid(row=0, column=5, padx=5, pady=5)
    #     report_types.bind("<<ComboboxSelected>>", self.update_additional_filters)

    #     # Additional filters frame
    #     self.additional_filters_frame = tk.Frame(inner_frame, bg="#2a3d4e")
    #     self.additional_filters_frame.pack(pady=5, fill=tk.X)

    #     # Generate button
    #     generate_btn = tk.Button(
    #         filter_frame,
    #         text="Generate Report",
    #         font=("Helvetica", 12, "bold"),
    #         bg="#ff6f61",
    #         fg="white",
    #         activebackground="#e55b4d",
    #         relief="flat",
    #         padx=10,
    #         pady=5,
    #         command=self.generate_report_data
    #     )
    #     generate_btn.grid(row=0, column=6, padx=10, pady=5)

    #     # Treeview container with responsive design
    #     tree_container = tk.Frame(inner_frame, bg="#e0f7fa")
    #     tree_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

    #     # Customize Treeview style
    #     style = ttk.Style()
    #     style.theme_use('clam')
    #     style.configure("Custom.Treeview",
    #                     background="#ffffff",
    #                     foreground="#1a252f",
    #                     fieldbackground="#e0f7fa",
    #                     borderwidth=0,
    #                     relief="flat")
    #     style.map("Custom.Treeview",
    #             background=[('selected', '#4dd0e1')],
    #             foreground=[('selected', '#ffffff')])
    #     style.configure("Custom.Treeview.Heading",
    #                     background="#4dd0e1",
    #                     foreground="#ffffff",
    #                     font=('Helvetica', 11, 'bold'),
    #                     borderwidth=0,
    #                     relief="flat")
    #     style.configure("Custom.TCombobox",
    #                     fieldbackground="#e0f7fa",
    #                     background="#4dd0e1",
    #                     foreground="#1a252f")

    #     # Treeview scrollbars
    #     x_scrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, style="TScrollbar")
    #     x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    #     y_scrollbar = ttk.Scrollbar(tree_container, style="TScrollbar")
    #     y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #     # Treeview with scrollbars
    #     self.report_tree = ttk.Treeview(
    #         tree_container,
    #         yscrollcommand=y_scrollbar.set,
    #         xscrollcommand=x_scrollbar.set,
    #         height=15,
    #         style="Custom.Treeview"
    #     )
    #     self.report_tree.pack(fill=tk.BOTH, expand=True)
    #     y_scrollbar.config(command=self.report_tree.yview)
    #     x_scrollbar.config(command=self.report_tree.xview)

    #     # Ensure button frame is below Treeview and visible
    #     button_frame = tk.Frame(inner_frame, bg="#2a3d4e")
    #     button_frame.pack(pady=10, fill=tk.X)
    #     tk.Button(
    #         button_frame,
    #         text="Export to PDF",
    #         font=("Helvetica", 12, "bold"),
    #         bg="#2ecc71",
    #         fg="white",
    #         activebackground="#27ae60",
    #         relief="flat",
    #         padx=10,
    #         pady=5,
    #         command=self.export_report_to_pdf
    #     ).pack(side=tk.LEFT, padx=10)

    #     # Status bar
    #     self.report_status = tk.Label(
    #         inner_frame,
    #         text="Ready to generate report",
    #         font=("Helvetica", 10),
    #         bg="#2a3d4e",
    #         fg="#e0f7fa",
    #         anchor='w'
    #     )
    #     self.report_status.pack(fill=tk.X, padx=20, pady=(0, 10))

    #     # Initial setup
    #     self.update_additional_filters()
    #     self.generate_report_data()
    

    # def update_additional_filters(self, event=None):
    #     for widget in self.additional_filters_frame.winfo_children():
    #         widget.destroy()

    #     report_type = self.report_type_var.get()
    #     if report_type == "Appointments":
    #         tk.Label(self.additional_filters_frame, text="Status:", bg="#2a3d4e", fg="#e0f7fa").pack(side=tk.LEFT, padx=5)
    #         self.appt_status_var = tk.StringVar(value="All")
    #         ttk.Combobox(
    #             self.additional_filters_frame,
    #             textvariable=self.appt_status_var,
    #             values=["All", "Scheduled", "Confirmed", "Completed", "Cancelled"],
    #             state="readonly",
    #             width=12,
    #             style="Custom.TCombobox"
    #         ).pack(side=tk.LEFT, padx=5)
    #     elif report_type == "Financial":
    #         tk.Label(self.additional_filters_frame, text="Payment Status:", bg="#2a3d4e", fg="#e0f7fa").pack(side=tk.LEFT, padx=5)
    #         self.payment_status_var = tk.StringVar(value="All")
    #         ttk.Combobox(
    #             self.additional_filters_frame,
    #             textvariable=self.payment_status_var,
    #             values=["All", "Paid", "Pending"],
    #             state="readonly",
    #             width=10,
    #             style="Custom.TCombobox"
    #         ).pack(side=tk.LEFT, padx=5)
    #     elif report_type == "Patient Payments":
    #         tk.Label(self.additional_filters_frame, text="Payment Status:", bg="#2a3d4e", fg="#e0f7fa").pack(side=tk.LEFT, padx=5)
    #         self.patient_payment_var = tk.StringVar(value="All")
    #         ttk.Combobox(
    #             self.additional_filters_frame,
    #             textvariable=self.patient_payment_var,
    #             values=["All", "Paid", "Unpaid"],
    #             state="readonly",
    #             width=10,
    #             style="Custom.TCombobox"
    #         ).pack(side=tk.LEFT, padx=5)

    # def generate_report_data(self):
    #     from_date = self.from_date_entry.get_date()
    #     to_date = self.to_date_entry.get_date()
    #     report_type = self.report_type_var.get()
    #     cursor = None

    #     try:
    #         cursor = self.db_connection.cursor(dictionary=True)
    #         for item in self.report_tree.get_children():
    #             self.report_tree.delete(item)
    #         self.report_tree["columns"] = []

    #         if report_type == "Summary":
    #             self.report_tree["columns"] = ("Metric", "Value")
    #             for col in self.report_tree["columns"]:
    #                 self.report_tree.heading(col, text=col, anchor=tk.W)
    #                 self.report_tree.column(col, width=250 if col == "Metric" else 150, anchor=tk.W)

    #             summary_data = []
    #             cursor.execute("SELECT COUNT(*) as count FROM patients")
    #             patient_count = cursor.fetchone()['count']
    #             summary_data.append(("Patients Registered", patient_count))

    #             cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE appointment_date BETWEEN %s AND %s", (from_date, to_date))
    #             appointments_count = cursor.fetchone()['count']
    #             summary_data.append(("Appointments Booked", appointments_count))

    #             cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE status = 'Completed' AND appointment_date BETWEEN %s AND %s", (from_date, to_date))
    #             completed_count = cursor.fetchone()['count']
    #             summary_data.append(("Appointments Completed", completed_count))

    #             cursor.execute("SELECT COUNT(*) as count FROM appointments WHERE status = 'Cancelled' AND appointment_date BETWEEN %s AND %s", (from_date, to_date))
    #             cancelled_count = cursor.fetchone()['count']
    #             summary_data.append(("Appointments Cancelled", cancelled_count))

    #             cursor.execute("SELECT SUM(amount) as total FROM billing WHERE payment_status = 'Paid' AND bill_date BETWEEN %s AND %s", (from_date, to_date))
    #             revenue = cursor.fetchone()['total'] or 0
    #             summary_data.append(("Total Revenue", f"${revenue:.2f}"))

    #             cursor.execute("SELECT COUNT(*) as count FROM doctors")
    #             doctor_count = cursor.fetchone()['count']
    #             summary_data.append(("Total Doctors", doctor_count))

    #             cursor.execute("SELECT COUNT(*) as count FROM staff")
    #             staff_count = cursor.fetchone()['count']
    #             summary_data.append(("Total Staff", staff_count))

    #             for metric, value in summary_data:
    #                 self.report_tree.insert("", tk.END, values=(metric, value))
    #             self.report_status.config(text=f"Generated summary report from {from_date} to {to_date}")

    #         elif report_type == "Patients":
    #             columns = ("Patient ID", "Name", "Gender", "DOB", "Blood Type", "Phone")
    #             self.report_tree["columns"] = columns
    #             for col in columns:
    #                 self.report_tree.heading(col, text=col, anchor=tk.W)
    #                 self.report_tree.column(col, width=120, anchor=tk.W)

    #             query = "SELECT p.patient_id, CONCAT(p.first_name, ' ', COALESCE(p.last_name, '')) as name, p.gender, p.date_of_birth, p.blood_type, p.phone FROM patients p ORDER BY p.patient_id"
    #             cursor.execute(query)
    #             results = cursor.fetchall()

    #             for row in results:
    #                 values = (
    #                     row['patient_id'],
    #                     row['name'] or 'Unknown',
    #                     row['gender'],
    #                     row['date_of_birth'].strftime('%Y-%m-%d'),
    #                     row['blood_type'] or 'N/A',
    #                     row['phone'] or 'N/A'
    #                 )
    #                 self.report_tree.insert("", tk.END, values=values)
    #             self.report_status.config(text=f"Total Patients: {len(results)}")

    #         elif report_type == "Appointments":
    #             columns = ("Appointment ID", "Date", "Time", "Patient", "Doctor", "Status", "Reason")
    #             self.report_tree["columns"] = columns
    #             for col in columns:
    #                 self.report_tree.heading(col, text=col, anchor=tk.W)
    #                 self.report_tree.column(col, width=120, anchor=tk.W)

    #             status = getattr(self, 'appt_status_var', tk.StringVar(value="All")).get()
    #             query = """
    #                 SELECT a.appointment_id, a.appointment_date, a.appointment_time,
    #                     CONCAT(p.first_name, ' ', COALESCE(p.last_name, '')) as patient_name,
    #                     CONCAT(d.first_name, ' ', COALESCE(d.last_name, '')) as doctor_name,
    #                     a.status, a.reason
    #                 FROM appointments a
    #                 LEFT JOIN patients p ON a.patient_id = p.patient_id
    #                 LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
    #                 WHERE a.appointment_date BETWEEN %s AND %s
    #             """
    #             params = [from_date, to_date]
    #             if status != "All":
    #                 query += " AND a.status = %s"
    #                 params.append(status)
    #             logger.debug(f"Appointments query: {query} with params: {params}")
    #             cursor.execute(query, tuple(params))
    #             results = cursor.fetchall()
    #             logger.debug(f"Appointments fetched: {len(results)} rows")

    #             if not results:
    #                 self.report_status.config(text="No appointments found for the selected date range.")
    #             else:
    #                 for row in results:
    #                     # Handle timedelta for appointment_time
    #                     time_str = 'N/A'
    #                     if row['appointment_time']:
    #                         if isinstance(row['appointment_time'], timedelta):
    #                             total_seconds = int(row['appointment_time'].total_seconds())
    #                             hours = total_seconds // 3600
    #                             minutes = (total_seconds % 3600) // 60
    #                             time_str = f"{hours:02d}:{minutes:02d}"
    #                         elif hasattr(row['appointment_time'], 'strftime'):
    #                             time_str = row['appointment_time'].strftime('%H:%M')
    #                     values = (
    #                         row['appointment_id'] or 'N/A',
    #                         row['appointment_date'].strftime('%Y-%m-%d') if row['appointment_date'] else 'N/A',
    #                         time_str,
    #                         row['patient_name'] or 'Unknown',
    #                         row['doctor_name'] or 'Unknown',
    #                         row['status'] or 'N/A',
    #                         row['reason'] or 'N/A'
    #                     )
    #                     self.report_tree.insert("", tk.END, values=values)
    #                 self.report_status.config(text=f"Total Appointments: {len(results)}")

    #         elif report_type == "Financial":
    #             columns = ("Bill ID", "Date", "Patient", "Amount", "Description", "Status")
    #             self.report_tree["columns"] = columns
    #             for col in columns:
    #                 self.report_tree.heading(col, text=col, anchor=tk.W)
    #                 self.report_tree.column(col, width=120, anchor=tk.W)

    #             payment_status = getattr(self, 'payment_status_var', tk.StringVar(value="All")).get()
    #             query = """
    #                 SELECT b.bill_id, b.bill_date, CONCAT(p.first_name, ' ', COALESCE(p.last_name, '')) as patient_name,
    #                     b.amount, b.description, b.payment_status
    #                 FROM billing b
    #                 LEFT JOIN patients p ON b.patient_id = p.patient_id
    #                 WHERE b.bill_date BETWEEN %s AND %s
    #             """
    #             params = [from_date, to_date]
    #             if payment_status != "All":
    #                 query += " AND b.payment_status = %s"
    #                 params.append(payment_status)
    #             cursor.execute(query, tuple(params))
    #             results = cursor.fetchall()

    #             total_amount = sum(row['amount'] for row in results)
    #             paid_amount = sum(row['amount'] for row in results if row['payment_status'] == "Paid")

    #             for row in results:
    #                 values = (
    #                     row['bill_id'],
    #                     row['bill_date'].strftime('%Y-%m-%d'),
    #                     row['patient_name'] or 'Unknown',
    #                     f"${row['amount']:.2f}",
    #                     row['description'] or 'N/A',
    #                     row['payment_status']
    #                 )
    #                 self.report_tree.insert("", tk.END, values=values)
    #             self.report_status.config(
    #                 text=f"Total Amount: ${total_amount:.2f} | Paid: ${paid_amount:.2f} | Pending: ${total_amount-paid_amount:.2f}"
    #             )

    #         elif report_type == "Staff":
    #             columns = ("Staff ID", "Name", "Role", "Phone", "Email")
    #             self.report_tree["columns"] = columns
    #             for col in columns:
    #                 self.report_tree.heading(col, text=col, anchor=tk.W)
    #                 self.report_tree.column(col, width=120, anchor=tk.W)

    #             query = "SELECT s.staff_id, CONCAT(s.first_name, ' ', s.last_name) as name, s.role, s.phone, s.email FROM staff s ORDER BY s.staff_id"
    #             cursor.execute(query)
    #             results = cursor.fetchall()

    #             for row in results:
    #                 values = (
    #                     row['staff_id'],
    #                     row['name'],
    #                     row['role'],
    #                     row['phone'] or 'N/A',
    #                     row['email'] or 'N/A'
    #                 )
    #                 self.report_tree.insert("", tk.END, values=values)
    #             self.report_status.config(text=f"Total Staff: {len(results)}")

    #         elif report_type == "Patient Payments":
    #             columns = ("Patient ID", "Name", "Total Amount", "Paid Amount", "Unpaid Amount", "Status")
    #             self.report_tree["columns"] = columns
    #             for col in columns:
    #                 self.report_tree.heading(col, text=col, anchor=tk.W)
    #                 self.report_tree.column(col, width=120, anchor=tk.W)

    #             payment_status = getattr(self, 'patient_payment_var', tk.StringVar(value="All")).get()
    #             query = """
    #                 SELECT p.patient_id, CONCAT(p.first_name, ' ', COALESCE(p.last_name, '')) as name,
    #                     SUM(b.amount) as total_amount,
    #                     SUM(CASE WHEN b.payment_status = 'Paid' THEN b.amount ELSE 0 END) as paid_amount,
    #                     SUM(CASE WHEN b.payment_status = 'Pending' THEN b.amount ELSE 0 END) as unpaid_amount,
    #                     CASE
    #                         WHEN SUM(CASE WHEN b.payment_status = 'Pending' THEN b.amount ELSE 0 END) > 0 THEN 'Unpaid'
    #                         ELSE 'Paid'
    #                     END as status
    #                 FROM patients p
    #                 LEFT JOIN billing b ON p.patient_id = b.patient_id
    #                 GROUP BY p.patient_id, p.first_name, p.last_name
    #             """
    #             params = []
    #             if payment_status != "All":
    #                 query += " HAVING status = %s"
    #                 params.append(payment_status)
    #             cursor.execute(query, tuple(params))
    #             results = cursor.fetchall()

    #             for row in results:
    #                 values = (
    #                     row['patient_id'],
    #                     row['name'] or 'Unknown',
    #                     f"${row['total_amount'] or 0:.2f}",
    #                     f"${row['paid_amount'] or 0:.2f}",
    #                     f"${row['unpaid_amount'] or 0:.2f}",
    #                     row['status']
    #                 )
    #                 self.report_tree.insert("", tk.END, values=values)
    #             self.report_status.config(text=f"Total Patients with Payments: {len(results)}")

    #     except Error as e:
    #         messagebox.showerror("Database Error", f"Failed to generate report: {e}")
    #         logger.error(f"Database error: {e}")
    #     finally:
    #         if cursor:
    #             cursor.close()

    # def export_report_to_pdf(self):
    #     from_date = self.from_date_entry.get_date()
    #     to_date = self.to_date_entry.get_date()
    #     report_type = self.report_type_var.get()

    #     try:
    #         filename = f"hospital_report_{report_type.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    #         doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
    #         data = [[self.report_tree.heading(col)["text"] for col in self.report_tree["columns"]]]
    #         for item in self.report_tree.get_children():
    #             data.append([str(val) for val in self.report_tree.item(item)["values"]])

    #         table = Table(data)
    #         style = TableStyle([
    #             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #             ('FONTSIZE', (0, 0), (-1, 0), 12),
    #             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    #             ('GRID', (0, 0), (-1, -1), 1, colors.black),
    #         ])
    #         table.setStyle(style)

    #         styles = getSampleStyleSheet()
    #         title = Paragraph(f"Hospital {report_type} Report", styles['Title'])
    #         subtitle = Paragraph(f"Date Range: {from_date} to {to_date}", styles['Normal'])
    #         elements = [title, subtitle, Spacer(1, 12), table]
    #         doc.build(elements)

    #         messagebox.showinfo("Success", f"Report exported to {filename}")
    #         if os.name == 'nt':  # Windows
    #             os.startfile(filename)
    #         else:  # Other OS
    #             os.system(f"open {filename}" if os.name == 'posix' else f"xdg-open {filename}")

    #     except Exception as e:
    #         messagebox.showerror("PDF Export Error", f"Failed to export PDF: {e}")

    def save_system_settings(self):
            opening_time = self.opening_time.get()
            closing_time = self.closing_time.get()
            duration = self.appointment_duration.get()

            # Validate inputs
            try:
                datetime.strptime(opening_time, "%H:%M")
                datetime.strptime(closing_time, "%H:%M")
                int(duration)
            except ValueError:
                messagebox.showerror("Error", "Invalid input format. Time should be HH:MM and duration should be a number")
                return

            # In a real application, you would save these settings to a database or config file
            messagebox.showinfo("Success", "Settings saved successfully (not persisted in this demo)")
        
    def show_doctor_dashboard(self, user_id):
         # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Doctor dashboard frame
        dashboard_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        dashboard_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = tk.Frame(dashboard_frame, bg="#2196F3", height=80)
        header_frame.pack(fill=tk.X)

        # Get doctor's name
        doctor_name = ""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT first_name, last_name FROM doctors WHERE user_id = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            if result:
                doctor_name = f"{result[0]} {result[1]}"
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch doctor data: {e}")

        tk.Label(
            header_frame,
            text=f"Doctor Dashboard - {doctor_name}",
            font=("Arial", 20, "bold"),
            bg="#2196F3",
            fg="white",
        ).pack(side=tk.LEFT, padx=20)

        logout_btn = tk.Button(
            header_frame,
            text="Logout",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=self.show_login_screen,
        )
        logout_btn.pack(side=tk.RIGHT, padx=20)

        # Navigation
        nav_frame = tk.Frame(dashboard_frame, bg="#333", width=200)
        nav_frame.pack(fill=tk.Y, side=tk.LEFT)

        buttons = [
            ("Dashboard", lambda: self.show_doctor_welcome(user_id)),
            ("My Schedule", lambda: self.show_doctor_schedule(user_id)),
            ("My Patients", lambda: self.show_doctor_patients(user_id)),
            ("Medical Records", lambda: self.show_doctor_medical_records(user_id)),
        ]

        for text, command in buttons:
            tk.Button(
                nav_frame,
                text=text,
                font=("Arial", 12),
                bg="#333",
                fg="white",
                relief=tk.FLAT,
                command=command,
            ).pack(fill=tk.X, pady=2)

        # Main content area
        self.doctor_content_frame = tk.Frame(dashboard_frame, bg="#f0f8ff")
        self.doctor_content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        # Show default view
        self.show_doctor_welcome(user_id)

    def show_doctor_welcome(self, user_id):
        # Clear content frame
        for widget in self.doctor_content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.doctor_content_frame,
            text="Welcome, Doctor",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=50)

        # Display today's appointments count
        try:
            cursor = self.db_connection.cursor()
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Get total appointments
            cursor.execute(
                """SELECT COUNT(*) FROM appointments 
                WHERE doctor_id = (SELECT doctor_id FROM doctors WHERE user_id = %s)
                AND appointment_date = %s""",
                (user_id, today)
            )
            today_appointments = cursor.fetchone()[0]
            
            # Get completed appointments
            cursor.execute(
                """SELECT COUNT(*) FROM appointments 
                WHERE doctor_id = (SELECT doctor_id FROM doctors WHERE user_id = %s)
                AND appointment_date = %s AND status = 'Completed'""",
                (user_id, today)
            )
            completed_appointments = cursor.fetchone()[0]
            
            # Display stats
            stats_frame = tk.Frame(self.doctor_content_frame, bg="#f0f8ff")
            stats_frame.pack()
            
            tk.Label(
                stats_frame,
                text="Today's Appointments:",
                font=("Arial", 14),
                bg="#f0f8ff"
            ).grid(row=0, column=0, padx=10, pady=5, sticky="e")
            
            tk.Label(
                stats_frame,
                text=str(today_appointments),
                font=("Arial", 14, "bold"),
                bg="#f0f8ff"
            ).grid(row=0, column=1, padx=10, pady=5, sticky="w")
            
            tk.Label(
                stats_frame,
                text="Completed:",
                font=("Arial", 14),
                bg="#f0f8ff"
            ).grid(row=1, column=0, padx=10, pady=5, sticky="e")
            
            tk.Label(
                stats_frame,
                text=str(completed_appointments),
                font=("Arial", 14, "bold"),
                bg="#f0f8ff"
            ).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch appointment data: {e}")

    def show_doctor_schedule(self, user_id):
        # Clear content frame
        for widget in self.doctor_content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.doctor_content_frame,
            text="My Schedule",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=10)

        # Date filter
        filter_frame = tk.Frame(self.doctor_content_frame, bg="#f0f8ff")
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Date:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, padx=5)
        self.doctor_schedule_date = tk.Entry(filter_frame, font=("Arial", 12))
        self.doctor_schedule_date.grid(row=0, column=1, padx=5)
        self.doctor_schedule_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        filter_btn = tk.Button(
            filter_frame,
            text="Filter",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=lambda: self.load_doctor_schedule(user_id),
        )
        filter_btn.grid(row=0, column=2, padx=10)

        # Appointments table
        columns = ("ID", "Patient", "Time", "Status", "Reason")
        self.doctor_schedule_tree = ttk.Treeview(
            self.doctor_content_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.doctor_schedule_tree.heading(col, text=col)
            self.doctor_schedule_tree.column(col, width=150, anchor=tk.CENTER)

        self.doctor_schedule_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Action buttons frame
        action_frame = tk.Frame(self.doctor_content_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)

        complete_btn = tk.Button(
            action_frame,
            text="Mark as Completed",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.update_appointment_status(user_id, "Completed"),
        )
        complete_btn.grid(row=0, column=0, padx=10)

        cancel_btn = tk.Button(
            action_frame,
            text="Cancel Appointment",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=lambda: self.update_appointment_status(user_id, "Cancelled"),
        )
        cancel_btn.grid(row=0, column=1, padx=10)

        # Load initial schedule
        self.load_doctor_schedule(user_id)

    def load_doctor_schedule(self, user_id):
        date = self.doctor_schedule_date.get()

        # Validate date
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
            return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT a.appointment_id, 
                          CONCAT(p.first_name, ' ', p.last_name),
                          a.appointment_time,
                          a.status,
                          a.reason
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                WHERE a.doctor_id = (SELECT doctor_id FROM doctors WHERE user_id = %s)
                AND a.appointment_date = %s
                ORDER BY a.appointment_time""",
                (user_id, date)
            )
            appointments = cursor.fetchall()

            # Clear existing data
            for item in self.doctor_schedule_tree.get_children():
                self.doctor_schedule_tree.delete(item)

            # Insert new data
            for appointment in appointments:
                self.doctor_schedule_tree.insert("", tk.END, values=appointment)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load schedule: {e}")

    def update_appointment_status(self, user_id, status):
        selected_item = self.doctor_schedule_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an appointment")
            return

        appointment_id = self.doctor_schedule_tree.item(selected_item)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm", f"Are you sure you want to mark this appointment as {status}?"
        )
        if not confirm:
            return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "UPDATE appointments SET status = %s WHERE appointment_id = %s",
                (status, appointment_id)
            )

            self.db_connection.commit()

            messagebox.showinfo("Success", f"Appointment marked as {status}")
            self.load_doctor_schedule(user_id)

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to update appointment: {e}")

    def show_doctor_patients(self, user_id):
        # Clear content frame
        for widget in self.doctor_content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.doctor_content_frame,
            text="My Patients",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=10)

        # Patients table
        columns = ("ID", "Name", "Gender", "Age", "Last Visit")
        self.doctor_patients_tree = ttk.Treeview(
            self.doctor_content_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.doctor_patients_tree.heading(col, text=col)
            self.doctor_patients_tree.column(col, width=120, anchor=tk.CENTER)

        self.doctor_patients_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Load patients data
        self.load_doctor_patients(user_id)

        # Action buttons frame
        action_frame = tk.Frame(self.doctor_content_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)

        view_records_btn = tk.Button(
            action_frame,
            text="View Medical Records",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=self.view_patient_records,
        )
        view_records_btn.grid(row=0, column=0, padx=10)

    def load_doctor_patients(self, user_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT DISTINCT p.patient_id, 
                          CONCAT(p.first_name, ' ', p.last_name),
                          p.gender, 
                          TIMESTAMPDIFF(YEAR, p.date_of_birth, CURDATE()),
                          MAX(a.appointment_date)
                FROM patients p
                JOIN appointments a ON p.patient_id = a.patient_id
                WHERE a.doctor_id = (SELECT doctor_id FROM doctors WHERE user_id = %s)
                GROUP BY p.patient_id
                ORDER BY p.last_name, p.first_name""",
                (user_id,)
            )
            patients = cursor.fetchall()

            # Clear existing data
            for item in self.doctor_patients_tree.get_children():
                self.doctor_patients_tree.delete(item)

            # Insert new data
            for patient in patients:
                self.doctor_patients_tree.insert("", tk.END, values=patient)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load patients: {e}")

    def view_patient_records(self):
        selected_item = self.doctor_patients_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a patient")
            return

        patient_id = self.doctor_patients_tree.item(selected_item)["values"][0]
        self.show_doctor_medical_records(self.current_user_id, patient_id)

    def show_doctor_medical_records(self, user_id, patient_id=None):
        # Clear content frame
        for widget in self.doctor_content_frame.winfo_children():
            widget.destroy()

        if patient_id is None:
            # Show list of patients to select from
            tk.Label(
                self.doctor_content_frame,
                text="Select a patient to view medical records",
                font=("Arial", 16, "bold"),
                bg="#f0f8ff",
            ).pack(pady=10)

            # Patients table
            columns = ("ID", "Name", "Gender", "Age")
            self.records_patients_tree = ttk.Treeview(
                self.doctor_content_frame, columns=columns, show="headings", height=15
            )

            for col in columns:
                self.records_patients_tree.heading(col, text=col)
                self.records_patients_tree.column(col, width=120, anchor=tk.CENTER)

            self.records_patients_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            # Load patients data
            try:
                cursor = self.db_connection.cursor()
                cursor.execute(
                    """SELECT DISTINCT p.patient_id, 
                              CONCAT(p.first_name, ' ', p.last_name),
                              p.gender, 
                              TIMESTAMPDIFF(YEAR, p.date_of_birth, CURDATE())
                    FROM patients p
                    JOIN appointments a ON p.patient_id = a.patient_id
                    WHERE a.doctor_id = (SELECT doctor_id FROM doctors WHERE user_id = %s)
                    GROUP BY p.patient_id
                    ORDER BY p.last_name, p.first_name""",
                    (user_id,)
                )
                patients = cursor.fetchall()

                # Insert data
                for patient in patients:
                    self.records_patients_tree.insert("", tk.END, values=patient)

                # Bind double click to view records
                self.records_patients_tree.bind(
                    "<Double-1>",
                    lambda e: self.show_doctor_medical_records(
                        user_id,
                        self.records_patients_tree.item(self.records_patients_tree.selection())["values"][0]
                    ))
                
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to load patients: {e}")

            return

        # Show medical records for specific patient
        try:
            cursor = self.db_connection.cursor()
            
            # Get patient info
            cursor.execute(
                """SELECT CONCAT(first_name, ' ', last_name), 
                          date_of_birth, gender, blood_type
                FROM patients
                WHERE patient_id = %s""",
                (patient_id,)
            )
            patient_info = cursor.fetchone()
            
            if not patient_info:
                messagebox.showerror("Error", "Patient not found")
                return

            # Display patient info
            info_frame = tk.Frame(self.doctor_content_frame, bg="#f0f8ff")
            info_frame.pack(fill=tk.X, pady=10)

            tk.Label(
                info_frame,
                text=f"Medical Records for {patient_info[0]}",
                font=("Arial", 16, "bold"),
                bg="#f0f8ff",
            ).pack(side=tk.LEFT, padx=20)

            tk.Label(
                info_frame,
                text=f"DOB: {patient_info[1]} | Gender: {patient_info[2]} | Blood Type: {patient_info[3] or 'Unknown'}",
                font=("Arial", 12),
                bg="#f0f8ff",
            ).pack(side=tk.LEFT, padx=20)

            # Add record button
            add_btn = tk.Button(
                self.doctor_content_frame,
                text="Add Medical Record",
                font=("Arial", 12),
                bg="#4CAF50",
                fg="white",
                command=lambda: self.show_add_medical_record_form(patient_id, user_id),
            )
            add_btn.pack(pady=10)

            # Medical records table
            columns = ("Date", "Diagnosis", "Treatment", "Notes")
            self.medical_records_tree = ttk.Treeview(
                self.doctor_content_frame, columns=columns, show="headings", height=15
            )

            for col in columns:
                self.medical_records_tree.heading(col, text=col)
                self.medical_records_tree.column(col, width=150, anchor=tk.CENTER)

            self.medical_records_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            # Load medical records
            cursor.execute(
                """SELECT record_date, diagnosis, treatment, notes
                FROM medical_records
                WHERE patient_id = %s AND doctor_id = (SELECT doctor_id FROM doctors WHERE user_id = %s)
                ORDER BY record_date DESC""",
                (patient_id, user_id)
            )
            records = cursor.fetchall()

            # Insert records
            for record in records:
                self.medical_records_tree.insert("", tk.END, values=record)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load medical records: {e}")
            
    def show_add_medical_record_form(self, patient_id, user_id):
        # Create a new top-level window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Medical Record")
        add_window.geometry("500x500")

        tk.Label(add_window, text="Add Medical Record", font=("Arial", 18, "bold")).pack(pady=10)

        # Form fields
        fields = [
            ("Date (YYYY-MM-DD):", "entry"),
            ("Diagnosis:", "entry"),
            ("Treatment:", "entry"),
            ("Notes:", "text"),
        ]

        self.medical_record_entries = {}

        for i, (label, field_type) in enumerate(fields):
            tk.Label(add_window, text=label, font=("Arial", 12)).pack(pady=5)

            if field_type == "entry":
                entry = tk.Entry(add_window, font=("Arial", 12))
                entry.pack(pady=5, ipadx=20)
                key = label.lower().split(":")[0].strip().replace(" ", "_").replace("(", "").replace(")", "")
                self.medical_record_entries[key] = entry

            elif field_type == "text":
                text = tk.Text(add_window, font=("Arial", 12), height=5, width=40)
                text.pack(pady=5)
                self.medical_record_entries[label.split(":")[0].lower().replace(" ", "_")] = text

        # Set default date to today
        for key in self.medical_record_entries:
            if "date" in key:
                self.medical_record_entries[key].insert(0, datetime.now().strftime("%Y-%m-%d"))
                break



                # Submit button
        submit_btn = tk.Button(
            add_window,
            text="Add Record",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.add_medical_record(patient_id, user_id, add_window),
        )
        submit_btn.pack(pady=20)


    def add_medical_record(self, patient_id, user_id, window):
        # Get all form data
        date = self.medical_record_entries["date_yyyy-mm-dd"].get()
        diagnosis = self.medical_record_entries["diagnosis"].get()
        treatment = self.medical_record_entries["treatment"].get()
        notes = self.medical_record_entries["notes"].get("1.0", tk.END).strip()

        # Validate inputs
        if not all([date, diagnosis]):
            messagebox.showerror("Error", "Date and Diagnosis are required")
            return

        cursor = None
        try:
            # Validate date
            datetime.strptime(date, "%Y-%m-%d")

            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Get doctor_id
            cursor.execute(
                "SELECT doctor_id FROM doctors WHERE user_id = %s",
                (user_id,)
            )
            doctor_id = cursor.fetchone()[0]

            # Insert medical record
            cursor.execute(
                """INSERT INTO medical_records 
                (patient_id, doctor_id, record_date, diagnosis, treatment, notes) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (patient_id, doctor_id, date, diagnosis, treatment, notes),
            )

            self.db_connection.commit()
            messagebox.showinfo("Success", "Medical record added successfully!")
            window.destroy()
            self.show_doctor_medical_records(user_id, patient_id)

        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to add medical record: {e}")
        finally:
            if cursor:
                cursor.close()


    
        


    def show_patient_dashboard(self, user_id):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Store current user ID
        self.current_user_id = user_id
        
        # Patient dashboard frame
        dashboard_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        dashboard_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = tk.Frame(dashboard_frame, bg="#2196F3", height=80)
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text="Patient Dashboard",
            font=("Arial", 24, "bold"),
            bg="#2196F3",
            fg="white",
        ).pack(side=tk.LEFT, padx=20)

        logout_btn = tk.Button(
            header_frame,
            text="Logout",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=lambda: self.show_loading_screen(lambda: self.show_login_screen()),
        )
        logout_btn.pack(side=tk.RIGHT, padx=20)

        # Navigation
        nav_frame = tk.Frame(dashboard_frame, bg="#333", width=200)
        nav_frame.pack(fill=tk.Y, side=tk.LEFT)

        buttons = [
            ("Dashboard", lambda: self.show_patient_welcome(user_id)),
            ("My Profile", lambda: self.show_patient_profile(user_id)),
            ("Book Appointment", lambda: self.show_add_appointment_form(is_admin=False)),
            ("View Appointments", lambda: self.show_patient_appointments(user_id)),
            ("Medical Records", lambda: self.show_medical_records(user_id)),
            ("Billing/Payments", lambda: self.show_patient_billing(user_id)),
        ]

        for text, command in buttons:
            tk.Button(
                nav_frame,
                text=text,
                font=("Arial", 12),
                bg="#333",
                fg="white",
                relief=tk.FLAT,
                command=command,
            ).pack(fill=tk.X, pady=2)

        # Main content area
        self.patient_content_frame = tk.Frame(dashboard_frame, bg="#f0f8ff")
        self.patient_content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        # Show default view
        self.show_patient_welcome(user_id)

    def show_patient_welcome(self, user_id):
        # Clear content frame
        for widget in self.patient_content_frame.winfo_children():
            widget.destroy()

        # Welcome message
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT first_name, last_name FROM patients WHERE user_id = %s",
                (user_id,)
            )
            patient_data = cursor.fetchone()
            if patient_data:
                welcome_text = f"Welcome, {patient_data[0]} {patient_data[1]}!"
            else:
                welcome_text = "Welcome!"
        except Error as e:
            welcome_text = "Welcome!"
            messagebox.showerror("Error", f"Failed to load patient data: {e}")

        tk.Label(
            self.patient_content_frame,
            text=welcome_text,
            font=("Arial", 24, "bold"),
            bg="#f0f8ff",
        ).pack(pady=50)

        # Quick actions
        tk.Label(
            self.patient_content_frame,
            text="Quick Actions",
            font=("Arial", 16, "bold"),
            bg="#f0f8ff",
        ).pack(pady=10)

        action_frame = tk.Frame(self.patient_content_frame, bg="#f0f8ff")
        action_frame.pack()

        actions = [
            ("Book Appointment", lambda: self.show_book_appointment(user_id)),
            ("View Appointments", lambda: self.show_patient_appointments(user_id)),
            ("Update Profile", lambda: self.show_patient_profile(user_id)),
        ]

        for text, command in actions:
            tk.Button(
                action_frame,
                text=text,
                font=("Arial", 12),
                bg="#2196F3",
                fg="white",
                command=command,
            ).pack(side=tk.LEFT, padx=10, pady=10)

    def show_patient_profile(self, user_id):
        # Clear content frame
        for widget in self.patient_content_frame.winfo_children():
            widget.destroy()

        # Create scrollable frame
        canvas = tk.Canvas(self.patient_content_frame, bg="#f0f8ff")
        scrollbar = ttk.Scrollbar(self.patient_content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f8ff")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack widgets
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Title
        tk.Label(
            scrollable_frame,
            text="My Profile",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=20)

        # Load patient data
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT p.patient_id, p.first_name, p.last_name, p.date_of_birth, 
                    p.gender, p.blood_type, p.phone, p.address, p.photo_path
                FROM patients p
                WHERE p.user_id = %s""",
                (user_id,)
            )
            patient_data = cursor.fetchone()

            if patient_data:
                # Display photo if exists
                if patient_data[8] and os.path.exists(patient_data[8]):
                    try:
                        image = Image.open(patient_data[8])
                        image = image.resize((150, 150), Image.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        photo_label = tk.Label(scrollable_frame, image=photo, bg="#f0f8ff")
                        photo_label.image = photo  # Keep reference
                        photo_label.pack(pady=10)
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to load photo: {e}")

                # Display patient information
                info_frame = tk.Frame(scrollable_frame, bg="#f0f8ff")
                info_frame.pack(pady=10)

                labels = [
                    ("Patient ID:", patient_data[0]),
                    ("First Name:", patient_data[1]),
                    ("Last Name:", patient_data[2]),
                    ("Date of Birth:", patient_data[3].strftime('%Y-%m-%d') if patient_data[3] else 'N/A'),
                    ("Gender:", patient_data[4]),
                    ("Blood Type:", patient_data[5] or 'N/A'),
                    ("Phone:", patient_data[6] or 'N/A'),
                    ("Address:", patient_data[7] or 'N/A'),
                ]

                for i, (label, value) in enumerate(labels):
                    tk.Label(
                        info_frame,
                        text=label,
                        font=("Arial", 12, "bold"),
                        bg="#f0f8ff",
                    ).grid(row=i, column=0, padx=5, pady=5, sticky="e")
                    tk.Label(
                        info_frame,
                        text=value,
                        font=("Arial", 12),
                        bg="#f0f8ff",
                    ).grid(row=i, column=1, padx=5, pady=5, sticky="w")

                # Edit button
                button_frame = tk.Frame(scrollable_frame, bg="#f0f8ff")
                button_frame.pack(pady=20)

                tk.Button(
                    button_frame,
                    text="Edit Profile",
                    font=("Arial", 12, "bold"),
                    bg="#4CAF50",
                    fg="white",
                    command=lambda: self.show_patient_registration(edit_mode=True, user_id=user_id),
                ).pack(side=tk.LEFT, padx=10)

                # Go Back button
                tk.Button(
                    button_frame,
                    text="Go Back",
                    font=("Arial", 12),
                    bg="#2196F3",
                    fg="white",
                    command=lambda: self.show_patient_welcome(user_id),
                ).pack(side=tk.LEFT, padx=10)

            else:
                tk.Label(
                    scrollable_frame,
                    text="Patient data not found",
                    font=("Arial", 14),
                    bg="#f0f8ff",
                ).pack(pady=20)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load patient data: {e}")

    def show_book_appointment(self, user_id):
        # Clear content frame
        for widget in self.patient_content_frame.winfo_children():
            widget.destroy()

        # Create scrollable frame
        canvas = tk.Canvas(self.patient_content_frame, bg="#f0f8ff")
        scrollbar = ttk.Scrollbar(self.patient_content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f8ff")

       # Configure canvas scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack widgets
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        # Title
        tk.Label(
            scrollable_frame,
            text="Book Appointment",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=20)

        # Form fields
        fields_frame = tk.Frame(scrollable_frame, bg="#f0f8ff")
        fields_frame.pack(pady=10)

        # Doctor selection
        tk.Label(
            fields_frame,
            text="Select Doctor:",
            font=("Arial", 12),
            bg="#f0f8ff",
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        self.doctor_var = tk.StringVar()
        doctor_cb = ttk.Combobox(
            fields_frame,
            textvariable=self.doctor_var,
            font=("Arial", 12),
            state="readonly"
        )
        doctor_cb.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Load doctors
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT doctor_id, first_name, last_name, specialization FROM doctors"
            )
            doctors = [
                f"Dr. {first_name} {last_name} ({specialization})" 
                for doctor_id, first_name, last_name, specialization in cursor.fetchall()
            ]
            doctor_cb['values'] = doctors
            if doctors:
                doctor_cb.current(0)
        except Error as e:
            messagebox.showerror("Error", f"Failed to load doctors: {e}")

        # Date selection
        tk.Label(
            fields_frame,
            text="Appointment Date:",
            font=("Arial", 12),
            bg="#f0f8ff",
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        self.appt_date = DateEntry(
            fields_frame,
            font=("Arial", 12),
            date_pattern='yyyy-mm-dd'
        )
        self.appt_date.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Time selection
        tk.Label(
            fields_frame,
            text="Appointment Time:",
            font=("Arial", 12),
            bg="#f0f8ff",
        ).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        
        self.appt_time = ttk.Combobox(
            fields_frame,
            font=("Arial", 12),
            values=[f"{h:02d}:{m:02d}" for h in range(8, 18) for m in [0, 30]],
            state="readonly"
        )
        self.appt_time.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.appt_time.current(0)

        # Reason
        tk.Label(
            fields_frame,
            text="Reason:",
            font=("Arial", 12),
            bg="#f0f8ff",
        ).grid(row=3, column=0, padx=5, pady=5, sticky="ne")
        
        self.appt_reason = tk.Text(
            fields_frame,
            font=("Arial", 12),
            height=5,
            width=30
        )
        self.appt_reason.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Button frame
        button_frame = tk.Frame(scrollable_frame, bg="#f0f8ff")
        button_frame.pack(pady=20)

        # Submit button
        tk.Button(
            button_frame,
            text="Book Appointment",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.book_appointment(user_id),
        ).pack(side=tk.LEFT, padx=10)

        # Go Back button
        tk.Button(
            button_frame,
            text="Go Back",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=lambda: self.show_patient_welcome(user_id),
        ).pack(side=tk.LEFT, padx=10)

    def book_appointment(self, user_id):
        # Get form data
        doctor = self.doctor_var.get()
        date = self.appt_date.get_date()
        time = self.appt_time.get()
        reason = self.appt_reason.get("1.0", tk.END).strip()

        # Validate inputs
        if not all([doctor, date, time, reason]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            # Extract doctor ID
            doctor_id = int(doctor.split("(")[-1].split(")")[0])

            # Get patient ID
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT patient_id FROM patients WHERE user_id = %s",
                (user_id,)
            )
            patient_id = cursor.fetchone()[0]

            # Insert appointment
            cursor.execute(
                """INSERT INTO appointments 
                (patient_id, doctor_id, appointment_date, appointment_time, status, reason)
                VALUES (%s, %s, %s, %s, 'Scheduled', %s)""",
                (patient_id, doctor_id, date, time, reason)
            )
            self.db_connection.commit()

            messagebox.showinfo("Success", "Appointment booked successfully!")
            self.show_patient_appointments(user_id)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to book appointment: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_patient_appointments(self, user_id):
        # Clear content frame
        for widget in self.patient_content_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(
            self.patient_content_frame,
            text="My Appointments",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=20)

        # Create treeview with scrollbars
        tree_frame = tk.Frame(self.patient_content_frame, bg="#f0f8ff")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Vertical scrollbar
        y_scrollbar = ttk.Scrollbar(tree_frame)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview
        columns = ("ID", "Date", "Time", "Doctor", "Status", "Reason")
        self.appointments_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )

        # Configure scrollbars
        y_scrollbar.config(command=self.appointments_tree.yview)
        x_scrollbar.config(command=self.appointments_tree.xview)

        # Configure columns
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=120, anchor=tk.CENTER)

        self.appointments_tree.pack(fill=tk.BOTH, expand=True)

        # Load appointments
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT a.appointment_id, a.appointment_date, a.appointment_time, 
                    CONCAT(d.first_name, ' ', d.last_name), a.status, a.reason
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.doctor_id
                JOIN patients p ON a.patient_id = p.patient_id
                WHERE p.user_id = %s
                ORDER BY a.appointment_date DESC, a.appointment_time DESC""",
                (user_id,)
            )
            appointments = cursor.fetchall()

            for appt in appointments:
                # Format time if it's a timedelta
                time_str = appt[2]
                if isinstance(appt[2], timedelta):
                    total_seconds = int(appt[2].total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    time_str = f"{hours:02d}:{minutes:02d}"

                self.appointments_tree.insert("", tk.END, values=(
                    appt[0],
                    appt[1].strftime('%Y-%m-%d'),
                    time_str,
                    appt[3],
                    appt[4],
                    appt[5]
                ))

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load appointments: {e}")

        # Button frame
        button_frame = tk.Frame(self.patient_content_frame, bg="#f0f8ff")
        button_frame.pack(pady=10)

        # Cancel button
        tk.Button(
            button_frame,
            text="Cancel Appointment",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=lambda: self.cancel_appointment(user_id),
        ).pack(side=tk.LEFT, padx=10)

        # Go Back button
        tk.Button(
            button_frame,
            text="Go Back",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=lambda: self.show_patient_welcome(user_id),
        ).pack(side=tk.LEFT, padx=10)

    def cancel_appointment(self, user_id):
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an appointment to cancel")
            return

        appointment_id = self.appointments_tree.item(selected[0])['values'][0]
        
        confirm = messagebox.askyesno(
            "Confirm Cancellation",
            "Are you sure you want to cancel this appointment?"
        )
        if not confirm:
            return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "UPDATE appointments SET status = 'Cancelled' WHERE appointment_id = %s",
                (appointment_id,)
            )
            self.db_connection.commit()
            messagebox.showinfo("Success", "Appointment cancelled successfully")
            self.show_patient_appointments(user_id)
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to cancel appointment: {e}")

    def show_medical_records(self, user_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT mr.record_id, mr.date, mr.diagnosis, mr.treatment, mr.notes
                FROM medical_records mr
                JOIN patients p ON mr.patient_id = p.patient_id
                WHERE p.user_id = %s
                ORDER BY mr.date DESC""",
                (user_id,)
            )
            records = cursor.fetchall()
            
            # Create new window
            records_window = tk.Toplevel(self.root)
            records_window.title("Medical Records")
            records_window.geometry("800x600")
            records_window.resizable(False, False)
            records_window.configure(bg="#f0f8ff")

            # Header
            header_frame = tk.Frame(records_window, bg="#3498db", height=60)
            header_frame.pack(fill=tk.X)
            tk.Label(
                header_frame,
                text="Medical Records",
                font=("Arial", 18, "bold"),
                bg="#3498db",
                fg="white"
            ).pack(pady=15)

            # Records display
            records_frame = tk.Frame(records_window, bg="#f0f8ff", padx=20, pady=20)
            records_frame.pack(fill=tk.BOTH, expand=True)

            if not records:
                tk.Label(
                    records_frame,
                    text="No medical records found",
                    font=("Arial", 12),
                    bg="#f0f8ff"
                ).pack(pady=20)
            else:
                # Create scrollable canvas for records
                canvas = tk.Canvas(records_frame, bg="#f0f8ff")
                scrollbar = ttk.Scrollbar(records_frame, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg="#f0f8ff")

                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")

                # Display records
                fields = ["Record ID:", "Date:", "Diagnosis:", "Treatment:", "Notes:"]
                for i, record in enumerate(records):
                    tk.Label(
                        scrollable_frame,
                        text=f"Record {i+1}",
                        font=("Arial", 14, "bold"),
                        bg="#f0f8ff",
                        fg="#2c3e50"
                    ).grid(row=i*6, column=0, columnspan=2, pady=(10, 5), sticky="w")
                    for j, (field, value) in enumerate(zip(fields, record)):
                        tk.Label(
                            scrollable_frame,
                            text=field,
                            font=("Arial", 12, "bold"),
                            bg="#f0f8ff"
                        ).grid(row=i*6+j+1, column=0, pady=2, padx=10, sticky="e")
                        tk.Label(
                            scrollable_frame,
                            text=value if value else "N/A",
                            font=("Arial", 12),
                            bg="#f0f8ff"
                        ).grid(row=i*6+j+1, column=1, pady=2, padx=10, sticky="w")

            # Close button
            button_frame = tk.Frame(records_frame, bg="#f0f8ff")
            button_frame.pack(pady=20)
            tk.Button(
                button_frame,
                text="Close",
                font=("Arial", 12),
                bg="#e74c3c",
                fg="white",
                command=records_window.destroy
            ).pack()

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load medical records: {e}")
            self.logger.error(f"Database error in show_medical_records: {e}")
        finally:
            if cursor:
                cursor.close()


    def show_patient_billing(self, user_id):
        # Clear content frame
        for widget in self.patient_content_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(
            self.patient_content_frame,
            text="My Billing/Payments",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=20)

        # Create treeview with scrollbars
        tree_frame = tk.Frame(self.patient_content_frame, bg="#f0f8ff")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Vertical scrollbar
        y_scrollbar = ttk.Scrollbar(tree_frame)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview
        columns = ("Bill ID", "Date", "Amount", "Description", "Status")
        self.billing_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )

        # Configure scrollbars
        y_scrollbar.config(command=self.billing_tree.yview)
        x_scrollbar.config(command=self.billing_tree.xview)

        # Configure columns
        for col in columns:
            self.billing_tree.heading(col, text=col)
            self.billing_tree.column(col, width=120, anchor=tk.CENTER)

        self.billing_tree.pack(fill=tk.BOTH, expand=True)

        # Load billing records
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT b.bill_id, b.bill_date, b.amount, b.description, b.payment_status
                FROM billing b
                JOIN patients p ON b.patient_id = p.patient_id
                WHERE p.user_id = %s
                ORDER BY b.bill_date DESC""",
                (user_id,)
            )
            bills = cursor.fetchall()

            total_amount = 0
            paid_amount = 0

            for bill in bills:
                self.billing_tree.insert("", tk.END, values=(
                    bill[0],
                    bill[1].strftime('%Y-%m-%d'),
                    f"${bill[2]:.2f}",
                    bill[3],
                    bill[4]
                ))

                total_amount += bill[2]
                if bill[4] == "Paid":
                    paid_amount += bill[2]

            # Summary
            summary_frame = tk.Frame(self.patient_content_frame, bg="#f0f8ff")
            summary_frame.pack(pady=10)

            tk.Label(
                summary_frame,
                text=f"Total Amount: ${total_amount:.2f}",
                font=("Arial", 12, "bold"),
                bg="#f0f8ff"
            ).pack(side=tk.LEFT, padx=10)

            tk.Label(
                summary_frame,
                text=f"Paid: ${paid_amount:.2f}",
                font=("Arial", 12),
                bg="#f0f8ff"
            ).pack(side=tk.LEFT, padx=10)

            tk.Label(
                summary_frame,
                text=f"Balance: ${(total_amount - paid_amount):.2f}",
                font=("Arial", 12),
                bg="#f0f8ff"
            ).pack(side=tk.LEFT, padx=10)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load billing records: {e}")

        # Button frame
        button_frame = tk.Frame(self.patient_content_frame, bg="#f0f8ff")
        button_frame.pack(pady=10)

        # Pay button
        tk.Button(
            button_frame,
            text="Make Payment",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.make_payment(user_id),
        ).pack(side=tk.LEFT, padx=10)

        # Go Back button
        tk.Button(
            button_frame,
            text="Go Back",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=lambda: self.show_patient_welcome(user_id),
        ).pack(side=tk.LEFT, padx=10)

    def make_payment(self, user_id):
        selected = self.billing_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a bill to pay")
            return

        bill_id = self.billing_tree.item(selected[0])['values'][0]
        bill_status = self.billing_tree.item(selected[0])['values'][4]
        
        if bill_status == "Paid":
            messagebox.showinfo("Info", "This bill has already been paid")
            return

        # Create payment window
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Make Payment")
        payment_window.geometry("400x300")

        # Payment form
        tk.Label(
            payment_window,
            text=f"Payment for Bill #{bill_id}",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Amount
        amount = float(self.billing_tree.item(selected[0])['values'][2].replace('$', ''))
        tk.Label(
            payment_window,
            text=f"Amount: ${amount:.2f}",
            font=("Arial", 12)
        ).pack(pady=5)

        # Payment method
        tk.Label(
            payment_window,
            text="Payment Method:",
            font=("Arial", 12)
        ).pack(pady=5)
        
        payment_method = ttk.Combobox(
            payment_window,
            values=["Credit Card", "Debit Card", "Bank Transfer", "Cash"],
            state="readonly"
        )
        payment_method.pack(pady=5)
        payment_method.current(0)

        # Submit button
        tk.Button(
            payment_window,
            text="Submit Payment",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.process_payment(user_id, bill_id, amount, payment_method.get(), payment_window),
        ).pack(pady=20)

    def process_payment(self, user_id, bill_id, amount, method, window):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "UPDATE billing SET payment_status = 'Paid', payment_method = %s, payment_date = CURDATE() WHERE bill_id = %s",
                (method, bill_id)
            )
            self.db_connection.commit()
            messagebox.showinfo("Success", "Payment processed successfully")
            window.destroy()
            self.show_patient_billing(user_id)
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to process payment: {e}")

    def show_patient_profile(self, user_id):
        # Clear content frame
        for widget in self.patient_content_frame.winfo_children():
            widget.destroy()

        try:
            cursor = self.db_connection.cursor()
            
            # Get patient information including photo path
            cursor.execute(
                """SELECT p.patient_id, p.first_name, p.last_name, p.date_of_birth, 
                        p.gender, p.blood_type, p.phone, p.address, p.photo_path,
                        u.username
                FROM patients p
                JOIN users u ON p.user_id = u.user_id
                WHERE p.user_id = %s""",
                (user_id,)
            )
            patient_data = cursor.fetchone()

            if not patient_data:
                messagebox.showerror("Error", "Patient not found")
                return

            # Main profile container with modern styling
            profile_container = tk.Frame(
                self.patient_content_frame, 
                bg="#f8f9fa",
                padx=20,
                pady=20
            )
            profile_container.pack(fill=tk.BOTH, expand=True)

            # Header frame with patient name
            header_frame = tk.Frame(
                profile_container,
                bg="#2c3e50",
                padx=15,
                pady=15
            )
            header_frame.pack(fill=tk.X, pady=(0, 20))

            tk.Label(
                header_frame,
                text=f"{patient_data[1]} {patient_data[2]}'s Profile",
                font=("Arial", 18, "bold"),
                bg="#2c3e50",
                fg="white"
            ).pack(side=tk.LEFT)

            # Main content frame (photo + details)
            content_frame = tk.Frame(profile_container, bg="#f8f9fa")
            content_frame.pack(fill=tk.BOTH, expand=True)

            # Photo frame (left side)
            photo_frame = tk.Frame(content_frame, bg="#f8f9fa", width=200)
            photo_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

            # Display patient photo or placeholder
            self.current_patient_photo_path = patient_data[8]  # Store photo path for upload
            self.patient_photo_label = tk.Label(
                photo_frame,
                bg="#e0e0e0",
                width=180,
                height=180,
                relief="solid",
                bd=1
            )
            self.patient_photo_label.pack(pady=(0, 10))

            # Load and display photo if exists
            if patient_data[8] and os.path.exists(patient_data[8]):
                try:
                    img = Image.open(patient_data[8])
                    img = img.resize((180, 180), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.patient_photo_label.config(image=photo)
                    self.patient_photo_label.image = photo
                except Exception as e:
                    print(f"Error loading image: {e}")
                    self.show_default_photo()
            else:
                self.show_default_photo()

            # Upload/change photo button
            upload_btn = tk.Button(
                photo_frame,
                text="Upload/Change Photo",
                font=("Arial", 10),
                bg="#3498db",
                fg="white",
                command=lambda: self.upload_patient_photo(user_id)
            )
            upload_btn.pack(pady=5)

            # Details frame (right side)
            details_frame = tk.Frame(content_frame, bg="#f8f9fa")
            details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Create a modern details table
            details = [
                ("Patient ID:", patient_data[0]),
                ("Username:", patient_data[9]),
                ("Date of Birth:", patient_data[3].strftime("%Y-%m-%d") if patient_data[3] else "N/A"),
                ("Gender:", patient_data[4]),
                ("Blood Type:", patient_data[5] or "N/A"),
                ("Phone:", patient_data[6] or "N/A"),
                ("Address:", patient_data[7] or "N/A")
            ]

            for i, (label, value) in enumerate(details):
                # Label
                tk.Label(
                    details_frame,
                    text=label,
                    font=("Arial", 12, "bold"),
                    bg="#f8f9fa",
                    fg="#2c3e50",
                    anchor="e"
                ).grid(row=i, column=0, sticky="e", padx=5, pady=5)

                # Value
                value_label = tk.Label(
                    details_frame,
                    text=value,
                    font=("Arial", 12),
                    bg="#f8f9fa",
                    fg="#34495e",
                    anchor="w"
                )
                value_label.grid(row=i, column=1, sticky="w", padx=5, pady=5)

            # Edit profile button
            edit_btn = tk.Button(
            profile_container,
            text="Edit Profile",
            font=("Arial", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            command=lambda: self.show_patient_registration(user_id=user_id)
        )
            edit_btn.pack(pady=20)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load patient data: {e}")

    def show_default_photo(self):
        # Create a default photo placeholder
        img = Image.new("RGB", (180, 180), "#e0e0e0")
        draw = ImageDraw.Draw(img)
        draw.text((60, 80), "No Photo", fill="#777777")
        photo = ImageTk.PhotoImage(img)
        self.patient_photo_label.config(image=photo)
        self.patient_photo_label.image = photo

    def upload_patient_photo(self, user_id):
        # Open file dialog to select image
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        
        if file_path:
            try:
                # Store the new photo path
                self.current_patient_photo_path = file_path
                
                # Display the new photo
                img = Image.open(file_path)
                img = img.resize((180, 180), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.patient_photo_label.config(image=photo)
                self.patient_photo_label.image = photo
                
                # Update database with new photo path
                cursor = self.db_connection.cursor()
                cursor.execute(
                    "UPDATE patients SET photo_path = %s WHERE user_id = %s",
                    (file_path, user_id)
                )
                self.db_connection.commit()
                
                messagebox.showinfo("Success", "Profile photo updated successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update photo: {e}")
            
    def update_patient_profile(self, user_id, window):
        # Get all form data using the consistent naming
        # ===== CHANGED THESE LINES =====
        first_name = self.edit_profile_entries["first_name"].get()
        last_name = self.edit_profile_entries["last_name"].get()
        dob = self.edit_profile_entries["date_of_birth"].get()
        gender = self.edit_profile_entries["gender"].get()
        blood_type = self.edit_profile_entries["blood_type"].get()
        phone = self.edit_profile_entries["phone"].get()
        address = self.edit_profile_entries["address"].get("1.0", tk.END).strip()
        username = self.edit_profile_entries["username"].get()
        new_password = self.edit_profile_entries["new_password"].get()
        confirm_password = self.edit_profile_entries["confirm_password"].get()
        # ===== END OF CHANGES =====

        # Validate inputs
        if not all([first_name, last_name, dob, gender, phone, address, username]):
            messagebox.showerror("Error", "All fields except blood type are required")
            return

        if new_password and new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Get patient_id
            cursor.execute("SELECT patient_id FROM patients WHERE user_id = %s", (user_id,))
            patient_id = cursor.fetchone()[0]

            # Check if username exists (excluding current user)
            cursor.execute(
                "SELECT username FROM users WHERE username = %s AND user_id != %s",
                (username, user_id)
            )
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return

            # Update patients table
            cursor.execute(
                """UPDATE patients 
                SET first_name = %s, last_name = %s, date_of_birth = %s, 
                    gender = %s, blood_type = %s, phone = %s, address = %s
                WHERE patient_id = %s""",
                (first_name, last_name, dob, gender, 
                blood_type if blood_type else None, phone, address, patient_id)
            )

            # Update users table
            if new_password:
                hashed_password = self.hash_password(new_password)
                cursor.execute(
                    "UPDATE users SET username = %s, password = %s WHERE user_id = %s",
                    (username, hashed_password, user_id)
                )
            else:
                cursor.execute(
                    "UPDATE users SET username = %s WHERE user_id = %s",
                    (username, user_id)
                )

            self.db_connection.commit()
            messagebox.showinfo("Success", "Profile updated successfully!")
            window.destroy()
            self.show_patient_profile(user_id)  # Refresh profile view

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to update profile: {e}")
        finally:
            if cursor:
                cursor.close()
                        
    def show_edit_profile(self, user_id):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Profile")
        edit_window.geometry("600x700")
        edit_window.configure(bg="#f8f9fa")

        # Header
        header = tk.Frame(edit_window, bg="#3498db", height=80)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="Edit Profile",
            font=("Arial", 18, "bold"),
            bg="#3498db",
            fg="white"
        ).pack(pady=20)

        # Main form container
        form_container = tk.Frame(edit_window, bg="#f8f9fa", padx=20, pady=20)
        form_container.pack(fill=tk.BOTH, expand=True)

        try:
            cursor = self.db_connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.*, u.username 
                FROM patients p 
                JOIN users u ON p.user_id = u.user_id 
                WHERE p.user_id = %s
            """, (user_id,))
            patient_data = cursor.fetchone()

            if patient_data:
                # ===== CHANGED THIS SECTION =====
                # Form fields with consistent naming
                fields = [
                    ("First Name", "entry", patient_data['first_name']),
                    ("Last Name", "entry", patient_data['last_name']),
                    ("Date of Birth", "entry", patient_data['date_of_birth']),  # Simplified label
                    ("Gender", "combobox", patient_data['gender'], ["Male", "Female", "Other"]),
                    ("Blood Type", "combobox", patient_data['blood_type'], 
                    ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
                    ("Phone", "entry", patient_data['phone']),
                    ("Address", "text", patient_data['address']),
                    ("Username", "entry", patient_data['username']),
                    ("New Password", "password", ""),
                    ("Confirm Password", "password", "")
                ]
                # ===== END OF CHANGES =====

                self.edit_profile_entries = {}

                for i, (label, field_type, default_value, *options) in enumerate(fields):
                    # Field container
                    field_frame = tk.Frame(form_container, bg="#f8f9fa")
                    field_frame.pack(fill=tk.X, pady=5)

                    # Label
                    tk.Label(
                        field_frame,
                        text=label + ":",  # Add colon here for display
                        font=("Arial", 10, "bold"),
                        bg="#f8f9fa",
                        fg="#2c3e50",
                        width=25,
                        anchor="e"
                    ).pack(side=tk.LEFT, padx=5)

                    # Input field
                    if field_type == "entry":
                        entry = tk.Entry(
                            field_frame,
                            font=("Arial", 10),
                            bd=1,
                            relief=tk.SOLID
                        )
                        entry.insert(0, default_value)
                        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
                    elif field_type == "combobox":
                        entry = ttk.Combobox(
                            field_frame,
                            font=("Arial", 10),
                            values=options[0],
                            state="readonly"
                        )
                        entry.set(default_value or "")
                        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
                    elif field_type == "text":
                        entry = tk.Text(
                            field_frame,
                            font=("Arial", 10),
                            height=4,
                            bd=1,
                            relief=tk.SOLID
                        )
                        entry.insert("1.0", default_value)
                        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
                    elif field_type == "password":
                        entry = tk.Entry(
                            field_frame,
                            font=("Arial", 10),
                            show="*",
                            bd=1,
                            relief=tk.SOLID
                        )
                        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

                    # ===== CHANGED THIS LINE =====
                    field_name = label.lower().replace(" ", "_")
                    self.edit_profile_entries[field_name] = entry
                    # ===== END OF CHANGE =====

                # Button container
                button_frame = tk.Frame(form_container, bg="#f8f9fa", pady=20)
                button_frame.pack(fill=tk.X)

                # Save button
                save_btn = tk.Button(
                    button_frame,
                    text="Save Changes",
                    font=("Arial", 12, "bold"),
                    bg="#2ecc71",
                    fg="white",
                    bd=0,
                    padx=20,
                    pady=5,
                    command=lambda: self.update_patient_profile(user_id, edit_window)
                )
                save_btn.pack(side=tk.RIGHT, padx=10)

                # Cancel button
                cancel_btn = tk.Button(
                    button_frame,
                    text="Cancel",
                    font=("Arial", 12),
                    bg="#e74c3c",
                    fg="white",
                    bd=0,
                    padx=20,
                    pady=5,
                    command=edit_window.destroy
                )
                cancel_btn.pack(side=tk.RIGHT)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load profile: {e}")
            

    def show_patient_appointments(self, user_id):
        # Clear content frame
        for widget in self.patient_content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.patient_content_frame,
            text="My Appointments",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=10)

        # New appointment button
        new_btn = tk.Button(
            self.patient_content_frame,
            text="Schedule New Appointment",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.show_schedule_appointment_form(user_id),
        )
        new_btn.pack(pady=10)

        # Appointments table
        columns = ("ID", "Date", "Time", "Doctor", "Status", "Reason")
        self.patient_appointments_tree = ttk.Treeview(
            self.patient_content_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.patient_appointments_tree.heading(col, text=col)
            self.patient_appointments_tree.column(col, width=120, anchor=tk.CENTER)

        self.patient_appointments_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Load appointments data
        self.load_patient_appointments(user_id)

        # Action buttons frame
        action_frame = tk.Frame(self.patient_content_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)

        cancel_btn = tk.Button(
            action_frame,
            text="Cancel Appointment",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=lambda: self.cancel_patient_appointment(user_id),
        )
        cancel_btn.grid(row=0, column=0, padx=10)


    def show_medical_records(patient_id, host, database, user, password):
        """Display comprehensive medical records in a scrollable window"""
        try:
            # Connect to database
            conn = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            
            # Create main window
            window = tk.Toplevel()
            window.title(f"Medical Records - Patient ID: {patient_id}")
            window.geometry("900x600")
            
            # Create main frame with scrollbar
            main_frame = tk.Frame(window)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            canvas = tk.Canvas(main_frame)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Fetch patient data
            cursor = conn.cursor(dictionary=True)
            
            # Get patient info
            cursor.execute("""
                SELECT first_name, last_name, date_of_birth, gender, blood_type 
                FROM patients WHERE patient_id = %s
            """, (patient_id,))
            patient_info = cursor.fetchone()
            
            # Display patient info at top
            info_frame = tk.LabelFrame(scrollable_frame, text="Patient Information", padx=10, pady=10)
            info_frame.pack(fill="x", padx=10, pady=5)
            
            tk.Label(info_frame, text=f"Name: {patient_info['first_name']} {patient_info['last_name']}").pack(anchor="w")
            tk.Label(info_frame, text=f"DOB: {patient_info['date_of_birth']}").pack(anchor="w")
            tk.Label(info_frame, text=f"Gender: {patient_info['gender']}").pack(anchor="w")
            tk.Label(info_frame, text=f"Blood Type: {patient_info['blood_type']}").pack(anchor="w")
            
            # Get medical records with doctor info
            cursor.execute("""
                SELECT mr.*, d.first_name AS doctor_first_name, 
                    d.last_name AS doctor_last_name, d.specialization
                FROM medical_records mr
                JOIN doctors d ON mr.doctor_id = d.doctor_id
                WHERE mr.patient_id = %s
                ORDER BY mr.record_date DESC
            """, (patient_id,))
            medical_records = cursor.fetchall()
            
            # Medical Records Section
            if medical_records:
                med_frame = tk.LabelFrame(scrollable_frame, text="Medical Records", padx=10, pady=10)
                med_frame.pack(fill="x", padx=10, pady=5)
                
                for record in medical_records:
                    record_frame = tk.Frame(med_frame, relief="groove", borderwidth=1, padx=5, pady=5)
                    record_frame.pack(fill="x", pady=3)
                    
                    tk.Label(record_frame, 
                            text=f"Date: {record['record_date']} | Doctor: Dr. {record['doctor_first_name']} {record['doctor_last_name']} ({record['specialization']})",
                            font=('Arial', 10, 'bold')).pack(anchor="w")
                    
                    tk.Label(record_frame, text=f"Diagnosis: {record['diagnosis']}").pack(anchor="w")
                    if record['treatment']:
                        tk.Label(record_frame, text=f"Treatment: {record['treatment']}").pack(anchor="w")
                    if record['notes']:
                        tk.Label(record_frame, text=f"Notes: {record['notes']}").pack(anchor="w")
                    
                    tk.Label(record_frame, text="-"*80, fg="gray").pack(anchor="w")
            else:
                tk.Label(scrollable_frame, text="No medical records found").pack()
            
            # Get appointments
            cursor.execute("""
                SELECT a.*, d.first_name AS doctor_first_name, 
                    d.last_name AS doctor_last_name, d.specialization
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE a.patient_id = %s
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            """, (patient_id,))
            appointments = cursor.fetchall()
            
            # Appointments Section
            if appointments:
                app_frame = tk.LabelFrame(scrollable_frame, text="Appointments", padx=10, pady=10)
                app_frame.pack(fill="x", padx=10, pady=5)
                
                for app in appointments:
                    app_subframe = tk.Frame(app_frame, relief="groove", borderwidth=1, padx=5, pady=5)
                    app_subframe.pack(fill="x", pady=3)
                    
                    tk.Label(app_subframe, 
                            text=f"Date: {app['appointment_date']} {app['appointment_time']} | Status: {app['status'].title()}",
                            font=('Arial', 10, 'bold')).pack(anchor="w")
                    
                    tk.Label(app_subframe, 
                            text=f"Doctor: Dr. {app['doctor_first_name']} {app['doctor_last_name']} ({app['specialization']})").pack(anchor="w")
                    
                    if app['reason']:
                        tk.Label(app_subframe, text=f"Reason: {app['reason']}").pack(anchor="w")
                    
                    tk.Label(app_subframe, text="-"*80, fg="gray").pack(anchor="w")
            
            # Get billing information
            cursor.execute("""
                SELECT b.*, p.payment_id, p.amount AS payment_amount, 
                    p.payment_method, p.payment_date, p.transaction_reference
                FROM billing b
                LEFT JOIN payments p ON b.bill_id = p.bill_id
                WHERE b.patient_id = %s
                ORDER BY b.bill_date DESC
            """, (patient_id,))
            billing_records = cursor.fetchall()
            
            # Billing Section
            if billing_records:
                bill_frame = tk.LabelFrame(scrollable_frame, text="Billing History", padx=10, pady=10)
                bill_frame.pack(fill="x", padx=10, pady=5)
                
                for bill in billing_records:
                    bill_subframe = tk.Frame(bill_frame, relief="groove", borderwidth=1, padx=5, pady=5)
                    bill_subframe.pack(fill="x", pady=3)
                    
                    tk.Label(bill_subframe, 
                            text=f"Bill Date: {bill['bill_date']} | Amount: ${bill['amount']} | Status: {bill['status']}",
                            font=('Arial', 10, 'bold')).pack(anchor="w")
                    
                    if bill['description']:
                        tk.Label(bill_subframe, text=f"Description: {bill['description']}").pack(anchor="w")
                    
                    if bill['payment_id']:
                        tk.Label(bill_subframe, 
                                text=f"Payment: ${bill['payment_amount']} via {bill['payment_method']} on {bill['payment_date']}").pack(anchor="w")
                    
                    tk.Label(bill_subframe, text="-"*80, fg="gray").pack(anchor="w")
            
            # Close database connection
            cursor.close()
            conn.close()
            
        except Error as e:
            error_window = tk.Toplevel()
            error_window.title("Database Error")
            tk.Label(error_window, text=f"Failed to load medical records:\n{str(e)}", fg="red").pack()
            tk.Button(error_window, text="OK", command=error_window.destroy).pack()




            
    def load_patient_appointments(self, user_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT a.appointment_id, a.appointment_date, a.appointment_time,
                        CONCAT(d.first_name, ' ', d.last_name), a.status, a.reason
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE a.patient_id = (SELECT patient_id FROM patients WHERE user_id = %s)
                ORDER BY a.appointment_date DESC, a.appointment_time DESC""",
                (user_id,)
            )
            appointments = cursor.fetchall()

            # Clear existing data
            for item in self.patient_appointments_tree.get_children():
                self.patient_appointments_tree.delete(item)

            # Insert new data
            for appointment in appointments:
                self.patient_appointments_tree.insert("", tk.END, values=appointment)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load appointments: {e}")

    def show_schedule_appointment_form(self, user_id):
        # Create appointment booking window
        add_window = tk.Toplevel(self.root)
        add_window.title("Schedule Appointment")
        add_window.geometry("500x500")
        add_window.resizable(False, False)
        
        # Styling
        bg_color = "#f0f8ff"
        add_window.configure(bg=bg_color)
        
        # Header
        header_frame = tk.Frame(add_window, bg="#3498db", height=60)
        header_frame.pack(fill=tk.X)
        tk.Label(
            header_frame,
            text="Book New Appointment",
            font=("Arial", 16, "bold"),
            bg="#3498db",
            fg="white"
        ).pack(pady=15)

        # Main form container
        form_frame = tk.Frame(add_window, bg=bg_color, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Doctor Selection
        tk.Label(
            form_frame,
            text="Select Doctor:",
            font=("Arial", 12),
            bg=bg_color
        ).grid(row=0, column=0, pady=5, sticky="e")

        self.doctor_var = tk.StringVar()
        doctor_combobox = ttk.Combobox(
            form_frame,
            textvariable=self.doctor_var,
            font=("Arial", 12),
            state="readonly",
            width=25
        )
        doctor_combobox.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        # Load doctors into combobox
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                SELECT doctor_id, CONCAT(first_name, ' ', last_name, ' - ', specialization) 
                FROM doctors
            """)
            doctors = cursor.fetchall()
            
            # Format: "Dr. Name - Specialty (ID: 123)"
            doctor_list = [f"{name} (ID: {id})" for id, name in doctors]
            doctor_combobox['values'] = doctor_list
            
            if doctor_list:
                doctor_combobox.current(0)
            else:
                messagebox.showwarning("No Doctors", "No doctors available for appointments")
                add_window.destroy()
                return
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load doctors: {e}")
            add_window.destroy()
            return

        # Date Selection
        tk.Label(
            form_frame,
            text="Appointment Date:",
            font=("Arial", 12),
            bg=bg_color
        ).grid(row=1, column=0, pady=5, sticky="e")

        self.date_var = tk.StringVar()
        date_entry = tk.Entry(
            form_frame,
            textvariable=self.date_var,
            font=("Arial", 12),
            width=25
        )
        date_entry.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Default to today

        # Time Selection
        tk.Label(
            form_frame,
            text="Appointment Time:",
            font=("Arial", 12),
            bg=bg_color
        ).grid(row=2, column=0, pady=5, sticky="e")

        self.time_var = tk.StringVar()
        time_combobox = ttk.Combobox(
            form_frame,
            textvariable=self.time_var,
            font=("Arial", 12),
            values=["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"],
            state="readonly",
            width=25
        )
        time_combobox.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        time_combobox.current(0)  # Default to first time slot

        # Reason for Visit
        tk.Label(
            form_frame,
            text="Reason:",
            font=("Arial", 12),
            bg=bg_color
        ).grid(row=3, column=0, pady=5, sticky="ne")

        self.reason_text = tk.Text(
            form_frame,
            font=("Arial", 12),
            height=4,
            width=30,
            wrap=tk.WORD
        )
        self.reason_text.grid(row=3, column=1, pady=5, padx=5, sticky="w")

        # Submit Button
        submit_btn = tk.Button(
            form_frame,
            text="Book Appointment",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=20,
            command=lambda: self.schedule_appointment(user_id, add_window)
        )
        submit_btn.grid(row=4, column=1, pady=20, sticky="e")

        # Cancel Button
        cancel_btn = tk.Button(
            form_frame,
            text="Cancel",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            width=10,
            command=add_window.destroy
        )
        cancel_btn.grid(row=4, column=0, pady=20, sticky="w")
        
    def schedule_appointment(self, user_id, window):
            try:
                # Get selected doctor (extract ID from combobox)
                doctor_str = self.doctor_var.get()
                doctor_id = int(doctor_str.split("(ID: ")[1].replace(")", ""))
                
                date = self.date_var.get()
                time = self.time_var.get()
                reason = self.reason_text.get("1.0", tk.END).strip()

                # Validate inputs
                if not all([doctor_id, date, time]):
                    messagebox.showerror("Error", "Please fill all required fields")
                    return

                # Get patient_id from user_id
                cursor = self.db_connection.cursor()
                cursor.execute("SELECT patient_id FROM patients WHERE user_id = %s", (user_id,))
                patient_id = cursor.fetchone()[0]

                # Check if time slot is available
                cursor.execute("""
                    SELECT appointment_id FROM appointments 
                    WHERE doctor_id = %s AND appointment_date = %s AND appointment_time = %s
                """, (doctor_id, date, time))
                
                if cursor.fetchone():
                    messagebox.showerror("Error", "This time slot is already booked")
                    return

                # Book appointment
                cursor.execute("""
                    INSERT INTO appointments 
                    (patient_id, doctor_id, appointment_date, appointment_time, status, reason)
                    VALUES (%s, %s, %s, %s, 'Scheduled', %s)
                """, (patient_id, doctor_id, date, time, reason))
                
                self.db_connection.commit()
                messagebox.showinfo("Success", "Appointment booked successfully!")
                window.destroy()
                
                # Refresh appointments view if needed
                if hasattr(self, 'show_patient_appointments'):
                    self.show_patient_appointments(user_id)
                    
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
            except Error as e:
                self.db_connection.rollback()
                messagebox.showerror("Database Error", f"Failed to book appointment: {str(e)}")
        

    def cancel_patient_appointment(self, user_id):
        selected_item = self.patient_appointments_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an appointment to cancel")
            return
        appointment_id = self.patient_appointments_tree.item(selected_item)["values"][0]
        status = self.patient_appointments_tree.item(selected_item)["values"][4]

        # Make status check case-insensitive
        if status.lower() != "scheduled":
            messagebox.showerror("Error", "Only scheduled appointments can be cancelled")
            return
        confirm = messagebox.askyesno(
            "Confirm", "Are you sure you want to cancel this appointment?"
        )
        if not confirm:
            return

        try:
            cursor = self.db_connection.cursor()
            # Use parameterized query to prevent SQL injection
            cursor.execute(
                "UPDATE appointments SET status = 'Cancelled' WHERE appointment_id = %s AND status = 'Scheduled'",
                (appointment_id,)
            )

            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Appointment could not be cancelled. It may have already been processed.")
            else:
                self.db_connection.commit()
                messagebox.showinfo("Success", "Appointment cancelled successfully!")
            
            # Refresh the appointments list
            self.load_patient_appointments(user_id)

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to cancel appointment: {e}")

    def show_patient_medical_records(self, user_id):
        # Clear the frame
        for widget in self.patient_content_frame.winfo_children():
            widget.destroy()

        # Get patient_id
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT patient_id FROM patients WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Patient not found.")
                return
            patient_id = result[0]
        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching patient ID: {e}")
            return

        # Title
        tk.Label(
            self.patient_content_frame,
            text="My Medical Records",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff"
        ).pack(pady=10)

        # Table of short summaries
        columns = ("Date", "Doctor", "Diagnosis")
        self.patient_records_tree = ttk.Treeview(
            self.patient_content_frame, columns=columns, show="headings", height=15
        )
        for col in columns:
            self.patient_records_tree.heading(col, text=col)
            self.patient_records_tree.column(col, anchor=tk.CENTER, width=200)

        self.patient_records_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Fetch records
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT mr.record_date, mr.diagnosis, mr.treatment, mr.notes,
                    CONCAT(d.first_name, ' ', d.last_name) AS doctor_name,
                    d.specialization
                FROM medical_records mr
                JOIN doctors d ON mr.doctor_id = d.doctor_id
                WHERE mr.patient_id = %s
                ORDER BY mr.record_date DESC
            """, (patient_id,))
            records = cursor.fetchall()

            if not records:
                messagebox.showinfo("No Records", "No medical records found.")
                return

            self.medical_record_data = records  # Save for use in detail view

            # Insert short version into tree
            for record in records:
                self.patient_records_tree.insert(
                    "", tk.END,
                    values=(record["record_date"], record["doctor_name"], record["diagnosis"])
                )

            # Bind double-click to view details
            self.patient_records_tree.bind("<Double-1>", lambda e: self.view_medical_record_details())

        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching records: {e}")
        
    def view_medical_record_details(self):
        selected_item = self.patient_records_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record.")
            return

        index = self.patient_records_tree.index(selected_item)
        record = self.medical_record_data[index]

        # Create a details popup
        details_window = tk.Toplevel(self.root)
        details_window.title("Medical Record Details")
        details_window.geometry("600x500")

        tk.Label(
            details_window,
            text="Medical Record Details",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        frame = tk.Frame(details_window)
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Basic info
        info_text = (
            f"Date: {record['record_date']}\n"
            f"Doctor: {record['doctor_name']} ({record['specialization']})\n"
            f"Diagnosis: {record['diagnosis']}\n"
        )
        tk.Label(frame, text=info_text, font=("Arial", 12), justify="left").pack(anchor="w", pady=5)

        # Treatment
        if record["treatment"]:
            tk.Label(frame, text="Treatment:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 0))
            treatment_box = tk.Text(frame, font=("Arial", 12), height=4, wrap=tk.WORD)
            treatment_box.insert("1.0", record["treatment"])
            treatment_box.config(state=tk.DISABLED)
            treatment_box.pack(fill=tk.X)

        # Notes
        if record["notes"]:
            tk.Label(frame, text="Notes:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 0))
            notes_box = tk.Text(frame, font=("Arial", 12), height=5, wrap=tk.WORD)
            notes_box.insert("1.0", record["notes"])
            notes_box.config(state=tk.DISABLED)
            notes_box.pack(fill=tk.BOTH, expand=True)


    def show_patient_billing(self, user_id):
        # Clear content frame
        for widget in self.patient_content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.patient_content_frame,
            text="My Billing Information",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=10)

        # Billing table
        columns = ("Bill ID", "Date", "Amount", "Status", "Description")
        self.patient_bills_tree = ttk.Treeview(
            self.patient_content_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.patient_bills_tree.heading(col, text=col)
            self.patient_bills_tree.column(col, width=120, anchor=tk.CENTER)

        self.patient_bills_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Load billing data
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT bill_id, bill_date, amount, payment_status, description
                FROM billing
                WHERE patient_id = (SELECT patient_id FROM patients WHERE user_id = %s)
                ORDER BY bill_date DESC""",
                (user_id,)
            )
            bills = cursor.fetchall()

            # Insert bills
            for bill in bills:
                self.patient_bills_tree.insert("", tk.END, values=bill)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load billing information: {e}")

        # Action buttons frame
        action_frame = tk.Frame(self.patient_content_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)

        pay_btn = tk.Button(
            action_frame,
            text="Pay Bill",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.pay_bill,
        )
        pay_btn.grid(row=0, column=0, padx=10)

    def pay_bill(self):
        selected_item = self.patient_bills_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a bill to pay")
            return

        bill_id = self.patient_bills_tree.item(selected_item)["values"][0]
        status = self.patient_bills_tree.item(selected_item)["values"][3]
        amount = self.patient_bills_tree.item(selected_item)["values"][2]

        if status == "Paid":
            messagebox.showerror("Error", "This bill has already been paid")
            return

        confirm = messagebox.askyesno(
            "Confirm", f"Are you sure you want to pay this bill of ${amount:.2f}?"
        )
        if not confirm:
            return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "UPDATE billing SET payment_status = 'Paid' WHERE bill_id = %s",
                (bill_id,)
            )

            self.db_connection.commit()

            messagebox.showinfo("Success", "Bill paid successfully!")
            
            # Reload billing data
            self.show_patient_billing(self.current_user_id)

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to pay bill: {e}")
            
    def show_staff_dashboard(self, user_id):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Staff dashboard frame
        dashboard_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        dashboard_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = tk.Frame(dashboard_frame, bg="#2196F3", height=80)
        header_frame.pack(fill=tk.X)

        # Get staff member's name
        staff_name = ""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT first_name, last_name FROM staff WHERE user_id = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            if result:
                staff_name = f"{result[0]} {result[1]}"
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch staff data: {e}")

        tk.Label(
            header_frame,
            text=f"Staff Dashboard - {staff_name}",
            font=("Arial", 20, "bold"),
            bg="#2196F3",
            fg="white",
        ).pack(side=tk.LEFT, padx=20)

        logout_btn = tk.Button(
            header_frame,
            text="Logout",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=self.show_login_screen,
        )
        logout_btn.pack(side=tk.RIGHT, padx=20)

        # Navigation
        nav_frame = tk.Frame(dashboard_frame, bg="#333", width=200)
        nav_frame.pack(fill=tk.Y, side=tk.LEFT)

        buttons = [
            ("Dashboard", lambda: self.show_staff_welcome(user_id)),
            ("Manage Appointments", lambda: self.show_staff_appointments(user_id)),
            ("Manage Patients Record", lambda: self.show_manage_patient_records(user_id)),
            ("Manage Billing", lambda: self.show_staff_billing(user_id)),
        ]

        for text, command in buttons:
            tk.Button(
                nav_frame,
                text=text,
                font=("Arial", 12),
                bg="#333",
                fg="white",
                relief=tk.FLAT,
                command=command,
            ).pack(fill=tk.X, pady=2)

        # Main content area
        self.staff_content_frame = tk.Frame(dashboard_frame, bg="#f0f8ff")
        self.staff_content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        # Show default view
        self.show_staff_welcome(user_id)

    def show_staff_welcome(self, user_id):
        # Clear content frame
        for widget in self.staff_content_frame.winfo_children():
            widget.destroy()

        # Welcome title
        tk.Label(
            self.staff_content_frame,
            text="Staff Dashboard",
            font=("Arial", 24, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        ).pack(pady=(20, 10))

        # Cards container
        cards_frame = tk.Frame(self.staff_content_frame, bg="#f0f8ff")
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Card 1: Appointments
        appointment_card = tk.Frame(
            cards_frame,
            bg="white",
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=20
        )
        appointment_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(
            appointment_card,
            text="Appointments",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#3498db"
        ).pack(pady=(0, 10))

        # Get today's appointment count
        today_appointments = 0
        try:
            cursor = self.db_connection.cursor()
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(
                "SELECT COUNT(*) FROM appointments WHERE appointment_date = %s",
                (today,)
            )
            today_appointments = cursor.fetchone()[0]
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch appointment count: {e}")

        tk.Label(
            appointment_card,
            text=f"Today: {today_appointments}",
            font=("Arial", 14),
            bg="white"
        ).pack()

        tk.Button(
            appointment_card,
            text="Manage Appointments",
            font=("Arial", 12),
            bg="#3498db",
            fg="white",
            command=lambda: self.show_staff_appointments(user_id)
        ).pack(pady=(15, 0))

        # Card 2: Patient Records
        records_card = tk.Frame(
            cards_frame,
            bg="white",
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=20
        )
        records_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        tk.Label(
            records_card,
            text="Patient Records",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2ecc71"
        ).pack(pady=(0, 10))

        # Get total patient count
        total_patients = 0
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM patients")
            total_patients = cursor.fetchone()[0]
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch patient count: {e}")

        tk.Label(
            records_card,
            text=f"Total Patients: {total_patients}",
            font=("Arial", 14),
            bg="white"
        ).pack()

        tk.Button(
            records_card,
            text="View Records",
            font=("Arial", 12),
            bg="#2ecc71",
            fg="white",
            command=lambda: self.show_staff_patient_records(user_id)
        ).pack(pady=(15, 0))

        # Card 3: Billing
        billing_card = tk.Frame(
            cards_frame,
            bg="white",
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=20
        )
        billing_card.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        tk.Label(
            billing_card,
            text="Billing",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#e74c3c"
        ).pack(pady=(0, 10))

        # Get pending payments
        pending_payments = 0
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM billing WHERE payment_status = 'Pending'"
            )
            pending_payments = cursor.fetchone()[0]
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch billing data: {e}")

        tk.Label(
            billing_card,
            text=f"Pending: {pending_payments}",
            font=("Arial", 14),
            bg="white"
        ).pack()

        tk.Button(
            billing_card,
            text="Manage Billing",
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            command=lambda: self.show_staff_billing(user_id)
        ).pack(pady=(15, 0))

        # Configure grid weights
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.columnconfigure(2, weight=1)
        cards_frame.rowconfigure(0, weight=1)

        # Recent activity section
        activity_frame = tk.Frame(self.staff_content_frame, bg="#f0f8ff")
        activity_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(
            activity_frame,
            text="Recent Activity",
            font=("Arial", 18, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        ).pack(anchor="w", pady=(10, 5))

        # Activity list
        activity_list = tk.Frame(activity_frame, bg="white", relief=tk.SUNKEN, borderwidth=1)
        activity_list.pack(fill=tk.BOTH, expand=True)

        # Get recent activity (example data)
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                SELECT 'Appointment' as type, CONCAT('With ', d.first_name, ' ', d.last_name) as description, 
                    a.appointment_date as date
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.doctor_id
                ORDER BY a.appointment_date DESC
                LIMIT 5
            """)
            activities = cursor.fetchall()

            for i, (activity_type, description, date) in enumerate(activities):
                activity_item = tk.Frame(activity_list, bg="white")
                activity_item.pack(fill=tk.X, padx=5, pady=5)

                tk.Label(
                    activity_item,
                    text=f"{date.strftime('%Y-%m-%d')}: {description}",
                    font=("Arial", 12),
                    bg="white",
                    anchor="w"
                ).pack(side=tk.LEFT, padx=10)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch recent activity: {e}")
            
    def show_manage_patient_records(self,user_id):
        # Clear content frame
        for widget in self.staff_content_frame.winfo_children():
            widget.destroy()

        # Modern styling variables
        bg_color = "#f8f9fa"
        header_color = "#343a40"
        text_color = "#495057"
        accent_color = "#6c757d"
        button_color = "#007bff"
        hover_color = "#0056b3"

        # Main container with padding
        main_container = tk.Frame(self.staff_content_frame, bg=bg_color, padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header with modern styling
        header_frame = tk.Frame(main_container, bg=header_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="Manage Patient Records",
            font=("Helvetica", 20, "bold"),
            bg=header_color,
            fg="white",
            padx=10,
            pady=10
        ).pack(side=tk.LEFT)

        # Search frame
        search_frame = tk.Frame(main_container, bg=bg_color)
        search_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            search_frame,
            text="Search Patients:",
            font=("Helvetica", 12),
            bg=bg_color,
            fg=text_color
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.patient_search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.patient_search_var,
            font=("Helvetica", 12),
            width=30,
            bd=2,
            relief=tk.GROOVE
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind("<KeyRelease>", self.filter_patient_records)

        # Treeview frame with scrollbars
        tree_frame = tk.Frame(main_container, bg=bg_color)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Patient.Treeview",
                    background="white",
                    foreground=text_color,
                    fieldbackground="white",
                    rowheight=25,
                    font=("Helvetica", 10))
        style.configure("Patient.Treeview.Heading",
                    font=("Helvetica", 12, "bold"),
                    background=accent_color,
                    foreground="white",
                    relief=tk.FLAT)
        style.map("Patient.Treeview",
                background=[('selected', button_color)],
                foreground=[('selected', 'white')])

        # Treeview scrollbars
        y_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        x_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Patient records treeview
        columns = ("ID", "Name", "Gender", "DOB", "Blood Type", "Phone")
        self.patient_records_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Patient.Treeview",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
            selectmode="browse"
        )
        self.patient_records_tree.pack(fill=tk.BOTH, expand=True)

        # Configure scrollbars
        y_scroll.config(command=self.patient_records_tree.yview)
        x_scroll.config(command=self.patient_records_tree.xview)

        # Configure columns
        for col in columns:
            self.patient_records_tree.heading(col, text=col, anchor=tk.W)
            self.patient_records_tree.column(col, width=120, anchor=tk.W, stretch=True)

        # Load patient data
        self.load_patient_records()

        # Bind double click event to view patient details
        self.patient_records_tree.bind("<Double-1>", self.view_patient_details)

        # Button frame
        button_frame = tk.Frame(main_container, bg=bg_color)
        button_frame.pack(pady=(15, 0))

        view_btn = tk.Button(
            button_frame,
            text="View Details",
            font=("Helvetica", 12),
            bg=button_color,
            fg="white",
            activebackground=hover_color,
            bd=0,
            padx=15,
            pady=5,
            command=lambda: self.view_patient_details(None)
        )
        view_btn.pack(side=tk.LEFT, padx=10)

        refresh_btn = tk.Button(
            button_frame,
            text="Refresh",
            font=("Helvetica", 12),
            bg=accent_color,
            fg="white",
            activebackground="#5a6268",
            bd=0,
            padx=15,
            pady=5,
            command=self.load_patient_records
        )
        refresh_btn.pack(side=tk.LEFT, padx=10)

    def load_patient_records(self):
        try:
            cursor = self.db_connection.cursor()
            
            # Clear existing data
            for item in self.patient_records_tree.get_children():
                self.patient_records_tree.delete(item)
            
            # Fetch patient data with photo path
            query = """
                SELECT p.patient_id, p.first_name, p.last_name, p.gender, 
                    p.date_of_birth, p.blood_type, p.phone, p.photo_path
                FROM patients p
                ORDER BY p.last_name, p.first_name
            """
            cursor.execute(query)
            patients = cursor.fetchall()

            # Insert data into treeview
            for patient in patients:
                self.patient_records_tree.insert("", tk.END, values=(
                    patient[0],  # ID
                    f"{patient[1]} {patient[2]}",  # Name
                    patient[3],  # Gender
                    patient[4].strftime('%Y-%m-%d') if patient[4] else '',  # DOB
                    patient[5] if patient[5] else 'N/A',  # Blood Type
                    patient[6] if patient[6] else 'N/A'  # Phone
                ), tags=(patient[7],))  # Store photo path in tags

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load patient records: {e}")

    def view_patient_details(self, event):
        selected_item = self.patient_records_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a patient first")
            return
        
        patient_id = self.patient_records_tree.item(selected_item)["values"][0]
        
        # Create patient details window
        details_window = tk.Toplevel(self.root)
        details_window.title("Patient Details")
        details_window.geometry("900x700")
        details_window.resizable(True, True)
        
        # Modern styling
        bg_color = "#f8f9fa"
        header_color = "#343a40"
        text_color = "#495057"
        accent_color = "#6c757d"
        
        # Main container
        main_frame = tk.Frame(details_window, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=header_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="Patient Details",
            font=("Helvetica", 18, "bold"),
            bg=header_color,
            fg="white",
            padx=10,
            pady=10
        ).pack(side=tk.LEFT)
        
        # Content frame with tabs
        tab_control = ttk.Notebook(main_frame)
        tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Personal Info Tab
        personal_frame = tk.Frame(tab_control, bg=bg_color)
        tab_control.add(personal_frame, text="Personal Information")
        
        # Photo and basic info frame
        photo_frame = tk.Frame(personal_frame, bg=bg_color)
        photo_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Patient photo
        photo_path = self.patient_records_tree.item(selected_item)["tags"][0]
        self.patient_photo_label = tk.Label(photo_frame, bg=bg_color)
        self.patient_photo_label.pack()
        
        if photo_path and os.path.exists(photo_path):
            try:
                img = Image.open(photo_path)
                img = img.resize((200, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.patient_photo_label.config(image=photo)
                self.patient_photo_label.image = photo  # Keep reference
            except Exception as e:
                messagebox.showwarning("Photo Error", f"Could not load patient photo: {e}")
                # Display placeholder
                placeholder = Image.new("RGB", (200, 200), "#e9ecef")
                draw = ImageDraw.Draw(placeholder)
                draw.text((50, 90), "No Photo Available", fill="#6c757d")
                photo = ImageTk.PhotoImage(placeholder)
                self.patient_photo_label.config(image=photo)
                self.patient_photo_label.image = photo
        else:
            # Display placeholder if no photo
            placeholder = Image.new("RGB", (200, 200), "#e9ecef")
            draw = ImageDraw.Draw(placeholder)
            draw.text((50, 90), "No Photo Available", fill="#6c757d")
            photo = ImageTk.PhotoImage(placeholder)
            self.patient_photo_label.config(image=photo)
            self.patient_photo_label.image = photo
        
        # Basic info frame
        info_frame = tk.Frame(personal_frame, bg=bg_color)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        try:
            cursor = self.db_connection.cursor()
            
            # Fetch patient details
            cursor.execute("""
                SELECT p.first_name, p.last_name, p.date_of_birth, p.gender, 
                    p.blood_type, p.phone, p.address, p.photo_path, 
                    u.username, u.user_id
                FROM patients p
                JOIN users u ON p.user_id = u.user_id
                WHERE p.patient_id = %s
            """, (patient_id,))
            patient_data = cursor.fetchone()
            
            if not patient_data:
                messagebox.showerror("Error", "Patient not found")
                details_window.destroy()
                return
            
            # Display patient info
            fields = [
                ("First Name:", patient_data[0]),
                ("Last Name:", patient_data[1]),
                ("Date of Birth:", patient_data[2].strftime('%Y-%m-%d') if patient_data[2] else 'N/A'),
                ("Gender:", patient_data[3]),
                ("Blood Type:", patient_data[4] if patient_data[4] else 'N/A'),
                ("Phone:", patient_data[5] if patient_data[5] else 'N/A'),
                ("Address:", patient_data[6] if patient_data[6] else 'N/A'),
                ("Username:", patient_data[8])
            ]
            
            for i, (label, value) in enumerate(fields):
                tk.Label(
                    info_frame,
                    text=label,
                    font=("Helvetica", 12, "bold"),
                    bg=bg_color,
                    fg=text_color
                ).grid(row=i, column=0, sticky="e", padx=5, pady=5)
                
                tk.Label(
                    info_frame,
                    text=value,
                    font=("Helvetica", 12),
                    bg=bg_color,
                    fg=text_color
                ).grid(row=i, column=1, sticky="w", padx=5, pady=5)
        
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch patient details: {e}")
        
        # Medical Records Tab
        medical_frame = tk.Frame(tab_control, bg=bg_color)
        tab_control.add(medical_frame, text="Medical Records")
        
        # Create scrollable frame for medical records
        med_canvas = tk.Canvas(medical_frame, bg=bg_color)
        med_scrollbar = ttk.Scrollbar(medical_frame, orient="vertical", command=med_canvas.yview)
        med_scrollable_frame = tk.Frame(med_canvas, bg=bg_color)
        
        med_scrollable_frame.bind(
            "<Configure>",
            lambda e: med_canvas.configure(scrollregion=med_canvas.bbox("all"))
        )
        
        med_canvas.create_window((0, 0), window=med_scrollable_frame, anchor="nw")
        med_canvas.configure(yscrollcommand=med_scrollbar.set)
        
        med_scrollbar.pack(side="right", fill="y")
        med_canvas.pack(side="left", fill="both", expand=True)
        
        try:
            # Fetch medical records
            cursor.execute("""
                SELECT mr.record_id, mr.record_date, d.first_name, d.last_name, 
                    mr.diagnosis, mr.treatment, mr.notes, mr.prescription
                FROM medical_records mr
                JOIN doctors d ON mr.doctor_id = d.doctor_id
                WHERE mr.patient_id = %s
                ORDER BY mr.record_date DESC
            """, (patient_id,))
            medical_records = cursor.fetchall()
            
            if medical_records:
                for i, record in enumerate(medical_records):
                    # Record frame
                    record_frame = tk.Frame(
                        med_scrollable_frame,
                        bg="white",
                        bd=2,
                        relief="groove",
                        padx=10,
                        pady=10
                    )
                    record_frame.pack(fill="x", pady=5, padx=5)
                    
                    # Header with doctor and date
                    header_frame = tk.Frame(record_frame, bg="white")
                    header_frame.pack(fill="x")
                    
                    tk.Label(
                        header_frame,
                        text=f"Dr. {record[2]} {record[3]}",
                        font=("Helvetica", 12, "bold"),
                        bg="white"
                    ).pack(side="left")
                    
                    tk.Label(
                        header_frame,
                        text=record[1].strftime('%Y-%m-%d'),
                        font=("Helvetica", 12),
                        bg="white"
                    ).pack(side="right")
                    
                    # Diagnosis
                    tk.Label(
                        record_frame,
                        text="Diagnosis:",
                        font=("Helvetica", 10, "bold"),
                        bg="white"
                    ).pack(anchor="w")
                    
                    tk.Label(
                        record_frame,
                        text=record[4] if record[4] else "Not specified",
                        font=("Helvetica", 10),
                        bg="white",
                        wraplength=600,
                        justify="left"
                    ).pack(anchor="w", fill="x")
                    
                    # Treatment
                    tk.Label(
                        record_frame,
                        text="Treatment:",
                        font=("Helvetica", 10, "bold"),
                        bg="white"
                    ).pack(anchor="w", pady=(5,0))
                    
                    tk.Label(
                        record_frame,
                        text=record[5] if record[5] else "Not specified",
                        font=("Helvetica", 10),
                        bg="white",
                        wraplength=600,
                        justify="left"
                    ).pack(anchor="w", fill="x")
                    
                    # Notes
                    tk.Label(
                        record_frame,
                        text="Notes:",
                        font=("Helvetica", 10, "bold"),
                        bg="white"
                    ).pack(anchor="w", pady=(5,0))
                    
                    tk.Label(
                        record_frame,
                        text=record[6] if record[6] else "None",
                        font=("Helvetica", 10),
                        bg="white",
                        wraplength=600,
                        justify="left"
                    ).pack(anchor="w", fill="x")
                    
                    # Prescription
                    tk.Label(
                        record_frame,
                        text="Prescription:",
                        font=("Helvetica", 10, "bold"),
                        bg="white"
                    ).pack(anchor="w", pady=(5,0))
                    
                    tk.Label(
                        record_frame,
                        text=record[7] if record[7] else "None",
                        font=("Helvetica", 10),
                        bg="white",
                        wraplength=600,
                        justify="left"
                    ).pack(anchor="w", fill="x")
            else:
                tk.Label(
                    med_scrollable_frame,
                    text="No medical records found for this patient",
                    font=("Helvetica", 12),
                    bg=bg_color,
                    fg=text_color
                ).pack(pady=20)
        
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch medical records: {e}")
        
        # Appointments Tab
        appointments_frame = tk.Frame(tab_control, bg=bg_color)
        tab_control.add(appointments_frame, text="Appointments")
        
        # Create treeview for appointments
        columns = ("Date", "Time", "Doctor", "Status", "Reason")
        self.patient_appointments_tree = ttk.Treeview(
            appointments_frame,
            columns=columns,
            show="headings",
            style="Patient.Treeview"
        )
        
        for col in columns:
            self.patient_appointments_tree.heading(col, text=col, anchor=tk.W)
            self.patient_appointments_tree.column(col, width=120, anchor=tk.W, stretch=True)
        
        scrollbar = ttk.Scrollbar(appointments_frame, orient="vertical", command=self.patient_appointments_tree.yview)
        self.patient_appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.patient_appointments_tree.pack(fill="both", expand=True)
        
        try:
            # Fetch patient appointments
            cursor.execute("""
                SELECT a.appointment_date, a.appointment_time, 
                    CONCAT(d.first_name, ' ', d.last_name), a.status, a.reason
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE a.patient_id = %s
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            """, (patient_id,))
            appointments = cursor.fetchall()
            
            for appointment in appointments:
                # Handle time formatting (could be timedelta or string)
                time_str = appointment[1]
                if isinstance(appointment[1], timedelta):
                    total_seconds = int(appointment[1].total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    time_str = f"{hours:02d}:{minutes:02d}"
                
                self.patient_appointments_tree.insert("", tk.END, values=(
                    appointment[0].strftime('%Y-%m-%d'),
                    time_str,
                    appointment[2],
                    appointment[3],
                    appointment[4] if appointment[4] else "N/A"
                ))
        
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch appointments: {e}")
        
        # Button frame at bottom
        button_frame = tk.Frame(main_frame, bg=bg_color)
        button_frame.pack(fill="x", pady=(10, 0))
        
        close_btn = tk.Button(
            button_frame,
            text="Close",
            font=("Helvetica", 12),
            bg=accent_color,
            fg="white",
            command=details_window.destroy
        )
        close_btn.pack(side="right", padx=10)
        
        # Add mousewheel scrolling for medical records
        def _on_mousewheel(event):
            med_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        details_window.bind("<MouseWheel>", _on_mousewheel)
        med_scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

    def filter_patient_records(self, event):
        search_term = self.patient_search_var.get().lower()
        
        for item in self.patient_records_tree.get_children():
            values = self.patient_records_tree.item(item)["values"]
            # Search in ID, Name, and Phone
            if (search_term in str(values[0]).lower() or 
                search_term in str(values[1]).lower() or 
                search_term in str(values[5]).lower()):
                self.patient_records_tree.item(item, tags=('visible',))
            else:
                self.patient_records_tree.item(item, tags=('hidden',))
        
        # Hide non-matching items
        for item in self.patient_records_tree.get_children():
            if 'hidden' in self.patient_records_tree.item(item)["tags"]:
                self.patient_records_tree.detach(item)
            else:
                self.patient_records_tree.reattach(item, '', 'end')

    def show_staff_appointments(self, user_id):
        # Clear content frame
        for widget in self.staff_content_frame.winfo_children():
            widget.destroy()

        # Title with modern styling
        title_frame = tk.Frame(self.staff_content_frame, bg="#f0f8ff")
        title_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            title_frame,
            text="Manage Appointments",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        ).pack(side=tk.LEFT, padx=20)

        # Filter frame with modern styling
        filter_frame = tk.Frame(self.staff_content_frame, bg="#ecf0f1", bd=2, relief=tk.RIDGE)
        filter_frame.pack(fill=tk.X, padx=20, pady=10, ipadx=10, ipady=10)

        # Date range filter
        tk.Label(
            filter_frame,
            text="Date Range:",
            font=("Arial", 11),
            bg="#ecf0f1"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.appt_from_date = DateEntry(
            filter_frame,
            font=("Arial", 11),
            date_pattern='yyyy-mm-dd',
            width=12,
            background='white',
            foreground='black'
        )
        self.appt_from_date.grid(row=0, column=1, padx=5, pady=5)
        self.appt_from_date.set_date(datetime.now().replace(day=1))

        tk.Label(
            filter_frame,
            text="to",
            font=("Arial", 11),
            bg="#ecf0f1"
        ).grid(row=0, column=2, padx=5, pady=5)

        self.appt_to_date = DateEntry(
            filter_frame,
            font=("Arial", 11),
            date_pattern='yyyy-mm-dd',
            width=12,
            background='white',
            foreground='black'
        )
        self.appt_to_date.grid(row=0, column=3, padx=5, pady=5)
        self.appt_to_date.set_date(datetime.now())

        # Status filter
        tk.Label(
            filter_frame,
            text="Status:",
            font=("Arial", 11),
            bg="#ecf0f1"
        ).grid(row=0, column=4, padx=5, pady=5, sticky="e")

        self.appt_status_var = tk.StringVar(value="All")
        status_combobox = ttk.Combobox(
            filter_frame,
            textvariable=self.appt_status_var,
            values=["All", "Scheduled", "Confirmed", "Completed", "Cancelled"],
            font=("Arial", 11),
            state="readonly",
            width=12
        )
        status_combobox.grid(row=0, column=5, padx=5, pady=5)

        # Filter by type (patient/doctor)
        tk.Label(
            filter_frame,
            text="Filter By:",
            font=("Arial", 11),
            bg="#ecf0f1"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.appt_filter_type = tk.StringVar(value="None")
        filter_type_combobox = ttk.Combobox(
            filter_frame,
            textvariable=self.appt_filter_type,
            values=["None", "Patient", "Doctor"],
            font=("Arial", 11),
            state="readonly",
            width=10
        )
        filter_type_combobox.grid(row=1, column=1, padx=5, pady=5)
        filter_type_combobox.bind("<<ComboboxSelected>>", self.update_appt_filter_options)

        # Filter value (dynamic based on type)
        self.appt_filter_value_var = tk.StringVar()
        self.appt_filter_value_combobox = ttk.Combobox(
            filter_frame,
            textvariable=self.appt_filter_value_var,
            font=("Arial", 11),
            state="readonly",
            width=20
        )
        self.appt_filter_value_combobox.grid(row=1, column=2, columnspan=2, padx=5, pady=5)

        # Apply filter button
        filter_btn = tk.Button(
            filter_frame,
            text="Apply Filters",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            command=lambda: self.load_staff_appointments(user_id)
        )
        filter_btn.grid(row=1, column=4, columnspan=2, padx=5, pady=5, sticky="e")

        # Treeview container with scrollbars
        tree_container = tk.Frame(self.staff_content_frame, bg="#f0f8ff")
        tree_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Vertical scrollbar
        y_scrollbar = ttk.Scrollbar(tree_container)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview with modern styling
        style = ttk.Style()
        style.configure("Custom.Treeview", 
                    background="#ffffff",
                    foreground="#2c3e50",
                    rowheight=25,
                    fieldbackground="#ffffff",
                    bordercolor="#bdc3c7",
                    borderwidth=1)
        style.map("Custom.Treeview", 
                background=[('selected', '#3498db')],
                foreground=[('selected', 'white')])
        style.configure("Custom.Treeview.Heading",
                    background="#3498db",
                    foreground="white",
                    padding=5,
                    font=('Arial', 11, 'bold'))

        columns = ("ID", "Date", "Time", "Patient", "Doctor", "Status", "Reason")
        self.staff_appointments_tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )

        # Configure columns
        col_widths = [50, 100, 80, 150, 150, 100, 200]
        for col, width in zip(columns, col_widths):
            self.staff_appointments_tree.heading(col, text=col)
            self.staff_appointments_tree.column(col, width=width, anchor=tk.CENTER)

        self.staff_appointments_tree.pack(fill=tk.BOTH, expand=True)

        # Configure scrollbars
        y_scrollbar.config(command=self.staff_appointments_tree.yview)
        x_scrollbar.config(command=self.staff_appointments_tree.xview)

        # Action buttons frame
        action_frame = tk.Frame(self.staff_content_frame, bg="#f0f8ff")
        action_frame.pack(fill=tk.X, padx=20, pady=10)

        # Add appointment button
        add_btn = tk.Button(
            action_frame,
            text="Add Appointment",
            font=("Arial", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            command=self.show_add_appointment_form
        )
        add_btn.pack(side=tk.LEFT, padx=5)

        # Edit appointment button
        edit_btn = tk.Button(
            action_frame,
            text="Edit Appointment",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            command=self.edit_staff_appointment
        )
        edit_btn.pack(side=tk.LEFT, padx=5)

        # Delete appointment button
        delete_btn = tk.Button(
            action_frame,
            text="Delete Appointment",
            font=("Arial", 11),
            bg="#e74c3c",
            fg="white",
            command=self.delete_staff_appointment
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

        # Status update buttons
        status_frame = tk.Frame(action_frame, bg="#f0f8ff")
        status_frame.pack(side=tk.RIGHT, padx=5)

        complete_btn = tk.Button(
            status_frame,
            text="Mark as Completed",
            font=("Arial", 11),
            bg="#27ae60",
            fg="white",
            command=lambda: self.update_staff_appointment_status(user_id, "Completed")
        )
        complete_btn.pack(side=tk.LEFT, padx=2)

        cancel_btn = tk.Button(
            status_frame,
            text="Cancel Appointment",
            font=("Arial", 11),
            bg="#e67e22",
            fg="white",
            command=lambda: self.update_staff_appointment_status(user_id, "Cancelled")
        )
        cancel_btn.pack(side=tk.LEFT, padx=2)

        # Load initial appointments
        self.load_staff_appointments(user_id)

    def update_appt_filter_options(self, event=None):
        filter_type = self.appt_filter_type.get()
        
        try:
            cursor = self.db_connection.cursor()
            
            if filter_type == "Patient":
                cursor.execute(
                    "SELECT patient_id, CONCAT(first_name, ' ', last_name) FROM patients ORDER BY last_name, first_name"
                )
                options = [f"{name} (ID: {id})" for id, name in cursor.fetchall()]
            elif filter_type == "Doctor":
                cursor.execute(
                    "SELECT doctor_id, CONCAT(first_name, ' ', last_name) FROM doctors ORDER BY last_name, first_name"
                )
                options = [f"{name} (ID: {id})" for id, name in cursor.fetchall()]
            else:
                options = []
                
            self.appt_filter_value_combobox['values'] = options
            if options:
                self.appt_filter_value_combobox.current(0)
            else:
                self.appt_filter_value_var.set("")
                
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load filter options: {e}")

    def load_staff_appointments(self, user_id):
        from_date = self.appt_from_date.get_date()
        to_date = self.appt_to_date.get_date()
        status = self.appt_status_var.get()
        filter_type = self.appt_filter_type.get()
        filter_value = self.appt_filter_value_var.get()

        try:
            cursor = self.db_connection.cursor()
            
            # Base query
            query = """
                SELECT a.appointment_id, a.appointment_date, a.appointment_time,
                    CONCAT(p.first_name, ' ', p.last_name),
                    CONCAT(d.first_name, ' ', d.last_name),
                    a.status, a.reason
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE a.appointment_date BETWEEN %s AND %s
            """
            params = [from_date, to_date]
            
            # Add status filter if not "All"
            if status != "All":
                query += " AND a.status = %s"
                params.append(status)
                
            # Add patient/doctor filter if selected
            if filter_type == "Patient" and filter_value:
                patient_id = filter_value.split("(ID: ")[1].replace(")", "")
                query += " AND a.patient_id = %s"
                params.append(patient_id)
            elif filter_type == "Doctor" and filter_value:
                doctor_id = filter_value.split("(ID: ")[1].replace(")", "")
                query += " AND a.doctor_id = %s"
                params.append(doctor_id)
                
            query += " ORDER BY a.appointment_date, a.appointment_time"
            
            cursor.execute(query, tuple(params))
            appointments = cursor.fetchall()

            # Clear existing data
            for item in self.staff_appointments_tree.get_children():
                self.staff_appointments_tree.delete(item)

            # Insert new data
            for appt in appointments:
                # Format time if it's a timedelta object
                time_str = str(appt[2])
                if isinstance(appt[2], timedelta):
                    hours = appt[2].seconds // 3600
                    minutes = (appt[2].seconds % 3600) // 60
                    time_str = f"{hours:02d}:{minutes:02d}"
                    
                self.staff_appointments_tree.insert("", tk.END, values=(
                    appt[0],  # ID
                    appt[1].strftime("%Y-%m-%d") if appt[1] else "N/A",  # Date
                    time_str,  # Time
                    appt[3],  # Patient
                    appt[4],  # Doctor
                    appt[5],  # Status
                    appt[6] if appt[6] else "N/A"  # Reason
                ))

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load appointments: {e}")

    def edit_staff_appointment(self):
        selected_item = self.staff_appointments_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an appointment to edit")
            return

        appointment_id = self.staff_appointments_tree.item(selected_item)["values"][0]

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT a.appointment_id, a.appointment_date, a.appointment_time,
                        a.patient_id, CONCAT(p.first_name, ' ', p.last_name),
                        a.doctor_id, CONCAT(d.first_name, ' ', d.last_name),
                        a.status, a.reason
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE a.appointment_id = %s""",
                (appointment_id,)
            )
            appointment_data = cursor.fetchone()

            if not appointment_data:
                messagebox.showerror("Error", "Appointment not found")
                return

            # Create edit window
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Appointment")
            edit_window.geometry("600x500")
            edit_window.resizable(False, False)

            # Configure window styling
            edit_window.configure(bg="#f0f8ff")

            # Header frame
            header_frame = tk.Frame(edit_window, bg="#3498db", height=60)
            header_frame.pack(fill=tk.X)
            tk.Label(
                header_frame,
                text="Edit Appointment",
                font=("Arial", 18, "bold"),
                bg="#3498db",
                fg="white"
            ).pack(pady=15)

            # Main form container
            form_frame = tk.Frame(edit_window, bg="#f0f8ff", padx=20, pady=20)
            form_frame.pack(fill=tk.BOTH, expand=True)

            # Date
            tk.Label(
                form_frame,
                text="Date:",
                font=("Arial", 12),
                bg="#f0f8ff"
            ).grid(row=0, column=0, pady=10, sticky="e")
            self.edit_appt_date = DateEntry(
                form_frame,
                font=("Arial", 12),
                date_pattern='yyyy-mm-dd',
                width=12
            )
            self.edit_appt_date.grid(row=0, column=1, pady=10, sticky="w")
            self.edit_appt_date.set_date(appointment_data[1])

            # Time
            tk.Label(
                form_frame,
                text="Time:",
                font=("Arial", 12),
                bg="#f0f8ff"
            ).grid(row=1, column=0, pady=10, sticky="e")
            self.edit_appt_time = ttk.Combobox(
                form_frame,
                font=("Arial", 12),
                values=[f"{h:02d}:{m:02d}" for h in range(8, 18) for m in [0, 30]],
                state="readonly",
                width=10
            )
            self.edit_appt_time.grid(row=1, column=1, pady=10, sticky="w")
            
            # Set current time
            if isinstance(appointment_data[2], timedelta):
                total_seconds = appointment_data[2].total_seconds()
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                current_time = f"{hours:02d}:{minutes:02d}"
            else:
                current_time = appointment_data[2].strftime("%H:%M") if appointment_data[2] else "08:00"
            self.edit_appt_time.set(current_time)

            # Patient (read-only)
            tk.Label(
                form_frame,
                text="Patient:",
                font=("Arial", 12),
                bg="#f0f8ff"
            ).grid(row=2, column=0, pady=10, sticky="e")
            tk.Label(
                form_frame,
                text=appointment_data[4],
                font=("Arial", 12),
                bg="#f0f8ff"
            ).grid(row=2, column=1, pady=10, sticky="w")

            # Doctor
            tk.Label(
                form_frame,
                text="Doctor:",
                font=("Arial", 12),
                bg="#f0f8ff"
            ).grid(row=3, column=0, pady=10, sticky="e")
            
            # Get all doctors for dropdown
            cursor.execute("SELECT doctor_id, CONCAT(first_name, ' ', last_name) FROM doctors ORDER BY last_name, first_name")
            doctors = [f"{name} (ID: {id})" for id, name in cursor.fetchall()]
            
            self.edit_appt_doctor = ttk.Combobox(
                form_frame,
                values=doctors,
                font=("Arial", 12),
                state="readonly",
                width=30
            )
            self.edit_appt_doctor.grid(row=3, column=1, pady=10, sticky="w")
            
            # Set current doctor
            current_doctor = f"{appointment_data[6]} (ID: {appointment_data[5]})"
            self.edit_appt_doctor.set(current_doctor)

            # Status
            tk.Label(
                form_frame,
                text="Status:",
                font=("Arial", 12),
                bg="#f0f8ff"
            ).grid(row=4, column=0, pady=10, sticky="e")
            self.edit_appt_status = ttk.Combobox(
                form_frame,
                values=["Scheduled", "Confirmed", "Completed", "Cancelled"],
                font=("Arial", 12),
                state="readonly",
                width=15
            )
            self.edit_appt_status.grid(row=4, column=1, pady=10, sticky="w")
            self.edit_appt_status.set(appointment_data[7])

            # Reason
            tk.Label(
                form_frame,
                text="Reason:",
                font=("Arial", 12),
                bg="#f0f8ff"
            ).grid(row=5, column=0, pady=10, sticky="ne")
            self.edit_appt_reason = tk.Text(
                form_frame,
                font=("Arial", 12),
                height=5,
                width=40,
                wrap=tk.WORD
            )
            self.edit_appt_reason.grid(row=5, column=1, pady=10, sticky="w")
            self.edit_appt_reason.insert("1.0", appointment_data[8] if appointment_data[8] else "")

            # Button frame
            button_frame = tk.Frame(form_frame, bg="#f0f8ff")
            button_frame.grid(row=6, column=0, columnspan=2, pady=20)

            # Update button
            update_btn = tk.Button(
                button_frame,
                text="Update Appointment",
                font=("Arial", 12, "bold"),
                bg="#3498db",
                fg="white",
                command=lambda: self.update_staff_appointment(appointment_id, edit_window)
            )
            update_btn.pack(side=tk.LEFT, padx=10)

            # Cancel button
            cancel_btn = tk.Button(
                button_frame,
                text="Cancel",
                font=("Arial", 12),
                bg="#e74c3c",
                fg="white",
                command=edit_window.destroy
            )
            cancel_btn.pack(side=tk.LEFT, padx=10)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch appointment data: {e}")

    def update_staff_appointment(self, appointment_id, window):
        date = self.edit_appt_date.get_date()
        time = self.edit_appt_time.get()
        doctor = self.edit_appt_doctor.get()
        status = self.edit_appt_status.get()
        reason = self.edit_appt_reason.get("1.0", "end-1c").strip()

        if not all([date, time, doctor, status]):
            messagebox.showerror("Error", "All fields except reason are required")
            return

        try:
            doctor_id = doctor.split("(ID: ")[1].replace(")", "")
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT CONCAT(p.first_name, ' ', p.last_name), p.email, 
                        CONCAT(d.first_name, ' ', d.last_name), a.patient_id
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE a.appointment_id = %s""",
                (appointment_id,)
            )
            data = cursor.fetchone()
            if not data:
                messagebox.showerror("Error", "Patient or doctor not found")
                return
            patient_name, patient_email, doctor_name, patient_id = data

            cursor.execute(
                """UPDATE appointments 
                SET appointment_date = %s, appointment_time = %s, doctor_id = %s, 
                    status = %s, reason = %s
                WHERE appointment_id = %s""",
                (date, time, doctor_id, status, reason if reason else None, appointment_id)
            )
            self.db_connection.commit()

            subject = "Appointment Updated - Grow Up Hospital"
            body = (
                f"Dear {patient_name},\n\n"
                f"Your appointment has been updated.\n"
                f"Appointment ID: {appointment_id}\n"
                f"Date: {date}\n"
                f"Time: {time}\n"
                f"Doctor: {doctor_name}\n"
                f"Status: {status}\n"
                f"Reason: {reason if reason else 'Not specified'}\n\n"
                f"Thank you for choosing Grow Up Hospital."
            )
            self.send_email_notification(patient_email, subject, body)
            messagebox.showinfo("Success", "Appointment updated successfully!")
            window.destroy()
            self.load_staff_appointments(self.current_user_id)

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to update appointment: {e}")
        finally:
            if cursor:
                cursor.close()
                
    def update_staff_appointment_status(self, user_id, status):
        selected_item = self.staff_appointments_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an appointment")
            return

        appointment_id = self.staff_appointments_tree.item(selected_item)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm", f"Are you sure you want to mark this appointment as {status}?"
        )
        if not confirm:
            return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT CONCAT(p.first_name, ' ', p.last_name), p.email, 
                        CONCAT(d.first_name, ' ', d.last_name), a.appointment_date, 
                        a.appointment_time, a.reason
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN doctors d ON a.doctor_id = d.doctor_id
                WHERE a.appointment_id = %s""",
                (appointment_id,)
            )
            data = cursor.fetchone()
            if not data:
                messagebox.showerror("Error", "Appointment not found")
                return
            patient_name, patient_email, doctor_name, appt_date, appt_time, reason = data

            cursor.execute(
                "UPDATE appointments SET status = %s WHERE appointment_id = %s",
                (status, appointment_id)
            )
            self.db_connection.commit()

            subject = f"Appointment {status} - Grow Up Hospital"
            body = (
                f"Dear {patient_name},\n\n"
                f"Your appointment (ID: {appointment_id}) has been marked as {status}.\n"
                f"Date: {appt_date}\n"
                f"Time: {appt_time}\n"
                f"Doctor: {doctor_name}\n"
                f"Reason: {reason if reason else 'Not specified'}\n\n"
                f"Thank you for choosing Grow Up Hospital."
            )
            self.send_email_notification(patient_email, subject, body)
            messagebox.showinfo("Success", f"Appointment marked as {status}")
            self.load_staff_appointments(user_id)

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to update appointment: {e}")
        finally:
            if cursor:
                cursor.close()

    def delete_staff_appointment(self):
        selected_item = self.staff_appointments_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an appointment to delete")
            return

        appointment_id = self.staff_appointments_tree.item(selected_item)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm", "Are you sure you want to delete this appointment?"
        )
        if not confirm:
            return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "DELETE FROM appointments WHERE appointment_id = %s",
                (appointment_id,)
            )
            self.db_connection.commit()

            messagebox.showinfo("Success", "Appointment deleted successfully!")
            self.load_staff_appointments(self.current_user_id)

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to delete appointment: {e}")
            
    def admin_create_appointment(self):
        # Ensure all variables are accessible
        patient_str = getattr(self, 'patient_var', None).get() if hasattr(self, 'patient_var') else None
        doctor_str = getattr(self, 'doctor_var', None).get() if hasattr(self, 'doctor_var') else None
        date = getattr(self, 'date_var', None).get() if hasattr(self, 'date_var') else None
        time = getattr(self, 'time_var', None).get() if hasattr(self, 'time_var') else None
        status = getattr(self, 'status_var', None).get() if hasattr(self, 'status_var') else None
        reason = getattr(self, 'reason_text', None).get("1.0", tk.END).strip() if hasattr(self, 'reason_text') else None

        if not all([patient_str, doctor_str, date, time, status]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            patient_id = int(patient_str.split("(ID: ")[1].split(")")[0])
            doctor_id = int(doctor_str.split("(ID: ")[1].split(")")[0])
            datetime.strptime(date, "%Y-%m-%d")

            cursor = None
            try:
                if self.db_connection.in_transaction:
                    self.db_connection.rollback()
                self.db_connection.start_transaction()
                cursor = self.db_connection.cursor()

                cursor.execute(
                    """INSERT INTO appointments 
                    (patient_id, doctor_id, appointment_date, appointment_time, status, reason) 
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (patient_id, doctor_id, date, time, status, reason if reason else None)
                )
                appointment_id = cursor.lastrowid

                # Verify and fetch patient and doctor details
                cursor.execute(
                    """SELECT CONCAT(p.first_name, ' ', p.last_name), p.email, 
                            CONCAT(d.first_name, ' ', d.last_name)
                    FROM patients p
                    JOIN doctors d ON d.doctor_id = %s
                    WHERE p.patient_id = %s""",
                    (doctor_id, patient_id)
                )
                data = cursor.fetchone()
                if not data:
                    raise ValueError("Patient or doctor not found in database")
                patient_name, patient_email, doctor_name = data

                self.db_connection.commit()

                # Send email notification
                subject = "New Appointment Scheduled - Grow Up Hospital"
                body = (
                    f"Dear {patient_name},\n\n"
                    f"A new appointment has been scheduled for you.\n"
                    f"Appointment ID: {appointment_id}\n"
                    f"Date: {date}\n"
                    f"Time: {time}\n"
                    f"Doctor: {doctor_name}\n"
                    f"Status: {status}\n"
                    f"Reason: {reason if reason else 'Not specified'}\n\n"
                    f"Thank you for choosing Grow Up Hospital."
                )
                self.send_email_notification(patient_email, subject, body)
                messagebox.showinfo("Success", "Appointment created successfully!")

                # Close the add appointment window (assuming it's the topmost window)
                if hasattr(self, 'add_appt_window') and self.add_appt_window.winfo_exists():
                    self.add_appt_window.destroy()
                self.load_staff_appointments(self.current_user_id)

            except Error as e:
                self.db_connection.rollback()
                self.logger.error(f"Database error in admin_create_appointment: {e}")
                messagebox.showerror("Database Error", f"Failed to create appointment: {e}")
            finally:
                if cursor:
                    cursor.close()

        except ValueError as e:
            self.logger.error(f"Value error in admin_create_appointment: {e}")
            messagebox.showerror("Error", f"Invalid input or {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error in admin_create_appointment: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def show_manage_patients(self):
        # Clear content frame
        for widget in self.admin_content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.admin_content_frame,
            text="Manage Patients",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=10)

        # Add patient button
        add_btn = tk.Button(
            self.admin_content_frame,
            text="Add New Patient",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=self.show_patient_registration,
        )
        add_btn.pack(pady=10)

        # Patients table
        columns = ("ID", "Name", "Gender", "Age", "Blood Type", "Phone")
        self.patients_tree = ttk.Treeview(
            self.admin_content_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.patients_tree.heading(col, text=col)
            self.patients_tree.column(col, width=120, anchor=tk.CENTER)

        self.patients_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Load patients data
        self.load_patients_data()

        # Action buttons frame
        action_frame = tk.Frame(self.admin_content_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)

        edit_btn = tk.Button(
            action_frame,
            text="Edit Patient",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=self.edit_patient,
        )
        edit_btn.grid(row=0, column=0, padx=10)

        delete_btn = tk.Button(
            action_frame,
            text="Delete Patient",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=self.delete_patient,
        )
        delete_btn.grid(row=0, column=1, padx=10)

    def load_patients_data(self):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT p.patient_id, CONCAT(p.first_name, ' ', p.last_name), 
                       p.gender, TIMESTAMPDIFF(YEAR, p.date_of_birth, CURDATE()), 
                       p.blood_type, p.phone
                FROM patients p
                ORDER BY p.last_name, p.first_name
            """
            cursor.execute(query)
            patients = cursor.fetchall()

            # Clear existing data
            for item in self.patients_tree.get_children():
                self.patients_tree.delete(item)

            # Insert new data
            for patient in patients:
                self.patients_tree.insert("", tk.END, values=patient)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load patients data: {e}")
            
    def edit_patient(self):
        selected_item = self.patients_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a patient to edit")
            return

        patient_id = self.patients_tree.item(selected_item)["values"][0]

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT p.patient_id, p.first_name, p.last_name, p.date_of_birth, 
                       p.gender, p.blood_type, p.phone, p.address, u.username
                FROM patients p
                JOIN users u ON p.user_id = u.user_id
                WHERE p.patient_id = %s""",
                (patient_id,)
            )
            patient_data = cursor.fetchone()

            if not patient_data:
                messagebox.showerror("Error", "Patient not found")
                return

            # Create edit window
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Patient")
            edit_window.geometry("600x700")

            tk.Label(edit_window, text="Edit Patient", font=("Arial", 18, "bold")).pack(pady=10)

            # Form fields
            fields = [
                ("First Name:", patient_data[1]),
                ("Last Name:", patient_data[2]),
                ("Date of Birth (YYYY-MM-DD):", patient_data[3]),
                ("Gender:", patient_data[4]),
                ("Blood Type:", patient_data[5]),
                ("Phone:", patient_data[6]),
                ("Address:", patient_data[7]),
                ("Username:", patient_data[8]),
            ]

            self.edit_patient_entries = {}

            for i, (label, value) in enumerate(fields):
                tk.Label(edit_window, text=label, font=("Arial", 12)).pack(pady=5)

                if label == "Gender:":
                    entry = ttk.Combobox(edit_window, values=["Male", "Female", "Other"], font=("Arial", 12))
                    entry.set(value)
                elif label == "Blood Type:":
                    entry = ttk.Combobox(
                        edit_window,
                        values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                        font=("Arial", 12)
                    )
                    entry.set(value)
                elif label == "Address:":
                    entry = tk.Text(edit_window, font=("Arial", 12), height=4, width=40)
                    entry.insert("1.0", value)
                else:
                    entry = tk.Entry(edit_window, font=("Arial", 12))
                    entry.insert(0, value)

                entry.pack(pady=5, ipadx=20)
                self.edit_patient_entries[label.split(":")[0].lower().replace(" ", "_")] = entry

            # Password fields (optional)
            tk.Label(edit_window, text="New Password (leave blank to keep current):", font=("Arial", 12)).pack(pady=5)
            self.edit_patient_password = tk.Entry(edit_window, font=("Arial", 12), show="*")
            self.edit_patient_password.pack(pady=5, ipadx=20)

            tk.Label(edit_window, text="Confirm New Password:", font=("Arial", 12)).pack(pady=5)
            self.edit_patient_confirm_password = tk.Entry(edit_window, font=("Arial", 12), show="*")
            self.edit_patient_confirm_password.pack(pady=5, ipadx=20)

            # Submit button
            submit_btn = tk.Button(
                edit_window,
                text="Update Patient",
                font=("Arial", 12, "bold"),
                bg="#4CAF50",
                fg="white",
                command=lambda: self.update_patient(patient_id, edit_window),
            )
            submit_btn.pack(pady=20)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch patient data: {e}")

    def update_patient(self, patient_id, window):
        # Get all form data
        first_name = self.edit_patient_entries["first_name"].get()
        last_name = self.edit_patient_entries["last_name"].get()
        date_of_birth = self.edit_patient_entries["date_of_birth"].get()
        gender = self.edit_patient_entries["gender"].get()
        blood_type = self.edit_patient_entries["blood_type"].get()
        phone = self.edit_patient_entries["phone"].get()
        address = self.edit_patient_entries["address"].get("1.0", tk.END).strip()
        username = self.edit_patient_entries["username"].get()
        password = self.edit_patient_password.get()
        confirm_password = self.edit_patient_confirm_password.get()

        # Validate inputs
        if not all([first_name, last_name, date_of_birth, gender, phone, address, username]):
            messagebox.showerror("Error", "All fields except blood type are required")
            return

        if password and password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            datetime.strptime(date_of_birth, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Get user_id for this patient
            cursor.execute("SELECT user_id FROM patients WHERE patient_id = %s", (patient_id,))
            user_id = cursor.fetchone()[0]

            # Check if username exists (excluding current patient)
            cursor.execute(
                "SELECT username FROM users WHERE username = %s AND user_id != %s",
                (username, user_id)
            )
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return

            # Update patients table
            cursor.execute(
                """UPDATE patients 
                SET first_name = %s, last_name = %s, date_of_birth = %s, 
                    gender = %s, blood_type = %s, phone = %s, address = %s
                WHERE patient_id = %s""",
                (first_name, last_name, date_of_birth, gender, 
                blood_type if blood_type else None, phone, address, patient_id)
            )

            # Update users table
            if password:
                hashed_password = self.hash_password(password)
                cursor.execute(
                    "UPDATE users SET username = %s, password = %s WHERE user_id = %s",
                    (username, hashed_password, user_id)
                )
            else:
                cursor.execute(
                    "UPDATE users SET username = %s WHERE user_id = %s",
                    (username, user_id)
                )

            self.db_connection.commit()
            messagebox.showinfo("Success", "Patient updated successfully!")
            window.destroy()
            self.load_patients_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to update patient: {e}")
        finally:
            if cursor:
                cursor.close()

    def delete_patient(self):
        selected_item = self.patients_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a patient to delete")
            return

        patient_id = self.patients_tree.item(selected_item)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm", "Are you sure you want to delete this patient? This will also delete all their medical records and appointments."
        )
        if not confirm:
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Get user_id for this patient
            cursor.execute("SELECT user_id FROM patients WHERE patient_id = %s", (patient_id,))
            user_id = cursor.fetchone()[0]

            # Delete from patients table
            cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))

            # Delete from users table
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

            # Note: Related records (appointments, medical records) should be deleted 
            # automatically if foreign key constraints with ON DELETE CASCADE are set up

            self.db_connection.commit()
            messagebox.showinfo("Success", "Patient deleted successfully!")
            self.load_patients_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to delete patient: {e}")
        finally:
            if cursor:
                cursor.close()
            
    def load_staff_data(self):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT s.staff_id, CONCAT(s.first_name, ' ', s.last_name), s.role, s.phone, s.email
                FROM staff s
                JOIN users u ON s.user_id = u.user_id
            """
            cursor.execute(query)
            staff_members = cursor.fetchall()

            # Clear existing data
            for item in self.staff_tree.get_children():
                self.staff_tree.delete(item)

            # Insert new data
            for staff in staff_members:
                self.staff_tree.insert("", tk.END, values=staff)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load staff data: {e}")

    def show_add_staff_form(self):
        # Create a new top-level window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Staff Member")
        add_window.geometry("500x600")

        tk.Label(add_window, text="Add New Staff Member", font=("Arial", 18, "bold")).pack(pady=10)

        # Form fields
        fields = [
            ("First Name:", "entry"),
            ("Last Name:", "entry"),
            ("Role:", "entry"),
            ("Phone:", "entry"),
            ("Email:", "entry"),
            ("Username:", "entry"),
            ("Password:", "entry", True),
            ("Confirm Password:", "entry", True),
        ]

        self.staff_form_entries = {}

        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(add_window, text=label, font=("Arial", 12)).pack(pady=5)

            if field_type == "entry":
                show = "*" if options and options[0] else ""
                entry = tk.Entry(add_window, font=("Arial", 12), show=show)
                entry.pack(pady=5, ipadx=20)
                self.staff_form_entries[
                    label.split(":")[0].lower().replace(" ", "_")
                ] = entry

        # Submit button
        submit_btn = tk.Button(
            add_window,
            text="Add Staff Member",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.add_staff(add_window),
        )
        submit_btn.pack(pady=20)

    def add_staff(self, window):
        # Get all form data
        first_name = self.staff_form_entries["first_name"].get()
        last_name = self.staff_form_entries["last_name"].get()
        role = self.staff_form_entries["role"].get()
        phone = self.staff_form_entries["phone"].get()
        email = self.staff_form_entries["email"].get()
        username = self.staff_form_entries["username"].get()
        password = self.staff_form_entries["password"].get()
        confirm_password = self.staff_form_entries["confirm_password"].get()

        # Validate inputs
        if not all([first_name, last_name, role, username, password, confirm_password]):
            messagebox.showerror("Error", "All fields except phone and email are required")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        cursor = None
        try:
            if self.db_connection.in_transaction:
                self.db_connection.rollback()
            
            self.db_connection.start_transaction()
            cursor = self.db_connection.cursor()
            
            # Check if username exists
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
                return

            # Insert user
            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)",
                (username, hashed_password, "staff"),
            )
            user_id = cursor.lastrowid

            # Insert staff
            cursor.execute(
                """INSERT INTO staff 
                (user_id, first_name, last_name, role, phone, email) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (user_id, first_name, last_name, role, phone, email),
            )

            self.db_connection.commit()
            messagebox.showinfo("Success", "Staff member added successfully!")
            window.destroy()
            self.load_staff_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to add staff member: {e}")
        finally:
            if cursor:
                cursor.close()
       

    def edit_staff(self):
        selected_item = self.staff_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a staff member to edit")
            return

        staff_id = self.staff_tree.item(selected_item)["values"][0]

        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT s.staff_id, s.first_name, s.last_name, s.role, s.phone, s.email, u.username
                FROM staff s
                JOIN users u ON s.user_id = u.user_id
                WHERE s.staff_id = %s
            """
            cursor.execute(query, (staff_id,))
            staff_data = cursor.fetchone()

            if not staff_data:
                messagebox.showerror("Error", "Staff member not found")
                return

            # Create edit window
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Staff Member")
            edit_window.geometry("500x500")

            tk.Label(edit_window, text="Edit Staff Member", font=("Arial", 18, "bold")).pack(pady=10)

            # Form fields
            fields = [
                ("First Name:", staff_data[1]),
                ("Last Name:", staff_data[2]),
                ("Role:", staff_data[3]),
                ("Phone:", staff_data[4]),
                ("Email:", staff_data[5]),
                ("Username:", staff_data[6]),
            ]

            self.edit_staff_entries = {}

            for i, (label, value) in enumerate(fields):
                tk.Label(edit_window, text=label, font=("Arial", 12)).pack(pady=5)

                entry = tk.Entry(edit_window, font=("Arial", 12))
                entry.insert(0, value)
                entry.pack(pady=5, ipadx=20)

                self.edit_staff_entries[
                    label.split(":")[0].lower().replace(" ", "_")
                ] = entry

            # Password fields (optional)
            tk.Label(edit_window, text="New Password (leave blank to keep current):", font=("Arial", 12)).pack(pady=5)
            self.edit_staff_password = tk.Entry(edit_window, font=("Arial", 12), show="*")
            self.edit_staff_password.pack(pady=5, ipadx=20)

            tk.Label(edit_window, text="Confirm New Password:", font=("Arial", 12)).pack(pady=5)
            self.edit_staff_confirm_password = tk.Entry(edit_window, font=("Arial", 12), show="*")
            self.edit_staff_confirm_password.pack(pady=5, ipadx=20)

            # Submit button
            submit_btn = tk.Button(
                edit_window,
                text="Update Staff",
                font=("Arial", 12, "bold"),
                bg="#4CAF50",
                fg="white",
                command=lambda: self.update_staff(staff_id, edit_window),
            )
            submit_btn.pack(pady=20)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch staff data: {e}")

    def update_staff(self, staff_id, window):
        # Get all form data
        first_name = self.edit_staff_entries["first_name"].get()
        last_name = self.edit_staff_entries["last_name"].get()
        role = self.edit_staff_entries["role"].get()
        phone = self.edit_staff_entries["phone"].get()
        email = self.edit_staff_entries["email"].get()
        username = self.edit_staff_entries["username"].get()
        password = self.edit_staff_password.get()
        confirm_password = self.edit_staff_confirm_password.get()

        # Validate inputs
        if not all([first_name, last_name, role, username]):
            messagebox.showerror("Error", "First Name, Last Name, Role, and Username are required")
            return

        if password and password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            # Start transaction
            self.db_connection.start_transaction()

            cursor = self.db_connection.cursor()

            # Get user_id for this staff member
            cursor.execute("SELECT user_id FROM staff WHERE staff_id = %s", (staff_id,))
            user_id = cursor.fetchone()[0]

            # Update staff table
            cursor.execute(
                """UPDATE staff 
                SET first_name = %s, last_name = %s, role = %s, phone = %s, email = %s
                WHERE staff_id = %s""",
                (first_name, last_name, role, phone, email, staff_id),
            )

            # Update users table
            if password:
                hashed_password = self.hash_password(password)
                cursor.execute(
                    "UPDATE users SET username = %s, password = %s WHERE user_id = %s",
                    (username, hashed_password, user_id)
                )
            else:
                cursor.execute(
                    "UPDATE users SET username = %s WHERE user_id = %s",
                    (username, user_id)
                )

            # Commit transaction
            self.db_connection.commit()

            messagebox.showinfo("Success", "Staff member updated successfully!")
            window.destroy()
            self.load_staff_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to update staff member: {e}")

    def delete_staff(self):
        selected_item = self.staff_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a staff member to delete")
            return

        staff_id = self.staff_tree.item(selected_item)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm", "Are you sure you want to delete this staff member?"
        )
        if not confirm:
            return

        try:
            # Start transaction
            self.db_connection.start_transaction()

            cursor = self.db_connection.cursor()

            # Get user_id for this staff member
            cursor.execute("SELECT user_id FROM staff WHERE staff_id = %s", (staff_id,))
            user_id = cursor.fetchone()[0]

            # Delete from staff table
            cursor.execute("DELETE FROM staff WHERE staff_id = %s", (staff_id,))

            # Delete from users table
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

            # Commit transaction
            self.db_connection.commit()

            messagebox.showinfo("Success", "Staff member deleted successfully!")
            self.load_staff_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to delete staff member: {e}")
            
    def show_staff_billing(self, user_id):
        # Clear content frame - use staff_content_frame instead of admin_content_frame
        for widget in self.staff_content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.staff_content_frame,
            text="Billing Management",
            font=("Arial", 20, "bold"),
            bg="#f0f8ff",
        ).pack(pady=10)

        # Add bill button
        add_btn = tk.Button(
            self.staff_content_frame,
            text="Add New Bill",
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.show_add_bill_form(user_id),
        )
        add_btn.pack(pady=10)

        # Billing table
        columns = ("Bill ID", "Patient", "Amount", "Date", "Status", "Description")
        self.billing_tree = ttk.Treeview(
            self.staff_content_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.billing_tree.heading(col, text=col)
            self.billing_tree.column(col, width=120, anchor=tk.CENTER)

        self.billing_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Load billing data
        self.load_billing_data()

        # Action buttons frame
        action_frame = tk.Frame(self.staff_content_frame, bg="#f0f8ff")
        action_frame.pack(pady=10)

        mark_paid_btn = tk.Button(
            action_frame,
            text="Mark as Paid",
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            command=lambda: self.update_bill_status("Paid"),
        )
        mark_paid_btn.grid(row=0, column=0, padx=10)

        view_btn = tk.Button(
            action_frame,
            text="View Bill",
            font=("Arial", 12),
            bg="#FFC107",
            fg="white",
            command=self.view_bill_details,
        )
        view_btn.grid(row=0, column=1, padx=10)

        delete_btn = tk.Button(
            action_frame,
            text="Delete Bill",
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            command=self.delete_bill,
        )
        delete_btn.grid(row=0, column=2, padx=10)
    
    def load_billing_data(self):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT b.bill_id, 
                    CONCAT(p.first_name, ' ', p.last_name),
                    b.amount, 
                    b.bill_date, 
                    b.payment_status,
                    b.description
                FROM billing b
                JOIN patients p ON b.patient_id = p.patient_id
                ORDER BY b.bill_date DESC
            """
            cursor.execute(query)
            bills = cursor.fetchall()

            # Clear existing data
            for item in self.billing_tree.get_children():
                self.billing_tree.delete(item)

            # Insert new data
            for bill in bills:
                self.billing_tree.insert("", tk.END, values=bill)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load billing data: {e}")

    def show_add_bill_form(self, user_id):
        # Create a new top-level window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Bill")
        add_window.geometry("500x500")

        tk.Label(add_window, text="Add New Bill", font=("Arial", 18, "bold")).pack(pady=10)

        # Form fields
        fields = [
            ("Patient:", "combobox", []),
            ("Amount:", "entry"),
            ("Description:", "text"),
        ]

        self.bill_form_entries = {}

        # Load patients for combobox
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT patient_id, CONCAT(first_name, ' ', last_name) FROM patients")
            patients = [f"{name} (ID: {id})" for id, name in cursor.fetchall()]
            fields[0] = ("Patient:", "combobox", patients)
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load patients: {e}")

        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(add_window, text=label, font=("Arial", 12)).pack(pady=5)

            if field_type == "entry":
                entry = tk.Entry(add_window, font=("Arial", 12))
                entry.pack(pady=5, ipadx=20)
                self.bill_form_entries[label.lower().replace(":", "")] = entry

            elif field_type == "combobox":
                entry = ttk.Combobox(
                    add_window,
                    values=options[0],
                    font=("Arial", 12),
                    state="readonly"
                )
                entry.pack(pady=5, ipadx=20)
                self.bill_form_entries[label.lower().replace(":", "")] = entry
                if options[0]:  # If there are patients
                    entry.current(0)

            elif field_type == "text":
                text = tk.Text(add_window, font=("Arial", 12), height=5, width=40)
                text.pack(pady=5)
                self.bill_form_entries[label.lower().replace(":", "")] = text

        # Submit button
        submit_btn = tk.Button(
            add_window,
            text="Add Bill",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=lambda: self.add_bill(user_id, add_window),
        )
        submit_btn.pack(pady=20)

    def add_bill(self, user_id, window):
        # Get form data
        patient = self.bill_form_entries["patient"].get()
        amount = self.bill_form_entries["amount"].get()
        description = self.bill_form_entries["description"].get("1.0", tk.END).strip()

        # Validate inputs
        if not all([patient, amount, description]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            # Extract patient ID
            patient_id = int(patient.split("(ID: ")[1].replace(")", ""))

            # Validate amount
            amount_float = float(amount)
            if amount_float <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return

            # Insert bill
            cursor = self.db_connection.cursor()
            cursor.execute(
                """INSERT INTO billing 
                (patient_id, amount, bill_date, payment_status, description) 
                VALUES (%s, %s, %s, %s, %s)""",
                (patient_id, amount_float, datetime.now().date(), "Pending", description),
            )
            self.db_connection.commit()

            messagebox.showinfo("Success", "Bill added successfully!")
            window.destroy()
            self.load_billing_data()

        except ValueError:
            messagebox.showerror("Error", "Invalid amount format")
        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to add bill: {e}")

    def update_bill_status(self, status):
        selected_item = self.billing_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a bill")
            return

        bill_id = self.billing_tree.item(selected_item)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm", f"Are you sure you want to mark this bill as {status}?"
        )
        if not confirm:
            return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "UPDATE billing SET payment_status = %s WHERE bill_id = %s",
                (status, bill_id)
            )
            self.db_connection.commit()

            messagebox.showinfo("Success", f"Bill marked as {status}")
            self.load_billing_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to update bill: {e}")

    def view_bill_details(self):
        selected_item = self.billing_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a bill")
            return

        bill_id = self.billing_tree.item(selected_item)["values"][0]

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """SELECT b.bill_id, 
                        CONCAT(p.first_name, ' ', p.last_name),
                        b.amount, 
                        b.bill_date, 
                        b.payment_status,
                        b.description
                FROM billing b
                JOIN patients p ON b.patient_id = p.patient_id
                WHERE b.bill_id = %s""",
                (bill_id,)
            )
            bill_data = cursor.fetchone()

            if not bill_data:
                messagebox.showerror("Error", "Bill not found")
                return

            # Create details window
            detail_window = tk.Toplevel(self.root)
            detail_window.title(f"Bill Details - ID: {bill_id}")
            detail_window.geometry("500x400")

            # Display bill information
            tk.Label(detail_window, text="Bill Details", font=("Arial", 16, "bold")).pack(pady=10)

            details = [
                ("Bill ID:", bill_data[0]),
                ("Patient:", bill_data[1]),
                ("Amount:", f"${bill_data[2]:.2f}"),
                ("Date:", bill_data[3].strftime("%Y-%m-%d")),
                ("Status:", bill_data[4]),
                ("Description:", bill_data[5]),
            ]

            for label, value in details:
                frame = tk.Frame(detail_window)
                frame.pack(fill=tk.X, padx=20, pady=5)
                
                tk.Label(frame, text=label, font=("Arial", 12, "bold"), width=12, anchor="w").pack(side=tk.LEFT)
                tk.Label(frame, text=value, font=("Arial", 12)).pack(side=tk.LEFT)

        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch bill details: {e}")

    def delete_bill(self):
        selected_item = self.billing_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a bill")
            return

        bill_id = self.billing_tree.item(selected_item)["values"][0]

        confirm = messagebox.askyesno(
            "Confirm", "Are you sure you want to delete this bill?"
        )
        if not confirm:
            return

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "DELETE FROM billing WHERE bill_id = %s",
                (bill_id,)
            )
            self.db_connection.commit()

            messagebox.showinfo("Success", "Bill deleted successfully!")
            self.load_billing_data()

        except Error as e:
            self.db_connection.rollback()
            messagebox.showerror("Database Error", f"Failed to delete bill: {e}")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementSystem(root)
    root.mainloop()