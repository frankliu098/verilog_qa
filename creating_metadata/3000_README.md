# The Zip CPU

The Zip CPU is a small, light-weight, RISC CPU. Specific design goals include:
- 32-bit: All registers, addresses, and instructions are 32-bits in length.
- A RISC CPU: Instructions nominally complete in one cycle each, with exceptions for multiplies, divides, memory accesses, and (eventually) floating-point instructions.
- A load/store architecture: Only load and store instructions may access memory.
- Includes Wishbone, AXI4-Lite, and AXI4 memory options.
- A (minimally) Von-Neumann architecture: Shared buses for instructions and data.
- A pipelined architecture: Stages for prefetch, decode, read-operand(s), ALU, memory, divide, and write-back.
- Two operating modes: Supervisor and user, with distinct access levels.
- Completely open source, licensed under the GPLv3.

## Unique features and characteristics

- 29 instructions are currently implemented. Six additional instructions are reserved for a floating-point unit (FPU), which has yet to be implemented.
- Most instructions can be executed conditionally.
- The CPU makes heavy use of pipelining.
- The CPU has no interrupt vectors, but uses two register sets for interrupt handling.

## Verilog File Descriptions

### File: ffetch.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/formal/ffetch.v
**Overall Purpose of the File:**
The `ffetch.v` file implements the instruction fetch logic for the Zip CPU, a small, lightweight RISC CPU soft core. Its purpose is to manage the process of fetching instructions from memory, ensuring that the CPU can properly interact with various types of memory configurations by adhering to specified instruction fetch properties. This module plays a crucial role in the instruction pipeline, impacting the performance and efficiency of the CPU's execution flow.

**Inter-module Relationships:**
The `ffetch` module interacts with several other components within the CPU architecture. It interfaces directly with:

1. **CPU Control Signals**: The input signals such as `cpu_new_pc` and `cpu_clear_cache` allow the instruction fetch unit to respond to changes in program control flow and cache states.
2. **Memory Prefetching**: The `pf_valid`, `pf_pc`, and `pf_insn` signals enable the fetch module to utilize prefetched instructions, contributing to faster execution and reducing latency.
3. **Execution Stage**: The `fc_insn` output can be used by subsequent decode and execution stages to access the fetched instruction, thus integrating with the entire instruction pipeline.

The module may also have interactions with memory-related modules to ensure correctness in instruction retrieval as dictated by the CPU’s control logic.

**Key Signals:**
- **Inputs:**
  - `i_clk`: Clock signal for synchronization.
  - `i_reset`: Reset signal to initialize the module.
  - `cpu_new_pc`: A signal indicating a new program counter (PC) value.
  - `cpu_clear_cache`: Command to clear the cache for fresh data retrieval.
  - `cpu_pc`: The current program counter from the CPU.
  - `pf_valid`: Indicates whether the prefetched instruction is valid.
  - `cpu_ready`: Signals that the CPU is ready for the next instruction fetch.
  - `pf_pc`: The program counter associated with the prefetched instruction.
  - `pf_insn`: The prefetched instruction data.
  - `pf_illegal`: Indicates if the fetched instruction was legal or resulted from a bus error.

- **Outputs:**
  - `fc_pc`: Program counter after the fetch operation.
  - `fc_illegal`: Signal indicating if the fetched instruction was deemed illegal.
  - `fc_insn`: The fetched instruction data.
  - `f_address`: The internal address being referenced by the fetch module.

**Behavior of the Module:**
The `ffetch` module contains combinational and sequential logic to manage the instruction fetching process. Key behaviors include:

1. **Instruction Address Calculation**: It maintains state regarding instruction addresses and uses clock cycles to transition between different states of instruction fetching.
  
2. **Handling Prefetch Logic**: The module can utilize prefetched instructions to decrease fetch times and efficiently utilize the CPU's instruction pipeline.

3. **Control Logic**:
   - It determines when to update the internal program counter based on inputs like `cpu_new_pc` and `cpu_ready`, ensuring that the instruction fetching aligns with the intended control flow of the CPU.
   - It manages scenarios where the fetched instruction might be marked as illegal (due to bus errors) and propagates this information to the modules downstream to handle such cases appropriately.

4. **Internal State Management**: The module employs registers, flags, and counters to track states and synchronize actions, such as whether to issue a new fetch or utilize cached instructions.

5. **Reset and Initialization Logic**: Handles the reset condition effectively to initialize states appropriately, ensuring robustness against unwanted states at power-on or reset events.

Overall, the `ffetch.v` file encapsulates the critical logic required for fetching instructions in a RISC CPU architecture while providing flexibility and fidelity through its interface with memory and control signals.

### File: fdebug.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/formal/fdebug.v
### Overview of the `fdebug.v` Verilog File

**Overall Purpose:**
The `fdebug.v` file describes the debugging interface of the ZipCPU core. It implements functionalities that allow control over the CPU's operational state, including the ability to reset the CPU, halt its execution, control stepping, and manage cache clearing and register overrides. The main aim is to facilitate debugging by providing external control over critical features of the CPU.

**Inter-module Relationships:**
The `fdebug.v` file interacts with various components of the ZipCPU architecture, particularly with the ZipSystem or ZipBones interface. It provides an external interface to control the CPU’s state and observe its behavior. The debugging signals can be tied to higher-level testing frameworks, enabling automated test cases or manual debugging support. The module likely interacts with internal CPU control signals to halt or reset its operations and modify registers during a halt state.

**Key Signals (Inputs/Outputs):**
1. **Inputs:**
   - `i_clk`: The clock signal to synchronize the module’s operations.
   - `i_reset`: A positive synchronous reset signal to reset the entire system.
   - `i_cpu_reset`: A reset signal specifically for the CPU, independent of the bus reset.
   - `i_halt`: A request to halt execution of the CPU.
   - `i_halted`: A signal indicating that the CPU has completely halted.
   - `i_clear_cache`: Request to clear the CPU cache; can only be activated while `i_halt` is asserted.
   - `i_dbg_we`: Write Enable signal to allow writing to a CPU register during a halt phase.
   - `i_dbg_reg`: Identifier of the register that is being accessed (0-31).
   - `i_dbg_data`: The data to be written to the specified register.
   - `i_dbg_stall`: Indicates that the CPU is not ready to accept write requests.
   - `i_dbg_break`: A signal indicating a break condition has occurred within the CPU.
   - `i_dbg_cc`: Status signals indicating specific conditions within the CPU (like bus errors, mode status, and sleep/halt states).

2. **Outputs:**
   - While no explicit outputs are listed in the provided information, typically such modules would have status signals or acknowledgement signals tied to their operations.

**Behavior of the Module:**
The `fdebug.v` module incorporates several control logic functionalities:
- It checks various request signals (like `i_halt`, `i_clear_cache`, and `i_dbg_we`) to determine if the CPU should stop executing instructions or perform cache cleaning tasks.
- The module maintains strict adherence to operational protocols, ensuring that cache clearing requests are only issued when the CPU is halted and that register write requests respect the stall conditions.
- The handling of the `i_dbg_reg`, `i_dbg_data`, and associated write operations allows developers to dynamically modify register values during debugging sessions to test specific behaviors or recover from erroneous states.

In essence, this file encapsulates critical functionalities necessary for debugging actions, thereby enabling developers to efficiently troubleshoot and validate the operation of the ZipCPU.

### File: abs_mpy.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/formal/abs_mpy.v
### Description of `abs_mpy.v`

#### Overall Purpose of the File
The `abs_mpy.v` file implements a multiplication unit for the Zip CPU, designed to provide an abstracted, simplified interface for handling multiplication operations. This module specifically caters to the needs of formal verification methods, allowing for more manageable testing and validation of the multiply operations. Importantly, this module can be configured for different multiplication algorithms and clock cycles required for the operation, abstracting the complexity for more efficient design and verification.

#### Inter-module Relationships
The `abs_mpy` module forms part of the larger Zip CPU architecture and operates within the context of arithmetic operations. It interacts with other components of the CPU’s arithmetic logic unit (ALU) or similar functionalities, particularly the `mpyop.v` file, which it was adapted from. This module can be indirectly linked to modules responsible for instruction decoding and execution, as those entities will trigger multiplication operations by sending appropriate control signals to the `abs_mpy`.

#### Key Signals
- **Inputs:**
  - `i_clk`: The clock signal for synchronizing operations.
  - `i_reset`: A reset signal used to initialize or reset the state of the module.
  - `i_stb`: Strobe signal indicating the start of the multiplication operation.
  - `i_op`: 2-bit operation signal determining the type of multiplication to perform (e.g., regular multiply, unsigned high, signed high).
  - `i_a`, `i_b`: 32-bit operands for the multiplication operation.

- **Outputs:**
  - `o_valid`: Indicates whether the result of the multiplication operation is valid.
  - `o_busy`: Indicates whether the multiplication operation is still in progress.
  - `o_result`: A 64-bit result of the multiplication operation, capable of holding larger products.
  - `o_hi`: A signal that returns the higher half of the multiplication result.

#### Module Behavior
The `abs_mpy` module operates by first determining the type of multiplication to execute based on the `i_op` control signal. Depending on the `OPT_MPY` parameter, it can either perform multiplication (when `OPT_MPY` is set) or disable it altogether (when `OPT_MPY` is set to 0). If multiplication is enabled, the module uses a simplified approach where results can be returned in 1 to 6 clock cycles, streamlining the computation for formal verification.

Key behaviors include:
- **Multiplication Control Logic**: The module contains decision logic that checks the incoming strobe (`i_stb`) and the operation type (`i_op`) to determine whether to proceed with a multiplication operation.
- **Busy and Valid Signals**: It tracks whether an operation is ongoing using the `r_busy` register, updating `o_busy` accordingly, and it manages the validity of the result through `o_valid`.
- **Result Evaluation**: The output result is produced based on the internal computation logic, which has provisions for handling delays to ensure that results are available only after the necessary calculations.

Overall, `abs_mpy.v` offers an efficient, adaptable, and formalizable mechanism for multiplication within the Zip CPU architecture, ensuring that its design allows for easier testing and integration with other CPU components.

### File: abs_div.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/formal/abs_div.v
### Purpose of the File

The `abs_div.v` file implements an abstract integer divide module for the Zip CPU architecture. Its primary purpose is to provide integer division capabilities, accommodating both signed and unsigned results. The module is intended to facilitate formal verification efforts by simplifying the interactions and ensuring various conditions can be checked more securely during the validation phase.

### Inter-module Relationships

The `abs_div` module interacts with various components of the Zip CPU architecture, which may include:

- **Pipeline Stages**: The divide operation may be performed during a particular stage of the CPU pipeline, hence it interacts with stages responsible for instruction execution and potentially the memory access stage.
- **Control Logic**: It may work in conjunction with control signals from the CPU's control unit to dictate when to perform a divide operation, handle stalls, or adjust parameters based on opcode interpretations.
- **Data Path Components**: It interacts directly with registers that provide the dividend and divisor, as well as output signals that indicate the status of the division operation, such as results and valid flags.
  
### Key Signals

- **Inputs**:
  - `i_reset`: Active high signal to reset the divide unit and transition it into idle state.
  - `i_wr`: Signal indicating a write operation that triggers the division process.
  - `r_dividend`: Register that holds the numerator for the division.
  - `r_divisor`: Register that holds the denominator for the division, which is adjusted during processing.

- **Outputs**:
  - `o_busy`: Indicates that the divide operation is in progress. This busy flag prevents other components from interfering until the division is complete.
  - `o_valid`: Signifies whether the division result is ready to be read from the output.
  - `o_quotient`: The result of the division operation, which may be either signed or unsigned based on the input flags and control logic.

### Behavior of the Module

The `abs_div` module operates as follows:

1. **Initial State and Reset**: When the `i_reset` signal is asserted, the module goes into an idle state. This includes initializing internal states and output signals.

2. **Start Division**: When a division operation is requested via the `i_wr` input:
   - The module sets `o_busy` high, indicating the divide operation is in progress.
   - The result register `o_quotient` is initialized to zero.
   - The inputs for the division (`r_dividend` and `r_divisor`) are prepared. The `r_divisor` is adjusted to simplify division by using multiplication instead of traditional division.

3. **Processing Phase**:
   - A preparatory cycle may convert signed division requests into unsigned ones.
   - The quotient is calculated over a series of clock cycles (up to 32), shifting the divisor and reducing it as appropriate until the correct quotient is accumulated.

4. **Completion of Division**:
   - Once the division logic has completed after the allotted cycles, `o_busy` is set low to indicate that the operation is complete. 
   - The `o_valid` output is set high, allowing downstream modules to read the `o_quotient` and utilize the result.

5. **Output Handling**: The protocol supports safeguards to ensure that `o_busy` and `o_valid` do not indicate true simultaneously, maintaining adherence to the Zip CPU's internal communication protocol.

In summary, the `abs_div.v` module encapsulates the logic for performing integer divisions efficiently while ensuring clear communication with the rest of the CPU architecture through its control signals and output conditions.

### File: f_idecode.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/formal/f_idecode.v
### Overview of `f_idecode.v`

**Overall Purpose:**
The `f_idecode.v` file is a Register Transfer Level (RTL) implementation designed to mirror the functionality of the `idecode.v` file in the Zip CPU project. Its primary purpose is to facilitate the verification of instructions processed in the ZipCPU pipeline without relying on clock cycles. By decoding instructions directly, it enhances the validation process by providing clarity on how instructions are interpreted and what operations they perform as they pass through the CPU pipeline.

**Inter-module Relationships:**
The `f_idecode` module interacts closely with the following components of the CPU architecture:

- **Instruction Fetch Logic:** It receives the fetched instruction from the instruction fetch stage, likely from a module similar to `ffetch.v`.
- **Execution Modules:** It provides decoded signals to execution modules as part of the pipeline, which may include arithmetic, logical, or control instruction corners.
- **Control Logic:** This module might interact with and provide signals for handling status flags like global interrupt enable (GIE) in conjunction with other control logic in the microarchitecture.

**Key Signals:**
1. **Inputs:**
   - `i_instruction` (31:0): The instruction fetched from memory that needs to be decoded.
   - `i_phase`: Indicates the execution phase of the instruction.
   - `i_gie`: A global interrupt enable signal that can affect instruction processing.

2. **Outputs:**
   - `o_illegal`: A signal that indicates whether the instruction is illegal or undefined.
   - `o_dcdR`, `o_dcdA`, `o_dcdB`: Decoded register addresses that will be used in the execution stage.
   - `o_I`: The immediate value extracted from the instruction.
   - `o_cond`: Conditional flags associated with the instruction.
   - `o_wF`, `o_op`, `o_ALU`, `o_M`, `o_DV`, `o_FP`, `o_break`, and `o_lock`: Various control signals that dictate the instruction's behavior in the CPU.
   - `o_wR`, `o_rA`, `o_rB`: Signals that determine write and read access for specified registers.
   - `o_prepipe`: A signal indicating if instruction pre-pipelining is occurring.
   - `o_sim`: A simulation flag.
   - `o_sim_immv`: Simulated immediate values for additional features in instruction execution.

**Behavior of the Module:**
The `f_idecode` module decodes the instruction in a purely combinatorial manner, meaning it does so without clock dependency. It analyzes the `i_instruction` input to interpret its contents and produce the necessary output signals. 

- **Control Logic:** 
  - The module utilizes several combinatorial logic constructs to identify specific instruction types (`w_ldi`, `w_mov`, etc.) by checking appropriate bits in the instruction. This helps in determining how to generate the output signals like `o_illegal` and others based on the legal range of instructions.

- **Instruction Handling:**
  - The decoded outputs will determine the operation types and control logic required for instruction execution. For instance, if it identifies an operation that requires the use of the ALU, it will assert the corresponding `o_ALU` signal accordingly.

- **Decoding Specific Patterns:**
  - It involves setting bit masks and using logical operations to decode parts of the instruction for generating output register addresses (`o_dcdR`, `o_dcdA`, `o_dcdB`) based on different instruction formats supported by the CPU architecture.

This structure allows `f_idecode.v` to serve as a crucial element in ensuring the accuracy of instruction decoding while contributing to the overall performance and reliability of the Zip CPU design.

### File: fmem.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/formal/fmem.v
### Purpose of the File
The `fmem.v` file serves to formalize the interface between the Zip CPU and its memory unit. The goal is to ensure that any memory unit conforming to the specified interface can interact with the Zip CPU without errors. This includes handling various types of memory operations, managing request signals, and indicating the memory unit's state.
  
### Inter-Module Relationships
The `fmem.v` module interacts with several other components in the CPU architecture, primarily:
- **CPU**: It communicates with the CPU to perform memory requests for reading and writing data.
- **Memory Units**: It defines the expected behavior and protocol for external memory, ensuring compatibility with various memory architectures.
- **Control Logic**: The interface includes signals that coordinate the operation between the CPU and memory, informing the CPU about the memory's status (busy, done, etc.).

### Key Signals (Inputs/Outputs)
**Inputs:**
- `i_clk`: Clock signal to synchronize operations.
- `i_sys_reset`: A global reset for the entire bus and memory unit.
- `i_cpu_reset`: A reset signal specifically for the CPU.
- `i_stb`: Indicates when the CPU is making a memory request.
- `i_pipe_stalled`: Indicates whether the memory unit can currently accept requests.
- `i_clear_cache`: Request to clear the memory cache.
- `i_lock`: Request for a locked sequence for atomic operations.
- `i_op`: Specifies the type of memory operation (e.g., load, store, etc.).
- `i_addr`: Address for the read/write operation.
- `i_data`: Data to be written during a store operation.
- `i_areg`: The register to which the read result should be written.
- `i_busy`: Indicates if the memory unit is currently busy.
- `i_rdbusy`: Indicates if the memory is busy but able to write back data to the CPU.
- `i_valid`: Indicates that the read data is valid and ready for processing.
- `i_done`: Indicates that the read/write operation has completed.
- `i_err`: Indicates a bus error occurred.
- `i_wreg`: The register which will hold the read result if `i_valid` is true.
- `i_result`: The data returned from the last read operation.

**Outputs:**
- `f_outstanding`: A counter for the number of outstanding memory requests.
- `f_pc`: Indicates whether the last read will update the program counter or flags register.

### Behavior of the Module
The behavior of the `fmem.v` module revolves around managing memory requests through the following key functionalities:

1. **Synchronous Operations**: The module operates in synchronization with a clock, processing requests and signals on rising or falling edges as defined.
  
2. **Control Logic**: The module has control logic that interprets the operation type (defined by `i_op`) to determine whether it performs a load or store operation and what kind of access it requests (32-bit, 16-bit, 8-bit). 

3. **State Management**:
   - The module maintains a state representing the memory unit's readiness (`i_busy`, `i_valid`, etc.) and handles the logic for memory operation completion (`i_done`, `f_outstanding`).

4. **Error Handling**: It includes mechanisms to handle bus errors, allowing the CPU to initiate appropriate exception handling routines.

5. **Result Handling**: When a read operation is completed, if `i_valid` is high, the module directs the result to the appropriate register indicated by `i_wreg`.

6. **Outstanding Requests**: The module increments `f_outstanding` for each request made (when `i_stb` is high) and decrements it when an operation is completed (when `i_done` is high). This keeps track of how many active requests from the CPU are being processed by the memory.

In summary, `fmem.v` acts as an intermediary that facilitates the transfer of data between the CPU and memory by ensuring that the requests are properly handled, and that the state of memory operations is accurately communicated back to the CPU.

### File: zipbones.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/mcy/zipcpu/zipbones.v
### Description of the Verilog File: zipbones.v

#### Overall Purpose
The `zipbones.v` file implements the core logic for the Zip CPU, a small and lightweight RISC CPU architecture. This module is designed to function as a minimalistic CPU system without any integrated peripherals, allowing external components to be connected as needed. The emphasis is on maintaining a small footprint, making it suitable for resource-constrained environments.

#### Inter-module Relationships
The `zipbones` module interacts with several components of the system:
- **Wishbone Interface**: It serves as a master interface to communicate with other memory components and peripherals via the Wishbone protocol. This includes:
  - Sending signals indicating the current cycle, strobe, write enable status, address, data, and select signals.
  - Receiving responses from the Wishbone slave, including acknowledgment and data back from memory.
  
- **External Interrupt Handling**: It includes input and output signals for managing interrupts:
  - Receives external interrupt signals via `i_ext_int`.
  - Signals external devices through `o_ext_int`.
  
- **Debug Interface**: It provides an optional Wishbone interface for debugging purposes, which allows for interaction with debugging tools or systems, including acknowledgment and data return for debugging operations.

- **Control Logic and State Management**: The module likely interfaces with state machines or control modules responsible for CPU operation control and instruction processing.

#### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_clk`: The clock signal driving the operation of the CPU.
  - `i_reset`: A reset signal to initialize or reset the CPU state.
  - `i_ext_int`: External interrupts input, allowing external events to interrupt the CPU processes.
  - **Debug Inputs**:
    - `i_dbg_cyc`, `i_dbg_stb`, `i_dbg_we`, `i_dbg_addr`, `i_dbg_data`: Signals for debugging operations.
  
- **Outputs**:
  - `o_wb_cyc`: Indicates that the CPU is making a Wishbone cycle.
  - `o_wb_stb`: An assertion indicating that the CPU is currently accessing a peripheral through the Wishbone protocol.
  - `o_wb_we`: A signal that indicates whether the current operation is a write operation.
  - `o_wb_addr`: The address for the memory operation.
  - `o_wb_data`: The data to be written to the memory or peripheral.
  - `o_ext_int`: The signal indicating an output external interrupt.
  - **Debug Outputs**:
    - `o_dbg_stall`, `o_dbg_ack`, `o_dbg_data`: Signals for the debugging interface.

#### Behavior of the Module
The `zipbones` module operates based on the states defined by the control logic within it:
- It handles the CPU reset state, initializing registers and internal states.
- The module supports the handling of external interrupts, checking `i_ext_int` to trigger appropriate responses.
- The Wishbone communication is handled based on current operation cycles, with state transitions depending on the `o_wb_cyc` and `o_wb_stb` signals, ensuring the correct addressing and data flow to and from the connected peripherals or memory.

The structure of `zipbones` suggests the use of combinational and sequential logic to manage data flow and control signals. The presence of control parameters and configurable options (like `IMPLEMENT_MPY`, `IMPLEMENT_DIVIDE`, etc.) allows the CPU functionality to be tailored for specific needs without altering the core structure significantly.

In summary, the `zipbones.v` file is crucial for encapsulating the core logic of the Zip CPU, facilitating interaction with external memory, handling interrupts, and providing monitoring/debugging capabilities, all while adhering to a minimalist design approach.

### File: zipmmu_tb.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/rtl/zipmmu_tb.v
### Description of the Verilog File: `zipmmu_tb.v`

#### Overall Purpose of the File
The `zipmmu_tb.v` file serves as a test-bench for the Memory Management Unit (MMU) of the Zip CPU, which is a lightweight RISC CPU architecture. The primary function of this test-bench is to verify the operation of the MMU independently of the CPU itself. This allows for focused testing of the MMU's functionality, detecting any issues before integrating it with the broader CPU system. The test-bench integrates with a C++ Verilator-enabled framework for testing.

#### Inter-Module Relationships
In the context of the CPU architecture:
- The `zipmmu_tb` module is designed to simulate the behavior of the MMU, providing its inputs for stimulus and capturing outputs for verification.
- The MMU interacts with other components of the CPU, such as:
  - `zipcpu` core (not detailed in this file) for instruction and data access.
  - Memory controller components to manage read/write operations.
  - Control buses that handle interactions between the CPU and the memory.
  
The test-bench might implement instances of these other modules or rely on external simulation tools and models to create a comprehensive testing environment.

#### Key Signals (Inputs/Outputs)
**Inputs:**
- `i_clk`: Clock signal for synchronizing the operations.
- `i_reset`: Reset signal to initialize the MMU and clear previous states.
- `i_ctrl_cyc_stb`: Control cycle strobe for operation signaling.
- Memory operation inputs:
  - `i_wbm_cyc`, `i_wbm_stb`, `i_wb_we`: Signals indicating memory cycle, strobe, and write enable, respectively.
  - `i_exe`: Execution signal that can trigger MMU operations.
  - `i_wb_addr`, `i_wb_data`, `i_wb_sel`: Address, data, and select lines for the incoming write bus.
- `i_gie`: Global interrupt enable signal.

**Outputs:**
- Status flags:
  - `o_rtn_stall`, `o_rtn_ack`, `o_rtn_err`, `o_rtn_miss`: Indicate the MMU's readiness and status in terms of data return.
  - `o_rtn_data`: The data returned by the MMU in response to queries.

Additional outputs exist under the `VZIPMMU_TB` conditional compilation, which return various status and data signals for debugging and analysis.

#### Behavior of the Module
The behavior of `zipmmu_tb` is centered around simulating and validating the MMU's functionality:
- **Control Logic:** The module processes incoming control signals to manage data transactions appropriately, responding to memory read/write requests.
- **State Machines:** Though full details of the internal state machines or control logic are not given in the visible portion of the code, the `i_ctrl_cyc_stb` and memory operation signals suggest that the MMU includes control state machines that dictate its operation based on the status of these signals. The unit may handle different states such as idle, read, write, stall, or error in response to input stimuli.
  
For the `VZIPMMU_TB` section, the test-bench likely utilizes additional signals such as `r_valid`, `wr_vtable`, etc., to facilitate the interaction with other test features, validate memory transactions, and ensure MMU performance metrics are met.

Overall, `zipmmu_tb.v` is a critical component for ensuring that the MMU behaves correctly and meets design specifications before it is integrated into the final CPU design.

### File: memdev.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/rtl/memdev.v
### Overall Purpose of the File

The `memdev.v` file implements an on-chip memory module that is accessible via the Wishbone bus interface. Its primary purpose is to provide a single-cycle, pipelined access memory for the Zip CPU architecture, allowing fast read and write operations. It can be pre-loaded with data from a specified hexadecimal file (`HEXFILE`) which enables testing and simulation of the CPU's behavior with predefined memory contents.

### Inter-module Relationships

The `memdev.v` module is designed to interact with other components in the CPU architecture, particularly:

- **Wishbone Bus Interface**: It interfaces directly with the Wishbone bus, receiving signals from the master device (such as the CPU) that control memory transactions. Specifically, it responds to read and write requests from the CPU.
- **CPU Control Logic**: It works closely with CPU control logic that generates the appropriate Wishbone signals (like `i_wb_cyc`, `i_wb_stb`, etc.) for memory access, enabling proper data flow in the pipeline.
- **Prefetch and Fetch Stages**: Memory fetching and storing are integral to instruction execution and data management. As such, `memdev.v` plays a role in the pipeline stages where instructions are fetched and results are written back.

### Key Signals (Inputs/Outputs)

**Inputs:**
- `i_clk`: Clock signal for synchronizing memory operations.
- `i_reset`: Resets the memory state.
- `i_wb_cyc`: Indicates if the current transaction is part of a Wishbone cycle.
- `i_wb_stb`: Signal to indicate that a memory access request is being made.
- `i_wb_we`: Write enable signal (high for writes).
- `i_wb_addr`: Address signal specifying which location in memory to access.
- `i_wb_data`: Data signal carrying the data to be written (in case of a write operation).
- `i_wb_sel`: Select signal for byte enables indicating which bytes are valid in a multi-byte transaction.

**Outputs:**
- `o_wb_stall`: Signal to indicate a stall condition on the Wishbone bus (to pause master).
- `o_wb_ack`: Acknowledge signal indicating the completion of the operation.
- `o_wb_data`: Data output for read operations, carrying the data read from memory.

### Behavior of the Module

The `memdev` module operates with the following characteristics:

1. **Memory Declaration**: A 2D array of memory is declared to store the data defined by the `LGMEMSZ` parameter. The memory size is determined by `LGMEMSZ`, which represents the logarithm of the memory size in bytes.

2. **Memory Pre-loading**: If a non-null `HEXFILE` is specified, the initial memory contents can be loaded using `$readmemh`, allowing testing with specific data.

3. **Memory Access Control**:
   - The memory can handle both read and write accesses. Write transactions are initiated when `i_wb_stb` is high and `i_wb_we` is true.
   - The module provides an acknowledge signal (`o_wb_ack`) and a data output (`o_wb_data`) after processing requests. 
   - If the `EXTRACLOCK` parameter is set, certain signals are delayed to allow proper pipelining. If set to zero, the memory can respond immediately to requests.

4. **Stall Handling**: The module can output a stall signal (`o_wb_stall`) based on the operational conditions, which helps to manage when the CPU or other bus masters must wait for memory accesses.

### Summary

In summary, the `memdev.v` file provides a memory interface for the Zip CPU, enabling efficient and pipelined data access while facilitating improved interaction through its Wishbone bus interface. It maintains alignment with the system's clocking and control signals, allowing integration with other modules in the CPU architecture.

### File: zipaxil.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipaxil.v
### Purpose of the File

The `zipaxil.v` file implements a top-level module for the Zip CPU, specifically integrating AXI-lite interfaces for instruction, data, and debugging. The design supports a very basic RISC architecture and is described as bus-width agnostic for both instruction and data buses, while enforcing a 32-bit width for the debug bus. It aims to encapsulate the core functionality of the Zip CPU and provide a simplified interface for communication with external components.

### Inter-module Relationships

The `zipaxil` module serves as a bridge between the CPU core and peripheral components through AXI-lite interfaces. It interacts with various core modules responsible for instruction processing, memory management, and debugging:

- **Core Interaction**: The module connects to the core of the Zip CPU, managing data flows and communication for instruction execution.
- **Memory Interfaces**: It encompasses memory-related modules where instructions and data are fetched or stored, potentially including instruction and data caches (depending on parameter configurations).
- **Debug Interfaces**: It provides accessory ports for debugging, allowing external debuggers to access the CPU's internal states and register values.
- **Peripheral Connections**: The design suggests that it can interface with peripherals, enabling easy integration into larger systems or SoCs (System on Chips).

Overall, `zipaxil.v` is a key component that connects and orchestrates the interactions among various subsystems within the CPU architecture.

### Key Signals (Inputs/Outputs)

The key signals of the `zipaxil` module include parameters that define the configuration and control of the CPU operation, as well as the AXI-lite interface signals. Here are important signals that could likely be present (though not explicitly shown in the provided snippet):

1. **Input Signals**:
   - `i_clk`: The clock signal for synchronous operation.
   - `i_reset`: The reset signal to initialize the CPU to a known state.
   - `axi_awaddr`: AXI address for write operations.
   - `axi_awvalid`: Signals that the address is valid for write.
   - `axi_wdata`: Data bus for AXI write operations.
   - `axi_wvalid`: Signals that the write data is valid.
   - Additional addresses and control signals for read/write operations.

