#include <iostream>
#include <string>

extern "C" {
   void __collier_init_MOD_getversionnumber_cll(char[5]);
}

namespace collier {

std::string collier_get_version()
{
   char version[6] = "";
   __collier_init_MOD_getversionnumber_cll(version);
   version[5] = '\0';

   return version;
}

} // namespace collier

int main()
{
   std::cout << "COLLIER (version " << collier::collier_get_version() << ")"
             << std::endl;

   return 0;
}
