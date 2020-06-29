# LLVM-Tracer
An LLVM pass to profile dynamic LLVM IR instructions and runtime values
Run:
------
After you build LLVM-Tracer, you can use example triad programs in the example
directory to test LLVM-Tracer.

Example program: triad
----------------------
  1. Go to /workspace/LLVM-Tracer/example/triad
  2. Run LLVM-Tracer to generate a dynamic LLVM IR trace
     a. LLVM-Tracer tracks regions of interest inside a program.
        In the triad example, we want to analyze the triad kernel instead of the setup
        and initialization work done in main. To tell LLVM-Tracer the functions we are
        interested in, set the enviroment variable WORKLOAD to be the top-level function name:

        ```
        export LLVM_HOME=/usr/local/lib
        export WORKLOAD=cg
        ```

        If you have multiple functions, separate them with commas.

        ```
        export WORKLOAD=$md,$md_kernel
        ```

        LLVM-Tracer will trace them differently based on the `-trace-all-callees` flag, which can be specified
        to the `opt` command (see step d).

        * If this flag is specified, then any function called by any function in the WORKLOAD variable will be traced.
          This is a simple way to trace multiple "top-level" functions at once.
        * If this flag is not specified, then only functions in the WORKLOAD variable will be traced.

     b. Generate the source code labelmap.

        ```
        export TRACER_HOME=/workspace/LLVM-Tracer
        ${TRACER_HOME}/bin/get-labeled-stmts cg.c -- -I${LLVM_HOME}/clang/6.0.0/include
        ```

     c. Generate LLVM IR:

        ```
        clang -g -O1 -S -fno-slp-vectorize -fno-vectorize -fno-unroll-loops -fno-inline -emit-llvm -o triad.llvm cg.c
        ```

     d. Run LLVM-Tracer pass.
        Before you run, make sure you already built LLVM-Tracer and have set
        the environment variable `TRACER_HOME` to where you put LLVM-Tracer
        code.

        ```
        opt -S -load=${TRACER_HOME}/lib/full_trace.so -fulltrace -labelmapwriter -trace-all-callees triad.llvm -o triad-opt.llvm
        llvm-link -o full.llvm triad-opt.llvm ${TRACER_HOME}/lib/trace_logger.llvm 
        ```

        The `-trace-all-callees` flag is optional and defaults to false.

     e. Generate machine code:

        ```
        llc -filetype=asm -o full.s full.llvm
        gcc -fno-inline -o triad-instrumented full.s -lstdc++ -lz -lm
        ```

     f. Run binary. It will generate a file called `dynamic_trace` under current directory.

       ```
       ./triad-instrumented
       ```

     g. There is a script provided which performs all of these operations.

       ```
       python llvm_compile.py $TRACER_HOME/example/triad triad
       ```
