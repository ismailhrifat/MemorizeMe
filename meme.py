from tkinter import *
from tkinter import font, messagebox, filedialog
import json
import random
from google.cloud import storage
import socket
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import webbrowser

main = Tk()
main.title('MemorizeMe')
main.geometry('600x400')
main.resizable(False, False)
icon = PhotoImage(file='icon.png')
main.iconphoto(False, icon)

font_main = font.Font(size=12, weight='bold', family='Ubuntu')
font_body = font.Font(size=14, family='MS Serif')
button_style = {
    "bg": "#007bff",      
    "fg": "white",         
    "font": ("Arial", 14), 
    "width": 15   
}
button_style_small = {
    "bg": "#007bff", 
    "fg": "white",         
    "font": ("Arial", 9),
    "width": 13           
}
button_style_signup = {
    "bg": "#007bff",       
    "fg": "white",         
    "font": ("Arial", 9), 
    "width": 27            
}
def save_file():
    font_path = "font.ttf" 
    font_name = "MyCustomFont"
    pdfmetrics.registerFont(TTFont(font_name, font_path))
    data = []
    data.append(["Question", "Answer"])
    with open("data.json", "r") as file:
        my_data = json.load(file)
    data_keys = list(my_data.keys())
    for i in range(len(data_keys)):
        data_rows = [data_keys[i], my_data[data_keys[i]]]
        data.append(data_rows)
    pdf_buffer = io.BytesIO()
    document = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    table_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), font_name),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("FONTNAME", (0, 1), (-1, -1), font_name),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
    ])
    table_data = [data[0]]
    table_data.extend(data[1:])
    table = Table(table_data)
    table.setStyle(table_style)

    document.build([table])

    try:
        save_path = filedialog.asksaveasfilename(
            initialfile="my_data.pdf",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        with open(save_path, "wb") as file:
            file.write(pdf_buffer.getvalue())
    except PermissionError:
        messagebox.showerror("Fill In Use", "The action can't be completed because file is open in System")

def start_uploading():
    try:
        socket.create_connection(("www.google.com", 80))
        global loading_label
        loading_label = Label(main, text="Uploading...")
        loading_label.place(x=260,y=170)
        main.after(10, upload_data)
    except OSError:
        messagebox.showerror("Error!", "Device is not connected to internet.")

def upload_data():
    client = storage.Client.from_service_account_json("keyfile.json")
    bucket = client.get_bucket("memorizeme")

    with open("user_registered.json", "r") as file:
        user_registered_data = json.load(file)

    email_id = list(user_registered_data.keys())[0]
    path = "userdata/" + email_id + ".json"
    blob_data = bucket.blob(path)
    blob_data.upload_from_filename("data.json")
    loading_label.place_forget()
    messagebox.showinfo("Succesfull!", "Data Uploaded!")

def destroying():
    try:
        to_destroy = [full_name_label,full_name_entry, email_label, email_entry, signup_button]
        for widgets in to_destroy:
            widgets.destroy()
    except NameError:
        pass
    try:
        to_remove = [question_get, question_print, show_answer_button]
        for widget in to_remove:
            widget.destroy()
    except NameError:
        pass
    try:
        to_delete = [answer_get, answer_print, one_more_button]
        for widget in to_delete:
            widget.destroy()
    except NameError:
        pass
    try:
        to_destroy = [question, answer, question_entry, answer_entry, submit_add_data]
        for widget in to_destroy:
            widget.destroy()
    except NameError:
        pass
    try:
        done_label.destroy()
    except NameError:
        pass

def main_body():
    def data_added():
        global done_label
        question = question_entry.get("1.0", "end-1c")
        answer = answer_entry.get("1.0", "end-1c")
        if question != "" and answer != "":
            new_data = {question : answer}
            with open("data.json", "r") as file:
                file_data = json.load(file)
            file_data.update(new_data)

            with open("data.json", "w") as file:
                json.dump(file_data, file)

            question_entry.delete("1.0", "end")
            answer_entry.delete("1.0", "end")
            done_label = Label(main, text="Data Added! You can add more.", font=font_main, fg="#007bff")
            done_label.place(x=160, y=300)
        else:
            messagebox.showwarning("Warning!", "Question or Answer is missing.")
    def add_data():
        destroying()
        global question, answer, question_entry,  answer_entry, submit_add_data
        question = Label(main, text="Question", font=font_main)
        question.place(x=10, y=70)
        question_entry = Text(main, wrap="word")
        question_entry.place(x=10, y=100, height=45, width=550)
        answer = Label(main, text="Answer", font=font_main)
        answer.place(x=10, y=160)
        answer_entry = Text(main, wrap="word")
        answer_entry.place(x=10, y=190, height=25, width=550)
        submit_add_data = Button(main, text="Submit", command=data_added, **button_style_small)
        submit_add_data.place(x=10, y= 230)

    add_data_button = Button(main, text="Add Data", command=add_data, **button_style)
    add_data_button.place(x=50, y=10)


    def get_data():
        global question_get, question_print, show_answer_button, one_more_button
        destroying()
        question_get = Label(main, text="Question", font=font_main)
        question_get.place(x=10, y=70)
        with open("data.json", "r") as file:
            data = json.load(file)
        random_keys = random.choice(list(data.keys()))
        question_print = Label(main, text=random_keys, font=font_body)
        question_print.place(x=10, y=100)

        def show_answer():
            global answer_get, answer_print, one_more_button
            answer_get = Label(main, text="Answer", font=font_main)
            answer_get.place(x=10, y=240)
            random_entry = data[random_keys]
            answer_print = Label(main, text=random_entry, font=font_body)
            answer_print.place(x=10, y=270)

        def erase():
            to_erase = [question_get, question_print, show_answer_button]
            for widget in to_erase:
                widget.destroy()
            try:
                to_erase = [answer_get, answer_print]
                for widget in to_erase:
                    widget.destroy()
            except NameError:
                pass
            get_data()
        one_more_button = Button(main, text="One more", command=erase, **button_style_small)
        one_more_button.place(x=250, y=340)
        show_answer_button = Button(main, text="Show Answer", command=show_answer, **button_style_small)
        show_answer_button.place(x=10, y=200)
        

    get_data_button = Button(main, text="Boost Memory", command=get_data, **button_style)
    get_data_button.place(x=350, y=10)

    menu_bar = Menu(main)
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Upload data to Cloud", command=start_uploading)
    file_menu.add_command(label="Download data as PDF", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=main.quit)
    menu_bar.add_cascade(label="File", menu=file_menu, font=(12))
    

    about_me = Menu(menu_bar, tearoff=0)
    def open_facebook():
        webbrowser.open("https://www.facebook.com/ismailhrifat/")
    about_me.add_command(label="Facebook", command=open_facebook)
    def open_website():
        webbrowser.open("https://ismailhrifat.wordpress.com/")
    about_me.add_command(label="Website", command=open_website)
    def open_github():
        webbrowser.open("https://github.com/ismailhrifat")
    about_me.add_command(label="Github", command=open_github)
    def open_mail():
        webbrowser.open("mailto: ismail.hoshen.rifat@gmail.com?subject=Report about MemorizeMe")
    about_me.add_command(label="Report", command=open_mail)
    menu_bar.add_cascade(label="About me", menu=about_me, font=12)
    main.config(menu=menu_bar)

try:
    open("user_registered.json", "r")
    main_body()
except FileNotFoundError:
    def start_sign_up():
        try:
            global login_label
            socket.create_connection(("www.google.com", 80))
            signup_button.config(text="Signing in...")
            main.after(10, sign_up)
        except OSError:
            messagebox.showerror("Error!", "Device is not connected to internet.")
    def sign_up():
        full_name = full_name_entry.get()
        email = email_entry.get()
        if full_name != "" and email != "":
            user_data = {
                email : full_name
                }
            with open("user_registered.json", "w") as file:
                json.dump(user_data, file)
            client = storage.Client.from_service_account_json("keyfile.json")
            bucket = client.get_bucket("memorizeme")
            blob = bucket.blob("userinfo.json")
            blob.download_to_filename("userinfo.json")
            with open("user_registered.json", "r") as file:
                user_registered_data = json.load(file)

            email_id = list(user_registered_data.keys())[0]
            path = "userdata/" + email_id + ".json"
            blob_data = bucket.blob(path)
            with open("userinfo.json", "r") as file:
                emails = json.load(file)
                if email_id in emails:
                    blob_data.download_to_filename("data.json")
                else:
                    with open("userinfo.json", 'r') as file:
                        user_data = json.load(file)
                    with open("user_registered.json", "r") as file:
                        user_registered_data = json.load(file)
                    user_data.update(user_registered_data)

                    with open("userinfo.json", "w") as file:
                        json.dump(user_data, file)

                    blob.upload_from_filename("userinfo.json")
            destroying()
            main_body()
        else:
            messagebox.showwarning("Warning!", "Name or Email is missing.")
    full_name_label = Label(main, text="Full Name", font=font_body)
    full_name_label.place(x=200, y=100)
    full_name_entry = Entry(main)
    full_name_entry.place(x=200, y=125, height=25, width=200)
    email_label = Label(main, text="Email", font=font_body)
    email_label.place(x=200, y=160)
    email_entry = Entry(main)
    email_entry.place(x=200, y=185, height=25, width=200)
    signup_button = Button(main, text="Sign Up", command=start_sign_up, **button_style_signup)
    signup_button.place(x=200, y=220)

main.mainloop()