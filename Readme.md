# Indenter
This is a Code preprocessing tool, written in Python, which allows you to write Code without semicolons and curly brackets i.e. Python like indentation.

### Supported Languages :
- C
- C++
- C#
- Java
- Go-Lang
- Java-Script
- PHP
- and many more...


## Usage
Run the code through Indenter before executing or compiling it.
In Terminal / Command Prompt
```
$ python indent.py InputFileName [-o OUTPUT_FILE] 
```
PS : "[]" Denote Optional parameters 


| Argument  |  Description |
| ------------- |:-------------:|
| InputFileName | Source Code File to Indent |
| -o OUTPUT_FILE, --output_file OUTPUT_FILE | Output File To Store Processed Code (If Not Specified Code is stored in the InputFile) |

Also See Examples given below

## Examples

**example.c Contains:**
```
#include <stdio.h>
int main()
	int i, j, rows
	printf("Enter number of rows: ")
	scanf("%d", &rows)
	for (i = 1; i <= rows; ++i)
		for (j = 1; j <= i; ++j)
			printf("* ")
		printf("\n")
	return 0
```
Notice how the above code has no ";" or "{}"

#### - To get Output in Same File
In Terminal
```$ python indent.py example.c```

#### - To get Output in a Different File
In Terminal
```$ python indent.py example.c -o output_file.c```


## Footnote
Inspired by [JavaPy](https://github.com/raptor4694/JavaPy)
This Dependency might have bugs.
[License](LICENSE)