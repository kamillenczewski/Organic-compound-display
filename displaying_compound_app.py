from tkinter import mainloop, Tk

MASTER = Tk()

from labelsmatrixbuilder import LabelsMatrixBuilder
from interpreting import interpret_compound_name

# Examples:
# 1,2,3-tribromo-1,4-dichloro-2,3-etyloheksan
# 1,2,3-tribromoheksan
# 2,2-dibromoheks-5-en
# 7-propylo-9-propylo-10,1-dipentylo-2,2-chloro-6,6,8-dimetylodekan
# 1-metylo-10,5-diheksylo-9-etylo-6,7,2-tribromo-3-nonylo-8-propylodekan
# 2,5-dibromo-10,6-dipropylo-8-metylo-5-etylo-2-butylo-3-chlorodekan

# Program limitations:
#   - element groups: bromo, chloro
#   - methyl groups: metylo <---> nonylo
#   - number prefixes: di, tri, tetra, penta

# Temporary:
#   - program ignores bound index and suffix of main alkane
#   - program can not work

def main():
    name = '5,1-dibutylo-1-etylo-4-bromo-10,1,10-trichloro-7,3-dimetylodekan'

    tags_matrix = interpret_compound_name(name)

    displaying_matrix = LabelsMatrixBuilder(MASTER, tags_matrix).build()

    mainloop()

if __name__ == '__main__':
    main()