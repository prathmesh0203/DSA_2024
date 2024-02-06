#include<iostream>
#include<vector>
using namespace std;

vector<int> rotateBY1(vector<int>a){
    int n = a.size();
    int temp = a[0];
    for(int i =1;i<n-1;i++){
        a[i-1] = a[i];
    }
    a[n-1] = temp;

    return a;


}   

