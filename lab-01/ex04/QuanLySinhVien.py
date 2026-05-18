from SinhVien import SinhVien

class QuanLySinhVien:
    def __init__(self):
        self.listSinhVien = []
        self._next_id = 1

    def soLuongSinhVien(self):
        return len(self.listSinhVien)

    def themSinhVien(self):
        name = input("Nhap ten: ")
        sex = input("Nhap gioi tinh: ")
        major = input("Nhap chuyen nganh: ")
        try:
            diemTB = float(input("Nhap diem trung binh: "))
        except Exception:
            diemTB = 0.0
        sv = SinhVien(self._next_id, name, sex, major, diemTB)
        self.xepLoaiHocLuc(sv)
        self.listSinhVien.append(sv)
        self._next_id += 1
        print("Da them sinh vien.")

    def updateSinhVien(self, ID):
        sv = self.findByID(ID)
        if sv is None:
            print("Sinh vien co ID = {} khong ton tai.".format(ID))
            return False
        print("Nhap thong tin moi (bo trong de giu nguyen):")
        name = input(f"Ten [{sv._name}]: ") or sv._name
        sex = input(f"Gioi tinh [{sv._sex}]: ") or sv._sex
        major = input(f"Chuyen nganh [{sv._major}]: ") or sv._major
        diem_input = input(f"Diem TB [{sv._diemTB}]: ")
        try:
            diemTB = float(diem_input) if diem_input.strip() != "" else sv._diemTB
        except Exception:
            diemTB = sv._diemTB
        sv._name = name
        sv._sex = sex
        sv._major = major
        sv._diemTB = diemTB
        self.xepLoaiHocLuc(sv)
        print("Da cap nhat sinh vien.")
        return True

    def deleteById(self, ID):
        sv = self.findByID(ID)
        if sv:
            self.listSinhVien.remove(sv)
            return True
        return False

    def findByID(self, ID):
        for sv in self.listSinhVien:
            if sv._id == ID:
                return sv
        return None

    def findByName(self, keyword):
        listSV = []
        for sv in self.listSinhVien:
            if keyword.upper() in sv._name.upper():
                listSV.append(sv)
        return listSV

    def sortByID(self):
        self.listSinhVien.sort(key=lambda x: x._id, reverse=False)

    def sortByName(self):
        self.listSinhVien.sort(key=lambda x: x._name, reverse=False)

    def sortByDiemTB(self):
        self.listSinhVien.sort(key=lambda x: x._diemTB, reverse=False)

    def xepLoaiHocLuc(self, sv: SinhVien):
        if sv._diemTB >= 8:
            sv._hocLuc = "Gioi"
        elif sv._diemTB >= 6.5:
            sv._hocLuc = "Kha"
        elif sv._diemTB >= 5:
            sv._hocLuc = "Trung binh"
        else:
            sv._hocLuc = "Yeu"

    def showSinhVien(self, listSV):
        print("{: <8} {:<18} {:<8} {:<15} {:<8} {:<8}".format("ID","Name","Sex","Major","DiemTB","Hoc Luc"))
        if len(listSV) > 0:
            for sv in listSV:
                print("{: <8} {:<18} {:<8} {:<15} {:<8} {:<8}".format(sv._id, sv._name, sv._sex, sv._major, sv._diemTB, sv._hocLuc))
        print("\n")

    def getListSinhVien(self):
        return self.listSinhVien
