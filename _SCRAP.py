import npyscreen
import sqlite3

DB_FILE = 'eyeglass_store.db'

class PatientForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.TitleText, name="First Name:", )
        self.add(npyscreen.TitleText, name="Last Name:")
        self.add(npyscreen.TitleText, name="Email:")
        self.add(npyscreen.TitleFixedText, name="DOB:", value="MM/DD/YYYY")
        self.dob = self.add(npyscreen.TitleText, name="MM/DD/YYYY")
        self.add(npyscreen.TitleText, name="Phone Number:")
        self.add(npyscreen.TitleText, name="Street Address:")
        self.add(npyscreen.TitleText, name="City:")
        self.add(npyscreen.TitleText, name="State:")
        self.add(npyscreen.TitleText, name="Zip:")
        self.add(npyscreen.ButtonPress, name='Create Patient', when_pressed_function=self.create_patient_record, rely=20, relx=30)
        self.add(npyscreen.ButtonPress, name='Cancel', when_pressed_function=self.parentApp.switchFormPrevious, rely=20, relx=50)

    def on_ok(self):
        dob = self.dob.value
        if len(dob) != 8 or not dob.isdigit():
            npyscreen.notify_confirm("Please enter DOB in MMDDYYYY format", title="Invalid DOB")
        else:
            formatted_dob = f"{dob[:2]}/{dob[2:4]}/{dob[4:]}"
            npyscreen.notify_confirm(f"DOB: {formatted_dob}", title="Success")

    def create_patient_record(self):
        first_name = self.get_widget('First Name:').value
        last_name = self.get_widget('Last Name:').value
        email = self.get_widget('Email:').value
        phone = self.get_widget('Phone:').value
        address1 = self.get_widget('Address 1:').value
        address2 = self.get_widget('Address 2:').value
        city = self.get_widget('City:').value
        state = self.get_widget('State:').value
        zipcode = self.get_widget('Zipcode:').value

        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO patients (first_name, last_name, email, phone, address1, address2, city, state, zipcode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (first_name, last_name, email, phone, address1, address2, city, state, zipcode))
        connection.commit()
        connection.close()
        self.parentApp.switchFormPrevious()

    def exit_application(self):
        self.parentApp.switchForm(None)

class EyeglassStoreApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', PatientForm, name='New Patient Form')

if __name__ == '__main__':
    app = EyeglassStoreApp()
    app.run()
