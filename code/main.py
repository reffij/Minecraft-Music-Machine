from decoder import decode
from tkinter import filedialog

def main() -> None:
    directory = filedialog.askopenfilename(initialdir='../nbs_songs',filetypes=[("Notebook files", "*.nbs")])
    info = decode(directory)
    with open("output.txt", 'w') as f2:
        f2.write(info)

if __name__ == '__main__':
    main()
