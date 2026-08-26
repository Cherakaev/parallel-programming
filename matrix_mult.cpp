#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>
#include <chrono>
#include <omp.h>

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
    string fileA = "data/matrix_A.txt";
    string fileB = "data/matrix_B.txt";
    int n;
    vector<double> A, B, C;

    int num_threads = 4;
    if (argc > 1) {
        num_threads = stoi(argv[1]);
    }
    
    int max_procs = omp_get_num_procs();
    if (num_threads > max_procs) {
        num_threads = max_procs;
    }

    omp_set_num_threads(num_threads);

    if (!readMatrix(fileA, A, n) || !readMatrix(fileB, B, n)) {
        cerr << "Error: Could not read matrices!" << endl;
        return 1;
    }

    C.assign(n * n, 0.0);
    auto start = chrono::high_resolution_clock::now();

    #pragma omp parallel for
    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n; ++k) {
            double a_ik = A[i * n + k];
            for (int j = 0; j < n; ++j) {
                C[i * n + j] += a_ik * B[k * n + j];
            }
        }
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> duration = end - start;

    double gflops = (2.0 * static_cast<double>(n) * n * n) / 1e9;
    double perf = gflops / duration.count();

    cout << "N: " << n << " | Threads: " << num_threads 
         << " | Time: " << duration.count() << "s | Perf: " << perf << " GFLOP/s" << endl;

    ofstream csv("experiment_results.csv", ios::app);
    csv << n << "," << num_threads << "," << duration.count() << "," << perf << "\n";
    csv.close();

    ofstream resFile("data/matrix_C.txt");
    resFile << n << "\n";
    for(int i=0; i<n*n; ++i) resFile << fixed << setprecision(6) << C[i] << ( (i+1)%n==0 ? "\n" : " " );

    return 0;
}