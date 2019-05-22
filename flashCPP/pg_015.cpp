#include <iostream>


int main(){
    int sum = 0;
    int val = 1;

    //read until end-of-file, calculating the runing sum of all values read
    while (std::cin >> val){
        sum += val;
    }
    std::cout << "Total sum = " << std::endl;
    return 0;
}
