class SinhVien:
    def __init__(self, id, name, sex, major, diemTB):
        self._id = id
        self._name = name
        self._sex = sex
        self._major = major
        self._diemTB = diemTB
        self._hocLuc = ""

    def __str__(self):
        return f"{self._id} - {self._name} - {self._sex} - {self._major} - {self._diemTB} - {self._hocLuc}"
