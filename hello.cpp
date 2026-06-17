#include<iostream>
using namespace std;

int main()
{
    int arr[] = {5,7,10,12,15};
    int n = sizeof(arr)/sizeof(arr[0]);
    int target = 22;
    int i=0,j=n-1;
    while(i<j)
    {
        if(arr[i]+arr[j]==target)
        {
            cout<<arr[i]<<" "<<arr[j]<<endl;
            i++;
            j--;
        }
        else if(arr[i]+arr[j]>target)
        {
            j--;
        }
        else
        {
            i++;
        }
    }
    return 0;
}

