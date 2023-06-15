import sqlite3
try:
	import tkinter
except ImportError:
	import Tkinter as tkinter

conn=sqlite3.connect("music.sqlite")

class Scrollbox(tkinter.Listbox):

	def __init__(self, window, **kwargs):
		# tkinter.Listbox.__init__(self, window, **kwrags) - # python 2
		super().__init__(window, **kwargs)

		self.scrollbar=tkinter.Scrollbar(window, orient=tkinter.VERTICAL, command=self.yview)

	def grid(self, row, column, sticky='nsw', rowspan=1, columnspan=1, **kwargs):
		# tkinter.Listbox.grid(self, row=row, column=column, sticky=sticky, rowpsan=rowspan, **kwrags) # python 2
		super().grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, **kwargs)
		self.scrollbar.grid(row=row, column=column, sticky='nse', rowspan=rowspan)
		self['yscrollcommand']=self.scrollbar.set

# def get_albums(event):
# 	lb=event.widget
# 	index=lb.curselection()[0]
# 	artist_name=lb.get(index),

# 	# get the artist ID from the database row
# 	artist_id=conn.execute("SELECT artists._id FROM artists WHERE artists.name=?",artist_name).fetchone()
# 	alist=[]
# 	for row in conn.execute("SELECT albums.name FROM albums WHERE albums.artist=? ORDER BY albums.name",artist_id):
# 		alist.append(row[0])
# 	albumLV.set(tuple(alist))

# def get_songs(event):
# 	lb=event.window
# 	index=int(lb.curselection()[0])
# 	album_name=lb.get(index),

# 	# get the artist id from the database row
# 	album_id=conn.execute("SELECT albums._id FROM albums WHERE albums.name=?",album_name).fetchone()
# 	aList=[]
# 	for row in conn.execute("SELECT songs.title FROM songs WHERE songs.album=? ORDER BY songs.track", album_id):
# 		aList.append(row[0])
# 	songLV.set(tuple(aList))

class DataListBox(Scrollbox):

	def __init__(self, window, connection, table, field, sort_order=(), **kwargs):
		# Scrollbox.__init__(self, window, **kwargs) # Python 2
		super().__init__(window, **kwargs)

		self.cursor=connection.cursor()
		self.table=table
		self.field=field

		self.sql_select = "SELECT "+ self.field + ", _id"+" FROM "+self.table
		if sort_order:
			self.sql_sort= " ORDER BY "+",".join(sort_order)
		else:
			self.sql_sort= " ORDER BY "+self.field

	def clear(self):
		self.delete(0, tkinter.END)

	# def requery(self):
	# 	print(self.sql_select+self.sql_sort)
	# 	self.cursor.execute(self.sql_select+self.sql_sort)

	# 	# clear the listbox contens before re-loading
	# 	self.clear()
	# 	for value in self.cursor:
	# 		self.insert(tkinter.END, value[0])

	def requery(self, link_value=None):
		if link_value:
			sql=self.sql_select+ " WHERE "+"artist"+"=?"+self.sql_sort
			print(sql)
			self.cursor.execute(sql, (link_value,))
		else:
			print(self.sql_select+self.sql_sort)
			self.cursor.execute(self.sql_select+self.sql_sort)

		# clear the listbox contents before re-loading
		self.clear()
		for value in self.cursor:
			self.insert(tkinter.END, value[0])

	def on_select(self, event):
		print(self is event.window)
		index=self.curselection()[0]
		value=self.get(index)

		link_id=self.cursor.execute(self.sql_select+" WHERE "+self.field+"=?",value).fetchone()[1]
		albumList.requery(link_id)

def get_albums(event):
    lb = event.widget
    index = lb.curselection()[0]
    artist_name = lb.get(index),

    # get the artist ID from the database row
    # artist_id = conn.execute("SELECT artists._id FROM artists WHERE artists.name=?", artist_name).fetchone()
    # alist = []
    # for row in conn.execute("SELECT albums.name FROM albums WHERE albums.artist = ? ORDER BY albums.name", artist_id):
    #     alist.append(row[0])
    # albumLV.set(tuple(alist))
    # # songLV.set(("Choose an album",))
    # songLV.set(("Choose an album",))
    artist_id=conn.execute("SELECT artists._id FROM artists WHERE artists.name=?",artist_name).fetchone()[0]
    albumList.requery(artist_id)

