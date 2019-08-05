from tkinter import *
from tkinter import ttk
import tkinter
import barcode
from barcode.writer import ImageWriter
import os
import backend
from PIL import Image, ImageDraw, ImageFont

code_list = []
products_name = []
for i in backend.select_code_data():
	code_list.append(i[1])
	products_name.append(i[2])

class AutocompleteCombobox(tkinter.ttk.Combobox):

        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)
                self['values'] = self._completion_list

        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()): # Match case insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,tkinter.END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,tkinter.END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(tkinter.INSERT), tkinter.END)
                        self.position = self.index(tkinter.END)
                if event.keysym == "Left":
                        if self.position < self.index(tkinter.END): # delete the selection
                                self.delete(self.position, tkinter.END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, tkinter.END)
                if event.keysym == "Right":
                        self.position = self.index(tkinter.END) # go to end (no selection)
                if len(event.keysym) == 1:
                        self.autocomplete()


def create_barcode(code,product_name,price):
	EAN = barcode.get_barcode_class('code128')
	code_name = code
	ean = EAN(code_name, writer=ImageWriter())
	barcode_image_name = ean.save('{}_{}'.format(code_name,product_name))
	cwd = os.getcwd()
	image = Image.open(barcode_image_name)
	image_main = Image.open('final_img_barcode.jpg')
	main_image_sizex,main_image_sizey = image_main.size
	resized_img = image.resize((main_image_sizex-1500,main_image_sizey-1200))
	image_main.paste(resized_img,(700,500))
	image_main.save("{}/barcodes/{}".format(cwd,barcode_image_name))
	image_after = Image.open("{}/barcodes/{}".format(cwd,barcode_image_name))
	draw = ImageDraw.Draw(image_after)
	font = ImageFont.truetype('roboto-bold.ttf', size=100)
	(x, y) = (main_image_sizex-2300,main_image_sizey-1100) # (1300, 2000)
	message = "RS : {}".format(price)
	color = 'rgb(0, 0, 0)'
	draw.text((x, y), message, fill=color,font=font)
	image_after.save("{}/barcodes/{}".format(cwd,barcode_image_name))
	os.remove(barcode_image_name)
	product_code_ent.delete(0,END)
	product_name_ent.delete(0,END)
	product_price_ent.delete(0,END)



"""
def create_barcode(code,product_name):
	code_list = []
	for i in backend.select_code_data():
		code_list.append(i[1])
	EAN = barcode.get_barcode_class('code128')
	code_name = code
	ean = EAN(code_name, writer=ImageWriter())
	barcode_image_name = ean.save('{}_{}'.format(code_name,product_name))
	cwd = os.getcwd()
	image = Image.open(barcode_image_name)
	image_main = Image.open('final_img_barcode.jpg')
	main_image_sizex,main_image_sizey = image_main.size
	resized_img = image.resize((main_image_sizex-1500,main_image_sizey-1200))
	image_main.paste(resized_img,(700,500))
	image_main.save("{}/barcodes/{}".format(cwd,barcode_image_name))
	os.remove(barcode_image_name)
	# treeview.insert('', 'end', values=(code,product_name))
	# if code in code_list:
	# 	pass
	# else:
	# 	backend.add_code(code,product_name)

"""

def save_barcode(code,product_name,price):
	if code in code_list:
		pass
	elif product_name in products_name:
		pass
	else:
		backend.add_code(code,product_name,price)
		treeview.insert('', 'end', values=(code,product_name,price))
		product_code_ent.delete(0,END)
		product_name_ent.delete(0,END)
		product_price_ent.delete(0,END)

mainWin = Tk()
mainWin.geometry('500x500')
mainWin.resizable(False, False)
mainWin.title('BAR CODE GENERATOR')
def get_selected_row(event):
	for nm in tree.selection():
		content = tree.item(nm, 'values')
	selected_tuple = content
	product_code_ent.delete(0,END)
	product_name_ent.delete(0,END)
	product_code_ent.insert(0,selected_tuple[0])
	product_name_ent.insert(0,selected_tuple[1])
	product_price_ent.delete(0,END)
	product_price_ent.insert(0,selected_tuple[2])

grand_frame = Frame(mainWin)
grand_frame.pack(side='left')

# empty_lb = Label(frame_main, text='\t ')
# empty_lb.pack(side='right')

main_top_frame_1= Frame(grand_frame, width=300)
main_top_frame_1.pack(side="top")

main_top_frame= Frame(grand_frame, width=300)
main_top_frame.pack(side="top")

main_bottom_frame=Frame(grand_frame, width=300, bg="black")
main_bottom_frame.pack(side="bottom")



button_cmp = Label(main_top_frame_1, text = "BAR CODE GENERATOR", font=('HELVETICA',20,'bold'))
button_cmp.pack(side='left')

# button_cmp = Label(main_top_frame_1, text = "  ",height=0)
# button_cmp.pack(side='left')


# button_shop = Button(main_top_frame_1, text = "Add Customer")
# button_shop.pack(side='left')

# button_cmp = Label(main_top_frame_1, text = " ",height=0)
# button_cmp.pack(side='left')