2. **Output Signals**:
   - `axi_bresp`: Response signal for AXI write transactions.
   - `axi_bvalid`: Indicates response validity.
   - `axi_araddr`: AXI address for read operations.
   - `axi_arvalid`: Signals that the address is valid for read.
   - `axi_rdata`: Data bus for AXI read operations.
   - `axi_rresp`: Response signal for AXI read transactions.
   - `axi_rvalid`: Indicates read data validity.
   - Other control signals, including status and interrupt signals.

### Behavior of the Module

The behavior of the `zipaxil` module revolves around managing the AXI interface as well as orchestrating the control logic for instruction and data operations. This includes:

- **Control Logic**: The control logic is responsible for directing data based on the received commands via the AXI interface, determining whether to initiate a read or write operation based on incoming signals.

- **State Machines**: The module likely contains state machine logic to handle various states of read and write operations, including address acknowledgment, data transfer, and response handling.

- **Data Processing/Logic**:
  - It interfaces with the instruction decoder and execution units, routing the fetched instructions based on the current execution context.
  - Handles memory access patterns—whether to utilize caches or interact directly with memory modules, as governed by the specified parameters (e.g., caches on or off).

The integration of parameters such as `OPT_PIPELINED`, `OPT_MPY`, `OPT_DIV`, and various operational options suggests a highly configurable design that can adapt to different requirements and optimizations based on the instantiation of the module.

In summary, `zipaxil.v` stands as a crucial component within the Zip CPU architecture, managing interactions among the CPU core, memory, and peripherals while maintaining flexibility and structural simplicity in its design.

### File: zipsystem.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipsystem.v
### Overview of `zipsystem.v`

#### Purpose
The `zipsystem.v` file implements the peripheral subsystems for the Zip CPU, a lightweight RISC CPU architecture. It serves as a collection of soft peripherals that interact with the CPU core, enabling enhanced functionalities without the need for dedicated hardware components. These peripherals include an interrupt controller, interval timers, watchdog timers, and a Direct Memory Access (DMA) controller, making the CPU capable of real-time operations and data management.

#### Inter-module Relationships
The `zipsystem.v` file interfaces with several modules in the CPU architecture:

- **CPU Core**: The primary interaction occurs with the CPU core, which utilizes this module's peripheral features via specific buses, namely:
  - **CPU Bus (`cpu`)**: This bus enables the CPU to communicate with both local and global peripheral components. It differentiates between two types of buses: the local bus (`_lcl_`) for accessing peripherals within the module and the global bus (`_gbl_`) for accessing external hardware.
  
- **Memory Management Unit (MMU)**: Interactions with the MMU occur via a dedicated bus, isolating the operations between the CPU and the external bus. The MMU manages the address translation and access control for memory operations involving the peripherals.

- **Debug Interfaces**: The system includes debug buses (`io_dbg`, `dbg`, etc.) that allow external debugging of the CPU and its peripherals without going through the CPU data pathways.

- **Direct Memory Access Controller**: The DMA controller allows for memory operations to be carried out independently of the CPU, thus relieving the CPU overhead during extensive data management tasks.

#### Key Signals (Inputs/Outputs)
The module's interfaces mainly consist of various signal buses shared with the CPU and peripherals. Some notable ones likely include:

- **Inputs**:
  - Signals from the CPU core to initiate read and write operations on peripherals.
  - Interrupt signals generated by the CPU or external sources to the interrupt controller.

- **Outputs**:
  - Data output signals that feed from the DMA and timers back to the CPU or external devices.
  - Control signals indicating timer events or interrupts to the rest of the CPU system.

While the specific bus signals are not detailed in the provided snippet, it typically would include control, address, and data signals that correspond to these functions.

#### Behavior of the Module
The `zipsystem.v` module contains essential control logic to manage its functionalities, including:

- **Interrupt Management**: The interrupt controller handles incoming interrupt requests, prioritizing and relaying them to the CPU. It manages masking and acknowledgment of interrupts.
  
- **Timer Management**: The implementation of interval timers and watchdog timers allows these peripherals to count down from a defined value. When the timer reaches zero, it can either stop or generate an interrupt request to the CPU, which can then read the timer’s status or reset it.

- **DMA Operations**: The Direct Memory Access Controller facilitates burst memory transfers autonomously, allowing read/write operations to occur without CPU intervention. The state machine architecture within the DMA manages address sequencing and transfer protocols.

Overall, the behavior encompasses synchronization with the CPU’s operational states, managing events via interrupts, timers, and direct memory transactions while minimizing CPU load during intensive data operations.

### File: zipbones.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipbones.v
### Overall Purpose of the File

The `zipbones.v` file implements the `Zip CPU`, a lightweight RISC CPU core designed for efficiency and simplicity. The primary purpose of this module is to provide a minimalistic CPU architecture without any integrated peripherals, allowing for flexible deployment in various configurations depending on system requirements. Users can implement additional peripherals externally as needed.

### Inter-module Relationships

The `zipbones` module interacts with other modules in the CPU architecture primarily for the following functions:

1. **Instruction Fetch and Execution:** It connects with instruction-related modules (such as `ffetch.v`, `fmem.v`, and `idecode.v`) to fetch and decode instructions for execution.
  
2. **Control Logic:** It works with control units to manage the flow of execution, branching, and memory accesses based on CPU options and configuration parameters.

3. **Register and Memory Interfaces:** It includes parameters to support distributed registers and cache mechanisms, facilitating efficient data management during computational tasks.

4. **Optional Extensions:** Various optional features such as Multiplication (`OPT_MPY`), Division (`OPT_DIV`), and Floating Point Units (`OPT_FPU`) can be linked within the broader system, depending on the configured parameters.

### Key Signals (Inputs/Outputs)

While the exact signal definitions are not fully outlined in the snippet, the module typically includes key inputs and outputs that would align with a CPU architecture:

- **Inputs:**
  - `clk`: The clock signal for synchronous operations.
  - `reset`: The signal that initializes or resets the CPU.
  - Other control signals that may handle branching or interrupt signals.

- **Outputs:**
  - `instruction_data`: Data output for the instruction fetched and decoded for execution.
  - `status_flags`: Various flags representing the CPU's status (e.g., zero, overflow, carry).
  - `memory_address`: Address signals that interact with the memory subsystem for reading/writing data.

### Behavior of the Module

1. **Control Logic:** It likely includes control logic for handling state transitions during instruction fetch, decode, and execute cycles. The implemented parameters specify architectural features that influence this control flow, such as pipelining and early branching.

2. **State Management:** The CPU operates based on states defined by the control logic, switching between states such as fetching, waiting, executing, and handling interrupts. The states depend on the configuration parameters, aligning the behavior with user requirements.

3. **Data Path Handling:** The module facilitates data paths to carry instructions and data between various component units, optimizing performance based on the selected configuration (such as caches, registers, and buses).

4. **Parameterization:** The CPU core's behavior is highly parameterized, allowing users to enable or disable various features (e.g., cache options, debugging ports) based on design specifications. This flexibility ensures the core can be tailored to specific applications, ranging from simple microcontroller tasks to more complex computations.

### Summary

In summary, the `zipbones.v` file is a foundational component of the Zip CPU, designed to provide a modularized and flexible architecture compatible with a range of possible applications. The inter-module relationships leverage parameterized configurations that influence the overall behavior and capabilities of the CPU, enabling a customizable development approach for hardware synthesis. The CPU's control logic and state management facilitate a streamlined instruction execution process, while the modules are designed for clear interfaces with other system components and peripherals.

### File: zipaxi.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipaxi.v
### Purpose of the File

The `zipaxi.v` file serves as a top-level module for the Zip CPU, integrating both AXI4 instruction and data interfaces along with AXI-lite debug interfaces. The design is aimed at providing a lightweight and simple implementation of a RISC CPU. It supports a streamlined instruction set featuring approximately 26 operational types and is adaptable to various bus widths, provided that the instruction and data buses meet a minimum width of 32 bits. The module is developed with flexibility in mind, potentially allowing for extensions such as floating point operations and non-register transactions.

### Inter-module Relationships

The `zipaxi` module interacts with various other components of the Zip CPU architecture. These include:

- **AXI4 Interfaces**: Facilitates communication with memory and possibly other peripheral devices using the AXI protocol, ensuring proper data transfer and control signals.
- **Debug Interfaces**: Utilizes AXI-lite for debugging purposes, allowing external devices to monitor and control the internal state of the CPU.
- **Pipeline Mechanisms**: Connects with the pipelined execution stages of the CPU, leveraging parameters like `OPT_PIPELINED` to influence module behavior particularly in relation to the instruction and data caches.
- **Memory Subsystem**: Works with memory components within the design to fetch and store data and instructions as dictated by the CPU's operational requirements.

### Key Signals (Inputs/Outputs)

The key inputs and outputs of the `zipaxi` module are defined with a series of parameters and local parameters, which are heavily utilized to configure the CPU’s behavior:

- **Parameters**:
  - `C_DBG_ADDR_WIDTH`: Configures address width for debug interfaces.
  - `C_AXI_DATA_WIDTH`: Sets the data width for the AXI interface.
  - `ADDRESS_WIDTH`: Defines the overall addressing capability of the CPU.
  - `C_AXI_ID_WIDTH`: Establishes identifier width for transactions.
  - Various operational parameters, such as `OPT_LGICACHE`, `OPT_LGDCACHE`, and `OPT_PIPELINED`, that influence specific performance and architectural decisions.

- **Control Signals**: Include reset signals, interrupt signals, and instruction/data request signals that connect to other components for operation.

### Behavior of the Module

The behavior of the `zipaxi` module is multifaceted, involving control logic and state machines that handle several tasks:

1. **Instruction and Data Fetching**: The module is responsible for issuing requests to fetch instructions and data from memory depending on the operational mode of the CPU.

2. **AXI Protocol Compliance**: It adheres to the AXI protocol, managing state transitions between IDLE, READ, WRITE, and WAIT states, ensuring proper completion of transactions.

3. **Pipeline Management**: Depending on configuration parameters, the module may implement pipelining for instruction fetching and execution to enhance throughput.

4. **Debug Interface Operation**: Uses AXI-lite for debug operations, allowing external programs to access internal registers and signals for diagnostic purposes.

5. **Flexibility in Configuration**: The various parameters allow the module to be customized for specific application needs, such as enabling or disabling certain features (e.g., multiplication and division operations, use of caches).

This control logic typically manages the flow of data through state machines, enabling seamless interaction between the CPU and memory or peripherals, while maintaining the required timing and data integrity as dictated by the AXI specification. 

In summary, `zipaxi.v` is a critical component of the Zip CPU design, providing the necessary interfaces for communication with external memory and debugging tools while configuring various aspects of the CPU's operational integrity and performance through a comprehensive parameter set.

### File: zipdma_s2mm.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma_s2mm.v
### Overview of `zipdma_s2mm.v`

#### Overall Purpose:
The `zipdma_s2mm.v` file implements the functionality of a DMA (Direct Memory Access) controller specifically designed for writing data from an incoming stream interface to a memory bus in the context of the Zip CPU architecture. The DMA controller has the capability to write data either in byte-sized, half-word (2 bytes), or word (4 bytes) increments, and it also supports writing at the full width of the memory bus (which can be up to 64 bits wide). It ensures that proper addressing and alignment are maintained during the write operations.

#### Inter-module Relationships:
- **Incoming Stream Interface:** The module interacts with other components of the system by using an incoming stream interface to receive data. The signals associated with this interface (`S_VALID`, `S_READY`, `S_DATA`, etc.) facilitate the data transfer from the stream into the DMA controller.
- **Outgoing Wishbone Interface:** The `zipdma_s2mm` communicates with the Wishbone memory bus interface through signals such as `o_wr_cyc`, `o_wr_stb`, `o_wr_we`, etc. This interface is responsible for writing data to the actual memory.
- The module likely interacts with other controllers or arbitration logic to properly handle incoming requests and manage state during data transfers.

#### Key Signals:
- **Inputs:**
  - `i_clk`: Clock signal for synchronous operation.
  - `i_reset`: Synchronous reset signal for the module.
  - `i_request`: Indicates that a data transfer request is initiated.
  - `i_inc`: Indicates whether to increment the address after each write.
  - `i_size`: Specifies the size of the data being transferred (1 byte, 2 bytes, or 4 bytes).
  - `i_addr`: The starting address in memory where data should be written.
  - `S_VALID`: Indicates valid data on the incoming stream.
  - `S_DATA`: The data being written.
  - `S_BYTES`: Specifies how many bytes are valid in `S_DATA`.
  - `S_LAST`: Specifies if this is the last data transfer in the sequence.

- **Outputs:**
  - `o_busy`: Indicates the DMA controller is currently busy and processing a data transfer.
  - `o_err`: Indicates an error occurred during the data transfer.
  - `S_READY`: Indicates that the DMA controller is ready to accept new data.
  - `o_wr_cyc`, `o_wr_stb`: Control signals for the Wishbone interface indicating a write cycle and a data strobe.
  - `o_wr_we`: Write enable signal.
  - `o_wr_addr`: Specifies the address in the memory where data will be written.
  - `o_wr_data`: The actual data to be written to memory.
  - `o_wr_sel`: Byte select signal, indicating which bytes in the word will be written.

#### Behavior of the Module:
The `zipdma_s2mm` module operates primarily as a data writer to memory based on incoming streams of data. The module coordinates several control signals and logic that handle the following functionalities:

1. **State Management:** The module maintains a state to indicate whether it's idle, busy, or facing an error condition. The `o_busy` output reflects the current state and prevents multiple writes from overlapping unless explicitly allowed.

2. **Control Logic for Writes:**
   - On `i_request`, if the DMA is not busy, it initializes a write operation by asserting `o_wr_cyc` and `o_wr_stb`, indicating that a write is being requested on the Wishbone bus.
   - It uses the `i_size` input to determine how many bytes must be transferred at once. The `i_addr` is updated based on `i_inc` after each write operation.
   - The `S_VALID` and `S_LAST` signals help the module manage when the stream is valid and when the last piece of data has been processed, respectively.

3. **Error Handling:** The `o_err` signal can be asserted to indicate an error condition, such as misalignment when the address is not suitable for the requested write size.

4. **Describing Behavior of Transfers:** It processes data coming in via the stream interface, checking bounds defined by the parameters for the incoming data size and writing it properly aligned to the Wishbone bus.

In summary, the `zipdma_s2mm` acts as a critical component in enabling efficient data transfer from an incoming stream to the memory system, managing addressing, control signals, and data alignment within a synchronous clocked environment typical of digital hardware design.

### File: zipdma_rxgears.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma_rxgears.v
Certainly! Here’s a detailed description of the `zipdma_rxgears.v` Verilog file based on the provided information:

### Overall Purpose
The `zipdma_rxgears.v` file implements a gearbox module as part of a DMA (Direct Memory Access) system for the Zip CPU architecture. Its primary purpose is to pack received data from an incoming stream before it is stored into a FIFO (First In First Out) structure. This packing helps in the alignment process by handling how the data is formatted and structured as it transitions between various system components.

### Inter-module Relationships
The `zipdma_rxgears` module interacts with multiple components within the Zip CPU architecture, specifically:
- **FIFO Module:** The packed data produced by the `zipdma_rxgears` module is intended for insertion into a FIFO structure, which manages the order and access of data in the system.
- **DMA Controller:** It works closely with the DMA controller to handle incoming streams of data, ensuring that the data is correctly packed and passed downstream for further processing and eventual transmission back to the bus.

### Key Signals
1. **Inputs:**
   - `i_clk`: Clock signal for synchronous operation.
   - `i_reset`: Active signal to reset the module.
   - `i_soft_reset`: Signal for initiating a soft reset.
   - `S_VALID`: Indicates that the incoming data is valid.
   - `S_READY`: Indicates that the module is ready to receive data.
   - `S_DATA`: The actual data being received with a width defined by `BUS_WIDTH`.
   - `S_BYTES`: The number of valid bytes in `S_DATA`.
   - `S_LAST`: Indicates if this is the last piece of data in the incoming stream.

2. **Outputs:**
   - `M_VALID`: Indicates that the packed data is valid and ready to be sent out.
   - `M_READY`: Indicates that the downstream component is ready to accept the data.
   - `M_DATA`: The packed data ready to be sent downstream.
   - `M_BYTES`: The number of valid bytes in the packed data.
   - `M_LAST`: Indicates if this packed data is the last piece to be transmitted.

### Module Behavior
The behavior of the `zipdma_rxgears` module can be summarized as follows:

- **Packing Logic**: 
  - The module maintains a fill state (tracked using the `fill` and `next_fill` registers) that accounts for the amount of valid data currently in the packing buffer.
  - Whenever valid incoming data (`S_VALID` is high) is detected and the module is ready to receive (`S_READY` is high), the module updates its state by adding the size of the incoming data (`S_BYTES`) to the fill count.
  - Conversely, when the packed data is sent out and acknowledged by the downstream module (`M_VALID` and `M_READY` are both high), it decrements the fill count accordingly. 

- **Control State Management**: 
  - The ranges of `next_fill` are monitored for conditions such as the incoming data being valid or whether it's the last data piece. This is crucial for ensuring that data is processed and transmitted correctly.
  - The module is expected to manage its internal state effectively to provide a consistent and reliable interface between the data sources and the FIFO buffer.

Overall, this module plays a critical role in the data handling and transfer process within the Zip CPU system by ensuring that data integrity is maintained while being transferred into the FIFO structure. Its efficiency in data packing contributes to the overall performance of the DMA operations concerning the CPU architecture.

### File: zipdma_mm2s.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma_mm2s.v
### Analysis of the Verilog file: zipdma_mm2s.v

#### Overall Purpose
The `zipdma_mm2s.v` file implements the "Memory to Stream" (MM2S) component of a Direct Memory Access (DMA) controller for the Zip CPU architecture. Its primary responsibility is to read data from memory and prepare it for transmission on an outgoing data stream, ensuring that the data is correctly aligned and ready for further processing.

#### Inter-module Relationships
The `zipdma_mm2s` module interacts with several other components in the CPU architecture:

1. **DMA Controller**: Acts as a slave to a system bus, coordinating reads from system memory.
2. **Memory Interface**: Interacts with the memory (through read cycles and addressing) to fetch data.
3. **Stream Interface**: Outputs the data to be processed downstream, ensuring that the data complies with the necessary streaming protocols.

The module's outputs are used by other components that may require data as part of a larger operation (such as data processing units or buffering mechanisms).

#### Key Signals (Inputs/Outputs)
##### Inputs:
- `i_clk`: Clock signal for synchronous operation.
- `i_reset`: Resets the internal state of the module.
- `i_request`: Indicates a request for a DMA transfer.
- `i_inc`: Indicates if the address should be incremented after a transfer.
- `i_size`: Specifies the number of bytes to transfer per beat.
- `i_transferlen`: Length of the transfer in bytes.
- `i_addr`: The byte-address from where to start reading in memory.

##### Outputs:
- `o_busy`: Indicates if the module is currently busy performing a read operation.
- `o_err`: Reports any errors that occur during the operation.
- `o_rd_cyc`: Signals a read cycle is active to the memory interface.
- `o_rd_stb`: Indicates a read strobe is issued.
- `o_rd_addr`: The address from which data should be read.
- `o_rd_sel`: Selects the corresponding byte lanes for the read operation.
- `M_VALID`: Indicates that the data on `M_DATA` is valid.
- `M_DATA`: The actual data being read out to the stream.
- `M_BYTES`: Indicates how many bytes of `M_DATA` are valid.
- `M_LAST`: Indicates whether the current data is the last piece being sent in the outgoing stream.

#### Behavior of the Module
The `zipdma_mm2s` module operates using finite state machine (FSM) logic to manage its various states throughout the data transfer process. 

1. **Initialization/Reset**: Upon reset, the module initializes its internal registers and flags.
2. **Request Handling**: When `i_request` is asserted, the module transitions to a busy state (`o_busy` = 1) and begins setting up for a memory read operation.
3. **Memory Read Cycle**:
   - The module asserts `o_rd_cyc` and `o_rd_stb` to initiate a read cycle. 
   - It calculates the address to read from based on the provided `i_addr`, considering address increments if `i_inc` is set.
   - It specifies which bytes should be read using `o_rd_sel`.
   - The data read from memory is captured into internal registers when acknowledged by the memory (`i_rd_ack`).
4. **Data Transmission**: 
   - The valid data is sent out on the `M_DATA` line with `M_VALID` asserted when data is available.
   - The number of valid bytes is communicated through `M_BYTES`, while `M_LAST` indicates if the current data is the last in the stream.
5. **Error Handling**: If an error is detected during the operation (`i_rd_err`), the `o_err` flag will be asserted, and the module can enter a recovery state or halt further operations until reset.

The module cycles through these states, managing its internal logic to ensure efficient and correct data transfer from memory to the streaming output based on ongoing requests and operational feedback.

### File: zipdma_txgears.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma_txgears.v
### Overall Purpose of the File
The `zipdma_txgears.v` file implements a component called ZipDMA, which is designed to unpack bus data words into a specified number of bytes (1, 2, 4, or more) per outgoing data word. This functionality is crucial for supporting peripherals that require byte-specific data transfers, as well as for interacting with memory systems that may not impose such restrictions. The module facilitates flexible data width communication between system buses and peripherals, optimizing data transfer efficiencies across the CPU.

