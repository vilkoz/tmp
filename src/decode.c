#include "dump.h"

void		decode_blocks(t_list *lst, t_num *nums)
{
	uint16_t	*c;
	t_list		*tmp;

	tmp = lst;
	while (tmp)
	{
		c = (uint16_t *)tmp->content;
		mpi_powm_d(c, nums->d, nums->n);
		tmp = tmp->next;
	}
}

void		decode_rsa(char *name, char *msg_name)
{
	t_num	*nums;
	t_list	*msg;

	nums = read_nums(name);
	msg = read_message(msg_name, DECODE);
	decode_blocks(msg, nums);
	ft_lstiter(msg, print_list);
}