def get_songs(event):
    lb = event.widget
    index = int(lb.curselection()[0])
    album_name = lb.get(index),

    # get the artist ID from the database row
    album_id = conn.execute("SELECT albums._id FROM albums WHERE albums.name=?", album_name).fetchone()
    alist = []
    for x in conn.execute("SELECT songs.title FROM songs WHERE songs.album=? ORDER BY songs.track", album_id):
        alist.append(x[0])
    songLV.set(tuple(alist))

mainWindow=tkinter.Tk()
mainWindow.title("Music DB Browser")
mainWindow.geometry('1024x768')

#column configure
mainWindow.columnconfigure(0, weight=2)
mainWindow.columnconfigure(1, weight=2)
mainWindow.columnconfigure(2, weight=2)
mainWindow.columnconfigure(3, weight=1)

#row configure
mainWindow.rowconfigure(0, weight=1)
mainWindow.rowconfigure(1, weight=5)
mainWindow.rowconfigure(2, weight=5)
mainWindow.rowconfigure(3, weight=1)

# ====== Label configure ====
tkinter.Label(mainWindow, text="Artists").grid(row=0, column=0)
tkinter.Label(mainWindow, text="Albums").grid(row=0, column=1)
tkinter.Label(mainWindow, text="Songs").grid(row=0, column=2)

# ---- Artist ListBox

# artistList=tkinter.Listbox(mainWindow)
# artistList=Scrollbox(mainWindow, background="blue")
# artistList=Scrollbox(mainWindow)
artistList=DataListBox(mainWindow, conn, "Artists","name")
artistList.grid(row=1, column=0, sticky='nsew', rowspan=2, padx=(30,0))
artistList.config(border=2, relief='sunken')

# --- adding artist scrollbar

# artistScroll=tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=artistList.yview)
# artistScroll.grid(row=1,column=0,sticky='nse',rowspan=2)
# artistList['yscrollcommand']=artistScroll.set

# Load artist from database
# for artist in conn.execute("SELECT artists.name FROM artists ORDER BY artists.name"):
# 	artistList.insert(tkinter.END, artist[0])

artistList.requery()
artistList.bind("<<ListboxSelect>>", get_albums)

# ------- Album ListBox

albumLV=tkinter.Variable(mainWindow)
albumLV.set(("Choose an artist",))
# albumList=tkinter.Listbox(mainWindow, listvariable=albumLV)
# albumList=Scrollbox(mainWindow, listvariable=albumLV)
albumList=DataListBox(mainWindow, conn, "albums", "name", sort_order=("name",))
albumList.requery()
albumList.grid(row=1, column=1, sticky='nsew',padx=(30,0))
albumList.config(border=2, relief='sunken')

albumList.bind("<<ListboxSelection>>", get_songs)

# ------ album Scrollbar

# albumScroll=tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=albumList.yview)
# albumScroll.grid(row=1, column=1, sticky='nse', rowspan=2)
# albumList['yscrollcommand']=albumScroll.set

# albumLV.set((1,2,3,4,5,6))
testList=range(0,100)
albumLV.set(tuple(testList))

# ----- Songs Listbox

songLV=tkinter.Variable(mainWindow)
songLV.set(("Choose an album",))
# songList=tkinter.Listbox(mainWindow, listvariable=songLV)

# songList=Scrollbox(mainWindow, listvariable=songLV)
songList=DataListBox(mainWindow, conn, "songs", "title", ("track","title"))
songList.requery()
songList.grid(row=1, column=2, sticky='nsew', padx=(30,0))
songList.config(border=2, relief='sunken')

# ---- Main Loop
mainWindow.mainloop()
print("Closing database connection")
conn.close()