# button_stock = Button(main_top_frame_1, text = "Add Product Details")
# button_stock.pack(side='left')

# button_cmp = Label(main_top_frame_1, text = " ",height=0)
# button_cmp.pack(side='left')


# button_stock = Button(main_top_frame_1, text = "Add Company")
# button_stock.pack(side='left')






win_lable = Label(main_top_frame, text= "\t ")
win_lable.grid(row=1, column=2)

win_lable = Label(main_top_frame, text= "\t ")
win_lable.grid(row=1, column=0)

win_lable = Label(main_top_frame, text= "\t ")
win_lable.grid(row=0, column=0)

c_frame1 = Frame(main_top_frame, width=400)
c_frame1.grid(row=1, column=1)

c_frame2 = Frame(main_top_frame, width=400)
c_frame2.grid(row=2, column=1)

c_frame3 = Frame(main_top_frame, width=400)
c_frame3.grid(row=3, column=1)

c_record = Label(c_frame1, text="\n ")
c_record.grid(row=0, column = 1)

c_l1 = Label(c_frame1, text="   Product Code :" )
c_l1.grid(row=1, column=0)

c_l2 = Label(c_frame1, text="   Product Name :")
c_l2.grid(row=3, column=0)

c_l2 = Label(c_frame1, text="   Product Name :")
c_l2.grid(row=5, column=0)

# c_l5 = Label(c_frame2, text="  ")
# c_l5.grid(row=4, column=0)


def search_by_code(code,name):
	data = backend.search_with_code_data(code,name)
	print(data)
	if data is not None:
		print('data is None')
		if name=='':
			try:
				product_name_ent.delete(0,END)
				product_name_ent.insert(0,data[2])
				product_price_ent.delete(0,END)
				product_price_ent.insert(0,data[3])
				product_name_ent.focus()
			except:
				product_name_ent.focus()
		elif code=='':
			product_code_ent.delete(0,END)
			product_code_ent.insert(0,data[1])
			product_price_ent.insert(0,data[3])
			c_b1.focus()
	else:
		print(code," : ", name)
		if name=='':
			product_name_ent.focus()
		elif code=='':
			product_price_ent.focus()

product_code_ent = AutocompleteCombobox(c_frame1, width=30)
product_code_ent.set_completion_list(code_list)
product_code_ent.grid(row=2, column=1, columnspan=4)
product_code_ent.focus_set()
product_code_ent.bind("<Return>", lambda event: search_by_code(product_code_ent.get(),''))



product_name_ent = AutocompleteCombobox(c_frame1, width=30)
product_name_ent.set_completion_list(products_name)
product_name_ent.grid(row=4, column=1, columnspan=4)
product_name_ent.bind("<Return>", lambda event: search_by_code('',product_name_ent.get()))
# product_name_ent.bind("<KeyRelease>", upper_address)


product_price_ent = Entry(c_frame1, width=33)
product_price_ent.grid(row=6, column=1, columnspan=4)
product_price_ent.bind("<Return>", lambda event: c_b1.focus())




c_empty_lable = Label(c_frame3, text='\t ')
c_empty_lable.grid(row=1, column=1)

def empty_entry_box():
	product_code_ent.delete(0,END)
	product_name_ent.delete(0,END)
	c_e3.delete(0,END)
	c_e4.delete(0,END)

c_b1 = Button(c_frame3, text="CREATE", width=10,command=lambda :create_barcode(product_code_ent.get(),product_name_ent.get(),product_price_ent.get()))
c_b1.grid(row=2, column=0)
c_b1.bind("<Return>", lambda event: create_barcode(product_code_ent.get(),product_name_ent.get(),product_price_ent.get()))



c_b2 = Button(c_frame3, text="SAVE", width=10,command=lambda :save_barcode(product_code_ent.get(),product_name_ent.get(),product_price_ent.get()))
c_b2.grid(row=2, column=4)
c_b2.bind("<Return>", lambda event: save_barcode(product_code_ent.get(),product_name_ent.get(),product_price_ent.get()))

# c_b2 = Button(c_frame3, text="SAVE", width=10)
# c_b2.grid(row=2, column=2)
# c_b2.bind("<Return>", lambda event: add_command())

c_empty_lable1 = Label(c_frame3, text='\t ')
c_empty_lable1.grid(row=3, column=1)


tree = ttk.Treeview(main_bottom_frame, columns=('Code', 'Name',"price"))
tree['show'] = 'headings'
tree.heading('#1', text='Product Code')
tree.heading('#2', text='Product Name')
tree.heading('#3', text='Price')
tree.column('#1', width=180, anchor='center')
tree.column('#2', width=200, anchor='center')
tree.column('#3', width=100, anchor='center')

tree.pack(side="left")
# tree.grid(row=4,column=0, columnspan=4, sticky='nsew')
tree.bind("<<TreeviewSelect>>",get_selected_row)
treeview = tree

for i in backend.select_code_data():
	tree.insert('',END,values=(i[1],i[2],i[3]))


vsb = ttk.Scrollbar(main_bottom_frame, orient="vertical", command=tree.yview)
vsb.pack(side="right", fill='y')
tree.configure(yscrollcommand=vsb.set)

mainWin.mainloop()