### Inter-module Relationships
The `zipdma_txgears` module interacts with other components within the CPU architecture by providing a bridge between the incoming data stream and outgoing data stream interfaces. It acts upon data provided by upstream components (potentially other DMA controllers, the CPU core, or memory buses) and prepares outgoing data for downstream devices that may require differently sized data transactions. Specifically, it connects to:
- **Incoming Stream Interface**: receives data and control signals from previous elements in the data pathway.
- **Outgoing Stream Interface**: sends processed data to downstream peripherals or modules, ensuring the correct byte alignment and size for each transaction.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_clk`: The clock signal that synchronizes the operations of the module.
  - `i_reset`: A reset signal that initializes or resets the internal state of the module.
  - `i_soft_reset`: An additional reset signal specifically for soft resets.
  - `i_size`: Two bits indicating the size of the data transfer.
  - `S_VALID`: Indicates that the input data is valid.
  - `S_READY`: Indicates that the module is ready to accept data.
  - `S_DATA`: The actual data bus carrying the input data.
  - `S_BYTES`: The number of valid bytes in the incoming data.
  - `S_LAST`: Marks the last piece of data in a stream.

- **Outputs**:
  - `M_VALID`: Indicates that the output data is valid.
  - `M_READY`: Signal from a downstream component that informs whether it is ready to accept new data.
  - `M_DATA`: The data bus carrying the output data.
  - `M_BYTES`: The number of valid bytes in the outgoing data stream.
  - `M_LAST`: Signifies whether the last piece of output data has been sent.

### The Behavior of the Module
The behavior of `zipdma_txgears` is primarily governed by a state machine mechanism that processes incoming data and facilitates outgoing data transfers based on the state of various signals. Here are the key aspects of its behavior:

- **Initialization**: Upon reset (either a hard reset or soft reset), the internal registers for incoming data (`sreg`) and the byte count (`fill`) are initialized to zero.

- **Data Handling**:
  - When `S_VALID` and `S_READY` are both high, the module captures incoming data (`S_DATA`) and the valid byte count (`S_BYTES`).
  - If `M_VALID` and `M_READY` indicate that the module is ready to send data, it processes the outgoing data accordingly:
    - If `M_LAST` is asserted, both `sreg` and `fill` are reset to zero.
    - The byte transfer capability is adjustable according to the specified `OPT_LITTLE_ENDIAN` parameter, with potential behavior defined (though not fully detailed in the provided snippet).

- **Control Logic**: 
  - `M_VALID`, `M_BYTES`, and `M_LAST` are derived based on the states associated with the processing of incoming and outgoing streams, regulating the flow of data and ensuring that the interface operates correctly according to the configuration dictated by `i_size`.

In summary, the `zipdma_txgears` module plays a fundamental role in managing data flows within a Zip CPU architecture, ensuring that data integrity and formatting requirements are adhered to when transferring information between various system components. It achieves this with a combination of state-based control logic and direct signal processing related to incoming and outgoing data streams.

### File: zipdma_ctrl.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma_ctrl.v
### Description of the Verilog File: `zipdma_ctrl.v`

#### Overall Purpose
The `zipdma_ctrl.v` file implements the control logic for a Direct Memory Access (DMA) engine within the Zip CPU architecture. This module is responsible for handling control requests related to DMA operations, interfacing via a 32-bit Wishbone bus. The control logic manages status reads and control writes, facilitating data transfers between memory and peripherals while accommodating various DMA configurations and operations.

#### Inter-module Relationships
The `zipdma_ctrl` module interacts with several other modules in the Zip CPU architecture, including:

- **DMA Engine**: It generates requests for data transfer (DMA request) and aborts those requests when necessary. 
- **Memory Access**: It provides source and destination addresses for DMA operations and communicates length parameters for transfers.
- **Interrupt Controller**: It can indicate when a DMA operation has completed via an interrupt signal (o_interrupt).
- **Status Feedback**: It reads feedback status signals such as `i_dma_busy` and `i_dma_err`, indicating ongoing operations or errors in the DMA controller's behavior.

The primary purpose of these interactions is to streamline data movement processes between memory and various peripherals, thus reducing CPU overhead during such tasks.

#### Key Signals (Inputs/Outputs)
1. **Inputs**:
    - `i_clk`: Clock signal for synchronous operations.
    - `i_reset`: Reset signal to initialize the state of the module.
    - `i_cyc`, `i_stb`, `i_we`: Control signals indicating the status of the Wishbone bus transaction.
    - `i_addr`: Address input for control registers.
    - `i_data`: Data input for control writes.
    - `i_sel`: Byte-select signals to indicate which part of the data bus is active.
    - `i_dma_busy`, `i_dma_err`: Input signals from the DMA engine indicating its busy state and error status.
    - `i_current_src`, `i_current_dst`: Current source and destination addresses for ongoing transfers.
    - `i_remaining_len`: Length of data remaining to be transferred.
    - `i_dma_int`: Interrupt input specific to DMA events.

2. **Outputs**:
    - `o_stall`: Signal indicating the need to stall the current operation.
    - `o_ack`: Acknowledge signal indicating that a control transaction was successful.
    - `o_data`: Data output for read transactions.
    - `o_dma_request`: Request signal sent to the DMA engine to initiate a transfer.
    - `o_dma_abort`: Signal to abort the current DMA transfer.
    - `o_src_addr`, `o_dst_addr`: Registers for the source and destination addresses of the DMA transfer.
    - `o_length`: Length of the data to transfer.
    - `o_transferlen`: Length used for transfers (potentially includes initialization data).
    - `o_mm2s_inc`, `o_s2mm_inc`: Increment signals for memory-to-Slave and Slave-to-memory transfers.
    - `o_mm2s_size`, `o_s2mm_size`: Size signals for memory-to-Slave and Slave-to-memory transfers.
    - `o_trigger`: Indicates a trigger event occurring in the DMA process.
    - `o_interrupt`: Interrupt output to signal the CPU when DMA operations have completed or encountered an error.

#### Behavior of the Module
The `zipdma_ctrl` module primarily behaves as a state-driven controller handling DMA operations. 

1. **Control Logic**: The control logic is designed to accept requests through the Wishbone interface. Depending on the inputs, the control logic can request a DMA transfer by setting `o_dma_request` to high. 

2. **State Management**: The module likely implements various internal states managed by local registers like `r_err`, `r_busy`, etc. When the `i_dma_busy` signal indicates the DMA engine is active, the controller may enter a busy state and refrain from issuing new requests until the current operation is completed.

3. **Error Handling**: The module checks for error conditions through the `i_dma_err` signal, which may trigger an abort request or set an interrupt signal to inform the CPU of the error.

4. **Triggering Transfers**: The `o_trigger` signal is used to inform the peripheral interface of a transfer initiation, while the `o_length` and address outputs are prepared based on the details provided via the Wishbone bus.

5. **Ack and Data Outputs**: When a control transaction is completed, the module provides an acknowledgment (`o_ack`) and can output data (`o_data`) for status reads, effectively handling bidirectional communication via the bus interface.

In summary, `zipdma_ctrl.v` serves as the brain of the DMA operation, managing signal flows, handling Read/Write actions through the Wishbone interface, and ensuring efficient communication between the CPU and memory peripherals.

### File: zipdma_fsm.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma_fsm.v
### Overall Purpose of the File
The `zipdma_fsm.v` file implements the finite state machine (FSM) for controlling the ZipDMA (Direct Memory Access) operations of a CPU architecture. Its primary function is to manage DMA transactions over the Wishbone bus, which cannot handle simultaneous read and write operations. Therefore, this FSM orchestrates the sequence of read and write requests necessary for efficient DMA transfers, breaking down larger transfers into manageable segments.

### Inter-module Relationships
The `zipdma_fsm` module interacts with several other modules within the Zip CPU ecosystem:
- **zipdma_mm2s and zipdma_s2mm**: These modules are responsible for memory-to-stream and stream-to-memory transfers, respectively. The FSM sends requests to these controllers and awaits their completion before proceeding with further operations.
- **Memory Controller**: It communicates with the memory subsystem to perform the actual read and write operations based on the addresses specified by the FSM.
- **Input Signals from CPU**: The FSM receives various control signals such as requests and addresses from the CPU to manage DMA operations effectively.

### Key Signals (Inputs/Outputs)
#### Inputs:
- `i_clk`: The clock signal for synchronizing the operations of the FSM.
- `i_reset`: A reset signal that initializes the FSM.
- `i_soft_reset`: A softer reset that may allow for quicker resets without full reinitialization.
- `i_dma_request`: A signal indicating a new DMA transaction request has been initiated.
- `i_src_addr`: The source address for the DMA transfer.
- `i_dst_addr`: The destination address for the DMA transfer.
- `i_length`: The length of the DMA transfer.
- `i_transferlen`: The transfer length for the DMA operations.
- `i_trigger`: This signal might indicate an event to trigger the FSM for starting the operation.

#### Outputs:
- `o_dma_busy`: A state signal indicating if a DMA transfer is currently in progress.
- `o_dma_err`: An error signal indicating whether an error occurred in the DMA process.
- `o_mm2s_request`: A signal used to request a read operation from the MM2S controller.
- `o_mm2s_addr`: The address to be used for the MM2S operation.
- `o_s2mm_request`: A signal indicating that a write request to the S2MM controller should be made.
- `o_s2mm_addr`: The address for the S2MM write operation.
- `o_remaining_len`: The length of the remaining data to be transferred.

### Behavior of the Module
The `zipdma_fsm` contains control logic that handles the state transitions based on various input signals and the current state of the DMA transfer. The module likely has a state machine structure with states such as:
1. **Idle State**: Waiting for a DMA request.
2. **Requesting State**: Sending requests to the MM2S and S2MM modules.
3. **Busy State**: Managing the ongoing DMA transfer, involving checks for busy signals and for potential errors from the MM2S and S2MM controllers.
4. **Completion State**: Handling the completion of transfers and preparing for the next request, updating the remaining length, and managing any errors that might have been detected.

The FSM will transition between these states based on input signals like `i_dma_request`, the `i_mm2s_busy`, and `i_s2mm_busy` signals, controlling the operations of the DMA based on the state of the MM2S and S2MM controllers until all operations complete successfully or an error is detected.

### File: zipdma.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma.v
### Overall Purpose of the File
The `zipdma.v` file implements a Direct Memory Access (DMA) controller for the Zip CPU architecture. Its purpose is to facilitate efficient data transfers between main memory and peripherals, minimizing CPU intervention and thus allowing the CPU to perform other tasks while data is being transferred. This upgraded version of the Wishbone DMA controller enhances the data transfer capabilities of the Zip CPU, making it suitable for modern applications where efficient data handling is crucial.

### Inter-Module Relationships
The `zipdma` module interacts with several other components in the Zip CPU architecture:

- **Master and Slave Ports**: The module has both a slave interface (for control communication) and a master interface (for data transfers). It interacts with other modules through the Wishbone interface, allowing it to receive commands, send data, and handle acknowledgment and error signals from other components in the bus architecture.

- **Interrupt Handling**: It receives interrupt signals from associated devices and generates an interrupt output to indicate when a DMA operation has completed. This allows the CPU to react to DMA completion asynchronously.

- **Data Structures**: The module may interact with memory elements to store or retrieve data being transferred but will do so transparently through the bus rather than directly interacting with memory modules.

### Key Signals (Inputs/Outputs)

#### Inputs:
- `i_clk`: Clock signal for sequential logic.
- `i_reset`: Reset signal to initialize the module.
- **Slave Interface**:
  - `i_swb_cyc`: Cycle signal to indicate a transaction is initiated.
  - `i_swb_stb`: Strobe signal indicating valid data is present.
  - `i_swb_we`: Write enable signal (indicates direction of data transfer).
  - `i_swb_addr`: Address signal for slave address space.
  - `i_swb_data`: Data input for write operations.
  - `i_swb_sel`: Byte select signals for the write operation.
- **Master Interface**:
  - `i_mwb_stall`: Indicates if the bus is busy (master should wait).
  - `i_mwb_ack`: Indicates acknowledgment from the target.
  - `i_mwb_data`: Data input from the master interface.
  - `i_mwb_err`: Error indication from the master interface.
- `i_dev_ints`: Interrupt signals from peripheral devices.

#### Outputs:
- **Slave Interface**:
  - `o_swb_stall`: Stall output to manage the slave bus protocol.
  - `o_swb_ack`: Acknowledgment output to indicate a successful control transfer.
  - `o_swb_data`: Data output for read operations.
- **Master Interface**:
  - `o_mwb_cyc`, `o_mwb_stb`, `o_mwb_we`: Control signals for initiating transactions as a DMA master.
  - `o_mwb_addr`: Address signal for the master transfer.
  - `o_mwb_data`: Data output for the transfer.
  - `o_mwb_sel`: Byte enable signals for the master transfer.
- `o_interrupt`: Indicates when an operation is completed and can trigger further CPU actions.

### Behavior of the Module
The `zipdma` module contains control logic that governs its behavior during DMA operations. Key features include:

- **State Machine**: The module likely implements a state machine to handle various states of a DMA request (idle, active, waiting, complete, error). This controls the flow of the transaction based on the inputs it receives and coordinates the transitions between different states as the DMA operation progresses.

- **Request Handling**: When the DMA request is made through the slave interface, the module initiates a cycle and uses control signals to manage the transfer process correctly.

- **Error Handling**: The module checks for various error conditions (like bus stalls and acknowledgment failures) and sets an error state if needed. It uses the `dma_err` signal to communicate errors to other components.

- **Interrupt Generation**: Upon the completion of the data transfer, the module asserts the `o_interrupt` signal, which serves to notify the CPU or other system components that the operation is complete.

Overall, the `zipdma` module is essential for efficient data management within the Zip CPU architecture, allowing for concurrent processing while data transfers occur seamlessly in the background. Its interaction with the Wishbone bus and handling of interrupts plays a critical role in its operation within a wider system context.

### File: cpuops.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/cpuops.v
### Overview of the `cpuops.v` Verilog File

#### Purpose
The `cpuops.v` file implements the Arithmetic Logic Unit (ALU) operations for the Zip CPU, which is a lightweight, RISC (Reduced Instruction Set Computing) soft core. The ALU in this module manages the execution of various instruction opcodes (specifically opcodes 0-13) related to arithmetic and logic functions, excluding divide operations (which are handled elsewhere).

#### Inter-module Relationships
The `cpuops` module interacts with various other components within the CPU architecture, including:
- **Instruction Fetch Stage**: It receives operation codes (opcodes) from the instruction decoder, likely provided by modules such as `f_idecode` or `idecode`.
- **Registers**: It utilizes input registers (like `i_a` and `i_b`) for data operation inputs, which are presumably connected to register files or data buses.
- **Execution Control**: It communicates with other control logic modules, such as decode and execution units, to indicate when operations are valid and when the unit is busy (`o_busy`).

The outputs may also feed into components that handle the next steps in the execution pipeline, indicating the results of arithmetic operations or status signals.

#### Key Signals
- **Inputs**:
  - `i_clk`: System clock input.
  - `i_reset`: Reset signal for module initialization.
  - `i_stb`: Strobe signal to indicate that the inputs are valid and should be processed.
  - `i_op[3:0]`: Opcode input specifying the operation to be performed.
  - `i_a[31:0]`, `i_b[31:0]`: Data inputs for operations (e.g., operands for addition, multiplication).
  
- **Outputs**:
  - `o_c[31:0]`: Result of the arithmetic or logic operation.
  - `o_f[3:0]`: Output flags that may represent status information (e.g., zero flag, overflow flag).
  - `o_valid`: Indicates whether the output result is valid.
  - `o_busy`: Indicates whether the ALU is currently processing an operation, critical for managing pipeline flow.
  
  - Additionally, debug outputs (defined under `VMPY_TB`) provide insight into internal signals and can be utilized for testing purposes without affecting synthesis.

#### Behavior
The behavior of the `cpuops` module encompasses several features:
1. **Arithmetic Operations**: It executes basic arithmetic operations based on the opcode provided. The core logic utilizes combinational logic to compute results based on the specific operations defined by the `i_op` signals.
  
2. **Flag Generation**: The outputs may include flag signals that denote the status of the operation, such as whether the result is zero, negative, or has overflowed.

3. **State Management**: There is a mechanism to indicate when the ALU is busy processing operations (`o_busy`), which is essential for ensuring that subsequent operations do not overlap with ongoing calculations.

4. **Conditional Logic**: Depending on specified parameters (like `OPT_SHIFTS`), the module can include or exclude certain functionalities (like shift operations). This gives the ALU flexibility in managing various instruction types based on configuration.

5. **Multiplication Handling**: If configured (controlled by `OPT_MPY`), it has provisions for handling multiplication operations, checking for whether a multiplication is in process (`mpybusy`, `mpydone`).

Overall, the `cpuops.v` file serves as a fundamental building block of the Zip CPU's execution unit, defining the core computation capabilities while ensuring compatibility and integration with other elements of the CPU pipeline.

### File: axilpipe.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axilpipe.v
### Purpose of the File
The `axilpipe.v` file implements a memory unit designed to support a CPU architecture based on the AXI-lite protocol. This module is capable of handling multiple concurrent requests, allowing outstanding memory operations, unlike simpler AXI interfaces that might manage only single requests. It provides a bridge between the CPU and memory, facilitating data transfers while obeying AXI-lite specifications.

### Inter-module Relationships
The `axilpipe` module interacts with:
- The CPU core, which sends requests to this memory unit (over signals like `i_stb`, `i_op`, `i_addr`, etc.) and expects responses (via `o_result`, `o_valid`, etc.).
- It acts as a mediator between the CPU’s operational commands and system memory, handling memory reads, writes, and any necessary error signaling.
- Other components in the system (possibly including caching mechanisms and higher-level memory controllers) may also rely on its behavior to maintain smooth memory access patterns and handle synchronization.

### Key Signals (Inputs/Outputs)
**Inputs:**
- `S_AXI_ACLK`: Clock signal for synchronization.
- `S_AXI_ARESETN`: Active-low reset signal for initialization.
- `i_cpu_reset`: Reset signal used to reset the CPU state.
- `i_stb`: Request signal indicating that the CPU is ready to process a memory operation.
- `i_lock`: Indicates if the operation should be atomic.
- `i_op`: Operation code specifying the type of operations (e.g., read, write).
- `i_addr`: Address for the memory operation.
- `i_data`: Data to be written in case of a write operation.
- `i_oreg`: Register index used for operation results.

**Outputs:**
- `o_busy`: Indicates the status of the memory operation, signaling when the unit is busy.
- `o_pipe_stalled`: Indicates if the pipeline should be stalled.
- `o_rdbusy`: Indicates if a read operation is currently in progress.
- `o_valid`: Indicates that the results of an operation are now valid.
- `o_err`: Error flag for signaling unsuccessful operations.
- `o_wreg`: Specifies which register the result should be written to.
- `o_result`: The result of memory operations.

### Behavior of the Module
The `axilpipe` module's behavior includes a state machine that manages the state of the memory operations. Key aspects include:
- **Request Handling:** When the CPU signals with `i_stb`, the module starts processing the request based on `i_op` and other inputs.
- **Concurrent Operations:** It supports handling multiple outstanding requests by managing internal states and queues, which allows for better CPU efficiency.
- **Response Control:** It sets outputs like `o_valid` and `o_result` when the operation is complete, providing feedback to the CPU.
- **Error Handling:** It includes logic to detect and signal errors using `o_err`, ensuring the CPU can handle any fault conditions gracefully.
- **Stalling and Busy Control:** The module includes mechanisms to assert `o_busy` and `o_pipe_stalled` to control the flow in the CPU pipeline, ensuring it works seamlessly with the instruction fetch and decode stages.
  
Through these functionalities, the `axilpipe` effectively bridges CPU requests and memory accesses, ensuring compliance with AXI-lite protocol while supporting efficient multitasking for memory operations.

### File: axidcache.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axidcache.v
### Purpose of the file
The `axidcache.v` file implements a data cache module for a CPU, utilizing the AXI (Advanced eXtensible Interface) protocol as its underlying communication mechanism. This cache module is designed to store and retrieve data efficiently, reducing access times to memory and improving overall system performance. The design is part of the Zip CPU architecture, a lightweight RISC CPU soft core developed by Gisselquist Technology.

### Inter-module Relationships
The `axidcache` module interacts with various components within the CPU architecture, particularly those associated with memory transactions over the AXI protocol. This includes, but is not limited to:
- **CPU core**: The cache serves as an intermediary between the CPU core and main memory, storing data for quick retrieval when the CPU issues requests.
- **AXI Master and Slave modules**: It likely interfaces with AXI master modules for issuing read/write commands, and with AXI slave modules for receiving data.
- **Memory Controller**: The cache would interface with a memory controller to fetch data in case of cache misses, ensuring data coherence and efficient memory access.
- **Cache Management Logic**: The design might also interact with cache management modules or components responsible for handling cache coherence and replacement policies.

### Key Signals (Inputs/Outputs)
The following are some key signals typically associated with the `axidcache` module:

- **Inputs**
  - `i_clk`: The clock signal for synchronizing operations.
  - `i_reset`: A reset signal to initialize the cache.
  - `axi_addr`: The address signal that indicates where the read/write is targeted.
  - `axi_data`: Data input for write operations.
  - `axi_write`: A control signal indicating when to write data.
  - `axi_read`: A control signal indicating when to perform a read operation.
  - Other AXI-specific signals such as `axi_valid`, `axi_ready`, etc.

- **Outputs**
  - `axi_read_data`: Data output from the cache when a read operation is completed.
  - `axi_response`: Signals the status (success or error) of the transactions.
  - `cache_hit`: An indication whether the requested data was found in the cache.
  - `cache_miss`: An indication that the requested data was not found in the cache, prompting a fetch from main memory.
  - `out_axi_ready`: Indicates when the cache is ready for the next transaction.

### Behavior of the Module
The `axidcache` module employs various control logic and potentially utilizes state machines to manage cache operations. General behaviors include:

1. **Fetching Data**: When a read operation is initiated, the module checks if the requested address is present in the cache (cache hit). If found, the data is retrieved immediately, and the operation is completed without involving the slower main memory.

2. **Handling Cache Misses**: If a cache miss occurs, the module generates a request to the main memory (or an upstream component) to retrieve the necessary data. Once the data is received, it is stored in the cache, and the read operation is completed.

3. **Cache Write Operations**: When a write is requested, the cache updates its data accordingly. Depending on the cache architecture, this might involve writing into the cache and possibly invalidating or updating affected lines.

4. **State Machine Logic**: The module likely features state machines to handle different phases of operations (idle, read, write, fetching data), managing transitions between these states based on the incoming signals and AXI protocol requirements.

5. **Sign Extension**: If `OPT_SIGN_EXTEND` is enabled, values returned to the CPU that are less than the width of a word are sign-extended, ensuring correctness in data representation.

Overall, the `axidcache` module encapsulates the essential behaviors for a functioning data cache within a CPU, optimizing performance through hierarchical data access strategies utilizing the AXI protocol. It’s crucial for improving data throughput and reducing latency in overall system performance.

### File: zipcore.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/zipcore.v
### Purpose of the File

The `zipcore.v` file implements a small, lightweight RISC CPU core known as the Zip CPU. It serves as the fundamental processing unit of the CPU architecture, incorporating features such as instruction fetching, execution, and handling interrupts. The design utilizes a range of parameters to configure the CPU's characteristics, such as address width, reset address, and optional features like multipliers, dividers, and debugging ports.

### Inter-module Relationships

The `zipcore` module interacts with multiple other modules in the CPU architecture:

- **Instruction Fetch Modules**: It connects with instruction fetch modules that request and validate instructions from memory, using signals like `o_pf_request_address`, `i_pf_valid`, and `i_pf_illegal` to manage instruction requests and their legality.
- **Debug Interface**: Provides a debug port that allows external tools or CPUs to halt, clear caches, and access CPU registers. It outputs various debug signals, including `o_dbg_stall`, `o_dbg_reg`, and `o_break`.
- **Peripheral Interfaces**: The core may interact with peripheral modules through bus interfaces for reading/writing data.
- **Control Logic**: Works in conjunction with control modules that handle execution states, branching, and cache management.
- **Memory Interface**: Communicates with memory modules for instruction cache management, indicated by control signals like `o_clear_icache` and `o_clken`.

### Key Signals (Inputs/Outputs)

#### Inputs
- `i_clk`: Clock signal for synchronous operation.
- `i_reset`: Reset signal to initialize the CPU state.
- `i_interrupt`: Indicates if an interrupt occurred, prompting the CPU to handle it.
- `i_halt`: Signal to pause the CPU operation for debugging.
- `i_clear_cache`: Command to clear the instruction cache.
- `i_dbg_wreg`, `i_dbg_we`, `i_dbg_data`, `i_dbg_rreg`: Signals involved in the debugging interface to write/read registers.
- `i_pf_valid`, `i_pf_illegal`: Signals indicating the validity and legality of fetched instructions.

#### Outputs
- `o_clken`: Clock enable signal for peripheral components to optimize power usage.
- `o_pf_new_pc`: Indicates a new program counter value for instruction fetching.
- `o_clear_icache`: Command to clear the instruction cache.
- `o_pf_ready`: Status indicator that the instruction fetch is ready.
- `o_pf_request_address`: Address requested for instruction fetching from the instruction cache.
- `o_dbg_stall`, `o_dbg_reg`: Outputs for debug operations indicating stall conditions and register values.
- `o_dbg_cc`: Debug condition code.
- `o_break`: Indicates a break condition in the debug interface.

### Behavior of the Module

The behavior of the `zipcore` module includes the following:

- **Instruction Fetching**: The core manages the fetching of instructions through signals that control the program counter and the cache's state. The control logic determines when to clear the cache or request new instructions.
- **Debug Control**: The debug interface allows monitoring and control of the CPU's internal state. The module processes debug commands to halt execution, read/write registers, and check status flags.
- **Response to Interrupts**: It handles interrupts by invoking specific control logic that prioritizes interrupt servicing and prepares execution states.
- **Conditional Execution**: Incorporating various optional features based on the parameters set during instantiation, like early branching and pipeline support, which influence how instructions are executed.
- **State management**: Implements state machines for managing different operating conditions—normal operation, halted state (for debugging), and responding to interrupts.

In summary, the `zipcore` module is the heart of a RISC CPU that organizes instruction handling, debugging, and integration with peripheral components, enabling efficient CPU operations.

### File: slowmpy.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/slowmpy.v
### Purpose of the File:
The `slowmpy.v` file implements a multiply unit for a lightweight RISC CPU called Zip CPU. This module can perform both signed and unsigned multiplication, depending on the configuration set by the parameter `OPT_SIGNED`. It is specifically designed for low logic usage and operates slower than other multiplication algorithms, taking one clock cycle per bit plus two additional cycles to complete the operation.

### Inter-module Relationships:
The `slowmpy` module interacts with other components of the Zip CPU architecture primarily through its input/output signals. It connects to the CPU core's datapath, likely providing multiplication results to be used in various arithmetic operations performed by the ALU or other components. The outputs of this module, such as the multiplication result and control signals (`o_done`, `o_busy`), inform downstream modules when the multiplication is complete or when the module is processing a multiplication request.

### Key Signals:
#### Inputs:
- `i_clk`: The clock signal that drives the sequential logic within the module.
- `i_reset`: A signal used to reset the internal state of the module.
- `i_stb`: A strobe input indicating that the multiplication operation should start.
- `i_a`: The first operand for multiplication (signed, width NA).
- `i_b`: The second operand for multiplication (signed, width NB).
- `i_aux`: An auxiliary input utilized for additional functionalities during operation.

#### Outputs:
- `o_busy`: This output signal indicates whether the multiplier is currently in operation.
- `o_done`: This output signal asserts when the multiplication operation has completed.
- `o_p`: The resultant product of the multiplication, with a width of `NA + NB - 1`.
- `o_aux`: An auxiliary output that can be used for additional features.

### Behavior of the Module:
The `slowmpy` module operates in a sequential manner controlled by the clock signal. It processes multiplication requests as follows:

1. **Initialization**: Upon reset (`i_reset`), the multipliers' internal state (including `aux`, `o_done`, and `o_busy`) is cleared.

2. **Processing**: Once enabled (i.e., when `o_busy` is low and `i_stb` is asserted), the process begins:
   - The module starts counting the number of bits required for multiplication (`count`) using a register, and the operands are prepared in their respective registers (`p_a`, `p_b`).
   - The actual multiplication takes place in a iterative manner based on the bits of the multiplier (`i_b`), shifting and adding appropriately.

3. **Control Logic**: 
   - A variable `almost_done` is used to facilitate the detection of the completion state without immediately setting `o_done`, allowing for smooth transitions.
   - The logic checks whether all bits have been multiplied and signals when the operation is done (via `o_done`).

4. **State Management**: The module maintains its busy state through the `o_busy` signal until the multiplication is complete (indicated by `o_done`).

In summary, `slowmpy.v` serves as a fundamental piece of the CPU's arithmetic logic, handling multiplication operations with specific characteristics focused on low logic usage and slower signal handling. The overall design promotes versatility in how multiplication results are produced and communicated with other parts of the CPU architecture.

### File: axiops.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axiops.v
Certainly! Here is the analysis of the Verilog file `axiops.v`.

### Overall Purpose of the File
The `axiops.v` file implements a memory unit that supports the AXI4 memory interface for a RISC CPU, specifically the Zip CPU. Its design is aimed at being a lightweight and straightforward implementation of the AXI4 protocol to facilitate communication between the CPU and memory.

### Inter-module Relationships
The `axiops` module interacts with various other components in the CPU architecture:
- **CPU core**: The `axiops` module is likely involved in processing memory requests from the CPU core, handling both read and write transactions.
- **Memory subsystem**: It communicates with the memory subsystem to fetch data or store data based on instructions from the CPU.
- Other AXI-compliant devices are likely interfaced through the `axiops`, such as peripherals and memory controllers that conform to the AXI4 protocol.

### Key Signals (Inputs/Outputs)
The `axiops` module has several parameters and interfaces that define its operation:
1. **Parameters**:
   - `C_AXI_ADDR_WIDTH`: Address width for Axi transactions.
   - `C_AXI_DATA_WIDTH`: Data width for Axi transactions.
   - `C_AXI_ID_WIDTH`: Identifier width for transactions.

2. **Outputs**:
   - Outputs related to the AXI protocol such as `ARREADY`, `RVALID`, `RDATA`, `AWREADY`, `WREADY`, `BVALID`, etc. (The specific signals would be defined in the parts of the module not shown in the provided excerpt).

3. **Inputs**:
   - Inputs related to commands from the CPU and peripheral devices, such as address and data inputs, valid signals, write strobe signals, etc.

### Behavior of the Module
The behavior of the `axiops` module is guided by its interactions as an AXI slave. Here are key points regarding its operation:

- **Protocol Handling**: The module implements the handshake required by the AXI protocol for read and write operations. This involves managing the `VALID` and `READY` signals appropriately to confirm the successful transmission of data.
  
- **Address Processing**: It processes incoming addresses based on parameters like `SWAP_ENDIANNESS` and `SWAP_WSTRB`, which determine how data is arranged and accessed.

- **Control Logic**: The module likely contains state machines that govern its operation state—such as idle, reading, writing, etc. This allows it to coordinate transactions efficiently and respond to the CPU's needs promptly.

- **Endianness Management**: The parameters for endianness swapping are crucial in defining how data is represented and accessed. This allows interoperability in scenarios where the CPU architecture's endianness differs from the AXI bus standard.

Overall, `axiops.v` serves as a critical interface module for enabling memory operations compliant with the AXI4 protocol, facilitating communications between the Zip CPU and memory resources or peripheral devices in the architecture.

### File: axilops.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axilops.v
### Overview of `axilops.v`

**Purpose:**
The `axilops.v` file implements a memory unit that supports the Zip CPU, designed specifically for interfacing using the AXI-Lite protocol. It provides basic memory operations while being efficient in terms of logic utilization. The design allows various configurations, particularly focusing on how data is represented (endianness) and written on the AXI bus.

### Inter-module Relationships:
The `axilops` module interacts with several components within the CPU architecture:

- **Zip CPU Core:** It provides interactions for memory read and write operations, which the CPU core utilizes for instruction fetching and data processing.
- **AXI Interface:** This module serves as an intermediary for the AXI-Lite protocol, converting CPU commands to AXI requests and vice versa. It is designed to work closely with AXI master/slave configurations.
- **Memory Subsystem:** The `axilops` module can be connected to physical memory (such as RAM or ROM) units to manage data transfers between the CPU and memory. 

### Key Signals:
#### Inputs:
- **Address and Data Signals:** These include address signals configured as per the `ADDRESS_WIDTH` and data signals matching the `C_AXI_DATA_WIDTH` (typically 32 bits).
- **Control Signals:** Standard AXI control signals such as `AWVALID`, `AWADDR`, `WVALID`, `WDATA`, `ARVALID`, and others that dictate the validity and nature of read/write operations.
- **Configuration Parameters:** Parameters like `SWAP_ENDIANNESS` and `SWAP_WSTRB` allow for modifying how data is ordered in memory.

#### Outputs:
- **Response Signals:** Outputs include signals like `AWREADY`, `WREADY`, `ARREADY`, `RVALID`, `RDATA`, and others that inform the CPU or other modules of the completion and success/failure of memory operations.
- **Error Signals:** Signals may include outputs that indicate errors in operations (e.g., write or read errors), depending on the AXI protocol requirements.

### Behavior of the Module:
The `axilops` module manages the following behaviors:

1. **Basic Memory Operations:** The module performs read and write operations based on incoming commands from the Zip CPU. It processes these commands adhering to the AXI-Lite protocol. 

2. **Endianness Handling:** Depending on the configuration parameters (`SWAP_ENDIANNESS` and `SWAP_WSTRB`), the module can convert data representations to support both big-endian and little-endian data formats. This is crucial for ensuring proper data interpretation when interfacing with different hardware or software expectations.

3. **State Machine Logic:** The module likely contains control logic, possibly in the form of finite state machines (FSM), to handle the state transitions between idle, address phase, write data phase, and read data phase correctly. This includes managing valid and ready signals appropriately.

4. **Memory Access Control:** It ensures that data integrity is maintained during accesses. The signal handshake facilitated by the AXI protocol (valid and ready signals) synchronizes communication between the CPU and memory, preventing data corruption.

5. **Error Management:** It detects and responds to potential errors during memory transactions, allowing for robust operations within the CPU system. 

In summary, `axilops.v` serves as a vital component of the Zip CPU architecture by enabling memory access while allowing configurability to support different data formats and operation rules through the AXI-Lite interface.

### File: div.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/div.v
### Overview of `div.v`

#### Overall Purpose of the File
The `div.v` file implements an integer division unit for the Zip CPU, capable of handling both signed and unsigned division operations. It effectively manages the division process through a shift-and-subtract algorithm, allowing for a sequential calculation over a series of clock cycles. This unit serves as a fundamental arithmetic operation within the CPU's architecture, providing necessary functionality for various computational tasks.

#### Inter-module Relationships
The `div.v` module is designed to interact with other components of the CPU, specifically:
- **Control Module**: It receives control signals (like `i_wr` for write) from a control unit, indicating when a division operation should commence. Upon receiving this signal, it sets its internal state to busy and prepares to process the division.
- **ALU (Arithmetic Logic Unit)**: The division module provides output to the ALU, making the results of the division available for further processing or combination with other arithmetic operations.
- **Data Path**: This module interacts with the data path of the CPU by receiving operands (dividend and divisor) and outputting the quotient and any status signals.

#### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_clk`: Clock signal for synchronous operation.
  - `i_reset`: Asynchronous reset to initialize the unit and bring it to an idle state.
  - `i_wr`: Write signal that triggers the start of a division operation, indicating that the inputs (dividend and divisor) are ready to be processed.

- **Outputs**:
  - `o_busy`: Indicates whether the division operation is currently in progress. Set to high when a division begins and low when finished.
  - `o_valid`: Signifies that the output (quotient) is valid and can be read. This is low until the division operation concludes.
  - `o_quotient`: The result of the division operation.

#### Behavior of the Module
The division module employs a state-driven approach to divvy up the work over multiple clock cycles:
1. **Idle State**: The module starts in an idle state, where it awaits the `i_wr` signal to initiate a divide operation.
2. **Busy Indication**: Upon asserting `i_wr`, the `o_busy` signal is set high, indicating that the division process has begun.
3. **Sign Handling**: If a signed division is required, it processes integer absolute values of the dividend and divisor while determining the correct sign for the output quotient. This typically involves one cycle for sign adjustment.
4. **Shift-and-Subtract Algorithm**: The actual division employs a series of shifts and subtractions:
   - If the divisor is larger than the current dividend, it shifts the divisor right.
   - When the divisor can be subtracted from the dividend, it does so and marks the respective quotient bit.
   - This process is repeated across 32 cycles, effectively implementing the long division process.
5. **Completion**: After traversing all necessary clock cycles, the quotient is finalized. If the operation was signed, the output may be negated based on the sign determined at the beginning.
6. **Status Update**: On the clock cycle that concludes the operation, the `o_busy` is set low, and `o_valid` is asserted high, indicating readiness for reading the `o_quotient`.

This design ensures a robust and fault-tolerant approach to implementing division, while adhering to the constraints of the Zip CPU’s overall architecture and operational protocols.

### File: pffifo.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/pffifo.v
### Overview of the `pffifo.v` File

#### Purpose of the File:
The `pffifo.v` file implements a prefetch FIFO (First-In-First-Out) buffer for the Zip CPU architecture. Its primary role is to keep the CPU supplied with instructions at a rate of ideally one instruction per clock cycle, which helps minimize stalls. The FIFO design allows it to hold multiple instructions, making it effective for scenarios with fewer branch instructions (i.e., when the program does not experience frequent changes in the control flow).

#### Inter-module Relationships:
- **Interaction with CPU Modules:** The `pffifo` module interacts with various components of the CPU. It receives inputs related to the program counter and cache management, and it outputs valid instructions to be executed. This interaction is crucial for managing instruction flow and maintaining an optimal execution pipeline.
  
- **Integration with Other Prefetch Mechanisms:** It is noted that the `pffifo` design is similar to other prefetch mechanisms, such as the `dblfetch` implementation, suggesting that it might share a common interface or methodology with those modules. This design consideration can enhance reusability and maintainability within the overall CPU architecture.

#### Key Signals:
- **Inputs:**
  - `i_clk`: The clock signal used for synchronization.
  - `i_reset`: Reset signal to initialize the module.
  - `i_new_pc`: Indicates that a new program counter value is present and should be processed.
  - `i_clear_cache`: Signal to clear the contents of the FIFO.
  - `i_ready`: Signals if the FIFO is ready for new instruction data.
  - `i_pc`: The current program counter value that is to be prefetched.

- **Outputs:**
  - `o_valid`: Indicates if the instruction fetched is valid.
  - `o_illegal`: Indicates if the fetched instruction is illegal.
  - `o_insn`: Provides the instruction fetched from the FIFO.
  - `o_pc`: Outputs the program counter value associated with the instruction.
  
- **Wishbone Bus Interface Outputs:**
  - `o_wb_cyc`, `o_wb_stb`: Control signals for the Wishbone bus.
  - `o_wb_we`: Write enable for bus transactions.
  - `o_wb_addr`: Address for the Wishbone bus.
  - `o_wb_data`: Data to be sent over the bus.
  - `o_wb_se`: Select enable signal for the bus.

#### Behavior of the Module:
The `pffifo` module utilizes internal state management and control logic to operate as a prefetch buffer:

- **FIFO Logic:** The module utilizes a FIFO data structure to store prefetched instructions until they are needed by the CPU. The depth of the FIFO is determined by the `LGFIFO` parameter, which could allow storage of multiple instructions.

- **Control Signals Management:** It manages various input signals such as `i_new_pc` to update the prefetch logic with new program counter values, while monitoring `i_ready` to indicate the module's readiness to process new instructions.

- **State Machine Implementation:** While the state machine details are not provided explicitly in the snippet, it can be inferred that it would control transitions between states such as idle, fetching, and providing output. This ensures smooth transitions based on the validity of the fetched instructions and synchronization with the clock.

