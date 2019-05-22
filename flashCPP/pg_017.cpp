#include <iostream>

int main(){
    // currVal is the number we're counting, we'll read new values into val
    int currVal = 0;
    int val = 0;

    // read the first number and ensure that we have data to process
    if (std::cin >> currVal){
        int cnt = 1;    // store the count for the current value we're processing
        while (std::cin >> val){    // read the remaining numbers
            if (val == currVal){    // if the vlaues are same
                ++cnt;              // increment the count by 1
            }
            else{                   // otherwise, print the count for previous value
                std::cout << currVal << " occurs " << cnt << " times." << std::endl;
                currVal = val;      // update the new value
                cnt = 1;            // reset the counter
            }
        }
        // remember to print the count for the last value that occurs
        std::cout << currVal << " occurs " << cnt << " times." << std::endl;
    }
    return 0;
}
