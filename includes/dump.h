#ifndef DUMP_H
# define DUMP_H

# include <fcntl.h>
# include <stdio.h>
# include <unistd.h>
# include <stdint.h>
# include <string.h>
# include "../libft/libft.h"

typedef struct		s_num
{
	uint16_t		*n;
	uint16_t		*e;
	uint16_t		*d;
	uint16_t		*p;
	uint16_t		*q;
	uint16_t		*u;
}					t_num;

void				encode_rsa(char *name);
t_num				*read_nums(char *name);

#endif