- **Output Generation:** Upon a successful fetch, valid instructions are output through `o_insn`, with corresponding signals (`o_valid`, `o_illegal`, and `o_pc`) used to inform the CPU about the status and details of the instruction just fetched.

Overall, `pffifo.v` serves a critical role in ensuring the CPU maintains a steady flow of instructions, minimizing stalls that could degrade performance, particularly in environments with consistent instruction flow.

### File: axiicache.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axiicache.v
### Overall Purpose of the File
The file **axiicache.v** implements an instruction cache (I-Cache) designed for a CPU with an AXI (Advanced eXtensible Interface) interface. Its primary purpose is to facilitate quick retrieval of instructions for the CPU, ensuring that each instruction can be returned within a single clock cycle. The module is engineered to minimize latency, especially during branch instructions, thereby improving the overall performance of the CPU.

### Inter-module Relationships
The **axiicache** module interacts with various other components in the CPU architecture, primarily through the AXI interface. It likely interfaces with modules such as:

- **CPU core**: Receiving instructions that need to be fetched.
- **BRAM (Block Random Access Memory)**: Used for storing the instructions, allowing for quick read access.
- **Controller Modules**: Handling AXI communication and managing data transfer to and from the cache.

The interplay between the instruction fetch process and other stages (such as decode and execute) in the CPU pipeline is critical, as the instruction cache must provide timely data for smooth execution flow.

### Key Signals (Inputs/Outputs)
The **axiicache** module has several parameters and signals, though the complete definition is not provided in the snippet. Notably:

#### Inputs:
- **C_AXI_ID_WIDTH**: Specifies the width of the ID field in the AXI transaction.
- **C_AXI_ADDR_WIDTH**: Defines the width of the address bus for the AXI protocol.
- **C_AXI_DATA_WIDTH**: Indicates the width of the data bus used for accessing memory.

#### Outputs:
- The specific output signals are not fully discernible from the snippet provided, but they typically include:
  - **Data Output**: The fetched instruction that will be sent to the CPU core.
  - **Valid/Ready signals**: Indicating the readiness to send data, and whether the received data is valid.

### Behavior of the Module
The behavior of the **axiicache** includes:

1. **Address Processing**: The module processes instruction addresses segmented into three parts: tag bits, cache line number, and cache position within the line. This structure allows the cache to determine whether the desired instruction is already present.

2. **Read Operations**: When the CPU requests an instruction, the cache checks the relevant tag and line number to see if it can quickly return the instruction without needing to access the main memory.

3. **Latency Management**: The design emphasizes avoiding unnecessary checks for cache hits. If the last accessed tag matches the current request, it can return the data immediately, enforcing efficiency by reducing clock cycles needed for instruction fetches.

4. **Stall Control for Branches**: If a jump instruction results in accessing a different cache line, the design may introduce a stall clock cycle to ensure data integrity and correctness.

5. **State Machine Logic**: Though not detailed in the snippet provided, there likely exists control logic in the form of state machines to manage cache states (idle, fetching, valid, etc.) depending on the instruction fetch process and AXI transactions.

Overall, the **axiicache** module plays a crucial role in enhancing the performance of the Zip CPU architecture by mitigating the delay associated with instruction retrieval through diligent cache management.

### File: prefetch.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/prefetch.v
### Description of the `prefetch.v` Verilog File

#### Overall Purpose
The `prefetch.v` file implements a simple instruction fetch mechanism for the Zip CPU architecture. It is designed to retrieve one instruction at a time from memory, providing a basic fetching capability that enables the CPU to perform its instruction cycles. While this implementation is straightforward and does not include pipelining or caching features, its simplicity allows for easy integration and debugging.

#### Inter-module Relationships
The `prefetch` module interacts primarily with the CPU core by fetching instructions that will be decoded and executed by subsequent modules in the pipeline. Specifically, it interfaces with:
- **Control Logic**: The `i_new_pc` signal notifies the `prefetch` module when a new program counter (PC) value is available. It determines whether to use the provided PC address (`i_pc`) to fetch the corresponding instruction.
- **Memory Modules**: The module depends on memory subsystems to retrieve instructions based on the PC value. While it does not contain detailed memory retrieval logic (as this would typically be handled elsewhere), it interacts with memory control signals.
- **Instruction Decode Mechanism**: The fetched instruction is provided to subsequent decode stages, which will interpret the instruction for execution.

#### Key Signals
- **Inputs**:
  - `i_clk`: The clock signal, driving synchronous operations in the module.
  - `i_reset`: A reset signal that sets the module back to its initial state.
  - `i_new_pc`: Indicates that a new program counter value is available for fetching an instruction.
  - `i_clear_cache`: A signal indicating that the instruction cache (if implemented) should be cleared.
  - `i_ready`: A signal indicating whether the CPU is ready to receive the fetched instruction.
  - `i_pc`: The suggested program counter value to fetch the corresponding instruction, provided `i_new_pc` is asserted.
  
- **Outputs**:
  - `o_valid`: Indicates if the output instruction is valid and has been correctly fetched from memory.
  - `o_illegal`: An output that signals whether a fetched instruction corresponds to an illegal operation or an incorrect memory access (for example, due to bus errors).
  - `o_instruction`: The actual instruction fetched from memory (not fully detailed in the abbreviated code, but typically would be defined).

#### Behavior of the Module
The `prefetch` module operates primarily in a synchronous manner with the clock (`i_clk`). Key features of its behavior include:

- **Fetching Logic**: The module checks the `i_new_pc` signal to determine when to fetch instructions. When this signal is asserted, the module utilizes the provided `i_pc` value to load the instruction.
- **Error Handling**: The module has capabilities to handle bus errors and respond accordingly by raising the `o_illegal` output if an illegal instruction is fetched.
- **Control Flow**: The state of the instruction fetch, whether valid or illegal, is maintained and communicated through the `o_valid` and `o_illegal` signals. This simple control logic is crucial as it ensures that the CPU can react appropriately to successfully fetched instructions or handle exceptions when an illegal instruction is encountered.
- **Simplicity and Future Enhancements**: The current implementation is intentionally simple, with suggestions for future versions to enhance functionality by implementing pipelined fetching or caching, which could significantly improve the performance of the CPU.

In summary, the `prefetch.v` module is a fundamental component of the Zip CPU architecture that handles instruction fetching. Its design emphasizes simplicity while laying the groundwork for more advanced features in subsequent iterations.

### File: dblfetch.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/dblfetch.v
### Overall Purpose of the File
The `dblfetch.v` file implements a dual-fetch instruction mechanism for the Zip CPU, enabling the concurrent fetching of two or more instruction words in a single bus cycle. This is an enhancement over simpler instruction fetching strategies like `prefetch.v`, allowing the CPU to maintain a constant flow of instructions even in scenarios where memory access may be slow. It optimizes the instruction fetching process to minimize idle CPU cycles waiting for instruction data.

### Inter-module Relationships
The `dblfetch` module interacts with several components within the Zip CPU architecture:

- **CPU Modules**: It receives signals from the CPU, particularly handling program counter updates and cache operations (e.g., `i_new_pc`, `i_clear_cache`). It provides fetched instructions (`o_insn`) back to the execution or decode stages of the CPU.

- **Memory Interface**: It interfaces with the memory subsystem through Wishbone signals, allowing it to request instructions over the bus (`o_wb_cyc`, `o_wb_stb`, `o_wb_addr`, and `o_wb_data`). The mix of inputs like `i_wb_stall`, `i_wb_ack`, and `i_wb_e` assists `dblfetch` in managing the memory interaction effectively.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_clk`: Clock signal for synchronization.
  - `i_reset`: Reset signal for initializing the module.
  - `i_new_pc`: Signal indicating a new program counter value.
  - `i_clear_cache`: Trigger to clear any cached instruction data.
  - `i_ready`: Indicates if the CPU is ready to fetch instructions.
  - `i_pc`: The current program counter for instruction fetching.
  - `i_wb_stall`: Signals if the memory is temporarily stalled.
  - `i_wb_ack`: Acknowledgment from memory indicating successful data transfer.
  - `i_wb_e`: Error signal indicating an issue in fetching.

- **Outputs**:
  - `o_valid`: Indicates if the output instruction is valid.
  - `o_illegal`: Signal to indicate that an illegal instruction was fetched.
  - `o_insn`: The fetched instruction word.
  - `o_pc`: The program counter corresponding to the fetched instruction.
  - `o_wb_cyc`: Control signal to initiate bus cycle.
  - `o_wb_stb`: Status signal indicating that a bus transfer is requested.
  - `o_wb_we`: Write-enable signal (output for the Wishbone memory interface).
  - `o_wb_addr`: Address for the memory transaction.
  - `o_wb_data`: Data being written to memory during a fetch operation.

### Behavior of the Module
The `dblfetch` module uses a combination of synchronous logic and state management to coordinate instruction fetching. Here's a breakdown of its key behaviors:

1. **Instruction Fetching Logic**:
   - When `i_new_pc` signals a new program counter, the module will prepare to fetch instructions corresponding to the new `i_pc` value.
   - It will send requests for two instruction words (or more) simultaneously when a bus cycle is active (`o_wb_cyc` and `o_wb_stb` are asserted).

2. **Control Logic**:
   - The module adjusts its state based on inputs such as `i_wb_stall` (indicating a pending state where it should wait) and `i_wb_ack` (indicating that data has been successfully received).
   - The state machine within the module likely governs transitions between states such as IDLE, FETCHING, and VALIDATING fetched data.

3. **Output Handling**:
   - Upon successful fetching of instructions, the module sets `o_valid` high to indicate that the fetched instruction (`o_insn`) is ready to be used by the CPU.
   - If an illegal instruction is fetched, it will assert `o_illegal`.

4. **Cache and Pipeline Integration**:
   - The design anticipates handling cases where the CPU must remain filled with data even during varying memory access times, exemplifying a strategy to keep a pipelined CPU architecture efficiently loaded with instruction data.

Overall, the `dblfetch.v` module plays a crucial role in enhancing the instruction fetch stage of the Zip CPU, increasing instruction throughput and minimizing latency associated with fetching single instructions.

### File: axilfetch.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axilfetch.v
### Purpose of the File
The `axilfetch.v` file implements the instruction fetching logic for the Zip CPU architecture using the AXI-lite protocol. It is designed to retrieve instructions from memory based on the current program counter (PC) and provides control to handle situations such as memory errors or invalid fetch requests. The module incorporates parameters to configure aspects such as address width, data width, instruction width, and whether endianness swapping is needed. 

### Inter-module Relationships
The `axilfetch` module directly interacts with the CPU core by fetching instructions based on a new program counter signal and feeding those instructions into the pipeline for execution. It communicates with the memory subsystem through the AXI-lite interface, which involves sending read requests and receiving instruction data. 

Additionally, the module interfaces with various components in the CPU ecosystem, such as:
- **Control Logic:** It utilizes CPU reset signals and cache clearance signals to synchronize operation.
- **Decode and Execute Stages:** The fetched instructions are forwarded to the instruction decode and execution units for further processing.
- **Cache Management:** Integration with caching mechanisms to facilitate instruction prefetching and validation.

### Key Signals
**Inputs:**
- `S_AXI_ACLK`: AXI input clock signal for synchronizing operations.
- `S_AXI_ARESETN`: Active-low reset signal for the AXI interface.
- `i_cpu_reset`: Resets the CPU state when asserted.
- `i_new_pc`: Indicates a new program counter value to fetch instructions from.
- `i_clear_cache`: Clears any cached instructions.
- `i_ready`: Signals that the fetching module is ready to operate.
- `i_pc`: Current program counter address to fetch the instruction from.

**Outputs:**
- `o_insn`: The instruction retrieved from the AXI bus.
- `o_pc`: Address from which the instruction was fetched, useful for tracking next instruction execution.
- `o_valid`: Indicates whether the fetched instruction is valid.
- `o_illegal`: Signals if there was a bus error during the fetch operation.
  
**AXI-lite Signals:**
- `M_AXI_ARVALID`: Indicates that a read address is valid.
- `M_AXI_ARREADY`: Acknowledges that the read address is ready.
- `M_AXI_ARADDR`: Address from which to read data.
- `M_AXI_RVALID`: Indicates if the read data is valid.
- `M_AXI_RREADY`: Acknowledges that the module is ready to receive data.
- `M_AXI_RDATA`: The instruction data received from memory.

### Behavior of the Module
The `axilfetch` module employs a control logic mechanism to manage instruction fetching. Here are key behaviors within the module:

1. **State Management**: The module operates based on the provided control signals (`i_cpu_reset`, `i_new_pc`, and `i_clear_cache`). These determine when to reset internal states, initiate a new instruction fetch, or clear any stored cache data.

2. **Fetching Process**: When `i_new_pc` is asserted, the module sets up an AXI read request by asserting `M_AXI_ARVALID`. It assigns `M_AXI_ARADDR` based on the incoming `i_pc` (current program counter). It waits for `M_AXI_ARREADY` to confirm the readiness of the AXI interface to process this request.

3. **Response Handling**: After sending the read request, the module monitors `M_AXI_RVALID` to check if valid data has been received. Upon receiving it, the instruction is recorded in `o_insn`, and the address is noted in `o_pc`. It will also assess if the fetched instruction is valid and assert the `o_valid` signal accordingly. An error during fetching (indicated by an invalid `M_AXI_RRESP`) would result in asserting `o_illegal`.

4. **Configurable Behavior**: The module uses parameters to adjust characteristics such as the data width and instruction width, enabling flexibility and adaptability to various CPU designs. This includes functionality for handling byte ordering based on the `SWAP_ENDIANNESS` parameter.

In summary, `axilfetch.v` is a vital module for instruction fetching in the Zip CPU, managing requests over an AXI-lite interface and ensuring the correct operation of the CPU pipeline through careful control of internal states and outputs.

### File: iscachable.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/iscachable.v
### Description of `iscachable.v`

#### Overall Purpose
The `iscachable.v` file implements a combinatorial logic module that determines whether a specific memory address is cacheable. This functionality is vital for both data cache control and maintaining the formal properties of the cache, ensuring that the CPU can efficiently manage memory access patterns. The module operates independent of clock cycles, relying entirely on the input address to generate its output.

#### Inter-module Relationships
The `iscachable` module interacts primarily with the data cache (`dcache`) and potentially other components involved in memory management within the CPU architecture. While it does not have direct connections to other modules, its output is critical for cache coherence and efficiency.

- It typically gets invoked by the data cache logic to evaluate whether the incoming address (from memory operations) can be served from cache memory.
- The decisions made by this module can influence cache miss penalties, cache line allocations, and the overall memory throughput of the CPU.

#### Key Signals
- **Inputs:**
  - `i_addr`: An input wire of width `ADDRESS_WIDTH` (default 32 bits) that represents the address being evaluated for cacheability.

- **Outputs:**
  - `o_cachable`: A one-bit output indicating whether the provided address `i_addr` is cacheable (1) or not (0).

#### Behavior of the Module
The behavior of the `iscachable` module is dictated by a combinational always block that assesses the value of the input address against predefined address ranges and masks:

1. **Initialization**: The output `o_cachable` is initially set to `1'b0`, indicating that the address is assumed to be non-cacheable.

2. **Condition Checks**:
   - The module checks if the incoming address (`i_addr`) matches any of the defined address ranges by ANDing it with the respective masks (SDRAM, FLASH, BKRAM).
   - Each check proceeds as follows:
     - If the address is within the range defined by `SDRAM_ADDR` and `SDRAM_MASK`, `o_cachable` is set to `1'b1`.
     - If the address is within the range defined by `FLASH_ADDR` and `FLASH_MASK`, `o_cachable` is also set to `1'b1`.
     - If it falls within the bounds set by `BKRAM_ADDR` and `BKRAM_MASK`, again, `o_cachable` results in `1'b1`.

This setup allows the module to efficiently ascertain if an address belongs to a specific memory region that can be cached. Since the logic operates purely combinationally, it offers fast responsiveness to address evaluations, which is critical for high-performance CPU operations.

### File: idecode.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/idecode.v
### Overview of `idecode.v`

**Overall Purpose:**
The `idecode.v` file implements the instruction decoding functionality of the Zip CPU architecture. Its main role is to interpret fetched instructions into their corresponding operational logic, which includes determining the type of operations and the operands involved. It is crucial for transforming raw instruction data into control signals that can direct the execution of corresponding tasks within the CPU.

**Inter-Module Relationships:**
The `idecode` module interacts with several other components in the CPU pipeline:
- **Instruction Fetch Module (e.g., `ffetch`):** It receives instructions from the fetch stage after they have been fetched from memory.
- **Execution Stage Modules:** After decoding, it provides essential control signals and decoded instruction information to execution stages (like ALU or memory operations).
- **Prefetching and Stall Logic:** It communicates with control signals related to program counter (PC) decisions and prefetching based on instruction validity and potential stalls due to control dependencies.

**Key Signals (Inputs/Outputs):**

**Inputs:**
- `i_clk`: Clock signal for synchronization.
- `i_reset`: Reset signal to initialize the module.
- `i_ce`: Chip enable signal (possibly for activation during specific operation phases).
- `i_stalled`: Input to indicate if the pipeline is stalled.
- `i_instruction`: The current instruction being decoded (32 bits).
- `i_gie`: Global interrupt enable signal.
- `i_pc`: The program counter value, which indicates the address of the instruction.
- `i_pf_valid`: Indicates if the fetched instruction is valid.
- `i_illegal`: A signal that suggests if the current instruction is potentially illegal.

**Outputs:**
- `o_valid`: Indicates if the decoding process has produced valid data (likely an acknowledgment to the following stages).
- `o_phase`: Indicates the phase of operation during decoding (context unknown without definition).
- `o_illegal`: A flag indicating if an illegal instruction was detected.
- `o_pc`: The program counter to be used for the next fetch or operation; this may be adjusted based on branching.
- `o_dcd{R,A,B}`: Designates decoded register usage.
- `o_pre{A,B}`: Prefetch signals for indirect addressing or operand fetching.
- `o_I`: Represents the instruction being processed post-decode.
- `o_zI`: Zero indicator for the instruction.
- `o_cond`, `o_wF`, `o_op`: Various flags and operation codes determined during the decoding.
- `o_lock`, `o_wR`, `o_r{A,B}`: Control signals for operand source/destination and potential locking mechanisms for memory or registers.
- Flags for early branching, jumps, and pipelining (`o_early_branch`, `o_ljmp`, `o_pipe`).
- Simulation and immediate values for simulation purposes (`o_sim`, `o_sim_immv`).

**Behavior of the Module:**
The `idecode` module operates predominantly on combinatorial logic, deriving output control signals based on the input instruction field. It likely contains:
- **Control Logic**: A combinatorial logic block that extracts parts of the instruction and determines the meaning (decoding).
- **State Management**: While primarily combinational, it may handle certain state transitions through control signals based on the current instruction phase or pipeline status.
- **Output Logic**: Establishes connections and sets up output signals (`o_*`) based on parsed instruction data.

Specific details about how each control signal is influenced would involve further investigation into the implementation but should include registers, ALU operations, branching logic, and response to interrupts that conditionally alter the flow of execution based on the decoded instruction. 

Overall, the functionality encapsulated within `idecode` is integral to the CPU's capability to correctly interpret and execute instructions in real-time, making it a fundamental building block in the Zip CPU architecture.

### File: mpyop.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/mpyop.v
### Purpose of the File

The `mpyop.v` file implements a multiply operation module for the Zip CPU, which is a small, lightweight RISC CPU soft core. Its main purpose is to encapsulate the multiply functionality of the CPU, enabling efficient multiplication of operands while abstracting the complexity of the multiplication algorithm. By separating the multiply operations into their own module, formal verification of the CPU design is made easier, as it focuses on different aspects of the architecture without the added complexity of multiply operations.

### Inter-module Relationships

The `mpyop` module interacts with other parts of the CPU, particularly the control and execution units. It receives input operands from the control logic and forwards the multiply results back to those stages. This interaction includes:

- **Control Logic**: The control unit likely issues commands for multiplication and receives the results back. It would also control whether the multiplication operation is valid or if the module is busy.
- **Execution Unit**: This unit would utilize the outputs from the `mpyop` module to perform register writes, depending on the results produced from the multiplication operations.

### Key Signals (Inputs/Outputs)

#### Inputs:
- `i_clk`: Clock signal used for synchronous operation.
- `i_reset`: Signal to reset the module.
- `i_stb`: Strobe signal indicating when a valid multiplication operation is requested.
- `i_op[1:0]`: 2-bit operation code that specifies the type of multiplication:
  - `2'b00`: 32x32 multiply, returning the low-order 32 bits.
  - `2'b10`: 32x32 unsigned multiply, returning the upper 32 bits.
  - `2'b11`: 32x32 signed multiply, returning the upper 32 bits.
- `i_a[31:0]`, `i_b[31:0]`: Two 32-bit input operands for the multiplication operation.

#### Outputs:
- `o_valid`: This signal becomes high when the multiplication result is valid and ready to be used.
- `o_busy`: Indicates that the module is currently busy performing a multiply operation and cannot accept new requests.
- `o_result[63:0]`: The 64-bit result of the multiplication operation.
- `o_hi`: Signal indicating if the high half of the multiplication result (typically needed for signed and unsigned multiplication results) is valid.

### Behavior of the Module

The behavior of the `mpyop` module includes the following aspects:

- **Multiplication Algorithms**: The module supports multiple multiplication algorithms based on the parameter `OPT_MPY`. This allows flexibility in choosing the optimal multiplication method for performance based on the design requirements. The timing performance varies based on the selected multiply algorithm.
  
- **Control Logic**: The module incorporates control logic that tracks whether the multiplication operation is in progress (`o_busy`) and whether the result is valid (`o_valid`). 

- **Mixed-Mode Operation**: Depending on the value of `i_op`, the module can perform three types of multiplication. This multi-functionality makes the `mpyop` module versatile and capable of serving different multiplication needs based on the context required by the CPU's instructions.

The implementation likely includes a state machine or similar control logic to handle the operation transitions from idle to busy states, as well as managing valid outputs. This ensures that the multiplication process occurs efficiently and that any requests are appropriately handled based on the module’s current state (i.e., whether it is busy or idle).

In summary, the `mpyop` module plays a crucial role in providing multiplication capabilities within the Zip CPU architecture while being configurable to different operational needs and constraints, promoting better design flexibility and support for future enhancement.

### File: pipemem.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/pipemem.v
### Description of the Verilog File `pipemem.v`

#### Overall Purpose of the File
The `pipemem.v` file implements a memory unit designed to support a pipelined Wishbone memory access interface for a CPU. The objective of this design is to allow the CPU to issue one memory access per clock cycle and to read back the results of these accesses at a similar rate, facilitating efficient on-chip memory read/write operations. This pipelined approach enables the CPU to achieve single-cycle access speeds, provided the memory can keep pace with the requests.

#### Inter-module Relationships
In the architecture of the CPU, the `pipemem` module interacts with several other components which include:
- **CPU Core**: It integrates with the execution unit of the CPU, handling memory operations (read/write) initiated by the CPU.
- **Wishbone Interface**: The `pipemem` module acts as a bridge to the Wishbone bus system, enabling global and local memory accesses. It coordinates with other Wishbone-compatible modules, managing signals such as `o_wb_cyc_gbl`, `o_wb_stb`, and `i_wb_data`.
- **Pipeline Stages**: It collaborates with pipeline control signals to manage stall conditions that may arise due to memory operation delays or conflicts.

#### Key Signals (Inputs/Outputs)
1. **Inputs**:
    - `i_clk`: Clock signal for synchronizing the operation of the memory.
    - `i_reset`: Reset signal to initialize the module at startup.
    - `i_pipe_stb`: Indicates that the CPU wants to start a new memory operation.
    - `i_lock`: A control signal that may dictate memory access locking behavior.
    - `i_op`: Operation type (for example, read or write).
    - `i_addr`: Address from which to read/write data.
    - `i_data`: Data to write to memory (if performing a write operation).
    - `i_oreg`: Register number for output data.
    - `i_wb_stall`, `i_wb_ack`, `i_wb_err`: Signals from the Wishbone bus denoting stall, acknowledgment, and error conditions, respectively.
    - `i_wb_data`: Data read from memory on the Wishbone bus.

2. **Outputs**:
    - `o_busy`: Indicates if the memory unit is currently busy with an operation.
    - `o_rdbusy`: Tells if a read operation is being processed.
    - `o_pipe_stalled`: Indicates if the pipeline is stalled waiting for memory operation completion.
    - `o_valid`: Indicates if the output read data is valid.
    - `o_err`: Indicates if there was an error during memory access.
    - `o_wreg`: Output register number for storing results.
    - `o_result`: The value read from or to be written to memory.
    - `o_wb_cyc_gbl`, `o_wb_cyc_lcl`: Wishbone cycles for global and local transactions.
    - `o_wb_stb_gbl`, `o_wb_stb_lcl`, `o_wb_we`: Strobe and write enable signals for Wishbone transactions.
    - `o_wb_addr`: The address for the Wishbone transaction.
    - `o_wb_data`: Data to be written via the Wishbone interface.
    - `o_wb_sel`: Byte select signals for the Wishbone bus.

#### Behavior of the Module
The `pipemem` module employs various control logic to manage its operations:
- It utilizes state machines or similar constructs to track the status of memory operations, responding to inputs and changes in the clock or reset signals.
- The module proceeds with memory operations based on the values received on its input signals, issuing read/write requests to the underlying memory via the Wishbone bus.
- It includes logic to handle situations where a Wishbone operation may stall, ensuring the CPU pipeline can be stalled appropriately (`o_pipe_stalled`).
- It manages simultaneous read or write requests, maintaining output states that reflect the status of these operations, including acknowledgments and errors from the connected Wishbone devices.
- The `o_valid` signal indicates when the data is ready for the CPU to read, adhering to the desired pipelined operation model.

In summary, `pipemem.v` serves as a critical component of the CPU architecture, enabling efficient pipelined access to memory while managing interactions with the CPU's operational state and external memory interfaces.

### File: zipwb.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/zipwb.v
### Overview of the `zipwb.v` File

#### Purpose:
The `zipwb.v` file is the central module of the Zip CPU architecture. Its primary objective is to integrate the core functionalities of the Zip CPU, which is designed to be a lightweight, RISC (Reduced Instruction Set Computing) processor. The module encapsulates the entire CPU pipeline and manages the flow of instructions through its various stages. This architecture supports a limited instruction set (26 types), is fully pipelined, and utilizes a 32-bit wide Wishbone bus for data and address transfers.

#### Inter-module Relationships:
The `zipwb` module interacts with several sub-modules of the Zip CPU, such as:
- **Prefetch Stage**: Responsible for fetching instructions from memory.
- **Instruction Decode Stage**: Handles decoding fetched instructions.
- **Read Operands Stage**: Reads necessary operands for the instruction.
- **Apply Instruction Stage**: Executes the instruction.
- **Write-back Results Stage**: Writes the output back to registers.

Each of these stages is defined in separate modules and communicates with `zipwb` through inputs and outputs that signify the progression of instructions through the pipeline. This pipelined structure allows independent processing of instructions at different stages, enhancing overall throughput.

#### Key Signals:
- **Inputs**:
  - `i_clk`: The clock signal used for synchronizing the operations of the module.
  - `i_reset`: A reset signal that initializes the state of the CPU and clears the pipeline when asserted.
  - Control signals for pipeline management.

- **Outputs**: 
  - The module has outputs representing the status and data of the CPU pipeline stages, but specific signals are not detailed in the provided content.

#### Behavior:
The `zipwb` module operates based on a pipelined structure governed by several control signals:
- **_ce (Clock Enable)**: Indicates whether the instruction from the previous stage (n-1) should be allowed to pass into the current stage (n).
- **_stall**: Signifies that the current stage (n) cannot accept a new instruction due to hazards like dependencies or resource conflicts.
- **_valid**: This indicates whether the current stage holds a valid instruction that can be acted upon.

The behavior and flow of instructions through the stages are tightly controlled by these signals:
- Assignments like `assign (n)_ce = (n-1)_valid && (!(n)_stall)` dictate that a stage can only accept a new instruction if the previous stage has a valid instruction and the current stage is not stalling.
- The state of valid instructions is updated on the clock edge (`posedge i_clk`), ensuring that transitions only occur in sync with the CPU clock.

The module's design effectively allows individual stages to process instructions based on their current status, meaning that a stage can stall when resources are not available or when there's a dependency, all without impacting the flow of other independent instructions through the pipeline. This modular management helps maintain high efficiency even under varying workloads.

### Conclusion
The `zipwb.v` module centralizes the operational logic of the Zip CPU, establishing a core that allows different instruction stages to operate concurrently while managing execution dependencies and maintaining an efficient pipeline structure.

### File: axipipe.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axipipe.v
### Overall Purpose of the File

The `axipipe.v` file implements a memory unit designed for a CPU based on the AXI-lite protocol. This module provides the capability to handle multiple outstanding memory requests simultaneously, which enhances the CPU's performance by allowing it to process incoming operations more efficiently than simpler memory request systems.

### Inter-module Relationships

The `axipipe` module interacts with various other components within the CPU architecture, particularly:
- It serves as an interface between the CPU core and memory, converting CPU-generated requests into AXI-lite protocol requests.
- The module communicates with instruction and data fetch units, processing read/write cycles and ensuring data is delivered correctly to the CPU.
- It is tied to control signals managed by other CPU components, likely to include a pipeline manager, which determines when the module should be active or idle (`o_busy`, `o_pipe_stalled`, `o_rdbusy`).

### Key Signals (Inputs/Outputs)

**Inputs:**
- `S_AXI_ACLK`: The clock signal for the AXI interface.
- `S_AXI_ARESETN`: Active-low reset signal for the AXI interface.
- `i_cpu_reset`: A CPU reset signal.
- `i_stb`: A strobe signal indicating a valid request from the CPU.
- `i_lock`: A signal indicating if the operation is a locked operation.
- `i_op`: A three-bit signal defining the operation type (e.g., read, write).
- `i_addr`: The address for the operation.
- `i_restart_pc`: The program counter restart address, which can be used for instruction fetching after a stall.
- `i_data`: Data input for write operations.
- `i_oreg`: Register output designation for write operations.

**Outputs:**
- `o_busy`: Indicates if the memory operation is currently busy (active).
- `o_pipe_stalled`: Indicates if the pipeline is stalled, preventing further operations.
- `o_rdbusy`: Indicates if the read operation is in progress.
- `o_valid`: Confirms that the output data is valid.
- `o_err`: An error signal confirming if any issues occurred during processing.
- `o_wreg`: Register number designated for writing results back to the CPU.
- `o_result`: The resulting data output from the memory operation.

### Behavior of the Module

The `axipipe` module operates to handle AXI-lite protocol requests issued by the CPU. Here are some key behaviors:

