vpath %.c src
vpath %.h include
objects=hello.o main.o

hello: $(objects)
	gcc $^ -o $@
	rm $(objects)

hello.o: hello.c
	gcc -c $< -o $@

main.o: main.c
	gcc -c $< -o $@

clean:
	rm hello
