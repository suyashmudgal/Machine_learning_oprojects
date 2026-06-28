#include <vector>
#include <stack>
using namespace std;

vector<int> nextGreaterElement(vector<int>& a, int n) {
    vector<int> ans(n, -1);
    stack<int> s;
    for (int i = 0; i < n; i++) {
        while (!s.empty() && a[i] > a[s.top()]) {
            ans[s.top()] = a[i];
            s.pop();
        }
        s.push(i);
    }
    return ans;
}