1. **Request Handling:** The module observes the `i_stb` signal to determine if the CPU has initiated a request. Upon receiving a valid request, it processes the operation as designated by `i_op`.

2. **State Management:** Internal state management is implied for operations, where different states can correspond to idle, processing, or error states. The module should transition states based on the request signals and completion of operations.

3. **Error Handling and Reporting:** The `o_err` signal is driven low or high depending on whether an internal error occurs (for instance, an invalid address). This allows the CPU to take corrective action.

4. **Pipeline Control:** The `o_pipe_stalled` and `o_busy` signals help control the pipeline flow in the CPU, indicating when the next instruction can proceed based on whether the current memory operation is still being processed.

5. **Data Transfer:** When an operation completes successfully, it transfers data through the `o_result` and designates a target register using `o_wreg`. The `o_valid` signal ensures that the CPU can safely read the data output.

### Conclusion

In summary, `axipipe.v` serves a critical role in bridging CPU operations with memory using the AXI-lite protocol, allowing for concurrent operation handling. Its interaction with other components and careful management of control signals contributes significantly to the overall functionality and performance of the architecture.

### File: pipefetch.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/pipefetch.v
### File Description: pipefetch.v

#### Overall Purpose:
The `pipefetch.v` file implements an instruction fetch module designed to improve the efficiency of instruction retrieval for a small RISC CPU soft core called Zip CPU. Its primary goal is to enable pipelined Wishbone bus accesses for fetching instructions, thereby reducing the likelihood of CPU stalls. By introducing a caching mechanism, it aims to keep the CPU consistently fed with instructions, preemptively managing delays that occur due to the inherent latency of memory read operations.

#### Inter-module Relationships:
The `pipefetch` module interacts with various other modules in the CPU architecture:

- **Memory Subsystem:** It communicates with the Wishbone interface for accessing memory. Specifically, signals are employed to request instruction reads, handle acknowledgments, and manage errors during memory transactions.
- **Control Logic:** This module is likely connected to other control logic in the CPU that coordinates instruction execution, branching, pipeline control, and potentially exception handling when illegal instructions are detected.
- **Stall Handling:** The `i_stall_n` input indicates whether the CPU pipeline is stalled, thereby affecting how instruction fetching proceeds. This interaction is crucial for maintaining a correct flow of instructions through the pipeline.

#### Key Signals (Inputs/Outputs):
- **Inputs:**
  - `i_clk`: The clock signal, driving synchronous operations.
  - `i_reset`: Resets the module, initializing state and disabling functionality.
  - `i_new_pc`: Signals the arrival of a new program counter value to fetch from.
  - `i_clear_cache`: Indicates requests to clear the instruction cache.
  - `i_stall_n`: Controls whether the instruction fetch operation is active or stalled.
  - `i_pc`: The program counter holding the address of the instruction to be fetched.

- **Outputs:**
  - `o_i`: The fetched instruction output.
  - `o_pc`: The output program counter for the next instruction address.
  - `o_v`: A valid signal indicating whether the fetched instruction is available.
  - `o_wb_cyc`, `o_wb_stb`, `o_wb_we`, `o_wb_addr`, `o_wb_data`: Signals interfacing with the Wishbone bus indicating cycles, transactions and data for instruction retrieval.
  - `o_illegal`: Indicates if an illegal instruction fetch attempt occurred.

#### Behavior of the Module:
The `pipefetch` module implements control logic that manages instruction fetching in a pipelined manner. The following aspects illustrate its behavior:

- **State Management:** It uses states to track instruction fetching progress, handling transitions based on new inputs, cache hits/misses, and stall conditions.
- **Pipelining Logic:** By predicting when instruction accesses to memory will be required, the module can issue fetch requests ahead of time, effectively decoupling instruction retrieval from execution stages.
- **Cache Handling:** The instruction cache is designed to store recently fetched instructions, enabling faster access on subsequent requests. If a cache miss occurs, the module will retrieve the instructions from the main memory.
- **Error Management:** The module incorporates mechanisms to handle illegal instruction fetches, linking behavior that may lead to bus errors, signaled by the `o_illegal` output, which allows for appropriate error handling in the CPU architecture.
  
Overall, the module is designed to enhance performance by balancing execution speed with the latencies of memory access, ensuring that the CPU maintains a continuous flow of instructions.

### File: pfcache.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/pfcache.v
### Description of the `pfcache.v` File

#### Overall Purpose of the File
The `pfcache.v` file implements a cache mechanism for a RISC CPU soft core (Zip CPU). Its primary purpose is to ensure that the CPU can fetch instructions efficiently, minimizing stalls while supplying one instruction per clock cycle. The cache is designed to store frequently accessed instructions, thus reducing memory access times and enhancing overall performance. The logic within the cache can handle requests for instructions and supports a reset feature to clear its contents when necessary.

#### Inter-module Relationships
The `pfcache` module interfaces closely with other components of the CPU architecture. It plays a critical role in the instruction fetch stage by:

- Interacting with the instruction fetch logic, which retrieves the instruction address from program counters and sends cache requests.
- Collaborating with memory modules for caching instructions that are fetched from the main memory when they are not found in the cache.
- Feeding decoded instructions to the execution stage of the CPU pipeline.

The output from this module is essential for maintaining the flow of instruction execution within the CPU pipeline.

#### Key Signals (Inputs/Outputs)
- **Inputs:**
  - Clock signal: Used for synchronizing cache operations.
  - Reset signal: Used to clear the cache contents and return to an initial state.
  - Memory address/Instruction request signals: For determining if the requested instruction is in the cache or needs to be fetched from memory.
  
- **Outputs:**
  - Instruction data: Provides the instruction to the CPU from the cache.
  - Cache hit/miss signals: Indicate whether the requested instruction was found in the cache (hit) or had to be fetched from memory (miss).

#### Behavior of the Module
The `pfcache` module employs control logic designed to optimize instruction retrieval:

1. **Caching Mechanism:**
   - Instruction addresses are divided into three components: Tag bits, cache line number, and cache position within the line.
   - The cache checks if an instruction is present based on the aforementioned components.

2. **Timing Control:**
   - The design considers the clock cycles required for reading data from the cache and verifying tag matches:
     - A step is taken to check if the requested instruction matches the cached value (tag match).
     - A delay is introduced to account for this check, allowing the module to either confirm a cache hit or proceed with fetching from memory if necessary.

3. **State Management:**
   - Control logic may include a state machine to manage cache states such as idle, fetching from memory, resolving hits or misses, and handling resets.

4. **Performance Optimization:**
   - The cache logic uses tagging and direct access principles to minimize the number of clocks required for successful instruction retrieval, enhancing the operational throughput of the CPU.

This modular design contributes to the efficient operation of the Zip CPU by ensuring that instruction fetching is streamlined, minimizing overall latency in instruction execution.

### File: dcache.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/dcache.v
### Description of `dcache.v`

#### Overall Purpose
The `dcache.v` file implements a data cache for the Zip CPU, which is designed to enhance memory access efficiency by maintaining a local cache of data. This cache aims to provide single-cycle read access to data that has been recently accessed and two-cycle access to data currently stored in the cache, thus minimizing the latency introduced by reading from a slower memory system.

#### Inter-Module Relationships
The data cache module interacts with several components of the Zip CPU architecture, specifically:
- **Bus Interface**: The cache handles memory read/write requests and interacts directly with the memory bus. All write accesses are sent out immediately to the bus, regardless of cache status, while cacheable reads can access cached data if available.
- **Memory Management Unit (MMU)**: The cache may work closely with the MMU to handle caching for virtual memory addresses, ensuring proper data retrieval even in the context of TLB (Translation Lookaside Buffer) misses.
- **Pipeline Stages**: The cache is likely to interact with instruction fetches and memory access stages of the CPU's pipeline, ensuring smooth data flow and access efficiency.

#### Key Signals
- **Inputs**:
  - `i_clk`: System clock, which drives the synchronous operations of the cache.
  - `i_reset`: Resets the cache state, ensuring that startup conditions are well-defined.
  - `i_write`/`i_read`: Control signals to determine the type of access being performed (write or read).
  - `i_address`: The memory address for the access request.
  - `i_data`: The data to be written (for write operations).
- **Outputs**:
  - `o_data`: Data output for read operations, providing the retrieved data back to the requesting entity.
  - `o_cache_miss`: A signal indicating whether the requested data was found in the cache or needs to be fetched from the main memory.
  - `o_valid`: A signal indicating the validity of the cached data in the response.

#### Behavior of the Module
The behavior of the `dcache.v` module is characterized by several key functionalities:
1. **Write Access**: All write operations are treated as cache misses, but the cache also updates itself immediately when writing to ensure data coherence. This is critical during bursts of writes.
  
2. **Read Access Types**:
   - **Non-Cacheable Reads**: These requests go to the bus immediately, as they do not use cache memory.
   - **Cache Reads**: 
     - If the requested data is in the cache (`cache hit`), the cache responds within one clock cycle for the data.
     - If the data is not in the cache (`cache miss`), the module will fetch from the main memory, which may take longer (up to two clock cycles).
     
3. **Handling Validity and Errors**: The cache module invalidates cache lines in case of errors detected during reads, offering a mechanism to ensure that incorrect data is not read. This is crucial for maintaining data integrity, especially when working with memory that may be subject to changes from other processes.

4. **Pipelined Operations**: The cache is designed for concurrent reads with background writes to the bus, providing a mechanism to boost throughput during high-memory access scenarios.

The module's design thus ensures efficient use of hardware resources while maintaining high-speed access to recently used data, crucial for performance in CPU operations. Overall, the `dcache.v` file encapsulates critical aspects of data caching and ultimately improves CPU efficiency by reducing access times to frequently used memory locations.

### File: memops.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/memops.v
### Overall Purpose of the File
The `memops.v` file describes a memory operation module for the Zip CPU, which is a RISC softcore designed for lightweight implementations. The module acts as a memory interface, managing read and write operations to memory and ensuring data transfer between the CPU and memory in a specified format. This module also handles synchronization issues, particularly ensuring that memory operations do not overlap incorrectly.

### Inter-Module Relationships
The `memops` module interacts closely with the CPU and the Wishbone bus protocol. It accepts commands and addresses from the CPU and generates control signals that communicate with the Wishbone bus, a common open-source bus specification for connecting components in a system-on-chip (SoC). The module's outputs include control signals used to manage bus traffic and facilitate our data transfer with other memory components.

- **Input Signals from CPU**: The module receives signals such as `i_stb`, `i_lock`, `i_op`, `i_addr`, `i_data`, and `i_oreg`, which inform it about the operations to be performed, including the request to read or write data, the address of the memory operation, and the data to be written.

- **Output Signals to CPU**: Outputs such as `o_busy`, `o_rdbusy`, `o_valid`, `o_err`, `o_wreg`, and `o_result` provide feedback to the CPU about the status of memory operations, indicating whether the operation is in progress, signaling errors, and passing back any read results.

- **Wishbone Communication**: The module produces several control lines for interacting with the Wishbone interface, including `o_wb_cyc_gbl`, `o_wb_cyc_lcl`, `o_wb_stb_gbl`, `o_wb_we`, and `o_wb_addr`, which are critical for coordinating memory access and data transfer on the Wishbone bus.

### Key Signals
- **Inputs**:
  - `i_clk` and `i_reset`: Clock and reset signals for synchronous operation.
  - `i_stb`: Strobe signal indicating that a valid operation is being requested.
  - `i_lock`: Lock signal to prevent other operations while waiting for the current command.
  - `i_op`: Operation type (read/write).
  - `i_addr`: Address for memory read/write operations.
  - `i_data`: Data to be written to memory (for write operations).
  - `i_oreg`: Register index for read/write operations.

- **Outputs**:
  - `o_busy`: Indicates if the memory module is currently busy processing an operation.
  - `o_rdbusy`: Register indicating if a read operation is ongoing.
  - `o_valid`: Signifies that the result is valid and can be used by the CPU.
  - `o_err`: Indicates if an error occurred during the operation.
  - `o_wreg`: Specifies the register to which the result should be written.
  - `o_result`: The data read from memory (in case of read operations).
  - `o_wb_cyc_gbl`, `o_wb_cyc_lcl`: Signals for the Wishbone global and local cycles.
  - `o_wb_stb_gbl`, `o_wb_stb_lcl`: Strobe signals for the Wishbone interface.
  - `o_wb_we`: Write enable for the Wishbone bus.
  - `o_wb_addr`, `o_wb_data`, `o_wb_sel`: Address, data, and select lines for the Wishbone bus transaction.

### Behavior of the Module
The `memops` module operates through a series of states in response to control signals from the CPU and the Wishbone interface. The control logic typically involves:

1. **Reception of Commands**: It waits for a valid command (indicated by `i_stb`) and checks for locks (`i_lock`) to determine if a new operation can start.

2. **Managing Request States**: Depending on the operation type (`i_op`), it will either prepare to read memory or write data. During this time, it sets `o_busy` and `o_wb_stb_gbl` or `o_wb_stb_lcl` to inform the Wishbone bus of ongoing transactions.

3. **Handling Responses**: Once a request is processed, it checks signals like `i_wb_ack` or `i_wb_err` to understand the outcome of the request and updates the output signals accordingly (like setting `o_valid` to signal that results are ready).

4. **Error Handling**: If an error occurs during operation (indicated by `i_wb_err`), the module will set the `o_err` signal to inform the CPU of the failed operation.

5. **Synchronization**: The design is sensitive to race conditions and concurrency, especially noting that issuing a new command before completing the previous one could result in unpredictable behavior.

Overall, `memops.v` is essential for the effective execution

### File: wbpriarbiter.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/wbpriarbiter.v
### Overview of `wbpriarbiter.v`

#### Overall Purpose:
The `wbpriarbiter.v` file implements a priority bus arbiter for the Wishbone bus interface, allowing two separate Wishbone masters to share the same bus while ensuring that one master can access the bus immediately when it is idle. The design aims to streamline the bus request handling without the complexity of combinatorial logic, guaranteeing consistent access times for the higher-priority master.

#### Inter-module Relationships:
This arbiter module interacts directly with two Wishbone master interfaces within a CPU architecture. Each master can make requests for bus access through control signals such as `cyc` (cycle), `stb` (strobe), and `we` (write enable). It manages interactions primarily with the following other components:
- **Wishbone Masters**: These are the initiators of bus transactions that make requests to access shared memory or peripherals.
- **Bus Slave Devices**: The arbiter routes bus control to the appropriate slave device based on which master is granted control of the bus.
  
The arbiter is essential in a pipelined architecture where multiple components might attempt to access shared resources simultaneously, ensuring orderly access and preventing potential conflicts.

#### Key Signals:
- **Inputs**:
  - `i_clk`: The clock signal that synchronizes the operation of the arbiter.
  - `i_a_cyc`, `i_a_stb`, `i_a_we`: Control signals from Master A indicating a bus cycle request.
  - `i_a_adr`: The address being accessed by Master A.
  - `i_a_dat`: The data being sent by Master A for write operations.
  - `i_a_sel`: Byte select signals for Master A.

- **Outputs**:
  - `o_a_stall`: Indicates if Master A is stalled (i.e., unable to continue its operation).
  - `o_a_ack`: Acknowledge signal to Master A once its transaction is complete.
  - `o_a_err`: Error signal for Master A if a transaction fails.

This module can also have similar inputs and outputs for Master B (not completely specified in the provided snippet).

#### Behavior of the Module:
The behavior of the `wbpriarbiter` module is governed by a straightforward arbitration scheme:

1. **Idle State**: By default, the arbiter grants bus access to Master A when no requests are being made (cyc is low).
2. **Bus Requests**: If Master B asserts its request by driving `i_b_cyc` (when it wants access), the arbiter checks the bus status:
   - If the bus is idle, it grants access to Master B.
   - The bus remains granted as long as the `cyc` signal is high from either master.
3. **Bus Granting Logic**: The arbiter uses this gathered information to determine which master gets the bus and issues a corresponding acknowledgment signal while managing stall and error conditions.
4. **Return to Default**: Once a master drops its `cyc` signal, the bus will revert back to Master A, ensuring a fair access strategy.

Additionally, the module accepts an optional parameter `OPT_ZERO_ON_IDLE`, which can be configured to zero the outputs when idle to reduce power consumption or highlight bus status during debugging.

### Conclusion
The `wbpriarbiter.v` is a crucial component in maintaining orderly bus transactions within the CPU architecture by allowing prioritized access to shared resources in a well-defined manner. Its design reduces logic complexity for arbitration while ensuring fair access for multiple masters.

### File: busdelay.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/busdelay.v
### Overview of `busdelay.v`

#### Purpose
The `busdelay.v` file implements a bus delay mechanism for the Wishbone bus in the Zip CPU architecture. Its primary function is to introduce a clock cycle delay for bus accesses, which helps alleviate timing issues observed when the original design did not meet the required timing constraints for specific hardware implementations. This delay ensures that, whenever the bus will stall, it is communicated to the master on the first clock, thereby aiding in the overall integrity of data transactions in the system.

#### Inter-module Relationships
The `busdelay` module interacts with other modules within the CPU architecture, particularly those involved with bus access and transaction handling. This may include:

- **Wishbone master modules**: These components send requests to the bus for data reading/writing. The `busdelay` module ensures that these requests are appropriately delayed, thus giving the masters a chance to react to stall conditions or other timing-related events.
- **Bus arbiter modules**: These may utilize the signaling from the `busdelay` module to better manage request priorities and bus access rights.
- **Memory or peripheral interface modules**: By regulating the timing and order of access requests, the `busdelay` facilitates smoother communication between the CPU and external resources.

#### Key Signals
Inputs:
- `input wi`: Represents write enable signals or instructions for the bus operations.
- Other inputs would typically be the control signals, such as `clk`, `rst` (reset), and any other signals related to stall conditions that specify whether the delay should be activated.

Outputs:
- Several outputs represent the delayed signals for bus commands and stall conditions, ensuring they are sent with the desired timing established by the parameters of the `busdelay`.

#### Behavior of the Module
The module's behavior is primarily driven by its parameters, including `DELAY_STALL` and options for low power. The key features include:

1. **Pipelined Access**: The `busdelay` module allows for a pipelined architecture where operations can occur concurrently across different clock cycles. Importantly, it maintains a single access per clock cycle even when the bus is pipelined.

2. **Timing Control**: It introduces control logic that determines when signals are passed through or delayed based on the state of the bus. This includes handling the stall condition intelligently to ensure that the master knows how to proceed with bus accesses.

3. **Conditional Logic**: The parameter `DELAY_STALL` allows configurability. When set to non-zero, it will utilize the logic that delays stall indications, ensuring that necessary timing constraints are respected. Conversely, when not needed, this feature can be disabled to optimize performance.

4. **No State Machine**: The implementation does not inherently use a state machine; rather, it relies on combinatory logic based on control signals and clock edges.

5. **Resource Management**: It also provides an option (`OPT_LOWPOWER`) that, when activated, can implement strategies to minimize resource usage.

In summary, the `busdelay` module plays a crucial role in managing the timing of bus accesses, ensuring reliable operation of the Zip CPU under varying operational constraints, particularly in situations where timing violations may occur. It highlights the balance between flexibility in design and the demands of ensuring robust hardware performance.

### File: fwb_master.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/fwb_master.v
### Description of the Verilog File: fwb_master.v

#### Overall Purpose
The `fwb_master.v` file implements a model for a Wishbone master in the Zip CPU architecture, focusing on formal verification rather than functional logic. Its primary purpose is to define rules and assertions on how the master component interacts with external Wishbone slaves to ensure correct transaction handling and response processing. This module aids in validating the master’s behavior through formal methods, such as using the SymbiYosys tool.

#### Inter-module Relationships
The `fwb_master` module interacts primarily with Wishbone slave modules within the Zip CPU architecture. It is designed to work in tandem with its counterpart, `formal_slave.v`, which defines expectations and asserts properties of the slave's outputs based on the master's inputs. This setup allows for a comprehensive verification of the bus protocol by establishing a clear contract between the master and any slaves it communicates with.

In essence:
- **fwb_master** outputs signals that initiate and control transactions.
- It relies on its corresponding slaves to respond appropriately, which is verified through assertions defined in `formal_slave.v`.

#### Key Signals
- **Inputs:**
  - `i_wb_stall`: Indicates if the master must wait before proceeding.
  - `i_wb_ack`: Acknowledgment signal from the slave indicating it has processed the request.
  - `i_wb_data`: Data returned from the slave during read transactions.
  - `i_wb_err`: Error signal from the slave indicating a transaction failure.

- **Outputs:**
  - `o_wb_cyc`: Cycle signal indicating an active transaction.
  - `o_wb_stb`: Strobe signal to indicate that the current transaction is valid.
  - `o_wb_we`: Write enable signal indicating whether the operation is a read or write.
  - `o_wb_addr`: Address of the transaction.
  - `o_wb_data`: Data to be sent in write transactions.
  - `o_wb_sel`: Select signal for byte addressing in read/write operations.

#### Behavior of the Module
The `fwb_master` module does not contain traditional functional logic but rather focuses on ensuring the correct behavior of a Wishbone master. The following points summarize its behavioral aspects:

- **Formal Verification Focus**: It does not execute transactions but checks whether the outputs (`o_wb_*` signals) adhere to the expected protocol during formal verification sessions.
  
- **Assertions and Assumptions**: The module includes assertions that verify outputs based on the inputs. The assertions are designed to ensure compliance with the Wishbone specification, verifying that the master properly handles the requests it generates, the states it enters, and the responses it expects.

- **State Management**: While the file does not explicitly define a state machine or control logic, the structure is implicitly defined through assertions that will validate the expected states of the master during a transaction cycle.

Overall, the `fwb_master.v` file serves as a specialized component for ensuring that the Wishbone master behaves correctly within the context of the Zip CPU and is a critical piece in the verification workflow of the entire CPU architecture.

### File: fwb_slave.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/fwb_slave.v
### Overall Purpose of the File
The `fwb_slave.v` file implements the behavior of a Wishbone slave in a CPU architecture. Its primary purpose is to encapsulate the formal verification of interactions between the CPU and other components through the Wishbone bus protocol. This module acts as a testbench for verifying that the slave correctly processes requests from a Wishbone master, responding with the appropriate outputs based on its incoming input conditions. Importantly, this module contains no functional logic—its focus is strictly on formal verification through assertions and assumptions regarding the interface signals.

### Inter-module Relationships
The `fwb_slave` module interacts with a Wishbone master, which generates requests and receives responses via the Wishbone bus. It is formally verified against a corresponding `formal_master.v`, which adheres to the same protocol but operates under the assumption of generating valid inputs for the slave. As a result, `fwb_slave` serves as an interface for ensuring that the slave responds according to the established rules of the Wishbone protocol, providing feedback on acknowledgment, error signaling, and data transfer when applicable.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_wb_cyc`: Indicates that the current transaction is valid and that the slave should respond accordingly.
  - `i_wb_stb`: Signals that a Wishbone request has been made and the slave should prepare to respond.
  - `i_wb_we`: Indicates the type of operation: a write (if high) or read (if low).
  - `i_wb_addr`: The address for the desired transaction, where either read or write actions are to take place.
  - `i_wb_data`: The data to be written to the address when `i_wb_we` is high.
  - `i_wb_sel`: Select lines to specify which part of the data bus is relevant for the current transaction.

- **Outputs**:
  - `o_wb_stall`: Used to indicate the slave is not ready to process the request, potentially causing the master to wait.
  - `o_wb_ack`: Acknowledgment signal indicating that the slave has received and registered the incoming request.
  - `o_wb_data`: Data to be returned to the master during a read operation.
  - `o_wb_err`: Error signal that indicates if there was an issue with processing the request.

### Behavior of the Module
The `fwb_slave` module is primarily constructed for formal verification rather than functional operation. Its purpose is to ensure that the slave adheres to the expected interaction rules defined by the Wishbone protocol. 

- **Control Logic**: While the file contains no actual control logic or state machines, the behavior is defined through `SLAVE_ASSUME` and `SLAVE_ASSERT` macros that specify what inputs can be expected and what outputs should be generated in response. 

- **Verification-Driven Design**: Input signals are assumed to follow certain rules, while outputs must conform to specified assertions. This allows the formal verification tools to check for correctness in how the slave handles standard scenarios defined in the Wishbone protocol.

Overall, `fwb_slave.v` is a vital component in the formal testbench context, ensuring that the Wishbone slave behaves correctly when interacted with by a master device during hardware verification processes.

### File: skidbuffer.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/skidbuffer.v
### Description of skidbuffer.v

#### Overall Purpose of the File
The `skidbuffer.v` file implements a basic SKID buffer used in high-throughput AXI (Advanced eXtensible Interface) communication within the Zip CPU architecture. The primary role of this module is to handle situations where data stalls may occur in the bus interface. It ensures that any incoming data during a stall condition is buffered, allowing the system to operate seamlessly without loss of information or control signals. By registering the outputs, the skid buffer accommodates the AXI specification's requirements that all outputs must be registered.

#### Inter-module Relationships
The `skidbuffer` module interacts with other components of the CPU architecture primarily through its bus interface. It connects to peripherals or other bus controllers on its inputs and provides outputs to the next stage in the communication process. The skid buffer thus serves as an intermediary, ensuring data integrity during periods of communication stalls. Its functionality directly impacts the performance and reliability of the AXI data transfers, making it crucial in managing data flow to and from various modules which may include memory controllers or other subsystems that utilize the AXI protocol.

#### Key Signals (Inputs/Outputs)
- **Inputs:**
  - `i_valid`: Indicates if valid data is present on the input bus. 
  - `i_data`: The actual data being transmitted.
  - `i_ready`: A signal indicating whether the receiving end is ready to accept data.

- **Outputs:**
  - `o_data`: The buffered data output either in the case of a delay or if the bus is ready.
  - `o_valid`: Indicates if there is valid data present on the output, derived from the internal storage conditions.
  - `o_ready`: A registered signal that indicates to upstream modules whether the skid buffer is ready to accept valid data.

#### Behavior of the Module
The skid buffer's operational behavior is dictated by the presence of stall conditions and the valid data stream. The control logic within the module ensures the following:

1. **Buffering Logic:** When the `i_ready` input indicates a stall (i.e., `i_ready` is low), the incoming data (`i_data`) is stored in a register (typically referred to as `r_data`), and the valid flag (`r_valid`) is set to indicate that valid data is now buffered. 

2. **Data Propagation:** When `i_ready` is high, the buffered data is made available on the output (`o_data`), and the output valid flag (`o_valid`) reflects the current state.

3. **Control Conditions:** Depending on the module configuration (via parameters), the skid buffer can either directly pass through data without holding it (`OPT_PASSTHROUGH`) or maintain output registers for synchronization (`OPT_OUTREG`).

4. **Power Management (Optional):** If the parameter `OPT_LOWPOWER` is set, the outputs will be driven to zero whenever the respective valid signal is low, reducing unnecessary toggling of the signals and thus minimizing power usage, particularly advantageous for large fanout conditions.

5. **State Management:** The behavior of the control signals ensures seamless back-and-forth communication with appropriate readiness signals, allowing upstream modules to function without knowledge of the internal buffering state.

In summary, the skid buffer is a critical module that enhances AXI bus communication by ensuring that stalls do not disrupt data flow, enabling higher throughput and efficiency within the CPU design.

### File: fwb_counter.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/fwb_counter.v
### Purpose of the File

The `fwb_counter.v` file implements a counter module for managing access to the Wishbone bus within the Zip CPU architecture. It handles the counting of outstanding requests and acknowledgments, making it essential for controlling bus transactions effectively. It allows the CPU to make decisions regarding bus cycles, stall conditions, and request acknowledgments.

### Inter-module Relationships

The `fwb_counter` module interacts with various components of the Wishbone bus system in the Zip CPU architecture. Specifically, it is designed to communicate with:

- **Wishbone Master Modules**: These modules initiate read and write operations through the Wishbone bus. The `fwb_counter` tracks active requests and manages the arbitration for the bus during these operations.
- **Wishbone Slave Modules**: These modules respond to requests made by the master. The `fwb_counter` keeps track of the number of acknowledgments (acks) received to ensure reliable communication.
- **Other Components in the CPU**: It may also interface with higher-level components that need information about the bus' status or the number of current outstanding requests.

### Key Signals (Inputs/Outputs)

1. **Inputs**:
   - `i_clk` - Clock signal for synchronous operation.
   - `i_reset` - Reset signal to initialize the module.
   - `i_wb_cyc` - Wishbone cycle signal indicating an active transaction.
   - `i_wb_stb` - Strobe signal indicating a valid operation.
   - `i_wb_we` - Write enable signal indicating a write operation.
   - `i_wb_addr` - Address for the current Wishbone operation.
   - `i_wb_data` - Data being written during a write operation.
   - `i_wb_sel` - Select signal for byte enabling during writes.
   - `i_wb_ack` - Acknowledgment signal from the Wishbone slave.
   - `i_wb_stall` - Stall signal indicating that the slave cannot accept a request.
   - `i_wb_idata` - Data read from the Wishbone slave.
   - `i_wb_err` - Error signal indicating a transaction failure.

2. **Outputs**:
   - `f_nreqs` - Output indicating the number of requests currently active.
   - `f_nacks` - Output indicating the number of acknowledgments received.
   - `f_outstanding` - Output indicating the number of outstanding requests to the bus.

### Behavior of the Module

The `fwb_counter` module contains logic for managing bus requests using a state machine or combinatorial logic to count outstanding requests. Here’s an overview of its behavior:

- **Request Counting**: It counts new requests initiated by the master using the `i_wb_cyc` and `i_wb_stb` signals. When a new request is detected, the counter for active requests is incremented.
  
- **Acknowledgment Handling**: Upon receiving an acknowledgment (`i_wb_ack`) from the slave, the module decrements the count of outstanding requests. This ensures that the master accurately tracks how many requests are still pending.

- **Control Logic**: The module can implement conditions to manage stall situations based on the `i_wb_stall` signal. If the bus is stalled, it adjusts the counters accordingly to prevent over-counting requests.

- **Parameterization**: The design uses parameters to customize behavior, such as maximum outstanding requests and conditions for allowing specific types of transactions (like read-modify-write). The use of localparams allows flexible configuration for different application scenarios.
  
- **State Management**: If required by the design, additional control logic can be implemented explicitly (not shown in the excerpt) to manage different states based on bus activity, optimizing performance based on the defined parameters.

In summary, the `fwb_counter` module is a crucial component that enhances the bus interfacing capabilities of the Zip CPU, ensuring robust management of bus transactions and interactions with Wishbone protocol-compliant slaves.

### File: sfifo.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/sfifo.v
### File Description: `sfifo.v`

#### Overall Purpose:
The `sfifo.v` file implements a synchronous data FIFO (First-In-First-Out) buffer for the Zip CPU architecture. This FIFO allows for the temporary storage of data with a specified byte width (`BW`) and length (`LGFLEN`), thereby enabling efficient data flow between different components of the CPU without requiring them to operate at the same clock speed.

#### Inter-module Relationships:
- **Component Interaction**: The FIFO module serves as a buffering mechanism for data, interacting primarily with the execution stages of the CPU. It can be used in data paths that require temporary storage or queuing of data, helping ensure that the data is available when needed without being lost or overwritten.
- **Potential Modules**: This FIFO could interface with modules for data manipulation, execution units, or memory controllers, providing a transient storage point where data can be safely written to or read from while maintaining orderly processing through the CPU pipeline.

#### Key Signals (Inputs/Outputs):
- **Inputs**:
  - `i_clk`: The main clock signal, which synchronizes the operations of the FIFO.
  - `i_reset`: A reset signal that initializes or clears the FIFO state.
  - `i_wr`: A write enable signal that, when high, allows data to be written to the FIFO.
  - `i_data`: The data input line where data is provided to be stored in the FIFO.
  - `i_rd`: A read enable signal that, when high, allows data to be read from the FIFO.

- **Outputs**:
  - `o_full`: Indicates if the FIFO is full. It prevents writing when high unless the `OPT_WRITE_ON_FULL` option is enabled.
  - `o_fill`: A register that shows the current number of data items in the FIFO (0 to `2^LGFLEN`).
  - `o_data`: The output data line that provides the data read from the FIFO.
  - `o_empty`: Indicates if the FIFO is empty, preventing reads when high.

#### Behavior of the Module:
- **FIFO Control**: The FIFO operates on clock edges, responding to the `i_clk` signal. Upon a reset (`i_reset`), both the fill count (`o_fill`) and write address (`wr_addr`) are set to zero.
  
- **Writing Data**:
  - On each clock cycle, if `i_wr` is high and the FIFO is not full (`o_full` is low), the provided data on `i_data` will be written to the memory array (`mem`) at the address specified by `wr_addr`.
  - The fill count (`o_fill`) will increase, and the write address (`wr_addr`) is incremented.

- **Reading Data**:
  - When `i_rd` is high and the FIFO is not empty (`o_empty` is low), data is read from the memory array into `o_data` and the fill count will decrease.
  
- **Full and Empty Conditions**:
  - The module maintains internal registers (`r_full`, `r_empty`) to keep track of whether the FIFO is full or empty based on the current fill level (`o_fill`).
  - The overflow and underflow conditions are controlled by parameters, allowing configurability, such as `OPT_WRITE_ON_FULL` and `OPT_READ_ON_EMPTY`.
  
This design provides robust FIFO behavior while being configurable for different operational modes, addressing the needs of the CPU's pipelined architecture for managing data flow efficiently. It supports both synchronous write/read operations and includes options to modify behavior under specific conditions, making it versatile for various usage scenarios within the Zip CPU framework.

### File: wbarbiter.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/wbarbiter.v
### Overview of `wbarbiter.v`

#### Overall Purpose
The `wbarbiter.v` file implements a priority bus arbiter for the Zip CPU architecture. This arbiter allows two separate Wishbone masters to access a shared bus, managing access based on request priority and potentially alternating access to ensure fair utilization of the bus. The design is optimized to reduce combinatorial complexity while ensuring that bus access delays are minimized.

#### Inter-module Relationships
The `wbarbiter` module interfaces directly with the Wishbone bus protocol, specifically designed for connections between multiple bus masters (referred to as Master A and Master B in the descriptions). It serves as an intermediary that manages which master can control the bus at any given time, particularly in cases where both masters assert their control signals concurrently.

The arbiter likely interacts with:
- **Bus Masters**: The external components or modules that issue read/write requests to the bus.
- **Memory/Peripheral Interfaces**: Other modules in the CPU that provide data storage or processing capabilities, requiring bus access for operations.
- **Control Logic**: It may link to control units responsible for higher-level decision-making in the CPU regarding memory access sequences.

#### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_clk`: Clock signal for synchronizing operations.
  - `i_reset`: Reset signal for initializing the arbiter to a known state.
  - `i_a_cyc`: Indicates that Master A is attempting to access the bus.
  - `i_a_stb`: Strobe signal from Master A, signaling a valid request.
  - `i_a_w`: Write control from Master A, indicating the type of operation (read or write).

