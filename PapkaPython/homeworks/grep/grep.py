
import argparse
import sys
import re


def output(line):
    print(line)

def hardcheck(p,s):
    pattern = p.replace('?','.')
    pattern = pattern.replace('*', '.*')
    result = re.findall(pattern, s)
    if result:
        return True
    else:
        return False

def correct_check(p,s):
    if ('?' in p) or ('*' in p):
        return hardcheck(p,s)
    elif (p in s):
        return True
    else:
        return False

def check (p,s,invert):
    if correct_check (p,s) and not invert:
        return True
    elif not (correct_check(p,s))and invert:
        return True
    else:
        return False
def print_block(lines,begin,end,line_number) :
    if line_number:
        for i in range(begin-1,end):
            output(str(i+1) + "-" + lines[i].rstrip())
    else:
        for i in range(begin-1,end):
            output(lines[i].rstrip())


def check_block(begin,end,num,A,B,lines,line_number):
    if (num-B)<=1:
        begin=1
    elif begin == -1:
        begin=num -B

    if (num - B) <= end:
        end=num+A
    else:
        print("--")
        print_block(lines,begin,end,line_number)
        print("--")
        begin = num - B
        end = num + A
    return begin,end

def grep(lines, params):
    num = 0
    z = 0
    B=params.before_context
    A=params.after_context
    C=params.context
    begin=-1
    end=15
    if C:
        A=C
        B=C
    for line in lines:
        line = line.rstrip()
        s = line
        p = params.pattern
        num += 1
        if params.ignore_case:
            s = s.lower()
            p = p.lower()


        if params.count and check(p, s, params.invert):
            z += 1
        elif check(p, s, params.invert) and params.line_number:
            if A or B:
                begin,end=check_block(begin,end,num,A,B,lines,params.line_number)
            else:
                output(str(num) + ":" + s)
        elif check(p, s, params.invert):
            if A or B:
                begin, end = check_block(begin,end,num,A,B,lines,params.line_number)
            else:
                output(line)

    if (A or B) and not(params.count):
        if end >=len(lines):
            end=len(lines)
        print("--")
        print_block(lines, begin, end,params.line_number)
        print("--")
    if params.count:
        output(str(z))


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()

