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
#include <string.h>

int main(){
	int scale = 0;
	while (1){
		void* p = malloc((50000+ scale)*sizeof(void));
		memset(p, '0', 50000 + scale);
		if (scale + 100 > 0){
		scale += 100;}
		usleep(500000);
	}
	return 0;
}