- **Outputs**:
  - The arbiter outputs signals that would determine which master is granted access to the bus (e.g., `o_cyc` to signify a valid bus cycle, potentially others for data transfer).

#### Behavior of the Module
The `wbarbiter` functions with a series of control logic steps to manage bus access:

1. **Bus Access**: The arbiter allows bus access when either Master A or Master B asserts the `o_cyc` line. If both masters assert their requests simultaneously, priority handling comes into play:
   - By default, Master A is given priority if both assert at the same time.
   - An option (`ALTERNATING`) allows the arbiter to alternate bus access between the two masters to ensure fairness.

2. **Persistent Ownership**: Once a bus cycle has started (i.e., a master asserts the `o_cyc`), that master continues to own the bus until it deasserts `o_cyc`. This ensures that a single master can complete its transaction without being interrupted.

3. **Guaranteed Deassertion**: The arbiter guarantees that `o_cyc` will be deasserted (set low) for one clock cycle at the end of a bus cycle, allowing for a clean transition of bus ownership.

4. **Next Cycle Arbitration**: On the subsequent clock cycle, the arbitration process begins again. If one master asserts its request, it will be granted access regardless of how long the other might have been waiting, unless the alternating procedure is in use.

5. **Control Logic**: The control logic is predominantly combinatorial, managing state transitions based on the requests from the masters while keeping the timing constraints and ensuring that bus access is handled as efficiently as possible.

In summary, `wbarbiter.v` is a crucial component in the bus interface of the Zip CPU architecture, ensuring that multiple masters can share a single bus resource efficiently and fairly. The implementation guarantees predictable behavior aligned with the design goals of reducing complexity and improving access times.

### File: wbdblpriarb.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/wbdblpriarb.v
### Overview of wbdblpriarb.v

**Overall Purpose:**
The `wbdblpriarb.v` file implements a dual priority arbiter for two separate Wishbone buses within the Zip CPU architecture. The intent is to streamline the arbitration process between two buses by allowing the Zip CPU to resolve address space efficiently one clock cycle earlier than traditional implementations. This modification is crucial for optimizing timing and reducing the number of sequential comparisons needed by peripherals, allowing for improved adherence to timing specifications.

### Inter-module Relationships:
The `wbdblpriarb` module interacts with both the local and external Wishbone buses. By implementing two sets of control signals (CYC_A, STB_A for one bus, and CYC_B, STB_B for the other), the arbiter allows the associated device (in this case, the Zip CPU) to determine whether an access is directed to the local ZipSystem bus or an external Wishbone bus in parallel. This setup simplifies the logic required for determining bus access and minimizes the number of timing-critical operations.

The arbiter communicates with other modules in the architecture, such as devices connected to the Wishbone interface (peripherals), which respond based on the CYC and STB signals provided by the arbiter.

### Key Signals (Inputs/Outputs):
**Inputs:**
- `CYC_A`: Indicates bus cycle for the first Wishbone bus (used by master A).
- `STB_A`: Indicates valid data transfer on the first Wishbone bus.
- `CYC_B`: Indicates bus cycle for the second Wishbone bus (used by master B).
- `STB_B`: Indicates valid data transfer on the second Wishbone bus.
- Additional control signals that manage bus arbitration.

**Outputs:**
- `CYC`: Outputs active bus cycle signal for the arbiter's selected bus.
- `STB`: Outputs active valid signal for the selected bus.
- Other Wishbone signals that are shared between both buses to maintain their operational integrity.
- Optional error signals as implemented to provide feedback on bus access outcomes.

### Behavior of the Module:
The `wbdblpriarb` arbiter operates with a priority arbitration mechanism that functions as follows:

1. **Cycle Determination**: Upon receiving CYC and STB signals from the two different masters (A and B), it assesses which master needs to access the bus.
  
2. **Control Logic**: The arbiter checks the states of CYC_A and CYC_B. Only one of these can be high at any given moment to ensure exclusive access to the underlying bus. If both are asserted, priority logic is applied to choose one.

3. **Clock Cycle Synchronization**: Importantly, the arbiter allows the CPU to resolve the bus access one clock cycle earlier than would typically be possible. This helps sustain timing margins by ensuring that the bus state is known before critical operations occur in downstream logic.
  
4. **Bus Signals Maintenance**: The arbiter manages the outputs such that only the CYC and STB of the winning bus (based on the arbitration logic) are presented to the downstream devices, ensuring that they interact with the correct bus.

5. **Error Handling**: Recently, support has been added to manage Wishbone error signals, providing feedback to the system about potential problems during bus transactions.

### Conclusion:
In summary, the `wbdblpriarb.v` file is a vital component of the Zip CPU's Wishbone interface, ensuring efficient access to system resources while adhering to timing constraints. Its design is integral for optimizing the performance of the Zip CPU architecture by allowing the arbiter to determine bus access earlier and reducing complexity in peripheral device selection logic. This functionality aids in maintaining system stability and enhancing throughput across the CPU's buses.

### File: wbdmac.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/wbdmac.v
Here's a detailed description of the `wbdmac.v` Verilog file according to the given requirements:

### Purpose
The `wbdmac.v` file implements a Wishbone Direct Memory Access (DMA) controller for the Zip CPU architecture. Its primary function is to facilitate the transfer of data between different addresses in the Wishbone address space without requiring CPU intervention. It allows for the movement of up to 4KB (or 1k Words) of data, efficiently managing memory operations during DMA transfers.

### Inter-module Relationships
The `wbdmac` DMA controller interacts with the Wishbone protocol, which is used for communication with various peripherals and memory blocks in the CPU architecture. Key interactions include:
1. **Wishbone Master Interface**: The DMA controller acts as a master in the Wishbone system, issuing reads and writes to transfer data to and from specified addresses.
2. **Peripheral Modules**: The DMA controller may interface with any memory or peripheral module that is connected to the Wishbone bus, allowing data to be transferred to these modules based on the configuration set within the DMA.

### Key Signals
- **Inputs**:
  - **Wishbone Control Signals**: Standard Wishbone signals such as `wb_clk`, `wb_rst`, `wb_cyc`, `wb_stb`, `wb_we`, `wb_addr`, and `wb_data` are utilized for controlling the DMA operations.
  
- **Outputs**:
  - **Status and Control Outputs**: Outputs reflecting the status of the DMA operation are provided, including signals that can indicate whether the DMA is busy or idle.
  - **Wishbone Data Outputs**: This includes data being transferred to the destination address.
  
- **Registers**:
  - **Control/Status Register (CSR)**: The module has internal registers that track the state of the DMA operation, the length of the transfer, source address, destination address, and other control bits that determine the behavior of the DMA.

### Behavior
The operational behavior of the `wbdmac` DMA controller can be summarized as follows:

1. **Initialization and Configuration**: Before a DMA transfer begins, the module requires the configuration of several control registers (length, source address, destination address) which can be set through Wishbone writes.

2. **Transfer Operation**: The DMA controller performs the data transfer based on the values configured in the registers:
   - It reads data from the source address.
   - Depending on the control signals, either increments the address for subsequent reads/writes or keeps the address fixed.
   - Data is written to the specified destination address.

3. **Idle and Busy States**: The controller maintains an idle state when not in operation. Upon receiving configuration and start commands, it transitions to a busy state until the transfer is complete. During operation, it updates the status register to indicate progress and completion of data transfers.

4. **Error Handling**: The module can also handle errors during transfers (e.g., bus errors) and reflects this in its status outputs.

5. **Control Logic**: The logic for control signals ensures that:
   - Writes to configuration registers occur only when the controller is in an idle state.
   - Transactions can be gracefully halted or aborted using specific control values written to the control/status register.

In summary, the `wbdmac.v` file provides a sophisticated DMA controller for efficient data transfer in a CPU architecture that employs the Wishbone interface, enabling seamless memory operations without excessive CPU load.

### File: ziptimer.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/ziptimer.v
### Purpose of the File
The `ziptimer.v` file provides a lightweight implementation of a timer for the Zip CPU architecture. This timer can be used for various timing tasks, including generating interrupts at specified intervals and monitoring the system for watchdog purposes. The timer is designed to facilitate simple configuration through its control registers.

### Inter-Module Relationships
The `ziptimer.v` module interacts with other components in the CPU architecture, primarily serving as an interrupt source for the CPU. It connects to the interrupt controller of the CPU, which can mask or handle the interrupts generated when the timer reaches zero. The timer can be integrated into the CPU's control flow such that it triggers resets or interrupt signals based on elapsed time. This integration provides essential functionalities for task scheduling and system reliability.

### Key Signals
- **Inputs:**
  - Control signals for configuring timer behavior, such as:
    - **Start_n/Stop:** This is effectively simplified as any write that isn’t zero starts the timer while writing zero stops it and clears the timer.
    - **AutoReload:** This signal determines if the timer reloads its value on reset automatically.
  
- **Outputs:**
  - **Interrupt signal (if applicable):** The timer can generate an interrupt when it counts down to zero. This is crucial for the CPU to respond to timing events.

### Behavior of the Module
The `ziptimer.v` module has two operational modes, determined by the configuration of its registers:
1. **Single Combined Register:** 
   - A single register is used for both control and value. When the timer value is "set," the reload value is established, and writing to this register automatically initiates the countdown.
   - Reading this register returns the current timer value.

2. **Separate Control and Value Registers:**
   - This configuration uses one register for the current timer value and another for the control logic. In this setup, the control register can keep track of the reload value.
   - When the timer interface is set to zero on the clock, an interrupt is triggered without setting it actively. This allows the timer to halt without generating an interrupt when set to zero directly.

**Control Logic:**
- The control bits are primarily simplified:
  - The start control is represented by any non-zero write, allowing for a more straightforward initiation of the timer.
  - The auto-reload feature reinitializes the timer automatically upon reset if enabled.
  - The timer only supports countdown functionality, with no capability for counting up.

**Watchdog Functionality:**
- The timer's behavior can be configured to serve as a watchdog. If the timer expires (counts down to zero), it can trigger a CPU reset by connecting its interrupt line to the CPU reset line, ensuring system stability.

Overall, the module implements straightforward timer functionality through registers while interacting efficiently with the CPU to enable basic timing and interrupt capabilities.

### File: zipjiffies.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/zipjiffies.v
### Purpose of the File
The `zipjiffies.v` file implements a peripheral for the Zip CPU, which is designed to handle timing operations analogous to the 'jiffies' concept in Linux. It allows the CPU to manage sleep timers for processes, enabling them to pause until a specified number of jiffies have elapsed. This functionality is crucial for multitasking and time-based scheduling in an operating system environment.

### Inter-Module Relationships
The `zipjiffies` module interacts with several components within the CPU architecture:
- **CPU Core**: It interfaces directly with the CPU to read and write jiffies. The CPU can issue read operations to obtain the current value of jiffies and write operations to set a new interrupt time.
- **Interrupt Controller**: When the jiffies timer expires and generates an interrupt, it signals the interrupt controller, potentially leading to a context switch or interrupt handling in the CPU.
- **Sleep Management**: The CPU can manage a list of sleep requests using the jiffies timer, coordinating with other peripherals or modules that handle process states.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - **Clock and Reset Signals**: Standard inputs for module functionality, typically `i_clk` and `i_reset`, to control timing and initialization.
  - **CPU Read/Write Control Signals**: These signals enable the CPU to read from or write to the jiffies register.
  
- **Outputs**:
  - **Jiffies Register Value**: When the CPU reads from the module, it receives the current value of the jiffies counter.
  - **Interrupt Signal**: An output signal that indicates when the timer has reached a specified jiffy count, causing an interrupt to be raised. 

### Behavior of the Module
- **Counter Management**: The module maintains a counter that keeps track of the current jiffies value. 
- **Write Operations**: When the CPU writes a value to the jiffies peripheral, the module calculates whether this value is closer to the current counter than any previously registered interrupt time. If so, it updates the interrupt time accordingly.
- **Ignoring Out-of-Range Writes**: Writes within a (N-1) bit space are considered, but any writes that occur within the last `2^(N-1)` ticks are ignored to prevent invalid timer settings.
- **Interrupt Generation**: The module generates an interrupt when the jiffies counter equals a specified value. Once the interrupt occurs, it needs a reset from the CPU to register a new timing value.
- **State Machine/Control Logic**: Potentially, the module may have simple state machine logic to handle various states of the jiffies counter, write operations, and interrupt signaling.

In summary, the `zipjiffies.v` module is a critical component of the Zip CPU, providing time-scheduling capabilities that allow processes to manage sleep and wake-up events efficiently. It maintains synchronization with the CPU and ensures timely delivery of interrupts based on the specified timing conditions. The design provides a straightforward interface while handling essential low-level timing complexities.

### File: zipmmu.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/zipmmu.v
### Overall Purpose of the File
The `zipmmu.v` file implements a Wishbone Memory Management Unit (MMU) for the Zip CPU architecture. This MMU acts as a "bump-in-the-line" that modifies memory access between the CPU and a separate Wishbone bus. It allows the CPU to configure the MMU by using a designated section of the memory space when in supervisor mode, ensuring that the management unit can be included or excluded based on the specific needs of the system designer.

### Inter-module Relationships
The MMU interacts with:
- **CPU**: The MMU receives configuration commands and memory access requests from the CPU when the CPU is in supervisor mode. Its operation is contingent on CPU state (e.g., supervisor or user mode).
- **Wishbone Bus**: It connects to two Wishbone buses—one for configuration and the other for memory access. Both buses cannot be accessed simultaneously, which necessitates careful control of bus activity.
- **Peripheral Memory**: The MMU is designed to integrate with the peripheral memory space to configure and manage virtual-to-physical address translation effectively.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - Control signals from the CPU indicating the operational context, such as supervisor mode.
  - Address and data lines from the Wishbone bus for configuration and memory access.
  
- **Outputs**:
  - Modified addresses and data back to the peripheral devices through the second Wishbone bus.
  - Status signals that indicate the operational state of the MMU (e.g., whether translation is active).

### Behavior of the Module
The MMU operates under various control mechanisms:
- **Context Switching**: When context = 0, the MMU acts as a simple pass-through, equating virtual pages to physical pages. If context != 0, the MMU engages in translation, matching virtual addresses against context and performing memory access accordingly.
  
- **Control Logic**: The MMU includes control logic to manage its operation based on the CPU state (supervisor mode versus user mode). It handles address decoding, translation lookaside buffer (TLB) management, and page table access, ensuring efficient memory accesses with minimal latency.

- **Performance Goals**: The design emphasizes performance, aiming for a single clock cycle delay on accesses through the MMU, while scaling the translation process to accommodate different page and context sizes dynamically.

### Summary
The `zipmmu.v` module is a crucial component of the Zip CPU architecture, providing the flexibility and functionality required for efficient memory management. Its design considers system modularity, performance optimization, and effective integration into the overall architecture while maintaining a clear separation between configuration and operational phases through the use of distinct Wishbone buses.

### File: zipcounter.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/zipcounter.v
### Overview of `zipcounter.v`

#### Overall Purpose of the File
The `zipcounter.v` file implements a simple counter module for the Zip CPU. Its primary function is to generate a clock tick count, which can be used for process accounting in the CPU, monitoring various CPU stalls, and potentially generating interrupts on rollovers. The counter can be reset but cannot be halted, ensuring it continuously counts clock ticks. It is particularly designed to measure CPU cycles allocated to tasks, and thus aids in understanding resource utilization in the CPU's operation.

#### Inter-module Relationships
The `zipcounter` module interacts with several components within the CPU architecture, including:
- **Interrupt Controller**: The `o_int` output generates an interrupt signal that is likely connected to the overall interrupt management system of the CPU, allowing tasks to handle time-sensitive operations or scheduling.
- **Wishbone Bus Interface**: The module has Wishbone bus inputs (`i_wb_cyc`, `i_wb_stb`, `i_wb_we`, and `i_wb_data`) for reading and writing data, indicating it participates in a bus protocol for communication with memory and other peripherals. Outputs such as `o_wb_stall` and `o_wb_ack` indicate its readiness to communicate over the Wishbone bus.
- **Other Peripherals or Controllers**: Although direct inter-module relationships are not explicitly detailed, it is likely that the counter interacts with other CPU components that report or utilize performance metrics, like the memory controller or task scheduler.

#### Key Signals (Inputs/Outputs)
1. **Inputs**:
   - `i_clk`: Clock input for synchronizing the counter's operations.
   - `i_reset`: Active-high reset signal to initialize or reset the counter.
   - `i_event`: A signal that potentially indicates specific events to be counted or monitored.
   - **Wishbone Bus Signals**:
     - `i_wb_cyc`: Indicates a Wishbone cycle is active.
     - `i_wb_stb`: Indicates that the Wishbone transaction is active.
     - `i_wb_we`: Write enable signal (active high) for writing data.
     - `i_wb_data`: Data input to be written to the counter.

2. **Outputs**:
   - `o_wb_stall`: Indicates if the module is currently stalled and unable to communicate.
   - `o_wb_ack`: Acknowledge signal for the Wishbone interface indicating the end of a transaction.
   - `o_wb_data`: Output data that can be read from the counter.
   - `o_int`: Interrupt signal generated by the counter on specific conditions (like rollover).

#### Behavior of the Module
The behavior of the `zipcounter` module is defined primarily in the `always` block triggered by the rising edge of `i_clk`. Key points include:
- **Initial Conditions**: The interrupt output (`o_int`) and its output data (`o_wb_data`) are initialized to zero.
- **Reset Behavior**: On receiving an active `i_reset`, both `o_int` and `o_wb_data` are reset to zero, ensuring a clean state.
- **Counting Logic**: The module increments a value on each clock cycle, implying that if it is not reset, it continuously counts up.
- **Write Operations**: When the `i_wb_stb` and `i_wb_we` signals are active, the module updates both `o_int` and `o_wb_data`, indicating it processes write requests from the Wishbone bus interface.
- **Interrupt Generation**: The `o_int` signal is likely set when the counted value reaches a certain threshold (presumably the rollover point for a 32-bit value), allowing the CPU to respond to elapsed time or completed tasks.

This design meets its purpose of monitoring and handling task execution times effectively while remaining a simple and efficient solution in the CPU architecture.

### File: icontrol.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/icontrol.v
### Purpose of `icontrol.v`

The `icontrol.v` file implements an interrupt controller designed for managing multiple interrupt sources in a CPU architecture. This module adheres to the Wishbone interface specification, allowing it to operate within a Wishbone compliant system. Its architecture is optimized for minimal latency, allowing interrupts to be processed with minimal delay and in a single clock cycle. This design efficiently facilitates the handling of interrupts, enabling a global interrupt enable feature and the ability to enable/disable specific interrupt lines.

### Inter-Module Relationships

The `icontrol` module plays a crucial role in the CPU architecture by interacting with other components in the system. Specifically, it receives and processes interrupt signals from various sources, potentially including peripherals, other subsystems, or internal events. The interrupts processed by the `icontrol` can influence the CPU's execution flow, indicating to the CPU that it needs to handle certain events or tasks.

Here’s how it typically interacts with other modules:
- **CPU Core**: The CPU core checks the status of interrupt signals from the `icontrol`, enabling it to respond to interrupts as they are asserted.
- **Peripheral Devices**: Peripheral devices route their interrupt signals to the `icontrol`, which consolidates these signals and passes the relevant information to the CPU.
- **Wishbone Bus**: It adheres to the Wishbone bus protocol for communication, allowing configuration and status reading/writing.

### Key Signals (Inputs and Outputs)

The key signals associated with the `icontrol.v` module include:

- **Inputs**:
  - **Interrupt Signals**: These are the interrupt requests from various sources, represented by bits (0-14).
  - **Control Signals**: These include both the global interrupt enable bit and specific enable bits (16-30).

- **Outputs**:
  - **Global Interrupt Enable Output**: Indicates whether interrupts are enabled globally (based on bit 31).
  - **Interrupt Pending Signals**: Status signals that indicate which interrupt sources are currently pending, represented by bits 0-14.
  - **Any Interrupt Pin**: An output that is set high if any interrupt is pending (bit 15).

### Behavior of the Module

The `icontrol` module operates according to a well-defined set of rules for processing interrupts. Here’s how its behavior can be characterized:

1. **Global Interrupt Control**: The presence of a global enable bit allows for a quick overriding of all individual interrupt lines. If this bit is set, interrupts can be generated; if cleared, individual interrupt lines can be managed without generating global interrupts.

2. **Interrupt Enable/Disable**: Bits 16-30 control individual interrupt source lines. A write to the register with a specific bit set enables that interrupt source, while writing with the global enable bit cleared disables it.

3. **Pending Interrupt Logic**: The module maintains a set of pending interrupt bits (bits 0-14). These bits are set whenever the corresponding interrupt source indicates a pending condition, regardless of whether that interrupt source is enabled. Writing a '1' to a specific bit clears that bit.

4. **Single-Cycle Access**: The design allows for interrupt status reading and configuration to occur in a single clock cycle, reducing the latency involved in managing interrupts.

5. **Parameterizable Behavior**: The module features a parameter `IUSED`, which allows the number of interrupts managed by the controller to be specified, providing flexibility in how the interrupt controller is integrated into various systems.

This design methodology emphasizes a balance between performance and configurability, enabling efficient and effective management of interrupts in a lightweight CPU architecture.

### File: axilperiphs.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/axilperiphs.v
### Overall Purpose of the File
The `axilperiphs.v` file implements an AXI-lite peripheral interface for managing various peripherals in a CPU architecture. Specifically, it serves as an interface for several embedded hardware functions, such as an interrupt controller, watchdog timer, and timer registers. Essentially, it acts as a bridge between the AXI-lite bus and the CPU, enabling configuration and control of various subsystems through a simple memory-mapped interface.

### Inter-module Relationships
The `axilperiphs` module interacts with various other components within the CPU architecture, particularly through its AXI-lite interface. It communicates with the following types of modules:
- **AXI Master Modules**: Other components in the system can issue read and write transactions through the AXI interface to configure or retrieve status information from the peripherals.
- **CPU Modules**: It receives signals from the CPU for control and status, such as reset and interrupt flags. This means it likely works closely with modules responsible for processing interrupts and managing CPU states (halted, running, etc.).
- **Peripherals**: The module connects directly to several core peripherals that are defined within its registers, allowing it to handle operations related to timers and interrupt processing.

### Key Signals (Inputs/Outputs)
The key signals in the module include the following:

#### Inputs
- **AXI Control Signals**:
  - `S_AXI_ACLK`: AXI clock input.
  - `S_AXI_ARESETN`: AXI reset input (active-low).
  - `S_AXI_AWVALID`, `S_AXI_WVALID`, `S_AXI_ARVALID`: Valid signals for write and read commands.
  - `S_AXI_AWADDR`: Address for write operations.
  - `S_AXI_WDATA`: Data being written to the peripheral.
  - `S_AXI_BREADY`, `S_AXI_RREADY`: Handshake signals from the master confirming readiness to process response data.

- **CPU Control Signals**:
  - `i_cpu_reset`: Resets the CPU.
  - `i_cpu_halted`: Indicates that the CPU is halted.
  - `i_cpu_gie`: General interrupt enable signal.
  - Other signals indicating states that may affect how peripherals operate, such as `i_cpu_pfstall` (prefetch stall) and `i_cpu_opstall` (operation stall).

#### Outputs
- **AXI Control Outputs**:
  - `S_AXI_AWREADY`, `S_AXI_WREADY`, `S_AXI_ARREADY`: Ready signals for AXI write and read commands.
  - `S_AXI_BVALID`, `S_AXI_BRESP`: Status of the write operation.
  - `S_AXI_RVALID`, `S_AXI_RDATA`, `S_AXI_RRESP`: Data and status for read operations.

### Behavior of the Module
The module's behavior involves processing AXI-lite transactions aimed at controlling and reading from the peripherals. Here is a high-level overview of its functionality:

1. **Initialization and Reset Handling**: On reset, the module initializes its state and prepares to respond to AXI commands. It can reset its internal state based on the `i_cpu_reset` signal.

2. **AXI Write Operations**: If a write is valid (`S_AXI_WVALID`), the module acknowledges the operation by asserting `S_AXI_WREADY`, and writes the data to the corresponding peripheral registers based on the address provided in `S_AXI_AWADDR`.

3. **AXI Read Operations**: For read operations, upon valid read requests (`S_AXI_ARVALID`), the module uses the address to determine which peripheral register to read from and responds with the appropriate data and status.

4. **Interrupt Processing**: The module's interactions with external interrupts (`i_`) involve handling incoming interrupt signals, indicating to the CPU when an interrupt needs to be serviced.

5. **Control Logic**: Control logic manages the state of read/write operations and ensures proper handshaking with the AXI master to facilitate smooth communication.

In summary, the `axilperiphs.v` module is critical for facilitating communication between a CPU and various peripheral devices, supporting operations such as interrupts and timer management while adhering to the AXI protocol.

### File: wbwatchdog.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/wbwatchdog.v
### Overall Purpose of the File
The `wbwatchdog.v` file implements a watchdog timer for the Zip CPU architecture. The watchdog's primary function is to monitor system activity by counting down from a specified timeout value. If the timer reaches zero without being reset, it triggers an interrupt to signal that a timeout condition has occurred, indicating potential issues such as a system hang or failure in expected responses.

