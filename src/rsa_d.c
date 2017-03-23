#include "rsa.h"
#include <stdint.h>
#include <string.h>
#include <stdio.h>

void	print_mpi(uint16_t *d)
{
	int		i;

	i = -1;
	while (++i < MPI_NUMBER_SIZE)
	{
		printf("%10d", d[i]);
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
	// printf("\nbefore div\n");
	// print_mpi(d);
	while (++i < MPI_NUMBER_SIZE)
	{
		tmp = d[i] & 0x8000;
		d[i] <<= 1;
		d[i] |= (tmp1 >> 15);
		tmp1 = tmp;
	}
	// printf("\nafter div\n");
	// print_mpi(d);
	// printf("\n\n");
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
	do
	{
		mpi_muluu(bufprod, bufmod, bufmod);
		mpi_moduu(bufprod, n);
		memcpy(bufmod, bufprod, MPI_NUMBER_SIZE * 2);
		mpi_div_2(d_buf);
		// print_mpi(d_buf);
	} while (!is_zero(d_buf));
	// Final multiplication with the original M
	mpi_muluu(bufprod, bufmod, m);
	mpi_moduu(bufprod, n);
	memcpy(m, bufprod, MPI_NUMBER_SIZE*2);
}
