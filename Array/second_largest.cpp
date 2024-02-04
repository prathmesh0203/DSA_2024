#include <vector>
#include <iostream>
#include <climits>
using namespace std;

vector<int> getSecondOrderElements(int n, vector<int> a) {
    int max_element = a[0];
    int min_element = a[0];

    for(int i=1; i<n; i++){
        if (a[i]> max_element){
            max_element = a[i];
        }

        if (a[i]< min_element){
            min_element = a[i];
        }

    }

    int pre_max = INT_MIN;
    int pre_min = INT_MAX;

    for (int i=0; i<n; i++){
        if (a[i] > pre_max && a[i] < max_element){
            pre_max = a[i];
        }

        if (a[i]< pre_min && a[i]> min_element){
            pre_min = a[i];
        }

    }

    vector<int> result;
    result.push_back(pre_max);
    result.push_back(pre_min);

    return result;

}

int main() {
    int n = 5;
    vector<int> a = {1, 2, 3, 4, 5};

    vector<int> result = getSecondOrderElements(n, a);
    cout << result[0] << " " << result[1] << endl;
    return 0;
}