import numpy as np
import os

def verify(dir_path="data"):
    file_a = f"{dir_path}/matrix_A.txt"
    file_b = f"{dir_path}/matrix_B.txt"
    file_c = f"{dir_path}/matrix_C.txt"

    if not (os.path.exists(file_a) and os.path.exists(file_b) and os.path.exists(file_c)):
        print("Ошибка: Не найдены файлы матриц. Сначала запустите генератор и C++ программу.")
        return

    print("Чтение матриц для верификации...")
    A = np.loadtxt(file_a, skiprows=1)
    B = np.loadtxt(file_b, skiprows=1)
    C_cpp = np.loadtxt(file_c, skiprows=1)

    print("Вычисление эталонного результата (NumPy)...")
    C_ref = A @ B

    print("Сравнение результатов...")
    if np.allclose(C_ref, C_cpp, atol=1e-4):
        print("✅ УСПЕХ: Результат работы C++ программы полностью СОВПАДАЕТ с эталонным!")
    else:
        print("❌ ОШИБКА: Результат работы C++ программы НЕ СОВПАДАЕТ с эталонным!")
        max_diff = np.max(np.abs(C_ref - C_cpp))
        print(f"Максимальная разность элементов: {max_diff}")

if __name__ == "__main__":
    verify()
