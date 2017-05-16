# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: vrybalko <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/11/23 14:08:11 by vrybalko          #+#    #+#              #
#    Updated: 2017/03/23 00:39:26 by vrybalko         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = fast_rsa

IDIR = includes/

VPATH = src:includes

BIN_DIR = bin/

FLAGS = -Wall -Wextra -Werror -I$(IDIR) -g

LIB = libft/libft.a

SRCS = main.c					\
	   encode.c					\
	   rsa.c					\
	   rsa_d.c					\
	   decode.c

BINS = $(addprefix $(BIN_DIR), $(SRCS:.c=.o))

all: $(NAME)

$(NAME): $(BINS)
	make -C libft/
	gcc -o $(NAME) $(BINS) $(FLAGS) $(FLAGS_X11) $(LIB)

$(BIN_DIR)%.o: %.c
	gcc $(FLAGS) -c -o $@ $<

clean:
	make -C libft/ clean
	/bin/rm -f $(BINS)

fclean: clean
	make -C libft/ fclean
	/bin/rm -f $(NAME)

re: fclean all
