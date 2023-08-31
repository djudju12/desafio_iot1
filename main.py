from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import numpy as np
from io import StringIO
import matplotlib.pyplot as plt

W, H = 800, 350

class Table:
    def __init__(self, frame) -> None:
        self.internal_frame = Frame(frame)
        self.values = None
        self.tree = None
        self.path = None

    def _get_content(self):
        with filedialog.askopenfile() as f:
            self.path = f.name
            d = StringIO(f.read())
            content = np.loadtxt(d, delimiter=",")
        
        return content
    
    def get_path(self):
        return self.path

    def show(self) -> None:
        self.values = self._get_content()
        if len(self.values) == 0:
            return 
        
        scrolly = Scrollbar(self.internal_frame)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx = Scrollbar(self.internal_frame,orient='horizontal')
        scrollx.pack(side=BOTTOM, fill=X)

        self.tree = ttk.Treeview(self.internal_frame, yscrollcommand=scrolly.set, xscrollcommand=scrollx.set, selectmode="none", height=200)

        scrolly.config(command=self.tree.yview)
        scrollx.config(command=self.tree.xview)
        
        self.tree.column("#0", width=0,  stretch=NO)
        self.tree['columns'] = [str(i) for i in range(len(self.values[0]))]
        for i, _ in enumerate(self.values[0]):
            self.tree.column(str(i), anchor=CENTER,width=30, stretch=False)    
        
        for i, row in enumerate(self.values):
            self.tree.insert(parent='', index='end', iid=i,  text='', values=row.tolist())

        self.tree.pack()
        self.internal_frame.place(x=W/2, y=0, relheight=1, relwidth=1, anchor='n')

    def avg(self):
        return np.average(self.values)
    
    def std(self):
        return np.std(self.values)
    
    def summ(self):
        return np.sum(self.values)

    def sum_line(self, line):
        return np.sum(self.values[line])

    def sum_column(self, column):
        return np.sum(self.values[:, column])
    
    def avg_line(self, line):
        return np.average(self.values[line])
    
    def avg_column(self, column):
        return np.average(self.values[:, column])
    
    def std_line(self, line):
        return np.std(self.values[line])
    
    def std_column(self, column):
        return np.std(self.values[:, column])


class LabeledPlaceholder:
    def __init__(self, frame, label_text, placeholder) -> None:
        self.label = Label(frame, text=label_text, font=("Courier", 12))
        self.placeholder = Label(frame, font=("Courier", 12), text=placeholder)

    
    def show(self, row, column):
        self.label.grid(row=row, column=column, sticky="w")
        self.placeholder.grid(row=row, column=column+1, sticky="w")

    def set_placeholder(self, text):
        if len(text) > 30:
            text = "..." + text[-30:]
        
        self.placeholder.config(text=text)


class LabeledEntry:
    def __init__(self, frame, label_text, placeholder=None) -> None:
        self.label = Label(frame, text=label_text, font=("Courier", 12))
        self.entry = Entry(frame, font=("Courier", 12), text=placeholder, width=10)

    def show(self, row, column):
        self.label.grid(row=row, column=column, sticky="w")
        self.entry.grid(row=row, column=column+1, sticky="w")


class CalcComponent:
    def __init__(self, frame, label_text) -> None:
        self.entry = LabeledEntry(frame=frame, label_text=label_text)
        self.sum = LabeledPlaceholder(frame=frame, label_text="Sum", placeholder="____")
        self.avg = LabeledPlaceholder(frame=frame, label_text="Avg", placeholder="____")
        self.std = LabeledPlaceholder(frame=frame, label_text="Std", placeholder="____")

    def show(self, row, column):
        self.entry.show(row, column)
        self.sum.show(row, column+2)
        self.avg.show(row, column+4)
        self.std.show(row, 6)
    
    def get_entry(self):
        return self.entry.entry.get()
    
    def set_placeholder(self, s, avg, std):
        self.sum.placeholder.config(text=f"{s:.2f}")
        self.avg.placeholder.config(text=f"{avg:.2f}")
        self.std.placeholder.config(text=f"{std:.2f}")


