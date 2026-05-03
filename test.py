import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from ttkbootstrap.icons import Icon

app = ttk.Window()
app.state('zoomed')

ttk.Label(app, text=Icon.error).pack()

app.mainloop()