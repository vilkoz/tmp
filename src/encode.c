#include "dump.h"

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
	return ((octet1 << 4) | octet2);
}

int			fill_num(t_num *nums, char *line)
{
	uint16_t	*tmp;
	uint8_t		*num;
	char		*pos;
	int			size;
	int			i;

	size = ft_atoi(ft_strchr(line, '(') + 1);
	tmp = (uint16_t *)malloc(size / 8);
	num = (uint8_t *)malloc(size / 8);
	pos = ft_strchr(line, '-');
	i = 0;
	while ((pos = ft_strchr(pos, ' ') + 1)[0] != '\0')
	{
		num[i] = byte_from_hex(pos);
		printf("byte = %2x, pos = %c%c\n", num[i], pos[0], pos[1]);
		i++;
	}
	i = -1;
	while (++i < size / 16)
	{
		tmp[i] = ((num[i * 2] << 8) | num[i * 2 + 1]);
		printf("tmp = %4x, pos = %2x%2x\n", tmp[i], num[i * 2], num[i * 2 + 1]);
	}
	if (choose_pointer(nums, line[0], tmp) == 1)
		return (1);
}

t_num	*read_nums(char *name)
{
	t_num	*nums;
	int		fd;
	char	*line;

	if ((fd = open(name, O_RDONLY)) == -1)
	{
		perror (name);
		return (NULL);
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

void	encode_rsa(char *name)
{
	t_num	*nums;

	nums = read_nums(name);
}
