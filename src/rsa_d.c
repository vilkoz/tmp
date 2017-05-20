#include "rsa.h"
#include <stdint.h>
#include <string.h>
#include <stdio.h>

#define BYTE_TO_BINARY_PATTERN "%c%c%c%c%c%c%c%c"
#define BYTE_TO_BINARY(byte)  \
  ((byte) & 0x80 ? '1' : '0'), \
  ((byte) & 0x40 ? '1' : '0'), \
  ((byte) & 0x20 ? '1' : '0'), \
  ((byte) & 0x10 ? '1' : '0'), \
  ((byte) & 0x08 ? '1' : '0'), \
  ((byte) & 0x04 ? '1' : '0'), \
  ((byte) & 0x02 ? '1' : '0'), \
  ((byte) & 0x01 ? '1' : '0') 

void	print_mpi(uint16_t *d)
{
	int		i;

	i = -1;
	while (++i < MPI_NUMBER_SIZE)
	{
		/* printf(BYTE_TO_BINARY_PATTERN, BYTE_TO_BINARY((char)((d[i] >> 24) & 0xff))); */
		/* printf(" "); */
		/* printf(BYTE_TO_BINARY_PATTERN, BYTE_TO_BINARY((char)((d[i] >> 16) & 0xff))); */
		/* printf(" "); */
		printf(BYTE_TO_BINARY_PATTERN, BYTE_TO_BINARY((char)((d[i] >> 8) & 0xff)));
		printf(" ");
		printf(BYTE_TO_BINARY_PATTERN, BYTE_TO_BINARY((char)((d[i] >> 0) & 0xff)));
		printf("  ");
	}
	printf("\n");
}

void	mpi_div_2(uint16_t *d)
{
	uint16_t	tmp;
	uint16_t	tmp1;
	int			i;

	i = -1;
	tmp = 0;
	/* printf("\nbefore div\n"); */
	/* print_mpi(d); */
	while (++i < MPI_NUMBER_SIZE)
	{
		tmp = d[i] & 0x8000;
		d[i] <<= 1;
		d[i] |= (tmp1 >> 15);
		tmp1 = tmp;
	}
	/* printf("\nafter div\n"); */
	/* print_mpi(d); */
	/* printf("\n\n"); */
}

int		is_zero(uint16_t *d_buf)
{
	int		i;

	i = -1;
	while (++i < MPI_NUMBER_SIZE)
	{
		if (d_buf[i] != 0)
			return (0);
	}
	return (1);
}

void	mpi_powm_d(uint16_t *m, const uint16_t *d, const uint16_t *n)
{
	uint16_t	bufprod[MPI_NUMBER_SIZE * 2]; // Squaring buffer, double size
	uint16_t	bufmod[MPI_NUMBER_SIZE]; // Modulo buffer, single size
	uint16_t	d_buf[MPI_NUMBER_SIZE];

	memcpy(bufmod, m, MPI_NUMBER_SIZE * 2);
	memcpy(d_buf, d, MPI_NUMBER_SIZE);
	while (!is_zero(d_buf))
	{
		mpi_muluu(bufprod, bufmod, bufmod);
		mpi_moduu(bufprod, n);
		memcpy(bufmod, bufprod, MPI_NUMBER_SIZE * 2);
		print_mpi(bufmod);
		mpi_div_2(d_buf);
		/* print_mpi(d_buf); */
	}
	// Final multiplication with the original M
	mpi_muluu(bufprod, bufmod, m);
	mpi_moduu(bufprod, n);
	memcpy(m, bufprod, MPI_NUMBER_SIZE*2);
}
