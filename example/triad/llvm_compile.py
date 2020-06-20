#!/usr/bin/env python
import os
import sys

kernels = {
'triad' : 'triad',
}

def main (directory, source):

  if not 'TRACER_HOME' in os.environ:
    raise Exception('Set TRACER_HOME directory as an environment variable')
  if not 'LLVM_HOME' in os.environ:
    raise Exception('Set LLVM_HOME directory as an environment variable')

  os.chdir(directory)
  obj = source + '.llvm'
  opt_obj = source + '-opt.llvm'
  executable = source + '-instrumented'
  os.environ['WORKLOAD']=kernels[source]

  TRACER_HOME = os.getenv('TRACER_HOME')
  LLVM_HOME = os.getenv('TRACER_HOME')

  source_file = source + '.c'
  print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n");
  os.system('%s/bin/get-labeled-stmts triad.c -- -I%s/lib/clang/3.4' % (TRACER_HOME, LLVM_HOME))
  print("BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n");
  os.system('clang -static -g -O1 -S -fno-slp-vectorize -fno-vectorize ' + \
            ' -fno-unroll-loops -fno-inline -fno-builtin -emit-llvm -o ' + \
            obj + ' '  + source_file)
  print("CAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n");
  os.system('opt -disable-inlining -S -load=' + TRACER_HOME + \
            '/lib/full_trace.so -fulltrace -labelmapwriter ' + obj + ' -o ' + opt_obj)
  print("DAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n");
  os.system('llvm-link -o full.llvm ' + opt_obj + ' ' + \
            TRACER_HOME + '/lib/trace_logger.llvm')
  print("EAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n");
  os.system('llc -O0 -disable-fp-elim -filetype=asm -o full.s full.llvm')
  print("FAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n");
  os.system('gcc -static -O0 -fno-inline -o ' + executable + ' full.s -lm -lz -lpthread -lstdc++')
  print("GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n");
  os.system('./' + executable)

if __name__ == '__main__':
  directory = sys.argv[1]
  source = sys.argv[2]
  print directory, source
  main(directory, source)
