from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import numpy as np
from io import StringIO

class Table:
    def __init__(self, root) -> None:
        self.root = root
        

    def _get_content(self):
        with filedialog.askopenfile() as f:
            d = StringIO(f.read())
            content = np.loadtxt(d, delimiter=",")
        
        return content
    

    def show(self) -> None:
        values = self._get_content()
        if len(values) == 0:
            return 
        
        scrolly = Scrollbar(self.root)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx = Scrollbar(self.root,orient='horizontal')
        scrollx.pack(side=BOTTOM, fill=X)

        table = ttk.Treeview(self.root,yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        table.pack()

        scrolly.config(command=table.yview)
        scrollx.config(command=table.xview)

        
        table.column("#0", width=0,  stretch=NO)
        table['columns'] = [str(i) for i in range(len(values[0]))]
        for i, _ in enumerate(values[0]):
            table.column(str(i), anchor=CENTER, width=30)
        
        for i, row in enumerate(values):
            table.insert(parent='', index='end', iid=i,  text='', values=row.tolist())
        
        table.pack()

def main():
    root = Tk()    
    W, H = 400, 400
    root.geometry(f"{W}x{H}")
    content = Frame(root)

    # Table 
    table_frame = Frame(content)
    table_frame.pack()
    table = Table(table_frame)
    table.show()

    # Load file
    # load_file = Button(content, text="Load", command=lambda:table.show(), width=5)
    # file_path = Label(content, text="File: ", font=("Arial", 12, "bold"))
    # file_path.grid(column=0, row=0, columnspan=1)
    # load_file.grid(column=2, row=0)

    # content.grid(column=0, row=0)
    # table_frame.grid(column=1, row=1)
    content.pack()
    mainloop()    

if __name__ == '__main__':
    main()