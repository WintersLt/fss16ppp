# Answers for HW2

## Active Shooter Exercise
####List two things not to do during an active shooter event.
- Do not panic
- Do not stop calling Emergency services even if the lines are jammed.

####List two things best to do during an active shooter event.
- Leave belongings behind and find a safer place to hide.
- Avoid places that trap or restrict movement.


## 3.1
Error: name 'repeat_lyrics' is not defined

## 3.2
The code works.

## 3.3
```python
def right_justify(s):
    
    length = len(s)
    pad = 70 - length;    
    for _ in xrange(pad):
        sys.stdout.write(' ');
    print s

right_justify("allen")
```

## 3.4
```python
def do_twice(f, value):
    f(value)
    f(value)

def print_twice(value):
    print value

def do_four(f,value):
    do_twice(f,value)
    do_twice(f,value)

do_four(print_twice,"spam")
```

## 3.5
```python
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
```

## 4.2
Screenshot for Exercise 4.2
[![Exercise4.2](https://github.com/WintersLt/fss16ppp/blob/master/code/2/think4%5C_2.png)](#Exercise4.2)

## 4.3
The output screenshot of exercise 4.3
[![Exercise4.3](https://github.com/WintersLt/fss16ppp/blob/master/code/2/think4%5C_3.png)](#Exercise4.3) 
