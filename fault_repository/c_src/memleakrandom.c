/*
 * =====================================================================================
 *
 *       Filename:  memleak.c
 *
 *    Description:  memmory leak
 *
 *        Version:  1.0
 *        Created:  11/26/2014 03:04:30 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>

int main(){
	while (1){
		int x = rand() % 100;
		if (x > 50){
			void* p = malloc(50000*sizeof(void));
			memset(p, '0', 50000);
		}
		usleep(500000);
	}
	return 0;
}
