class Solution {
public:
    int aggressiveCows(vector<int>& stalls, int k) {
        sort(stalls.begin(), stalls.end());
        int low = 1;  
        int high = stalls.back() - stalls[0];  
        
        while(left < right) {  
            int mid = left + (right - left + 1) / 2;  
            
            if(canPlaceCows(stalls, k, mid)) {
                left = mid;  
            } else {
                right = mid - 1;  
            }
        }
        return left;
    }
    
    bool canPlaceCows(vector<int>& stalls, int k, int minDist) {
        int cows = 1;
        int lastPos = stalls[0];
        
        for(int i = 1; i < stalls.size(); i++) {
            if(stalls[i] - lastPos >= minDist) {
                cows++;
                lastPos = stalls[i];
                if(cows == k) return true;
            }
        }
        return false;
    }
};