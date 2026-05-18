def tinh_tong_so_chan(lst):
    tong = 0
    for num in lst:
        if num % 2 == 0:
            tong += num
    return tong


def parse_input(s):
    items = [it.strip() for it in s.split(',') if it.strip() != ""]
    nums = []
    for it in items:
        try:
            nums.append(int(it))
        except ValueError:
            # bỏ qua phần tử không phải số
            pass
    return nums


if __name__ == "__main__":
    s = input("Nhập danh sách các số, cách nhau bằng dấu phẩy: ")
    numbers = parse_input(s)
    tong_chan = tinh_tong_so_chan(numbers)
    print("Tổng các số chẵn trong List là:", tong_chan)
