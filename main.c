#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

void arr_p(int* arr, int len)
{
	printf("[");
	for (int i = 0; i < len; i++)
	{
		printf("0x%X(%d)", &arr[i], arr[i]);
		if (i < len - 1) { printf(", "); }
		else { printf("]\n"); }
	}
}

int main()
{
	int arr1[6] = { 0, 1, 2, 3, 4, 5};
	arr_p(arr1, 6);
	printf("arr1=0x%X &arr1=0x%X \n", arr1, &arr1);
	printf("(&arr1)[0]=0x%X &((&arr1)[0][0])=0x%X &((&arr1)[0][1])=0x%X \n", (&arr1)[0], &((&arr1)[0][0]), &((&arr1)[0][1]));
	printf("(&arr1)[1]=0x%X &((&arr1)[1][0])=0x%X &((&arr1)[1][1])=0x%X \n", (&arr1)[1], &((&arr1)[1][0]), &((&arr1)[1][1]));

	int **parr1 = &arr1;
	printf("parr1[0]=0x%X parr1[1]=0x%X \n", parr1[0], parr1[1]);


	int arr2[2][3] = { {0,1,2}, {3,4,5} };
	arr_p(arr2, 6);
	printf("arr2=0x%X &arr2=0x%X \n", arr2, &arr2);
	printf("arr2[0]=0x%X &arr2[0]=0x%X \n", arr2[0], &arr2[0]);
	printf("arr2[1]=0x%X &arr2[1]=0x%X \n", arr2[1], &arr2[1]);
	printf("arr2[0][0]=0x%X &arr2[0][0]=0x%X \n", arr2[0][0], &arr2[0][0]);
	printf("arr2[1][0]=0x%X &arr2[1][0]=0x%X \n", arr2[1][0], &arr2[1][0]);
	int *parr3 = (int*)malloc(3 * sizeof(int));
	parr3[0] = 0; parr3[1] = 1; parr3[2] = 2;
	int* parr4 = (int*)malloc(6 * sizeof(int));

}
