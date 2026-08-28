#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>
#include <cuda_runtime.h>

using namespace std;

__global__ void matrixMulKernel(const double* A, const double* B, double* C, int n) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < n && col < n) {
        double sum = 0.0;
        for (int k = 0; k < n; ++k) {
            sum += A[row * n + k] * B[k * n + col];
        }
        C[row * n + col] = sum;
    }
}

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
    vector<double> h_A, h_B, h_C;

    int block_size = 16;
    if (argc > 1) {
        block_size = stoi(argv[1]);
    }

    if (!readMatrix(fileA, h_A, n) || !readMatrix(fileB, h_B, n)) {
        cerr << "Error: Could not read matrices!" << endl;
        return 1;
    }

    h_C.resize(n * n, 0.0);
    size_t bytes = n * n * sizeof(double);

    double *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, bytes);
    cudaMalloc(&d_B, bytes);
    cudaMalloc(&d_C, bytes);

    cudaMemcpy(d_A, h_A.data(), bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B.data(), bytes, cudaMemcpyHostToDevice);

    dim3 threadsPerBlock(block_size, block_size);
    dim3 blocksPerGrid((n + block_size - 1) / block_size, (n + block_size - 1) / block_size);

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    cudaEventRecord(start);
    matrixMulKernel<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, n);
    cudaEventRecord(stop);
    
    cudaEventSynchronize(stop);

    float kernelTimeMs = 0;
    cudaEventElapsedTime(&kernelTimeMs, start, stop);
    double duration = kernelTimeMs / 1000.0;

    cudaMemcpy(h_C.data(), d_C, bytes, cudaMemcpyDeviceToHost);

    double gflops = (2.0 * static_cast<double>(n) * n * n) / 1e9;
    double perf = gflops / duration;

    cout << "N: " << n << " | Block: " << block_size << "x" << block_size 
         << " | Time: " << duration << "s | Perf: " << perf << " GFLOP/s" << endl;

    ofstream csv("experiment_results.csv", ios::app);
    csv << n << "," << block_size << "," << duration << "," << perf << "\n";
    csv.close();

    ofstream resFile("data/matrix_C.txt");
    resFile << n << "\n";
    for (int i = 0; i < n * n; ++i) {
        resFile << fixed << setprecision(6) << h_C[i] << ((i + 1) % n == 0 ? "\n" : " ");
    }
    resFile.close();

    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);

    return 0;
}