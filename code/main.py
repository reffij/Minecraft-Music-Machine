from decoder import decode
from tkinter import filedialog

def main() -> None:
    directory = filedialog.askopenfilename(initialdir='./',filetypes=('.nbs'))
    coordinates_data:list[list[str]] = []
    with open('coordinates.csv', 'r') as f1:
        for line in f1:
            coordinates_data.append(line.split(','))

    info = decode(directory)
    with open("output.txt", 'w') as f2:
        f2.write(info)

if __name__ == '__main__':
    main()
