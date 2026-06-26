#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
public:
    int maximumSum(vector<int>& arr) {
        int n = arr.size();
        if (n == 1) {
            return arr[0];
        }
        
        int max_ending_here = arr[0];                 // bina delete
        int max_ending_here_with_deletion = arr[0];   // ek delete
        int ans = arr[0];
        
        for (int i = 1; i < n; i++) {
           
            int prev_max_ending_here = max_ending_here;
            
            
            max_ending_here = max(arr[i], max_ending_here + arr[i]);
            
            max_ending_here_with_deletion = max(
                max_ending_here_with_deletion + arr[i],
                prev_max_ending_here
            );
            
           
            ans = max(ans, max(max_ending_here, max_ending_here_with_deletion));
        }
        
        return ans;
    }
};