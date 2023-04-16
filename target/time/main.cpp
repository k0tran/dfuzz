/// This is CLI module for hand-testing class

// std
#include <iostream>

#include "time.hpp"

int main() {
    std::cout << "Enter time in ms" << std::endl << "> ";

    uint ms;
    std::cin >> ms;

    Time t;

    // for exploiting security hole
    t.set(ms);
    
    std::cout << "Time in seconds" << std::endl << t.secs() << std::endl;

    return 0;
}