#include "dump.h"

int		put_usage(void)
{
		printf("usage: ./rsa -e|-d dumped_file file_with_msg\n");
		return (1);
}

int		main(int argc, char **argv)
{
	if (argc != 4)
		return (put_usage());
	if (ft_strcmp(argv[1], "-e") == 0)
		encode_rsa(argv[2], argv[3]);
	else if (ft_strcmp(argv[1], "-d") == 0)
		printf("(placeholder)\n");
		//decode_rsa(argv[2]);
	else
		return (put_usage());
	return (0);
}
