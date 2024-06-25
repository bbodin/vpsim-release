/*
 * Copyright (C) 2024 Commissariat à l'énergie atomique et aux énergies alternatives (CEA)

 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at

 *    http://www.apache.org/licenses/LICENSE-2.0 

 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <string.h>
#include <iostream>

#include "sesamController.hpp"

using namespace std;

void usage(){
  printf("Sesam user controller\n");
  printf("v0.0.2\n");
  printf("Usage: sesam <command> <parameter>\n");
  printf("\nCommand:\n");
  printf("    help\t\tShow this message\n");
  printf("    show\t\tShow component status\n");
  printf("    benchmark\t\tShow performance statistics of the executed program\n");
  printf("    quit\t\tQuit VPSim\n");
}

int main(int argc, char **argv)
{
  char cmd[20];
  char parameter[10][30]; /* Maximum 10 parameters */
  int nb_param;

  int i;

  if (argc < 2) {
    usage();
    exit(1);
  }

  /* Copy input variables to internal */
  strcpy(cmd, argv[1]);

  map_sesam_mem();

  /* Verify command */
  if (strcmp(cmd,"help") == 0) {
    printf("Help: ");
    usage();
    return 0;
  }
  else if (strcmp(cmd,"quit") == 0) {
    /* Call function to quit vpsim */
    printf("Quitting VPSIM environment ...\n");
    sesam_quit();
  }
  else if (strcmp(cmd,"list") == 0) {
    /* Call function to list vpsim components */
    printf("Components in VPSIM: \n");
    sesam_list_component();
  }
  else if (strcmp(cmd,"benchmark") == 0) {
    if (argc < 3) {
      printf("Please put your benchmark application...");
      printf("Usage: sesam benchmark <name_of_application>");
      exit(1);
    }

    ostringstream s;

    string tmp = argv[2];
    if (tmp.substr(tmp.find_last_of(".") + 1) == "out"){
        for (i = 3; i < argc; ++i)
            s << argv[i] << " ";
    } else {
        for (i = 2; i < argc; ++i)
            s << argv[i] << " ";
    }

    size_t pos = tmp.find("./");
    if (pos != string::npos){
      tmp = tmp.substr(pos+2);
    }
    int n = tmp.length();
    char name[n+1];
    strcpy(name,tmp.c_str());
    sesam_get_name(n, name);


    sesam_start_bench();
    system(s.str().c_str());
    sesam_end_bench();
  }
  else {
    if (argc < 3) {
      printf("Missing argument: ");
      usage();
      exit(1);
    }

    /* Get argument */
    nb_param = argc - 1;
    for (i = 0; i < nb_param; ++i) {
      strcpy(parameter[i],argv[i+1]);
    }

    sesam_exec_command(nb_param, parameter);

  }

  unmap_sesam();

  return 0;
}
