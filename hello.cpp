#include <vector>
using namespace std;

// Helper function to handle recursion
void generateNumbers(int current, int x, vector<int> &ans) {
    // Base case: stop when current number exceeds x
    if (current > x) {
        return;
    }
    
    // Add the current number to the vector
    ans.push_back(current);
    
    // Recursive call for the next number
    generateNumbers(current + 1, x, ans);
}

vector<int> printNos(int x) {
    vector<int> ans;
    generateNumbers(1, x, ans);
    return ans;
}