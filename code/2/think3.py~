
#3.1 Error: name 'repeat_lyrics' is not defined

#3.2 Worked!

#3.3

def right_justify(s):
    
    length = len(s)
    pad = 70 - length;    
    for _ in xrange(pad):
        sys.stdout.write(' ');
    print s

right_justify("allen")


#3.4

def do_twice(f, value):
    f(value)
    f(value)

def print_twice(value):
    print value

def do_four(f,value):
    do_twice(f,value)
    do_twice(f,value)

do_four(print_twice,"spam")

#3.5

def draw_edgeRow(col):
	for _ in xrange(col):
		print "+","-","-","-","-",
	print "+"

def draw_middle(col):
	for _ in xrange(4):
		for _ in xrange(col):
			print "|"," "," "," "," ",
		print "|"

def draw_grid(row,col):

	for _ in xrange(row):
		draw_edgeRow(col)
		draw_middle(col)
	draw_edgeRow(col)

	
draw_grid(4,4)

