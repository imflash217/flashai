#include <iostream>

/*
 * author = @imflash217
 * copyright = flashAI, @2019
 */

int main(){
    // prompt user tto input two numbers
    std::cout << "Enter two numbers" << std::endl;
    
    // variables to store values
    int v1 = 0;
    int v2 = 0;

    // read input
    std::cin >> v1 >> v2;

    //std::cout << "The sum of " << v1 << " and " << v2 << " is " << v1 + v2 << std::endl;
    std::cout << v1 << " + " << v2 << " = " << v1+v2 << std::endl;
    
    return 0;
}
