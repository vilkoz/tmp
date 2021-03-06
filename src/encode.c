#include "dump.h"

uint16_t	rev_uint(uint16_t a)
{
	unsigned char	p1;
	unsigned char	p2;
	uint16_t		res;

	p1 = (a >> 8) & 0xff;
	p2 = (a >> 0) & 0xff;
	res = reverse(p2) << 8 | reverse(p1);
	return (res);
}

uint16_t	rev_endian(uint16_t a)
{
	uint16_t b0,b1;
	uint16_t res;

	b0 = (a & 0x00ff) << 8u;
	b1 = (a & 0xff00) >> 8u;
	res = b0 | b1;
	return (res);
}

int			choose_pointer(t_num *nums, char c, uint16_t *tmp)
{
	if (c == 'n')
		nums->n = tmp;
	else if (c == 'e')
		nums->e = tmp;
	else if (c == 'd')
		nums->d = tmp;
	else if (c == 'p')
		nums->p = tmp;
	else if (c == 'q')
		nums->q = tmp;
	else if (c == 'u')
		nums->u = tmp;
	else
		return (1);
	return (0);
}

uint8_t		byte_from_hex(char *pos)
{
	unsigned char	octet1;
	unsigned char	octet2;

	if (ft_isdigit(pos[0]))
		octet1 = pos[0] - '0';
	else
		octet1 = pos[0] - 'a' + 10;
	if (ft_isdigit(pos[1]))
		octet2 = pos[1] - '0';
	else
		octet2 = pos[1] - 'a' + 10;
	return (((octet1 << 4) | octet2));
}

int			fill_num(t_num *nums, char *line)
{
	uint16_t	*tmp;
	uint8_t		*num;
	char		*pos;
	int			size;
	int			i;

	size = ft_atoi(ft_strchr(line, '(') + 1);
	tmp = (uint16_t *)malloc(size / 8 + 1);
	num = (uint8_t *)malloc(size / 8 + 1);
	pos = ft_strchr(line, '-');
	i = 0;
	while ((pos = ft_strchr(pos, ' ') + 1)[0] != '\0')
	{
		num[i] = byte_from_hex(pos);
		i++;
	}
	i = -1;
	while (++i <= size / 16)
	{
		tmp[i] = ((num[i * 2] << 8) | (num[i * 2 + 1]));
		tmp[i] = rev_endian(tmp[i]);
	}
	if (choose_pointer(nums, line[0], tmp) == 1)
		return (1);
	return (0);
}

t_num		*read_nums(char *name)
{
	t_num	*nums;
	int		fd;
	char	*line;

	if ((fd = open(name, O_RDONLY)) == -1)
	{
		perror (name);
		exit (1);
	}
	nums = (t_num*)malloc(sizeof(t_num));
	line = NULL;
	while (get_next_line(fd, &line) > 0)
	{
		if (fill_num(nums, line) == 1)
			return (NULL);
		free (line);
	}
	return (nums);
}

unsigned char	reverse(unsigned char b)
{
	b = (b & 0xF0) >> 4 | (b & 0x0F) << 4;
	b = (b & 0xCC) >> 2 | (b & 0x33) << 2;
	b = (b & 0xAA) >> 1 | (b & 0x55) << 1;
	return b;
}

t_list			*char_to_bytes(t_list *lst)
{
	unsigned char	*tmp;
	uint16_t		*num;
	int				i;
	int				j;

	tmp = lst->content;
	if (tmp == NULL || tmp[0] == '\0')
		return (NULL);
	num = (uint16_t *)malloc(sizeof(uint16_t) * MPI_NUMBER_SIZE);
	if ((i = ft_strlen((char *)tmp)) < 256)
		j = i / 2 - 1;
	else
		j = MPI_NUMBER_SIZE - 1;
	while (--i - 1 >= 0)
		num[i / 2] = (tmp[i]) << 8 | (tmp[i - 1]);
	if (i == 0)
		num[i / 2] = 0 | (tmp[i]);
	while (++j < MPI_NUMBER_SIZE)
		num[j] = 0;
	return (ft_lstnew((void *)num, sizeof(uint16_t) * MPI_NUMBER_SIZE));
}

t_list		*read_message(char *msg_name, int type)
{
	int				fd;
	t_list			*lst;
	unsigned char	buf[256];
	int				i;

	if ((fd = open(msg_name, O_RDONLY)) == -1)
	{
		perror(msg_name);
		exit(1);
	}
	lst = NULL;
	while ((i = read(fd, buf, 256)) > 0)
		ft_lstadd(&lst, ft_lstnew((void *)buf, sizeof(char) * 256));
	if (type == ENCODE)
		return (ft_lstmap(lst, char_to_bytes));
	else
		return (lst);
}

void		encode_blocks(t_list *lst, t_num *nums)
{
	uint16_t	*m;
	t_list		*tmp;

	tmp = lst;
	while (tmp)
	{
		m = (uint16_t *)tmp->content;
		mpi_powm65537(m, nums->n);
		tmp = tmp->next;
	}
}

void		print_list(t_list *lst)
{
	int				i;
	unsigned char	*tmp;

	i = -1;
	tmp = (unsigned char *)lst->content;
	while (++i < (int)lst->content_size)
		printf("%c", tmp[i]);
}

void		encode_rsa(char *name, char *msg_name)
{
	t_num	*nums;
	t_list	*msg;

	nums = read_nums(name);
	msg = read_message(msg_name, ENCODE);
	// ft_lstiter(msg, print_list);
	encode_blocks(msg, nums);
	ft_lstiter(msg, print_list);
}
