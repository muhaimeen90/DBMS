#include<bits/stdc++.h>
#include<omp.h>
using namespace std;

int main(){

    const int rows = 10000;
    const int cols = 2;
    vector<vector<int>> array1(rows, vector<int>(cols));
    vector<vector<int>> array2(rows, vector<int>(cols));

    srand(time(0));

    for(int i = 0; i < rows; ++i) {
        array1[i][0] = rand() % 100000 + 1;
        array2[i][0] = rand() % 100000 + 1;
        array1[i][1] = 'a' + rand() % 3;
        array2[i][1] = 'd' + rand() % 3;
    }
    ofstream file1("/home/bsse1423/bsse1423/Sem5/DBMS-2/1423/array1.txt");
    ofstream file2("/home/bsse1423/bsse1423/Sem5/DBMS-2/1423/array2.txt");

    for(int i = 0; i < rows; ++i) {
        file1 << array1[i][0] << " " << static_cast<char>(array1[i][1]) << endl;
        file2 << array2[i][0] << " " << static_cast<char>(array2[i][1]) << endl;
    }

    file1.close();
    file2.close();
    vector<vector<int>> array3(rows, vector<int>(3));
    // #pragma omp parallel for shared(array1, array2, array3)
    // for(int i=0; i<rows; i++){
    //     for(int j=0; j<rows/4; j++){
    //         if(array1[i][0]==array2[j][0]){
    //             array3[i][0] = array1[i][0];
    //             array3[i][1] = array1[i][1];
    //             array3[i][2] = array2[j][1];
    //         }
    //     }
    //     for(int j=rows/4; j<rows/2; j++){
    //         if(array1[i][0]==array2[j][0]){
    //             array3[i][0] = array1[i][0];
    //             array3[i][1] = array1[i][1];
    //             array3[i][2] = array2[j][1];
    //         }
    //     }
    //     for(int j=rows/2; j<3*rows/4; j++){
    //         if(array1[i][0]==array2[j][0]){
    //             array3[i][0] = array1[i][0];
    //             array3[i][1] = array1[i][1];
    //             array3[i][2] = array2[j][1];
    //         }

    //     }
    //     for(int j=3*rows/4; j<rows; j++){
    //         if(array1[i][0]==array2[j][0]){
    //             array3[i][0] = array1[i][0];
    //             array3[i][1] = array1[i][1];
    //             array3[i][2] = array2[j][1];
    //         }

    //     }

    // }
    #pragma omp parallel sections
    {
        #pragma omp section
        {
            for(int i=0; i<rows/4; i++){
                for(int j=0; j<rows; j++){
                    if(array1[i][0]==array2[j][0]){
                        array3[i][0] = array1[i][0];
                        array3[i][1] = array1[i][1];
                        array3[i][2] = array2[j][1];
                    }
                }
            }
        }
        #pragma omp section
        {
            for(int i=rows/4; i<rows/2; i++){
                for(int j=0; j<rows; j++){
                    if(array1[i][0]==array2[j][0]){
                        array3[i][0] = array1[i][0];
                        array3[i][1] = array1[i][1];
                        array3[i][2] = array2[j][1];
                    }
                }
            }
        }
        #pragma omp section
        {
            for(int i=rows/2; i<3*rows/4; i++){
                for(int j=0; j<rows; j++){
                    if(array1[i][0]==array2[j][0]){
                        array3[i][0] = array1[i][0];
                        array3[i][1] = array1[i][1];
                        array3[i][2] = array2[j][1];
                    }
                }
            }
        }
        #pragma omp section
        {
            for(int i=3*rows/4; i<rows; i++){
                for(int j=0; j<rows; j++){
                    if(array1[i][0]==array2[j][0]){
                        array3[i][0] = array1[i][0];
                        array3[i][1] = array1[i][1];
                        array3[i][2] = array2[j][1];
                    }
                }
            }
        }
    }
    ofstream file3("/home/bsse1423/bsse1423/Sem5/DBMS-2/1423/array3.txt");

    for(int i = 0; i < rows; ++i) {
        if(array3[i][0] != 0) { // Assuming 0 is not a valid value and indicates no match
            file3 << array3[i][0] << " " << static_cast<char>(array3[i][1]) << " " << static_cast<char>(array3[i][2]) << endl;
        }
    }

    file3.close();
}