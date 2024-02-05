#include <vector>
#include <iostream>
#include <climits>
using namespace std;

bool checkSortedArray(vector<int> a){
    int sum = 0;
    int n = a.size();

    for(int i = 1; i<n; i++){
        if (a[i]<a[i-1]){
            sum += 1;
        }
        else{
            sum = sum;
        }
    }
    return (sum == 0);
}

int main(){
    vector<int>a = {1,2,3,4,5};
    vector<int>b = {2,5,3,72,1};
    cout<<checkSortedArray(a)<<endl;
    cout<<checkSortedArray(b)<<endl;
}

