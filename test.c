#include "dump.h"
/* #define SMALLNUMS */
#define BIGNUMS

int		is_even(uint16_t *d_buf)
{
	int		i;

	i = -1;
	while (++i < MPI_NUMBER_SIZE)
	{
		if (d_buf[i] % 2 == 1)
			return (0);
	}
	return (1);
}

void	mpi_powm_d2(uint16_t *m, const uint16_t *d, const uint16_t *n)
{
	uint16_t	bufprod[MPI_NUMBER_SIZE * 2]; // Squaring buffer, double size
	uint16_t	resbufprod[MPI_NUMBER_SIZE * 2]; // Squaring buffer, double size
	uint16_t	bufmod[MPI_NUMBER_SIZE]; // Modulo buffer, single size
	uint16_t	d_buf[MPI_NUMBER_SIZE];
	uint16_t	res[MPI_NUMBER_SIZE];

	memcpy(bufmod, m, MPI_NUMBER_SIZE * 2);
	memcpy(d_buf, d, MPI_NUMBER_SIZE);
	bzero((void*)res, MPI_NUMBER_SIZE * sizeof(uint16_t));
	res[MPI_NUMBER_SIZE - 1] = 1;
	while (!is_zero(d_buf))
	{
		if (!is_even(d_buf))
		{
			mpi_muluu(resbufprod, res, bufmod);
			mpi_moduu(resbufprod, n);
			memcpy(res, resbufprod, MPI_NUMBER_SIZE * 2);
		}
		mpi_div_2(d_buf);
		mpi_muluu(bufprod, bufmod, bufmod);
		mpi_moduu(bufprod, n);
		memcpy(bufmod, bufprod, MPI_NUMBER_SIZE * 2);
		/* print_mpi(d_buf); */
	}
	// Final multiplication with the original M
	/* mpi_muluu(bufprod, bufmod, m); */
	/* mpi_moduu(bufprod, n); */
	memcpy(m, res, MPI_NUMBER_SIZE*2);
}

void	print_shit(const uint16_t *m)
{
	int		i;

	i = -1;
	while (++i < MPI_NUMBER_SIZE)
	{
		printf("%x ", m[i]);
	}
	printf("\n");
}

#define WIDTH 16

void	print_dsize(const uint16_t *m)
{
	int		i;
	int		j;

	i = -1;
	j = WIDTH;
	while (++i < MPI_NUMBER_SIZE)
	{
		j--;
		printf("%04x ", (m[i]));
		if (j == 0)
		{
			j = WIDTH;
			printf("\n");
		}
	}
	printf("\n");
}

void	print_res(const uint16_t *m)
{
	int		i;
	int		j;

	i = -1;
	j = WIDTH;
	while (++i < MPI_NUMBER_SIZE)
	{
		j--;
		printf("%04x ", rev_endian(m[i]));
		if (j == 0)
		{
			j = WIDTH;
			printf("\n");
		}
	}
	printf("\n");
}

int			main(void)
{
	uint16_t	m[MPI_NUMBER_SIZE * 2];
#ifdef SMALLNUMS
	uint16_t	d[MPI_NUMBER_SIZE];
	uint16_t	n[MPI_NUMBER_SIZE * 2];

#endif
	bzero((void*)m, MPI_NUMBER_SIZE * 2 * sizeof(uint16_t));
	m[MPI_NUMBER_SIZE - 1] = rev_endian(0x6765);
	m[MPI_NUMBER_SIZE - 2] = rev_endian(0x7361);
	m[MPI_NUMBER_SIZE - 3] = rev_endian(0x6573);
	m[MPI_NUMBER_SIZE - 4] = rev_endian(0x5f6d);
	m[MPI_NUMBER_SIZE - 5] = rev_endian(0x7374);
	m[MPI_NUMBER_SIZE - 6] = rev_endian(0x7465);
	/* m[MPI_NUMBER_SIZE - 1] = (0x6765); */
	/* m[MPI_NUMBER_SIZE - 2] = (0x7361); */
	/* m[MPI_NUMBER_SIZE - 3] = (0x6573); */
	/* m[MPI_NUMBER_SIZE - 4] = (0x5f6d); */
	/* m[MPI_NUMBER_SIZE - 5] = (0x7374); */
	/* m[MPI_NUMBER_SIZE - 6] = (0x7465); */
#ifdef SMALLNUMS
	bzero((void*)n, MPI_NUMBER_SIZE * sizeof(uint16_t));
	bzero((void*)d, MPI_NUMBER_SIZE * sizeof(uint16_t));

	d[MPI_NUMBER_SIZE - 1] = rev_endian(0x84fb);
	d[MPI_NUMBER_SIZE - 2] = rev_endian(0x8f1f);
	d[MPI_NUMBER_SIZE - 3] = rev_endian(0x4b);

	n[MPI_NUMBER_SIZE * 2 - 1] = rev_endian(0xddb2);
	n[MPI_NUMBER_SIZE * 2 - 2] = rev_endian(0x1df1);
	n[MPI_NUMBER_SIZE * 2 - 3] = rev_endian(0xc8);

	printf("\nm =\n");
	print_shit(m);
	printf("\n");
	print_mpi(m);
	printf("\nn =\n");
	print_shit(n);
	printf("\n");
	print_mpi(n);
	printf("\n");
	/* mpi_powm_d2(m, d, n); */
	/* printf("%x%x%x\n",m[MPI_NUMBER_SIZE - 3], m[MPI_NUMBER_SIZE - 2], m[MPI_NUMBER_SIZE - 1]); */
	/* printf("%x%x%x\n",m[0], m[1], m[2]); */
	/* print_mpi(m); */
	mpi_powm65537(n, m);
	/* printf("%x%x%x\n",m[0], m[1], m[2]); */
	printf("res:\n");
	print_mpi(m);
	print_shit(m);
	printf("print_res res\n");
	print_res(m);
	/* printf("n:\n"); */
	/* print_mpi(n); */
	/* print_shit(n); */
#endif
#ifdef BIGNUMS
	t_num	*nums;

	nums = read_nums("numbers.txt");
	printf("m\n");
	/* print_mpi(m); */
	/* print_shit(m); */
	print_dsize(m);
	printf("n\n");
	print_dsize(nums->n);
	mpi_powm65537(m, nums->n);
	printf("\nres\n");
	print_dsize(m);
	/* printf("\nd\n"); */
	/* print_dsize(nums->d); */
#endif
}
