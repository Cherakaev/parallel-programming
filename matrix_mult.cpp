#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>
#include <mpi.h>

using namespace std;

bool readMatrix(const string& filename, vector<double>& matrix, int& n) {
    ifstream file(filename);
    if (!file.is_open()) return false;
    file >> n;
    matrix.resize(n * n);
    for (int i = 0; i < n * n; ++i) file >> matrix[i];
    file.close();
    return true;
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    string fileA = "data/matrix_A.txt";
    string fileB = "data/matrix_B.txt";
    int n = 0;
    vector<double> A, B, C;

    if (rank == 0) {
        if (!readMatrix(fileA, A, n) || !readMatrix(fileB, B, n)) {
            cerr << "Error: Could not read matrices!" << endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        C.resize(n * n, 0.0);
    }

    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (rank != 0) {
        B.resize(n * n);
    }
    MPI_Bcast(B.data(), n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    vector<int> sendcounts(size, 0);
    vector<int> displs(size, 0);
    int remainder = n % size;
    int offset = 0;

    for (int i = 0; i < size; ++i) {
        int local_rows = n / size + (i < remainder ? 1 : 0);
        sendcounts[i] = local_rows * n;
        displs[i] = offset;
        offset += sendcounts[i];
    }

    int local_elements = sendcounts[rank];
    int local_rows = local_elements / n;
    vector<double> local_A(local_elements);
    vector<double> local_C(local_elements, 0.0);

    MPI_Scatterv(rank == 0 ? A.data() : nullptr, sendcounts.data(), displs.data(), MPI_DOUBLE,
                 local_A.data(), local_elements, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    double start_time = 0.0;
    if (rank == 0) {
        start_time = MPI_Wtime();
    }

    for (int i = 0; i < local_rows; ++i) {
        for (int k = 0; k < n; ++k) {
            double a_ik = local_A[i * n + k];
            for (int j = 0; j < n; ++j) {
                local_C[i * n + j] += a_ik * B[k * n + j];
            }
        }
    }

    MPI_Gatherv(local_C.data(), local_elements, MPI_DOUBLE,
                rank == 0 ? C.data() : nullptr, sendcounts.data(), displs.data(), MPI_DOUBLE,
                0, MPI_COMM_WORLD);

    if (rank == 0) {
        double end_time = MPI_Wtime();
        double duration = end_time - start_time;

        double gflops = (2.0 * static_cast<double>(n) * n * n) / 1e9;
        double perf = gflops / duration;

        cout << "N: " << n << " | Procs: " << size 
             << " | Time: " << duration << "s | Perf: " << perf << " GFLOP/s" << endl;

        ofstream csv("experiment_results.csv", ios::app);
        csv << n << "," << size << "," << duration << "," << perf << "\n";
        csv.close();

        ofstream resFile("data/matrix_C.txt");
        resFile << n << "\n";
        for (int i = 0; i < n * n; ++i) {
            resFile << fixed << setprecision(6) << C[i] << ((i + 1) % n == 0 ? "\n" : " ");
        }
        resFile.close();
    }

    MPI_Finalize();
    return 0;
}