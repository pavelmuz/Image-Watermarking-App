from tkinter import *
from tkinter import filedialog as fd

import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageTk

FONT = ImageFont.truetype(font="Futura Md BT Bold.ttf", size=60)
file_path = None
img = None


def open_file():
    global file_path
    filetypes = (
        ("Image files", "*.jpg"),
        ("PNG files", "*.png"),
        ("all files", "*.*")
    )
    file_path = fd.askopenfilename(
        title="Open image",
        initialdir="/",
        filetypes=filetypes
    )
    path_to_img.config(text="File loaded", fg="green")


def show_img():
    preview_window = Toplevel(app)
    preview_window.title("Photo Preview")
    # If no image selected
    if file_path is None:
        preview_window.minsize(width=300, height=200)
        error_label = Label(preview_window, text="No photo selected", fg="red")
        error_label.place(x=150, y=100, anchor=CENTER)
        path_to_img.config(text="No photo selected, try again", fg="red")
    # If image is selected
    else:
        # Load Image by file_path and getting resoultion
        pill_img = Image.open(file_path)
        w, h = pill_img.size
        aspect_ratio = h / w
        # Setting window height for horizontal or rectangle images
        if w >= h:
            preview_w = 650
        # Setting window height for verttical images
        else:
            preview_w = 350
        # Resizing image to fit new window and setting Canvas size and window height
        canvas_w = preview_w - 20
        canvas_h = round(canvas_w * aspect_ratio)
        preview_h = canvas_h + 20
        pill_img = pill_img.resize((canvas_w, canvas_h), Image.ANTIALIAS)
        preview_img = ImageTk.PhotoImage(pill_img)
        # Setting window size
        preview_window.minsize(width=preview_w, height=preview_h)
        # Creating Canvas and placing image on it
        preview_canvas = Canvas(
            preview_window, width=canvas_w, height=canvas_h)
        preview_canvas.place(x=preview_w / 2, y=preview_h / 2, anchor=CENTER)
        preview_canvas_img = preview_canvas.create_image(
            canvas_w / 2, canvas_h / 2, image=preview_img, anchor=CENTER)
    preview_window.mainloop()


def add_text_watermark():
    global img
    # # If no image selected
    if file_path is None:
        path_to_img.config(text="No photo selected, try again", fg="red")
    else:
        text = watermark_entry.get()
        img = Image.open(file_path)
        w, h = img.size
        watermark = ImageDraw.Draw(img)
        text_width = watermark.textlength(text=text, font=FONT)
        watermark.text((w - text_width - 20, h - 80),
                       text=text, fill=(255, 0, 0), font=FONT)
        result_label.config(text="Success", fg="green")


def show_result():
    result_window = Toplevel(app)
    result_window.title("Result Preview")
    # If no watermak added
    if img is None:
        result_window.minsize(width=300, height=200)
        error_label = Label(result_window, text="No watermark added", fg="red")
        error_label.place(x=150, y=100, anchor=CENTER)
        result_label.config(
            text="Please type text for watermark", fg="red")
    # If watermark added
    else:
        # Get image resolution
        w, h = img.size
        aspect_ratio = h / w
        # Setting window height for horizontal or rectangle images
        if w >= h:
            preview_w = 650
        # Setting window height for verttical images
        else:
            preview_w = 350
        # Resizing image to fit new window and setting Canvas size and window height
        canvas_w = preview_w - 20
        canvas_h = round(canvas_w * aspect_ratio)
        preview_h = canvas_h + 50
        img_resized = img.resize((canvas_w, canvas_h), Image.ANTIALIAS)
        watermarked_img = ImageTk.PhotoImage(img_resized)
        # Setting window size
        result_window.minsize(width=preview_w, height=preview_h)
        # Creating Canvas and placing image on it
        result_canvas = Canvas(result_window, width=canvas_w, height=canvas_h)
        result_canvas.place(
            x=preview_w / 2, y=(preview_h - 30) / 2, anchor=CENTER)
        result_canvas_img = result_canvas.create_image(
            canvas_w / 2, canvas_h / 2, image=watermarked_img, anchor=CENTER)
        # Btn to save watermarked image as file
        save_btn = Button(result_window, text="Save Result As",
                          command=save_result)
        save_btn.place(x=preview_w / 2, y=preview_h - 25, anchor=CENTER)
    result_window.mainloop()


def save_result():
    filetypes = (
        ("Image files", "*.jpg"),
        ("PNG files", "*.png"),
        ("all files", "*.*")
    )
    img_name = fd.asksaveasfilename(
        filetypes=filetypes, defaultextension=filetypes)
    if img_name:
        img.save(img_name)


def open_logo():
    global logo_path
    filetypes = (
        ("Image files", "*.jpg"),
        ("PNG files", "*.png"),
        ("all files", "*.*")
    )
    logo_path = fd.askopenfilename(
        title="Open image",
        initialdir="/",
        filetypes=filetypes
    )
    logo_result_label.config(text="Logo image loaded", fg="green")


def add_image_watermark():
    # # If no image selected
    if file_path is None:
        path_to_img.config(text="No photo selected, try again", fg="red")
    else:
        img = Image.open(file_path)
        img_w, img_h = img.size
        logo_img = Image.open(logo_path)
        logo_w, logo_h = logo_img.size
        img.paste(im=logo_img, box=(img_w - logo_w - 20, img_h - logo_h - 20))
        img.save("test.jpg")


app = Tk()
app.title("Image Watermarking")
app.minsize(width=400, height=300)

open_btn = Button(text="Browse Files", command=open_file)
open_btn.grid(row=0, column=0)

show_btn = Button(text="Preview Image", command=show_img)
show_btn.grid(row=0, column=1)

path_to_img = Label(text="")
path_to_img.grid(row=1, column=0, columnspan=4)

text_watermark_label = Label(text="Type in text for watermark:")
text_watermark_label.grid(row=2, column=0)

watermark_entry = Entry(width=30)
watermark_entry.grid(row=3, column=0, columnspan=4)

result_label = Label(text="")
result_label.grid(row=4, column=0, columnspan=3)

watermark_brn = Button(text="Add Watermark", command=add_text_watermark)
watermark_brn.grid(row=5, column=0)

result_btn = Button(text="Show Result", command=show_result)
result_btn.grid(row=5, column=1)

img_watermark_label = Label(text="Select logo for watermarking")
img_watermark_label.grid(row=6, column=0)

logo_select_btn = Button(text="Browse Logo", command=open_logo)
logo_select_btn.grid(row=7, column=0)

logo_result_label = Label(text="")
logo_result_label.grid(row=8, column=0, columnspan=3)

add_img_watermark_btn = Button(
    text="Add Img Logo", command=add_image_watermark)
add_img_watermark_btn.grid(row=9, column=0)


app.mainloop()
