from requests import get, post
from json import loads
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter.messagebox import showinfo
from ttkbootstrap import Window, Treeview, LabelFrame, Label, Entry, Button, StringVar, Scrollbar, Menu, Toplevel, Combobox
from ttkbootstrap.style import Style
from threading import Thread



class WinGUI2(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.__win()
        self.stylelist = ("cosmo", "flatly", "litera", "minty", "lumen", "sandstone", "yeti", "pulse", "united", "morph", "journal", "darkly", "superhero", "solar", "cyborg", "cerculean", "simplex", "vapor")
        self.tk_select_box_1 = self.__tk_select_box_1(self)
        self.tk_button_cancel = self.__tk_button_cancel(self)
        self.tk_button_ok = self.__tk_button_ok(self)
 
    def __win(self):
        self.title("更改界面风格")
        width = 230
        height = 90
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
 
    def __tk_select_box_1(self, parent):
        self.select_box_1_var = StringVar(parent, "")
        cb = Combobox(parent, state="readonly", textvariable=self.select_box_1_var, bootstyle="default", values=self.stylelist)
        cb.place(x=10, y=10, width=210, height=30)
        cb.current(0)
        return cb
 
    def __tk_button_cancel(self, parent):
        btn = Button(parent, text="取消", takefocus=False, bootstyle="default")
        btn.place(x=10, y=50, width=100, height=30)
        return btn
 
    def __tk_button_ok(self, parent):
        btn = Button(parent, text="确定", takefocus=False, bootstyle="default")
        btn.place(x=120, y=50, width=100, height=30)
        return btn
 
class Win2(WinGUI2):
    def __init__(self, parent, ok):
        super().__init__(parent)
        self.__event_bind()
        self.tk_select_box_1.current(self.stylelist.index(parent.stylename))
        self.parent = parent
        self.last = parent.stylename
        self.ok_ = ok
 
    def change(self, evt):
        self.parent.stylename = self.select_box_1_var.get()
        self.parent._style = Style(self.parent.stylename)
 
    def cancel(self, evt):
        self.parent.stylename = self.last
        self.parent._style = Style(self.last)
        self.ok()
 
    def ok(self, evt=None):
        self.ok_()
        self.destroy()
 
    def __event_bind(self):
        self.tk_select_box_1.bind('<<ComboboxSelected>>', self.change)
        self.tk_button_cancel.bind('<Button-1>', self.cancel)
        self.tk_button_ok.bind('<Button-1>', self.ok)
        self.protocol("WM_DELETE_WINDOW", self.ok)



class WinGUI(Window):
    def __init__(self):
        super().__init__(themename="cosmo", hdpi=False)
        self.__win()
        self.tk_table_1 = self.__tk_table_1(self)
        self.tk_label_frame_1 = self.__tk_label_frame_1(self)
        self.tk_label_1 = self.__tk_label_1(self.tk_label_frame_1)
        self.tk_input_name = self.__tk_input_name(self.tk_label_frame_1)
        self.tk_button_search = self.__tk_button_search(self.tk_label_frame_1)
 
    def __win(self):
        self.title("音乐下载程序")
        width = 600
        height = 400
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

    def scrollbar_autohide(self, vbar, hbar, widget):
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self, vbar, widget, x, y, w, h):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(x=x + w, y=y, height=h, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(x=x, y=y + h, width=w, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_table_1(self, parent):
        columns = {'搜索词': 100, "状态": 80, "索引": 48, "名称": 200, "歌手": 148}
        tk_table = Treeview(parent, show="headings", bootstyle="primary", columns=list(columns.keys()))
        for text, width in columns.items():
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', minwidth=width, width=width, stretch=False)
        tk_table.place(x=10, y=80, width=580, height=310)
        self.create_bar(parent, tk_table, True, False, 10, 80, 580, 310)
        return tk_table
 
    def __tk_label_frame_1(self, parent):
        frame = LabelFrame(parent, text="添加", bootstyle="primary")
        frame.place(x=10, y=10, width=580, height=60)
        return frame
 
    def __tk_label_1(self, parent):
        label = Label(parent, text="名称：", anchor="center", bootstyle="default")
        label.place(x=10, y=0, width=50, height=30)
        return label
 
    def __tk_input_name(self, parent):
        self.input_name_var = StringVar(parent, "")
        ipt = Entry(parent, bootstyle="default", textvariable=self.input_name_var)
        ipt.place(x=60, y=0, width=420, height=30)
        return ipt
 
    def __tk_button_search(self, parent):
        btn = Button(parent, text="添加", takefocus=False, bootstyle="default outline")
        btn.place(x=490, y=0, width=80, height=30)
        return btn
 
class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()
        self.config(menu=self.create_menu())
        self.l = []
        self.n = []
        self.done = []
        self.path = 'C:/Users/Administrator/Downloads'
        self.stylename = "cosmo"
 
    def create_menu(self):
        menu = Menu(self, tearoff=False)
        sub_menu = Menu(menu, tearoff=False)
        sub_menu.add_command(label="添加歌曲列表", command=self.add_from_file)
        sub_menu.add_command(label="全部下载", command=self.download_all)
        menu.add_cascade(label="批量操作", menu=sub_menu)

        menu.add_command(label="更改保存位置", command=self.change)
        menu.add_command(label="更改界面风格", command=self.change_theme)
        menu.add_command(label="操作指引", command=self.how)
        menu.add_command(label="关于", command=self.about)
        return menu
 
    def add_from_file(self):
        file_path = askopenfilename(title="选择歌曲列表文件")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        t = Thread(target = self.run, args = (line,))
                        t.daemon = True
                        t.start()
    
    def download_all(self):
        for item in self.tk_table_1.get_children():
            if self.tk_table_1.item(item, 'values')[1] != "正在搜索":
                index = int(item[1:]) - 1
                if not self.done[index]:
                    self.done[index] = True
                    self.tk_table_1.set(item, column='#002', value='正在下载')
                    t = Thread(target = self.download, args = (index, item))
                    t.daemon = True
                    t.start()

    def search(self, name: str, pn: int = 0, rn: int = 10):
        if pn != 0:
            url = 'https://search.kuwo.cn/r.s?all=%s&ft=music&client=kt&cluster=0&pn=%d&rn=%d&rformat=json&callback=searchMusicResult&encoding=utf8&vipver=MUSIC_8.0.3.1' % (name, pn, rn)
        else:
            url = 'https://search.kuwo.cn/r.s?all=%s&ft=music&client=kt&cluster=0&rn=%d&rformat=json&callback=searchMusicResult&encoding=utf8&vipver=MUSIC_8.0.3.1' % (name, rn)

        html = get(url)

        data = eval(html.text[17 : -53])['abslist']

        return([{'name': data[i]['SONGNAME'].replace("&nbsp;", " "), 'index': data[i]['MUSICRID'][6:], 'singer': data[i]['ARTIST'].replace("&nbsp;", " ")} for i in range(len(data))])

    def downloadm(self, id: str, path: str) -> None:
        url = 'https://api.isoudy.com/api/ajax.php'
        data = {'mid': id}

        req = post(url, data = data)
        content = loads(req.text)

        reponse = get(content['data']['url'])

        with open(path, 'wb') as f:
            f.write(reponse.content)

    def run(self, name):
        index = len(self.l)
        self.l.append([])
        self.n.append(0)
        self.done.append(False)
        self.tk_table_1.insert('', 'end', text=index, values=[name, "正在搜索", 0, '-', '-'])
        self.l[index] = self.search(name, 0, 10)
        item = "I%03d" % (index + 1)
        self.tk_table_1.set(item, column='#002', value='等待确认')
        self.tk_table_1.set(item, column='#004', value=self.l[index][self.n[index]]['name'])
        self.tk_table_1.set(item, column='#005', value=self.l[index][self.n[index]]['singer'])

    def download(self, index, item):
        self.downloadm(self.l[index][self.n[index]]['index'], '%s/%s.mp3' % (self.path, self.l[index][self.n[index]]['name']))
        self.tk_table_1.set(item, column='#002', value='下载完成')

    def add(self, evt):
        if self.input_name_var.get() != "":
            t = Thread(target = self.run, args = (self.input_name_var.get(),))
            t.daemon = True
            t.start()

    def left(self, evt):
        item = self.tk_table_1.selection()
        if item != () and self.tk_table_1.item(item, 'values')[1] != "正在搜索":
            index = int(item[0][1:]) - 1
            if not self.done[index] and self.n[index] != 0:
                self.n[index] -= 1
                self.tk_table_1.set(item[0], column='#003', value=self.n[index])
                self.tk_table_1.set(item[0], column='#004', value=self.l[index][self.n[index]]['name'])
                self.tk_table_1.set(item[0], column='#005', value=self.l[index][self.n[index]]['singer'])

    def right_thread(self):
        item = self.tk_table_1.selection()
        if item != () and self.tk_table_1.item(item, 'values')[1] != "正在搜索":
            index = int(item[0][1:]) - 1
            if not self.done[index]:
                self.done[index] = True
                self.n[index] += 1
                self.tk_table_1.set(item[0], column='#003', value=self.n[index])
                if self.n[index] >= len(self.l[index]):
                    self.tk_table_1.set(item[0], column='#002', value='正在搜索')
                    self.tk_table_1.set(item[0], column='#004', value='-')
                    self.tk_table_1.set(item[0], column='#005', value='-')
                    self.l[index] += self.search(self.tk_table_1.item(item, 'values')[0], int(len(self.l[index]) / 10), 10)
                    self.tk_table_1.set(item[0], column='#002', value='等待确认')
                self.tk_table_1.set(item[0], column='#004', value=self.l[index][self.n[index]]['name'])
                self.tk_table_1.set(item[0], column='#005', value=self.l[index][self.n[index]]['singer'])
                self.done[index] = False

    def right(self, evt):
        t = Thread(target = self.right_thread)
        t.daemon = True
        t.start()

    def rt(self, evt):
        item = self.tk_table_1.selection()
        if item != () and self.tk_table_1.item(item, 'values')[1] != "正在搜索":
            index = int(item[0][1:]) - 1
            if not self.done[index]:
                self.done[index] = True
                self.tk_table_1.set(item[0], column='#002', value='正在下载')
                t = Thread(target = self.download, args = (index, item[0]))
                t.daemon = True
                t.start()
    
    def change(self):
        path = askdirectory(initialdir=self.path, title='更改保持位置')
        if path != "":
            self.path = path

    def about(self):
        showinfo(title='关于', message='应用名称：音乐下载器（music_downloader）\n版本：1.0\n作者：樊\n\n通过“酷我音乐”（http://www.kuwo.cn）的搜索引擎搜索音乐，并使用“爱好歌音乐网”（https://www.ihaoge.net/）进行解析下载。')

    def how(self):
        showinfo(title='操作指引', message='输入乐曲名或歌手名，按下回车键或点击添加键将其添加至队列中。\n\n在队列中选择某一首歌曲：通过左右键切换搜索结果，按下回车键以将音乐保存至本地。\n\n批量操作文件格式：使用UTF-8编码，每行一首歌。')
 
    def ok(self):
        self.attributes("-disabled", 0)

    def change_theme(self):
        Win2(self, self.ok)
        self.attributes("-disabled", 1)

    def __event_bind(self):
        self.tk_button_search.bind('<Button-1>', self.add)
        self.tk_table_1.bind('<Left>', self.left)
        self.tk_table_1.bind('<Right>', self.right)
        self.tk_table_1.bind('<Return>', self.rt)
        self.tk_input_name.bind('<Return>', self.add)

Win().mainloop()