### Inter-module Relationships
The `wbwatchdog` module interacts with other components of the CPU ecosystem in the following ways:
- It receives the `i_timeout` value which is a constant input that defines how long the watchdog will count down before triggering an interrupt (`o_int`).
- The watchdog's output interrupt signal (`o_int`) can be used by other modules (such as an interrupt controller or the CPU core itself) to take necessary actions upon a timeout condition.
- The interaction with the clock (`i_clk`) and reset (`i_reset`) inputs allows the watchdog to align its behavior with the overall CPU clock cycle and system reset operations.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_clk`: The system clock signal, used to synchronize the operation of the watchdog timer.
  - `i_reset`: A signal to reset the timer and interrupt status.
  - `i_timeout[(BW-1):0]`: A constant value indicating the timer's initial countdown threshold.

- **Outputs**:
  - `o_int`: An interrupt signal that indicates when the timer has counted down to zero, alerting other modules to a timeout condition.

### Behavior of the Module
1. **Initialization**: The internal register `r_value` is initialized to all ones. During the first positive edge of the clock after a reset, it is set to the `i_timeout` value. This register acts as the countdown timer.
   
2. **Counting Logic**: On each subsequent clock cycle, if not in an interrupt state (`!o_int`), the module increments `r_value`. The counting approach used in this implementation effectively behaves as counting down by adding one to a register initialized to `i_timeout`, though the actual operation is incrementing:

   ```verilog
   r_value <= r_value + {(BW){1'b1}}; // effectively counting down by adding 1 
   ```

3. **Interrupt Logic**: The interrupt signal `o_int` is set when `r_value` equals `0`, indicated by `r_value == { {(BW-1){1'b0}}, 1'b1 }`. This condition triggers notifications of a timeout:

   - If the timer is reset (`i_reset`), the interrupt signal also resets to `0`.
   - The interrupt signal indicates active timeout conditions when the timer reaches zero.

4. **Control Logic**: The module effectively has a simple state machine that keeps track of whether counting is active (not in interrupt state) and manages the reset state appropriately to ensure that any anomalies in operation can be detected by the interacting CPU modules.

In summary, the `wbwatchdog.v` module provides a crucial function for monitoring and managing CPU activity via a timeout mechanism, helping to maintain system integrity and assist in debugging efforts during development or operational phases. Its interaction with signals related to timing and interrupts underlines its importance in the overall CPU architecture.

### File: wbdown.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/wbdown.v
### Purpose of the File

The `wbdown.v` file implements functionality for down-converting a Wishbone bus from a wider data width to a smaller one in the context of a CPU architecture. It is designed to facilitate communication between components that may have differing data width requirements, effectively allowing for seamless integration and data transfer across modules with varying interface specifications.

### Inter-module Relationships

The `wbdown` module interacts with multiple other components within the CPU architecture, particularly those that utilize the Wishbone protocol for communication. The interactions can be summarized as follows:
- **Wide Bus Interface**: It receives inputs from a wider width interface (such as a wider CPU or memory bus) via signals like `i_wcyc`, `i_wstb`, and `i_wdata`. 
- **Small Bus Interface**: It outputs to a smaller width interface (like peripherals or smaller modules) through signals such as `o_cyc`, `o_stb`, and `o_data`.
- **Arbitration & Acknowledgment**: It provides signals for acknowledgment (like `o_wack`, `i_ack`) and handles stalls (`o_wstall`, `i_stall`), facilitating proper communication flow and back-pressure signaling as required by the operation of the involved components.

### Key Signals

**Inputs**:
- `i_clk`: Clock signal for synchronous operation.
- `i_reset`: Reset signal to initialize or reset the module.
- `i_wcyc`, `i_wstb`, `i_wwe`: Wishbone control signals for wide bus transactions.
- `i_waddr`: Address for the wide bus.
- `i_wdata`: Data input for the wide bus.
- `i_wsel`: Byte select for the wide bus.
- `i_stall`: Stall signal from the smaller bus side.
- `i_ack`: Acknowledgment signal from the smaller bus side.
- `i_data`: Data input from the smaller bus.
- `i_err`: Error signal from the smaller bus.

**Outputs**:
- `o_cyc`, `o_stb`, `o_we`: Control signals for the smaller bus transactions.
- `o_addr`: Address for the smaller bus.
- `o_data`: Data output for the smaller bus.
- `o_sel`: Byte select for the smaller bus.
- `o_wstall`: Stall signal directed back to the wide bus.
- `o_wack`: Acknowledgment signal directed back to the wide bus.
- `o_wdata`: Transmitted data sent back on the wide bus.
- `o_werr`: Error signal sent back on the wide bus.

### Behavior of the Module

The behavior of the `wbdown` module can be described as follows:

1. **Data Path Adjustment**: 
   - If the data widths of the wide and small buses are the same (i.e., `WIDE_DW == SMALL_DW`), the module directly assigns input signals to output signals without modification. This is handled under the `NO_ADJUSTMENT` generate block.
   
2. **Control Logic**: 
   - The module generates the necessary control signals (i.e., `o_cyc`, `o_stb`, `o_we`, etc.) based on incoming wide bus signals. This implies that when a transaction occurs on the wide bus (indicated through `i_wcyc`, `i_wstb`), equivalent signals are asserted for the smaller bus.
   
3. **Stall and Acknowledgment Handling**:
   - The module tracks stall conditions and acknowledgments. If there is a stall signal from the small bus, it propagates that to the wide bus through the `o_wstall` output. The module also handles acknowledgment and error propagation back to the wide bus.

4. **Data Consistency**: 
   - The module ensures that data flow is seamless and that the widths are properly managed. It uses the `i_wsel` input to denote the active byte lanes in the original wider data format, which influences how data is consolidated and presented in smaller widths.

Overall, the `wbdown` module serves as an crucial interface for managing differing data widths within the CPU architecture, handling both control and data signals effectively.

### File: addrdecode.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/addrdecode.v
### Purpose of the File
The `addrdecode.v` file implements an address decoder for the Zip CPU architecture. Its main role is to decode the incoming address lines from a master (likely a CPU) and determine which slave device (memory or peripheral) should respond to the request based on the address provided. 

### Inter-module Relationships
The `addrdecode` module interacts with various components of the Zip CPU architecture, specifically:
- **Master Devices**: It receives address requests from a master (like the Zip CPU itself) that needs to access slaves.
- **Slave Devices**: The module routes address requests to slave peripherals or memory that are defined by the parameters `SLAVE_ADDR` and `SLAVE_MASK`. 
- **Bus Systems**: It is often connected to a bus system (like AXI), using the `ACCESS_ALLOWED` parameter to manage read and write access to the different slave devices.

### Key Signals
- **Inputs**:
  - The inputs are not fully listed, but key inputs likely include address lines from the CPU or a master device that will dictate which peripheral or memory is being addressed.
  
- **Outputs**: 
  - The expected outputs would typically include:
    - Signals to indicate which slave device has been selected based on the decoded address.
    - Control signals to enable or disable communication with the selected slave.
  
### Behavior of the Module
The `addrdecode` module contains several key behaviors:
1. **Address Mapping**: It maps incoming addresses to specific slaves via the `SLAVE_ADDR` and `SLAVE_MASK` parameters. This allows it to determine which slave(s) can potentially respond to an access request.
  
2. **Access Control**: Through the `ACCESS_ALLOWED` parameter, the module allows for configurable access rights on a per-slave basis. This helps in determining whether a master can initiate read or write operations on particular slaves.

3. **Registered Output (if OPT_REGISTERED is set)**: If the `OPT_REGISTERED` parameter is enabled, the address decoding is registered, meaning the output will only change on a clock edge. This can help with timing and setup/hold requirements in a pipelined environment.

4. **Low Power Mode (if OPT_LOWPOWER is set)**: Under low power conditions, the module may minimize activity to conserve power, which could affect how often or when slaves are accessed.

### Control Logic
The module likely contains combinational logic to perform the address decoding as well as possibly state machines for managing the registered outputs and access rights. This would involve:
- Comparisons between the incoming address and predefined slave address ranges (using `SLAVE_MASK`).
- Generation of control signals based on the results of the comparisons that drive the access to slave devices.

In summary, the `addrdecode.v` module is crucial in determining which peripheral or memory block is accessed during CPU operations based on address requests, allowing for flexible and efficient bus management in the Zip CPU architecture.

### File: axilxbar.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axilxbar.v
### Description of `axilxbar.v`

#### Overall Purpose
The `axilxbar.v` file implements a crossbar interconnect for AXI-lite communication in a CPU architecture, specifically designed to connect multiple AXI-lite master sources to multiple AXI-lite slave destinations. Its purpose is to facilitate dynamic communication between masters and slaves, allowing any master to talk to any slave as long as that slave is available (not busy), thus enhancing data throughput within the CPU system.

#### Inter-module Relationships
The crossbar connects the various masters (CPU cores or peripheral devices that generate transactions) to slave devices (memory, I/O peripherals, or other components that respond to transactions). This module interacts directly with:

- **Masters:** It takes input from multiple master devices, managing requests and granting access.
- **Slaves:** It outputs requests and data to slaves, managing responses.
- **Arbiter Logic:** The crossbar implements arbiter logic that ensures that one master can communicate with a slave at any one time, ensuring no two masters attempt to access the same slave simultaneously.
- **Transaction Control Logic:** Since the crossbar inherently introduces latency, it ensures that the timing of requests and responses is managed properly across the clock cycles.
  
This interaction allows for efficient communication and resource sharing in a multi-master, multi-slave scenario.

#### Key Signals (Inputs/Outputs)
1. **Inputs:**
   - **Master Request Lines:** Signals from each master indicating a request to access one or more slave devices.
   - **Slave Address Signals:** Signals to determine which slave each master is attempting to communicate with.
   - **Control Signals:** Signals to manage the grant process and acknowledge responses from slaves.

2. **Outputs:**
   - **Slave Access Grant Lines:** Signals that specify which master has been granted access to a slave.
   - **Slave Data Outputs:** Data being sent from the masters to the slaves and acknowledgments coming back from the slaves.

#### Behavior of the Module
1. **Transaction Handling:**
   - It performs arbitration to grant access to the first master requesting access to a slave, while keeping track of transaction status.
   - It ensures that once a master is granted access, it holds that access until the transaction is completed, preventing other masters from conflicting.

2. **Latency Management:**
   - It is designed to manage up to four clock cycles of latency due to its architectural design that requires sequential transaction steps (e.g., requesting, granting, acknowledgments).

3. **Control Logic:**
   - The crossbar uses control logic to handle transitions between states based on master requests and slave availability.
   - Masters have priority based on their assigned number; lower-numbered masters get priority in access contention scenarios.

4. **Dynamic Adjustments:**
   - It monitors conditions such as response reception to manage grant assignments accurately.
   - Grants can be lost if there is no activity (idle timeout), or if a higher priority master requests access.

5. **Special Handling:**
   - There is a special handling mechanism for cases where no valid address is provided, allocating a default slave for such scenarios.

6. **Low Power Mode:**
   - If the `OPT_LOWPOWER` configuration is active, the module can deactivate unused outputs, potentially reducing power consumption.

Overall, the `axilxbar.v` module serves as an efficient communication backbone, enabling dynamic and concurrent transactions between multiple masters and slaves while handling latency and priority effectively.

### File: zipdma_check.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/zipdma_check.v
### Overall Purpose of the File
The file `zipdma_check.v` is designed to implement a testing module for the ZipDMA (Direct Memory Access) subsystem of the Zip CPU architecture. It primarily focuses on verifying the operation of the ZipDMA by simulating interactions over a Wishbone bus interface, which is a common bus standard for interconnected hardware modules. By providing a testing mechanism, it ensures the accuracy and reliability of data transactions involving the DMA.

### Inter-module Relationships
The `zipdma_check` module interacts with other components in the Zip CPU architecture primarily via the Wishbone bus. It accepts inputs from various Wishbone signals for controlling data transfers and acknowledging transactions. The following are key aspects of its inter-module relationships:

- **Wishbone Interface**: The module provides inputs and outputs associated with the Wishbone protocol, including signals for initiating a cycle (`i_wb_cyc`), strobing a transaction (`i_wb_stb`), indicating read/write operations (`i_wb_we`), and addressing (`i_wb_addr`). It provides outputs that confirm the success or failure of transactions, such as the acknowledgement signal (`o_wb_ack`).
  
- **Collaboration with DMA Module**: Although not explicitly instantiated in this file, the operations and data flows simulated within `zipdma_check` are intended to validate the behavior of the ZipDMA module that would be communicating through this interface.

### Key Signals (Inputs/Outputs)
The module defines several critical inputs and outputs:

#### Inputs:
- `i_clk`: The clock signal driving the module's behavior.
- `i_reset`: A reset signal to initialize the module.
- `i_wb_cyc`, `i_wb_stb`, `i_wb_we`: Control signals for initiating bus transactions.
- `i_wb_addr`: The address for the Wishbone operation.
- `i_wb_data`: The data being written to the bus.
- `i_wb_sel`: The byte selection for the write operation, indicating which bytes of the word are valid.

#### Outputs:
- `o_wb_stall`: Indicates if the operation should stall.
- `o_wb_ack`: Acknowledgement output that confirms a transaction has been successfully completed.
- `o_wb_data`: The data output from the module.
- `o_wb_err`: Indicates any errors that occur during the transaction.

#### Wishbone Status Port Inputs/Outputs:
- Similar inputs (`i_st_cyc`, `i_st_stb`, `i_st_we`, etc.) and outputs (`o_st_stall`, `o_st_ack`, etc.) are also defined for managing transactions on the status port of the module.

### Behavior of the Module
The behavior of `zipdma_check` is characterized by several features:

1. **Local Parameter Definitions**: The module defines local parameters for data width (DW), address width (AW), and byte width (BW), which are computed based on the parameters passed to the module.

2. **Data Enable Generation**: Signals `rd_data_en` and `wr_data_en` are generated to determine when a read or write operation has been requested based on the Wishbone signals.

3. **Wishbone Output Assignments**: The outputs for the Wishbone protocol are continuously driven:
   - `o_wb_stall` is set to `0`, indicating no stalls.
   - `o_wb_err` is set to `0`, indicating no errors.
   - `o_wb_data` reflects the internal state represented by an LFSR (Linear Feedback Shift Register) value stored in `lfsr_state`.

4. **Acknowledgement Logic**: The `o_wb_ack` signal is a registered output that would typically change based on transaction conditions. This acknowledgment signal is crucial for signaling to the requesting module whether the requested operation was successful or not.

5. **Stateful Behavior**: The module maintains local states and counters (`rd_count` and `wr_count`) to track read and write operations, which could potentially be used within the behavior of the module for controlling or monitoring purposes.

Overall, `zipdma_check.v` is a crucial component for testing the interaction of Wishbone based DMA transactions within the Zip CPU architecture, ensuring that the DMA operations perform as expected when interfacing with other modules over the bus.

### File: wbxbar.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/wbxbar.v
### Overall Purpose of the File
The `wbxbar.v` file implements a configurable Wishbone cross-bar interconnect for a RISC CPU architecture known as the Zip CPU. This interconnect adheres to the WB-B4 pipeline specification and enables communication between multiple master and slave components in the CPU system. The cross-bar allows for concurrent transactions, enhancing system performance by managing the routing of requests and responses among different masters and slaves.

### Inter-module Relationships
The `wbxbar` module interacts with various other components in the CPU architecture:
- **Masters:** It serves as the central hub for multiple masters (such as different CPU cores, memory controllers, or peripherals) to send requests.
- **Slaves:** It connects to various slave devices that respond to these requests, which can be memory blocks, I/O devices, or any peripheral that complies with the Wishbone protocol.
- The cross-bar coordinates the timing and access to these slaves, ensuring that the appropriate devices respond without conflicts. By switching input from different masters to various slave outputs, it effectively mediates the communication within the system.

### Key Signals
- **Inputs:**
  - Master request signals, which indicate when a master wants to initiate a transaction (the specific names would be defined in the code).
  - Address and control signals from the masters that specify which slave devices to access and how to interact with them.
  
- **Outputs:**
  - Slave response signals that indicate whether the operation was successful or if an error occurred.
  - Data lines that relay the requested data back to the respective master after a successful read operation, or forward data from the master for write operations.

### Module Behavior
The `wbxbar` module's behavior can be broken down into several key aspects:
- **Transaction Management:** The module manages up to `NM` (number of masters) and `NS` (number of slaves) transactions, allowing one request per clock cycle. 
- **Latency Control:** Transactions are completed in a minimum of three clock cycles: one to initiate the access, another for the data to travel to the slave, and one for the return to the master.
- **Wait States and Timeouts:** The design includes optional timeout mechanisms (`OPT_TIMEOUT`, `OPT_STARVATION_TIMEOUT`). If a slave does not respond within a designated timeframe, a bus error is signaled, enabling the master to handle stalls or prolonged wait states better.
- **Address and Transaction Routing:** The module routes data based on provided address signals, using `SLAVE_ADDR` and `SLAVE_MASK` to define valid addresses and control which slaves respond to specific address requests.
- **Optimization Features:** Several options exist to adjust the performance (such as maximum burst settings, double buffering for increased clock speed, and low-power operation). These optimizations allow for customization based on specific design requirements.

In terms of control logic, while the specifics would depend on the actual code implementation, the module likely includes state management to handle arbitration, transaction initiation, and transfer acknowledgment between the involved masters and slaves. 

Overall, the `wbxbar` is an essential piece of the system architecture, providing robust interconnectivity between processing components and peripherals, fostering effective communication in a pipelined CPU environment.

### File: axilite2axi.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axilite2axi.v
### Overview of `axilite2axi.v`

1. **Overall Purpose of the File:**
   The `axilite2axi.v` file implements a protocol converter that translates AXI Lite interface signals to a full AXI interface. This is significant in a RISC CPU design context, allowing simplified control for peripheral devices through an AXI Lite interface while enabling their connection to the full AXI standard used for data transactions within the CPU and memory subsystems.

2. **Inter-Module Relationships:**
   - The module interacts with AXI slave and master modules, converting requests and responses between the AXI Lite protocol (typically employed for simpler, low-bandwidth data transfers) and the more robust AXI protocol (which supports burst transfers and multiple outstanding transactions).
   - It serves as a bridge between high-level transactions that might come from a CPU or higher-level peripheral interface (using AXI Lite) and the lower-level hardware that requires full AXI compliance. 
   - This can be critical for integrating memory controllers, DMA engines, or other peripherals that operate on an AXI interface while providing a simplified interface for lower-complexity components.

3. **Key Signals (Inputs/Outputs):**
   - **Inputs:**
     - **ACLK:** Clock signal for synchronization.
     - **ARESETN:** Active-low reset signal for initializing the state of the module.
     - AXI Lite signals such as `S_AXI_AWVALID`, `S_AXI_AWADDR`, `S_AXI_WVALID`, `S_AXI_WDATA`, etc., which are used for write requests.
     - Signals for read requests such as `S_AXI_ARVALID`, `S_AXI_ARADDR`.
   
   - **Outputs:**
     - Signals like `M_AXI_AWVALID`, `M_AXI_AWADDR`, `M_AXI_WVALID`, `M_AXI_WDATA`, etc., that are generated for full AXI operation.
     - `S_AXI_BVALID`, `S_AXI_RVALID` to indicate the validity of responses from the slave side.
     - Read data and response signals (`S_AXI_RDATA`, `S_AXI_RRESP`, etc.).

4. **Behavior of the Module:**
   - The module operates by handling state transitions based on the input signals. It maintains a state machine that regulates the acknowledgment of requests and readiness to accept further transfers.
   - When an AXI Lite write request is detected (`S_AXI_AWVALID` & `S_AXI_WVALID`), it converts this transaction into a full AXI transaction by asserting the corresponding master interface signals (`M_AXI_AWVALID`, etc.) and includes responses on the slave interface as required.
   - Similarly, for read operations, it processes `S_AXI_ARVALID` and appropriately drives the master signals for reading data from an AXI-compliant peripheral.
   - The module likely includes control logic to manage handshaking between the AXI Lite and AXI interfaces ensuring proper timing and valid data transfers, thus implementing a complete protocol conversion.

### Summary:
The `axilite2axi.v` module is a critical component in a RISC CPU design, allowing simplified control via AXI Lite to be effectively translated to the more complex requirements of the AXI standard interface. It manages state transitions, handles control signals, and ensures seamless communication between the CPU and peripherals, thereby enhancing the overall design's flexibility and functionality.

### File: memdev.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/memdev.v
### Overall Purpose of the File

The `memdev.v` file implements a simple on-chip memory module that can be accessed via the Wishbone bus. It is designed to support single-cycle pipelined access to memory, which is essential for a CPU architecture requiring efficient and quick data retrieval and storage. This module serves as a memory device that can be utilized in the Zip CPU project, enabling the storage of instructions and data required for operation.

### Inter-module Relationships

The `memdev.v` module interacts with other parts of the CPU architecture, specifically as a memory device connected to the Wishbone bus. It interfaces with:

- **Wishbone Bus**: It receives control signals from other modules (e.g., CPU core) over the Wishbone protocol, enabling read and write operations.
- **The CPU Core**: Functional blocks such as the CPU core send instructions and data to be stored in, or retrieved from, this memory module.

This interaction allows the CPU to fetch instructions and store results efficiently, as `memdev` plays a vital role in maintaining the pipeline operation of the Zip CPU system.

### Key Signals (Inputs/Outputs)

#### Inputs:
- `i_clk`: Clock signal for synchronizing operations.
- `i_reset`: Reset signal for initializing the memory state.
- `i_wb_cyc`: Indicates a Wishbone cycle is in progress.
- `i_wb_stb`: Strobe signal to signify the assertion of a request.
- `i_wb_we`: Write enable signal to indicate a write operation.
- `i_wb_addr`: Address for the memory operation.
- `i_wb_data`: Data input to be written to memory in the case of a write operation.
- `i_wb_sel`: Byte enable signal that indicates which bytes of `i_wb_data` are valid.

#### Outputs:
- `o_wb_stall`: Stalling signal to regulate the pacing of requests.
- `o_wb_ack`: Acknowledge signal indicating completion of a Wishbone operation.
- `o_wb_data`: Data output on read operations.

### Behavior of the Module

The `memdev.v` module involves the following behavior:

1. **Memory Declaration**: It declares a 2D array `mem` to represent the memory space, where the size is based on the parameterized address width (`AW`).

2. **Memory Initialization**: If a `HEXFILE` is provided, the module loads initial values into the memory from the specified hex file using the `$readmemh` function during simulation. This is useful for preloading the memory with instruction code or data.

3. **Transaction Handling**:
    - When the `EXTRACLOCK` parameter is set to `0`, the module assigns the input WISHBONE signals directly to internal control signals for processing the request in the same clock cycle.
    - In the case where `EXTRACLOCK` is set to `1`, indicating an extra clock cycle for memory operations, additional logic is implemented to handle the timing of transactions.
    
4. **Operations**:
    - The module responds to WISHBONE transactions by checking the `i_wb_stb` (strobe) and `i_wb_we` (write enable) signals. If a write operation is indicated, the corresponding data is written to the memory at the specified address. For read operations, the data from the corresponding address in the memory is assigned to the output `o_wb_data`.

5. **Acknowledge and Stall Signals**: The `o_wb_ack` signal is utilized to inform the CPU core that the requested operation has been completed, while `o_wb_stall` can be used to delay requests if necessary, ensuring proper synchronization and data flow within the overall pipeline architecture.

In summary, `memdev.v` is crucial for the operation of the Zip CPU, implementing memory management that interfaces with the broader system architecture while ensuring efficient operation through pipelining and appropriate data handling mechanisms.

### File: axi_tb.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axi_tb.v
### Overall Purpose of the File
The `axi_tb.v` file serves as the top-level testbench for the Zip CPU, particularly focused on testing all configurations related to AXI (Advanced eXtensible Interface) and AXI-lite. This module establishes a simulation environment that allows for testing the CPU's functionality, including its various memory operations, console port functionality, and external debugging capabilities. It is designed to facilitate comprehensive testing to help identify and rectify any potential bugs before official releases.

### Inter-module Relationships
The testbench interacts with several other modules in the CPU architecture, including:
- **Memory:** It simulates access to memory, providing the necessary interfaces to read and write data during tests.
- **Console port:** Provides an interface to output messages directly to the console, facilitating easier debugging.
- **External Debug Access:** This allows external tools or facilities to monitor and control the internal states of the CPU during the test.
- **WBScope:** Likely for visualization and monitoring of the Wishbone bus signals. 

Through these interactions, the testbench can simulate various scenarios that the CPU might encounter in real-world applications.

### Key Signals (Inputs/Outputs)
The module leverages several parameters that configure its behavior, although specific signal definitions were not included in the given text. Here are some notable parameters (considered as "signals" in this context):
- **PARAMETERS:** 
  - `ADDRESS_WIDTH` (28 bits): Defines the addressable memory width.
  - `BUS_WIDTH` (32 bits): Specifies the width of the data bus.
  - Several options (e.g., `OPT_ZIPAXIL`, `OPT_PIPELINED`, `OPT_LGICACHE`, etc.) that determine various configurations and capabilities of the CPU such as pipelining, cache sizes, and operational features (like multiplication and division).

### Behavior of the Module
The behavior of the testbench involves setting up the simulation environment and iterating through a series of test scenarios to evaluate the CPU's performance. Although the provided code does not include specific control logic or state machine definitions, we can informally deduce typical activities from a testbench module, such as:

- **Initialization:** Setting up initial conditions for simulation, such as resetting the CPU and configuring memory.
- **Stimuli Generation:** Generating inputs that mimic various instruction sequences that the CPU needs to process.
- **Monitoring:** Observing outputs and states of the CPU during operation to check for expected behavior, such as correct memory reads/writes and correct execution of instructions.
- **Timing Analysis:** Utilizing time scales to simulate the required delays between clock cycles and operations.

In the context of AXI, the module would also likely include control logic that handles AXI-specific handshake signals, ensuring proper data transfer between the CPU and memory or peripherals.

### File: wb_tb.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/wb_tb.v
### Overall Purpose of the File

The `wb_tb.v` file serves as a top-level testbench for the Zip CPU, focusing on different Wishbone configurations. It aims to simulate and validate the functionality of the Zip CPU by providing the necessary environment to test various components and configurations of the CPU. It includes essential elements like memory, a console port for debugging (not a serial port), external debug access, and a WBScope for visualization of signals. The intention is to perform rigorous testing, ensuring the CPU operates correctly across its various configurations before any official release.

### Inter-module Relationships

The `wb_tb.v` file interacts with several other modules within the Zip CPU architecture, primarily focusing on the following:

- **Memory Modules**: It interfaces with memory components to simulate read/write operations during the execution of test programs.
- **Console Port**: Facilitates direct output to the console for debugging information, allowing the monitoring of CPU operations during the test runs.
- **WBScope Module**: Provides visualization tools for observing the signals and behavior of the Wishbone bus, aiding in debugging and performance analysis.

The testbench effectively connects to the CPU core and its subsystems, engaging in instruction fetching and execution as governed by the configured Wishbone bus standards.

### Key Signals (Inputs/Outputs)

While the provided code snippet does not show all the signals explicitly defined, we can infer the following key signals:

- **Inputs**: Likely consist of clock and reset signals, alongside any specific configuration parameters passed to various components.
- **Outputs**: Would encompass data signals related to memory transactions, control signals for various CPU operations, and potentially status flags for the testbench results, facilitating the assessment of whether the simulations pass or fail.

### Behavior of the Module 

The behavior of the `wb_tb` module can be outlined as follows:

1. **Parameterizable Configurations**: The module accepts various parameters (e.g., address and bus width, cache options, memory operations) that can be adjusted to match specific test scenarios or configurations of the Zip CPU.

2. **Instantiating Components**: The testbench instantiates the Zip CPU and other required components (like memory, wishbone interface, etc.), establishing the necessary environment for operation.

3. **Simulation Control**: The module likely includes control logic to manage the simulation time, including clock generation and reset conditions, as well as monitoring states of the instantiated modules.

4. **Data Processing**: It facilitates the testing of data processing by injecting test vectors into the CPU and checking the responses, capturing any deviations from expected behavior.

5. **Debugging Features**: By using the console output and possibly integrating with external debugging tools, the testbench provides visibility into the internal workings of the CPU during the simulation, logging important events and states.

6. **Test Execution**: The testbench is designed to run a defined set of CPU instructions or a complete test program to validate the integrated architecture's behavior under various scenarios.

Overall, the `wb_tb.v` serves as a comprehensive infrastructure for testing and debugging the Zip CPU, ensuring that it meets performance and functionality standards prior to utilization in broader contexts.

### File: axilempty.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axilempty.v
### Description of the `axilempty.v` Verilog File

#### Overall Purpose
The `axilempty.v` file implements a minimal AXI-lite interface that serves as a dummy slave module. It is specifically designed for scenarios where there are AXI masters trying to initiate communications but no actual slave devices are present. This empty shell handles incoming AXI transactions and responds appropriately, ensuring that requests do not generate unhandled responses. This is particularly useful during system testing or when simulating a bus where some master buses have no corresponding slaves.

#### Inter-module Relationships
In the context of the CPU architecture, the `axilempty` module interacts with AXI master modules—these could be memory controllers or processing units that attempt to communicate with peripherals over the AXI interface. The module essentially allows these masters to issue requests while knowing there will be safe, well-defined responses (specifically error signals in lieu of actual data or status). It is connected to the broader AXI system, enabling proper handling of read and write requests even when no functional slave devices are connected.

#### Key Signals
**Inputs:**
1. `S_AXI_ACLK`: The clock signal for the AXI interface.
2. `S_AXI_ARESETN`: Active-low reset signal for the AXI interface.
3. `S_AXI_AWVALID`: Indicator that an address write transaction is valid.
4. `S_AXI_WVALID`: Indicates that write data is valid.
5. `S_AXI_BREADY`: Indicates that the master is ready to receive the response for a write transaction.
6. `S_AXI_ARVALID`: Indicates that an address read transaction is valid.
7. `S_AXI_RREADY`: Indicates that the master is ready to accept read data.

**Outputs:**
1. `S_AXI_AWREADY`: Indicates that the slave is ready to receive a write address.
2. `S_AXI_WREADY`: Indicates that the slave is ready to receive the write data.
3. `S_AXI_BVALID`: Indicates that the slave has created a response for a write transaction.
4. `S_AXI_BRESP`: Contains the response indicating whether the write was successful or an error occurred.
5. `S_AXI_ARREADY`: Indicates the slave is ready to receive a read address.
6. `S_AXI_RVALID`: Indicates that the slave has valid read data.
7. `S_AXI_RDATA`: Provides the data for read requests.
8. `S_AXI_RRESP`: Contains the response for read requests, indicating the success or error.

#### Behavior of the Module
The behavior of the `axilempty` module is characterized by its handling of AXI read and write transactions. Here’s an overview of its functionality:

1. **Reset Logic:** The module uses the reset signal (`S_AXI_ARESETN`) to ensure that it can be initialized properly. When active, the module's outputs are set to safe values (typically low).

2. **Write Transactions:**
   - When `S_AXI_AWVALID` is asserted, the module will set `S_AXI_AWREADY` to indicate that it is ready to accept a write address.
   - If `S_AXI_WVALID` is also asserted, it will become `S_AXI_WREADY` to signify readiness to accept data.
   - Upon completing a write transaction, `S_AXI_BVALID` is asserted to indicate a response is ready, and `S_AXI_BRESP` outputs a success or error signal as needed.

3. **Read Transactions:**
   - When `S_AXI_ARVALID` is asserted, the module will assert `S_AXI_ARREADY`, indicating it can receive a read address.
   - Once a read transaction commences, the module generates a response by asserting `S_AXI_RVALID` and providing `S_AXI_RDATA`. The response (`S_AXI_RRESP`) will also indicate success or any errors encountered.

4. **Control Logic:** The control logic ensures that for every transaction made by the masters, defined responses (valid or error) are reliably produced even if no actual data transfer occurs, thereby maintaining a compliant AXI-lite interface operation for the simulation or architecture testing.

In conclusion, `axilempty.v` plays a pivotal role in testing and debugging scenarios where one needs to simulate AXI connections without implementing real peripheral logic or when the system should operate without errors due to lack of hardware.

### File: axi2axilsub.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axi2axilsub.v
### Overall Purpose of the File

The `axi2axilsub.v` file implements a hardware module that converts signals from an AXI (Advanced eXtensible Interface) bus to an AXI-Lite bus. The main goal of this conversion is to enable communication between master and slave devices in a system where the master operates using the AXI protocol while the slave utilizes the less complex AXI-Lite protocol. The module ensures that this conversion maintains a performance level equivalent to that of the AXI protocol, allowing transactions to be completed in a single clock cycle. Additionally, the design is configurable in terms of data width, which can be resized for potential improvements based on specific application requirements.

### Inter-module Relationships

The `axi2axilsub` module interacts with several components in the larger CPU architecture:
1. **AXI Master Modules**: Communicates with AXI masters that use the full AXI protocol.
2. **AXI-Lite Slave Modules**: Connects to AXI-Lite compliant slaves, translating the requests and responses between the two bus types.
3. **FIFO Buffers**: Utilizes FIFO (First In, First Out) buffers to handle data flow and buffering between the AXI and AXI-Lite interfaces, ensuring that data is synchronized and appropriately queued.
4. **Control Logic Modules**: Interfaces with control logic to manage the state of transactions and monitor the status of data being transmitted.

### Key Signals (Inputs/Outputs)

The module defines several parameters and input/output signals:

1. **Parameters**:
   - `C_AXI_ID_WIDTH`: Width of the AXI ID field.
   - `C_S_AXI_DATA_WIDTH`: Data width for the AXI-Lite slave.
   - `C_M_AXI_DATA_WIDTH`: Data width for the AXI master.
   - `C_AXI_ADDR_WIDTH`: Address width for AXI transactions.
   - `OPT_LOWPOWER`, `OPT_WRITES`, `OPT_READS`: Options that can adjust the functionality related to power management and read/write operations.
   - `LGFIFO`: Specifies the log size of the FIFO used to manage outstanding transactions.

2. **Inputs/Outputs (not explicitly provided in the segment)**:
   - **Inputs**: Typically includes signals like clock, reset, AXI control signals (valid, ready, etc.), address, and data inputs for the AXI side.
   - **Outputs**: Includes AXI-Lite control signals, address, and data outputs, which correspond to the converted AXI-Lite transactions.

(Note: The specific nature of these signals would be obtained from the complete content of the Verilog file, which may not have been provided in the current segment.)

### Behavior of the Module

The `axi2axilsub` module behaves in a way that manages the transition between the AXI and AXI-Lite protocols while ensuring performance consistency:
1. **Transaction Handling**: The module monitors incoming transactions and converts the transaction format to conform to AXI-Lite requirements, adjusting the address widths and data widths as specified by the parameters.
2. **Control Logic**: It incorporates control logic that adjusts signal readiness and acknowledgement based on the AXI protocol's handshaking requirements, thus ensuring that transactions adhere to the necessary timing within the specified clock cycles.
3. **FIFO Buffering**: The FIFO buffers help in managing variable data processing times, allowing the system to accommodate any delays encountered at the AXI-Lite slave side without causing backpressure on the AXI master.
4. **Configuration Flexibility**: The provided parameters allow adaptation in terms of data widths and FIFO sizes, enabling design scalability and adaptability to specific system requirements.
5. **Latency Management**: While ensuring performance during data transactions, the module acknowledges that the AXI specification inherently introduces additional clock cycles (overhead) for AXI-Lite transactions.

Overall, the behavior of the `axi2axilsub` module is crucial for maintaining efficient data transactions within a mixed bus architecture of AXI and AXI-Lite based components in a CPU system.

### File: wbscope.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/wbscope.v
### Purpose of the File
The **wbscope.v** file implements a bus-accessed logic analyzer or scope for the Zip CPU architecture. This module provides the ability to record and report 32-bit values as they transit through the FPGA, effectively allowing monitoring and debugging of data transfers. The scope captures data values upon clock ticks when enabled and can be controlled to stop and start recording based on a trigger signal. This is particularly useful for observing the operational behavior of the CPU in real-time, aiding in debugging and verification tasks.

### Inter-module Relationships
The wbscope module interacts with several other components within the CPU architecture. It specifically connects to the Wishbone bus (a common bus protocol for hardware devices) and potentially interfaces with other modules that communicate over this bus. Here’s how it typically integrates:
- **Data Capture**: It connects to data buses, capturing values that flow through them, which may include outputs from the CPU or other peripherals.
- **Control Interaction**: The wbscope may receive control signals from the CPU or other management modules that dictate when to start or stop recording data.
- **Data Retrieval**: Other modules, such as a CPU core, can read the captured data through the wbscope's provided output ports, allowing examination of past performance or operational states.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - **i_clk**: This clock signal determines when the module checks for data inputs and triggers recording.
  - **i_reset**: A reset signal to clear the recorded data and prepare the scope for a new capture session.
  - **i_trigger**: A control signal that starts the recording process; when activated, the scope begins storing data values.
  - **i_data**: The 32-bit data input from the bus, which is recorded by the scope.
- **Outputs**:
  - **o_triggered**: An output flag that indicates when the trigger condition has been met.
  - **o_stopped**: An output flag that indicates the scope has paused recording after the trigger event.

### Behavior of the Module
The wbscope module employs a control logic that orchestrates the recording of data as follows:

1. **Reset State**: When the i_reset signal is asserted, the module clears any stored data and prepares to begin a new recording session.
  
2. **Recording Phase**: When the i_trigger signal is asserted:
   - The scope captures the value on i_data every clock tick as long as the clock (i_clk) is active and the module is in a recording state.
   - Values are stored in a circular buffer, allowing efficient use of memory and ensuring that the latest data is always available for retrieval.
   - The internal logic manages a pointer or index to track where the next data should be stored in the buffer.

3. **Trigger Condition**: Upon receiving the i_trigger signal, the module sets the o_triggered output high, indicating that data recording has started. 

4. **Stopping Condition**: After the data has been recorded for a certain duration, determined by an internal holdoff parameter (**br_holdoff**), the recording will stop and the o_stopped output will be asserted. This flag signals to other modules that the data capture has concluded and is ready for retrieval.

5. **Data Reading**: During the stopped state, external circuits can read values from the scope. This operation is typically controlled by additional signals that manage the interface between the wbscope module and whatever is reading the data.

6. **Data Management**: The behavior involves managing the circular buffer such that each new write resets the read address, ensuring that the older data can be accessed as required.

Overall, the wbscope module serves as a powerful debugging and monitoring tool within the FPGA-based architecture of the Zip CPU, facilitating various analysis tasks by providing insights into data movement and processing across the bus system.

### File: iscachable.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/iscachable.v
### Description of the Verilog File `iscachable.v`

#### Overall Purpose
The `iscachable.v` file implements a combinatorial logic module that determines whether a specific memory address is cachable within the context of the Zip CPU. This is particularly useful in the design of the data cache (dcache) for the CPU, as it aids in identifying memory addresses that can be stored in the cache versus those that should not. This determination is critical for optimizing memory access and improving the efficiency of the CPU’s operation.

#### Inter-Module Relationships
The `iscachable` module serves as a helper function within the CPU architecture, interacting primarily with the data cache (dcache) module. It is tailored to be used in the test bench configuration of the Zip CPU, which implies that it may also be used in formal verification projects to ensure that the dcache behaves correctly concerning memory addresses. The output from the `iscachable` module (the `o_cachable` signal) informs the dcache regarding which addresses are eligible for caching.

#### Key Signals
- **Inputs**:
  - `i_addr`: A wire input representing the address that is being evaluated to determine its cachability. It is `AW` bits wide, where `AW` is defined based on the parameter `ADDRESS_WIDTH`.

- **Outputs**:
  - `o_cachable`: A registered output signal that indicates whether the input address (`i_addr`) is cachable (`1'b1`) or not (`1'b0`).

#### Behavior of the Module
The `iscachable` module operates entirely as combinatorial logic. It continuously checks the provided address (`i_addr`) against certain parameters defined for memory addresses (`MEM_ADDR` and `MEM_MASK`). The behavior is encapsulated in an `always @(*)` block, which ensures that the output (`o_cachable`) is updated whenever the input (`i_addr`) changes.

- The default value of `o_cachable` is initially set to `0` (non-cachable).
- The logic checks if `MEM_ADDR` is not zero and if the bitwise AND of the input address (`i_addr`) and `MEM_MASK` equals `MEM_ADDR`. If both conditions are true, it sets `o_cachable` to `1`, indicating the address is cachable.

Thus, the module functions by evaluating the input address in relation to a base memory address and a mask, providing a very precise method to determine cachability in a straightforward and efficient manner. This behavior is critical to the overall performance of the CPU, as it supports effective data caching and retrieval mechanisms.

### File: axilcon.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axilcon.v
### Overview of `axilcon.v`

#### Purpose of the File
The `axilcon.v` file implements a basic AXI-Lite console port controller within the Zip CPU architecture. This module provides the interface for communication with various AXI-Lite devices, emulating the functionality of the WBUART core. Its primary function is to facilitate the reading from and writing to a limited set of configuration registers, which are associated with a console or debug interface, allowing user control and interaction with the CPU and peripherals.

#### Inter-module Relationships
The `axilcon` module interacts with other components of the Zip CPU architecture, primarily through the AXI-Lite protocol. It communicates with:

- **AXI-Lite Master**: Executes write and read operations via the standard AXI-Lite signals.
- **Peripheral Modules**: May connect to various peripherals that implement configuration registers or control logic via AXI-Lite, enabling operations such as reading data from or writing data to these peripherals.

#### Key Signals (Inputs/Outputs)
The key signals of the `axilcon` module include:

**Inputs:**
- `S_AXI_ACLK`: The clock signal for the AXI-Lite interface.
- `S_AXI_ARESETN`: The reset signal, active low.
- `S_AXI_AWVALID`: Indicates that a write address is valid.
- `S_AXI_AWADDR`: The address to which data is being written.
- `S_AXI_WVALID`: Indicates that write data is valid.
- `S_AXI_WDATA`: The data to be written.
- `S_AXI_WSTRB`: The write strobes for the data to indicate which bytes to write.
- `S_AXI_BREADY`: Indicates that the master is ready to receive a response.
- `S_AXI_ARVALID`: Indicates that an address for a read is valid.
- `S_AXI_ARADDR`: The address to read data from.
- `S_AXI_RREADY`: Indicates that the master is ready to accept read data.

**Outputs:**
- `S_AXI_AWREADY`: Signals that the module is ready to accept a write address.
- `S_AXI_WREADY`: Signals that the module can accept write data.
- `S_AXI_BVALID`: Signals that a write response is valid.
- `S_AXI_BRESP`: Provides the status of the write operation (success or error).
- `S_AXI_ARREADY`: Signals that the module is ready to accept a read address.
- `S_AXI_RVALID`: Indicates that the requested read data is valid.
- `S_AXI_RDATA`: The data being read from the console port.
- `S_AXI_RRESP`: Provides the status of the read operation.

#### Behavior of the Module
The behavior of the `axilcon` module can be summarized as follows:

- **State Management**: The module maintains states primarily for managing transactions (writing and reading). It uses the `AWVALID` and `WVALID` signals to determine when a write transaction is occurring, and similarly manages `ARVALID` for read transactions.
  
- **Control Logic**: The state machine logic handles the following:
  - Acknowledging valid write addresses and data by asserting `AWREADY` and `WREADY`.
  - Generating valid responses via `BVALID` and `BRESP` after the write operation is completed.
  - Responding to read requests by asserting `ARREADY`, and subsequently providing valid read data and generating a valid response with `RVALID` and `RRESP`.

- **Data Management**: The data written to and read from the module can be configurations or control values. The module is specifically intended for 32-bit data with the underlying structure utilizing a limited address space determined by `C_AXI_ADDR_WIDTH`.

Overall, the `axilcon.v` module serves as a crucial interface in the Zip CPU's architecture, allowing the CPU to configure and communicate with peripherals using the AXI-Lite communication protocol effectively. It encapsulates the necessary control logic to synchronize, validate, and manage data transactions across the AXI-Lite interface.

### File: demofull.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/demofull.v
### Overall Purpose of the File

The `demofull.v` file implements a demonstration of a formally verified AXI4 core interface for a peripheral module designed to be used with the Zip CPU. This core is intended to facilitate the interaction between the AXI (Advanced eXtensible Interface) master and the associated peripheral while ensuring proper data transfer through defined transactions.

### Inter-module Relationships

The module interacts with several other components in the Zip CPU architecture as follows:

1. **AXI Master Module**: The `demofull` serves as an AXI slave in the system and is designed to respond to read and write requests initiated by an AXI master.
2. **Memory Controller/Peripheral Interface**: It handles communication between the CPU and any associated memory or hardware peripheral. This module allows reading and writing of data based on control signals provided by the master interface.

By functioning as a peripheral, `demofull.v` effectively connects the CPU's request for data or instructions to the necessary hardware, allowing for seamless integration within the larger system architecture.

### Key Signals (Inputs/Outputs)

- **Inputs**:
  - `S_AXI_ACLK`: AXI protocol clock signal.
  - `o_we`: Write enable signal.
  - `o_rd`: Read enable signal.
  - Other control and address signals specific to AXI interface (`o_waddr`, `o_wdata`, `o_wstrb`, etc.)

- **Outputs**:
  - `i_rdata`: Data read from the peripheral or memory.
  - Other status signals related to data transfer.

These signals facilitate the fundamental operations of reading from and writing to the peripheral.

### Behavior of the Module

The behavior of the `demofull` module is primarily defined by the following aspects:

1. **Data Transfer Logic**:
   - The module listens for write and read commands based on the `o_we` and `o_rd` signals. 
   - When `o_we` is true, it processes the write operation by iterating through the data bus (`o_wdata`) and updating the internal memory based on the write strobes (`o_wstrb`).
   - When `o_rd` is asserted, it outputs the read data (`i_rdata`) based on the current state of the address inputs.

2. **Control Logic**:
   - Control logic manages the strobe signals and ensures data integrity during writes by defining how writes should be processed (e.g., by updating only specific bytes based on the write strobe).
  
3. **Latency Handling**:
   - The design anticipates a certain latency for read and write operations, as described in the comments. The write channel introduces two clock cycles of latency, and the read channel introduces a single clock cycle of latency. This must be considered during control logic design and system timing.

4. **Parameterization**:
   - The module allows for parameterization around the AXI interface width, address width, and lock options. This flexibility makes `demofull` adjustable for different hardware configurations while remaining compliant with the AXI standard.

Overall, `demofull.v` serves as a robust implementation for managing data transactions in a CPU environment, illustrating both the functional aspect and performance characteristics expected from a typical AXI-based peripheral.

### File: axilscope.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axilscope.v
### Overview of `axilscope.v`

#### Purpose
The `axilscope.v` file is designed to implement a bus-accessed logic analyzer (or 'scope') for the Zip CPU, a small and lightweight RISC CPU soft core. This module records 32-bit values that pass through it every clock cycle when enabled. It captures data until a specified trigger occurs, at which point it records additional data for a designated hold-off period before stopping. This module facilitates debugging by allowing data to be read back in chronological order after the scope has been triggered.

#### Inter-module Relationships
The `axilscope.v` module interacts with other parts of the CPU architecture, specifically:
- **CPU Core**: The scope records data transmitted through the CPU’s buses, helping in debugging and performance analysis.
- **Memory Modules**: If the scope is connected to any memory access lines, it can capture data values being read from or written to memory.
- **Triggering Modules**: The scope works closely with any modules that can generate triggers, indicating when data should be recorded or when certain conditions in the system have been met.
- **Other Peripherals**: It may interface with other peripherals in the system, allowing for comprehensive monitoring of bus activity.

#### Key Signals
- **Inputs**:
  - `i_clk`: The clock signal used to synchronize recording operations. 
  - `i_reset`: A reset signal that initializes the scope’s operational state.
  - `i_trigger`: Input signal that, when asserted, indicates that the data recording should commence or should capture additional data.
  - `i_data`: The data input line where 32-bit values are received for recording in the scope.
  - `i_ctrl`: Control signals that manage the scope's state, possibly to enable or disable the capturing feature.

- **Outputs**:
  - `o_triggered`: An output flag that indicates that the scope has captured the start of a recording phase due to the trigger being asserted.
  - `o_stopped`: An output flag that signifies that the recording has stopped, allowing for data reading.
  - `o_data`: Outputs the recorded values for external reading purposes, organized from oldest to newest.

#### Behavior
The `axilscope.v` module’s behavior is predicated on a finite state machine (FSM) mechanism that manages the recording and retrieval of data:

1. **Reset Phase**: Upon receiving a reset (`i_reset`), the module initializes its internal state, effectively preparing it for operation.
  
2. **Recording Phase**: Once initialized, the module transitions into a recording state where it captures values from `i_data` every clock cycle (`i_clk`) until the `i_trigger` signal is asserted.

3. **Trigger Detection**: When the trigger activates, the module sets the `o_triggered` output high, indicating the capture point. After this, it continues to record for a specified hold-off duration (defined by `br_holdoff`).

4. **Data Capture**: During this time, the captured data is stored in a circular buffer while the module keeps track of the number of entries.

5. **Stop Phase**: After accumulating data for the hold-off period, the module sets the `o_stopped` output high, indicating that data recording has ceased, and the CPU can begin reading from the buffer.

6. **Readout Phase**: While in the stopped state, external modules such as the CPU can read out the buffered data values one at a time, aligned to specific clock cycles (`i_rd` and possibly another clock signal for reading).

7. **Repeat**: Once the data has been read, the scope can be reset for another operation cycle, thus restarting the entire process.

This structured approach allows for comprehensive monitoring and recording of data traffic in a CPU environment, facilitating debugging and analysis of the system's performance and behavior.

### File: axiempty.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axiempty.v
### Description of `axiempty.v`

#### Overall Purpose
The `axiempty.v` file implements a basic AXI core intended to serve as a placeholder for AXI transactions in a larger CPU architecture. The main function of this module is to provide a predefined response to an AXI master when there are no actual slaves connected to the AXI bus. This module essentially simulates a system where invalid or erroneous transactions are handled by returning bus error responses for any requested transactions. This functionality is beneficial during simulation or testing when actual peripherals or memory modules are unavailable.

#### Inter-module Relationships
- The `axiempty` module interacts with other components of the CPU that generate AXI transactions, such as AXI masters (which may belong to different elements like processing units, DMA controllers, etc.).
- It provides feedback to the master regarding the status of the transactions via signals such as `S_AXI_BRESP` for write responses and `S_AXI_RRESP` for read responses.
- By simulating the lack of slaves, this module helps in verifying how the CPU handles unexpected behavior or errors in a controlled environment.

#### Key Signals
- **Inputs:**
  - `S_AXI_ACLK`: The clock signal for synchronous operation.
  - `S_AXI_ARESETN`: The active low reset signal.
  - `S_AXI_AWVALID`: Indicates that the write address is valid.
  - `S_AXI_WVALID`: Indicates that write data is valid.
  - `S_AXI_BREADY`: Indicates that the master is ready to receive a write response.
  - `S_AXI_ARVALID`: Indicates that the read address is valid.
  - `S_AXI_RREADY`: Indicates that the master is ready to receive read data.
  
- **Outputs:**
  - `S_AXI_AWREADY`: Indicates that the module is ready to accept the write address.
  - `S_AXI_WREADY`: Indicates that the module is ready to accept write data.
  - `S_AXI_BVALID`: Indicates that a write response is valid and ready to be sent.
  - `S_AXI_BID`: Contains the ID for the write response.
  - `S_AXI_BRESP`: Contains the write response codes, indicating errors.
  - `S_AXI_ARREADY`: Indicates that the module is ready to accept a read address.
  - `S_AXI_RVALID`: Indicates that a read response is valid and data can be read.
  - `S_AXI_RID`: Contains the ID for the read response.
  - `S_AXI_RDATA`: The read data response (which, in this case, may not be valid as it provides an error).
  - `S_AXI_RLAST`: Indicates the last read response in a burst.
  - `S_AXI_RRESP`: Contains the read response codes, indicating errors.

#### Behavior of the Module
- The `axiempty` module contains control logic to manage AXI transactions based on the provided signals and the clock. The write and read operations are processed independently, primarily involving handling the validity of address and data entries from the AXI master.
- For write operations:
  - When `S_AXI_AWVALID` is asserted, the module will respond with `S_AXI_AWREADY` indicating readiness to accept the address. Once the address is accepted and `S_AXI_WVALID` is also asserted, the module will indicate it is ready to receive data by asserting `S_AXI_WREADY`.
  - After receiving data, the module will always respond as valid with a write response (`S_AXI_BVALID`), along with a response code indicating an error.
  
- For read operations:
  - The `axiempty` module behaves similarly. It responds to `S_AXI_ARVALID` with `S_AXI_ARREADY` when ready to accept a read address.
  - Once the read address is accepted, the module will assert `S_AXI_RVALID` to indicate that a read response is ready, again with an appropriate error response.

The design highlights the importance of handling error responses effectively while being straightforward in terms of state management. The overall structure ensures that the AXI protocol's requirements are respected, even in scenarios where actual bus transactions cannot occur.

### File: axi_addr.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axi_addr.v
### Overview of the Verilog File: axi_addr.v

#### Overall Purpose:
The `axi_addr.v` file implements the address generation logic for the AXI (Advanced eXtensible Interface) protocol compliant system. This module supports complex addressing modes such as FIXED, INCREMENTING, and WRAPPING. Its primary function is to calculate the next address based on the current address and the burst mode, ensuring proper alignment of addresses during data transfer operations. This is crucial for high-performance systems that require compliant and efficient communication between components.

#### Inter-module Relationships:
The `axi_addr` module interacts with other components of the CPU that utilize the AXI protocol for data communication. Specifically, it is integrated with modules that handle AXI transactions, such as:

- **Memory Controllers:** To calculate the next address for read/write operations.
- **Master and Slave AXI interfaces:** To ensure correct information is passed based on the type of burst being performed.
- **Burst Counters or State Machines:** Where the address is fed into control logic that dictates the flow of the AXI transactions.

By providing a consistent method for address calculation, it facilitates predictable and efficient memory access across various components that utilize AXI.

#### Key Signals:

- **Inputs:**
  - `i_last_addr`: The last address that was accessed.
  - `i_size`: Specifies the size of the transfer (e.g., byte, half-word, word).
  - `i_burst`: Defines the type of burst transaction (fixed, incrementing, wrap).
  - `i_len`: Specifies the length of the burst in terms of beats.

- **Outputs:**
  - `o_next_addr`: The computed next address in the sequence based on the burst type and other parameters.

#### Behavior of the Module:
The behavior of the `axi_addr` module includes:

1. **Address Calculation Logic:**
   - The module has several conditional branches that determine how the next address should be calculated based on the current addressing mode (i.e., `i_burst`). 
   - **INCREMENT mode:** Calculates the next address by adding an appropriate increment based on `i_size`.
   - **WRAP mode:** Although not fully shown in the provided excerpt, addresses would typically be manipulated to resemble a circular buffer operation, wrapping around when a specified limit is reached.

2. **Dynamic Address Calculation:**
   - The use of `$clog2(DW)` allows the module to dynamically handle data width variations, which is essential for compatibility with different AXI configurations.

3. **Default Values and Address Increment Logic:**
   - The module initializes and calculates default increments based on the address size. The calculations ensure proper alignment as aligned accesses are critical in the AXI protocol.

4. **Parameterization:** 
   - The module is parameterized (e.g., `AW`, `DW`) to allow flexibility in the address and data widths, making it reusable in various configurations across different designs.

5. **Synthesizable Logic:**
   - The module employs combinational logic evident from the use of `always @(*)`, indicating it responds to changes in the input signals to produce the output `o_next_addr` immediately, ensuring low-latency address computation.

Overall, the `axi_addr` module is a fundamental part of the system that guarantees that address calculations are handled efficiently and according to the specifications of the AXI protocol. Its proper functioning is essential for maintaining high performance in data transactions within the CPU architecture.

### File: axixbar.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axixbar.v
### Purpose of the File

The `axixbar.v` file implements a full crossbar switch designed to connect multiple AXI master components (NM masters) to multiple AXI slave devices (NS slaves) in a System-on-Chip (SoC) architecture. This crossbar allows any master to communicate with any slave, thus enabling flexible and efficient interconnectivity within the system. The core feature of this implementation is to provide the capability of handling transactions per clock cycle, which emphasizes high throughput. However, it also introduces certain latencies due to the arbiter's operation, meaning that there is a minimum latency of four clock cycles for transactions.

### Inter-Module Relationships

The `axixbar` module interacts with other components in the CPU architecture by serving as a bus arbiter and interconnect, allowing transactions initiated by several master devices to be routed to the appropriate slave devices. It enforces control logic ensuring that only one master communicates with a slave at any given time. 

In practice, this module would likely interact with:
- **AXI Master Modules**: These modules generate requests to the crossbar for data transactions. 
- **AXI Slave Modules**: These modules respond to requests, sending back data or acknowledgments.
- **Arbiter Logic**: The module contains internal arbitration logic to determine which requests from the various masters should be granted access to the slaves, based on priority and request conditions.

### Key Signals (Inputs/Outputs)

While the specific signal names and their widths are not provided in the description, in a typical AXI crossbar implementation, we can expect the following:

- **Inputs**: 
  - `axi_master_request[NM]`: Signals from each of the NM AXI masters indicating their requests to communicate with slaves.
  - `axi_master_id[NM]`: Identification signals that distinguish transactions from different masters.
  - `axi_slave_response[NS]`: Acknowledgments or responses from storage devices confirming transaction completion.

- **Outputs**: 
  - `axi_slave_address[NS]`: Addressing signals directing data to the correct slave.
  - `axi_slave_data[NS]`: Data signals carrying information to the selected slave.
  - `axi_grant[NM]`: Grant signals that indicate which master has permission to communicate with a slave at any clock cycle.
  
### Behavior of the Module

The `axixbar` module manages transaction requests through control logic and contains arbitration mechanisms. Its behavior can be summarized as follows:

1. **Request Handling**: Each clock cycle, it evaluates requests from the NM masters. It checks for contention and determines which master's request can be granted.

2. **Arbitration Logic**: The arbiter uses several conditions to grant channel access:
   - Only one master can be granted access to a slave at a time.
   - Requests must be confirmed that no other channel currently has a grant.
   - Responses must be received from the current channel before moving on to the next.

3. **Transaction Latency**: The architecture imposes a minimum latency (at least four clock cycles) from the initiation of a request until a response can be received, due to the requirement for multiple clock cycles to process requests and send data.

4. **Outstanding Transactions**: It also manages outstanding transactions, limiting the number based on configurable parameters. This prevents overflow and maintains proper operation within the defined specifications.

5. **Low Power Option**: If configured with the low-power option, the module will set unused output values to zero, which can help in debugging or simulation scenarios by keeping output signals from being randomly driven high.

In summary, `axixbar.v` acts as a complex controller for facilitating communication between multiple AXI masters and slaves while managing priorities, requests, and ensuring that the overall system maintains reliable operation amidst varying request loads.

### File: axi2axilite.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axi2axilite.v
### Purpose of the File

The file `axi2axilite.v` implements a conversion module that transforms the AXI (Advanced eXtensible Interface) protocol into the AXI-Lite protocol. This conversion is designed to achieve low-latency transactions without sacrificing performance, aiming for one clock cycle per transaction. The design is flexible, with configurable parameters that allow it to adapt to different bus widths and transaction requirements while maintaining efficiency in operation.

### Inter-Module Relationships

This AXI-to-AXI-Lite converter interacts with other components in the CPU architecture as follows:
- **With Master Modules**: It interfaces with AXI master modules, handling commands and data from the master and converting them to AXI-Lite transactions that can be processed by AXI-Lite compliant slaves.
- **With Slave Interfaces**: As the output module, it serves as an intermediary between the AXI master and AXI-Lite slaves, managing the translation of protocol communication effectively.
- **Potentially With FIFO Modules**: Given the FIFO length parameter (`LGFIFO`), it can work in conjunction with FIFO structures for buffering data transactions, which could be necessary for operation with slower slave devices.

### Key Signals

**Inputs:**
- `S_AXI_ACLK`: The clock signal for the AXI interface.
- Additional input signals typically include:
  - `S_AXI_AWADDR`, `S_AXI_AWVALID`, `S_AXI_AWREADY`: Signals related to address write transactions.
  - `S_AXI_WDATA`, `S_AXI_WSTRB`, `S_AXI_WVALID`, `S_AXI_WREADY`: Signals associated with the data write transactions.
  - `S_AXI_BVALID`, `S_AXI_BREADY`: Signals indicating the status of write responses.
  - `S_AXI_ARADDR`, `S_AXI_ARVALID`, `S_AXI_ARREADY`: Signals related to read address transactions.
  - `S_AXI_RDATA`, `S_AXI_RVALID`, `S_AXI_RREADY`: Signals associated with read data responses.

**Outputs:**
- `M_AXI_AWADDR`, `M_AXI_AWVALID`, `M_AXI_AWREADY`: Signals for the address write channel for AXI-Lite.
- `M_AXI_WDATA`, `M_AXI_WSTRB`, `M_AXI_WVALID`, `M_AXI_WREADY`: Signals for data write channels in AXI-Lite.
- `M_AXI_BVALID`, `M_AXI_BREADY`: Signals indicating the status of write responses in the AXI-Lite version.
- `M_AXI_ARADDR`, `M_AXI_ARVALID`, `M_AXI_ARREADY`: Output signals for read address transactions for AXI-Lite.
- `M_AXI_RDATA`, `M_AXI_RVALID`, `M_AXI_RREADY`: Output signals for read data responses.

### Behavior of the Module

The `axi2axilite` module operates effectively by implementing control logic that governs the transactions between its input AXI protocol and output AXI-Lite protocol. 

1. **State Machine**: It likely includes a finite state machine (FSM) that manages the various transaction states such as idle, read, write, and response handling.
2. **Transaction Management**: The converter responds to valid input signals, translating them accordingly and generating the corresponding output signals for AXI-Lite. For read transactions, it acknowledges and provides data based on the AXI-Lite requirements.
3. **FIFO Management**: The FIFO buffer management, influenced by `LGFIFO`, may facilitate temporary storage of data, ensuring that multiple outstanding transactions can be handled efficiently while maintaining synchronization with the AXI-Lite responses.
4. **Latency Handling**: Given the additional 2-clock overhead mentioned, the design implements features to accommodate increased latency for AXI transactions while retaining performance criteria.

In summary, the `axi2axilite.v` module is a pivotal part of the CPU architecture, bridging high-performance AXI transactions to the simpler and slower AXI-Lite protocol, while managing all necessary protocol transformations efficiently.

