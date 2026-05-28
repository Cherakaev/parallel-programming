import numpy as np
import sys
import os


def generate_matrices(n, dir_path="data"):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    print(f"Генерация матриц {n}x{n}...")

    A = np.random.rand(n, n).astype(np.float64)
    B = np.random.rand(n, n).astype(np.float64)

    np.savetxt(f"{dir_path}/matrix_A.txt", A, header=str(n), comments='', fmt='%.6f')
    np.savetxt(f"{dir_path}/matrix_B.txt", B, header=str(n), comments='', fmt='%.6f')

    print(f"Матрицы успешно сохранены в папку {dir_path}/")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        N = int(sys.argv[1])
    else:
        N = 200

    generate_matrices(N)