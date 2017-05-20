#ifndef DUMP_H
# define DUMP_H

# include <fcntl.h>
# include <stdio.h>
# include <unistd.h>
# include <stdint.h>
# include <string.h>
# include "../libft/libft.h"
# include "rsa.h"

# define ENCODE 1
# define DECODE 2

typedef struct		s_num
{
	uint16_t		*n;
	uint16_t		*e;
	uint16_t		*d;
	uint16_t		*p;
	uint16_t		*q;
	uint16_t		*u;
}					t_num;

/*
** encode.c
*/

void				encode_rsa(char *name, char *msg_name);
t_num				*read_nums(char *name);
t_list				*read_message(char *msg_name, int type);
void				print_list(t_list *lst);
unsigned char		reverse(unsigned char b);
uint16_t			rev_endian(uint16_t a);

/*
** decode_rsa.c
*/

void				decode_rsa(char *name, char *msg_name);

/*
** rsa_d.c
*/

void				print_mpi(uint16_t *d);
int					is_zero(uint16_t *d_buf);
int					is_even(uint16_t *d_buf);
void				mpi_div_2(uint16_t *d);

#endif
