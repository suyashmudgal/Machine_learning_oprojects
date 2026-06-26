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
            // pehle purana max_ending_here store karo (kyunki baad mein use hoga)
            int prev_max_ending_here = max_ending_here;
            
            // normal Kadane update
            max_ending_here = max(arr[i], max_ending_here + arr[i]);
            
            // with deletion update:
            // option 1: deletion already use karke current add karo
            // option 2: current element ko delete karo (toh sum = prev_max_ending_here)
            max_ending_here_with_deletion = max(
                max_ending_here_with_deletion + arr[i],
                prev_max_ending_here
            );
            
            // answer update
            ans = max(ans, max(max_ending_here, max_ending_here_with_deletion));
        }
        
        return ans;
    }
};