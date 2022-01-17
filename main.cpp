#include <iostream>
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <SFML/Window.hpp>
#include <SFML/Audio.hpp>
#include <SFML/Network.hpp>

int main()
{
  std::cout << "Hello world"
            << "\n";

  system("read -n1 -r -p \"Press any key to continue...\"");
  return 0;
}