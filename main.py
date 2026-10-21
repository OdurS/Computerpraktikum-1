from gap_interface.gap_interface_main import GAPInterface as gap


def main():

        A = [
            [1, 2],
            [3, 4]
        ]

        B = [
            [2, 0],
            [1, 3]
        ]

        result = gap.multiply_matrices(A, B)

        print("Matrixprodukt:")
        print(result)

        det = gap.determinant(A)

        print("Determinante von A:")
        print(det)


if __name__ == "__main__":
    main()
