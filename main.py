from tkinter import *
from tkinter import filedialog as fd

from PIL import Image, ImageDraw, ImageFont, ImageTk

FONT = ImageFont.truetype(font="Futura Md BT Bold.ttf", size=60)
CANVAS_W = 600
CANVAS_H = 336
PREVIEW_W = 620
PREVIEW_H = 348
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
    print(file_path)
    path_to_img.config(text="File loaded", fg="green")


def show_img():
    global file_path

    new_window = Toplevel(app)
    new_window.title("Photo Preview")

    if file_path is None:
        new_window.minsize(width=PREVIEW_W, height=PREVIEW_H)
        error_label = Label(new_window, text="No photo selected", fg="red")
        error_label.place(x=PREVIEW_W / 2, y=PREVIEW_H / 2, anchor=CENTER)
        path_to_img.config(text="No photo selected, try again", fg="red")

    else:

        pill_img = Image.open(file_path)
        w, h = pill_img.size
        aspect_ratio = h / w

        if w > h:
            new_w = CANVAS_W - 20
            new_h = round(new_w * aspect_ratio)
            pill_img = pill_img.resize((new_w, new_h), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(pill_img)

            new_window.minsize(width=PREVIEW_W, height=PREVIEW_H)

            canvas2 = Canvas(new_window, width=CANVAS_W, height=CANVAS_H)
            canvas2.place(x=PREVIEW_W / 2, y=PREVIEW_H / 2, anchor=CENTER)
            canvas_img = canvas2.create_image(
                CANVAS_W / 2, CANVAS_H / 2, image=img, anchor=CENTER)
        else:
            new_w = CANVAS_H - 20
            new_h = round(new_w * aspect_ratio)
            pill_img = pill_img.resize((new_w, new_h), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(pill_img)

            new_window.minsize(width=PREVIEW_H, height=PREVIEW_W)

            canvas2 = Canvas(new_window, width=CANVAS_H, height=CANVAS_W)
            canvas2.place(x=PREVIEW_H / 2, y=PREVIEW_W / 2, anchor=CENTER)
            canvas_img = canvas2.create_image(
                CANVAS_H / 2, CANVAS_W / 2, image=img, anchor=CENTER)

    new_window.mainloop()


def add_watermark():
    global img
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
    new_window = Toplevel(app)
    new_window.title("Result Preview")

    if img is None:
        new_window.minsize(width=PREVIEW_W, height=PREVIEW_H)
        error_label = Label(new_window, text="No watermark added", fg="red")
        error_label.place(x=PREVIEW_W / 2, y=PREVIEW_H / 2, anchor=CENTER)
        result_label.config(
            text="Please type text for watermark", fg="red")

    else:

        w, h = img.size
        aspect_ratio = h / w
        if w > h:
            new_w = CANVAS_W - 20
            new_h = round(new_w * aspect_ratio)
            img_resized = img.resize((new_w, new_h), Image.ANTIALIAS)
            watermarked_img = ImageTk.PhotoImage(img_resized)

            new_window.minsize(width=PREVIEW_W, height=PREVIEW_H + 50)

            canvas2 = Canvas(new_window, width=CANVAS_W, height=CANVAS_H)
            canvas2.place(x=PREVIEW_W / 2, y=PREVIEW_H / 2, anchor=CENTER)
            canvas_img = canvas2.create_image(
                CANVAS_W / 2, CANVAS_H / 2, image=watermarked_img, anchor=CENTER)
            save_btn = Button(new_window, text="Save Result As",
                              command=save_result)
            save_btn.place(x=PREVIEW_W / 2, y=PREVIEW_H + 20, anchor=CENTER)
        else:
            new_w = CANVAS_H - 20
            new_h = round(new_w * aspect_ratio)
            img_resized = img.resize((new_w, new_h), Image.ANTIALIAS)
            watermarked_img = ImageTk.PhotoImage(img_resized)

            new_window.minsize(width=PREVIEW_H, height=PREVIEW_W + 50)

            canvas2 = Canvas(new_window, width=CANVAS_H, height=CANVAS_W)
            canvas2.place(x=PREVIEW_H / 2, y=PREVIEW_W / 2, anchor=CENTER)
            canvas_img = canvas2.create_image(
                CANVAS_H / 2, CANVAS_W / 2, image=watermarked_img, anchor=CENTER)
            save_btn = Button(new_window, text="Save Result As",
                              command=save_result)
            save_btn.place(x=PREVIEW_H / 2, y=PREVIEW_W + 20, anchor=CENTER)

    new_window.mainloop()
    pass


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

watermark_brn = Button(text="Add Watermark", command=add_watermark)
watermark_brn.grid(row=5, column=0)

result_btn = Button(text="Show Result", command=show_result)
result_btn.grid(row=5, column=1)

img_watermark_label = Label(text="Select logo for watermarking")
img_watermark_label.grid(row=6, column=0)

logo_select_btn = Button(text="Browse Logo")
logo_select_btn.grid(row=7, column=0)

add_img_watermark_btn = Button(text="Add Img Logo")
add_img_watermark_btn.grid(row=7, column=1)


app.mainloop()
