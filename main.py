from tkinter import *
from tkinter import filedialog as fd

from PIL import Image, ImageDraw, ImageFont, ImageTk

FONT = ImageFont.truetype(font="Futura Md BT Bold.ttf", size=60)
file_path = None
img = None


def open_file():
    global file_path
    filetypes = (
        ("Image files", "*.jpg"),
        ("all files", "*.*")
    )
    file_path = fd.askopenfilename(
        title="Open image",
        initialdir="/",
        filetypes=filetypes
    )
    if file_path != "":
        path_to_img.config(text="File loaded", fg="green")
        show_btn.config(state="normal")
        logo_watermark_btn.config(state="normal")
        text_watermark_btn.config(state="normal")
        watermark_btn.config(state="normal")


def show_img():
    preview_window = Toplevel(app)
    preview_window.title("Photo Preview")
    # If image is selected
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


def add_watermark():
    global img
    # # If no image selected
    if file_path is None:
        result_label.config(
            text="No photo or logo selected, try again", fg="red")
    else:
        img = Image.open(file_path)
        img_w, img_h = img.size
        if choice.get() == "text":
            text = watermark_entry.get()
            watermark = ImageDraw.Draw(img)
            text_width = watermark.textlength(text=text, font=FONT)
            watermark.text((img_w - text_width - 20, img_h - 80),
                           text=text, fill=(255, 0, 0), font=FONT)
        elif choice.get() == "logo":
            logo_img = Image.open(logo_path)
            logo_w, logo_h = logo_img.size
            img.paste(im=logo_img, box=(
                img_w - logo_w - 20, img_h - logo_h - 20))
        result_label.config(text="Success", fg="green")
        result_btn.config(state="normal")
        save_btn.config(state="normal")


def show_result():
    result_window = Toplevel(app)
    result_window.title("Result Preview")
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
    preview_h = canvas_h + 20
    img_resized = img.resize((canvas_w, canvas_h), Image.ANTIALIAS)
    watermarked_img = ImageTk.PhotoImage(img_resized)
    # Setting window size
    result_window.minsize(width=preview_w, height=preview_h)
    # Creating Canvas and placing image on it
    result_canvas = Canvas(result_window, width=canvas_w, height=canvas_h)
    result_canvas.place(
        x=preview_w / 2, y=preview_h / 2, anchor=CENTER)
    result_canvas_img = result_canvas.create_image(
        canvas_w / 2, canvas_h / 2, image=watermarked_img, anchor=CENTER)
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
    result_label.config(text="Logo image loaded", fg="green")


def watermark_type():
    if choice.get() == "text":
        watermark_entry.config(state="normal")
        logo_select_btn.config(state="disabled")
    elif choice.get() == "logo":
        watermark_entry.config(state="disabled")
        logo_select_btn.config(state="normal")


app = Tk()
app.title("Image Watermarking")
app.minsize(width=400, height=200)
app.config(padx=30, pady=30)

open_btn = Button(text="Browse Files", command=open_file, width=10)
open_btn.grid(row=0, column=0)

show_btn = Button(text="Preview Image", command=show_img,
                  state="disabled", width=10)
show_btn.grid(row=0, column=1)

path_to_img = Label(text="")
path_to_img.grid(row=1, column=0, columnspan=2)

choice = StringVar()

text_watermark_btn = Radiobutton(
    text="Add text watermark", variable=choice, value="text", command=watermark_type, state="disabled")
text_watermark_btn.grid(row=2, column=0)

logo_watermark_btn = Radiobutton(
    text="Add logo watermark", variable=choice, value="logo", command=watermark_type, state="disabled")
logo_watermark_btn.grid(row=2, column=1)

text_watermark_label = Label(text="Type in text for watermark")
text_watermark_label.grid(row=3, column=0)

img_watermark_label = Label(text="Select logo for watermarking")
img_watermark_label.grid(row=3, column=1)

watermark_entry = Entry(width=20, state="disabled")
watermark_entry.grid(row=4, column=0)

logo_select_btn = Button(
    text="Browse Logo", command=open_logo, state="disabled", width=10)
logo_select_btn.grid(row=4, column=1)

result_label = Label(text="")
result_label.grid(row=5, column=0, columnspan=3)

watermark_btn = Button(text="Add Watermark",
                       command=add_watermark, state="disabled", width=10)
watermark_btn.grid(row=6, column=0, columnspan=2)

result_btn = Button(text="Show Result", command=show_result,
                    state="disabled", width=10)
result_btn.grid(row=7, column=0, columnspan=2)

save_btn = Button(text="Save Result As", command=save_result,
                  state="disabled", width=10)
save_btn.grid(row=8, column=0, columnspan=2)

app.mainloop()
