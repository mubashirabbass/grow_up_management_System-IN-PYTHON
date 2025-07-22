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