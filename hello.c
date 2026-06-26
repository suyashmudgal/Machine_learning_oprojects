class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int n = prices.size();
        int maxProfit = 0;  // agar profit nahi hota toh 0 hi return karna hai
        
        // Buy karne ka din
        for (int i = 0; i < n; i++) {
            // Sell karne ka din (i ke baad wala)
            for (int j = i + 1; j < n; j++) {
                int profit = prices[j] - prices[i];
                if (profit > maxProfit) {
                    maxProfit = profit;
                }
            }
        }
        
        return maxProfit;
    }
};