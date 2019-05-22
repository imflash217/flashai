#include <iostream>

/*
 * author = @imflash217
 * copyright = @flashAI, 2019
 * Description : "Writing a program to sum the number from 1 to 10"
 */

int main(){
    int sum = 0;
    int val = 1;

    while (val <= 10){
        sum += val;
        ++val;
    }
    std::cout << "Total sum = " << sum << std::endl;

    return 0;
}
