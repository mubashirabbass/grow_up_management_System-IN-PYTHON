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