class MatrixComponent:
    def __init__(self, frame) -> None:
        self.sum = LabeledPlaceholder(frame=frame, label_text="Matrix Sum", placeholder="____")
        self.avg = LabeledPlaceholder(frame=frame, label_text="Avg", placeholder="____")
        self.std = LabeledPlaceholder(frame=frame, label_text="std", placeholder="____")
        

    def show(self, row, column):
        self.sum.show(row, column)
        self.std.show(row, column+2)
        self.avg.show(row, column+4)
    
    def set_placeholder(self, s, avg, std):
        self.sum.placeholder.config(text=f"{s:.2f}")
        self.avg.placeholder.config(text=f"{avg:.2f}")
        self.std.placeholder.config(text=f"{std:.2f}")


def calc(table, line_component: CalcComponent, column_component: CalcComponent, matrix_component: MatrixComponent):
    line = line_component.get_entry()
    column = column_component.get_entry()
    print("line", line)
    print("column", column)
    if line == "" and column == "":
        return
    
    line = int(line)
    column = int(column)

    line_avg, line_std, line_sum = table.avg_line(line), table.std_line(line), table.sum_line(line)
    col_avg, col_std, col_sum = table.avg_line(column), table.std_line(column), table.sum_line(column)

    line_component.set_placeholder(s=line_sum, avg=line_avg, std=line_std)
    column_component.set_placeholder(avg=col_avg, std=col_std, s=col_sum)

    avg, std, s = table.avg(), table.std(), table.summ()
    matrix_component.set_placeholder(avg=avg, std=std, s=s)

def plot_me(table):
    plt.figure(figsize=(8, 8))
    plt.style.use('_mpl-gallery')
    heatmap = plt.imshow(table.values, cmap='viridis')
    plt.subplots_adjust(left=0.15, right=0.85, bottom=0.15, top=0.85)
    plt.colorbar(heatmap)
    plt.show()


def open_file(table, label: Label):
    table.show()
    label.config(text=table.get_path())

def main():
    root = Tk()    
    root.geometry(f"{W}x{H}")

    # Main window
    content = Frame(root)
    content.grid(row=0, column=0)

    # Table 
    table_frame = Frame(content, width=W, height=H-110, border=1, relief="sunken")
    table = Table(table_frame)

    # load 
    load_label = Label(content, text="File :", font=("Courier", 12))
    load_path = Label(content, font=("Courier", 12), text="___________")

    load_button = Button(content, text="Load", font=("Courier", 12), command=lambda:open_file(table, load_path),  width=12)
    
    # Plot
    plot_button = Button(content, text="Plot", font=("Courier", 12), command=lambda:plot_me(table), width=12)

    # Line entry
    line_component = CalcComponent(content, "Line:")

    # Column entry
    column_component = CalcComponent(content, "Column:")

    # Calc button
    calc_button = Button(content, text="Calc", font=("Courier", 12), width=12, command=lambda:calc(table, line_component, column_component, matrix_component))

    # Matrix calculation
    matrix_component = MatrixComponent(content)

    # Putting everithing together
    load_label.grid(row=0, column=0, sticky="w")
    load_path.grid(row=0, column=1, sticky="w", columnspan=7)
    load_button.grid(row=0, column=8, columnspan=2, sticky="e")
    line_component.show(row=2, column=0)
    column_component.show(row=3, column=0)
    matrix_component.show(row=4, column=0)
    plot_button.grid(row=2, column=7,  columnspan=2, sticky="e")
    calc_button.grid(row=4, column=7, columnspan=2, sticky="e")
    table_frame.grid(row=1, column=0, columnspan=9)
    
    # and run
    mainloop()    

if __name__ == '__main__':
    main()