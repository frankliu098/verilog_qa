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
The Verilog file `ffetch.v` focuses on the instruction fetch mechanism for a CPU, specifically within the Zip CPU architecture. Here’s a detailed overview based on your requirements:

### Overall Purpose
The main purpose of the `ffetch.v` file is to implement the instruction fetch logic for the Zip CPU. It is designed to handle the prefetching and fetching of instructions from memory, ensuring that the CPU interacts correctly with the memory subsystem during instruction retrieval. The module aims to guarantee that the instruction fetch behavior aligns with expected properties related to memory interfaces.

### Inter-module Relationships
`ffetch.v` interacts primarily with the following entities in the CPU architecture:
- **Pipeline Stages**: It serves as a crucial component in the instruction fetch stage of the CPU’s pipeline. The fetched instructions are used by the decode and execution stages, though they are not explicitly defined in this file.
- **Memory Subsystem**: The module communicates with other memory-related modules to fetch correct instruction data based on the provided program counter (PC).
- **Control Units**: It works in conjunction with the CPU control logic, where signals indicating new program counters or cache invalidation (clearing) affect the fetching behavior.

### Key Signals
- **Inputs**:
  - `i_clk`: The clock signal for synchronous operation.
  - `i_reset`: Reset signal to initialize the state of the fetch module.
  - `cpu_new_pc`: Signal indicating a new program counter value is available.
  - `cpu_clear_cache`: Signal indicating that the instruction cache should be invalidated.
  - `cpu_pc`: The current program counter being used by the CPU.
  - `pf_valid`: Indicates if the fetched instruction is valid.
  - `cpu_ready`: Signal indicating the CPU is ready for the next fetch.
  - `pf_pc`: The program counter from which the instruction is fetched.
  - `pf_insn`: The instruction fetched from memory.
  - `pf_illegal`: Indicates if the fetched instruction is illegal.
  
- **Outputs**:
  - `fc_pc`: The output program counter after the fetch logic processes it.
  - `fc_illegal`: Indicates whether the fetched instruction was illegal.
  - `fc_insn`: The fetched instruction to be sent to the next pipeline stage.
  - `f_address`: Current address being fetched, updated based on the program counter and instruction width.

### Behavior of the Module
- **Address Tracking**: `ffetch.v` contains logic to manage the current address (`f_address`) for instruction fetching. When a new program counter signal (`cpu_new_pc`) is received, it updates the `f_address`. If an instruction is valid (`pf_valid`), it increments the address to point to the next instruction, considering the instruction's width.

- **Validity Processing**: The module ensures that instruction validity (`pf_valid`) and legality (`pf_illegal`) are correctly signaled. It tracks instructions through past states using a flag (`f_past_valid`) that helps manage historical signal checks.

- **Assertions**: The module employs assertions to verify that conditions regarding the fetched instructions and the CPU's PC align correctly. It contains logic to guarantee that, under various conditions (reset, cache clear, stalled states), the expected behavior holds.

- **Contract Checking**: The fetching module checks contracts regarding instruction alignment. For example, if `OPT_ALIGNED` is set, the module checks that the PC alignment conforms to specified alignment rules.

- **Control Logic**: The state of whether a new program counter is needed (`need_new_pc`) is explicitly managed based on resets or cache clearing conditions.

Overall, the `ffetch.v` module provides both logical and temporal management of instruction fetching in the Zip CPU, ensuring that the instruction pipeline flows smoothly with correctly validated and aligned instructions. It is pivotal for maintaining proper operation within the CPU's pipeline and interaction with memory.

### File: fdebug.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/formal/fdebug.v
### Overall Purpose of the File:
The `fdebug.v` file in the Zip CPU implementation describes the formal properties and the debugging interface of the ZipCPU core. It allows external systems to perform operations such as resetting the CPU, halting the CPU, and overriding specific registers for debugging purposes. The module ensures correct behavior when interacting with the core for debugging, interfacing with control signals, and validating assumptions about the system.

### Inter-module Relationships:
The `fdebug` module interacts with various other components in the CPU architecture, particularly those responsible for control flow and debugging:
- It communicates with the **ZipCPU core** which handles the actual execution of instructions. The `fdebug` module provides an interface to manipulate and monitor the state of the CPU during debugging sessions.
- It also works closely with any of the wrappers or system modules, like **ZipSystem** and **ZipBones**, allowing these higher-level modules to leverage its debugging capabilities, ensuring proper management of reset lines, halt conditions, and cache clearing operations.

### Key Signals (Inputs/Outputs):
#### Inputs:
1. **i_clk**: The clock signal for synchronization.
2. **i_reset**: A synchronous reset signal that initializes system states.
3. **i_cpu_reset**: A specific reset signal for the CPU, separate from the system reset.
4. **i_halt**: A request to halt CPU operations.
5. **i_halted**: Indicates whether the CPU is completely halted.
6. **i_clear_cache**: A request to clear the CPU's cache.
7. **i_dbg_we**: Indicates a write enable for the debugging interface.
8. **i_dbg_reg**: The register number (0-31) that is targeted for writing.
9. **i_dbg_data**: Data intended to be written to the specified register.
10. **i_dbg_stall**: Indicates that the CPU cannot handle the current write request.
11. **i_dbg_break**: Signals that a break condition has occurred, interrupting normal CPU operation.
12. **i_dbg_cc**: Various CPU conditions such as bus errors or sleep states.

#### Outputs:
The module does not define direct output signals; however, it asserts/detects conditions on the internal state and can influence the status of the CPU through signal checks and assumptions.

### Behavior of the Module:
The `fdebug` module employs several mechanisms to ensure the CPU's debugging interface works correctly:

1. **Control Logic**:
   - The module contains several `assert` and `assume` statements, implemented conditionally based on the target system (indicated by `ZIPCPU`).
   - It tracks the validity of previous clock states through the `f_past_valid` register, which is initially set to 0 and becomes 1 on the first clock edge.

2. **Assumption Checks**:
   - Assumptions are made about the reset states, ensuring that if either a system reset or a CPU reset is active, various conditions are upheld.
   - The module checks that writing to registers (via `i_dbg_we`) is only allowed when the CPU is halted (`i_halt` signal).

3. **Stall Conditions**:
   - If a stall condition is indicated (`i_dbg_stall`), the system assumes that writes are valid but cannot proceed until the stall condition is resolved.
   - The module ensures that if the CPU is not in the halted state, the debug stall should not be asserted.

4. **Cache Management**:
   - When the cache clear request `i_clear_cache` is asserted, conditions ensure that this can only happen when the CPU is halted, to prevent cache inconsistencies during operations.

5. **Break Conditions**:
   - If a break is signaled (`i_dbg_break`), assertions are made to ensure that the CPU must either halt or reset, facilitating appropriate error handling.

6. **Halt Management**:
   - The module checks conditions to confirm that the CPU cannot resume operations until it has been explicitly released from a halted state.
   - It monitors the transitions of the halt signal, ensuring it remains active until the CPU indicates it has halted.

In conclusion, the `fdebug.v` module provides a comprehensive interface for debugging the ZipCPU, maintaining operational integrity while allowing users to manipulate register states and observe conditions critical to debugging CPU behavior.

### File: abs_mpy.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/formal/abs_mpy.v
### Overall Purpose of the File

The `abs_mpy.v` file is a Verilog module that abstracts the multiplication operation to simplify the interface and make it easier to use with formal methods. It serves as a lightweight implementation of multiplication functionality for the Zip CPU architecture, allowing it to handle operations like `MPY`, `MPYUHI`, and `MPYSHI`. The module's design ensures that multiplication can produce results in a faster time frame (from 1 to 6 clock cycles) based on the chosen architecture configuration.

### Inter-module Relationships

The `abs_mpy` module interacts with various components within the CPU architecture, primarily connecting with:

- **Control Logic:** The module receives control signals (e.g., `i_op` and `i_stb`) indicating the type of multiplication operation requested. This is essential for the CPU's execution pipeline, where the ALU or other components would signal multiplication needs to the `abs_mpy` module.
- **Data Path:** It utilizes inputs (`i_a`, `i_b`) from other modules that provide the operands for multiplication, which might come from registers or the output of previous arithmetic operations.
- **Output Feedback:** The results (`o_result`) are sent back to other components of the CPU after processing, providing the necessary multiplication output needed for subsequent operations.

### Key Signals (Inputs/Outputs)

#### Inputs:
- `i_clk`: The clock signal, used for synchronization across the module's logic.
- `i_reset`: A reset signal to initialize the module state.
- `i_stb`: A strobe signal that indicates when a multiply operation is requested.
- `i_op`: A 2-bit input selecting the type of multiply operation (e.g., standard multiply, unsigned higher half, signed higher half).
- `i_a`, `i_b`: 32-bit operands for the multiplication operation.

#### Outputs:
- `o_valid`: A register that indicates if the output result is valid.
- `o_busy`: A signal indicating if the multiplication is currently in progress.
- `o_result`: A 64-bit output that contains the result of the multiplication operation.
- `o_hi`: A register output that returns the high half of the multiplication result when applicable.

### Behavior of the Module

The behavior of the `abs_mpy` module can be summarized as follows:

1. **Multiplication Control Logic:**
   - The module operates based on the incoming `i_stb` signal, which starts the multiplication process.
   - The type of operation is determined by the `i_op` input, which selects between different multiplication modes.

2. **State Management:**
   - The module uses a two-stage control system to manage validity and busy states. The output validity (`o_valid`) is determined based on the processing completion and the strobe input.
   - A counter-like mechanism (`delay_to_valid`) is employed to track how many clock cycles are needed before multiplication results are available, adhering to the specified architecture delays.

3. **Asynchronous and Synchronous Logic:**
   - Several always blocks respond to the clock edge (`posedge i_clk`) to manage state transitions based on the reset condition and input signals.
   - Immediate assignments (`always @(*)`) manage conditions based on inputs without relying on clock edges.

4. **Result Handling:**
   - If the multiply operation is in progress, the results are updated into the `o_result` and the high half of the result is managed with the `o_hi` output based on the operation type.
   - The `o_busy` output indicates the ongoing operation, ensuring downstream components know when multiplication is being processed.

5. **Formal Verification Assistance:**
   - The module includes assumptions for formal verification, particularly regarding the number of expected delays and the proper sequencing of operations, providing clearer paths for formal methods to verify correctness.

In summary, `abs_mpy.v` encapsulates the multiplication operation within the CPU, facilitating easier integration, management of timing and control signals, as well as providing outputs necessary for further processing in the instruction pipeline.

### File: abs_div.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/formal/abs_div.v
### Overall Purpose of the File
The `abs_div.v` file implements an abstract integer division module for the Zip CPU, which is a lightweight RISC CPU soft core. This module is capable of performing division operations, either as signed or unsigned integers. The design is abstracted to simplify interaction with formal verification tools, making it easier to validate the correctness of the unit without necessarily implementing the division logic. The comments in the file highlight that this module is primarily for testing and verification purposes, rather than for production use.

### Inter-module Relationships
The `abs_div` module interacts with various components of the Zip CPU architecture, including:
- **Control Logic**: The division unit requires external control signals (e.g., `i_wr` for starting the operation) that are typically provided by another control module within the CPU.
- **Memory Operations**: Depending on its architecture, this division module may interact with registers or memory elements to read operands (`i_numerator` and `i_denominator`) and write the result (`o_quotient`). 
- **Pipeline Stages**: As a functional unit, it likely participates in the CPU's pipeline, feeding results into subsequent stages or awaiting completion signals from the execution unit.

### Key Signals (Inputs/Outputs)
#### Inputs:
- `i_clk`: The clock signal to synchronize operations.
- `i_reset`: An asynchronous reset signal to initialize the module.
- `i_wr`: A signal indicating that a write (or a division request) is happening.
- `i_signed`: A flag that determines whether the operation is a signed division.
- `i_numerator` and `i_denominator`: The operands for the division operation.

#### Outputs:
- `o_busy`: A status signal indicating whether the division operation is currently in progress.
- `o_valid`: A signal that indicates when a valid result is available.
- `o_err`: An error signal indicating if an error occurred during the division operation.
- `o_quotient`: The resulting quotient from the division operation.
- `o_flags`: A flag output that provides additional status, such as indicative of a zero result or sign of the quotient.

### Behavior of the Module (Control Logic and State Machines)
The behavior of the `abs_div` module is primarily dictated by state management through the `i_reset` and `i_wr` signals:

- **State Initialization**: On reset, internal state is initialized (particularly `r_busy_counter` and `o_valid`).
  
- **Busy Indicator**: The `o_busy` signal is driven high when the division operation is active. The `r_busy_counter` variable tracks the countdown until the division is completed, decrementing every clock cycle.

- **Validation Signal**: The `o_valid` output is set to high when the `r_busy_counter` reaches 1, indicating that a division has just completed, and the result is ready.

- **Division Process**: While not implemented in detail in this abstract module, the division logic is described as working via shifting and subtraction, resembling the classical algorithm for division. The design enforces the protocol that `o_valid` and `o_busy` cannot be high simultaneously, thereby ensuring that valid results are not produced until after the module has finished computation.

- **Assertions and Assumptions**: The module contains formal checks such as `assert` statements to validate internal states and behaviors against expected operation protocols. It ensures that under certain conditions, erroneous states do not occur and that output conditions meet the pre-established logic of the CPU's operational rules.

In summary, `abs_div` serves as a foundational unit within the Zip CPU for handling division operations, structured to facilitate both operational functionality and formal verification integrity.

### File: f_idecode.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/formal/f_idecode.v
Certainly! Here is a detailed analysis of the Verilog file `f_idecode.v`:

### Overall Purpose
The `f_idecode.v` file implements a simplified instruction decoder for the Zip CPU architecture. Its primary role is to decode instructions that pass through the pipeline, allowing for verification of the instructions without requiring clock synchronization. This functionality is essential for ensuring that the instruction set and behavior are as expected during validation and testing phases.

### Inter-module Relationships
The `f_idecode` module interacts with several other components in the CPU architecture, particularly during the decoding stage of instruction processing. It is designed to mirror the functionality of the `idecode.v` file, which likely contains the actual instruction decoding with clock-based operations. Here are some key interactions:
- **Input Signals**: It accepts the raw instruction as an input, along with phase and global interrupt enable signals. This data is critical for determining how to decode and interpret the instruction.
- **Output Signals**: The outputs from `f_idecode` provide information about the decoded instruction, including which registers are involved (destination, source) and any control signals that dictate the operation of the subsequent pipeline stages (e.g., whether to write back results, the condition for executing the instruction).
- **Other Modules**: The output signals can be used by execution and control components of the CPU, ensuring they have all necessary information regarding each instruction that is decoded. It interacts with the execution stages where the actual processing of these decoded operations occurs (by indicating whether operations like load/store, ALU operations, or special operations (like simulation instructions) should proceed).

### Key Signals (Inputs/Outputs)
**Inputs:**
- `i_instruction`: 32-bit instruction input that contains the opcode and operand information.
- `i_phase`: Indicates the current phase of instruction processing.
- `i_gie`: Global Interrupt Enable signal affecting the behavior of the instruction.

**Outputs:**
- `o_illegal`: A flag indicating whether the instruction is illegal or not.
- `o_dcdR`, `o_dcdA`, `o_dcdB`: Indicate the destination and source registers based on the decoded instruction.
- `o_I`: The immediate value extracted from the instruction.
- `o_cond`: Condition flags for when the instruction should execute.
- Other control signals (`o_wF`, `o_op`, and operational flags like `o_ALU`, `o_M`, etc.) indicate how the instructions affect the processor state and which operations should be taken.

### Behavior of the Module
The behavior of the `f_idecode` module is governed primarily by combinational logic, as it performs instruction decoding without clocking. Its main features include:

1. **Instruction Decoding**: The module first applies logic to set `iword`, a modified version of `i_instruction`, based on whether compressed instruction sets (CIS) are used.

2. **Operation Classification**: It identifies various types of operations (e.g., memory operations, ALU operations, special functions like break) through generated flags (`w_mov`, `w_ldi`, `w_brev`, etc.). 

3. **Register Decoding**: The destination registers and source operands are determined based on the decoded instruction. This includes computing fields for `w_dcdR`, `w_dcdA`, and `w_dcdB`.

4. **Control Signal Generation**: Several control signals determine whether the operation modifies the flags (`o_wF`), writes back results (`o_wR`), or requires using specific registers (`o_rA`, `o_rB`).

5. **Illegal Instruction Detection**: The module continuously checks for illegal instructions based on unsupported operations or register conditions, asserting `o_illegal` accordingly.

6. **Immediate Value Extraction**: The immediate value is extracted and formatted based on the instruction type, with different branches for regular vs. compressed immediate extraction.

This parallel logic allows the CPU to efficiently determine the necessary actions for each instruction in a pipelined manner, ensuring that the overall processing flow remains uninterrupted.

### File: fmem.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/formal/fmem.v
### Purposes of `fmem.v`:

The `fmem.v` file is designed for formal verification of the interface between the CPU (specifically the Zip CPU) and the memory unit. The purpose is to ensure that memory operations (both read and write) performed by the CPU adhere to defined protocols for synchronizing with memory, including assumptions and assertions about operational states, error handling, and the legality of memory requests. It outlines the behavior expected from a compliant memory unit that will interact with the CPU without errors.

### Inter-Module Relationships:

- **CPU Interaction**: The `fmem` module acts as a bridge between the CPU and the memory unit, handling requests made by the CPU through signals like `i_stb`, `i_op`, `i_addr`, etc. 
- **Memory Unit Compatibility**: The module checks that any memory unit designed to interface with the Zip CPU conforms to specific criteria, indicating that it must handle operations like reading or writing data appropriately, managing requests, and signaling completion or error states.
- **Formal Verification Framework**: The module is structured within a formal verification framework, making use of assumptions (`assume`) and assertions (`assert`) to validate the interactions and guarantee the correctness of operations being performed.

### Key Signals (Inputs/Outputs):

#### Inputs:
- `i_clk`: The clock signal for synchronous operation.
- `i_sys_reset`: A signal for the global reset that resets the entire bus.
- `i_cpu_reset`: Indicates if the CPU is reset.
- `i_stb`: Strobe signal indicating that the CPU makes a request to the memory.
- `i_pipe_stalled`: Indicates if the memory unit cannot accept requests from the CPU.
- `i_clear_cache`: Request from the CPU to clear any cached memory.
- `i_lock`: Request to initiate a locked sequence.
- `i_op[2:0]`: Operation type (read, write, etc.).
- `i_addr[31:0]`: Address for read/write operations.
- `i_data[31:0]`: Data to be written during a store operation.
- `i_oreg[4:0]`: Register for writing the return data back to.
- `i_busy`: Indicates if the memory unit is busy.
- `i_rdbusy`: Indicates if the memory unit is busy doing a read.
- `i_valid`: Indicates if a read has completed and data is available.
- `i_done`: Signals that a read or write operation has finished.
- `i_err`: Status for a bus error during operation.
- `i_wreg[4:0]`: Register to write the result of a read operation.
- `i_result[31:0]`: Result of the last read operation.

#### Outputs:
- `f_outstanding[F_LGDEPTH-1:0]`: Count of outstanding requests to memory.
- `f_pc`: Indicates if the last operation will write to PC or flags register.
- `f_gie`: Indicates if registers being read are user mode registers.
- `f_read_cycle`: Indicates whether the current operation is a read.
- `f_axi_write_cycle`: Indicates if in an AXI exclusive access write cycle.
- `f_last_reg[4:0]`: Last register read which data is returned to.
- `f_addr_reg[4:0]`: The base address register being used.

### Behavior of the Module:

1. **Reset Logic**: Handles initialization and resetting of internal states upon CPU or system reset. It ensures proper assumptions during the reset state (e.g., no valid operations or errors).
  
2. **Outstanding Requests Management**: It tracks the number of outstanding requests using a counter (`f_outstanding`). This counter increments with each strobe (`i_stb`) and decrements upon a done signal (`i_done`), ensuring it does not exceed a defined maximum depth (`OPT_MAXDEPTH`).

3. **Error Handling and Validity Checks**: It checks for conditions such as `i_err` indicating bus errors and ensures appropriate handling around memory requests in terms of validity (`i_valid`).

4. **Pipeline and Lock Management**: The module verifies that requests are not issued when the memory is busy, inhibiting new requests if the memory unit's state indicates it is processing earlier requests. It also handles lock sequences that may span multiple operations.

5. **Assertions and Assumptions**: Leveraging assertions and assumptions allows the module to formally verify that the CPU adheres to expected behaviors while interacting with memory, ensuring the operational protocols designed for memory transactions are maintained.

6. **State Tracking**: The module maintains individual states such as whether an operation is a read or write cycle and tracks the last accessed registers, managing how operations can proceed based on the current pipeline logic. 

Overall, the `fmem` module plays a crucial role in ensuring the Zip CPU's memory operations are properly synchronized, validated, and error-free through the formal verification approach.

### File: zipbones.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/mcy/zipcpu/zipbones.v
### Purpose of the File

The `zipbones.v` file implements the Zip CPU, a small, lightweight RISC CPU soft core designed to provide basic CPU functionality with minimal resource utilization. This implementation does not include any peripheral components directly but is structured to allow peripheral integration separately. The design aims to provide a basic instruction set and CPU control to facilitate performance in embedded systems and educational applications.

### Inter-module Relationships

The `zipbones.v` module interfaces with various components of the CPU architecture, including:

- **Wishbone Interface**: 
  - The module connects to a Wishbone master bus for communication with memory and other components. It handles signals like `o_wb_cyc`, `o_wb_stb`, `o_wb_we`, `o_wb_addr`, `o_wb_data`, and `o_wb_sel` for reading from and writing to the memory.
  - It also receives acknowledgment and data from the Wishbone slave through signals like `i_wb_stall`, `i_wb_ack`, `i_wb_data`, and `i_wb_err`.

- **Interrupt Handling**: 
  - The module takes external interrupts as input (`i_ext_int`) and generates an output interrupt (`o_ext_int`) for external handlers, coordinating how and when the CPU halts.

- **Debug Interface**:
  - The debug signals (`i_dbg_cyc`, `i_dbg_stb`, `i_dbg_we`, etc.) allow for debugging the CPU by enabling read/write access to internal registers through a distinct Wishbone slave interface.

- **ZIP CPU Core**:
  - The core of the CPU is instantiated as `zipcpu`, taking various input controls (like reset and halt) and outputting control signals for memory interfaces.

Overall, `zipbones.v` serves as a conduit between the CPU's core functionalities and its external interfaces, ensuring communication with memory and other peripherals while offering debugging capabilities.

### Key Signals

#### Inputs:
- `i_clk`: Clock signal for synchronous operations.
- `i_reset`: Active signal for resetting the CPU.
- `i_ext_int`: External interrupt signal.
- `i_dbg_cyc`, `i_dbg_stb`, `i_dbg_we`, `i_dbg_addr`, `i_dbg_data`: Signals for the debug community interface.
- `mutsel`: Bus signal used for addressing specific memory functions.

#### Outputs:
- `o_wb_cyc`, `o_wb_stb`, `o_wb_we`, `o_wb_addr`, `o_wb_data`, `o_wb_sel`: Master signals to communicate with a Wishbone slave.
- `o_ext_int`: Output for external interrupt handlers.
- `o_dbg_stall`, `o_dbg_ack`, `o_dbg_data`: Signals for the debug interface.
- `o_cpu_debug`: Provides additional debugging information if debugging scope is defined.

### Behavior of the Module

The behavior of the `zipbones.v` module is governed by control logic that primarily handles processor state management, instruction execution flow, and debugging access. Key aspects include:

- **Control Logic**:
  - A series of registers and state variables manage CPU commands such as reset, halt, and cache clearance based on debug commands received, effectively controlling operational states within the CPU.
  - For example, the command for resetting the CPU sets `cmd_reset` as active when a write command is detected on the debug bus and the corresponding reset bit is set.

- **Instruction and Data Handling**:
  - The CPU handles various data pathways for read/write operations. It uses the Wishbone protocol to communicate with memory, switching on and off the correct signals based on the current operation.
  - The core CPU functionality (`zipcpu`) receives signals to manage its internal state, including read/write transactions, and sends back debug data as needed.

- **Interrupt Management**:
  - External interrupts are processed to control the CPU's response to hardware events. If a halt command is received or if the CPU is stalled, then the external interrupt line can signal the presence of high-priority events, feeding back into the core operations.

Overall, the `zipbones.v` module is essential for integrating the CPU's core logic with external communication and control mechanisms, ensuring that it can execute instructions efficiently and respond to external conditions.

### File: zipmmu_tb.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/rtl/zipmmu_tb.v
### Overall Purpose of the File

The `zipmmu_tb.v` file serves as a test-bench for the Memory Management Unit (MMU) of the Zip CPU architecture. Its primary purpose is to validate the functionality and correctness of the MMU independent of the CPU itself. The test-bench is structured to interact with the MMU in accordance with Verilog simulation systems, specifically targeted to be compatible with C++ Verilator-enabled test environments.

### Inter-module Relationships

The `zipmmu_tb` module interacts with various components within the Zip CPU architecture:

1. **Module Under Test (mut)**: The `zipmmu` module, parameterized by an address width and other configuration settings, is the central module being tested. This module handles the internal workings of the MMU.

2. **Memory Model (memdev)**: The test-bench includes a memory model instantiated as `memdev`, which simulates memory operations. It responds to memory cycles (`mem_cyc`), enabling the MMU to read and write data to the simulated RAM based on address and control signals.

3. **Control Bus and Memory Bus**: The module has defined interactions with a control bus (represented by signals such as `i_ctrl_cyc_stb`, `i_wb_we`, etc.) and a memory bus (with signals like `i_wbm_cyc`, `i_wbm_stb`, and `mem_addr`) to handle memory requests, data transfer, and acknowledgments.

### Key Signals (Inputs/Outputs)

**Inputs:**
- `i_clk`: The clock signal for synchronous operation.
- `i_reset`: A reset signal to initialize or clear the module states.
- Control signals such as `i_ctrl_cyc_stb` for control cycles, and data signals like `i_wb_addr`, `i_wb_data` representing addresses and data being written.

**Outputs:**
- `o_rtn_stall`: Indicates a stall in the return path.
- `o_rtn_ack`: Acknowledge signal for received data.
- `o_rtn_data`: Data returned after a memory operation.
- Various internal signals related to TLB (Translation Lookaside Buffer) operations, context management, and memory access status.

### Behavior of the Module

The `zipmmu_tb` module exhibits the following behaviors:

1. **Clock and Reset Handling**: On the rising edge of the clock, if the module is in a reset state, it initializes the error signal `mem_err`. If there is no cycle activity (`mem_cyc`), it also clears the error state.

2. **Control Logic**:
   - It monitors the incoming control cycle signals to determine whether memory accesses should proceed.
   - The MMU reacts to control signals to manage memory requests and translate addresses via TLB, which engages different outputs based on whether the operation is a read or write.

3. **Response Handling**:
   - The output signals (`o_rtn_stall`, `o_rtn_ack`, and `o_rtn_data`) are dynamically assigned based on whether the access is directed towards a control bus or the memory bus.
   - If the MMU experiences an error or a stall condition, it appropriately sets the respective output signals.

4. **TLB Management**: The module incorporates logic for managing TLB entry validity and hits/misses. Through signals like `tlb_valid`, `s_tlb_hit`, and `s_tlb_miss`, it checks whether the requested address hits the TLB or requires fallback to a page table access.

5. **Simulation Compliance**: The module contains dedicated segments to comply with Verilator by managing unused signals, ensuring that the test-bench remains clean and compliant with linting requirements.

Overall, the `zipmmu_tb` module is an essential component for validating the MMU's functionality and ensuring that it operates as intended within the Zip CPU architecture, providing a structured environment for testing memory address translations and accesses.

### File: memdev.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/bench/rtl/memdev.v
Certainly! Here’s a detailed analysis of the Verilog file `memdev.v`.

### Overall Purpose
The `memdev.v` file implements a simple on-chip memory module that interfaces with the Wishbone bus protocol. The purpose of this memory module is to provide accessible memory to the system, allowing read and write operations to occur in line with CPU instructions. This memory supports pipelined access, theoretically allowing subsequent transactions to occur in a single cycle, depending on the system's configuration.

### Inter-module Relationships
The `memdev` module interacts with various components in the CPU architecture, particularly other modules that utilize the Wishbone bus for communication, including the following:
- **Zip CPU or Master Modules**: As a slave device, it responds to memory requests made by the CPU or other devices on the Wishbone bus, enabling data read/write operations.
- **fwb_slave Module**: The file contains references for formal verification, particularly through the instantiation of the `fwb_slave` module to check memory accessibility and transaction integrity.

This design indicates a well-structured relationship where the `memdev` acts as a memory repository, while the CPU and other components handle the instruction flow and control logic for accessing this memory.

### Key Signals
- **Inputs**:
  - `i_clk`: Clock input for synchronizing operations.
  - `i_reset`: Reset signal to initialize the module state.
  - `i_wb_cyc`: Indicates that a Wishbone cycle is in progress.
  - `i_wb_stb`: Strobe signal indicating that a valid transaction is taking place.
  - `i_wb_we`: Write enable signal to determine if the operation is a read or a write.
  - `i_wb_addr`: Address bus to access specific memory locations.
  - `i_wb_data`: Data bus for inputting data during write operations.
  - `i_wb_sel`: Select lines to determine which byte(s) are being written.

- **Outputs**:
  - `o_wb_stall`: Indicates if the bus transaction is stalled.
  - `o_wb_ack`: Acknowledge signal to indicate that the operation has been completed.
  - `o_wb_data`: Data bus for reading data during read operations.

### Behavior of the Module
The behavior of the `memdev` module can be summarized as follows:

1. **Memory Pre-loading**: If a hex file is specified, it utilizes the `$readmemh` command to preload memory with contents from that file at simulation start.

2. **Delay Management**: If `EXTRACLOCK` is enabled, it adds an extra clock cycle delay to the read/write operations. This allows signals to be stabilized before they are processed further. If `EXTRACLOCK` is not used, operations occur in a single cycle.

3. **Read/Write Operations**:
   - For reading, on the clock's rising edge, the module reads data from the memory at the specified address and outputs it via `o_wb_data`.
   - For writing, if the corresponding write strobe (`w_wstb`) is asserted, the module updates the memory at the specified address with the provided data based on the byte select lines.

4. **Acknowledgment Logic**: The module tracks whether a transaction has occurred and asserts or de-asserts the acknowledge signal (`o_wb_ack`) based on transaction status, thereby informing the bus master of the operation's status.

5. **Stalling Logic**: The output signal `o_wb_stall` is statically assigned to `0`, indicating that this memory module is assumed to always be ready for transactions without delays.

6. **Formal Verification**: Contains formal properties for checking the correctness of interactions, ensuring that read and write operations comply with expected behaviors and constraints.

Overall, the `memdev.v` file provides a critical function within the CPU architecture, facilitating memory transactions and enhancing the CPU's operational capabilities while being structured for verification to ensure reliable performance.

### File: zipaxil.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipaxil.v
### Overview of the `zipaxil.v` File

**Purpose:**
The `zipaxil.v` file is designed to serve as a potential top-level module for the Zip CPU architecture, which implements an AXI-lite interface for instruction, data, and debugging. It aims to facilitate simplicity in design by supporting a minimal set of features typical of a RISC (Reduced Instruction Set Computing) CPU, operating independently of specific bus widths (except for a fixed 32-bit debug bus). The instruction and data buses must be at least 32 bits wide, and various configuration parameters allow for flexibility in features such as caches, parallel processing, and debug capabilities.

### Inter-module Relationships:
- **Zip CPU Core Interaction**: The `zipaxil` module interfaces directly with a core CPU module (`zipcore`) that handles the execution of instructions. It connects to various interfaces for instruction fetching, data memory access, and debug operations.
- **AXI-lite Interface**: The file provides AXI-lite protocol support, enabling communication with external bus masters (such as memory controllers) through defined AXI signals for read and write operations.
- **Debug Interface**: It interacts with a debugging module (`fdebug`) to enable monitoring, stepping, and halting capabilities while the CPU executes programs.

### Key Signals:
- **Inputs:**
  - `S_AXI_ACLK`: System clock input for synchronization.
  - `S_AXI_ARESETN`: Active-low reset signal for the system.
  - `i_interrupt`: External interrupt signal to the CPU.
  - `i_cpu_reset`: Software reset signal for internal control.
  
  - Debug Interface Inputs:
    - Various debug control inputs for registers, write signals, etc.

- **Outputs:**
  - `M_INSN_*`: Signals for the instruction fetch interface, including address, data, valid status, etc.
  - `M_DATA_*`: Signals for the data interface, similar to instruction signals, allowing memory operations to occur.
  - `o_cmd_reset`, `o_halted`, `o_gie`: Control signals related to CPU state management (such as reset, halt commands, and global interrupt enable).
  - `o_prof_stb`, `o_prof_addr`, and `o_prof_ticks`: Outputs used for profiling the CPU performance during execution.

### Behavior:
- **Control Flow**: The module employs several control signals to manage the CPU state, including handling reset conditions and halting based on debug commands. It maintains various states dictated by the commands received via the AXI-lite debug interface.
  
- **Debug Handling**: The debug interface controls are implemented via state machines that process write and read requests, providing responses and managing the internal states for debugging tools.
  
- **Instruction Fetching Logic**: The instruction fetch logic is integrated with a dedicated module (`axilfetch`) to manage instruction prefetching and verification. Signals indicate valid instruction requests and coordinate with the instruction memory.
  
- **Memory Access**: The module also incorporates a memory access control section that manages data reads/writes through either pipelined memory operations (`axilpipe`) or straightforward memory access (`axilops`). The choice between these is determined by configuration parameters that adapt the module's performance characteristics depending on cache configuration and power constraints.

### Summary:
The `zipaxil.v` file orchestrates the communication between the Zip CPU core and external interfaces, ensuring smooth operation across instruction execution, memory access, and debugging while maintaining a modular and extensible design. Its combination of AXI-lite support, debug capabilities, and interaction with specialized fetching and memory handling modules allows it to play a crucial role in the CPU architecture aimed at efficient processing and simplified control.

### File: zipsystem.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipsystem.v
### Description of `zipsystem.v`

#### Overall Purpose
The `zipsystem.v` file implements the Zip CPU's system architecture, integrating several soft peripherals alongside the core CPU design. It is responsible for handling various functionalities such as interrupt generation, timers, and a Direct Memory Access (DMA) controller. The module is designed to operate primarily on the data bus, facilitating communication and operation between the CPU and peripherals, without direct external hardware.

#### Inter-module Relationships
- **CPU Core**: The `zipsystem` module interfaces directly with the CPU core through a Wishbone bus, allowing it to send and receive control commands, data, and configuration information.
- **Peripherals**: Various peripherals such as interrupt controllers, timers, and DMA controllers are instantiated within this module, enabling the CPU to access and manage these components seamlessly. It connects and routes signals between the CPU and these peripherals.
- **Memory Management Unit (MMU)**: It sits between the CPU's Wishbone interface and external bus, providing necessary address translation and management.
- **Bus Interfaces**: It also manages access and control signals for different buses, ensuring clean communication paths for operations.

#### Key Signals
- **Inputs**:
  - `i_clk`: Clock signal for timing the operations of the system.
  - `i_reset`: Reset signal to initialize the module.
  - `i_ext_int`: External interrupt signals from external sources.
  - Various Wishbone bus signals such as `i_dbg_cyc`, `i_dbg_stb`, `i_dbg_we`, etc., for debugging and peripheral control.
  
- **Outputs**:
  - `o_ext_int`: The single outgoing interrupt to the CPU.
  - Wishbone bus signals as outputs for communication with the CPU `o_wb_cyc`, `o_wb_stb`, `o_wb_we`, `o_wb_addr`, `o_wb_data`, `o_wb_sel`, and various peripheral outputs for timers, DMA, etc.
  - `o_prof_stb`, `o_prof_addr`, `o_prof_ticks` used for drive profiling signals.

#### Behavior of the Module
- **Control Logic**: The module contains complex control logic to manage interfacing with the CPU and different peripherals. For example, it decodes incoming addresses to select appropriate peripherals when bus transactions occur. Control signals determine which peripheral is engaged in a transaction based on the received addresses on the bus.
  
- **Interrupt Handling**: The module generates a main interrupt vector from various internal and external interrupt sources, coordinating responses based on priority and configuration. The interrupt signals are processed and forwarded to the CPU as needed.

- **Timers and Counters**: The design incorporates interval timers and watchdog timers, where timer modules count down from specified values, generating interrupts under certain conditions (like reaching zero). Performance counters track CPU activity and operational statistics.

- **Direct Memory Access (DMA)** handling provides a way for memory operations to occur without CPU intervention, which can enhance performance for bulk memory tasks.

- **State Management**: The module has several instantiated state machines for controlling the timers, DMA operations, and bus status management to ensure that all components function coherently and that resources are efficiently utilized. Temporary registers and stateful design patterns allow the tracking of commands and configuration for peripherals during CPU operation.

Overall, `zipsystem` acts as a central hub that interconnects the core CPU functionality with peripheral devices while implementing necessary control mechanisms to facilitate smooth operations in the CPU architecture.

### File: zipbones.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipbones.v
### Description of `zipbones.v`

#### Overall Purpose of the File
The `zipbones.v` file implements the core functionality of the Zip CPU, a lightweight RISC CPU soft core designed for resource-constrained environments. Its aim is to provide processing capabilities without including any peripherals; it serves as the central processing unit of a system where peripherals must be implemented in separate modules. 

#### Inter-module Relationships
The `zipbones` module interacts primarily with the following components:
- **Wishbone Bus Interface**: It communicates with external memory and devices via the Wishbone bus. Signals for address, data, control, and bus status (e.g. `o_wb_stb`, `i_wb_stall`, `o_wb_cyc`) are exchanged with the Wishbone infrastructure for reading and writing data.
- **Debug Module**: There are provisions for a debug bus that enables the inspection and control of the CPU via the signals `i_dbg_*` and `o_dbg_*`. This includes reading and writing internal registers, controlling CPU execution flow, and handling breakpoints.
- **Internal CPU Modules (e.g. ZipWB)**: The CPU's operational functionality, such as instruction execution, branching, and cache operations, is encapsulated in other modules like the `zipwb` (Wishbone-based processing core), which it instantiates within its architecture.
- **Interrupt Handling**: The module interacts with external interrupts through the `i_ext_int` and generates an outgoing interrupt signal `o_ext_int`, impacting control flow and state management.

#### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_clk`: Clock signal for synchronization.
  - `i_reset`: Resets the CPU state to initial conditions.
  - `i_ext_int`: Incoming external interrupt signal.
  - `i_dbg_*`: Signals pertaining to debug operations (e.g., debug cycle, debug write).
  
- **Outputs**:
  - `o_wb_*`: Signals related to the Wishbone bus interface (e.g., `o_wb_cyc`, `o_wb_stb`, `o_wb_addr`, `o_wb_data`).
  - `o_ext_int`: Outgoing interrupt signal.
  - `o_dbg_*`: Signals associated with the debug interface (e.g., acknowledgment and data).
  - Control signals for CPU functional modules, showing the state and behavior of the CPU.

#### Behavior of the Module
The `zipbones` module incorporates various behaviors and control logic:
- **State Management**: It includes logic to handle CPU reset, halt, and step commands, which dictate when the CPU should proceed with processing instructions versus stopping for debugger interaction. Key variables like `cmd_reset`, `cmd_halt`, and `cmd_step` are maintained as registers and are updated based on CPU and debugging inputs.
- **Processing Control**: The CPU processes instructions based on the control signals generated from the debug interface and its internal state. This involves handling interrupts and managing normal operations on how instructions are fetched and executed.
- **Debug Functionality**: The debug logic tracks commands that allow external access to internal states, replacing registers, and can control the CPU via specific bits. The debug interface is monitored to ensure consistency and correct operation.
- **Error Handling**: Signals for errors (e.g., `i_wb_err`) and stall conditions (`i_wb_stall`) allow the module to appropriately react to bus conditions and maintain proper coordination with external memory.

The `zipbones` module exemplifies a structured approach to designing a CPU core capable of handling both normal operations and debugging scenarios, effectively managing resources without including peripheral architectures within the module itself.

### File: zipaxi.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipaxi.v
### Overview of the `zipaxi.v` File

#### Purpose
The `zipaxi.v` file serves as the top-level module for the Zip CPU, integrating the core functionality of the CPU with AXI4 (Advanced eXtensible Interface) for instruction and data interfacing, as well as an AXI-lite debug interface. This design is tailored to be lightweight and simple while supporting a RISC-like instruction set, making it suitable for various implementations including embedded systems.

#### Inter-module Relationships
The `zipaxi` module interacts with several other modules in the CPU architecture:

1. **Zip Core (`zipcore`)**: The primary processing unit of the CPU, `zipcore` is instantiated within `zipaxi` and is controlled via signals for resetting, halting, and memory operations.
2. **Fetching Modules**: Various modules are responsible for instruction fetching, such as `axiicache` and `axilfetch`, which handle retrieving instructions based on the AXI interface. The core of instruction fetching is accomplished through the integration of these cache modules, allowing for efficient memory access.
3. **Memory Units**: The module interfaces with data handling blocks such as `axidcache`, `axipipe`, and `axiops` to support memory read and write operations over the AXI bus.
4. **Debug Module**: An optional debugging interface is also present, allowing external control signals for halt and reset, communicating with the debug registers via `fdebug`.

#### Key Signals (Inputs/Outputs)

**Inputs:**
- `S_AXI_ACLK`, `S_AXI_ARESETN`: Clock and reset signals for the AXI interface.
- `i_interrupt`, `i_cpu_reset`: External interrupt and CPU reset signals to control the state of the CPU.
- Various debug inputs that control debugging behavior through the AXI-lite interface.

**Outputs:**
- Instruction fetch outputs: Signals for instruction fetching modules like `M_INSN_*` that indicate the status of instruction accesses.
- Data bus outputs: Signals like `M_DATA_*` for read/write operations on the data bus.
- Control signals for the CPU state, including `o_cmd_reset`, `o_halted`, indicating if the CPU is running or halted, and other performance metrics.

#### Behavior of the Module
The `zipaxi` module operates through several key behaviors and control logics:

1. **State Control Logic**: Implements basic control for halting and resetting the CPU. It handles commands such as halt or step requests based on the debug interface inputs. The module features conditions for resetting or halting the CPU depending on the state of the debug signals.

2. **Instruction and Data Fetching**: The module includes a fetch mechanism that relies on several configurable parameters to manage how instructions are prefetched from memory. The fetching logic depends on configurations such as cache sizes and whether the CPU is operating in a pipelined mode.

3. **Debug Interface Management**: It manages the signals pertaining to the debug interface, determining how data is read from and written to debug registers. This management includes setting up acknowledgments and handling valid conditions for debug read/write operations.

4. **AXI Bus Interaction**: The behavior of the AXI bus signals is managed to ensure proper read and write transactions, including handling valid and ready signals coming from or going to the AXI interface.

5. **Memory Access Requests**: It ensures adherence to memory access protocols, coordinating reads and writes between AXI4 and internal signals that interface with cache and memory modules.

In summary, `zipaxi.v` encapsulates the core functions of the Zip CPU while managing its interactions with memory and debug utilities, all organized to ensure streamlined performance and access patterns across a wide range of applications. This architecture enables usability in varied contexts while remaining simple and efficient.

### File: zipdma_s2mm.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma_s2mm.v
### Overall Purpose of the File
The `zipdma_s2mm.v` file implements the "Stream to Memory-Mapped" (S2MM) functionality of the ZipDMA (Direct Memory Access) controller within the Zip CPU architecture. Its primary role is to manage the writing of data from a streaming source back to a memory bus. The module facilitates data transfer in various widths (1, 2, or 4 bytes at a time, or full bus width) and ensures proper address alignment when necessary.

### Inter-module Relationships
In the context of the CPU architecture, `zipdma_s2mm.v` interacts with several components:
- **Input Stream Interface**: The module receives data through input signals that represent a streaming source (e.g., data, valid signals).
- **Outgoing Wishbone Interface**: The module communicates with the Wishbone bus for memory operations, detailing read/write cycles, acknowledgments, and address information.
- **Other DMA Components**: It may cooperate with other DMA modules (like S2MM or MM2S) in a larger DMA system, managing data flows from various sources to memory.
- **Control Logic**: The control logic ensures that the state of operations (busy, error conditions) is tracked and communicated to other parts of the architecture.

### Key Signals
#### Inputs:
- `i_clk` and `i_reset`: Clock and reset signals for synchronous operation.
- `i_request`: Indicates a request for starting a write operation.
- `i_inc`: Indicates whether the address should increment after each operation.
- `i_size`: Specifies the size of data being transferred (byte, 16-bit, 32-bit, or full bus width).
- `i_addr`: The starting memory address for the write operations.

#### Outputs:
- `o_busy`: Indicates the module is currently processing a request.
- `o_err`: Indicates an error has occurred during operation.
-  `o_wr_cyc`, `o_wr_stb`: Control signals for Wishbone bus asserting a write cycle and a write strobe.
- `o_wr_addr`: Contains the address where data will be written to memory.
- `o_wr_data`: The actual data to be written.
- `o_wr_sel`: Byte enable signals that indicate which bytes in the data bus are being written.

### Behavior of the Module
The behavior of the `zipdma_s2mm` module can be summarized in the following key points:

1. **Data Transfer Management**: The module manages data flowing into memory from a streaming source. It adequately handles alignment requirements based on the specified data width and increment settings.

2. **State Tracking**:
   - The module has logic to track if a request is in progress (`o_busy`) and checks for errors (`o_err`).
   - The module uses stateful behavior to manage whether it is currently receiving data and whether the address has overflowed.

3. **Control Logic & Address Management**:
   - When a write request is initiated, it records the incoming data, prepares the next address based on the increment and size, and adjusts the write address and data accordingly.
   - It checks for address alignment issues and ensures data integrity during transfers. If data is being sent in multiple bytes, it correctly constructs the next address, maintaining required byte boundaries.

4. **Data and Select Signal Preparation**: 
   - The module prepares the data to write (`o_wr_data`) along with select signals (`o_wr_sel`) based on the incoming stream data and its corresponding size.
   - It properly formats and aligns the data for transfer based on whether the output is in little or big-endian format.

5. **Pipeline Control**: The module contains a pipeline control mechanism to manage ongoing transmissions. It tracks outstanding write requests to ensure the memory bus is not over-subscribed.

6. **Formal Verification**: The module has formal properties defined that ensure consistency and correctness of operations, using assertions to validate behavior in various scenarios.

In essence, `zipdma_s2mm` acts as a critical bridge between stream-based data flows and memory-mapped architecture, ensuring that data is written correctly and efficiently while managing the technical constraints of the bus and data width.

### File: zipdma_rxgears.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma_rxgears.v
### Overall Purpose of the File
The `zipdma_rxgears.v` file implements part of the Zip DMA (Direct Memory Access) architecture for the Zip CPU. Its main function is to handle the packing of incoming data streams before they are written to a FIFO (first-in, first-out) data structure. This packing is a crucial step in the alignment process, ensuring that data is structured correctly for further processing. As data is received, it is organized and formatted based on the specified endianness before being forwarded to the FIFO.

### Inter-module Relationships
The `zipdma_rxgears` module interacts with several other components in the Zip CPU architecture:
- **FIFO Module**: It communicates with a FIFO to store the packed data for later reading or processing by other units in the CPU.
- **Input and Output Stream Interfaces**: The module connects with input and output data streams, handling incoming data validity (S_VALID) and readiness (S_READY) signals for proper synchronization, as well as translating between the format of the received data and what the FIFO expects.
- **Control Logic**: It integrates with control logic to manage data flow and ensure alignment with peripheral devices or memory accesses.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_clk`: Clock signal for synchronization.
  - `i_reset`: Reset signal to initialize the module.
  - `i_soft_reset`: A soft reset input for non-initialization resets.
  - `S_VALID`: Signal to indicate incoming data is valid.
  - `S_READY`: Signal indicating the module is ready to receive data.
  - `S_DATA`: The actual incoming data word to be processed.
  - `S_BYTES`: Indicates how many bytes of the incoming data are valid.
  - `S_LAST`: A signal marking the last data item of the incoming stream.

- **Outputs**:
  - `M_VALID`: Indicates that the output data is valid and ready to be used or read.
  - `M_READY`: Signal indicating that the next stage is ready to receive data.
  - `M_DATA`: The packed outgoing data to be sent to the FIFO.
  - `M_BYTES`: Specifies how many bytes of the output data are valid.
  - `M_LAST`: Marks the final piece of data being sent out.

### Behavior of the Module
The module implements control logic that manages the packing of received data and transitions between states based on the validity and readiness signals:

1. **Filling Logic**: It maintains a register to count bytes being filled (`fill`), which is updated according to the incoming data's validity and how many bytes are arriving. It checks if the FIFO is ready and whether the last piece of incoming data has been received (`S_LAST` signal).

2. **Output Control**: The `M_VALID` signal indicates whether the packed data is ready to be forwarded to the FIFO based on the current internal state and whether the FIFO is ready to accept more data. If the FIFO is ready and a new valid stream is detected, it updates the `M_DATA` with the packed data.

3. **Data Packing Logic**: The incoming data can be adjusted based on the endianness specified by `OPT_LITTLE_ENDIAN`. The packing considers the shift required based on how many bytes have been filled so far.

4. **Reset Handling**: The module responds to reset signals to initialize registers, ensuring that internal states are properly cleared or set when the `i_reset` or `i_soft_reset` signals are active.

5. **Formal Properties**: The module contains formal verification constructs that assert certain properties about the input and output signals, ensuring that the behaviors meet specified conditions, such as the number of bytes filled not exceeding expectations and the proper handling of incoming and outgoing stream properties.

This robust design handles edge cases (e.g., partial words, endianness) and mutual dependencies with other components to facilitate smooth data transitions within the CPU architecture.

### File: zipdma_mm2s.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma_mm2s.v
### Overall Purpose of the File

The file **zipdma_mm2s.v** implements a component of the ZipDMA (Direct Memory Access) system designed for transferring data from memory to an output stream. This module specifically handles reading values from memory and aligning them with the outgoing data format. It plays a crucial role in enabling fast data transfer without burdening the CPU with the overhead of each individual data read, thus enhancing the overall performance of the CPU system.

### Inter-Module Relationships

The **zipdma_mm2s** module interacts with several other components in the ZipCPU architecture, including:

- **Memory System**: It communicates with the memory system to request data via the wishbone protocol, indicated by the signals like `o_rd_cyc`, `o_rd_stb`, and `i_rd_ack`.
- **DMA Control Logic**: The module responds to control signals (`i_request`, `i_inc`) that manage the start and progression of a DMA transfer.
- **Outgoing Stream Interface**: It interfaces with a data stream where it outputs valid data through signals like `M_VALID`, `M_DATA`, and `M_BYTES`.
- It depends on external acknowledgments and stalling signals (`i_rd_ack`, `i_rd_stall`) which regulate the flow of data, ensuring the system does not overwhelm the receiving components or miss any data packets.

### Key Signals (Inputs/Outputs)

#### Inputs:
- `i_clk`: Clock signal used for synchronization of the module operations.
- `i_reset`: Active high signal to reset the module and clear registers.
- `i_request`: Indicates a new DMA request to initiate data reading.
- `i_inc`: Controls whether the address should increment during reads.
- `i_size`: Specifies the size of data to be transferred (byte, half-word, word).
- `i_transferlen`: Indicates the total number of bytes to be transferred.
- `i_addr`: The starting byte address from which data reading begins.
- `i_rd_stall`: High when a read operation is stalled.
- `i_rd_ack`: Acknowledgment signal from the memory system confirming receipt of a read request.
- `i_rd_data`: The data returned from the memory system for reads.
- `i_rd_err`: Indicates if there was an error during the read operation.

#### Outputs:
- `o_busy`: Indicates if the module is currently busy processing a request.
- `o_err`: Signals an error state in the DMA operation.
- `o_rd_cyc`: Activates the read cycle in the wishbone protocol.
- `o_rd_stb`: Indicates that the read operation is valid.
- `o_rd_addr`: The address from which to read data.
- `o_rd_sel`: Select lines indicating which data bytes are valid for the current transaction.
- `M_VALID`: Signals that valid data is available for the outgoing stream.
- `M_DATA`: The actual data read from memory, now output for the downstream processing.
- `M_BYTES`: Indicates the number of bytes of valid data available in the output.
- `M_LAST`: Marks the last piece of data in the outgoing transaction.

### Behavior of the Module

The module operates based on controls and states that govern DMA transfers. It includes the following behavior:

1. **State Management**: The module maintains a state machine that manages when to read data, how much data to read per cycle, and how to transition between states based on input from the CPU and memory subsystem.

2. **Read Cycle Control**: The logic checks for `i_request` and, if not currently busy (`!o_busy`), initiates a new read cycle. It sets `o_rd_cyc` and `o_rd_stb` to request a read cycle and prepares the address to read from.

3. **Error Handling**: The state machine tracks potential errors during reads (using `i_rd_err`) and updates the `o_err` signal accordingly. If an error occurs or the read completes, it resets relevant state variables.

4. **Data Processing**: While reading data, it aligns the incoming data based on the specified byte size (`i_size`) and adjusts selection lines (`o_rd_sel`) accordingly, preparing the outgoing data for the next stage in the pipeline.

5. **Output Management**: It generates signals `M_VALID`, `M_DATA`, `M_BYTES`, and `M_LAST` for the outgoing stream, crucial for downstream processing.

6. **Handling Incremental Addresses**: Depending on `i_inc`, the module can increment the address for sequential read requests, adjusting the sub-address used for data selection.

This implementation allows efficient and flexible data transfers from memory to the output stream, facilitating high-performance memory accesses, crucial in a CPU architecture aiming for efficiency.

### File: zipdma_txgears.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma_txgears.v
### Purpose of the File
The file `zipdma_txgears.v` is part of the Zip CPU project and implements the ZipDMA (Direct Memory Access) functionality. The primary role of this module is to unpack bus words received from a peripheral into smaller byte-aligned transfers, enabling communication with peripherals that require data transfers of 1, 2, or 4 bytes. This feature is crucial for interacting with devices that do not support larger bus-word transfers, ensuring compatibility and efficiency in data communication.

### Inter-Module Relationships
The `zipdma_txgears` module interacts with various components of the Zip CPU architecture, most notably:
- **Data Path**: The module receives data words (`S_DATA`) from a source (typically a memory or another peripheral) and sends them out as smaller units (`M_DATA`) to a destination.
- **Control Logic**: It works in conjunction with other DMA logic to manage the flow of data and control signals like `S_VALID`, `S_READY`, `M_VALID`, and `M_READY`.
- Other parts of the Zip CPU that deal with configuration, such as the `i_size` input for specifying the width of the transfer (1, 2, or 4 bytes), may also reference or control this module indirectly.

### Key Signals
- **Inputs**:
  - `i_clk`: The clock input for synchronous operation.
  - `i_reset` and `i_soft_reset`: Reset signals for initializing the module.
  - `i_size`: A 2-bit signal indicating the size of transfers (1, 2, or 4 bytes).
  - `S_VALID`: Indicates valid data input from the source module.
  - `S_READY`: Indicates the module is ready to receive data.
  - `S_DATA`: The incoming bus data being transferred.
  - `S_BYTES`: The number of valid bytes in `S_DATA`.
  - `S_LAST`: Signifies the last element in a sequence of data transfers.

- **Outputs**:
  - `M_VALID`: Indicates valid data output to the next stage.
  - `M_READY`: Acknowledges readiness to receive data from the upstream module.
  - `M_DATA`: The processed outgoing data ready for transfer.
  - `M_BYTES`: The count of valid bytes in `M_DATA`.
  - `M_LAST`: Indicates whether the output data is the last fragment of a multi-part transfer.

### Behavior of the Module
The `zipdma_txgears` module is designed to handle the conversion and flow control of data as follows:
- **State Management**: It maintains several registers (`sreg`, `m_valid`, `m_last`, etc.) for tracking the state of incoming and outgoing data. The states are determined by the synchronization between the `S_VALID` and `S_READY` signals, which control when data can be processed.
  
- **Data Handling**: The module utilizes a fill mechanism to determine how many bytes can still be processed (`fill`) and adjusts the input and output data according to the specified size (`i_size`). For each clock cycle with valid input, it shifts the data register (`sreg`) and reduces the `fill` count appropriately based on the transfer size.
  
- **Control Logic**: Logic conditions are implemented to manage different scenarios:
  - When incoming data becomes available and is accepted by the module, `S_DATA` is stored, and `S_BYTES` counts the number of bytes.
  - The output validity (`M_VALID`) is determined based on conditions of the fill register and the current transfer size specified by `i_size`.
  
- **Last Data Signal**: The module also manages the `M_LAST` signal and similar flags to ensure proper flow completion, indicating whether the current transfer is the last part of a sequence.

Overall, this module forms a critical component in the data path of the Zip CPU, ensuring that various peripherals can communicate effectively by accommodating different data transfer requirements.

### File: zipdma_ctrl.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma_ctrl.v
### Overall Purpose of the File
The `zipdma_ctrl.v` file implements a control module for a Direct Memory Access (DMA) system within the Zip CPU architecture. This module manages control requests through a 32-bit Wishbone bus interface, facilitating status reads and control writes. Its primary role is to handle the configuration and management of DMA operations, ensuring data transfer between the memory and peripherals efficiently without involving the CPU directly.

### Inter-module Relationships
The `zipdma_ctrl` module interacts with several other components within the Zip CPU architecture:

1. **DMA Operations**: It directly generates control signals for starting (`o_dma_request`) and aborting (`o_dma_abort`) DMA operations and receives feedback on the DMA status from the `i_dma_busy`, `i_dma_err`, and other DMA-related inputs.
2. **Memory**: It interfaces with memory components to manage source (`o_src_addr`), destination (`o_dst_addr`), and transfer length (`o_length`) parameters, coordinating transfers between peripherals and memory locations.
3. **Interrupt System**: It interacts with an interrupt system by generating an interrupt signal (`o_interrupt`) based on error conditions and DMA completion status, allowing the CPU to respond to these events.

### Key Signals (Inputs/Outputs)

#### Inputs:
- `i_clk`: Clock signal for synchronous operations.
- `i_reset`: Asynchronous reset signal.
- `i_cyc`, `i_stb`, `i_we`: Bus control signals indicating read/write operations.
- `i_addr`: Address signal for selecting control registers.
- `i_data`: Data input for the control registers.
- `i_sel`: Byte selection signal.
- `i_dma_busy`, `i_dma_err`: Signals indicating the status of the DMA transaction.
- `i_dma_int`: Signals related to DMA interrupts.
- `i_current_src`, `i_current_dst`, `i_remaining_len`: Status signals providing the current state of the DMA transfers.

#### Outputs:
- `o_stall`: Indicates a stall condition for the Wishbone bus.
- `o_ack`: Acknowledge signal for bus transactions.
- `o_data`: Output data for read operations.
- `o_dma_request`, `o_dma_abort`: Control outputs for initiating or aborting DMA operations.
- `o_src_addr`, `o_dst_addr`: Address outputs for the source and destination of DMA transfers.
- `o_length`, `o_transferlen`: Outputs defining the length of the transfer.
- `o_mm2s_inc`, `o_s2mm_inc`: Increment indications for memory-to-stream and stream-to-memory operations.
- `o_trigger`: Control signal for triggering the DMA process.
  
### Behavior of the Module
The `zipdma_ctrl` module is responsible for:

1. **Control Register Handling**: It uses a state machine to manage reading from and writing to control registers associated with DMA operations, including configurations and status.
2. **Data Handling**: On writes to the control registers, the module updates internal state variables that represent the current configuration of the DMA, including source and destination addresses, transfer length, and increment settings.
3. **State Management**: The module maintains a state regarding the ongoing DMA operation (busy, idle, error states) and responds accordingly by managing the request signals.
4. **Interrupt Generation**: It generates interrupts based on DMA completion or errors, allowing the CPU to take appropriate actions.
5. **Stall Handling**: The o_stall signal is always zero in this design, indicating that the controller does not impose any stalling requirements on the bus.

The module uses synchronous logic controlled by a clock with combinatorial logic to derive the outputs from the current inputs and internal states. It responds to bus transactions to ensure the proper configuration and status are maintained throughout the operation of the DMA controller.

### File: zipdma_fsm.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma_fsm.v
### Purpose of the File
The `zipdma_fsm.v` file implements the finite state machine (FSM) for the ZipDMA controller, which is part of the Zip CPU architecture. The primary function of this module is to manage the control logic for Direct Memory Access (DMA) transactions, enabling efficient data transfers between memory and peripherals. The FSM handles both memory-to-stream (MM2S) and stream-to-memory (S2MM) operations, breaking down large DMA transfers into manageable read and write requests.

### Inter-module Relationships
The `zipdma_fsm` module interacts with several other components in the CPU architecture, specifically:

- **zipdma_mm2s**: This controller handles the initiation and management of memory reads. The FSM issues requests to this module and waits for it to signal its readiness to proceed.
- **zipdma_s2mm**: This controller manages memory writes. Similar to the MM2S controller, the FSM communicates with this module, issuing write requests based on the current state of the DMA transfer.
- **Peripheral or Memory Component**: The `zipdma_fsm` interacts with the memory subsystem through the i_src_addr, i_dst_addr inputs and the MM2S/S2MM transfer logic, ensuring data is read from and written to the correct addresses.
  
The `zipdma_fsm` module is also usually coordinated with a top-level system controller that manages DMA requests and provides the necessary triggers and error controls.

### Key Signals (Inputs/Outputs)

#### Inputs:
- `i_clk`: The clock signal for synchronization.
- `i_reset`: A reset signal to initialize the state of the FSM.
- `i_soft_reset`: An additional reset signal for soft resets.
- `i_dma_request`: Indicates a new DMA request.
- `i_src_addr`: Source address for the DMA transfer.
- `i_dst_addr`: Destination address for the DMA transfer.
- `i_length`: Length of the data to be transferred.
- `i_transferlen`: Maximum transfer length in one operation.
- `i_trigger`: A trigger signal for initiating a read.
- `i_mm2s_busy`: Indicates whether the MM2S controller is busy.
- `i_mm2s_err`: Indicates an error from the MM2S controller.
- `i_mm2s_inc`: A signal to increment the MM2S address.
- `i_s2mm_busy`: Indicates whether the S2MM controller is busy.
- `i_s2mm_err`: Indicates an error from the S2MM controller.
- `i_s2mm_inc`: A signal to increment the S2MM address.

#### Outputs:
- `o_dma_busy`: Indicates if a DMA transfer is currently in progress.
- `o_dma_err`: This output signals if an error occurred during DMA operations.
- `o_mm2s_request`: A request signal to the MM2S controller indicating it should initiate a read.
- `o_mm2s_addr`: The current address for the MM2S controller.
- `o_mm2s_transferlen`: The number of bytes left to transfer in the MM2S operation.
- `o_s2mm_request`: A request signal to the S2MM controller for writing data.
- `o_s2mm_addr`: The current address for the S2MM controller.
- `o_s2mm_transferlen`: The number of bytes left to transfer in the S2MM operation.
- `o_remaining_len`: Remaining length of the data to be transferred.

### Behavior of the Module
The `zipdma_fsm` consists of a finite state machine that operates in the following states:

1. **S_IDLE**: The initial state where no DMA transfer is in progress. The FSM transitions to other states upon receiving a DMA request.

2. **S_WAIT**: In this state, the FSM checks if there are remaining data lengths to transfer. If a trigger is received, it transitions to the `S_READ` state.

3. **S_READ**: The FSM issues a read request to the MM2S controller. It checks if the controller is busy. If not, it updates the source address and the remaining length for the DMA transfer, transitioning to the `S_WRITE` state once the read operation is complete.

4. **S_WRITE**: After the read phase, this state is responsible for issuing a write request to the S2MM controller. It behaves similarly to the read operation, checking for busy status and transitioning back to the `S_WAIT` or `S_IDLE` states as appropriate.

Control logic handles transitions between states based on the status of the MM2S and S2MM controllers, DMA requests, and error conditions. Error signals for both MM2S and S2MM paths are also monitored to set the `o_dma_err` output accordingly.

In summary, `zipdma_fsm.v` designs a robust control mechanism for managing DMA data transfers in the Zip CPU architecture, ensuring correct sequencing and handling error conditions properly.

### File: zipdma.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/zipdma/zipdma.v
### Overview of the Verilog File `zipdma.v`

#### Purpose
The `zipdma.v` file implements the upgraded Wishbone Direct Memory Access (DMA) controller for the ZipCPU, a lightweight RISC CPU core. Its main function is to facilitate the transfer of data between memory and peripherals without CPU intervention, enhancing data throughput and freeing up CPU resources for other tasks. The module manages both read (Memory-to-Stream, MM2S) and write (Stream-to-Memory, S2MM) transfers, handling memory access requests and errors.

#### Inter-module Relationships
The `zipdma` module interacts with several other modules in the ZipCPU architecture:

1. **Control Module (`zipdma_ctrl`)**: This module is responsible for handling the control signals related to DMA requests, managing the operational state of the DMA controller, and generating appropriate addresses and lengths for data transfers.
  
2. **Finite State Machine (`zipdma_fsm`)**: This module coordinates the data transfer process, sending out requests to other modules based on the state of the DMA operation and tracking the state of the transfer (busy, error, etc.).
  
3. **MM2S and S2MM Transfer Modules (`zipdma_mm2s` and `zipdma_s2mm`)**: These modules handle the specifics of memory-to-stream and stream-to-memory transfers, respectively. They manage the data flow and interface with the Wishbone bus for data operations.
  
4. **FIFO Modules (`sfifo`)**: This module is used to buffer the data being transferred, allowing for decoupling between the speed of different modules (streaming data interfaces vs. memory interface).
  
5. **Arbiter (`wbarbiter`)**: This module controls access to the Wishbone bus for different DMA operations (MM2S and S2MM), ensuring proper arbitration between competing data requests.

#### Key Signals
- **Inputs**:
  - `i_clk`: The clock signal for the synchronous operation of the DMA controller.
  - `i_reset`: A reset signal to initialize the module’s state.
  - `i_swb_*`: Signals for the Slave Wishbone interface (requests, address, data, etc.).
  - `i_dev_ints`: Interrupt signals from other devices, used for notifying the DMA controller of relevant events.

- **Outputs**:
  - `o_swb_*`: Signals for the Slave Wishbone outputs (acknowledge, stall, data).
  - `o_mwb_*`: Signals for the Master Wishbone interface (cyclic request, address, data, etc.).
  - `o_interrupt`: Signal indicating an interrupt condition for the completion of DMA transfers.

#### Behavior
The `zipdma` module operates using a combination of request signals and state management:

1. **Control Flow**: The module begins transactions based on incoming requests over the Slave Wishbone interface. Depending on the operation type (read or write), it will initiate the corresponding transfer protocol.

2. **State Machine**: It features a state machine that manages various states of the DMA operation, handling paths through busy, error, and idle states. The `zipdma_fsm` module is utilized to track these transitions and trigger required responses.

3. **Request Handling**: When a DMA transfer is requested, the module consolidates data (source, destination, length) and issues requests to the memory interface for data movement. It continues to manage these requests, acknowledging completion or dealing with possible errors.

4. **FIFO Buffering**: The use of FIFO structures allows for smoothing out disparities in data rates between the streaming interfaces and the memory interface. The FIFO handles read and write operations independently, providing buffers during transfers.

5. **Error Handling**: In case an error occurs (e.g., memory errors), the module can set an error flag that is propagated through its output signals (e.g., `o_swb_ack`).

### Conclusion
The `zipdma.v` file represents a crucial component of the ZipCPU architecture, facilitating efficient data transfer between memory and peripherals while isolating and managing control logic through state machines and well-defined interfaces with other modules. Its overall design helps optimize CPU performance by offloading data movement tasks into dedicated hardware, emphasizing modularity and scalability in the DMA operation.

### File: cpuops.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/cpuops.v
### Description of `cpuops.v`

#### Overall Purpose
The `cpuops.v` file implements the arithmetic logic unit (ALU) functions for the Zip CPU, a lightweight RISC CPU soft core. The ALU handles various instruction opcodes (specifically, 0-13) through combinatorial logic to perform arithmetic and logical operations such as addition, subtraction, bitwise AND, OR, XOR, shifts, and multiplication. The ALU also determines flags for conditions like zero, negative, overflow, and carry, which are vital for the CPU's operation.

#### Inter-module Relationships
The `cpuops.v` module serves as a core component of the Zip CPU architecture and interacts with several other modules as follows:
- **Prefetch and Fetch Modules:** It receives instruction opcodes (`i_op`), which are fetched from memory through prefetching mechanisms handled by modules like `ffetch.v`.
- **Control Logic Modules:** Outputs such as `o_valid` and `o_busy` indicate to the control unit when the ALU results are valid or when the ALU is busy processing an operation, thereby helping manage the overall flow of operations in the CPU pipeline.
- **Multiplication Modules:** When the ALU needs to perform a multiplication operation, it delegates this task to an external multiplier module (defined as `mpyop`), which is conditional on parameter `OPT_MPY`. The results of multiplication are then processed back into the ALU.
  
The `cpuops.v` module is critical for decoding the instruction set and performing the requisite arithmetic operations before sending the results onward in the CPU pipeline.

#### Key Signals
- **Inputs:**
  - `i_clk`: Clock signal for synchronizing operations.
  - `i_reset`: Resets the module to a known initial state.
  - `i_stb`: Strobe signal indicating data validity for the current operation.
  - `i_op`: 4-bit input representing the operation code.
  - `i_a`, `i_b`: 32-bit inputs representing the operands for arithmetic operations.

- **Outputs:**
  - `o_c`: 32-bit output carrying the result of the operation.
  - `o_f`: 4-bit output carrying condition flags (zero, negative, overflow, carry).
  - `o_valid`: Indicates if the output result is valid.
  - `o_busy`: Indicates if the ALU is currently busy handling an operation.

#### Behavior of the Module
The main operational behavior of the `cpuops.v` module is defined through synchronous logic responding to clock edges and conditional statements. Here are the specific inner workings:

1. **Operation Execution**: On a valid `i_stb` signal:
   - The module evaluates a case structure based on `i_op`. Depending on the opcode, it performs different arithmetic or logic operations (e.g., addition, subtraction, bitwise operations, and shifts).
   - It also handles the specifics of multiplication operations based on the configured multiplication options and interfaces with a dedicated multiplication module.
   - Condition flag values (`z`, `n`, `v`) are calculated based on the output (`o_c`).

2. **Flags and Output Control**:
   - Flags for zero, negative, and overflow conditions are computed continuously and output through `o_f`.
   - The `o_valid` signal is used to inform other connected modules that the result can be utilized further down the processing pipeline.

3. **State Handling**:
   - The `r_busy` register tracks if the ALU is currently busy performing an operation, including factoring in the multiply operation handling.
   - The output `o_busy` serves as an indicator for the CPU control logic to manage execution flow effectively.

Overall, this module establishes a robust and flexible mechanism for processing various CPU instructions, ensuring quick response times and proper management of operational states. The usage of enables (`i_stb`) and flags allows seamless integration with the CPU's pipelined architecture, supporting efficient instruction execution.

### File: axilpipe.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axilpipe.v
### Purpose of the File
The `axilpipe.v` file implements an AXI-lite (Advanced eXtensible Interface-lite) pipeline module designed to manage memory transactions for a small, lightweight RISC CPU architecture known as Zip CPU. The purpose of the file is to support multiple outstanding memory requests simultaneously while providing efficient handling of read and write operations through a FIFO (First In, First Out) approach. This pipeline architecture enables the CPU to issue read and write requests to memory without stalling the execution pipeline even when there are pending transactions.

### Inter-module Relationships
The `axilpipe` module interacts primarily with the following components:
- **CPU Interface**: It communicates directly with the CPU core by receiving control signals (`i_stb`, `i_lock`, `i_op`, `i_addr`, `i_data`, `i_oreg`) and providing feedback signals (`o_busy`, `o_pipe_stalled`, `o_rdbusy`, etc.).
- **AXI-Lite Bus Interface**: It connects to the AXI-lite memory bus, managing signals like `M_AXI_AWVALID`, `M_AXI_WVALID`, and `M_AXI_ARVALID` for write and read requests, respectively.
- **FIFO Logic**: The module maintains a FIFO buffer for storing transaction data and managing multiple outstanding requests. Signals related to this FIFO structure are crucial for tracking read and write operations.
- **Control Logic**: It incorporates control logic to handle transaction state and to detect misaligned requests, ensuring proper communication and data integrity throughout the transaction.

### Key Signals (Inputs/Outputs)
**Inputs:**
- `S_AXI_ACLK`: Clock signal for the module.
- `S_AXI_ARESETN`: Active-low reset signal for the AXI interface.
- `i_cpu_reset`: Reset signal from the CPU.
- `i_stb`: Strobe signal indicating a valid request from the CPU.
- `i_lock`: Lock signal for atomic operations.
- `i_op`: Operation code indicating the type of access (read/write).
- `i_addr`: Memory address for the operation.
- `i_data`: Data to be written (if applicable).
- `i_oreg`: Register number for the operation.

**Outputs:**
- `o_busy`: Indicates if the module is currently busy handling transactions.
- `o_pipe_stalled`: Indicates if the transaction pipeline is stalled, affecting CPU operations.
- `o_rdbusy`: Indicates if the module is waiting for a read response.
- `o_valid`: Validity of the read result.
- `o_err`: Indicates if an error has occurred during a transaction.
- `o_wreg`: Register number where the resultant data is written.
- `o_result`: Data read from memory or modified data.

### Behavior of the Module
The `axilpipe` module operates using a series of control logic components and state machines to manage memory transactions effectively:
1. **Transaction Handling**: The module has been designed to allow multiple operations to occur simultaneously. It does this by asserting the appropriate AXI signals (`M_AXI_AWVALID`, `M_AXI_WVALID`, etc.) based on incoming CPU requests.
2. **Pipeline State Management**: It tracks outstanding transactions via a count (`beats_outstanding`) that is updated on each clock cycle based on the success or completion of transactions. It also monitors conditions under which the pipeline can stall or continues processing.
3. **Error Checking**: The module identifies misaligned requests and responds accordingly, either by providing an error signal or handling the alignment through additional logic for realignment in memory transactions.
4. **FIFO Management**: The module maintains data buffers (FIFO) for read and write operations to facilitate overwriting and reading from previous operations without impacts on subsequent CPU instructions. It manages read/write addresses and maintains alignment requirements effectively.
5. **Control State Logic**: The control logic determines when to initiate a new transaction, when to stall the pipeline (dependent on FIFO states), and when to assert error signals if conditions are not favorable for proper transaction execution.

Overall, the `axilpipe` module plays a critical role in the efficient functioning of a RISC CPU system architecture by enabling robust and efficient memory access patterns while managing various states of transaction readiness and alignment.

### File: axidcache.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axidcache.v
### Overview of axidcache.v

#### Purpose:
The `axidcache.v` file implements a data cache for the Zip CPU architecture, utilizing the AXI protocol for data transactions. The primary function of this module is to manage data storage and retrieval efficiently by caching memory reads and writes, minimizing the need for direct memory accesses, and improving overall CPU performance through reduced latency and increased speed of data fetches.

#### Inter-module Relationships:
The `axidcache` module interacts with several other modules within the Zip CPU architecture, primarily:
- **CPU Module**: It interfaces with the CPU to handle cache requests (read/write operations) by utilizing control signals and managing data transactions.
- **AXI Interface Modules**: It connects to the AXI bus, generating appropriate AXI signals (`M_AXI_*`) for read and write operations to the memory.
- **iscachable Module**: It checks if an address is cachable and determines if cache operations should proceed or bypass the cache mechanism.
- **fmem Module**: This module handles the memory interface, allowing the CPU to read data from the `axidcache` when it's hit and manages transactions accordingly.

#### Key Signals (Inputs/Outputs):
**Inputs:**
- `S_AXI_ACLK`: The clock signal for synchronization.
- `S_AXI_ARESETN`: Active low reset signal to initialize the module.
- `i_cpu_reset`: Reset signal from the CPU indicating the need to reinitialize state.
- `i_clear`: For clearing cache entries.
- `i_pipe_stb`: Indicates when the CPU wants to make a transaction.
- `i_lock`: Indicates if the transaction requires an exclusive access lock.
- `i_op`: Operation type (read/write).
- `i_addr`: Address for the transaction.
- `i_data`: Data to be written (used in write operations).
- `i_oreg`: Register information for CPU operations.

**Outputs:**
- `o_busy`: Signals if the module is currently busy with a cache operation.
- `o_rdbusy`: Indicates that a read operation is currently ongoing.
- `o_pipe_stalled`: Indicates whether the pipeline needs to stall due to cache operations.
- `o_valid`: Signals that valid data is ready for the CPU.
- `o_err`: Indication of an error during data access.
- `o_wreg`: Register for write data to the CPU.
- `o_data`: The data read from the cache.

#### Behavior:
The `axidcache` module encapsulates behavior focused on managing cache states through control logic, including state machines that handle different cache states (idle, read, write, etc.). The core behavior includes:

1. **Cache Lookup Mechanism**: It determines if data requested by the CPU is present in the cache (cache hit) or needs to be fetched from the memory (cache miss).
  
2. **Managing Transactions**: The module communicates with the AXI bus to perform read and write transactions. It generates the appropriate AXI signals based on its internal state and user requests.

3. **State Machines**: 
   - The state machine manages transitions between different cache states (e.g., `DC_IDLE`, `DC_READC`, `DC_WRITE`, etc.). Each state dictates specific behaviors: whether to initiate a read, wait for a response, or handle errors.
   - Actions are taken based on the signals from the CPU and from the AXI responses.

4. **Transaction Counting**: It keeps track of outstanding transactions to ensure that the cache does not exceed limits on concurrent requests.

5. **Error Handling**: Implements logic to track error states based on AXI responses and pipeline operations, ensuring robust communication and error reporting back to the CPU.

Overall, `axidcache.v` forms a central role in managing data flow within the CPU architecture and bridging the CPU to the memory subsystem efficiently while maintaining a high degree of data integrity and performance optimization through caching.

### File: zipcore.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/zipcore.v
### Overview and Purpose
The `zipcore.v` file implements a lightweight RISC CPU core called the Zip CPU. Its primary purpose is to serve as the central processing unit (CPU) that fetches, decodes, and executes instructions while managing associated control logic, pipeline processing, and memory interactions. The design is parameterized to offer flexibility for various configurations, including options for multiplication, division, floating-point operations, and early branching.

### Inter-module Relationships
`zipcore.v` interacts with several key modules in the CPU architecture:

1. **Instruction Fetch Modules**: 
   - It connects to the instruction fetch module to retrieve instructions, handle prefetching, and manage the instruction pipeline state.

2. **Instruction Decode**: 
   - The `zipcore` module serves as an interface to the instruction decoding process, where the fetched instructions are eligible for further decoding and execution. The `idecode` submodule is instantiated within `zipcore` to decode instructions.

3. **Arithmetic Logic Unit (ALU)**: 
   - The `cpuops` module, representing the ALU, performs arithmetic and logical operations. Outputs from the ALU are directed back into the register bank or memory as required.

4. **Memory Control**: 
   - The core interfaces with memory control modules such as `fmem` to manage memory operations like reads and writes effectively. This interaction ensures that the CPU communicates with the system memory appropriate for its current operation.

5. **Debugging Interface**: 
   - It includes provisions for debugging through the `fdebug` module, allowing external control and status monitoring.

6. **Prefetch Module**: 
   - Handles prefetching of instructions, assisting in mitigating any pipeline stalls that may occur due to instruction fetch latencies.

### Key Signals
Key signals of the `zipcore` module include:

- **Inputs**:
  - `i_clk`: Clock signal to synchronize operations.
  - `i_reset`: A reset signal to initialize the CPU state.
  - `i_interrupt`: Interrupt signal for asynchronous operation requests.
  - `i_halt`: Signals when the CPU should halt its operations.
  - Control and data signals for debugging, instruction fetching, and memory operations (e.g., `i_dbg_wreg`, `i_dbg_data`).

- **Outputs**:
  - `o_clken`: Clock enable signal that indicates when the core should be active.
  - `o_pf_new_pc`: New program counter to fetch the next instruction.
  - `o_mem_ce`: Chip enable signal for memory access.
  - `o_mem_addr`: Address signal for memory operations.
  - Debug signals (`o_dbg_stall`, `o_dbg_reg`, etc.).

### Behavior of the Module
The `zipcore` module operates in a multi-stage pipeline design, which includes the following behaviors:

1. **Pipeline Management**:
   - The core processes instructions through various stages (fetch, decode, execute, and write-back). Each stage has dedicated logic to ensure that signals propagate correctly without unnecessary stalls.

2. **Control Logic**:
   - Control signals determine whether the pipeline should advance, stall, or flush, based on the current state of ongoing operations (e.g., instruction fetch, decode, ALU operations).
   - This control ensures that valid operations are allowed to proceed while coordinating between modules actively (e.g., when waiting for data from memory).

3. **Execution Logic**:
   - The module manages condition codes and flags for operations, including branching and execution outcomes. For instance, handling illegal instructions or trapped conditions is built into the state machine and control flow logic.

4. **Memory Interfaces**:
   - Memory interface logic handles read and write operations to the data memory, coordinating with the memory hierarchy (including caches) to ensure timely data access.

5. **Debugging Support**:
   - The core includes mechanisms for debugging, including support for breakpoints and outputting current register states for examination during simulation.

6. **Conditional State**:
   - The operation modes are heavily influenced by flags and control signals that determine whether the core operates in user or supervisor mode, addressing permissions and access limitations appropriately.

Overall, `zipcore.v` encapsulates complex logic to ensure efficient operation within a pipelined architecture while maintaining flexibility through configurable parameters and signal outputs. The interactions with other modules facilitate a seamless operation that meets the requirements of a RISC architecture.

### File: slowmpy.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/slowmpy.v
### Overall Purpose
The `slowmpy.v` file implements a signed and unsigned multiplier for a RISC CPU architecture named Zip CPU. It is designed to perform multiplication operations based on a slow, low-power algorithm that processes one bit of the multiplicands per clock cycle, plus additional cycles to finalize the computation. This multiplier is suitable for environments where power efficiency is a priority, and it effectively manages signed and unsigned multiplications.

### Inter-module Relationships
The `slowmpy` module interacts with other components of the CPU architecture by providing multiplication capabilities. It responds to control signals and data inputs from the calling module, likely the execution unit or the arithmetic logic unit (ALU), which handles instruction execution. The output of this multiplier (`o_p`) is used by subsequent stages, which could involve further arithmetic, result storage, or control logic that needs the result of the multiplication. The overall integration allows the CPU to execute multiplication instructions as part of its instruction set.

### Key Signals
**Inputs:**
- `i_clk`: Clock signal used to synchronize operations within the module.
- `i_reset`: Reset signal to initialize the module.
- `i_stb`: Strobe signal indicating that the module should accept input and start processing.
- `i_a`: The first operand of the multiplication, a signed integer.
- `i_b`: The second operand of the multiplication, which can also be signed or unsigned.
- `i_aux`: Auxiliary input used as an additional control signal.
  
**Outputs:**
- `o_busy`: Indicates if the multiplier is currently performing a multiplication operation.
- `o_done`: Signals that the multiplication operation has completed.
- `o_p`: The result of the multiplication operation, which combines the bits from the two operands.
- `o_aux`: An auxiliary output potentially used for additional control or status signaling.

### Behavior of the Module
The `slowmpy` module has a control flow that operates around the state of the `o_busy` signal. 

1. **Initialization and Control Logic**:
   - When `i_reset` is activated, the module resets its internal registers (`aux`, `o_done`, `o_busy`) to indicate it’s not busy and no output is pending.
   - When the module is not busy and `i_stb` is asserted, it prepares for a new multiplication by initializing the counting mechanism, loading the input operands (`i_a` and `i_b`), and setting `o_busy` high.

2. **Multiplication Process**:
   - The module uses a loop controlled by a count register that decrements for each bit processed:
     - Each clock cycle shifts the second operand (`p_b`) right.
     - If the least significant bit of `p_b` is high, it adds the shifted first operand (`p_a`) to a partial result.
     - This process involves managing partial results over multiple cycles (equal to the width of the operands) until the multiplication is complete.

3. **Completion Logic**:
   - When the multiplication is finished (indicated by the `almost_done` flag), the result is finalized, and the `o_done` signal is set high to indicate that the multiplication is ready. 
   - The result is correctly configured depending on whether the multiplication is signed or unsigned.

4. **Formal Verification (When Applicable)**:
   - The module includes formal properties to validate assumptions and constraints during simulation, ensuring that the multiplier behaves correctly throughout its operation and adheres to expected output conditions.

The overall behavior showcases several essential digital design principles, such as sequential output generation and resource management in terms of busy/wait conditions. The use of a state machine-like approach helps manage the timing and sequencing of operations, crucial for achieving reliable CPU operations, especially in embedded systems or low-power scenarios.

### File: axiops.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axiops.v
### Description of the Verilog File `axiops.v`

#### Overall Purpose of the File:
The `axiops.v` file implements an AXI4 compliant memory interface for a lightweight RISC CPU, specifically the Zip CPU. Its main function is to facilitate read and write operations between the CPU and memory using the AXI4 protocol, handling data transfer and addressing issues while supporting various operational configuration parameters.

#### Inter-module Relationships:
1. **Interaction with AXI-compatible Components**: 
   - The `axiops` module sends and receives signals to/from other AXI components in the system, such as memories, other processors, or peripheral devices that communicate over the AXI4 bus.
   - It interacts with other components such as `fmem` (a memory unit), establishing a critical bridge between the CPU and memory for efficient data handling.

2. **Integration within the CPU Architecture**:
   - The `axiops` module interfaces directly with the CPU core through signals such as `i_stb`, `i_lock`, `i_op`, `i_addr`, and others, to control and manage data flow based on CPU instructions.
   - It also communicates the status of operations to control logic in the CPU, such as whether a read/write operation is busy (`o_busy`), valid (`o_valid`), or has encountered an error (`o_err`).

#### Key Signals (Inputs/Outputs):
- **Inputs**:
  - `S_AXI_ACLK`: Clock signal for the AXI interface.
  - `S_AXI_ARESETN`: Active-low reset signal for the AXI interface.
  - `i_cpu_reset`: Reset signal for the CPU.
  - `i_stb`: Indicates that the CPU wants to perform a transaction.
  - `i_lock`: Signal indicating locked access to shared resources.
  - `i_op`: Specifies the type of operation (read/write).
  - `i_addr`: Address for the operation.
  - `i_data`: Data to be written (for write operations).
  - `i_oreg`: Register number to write or read data.

- **Outputs**:
  - `o_busy`: Indicates if the interface is currently busy processing a request.
  - `o_rdbusy`: Indicates if a read operation is currently underway.
  - `o_valid`: Signifies that the result of an operation is valid and can be read by the CPU.
  - `o_err`: Indicates if an error occurred during the transaction.
  - `o_wreg`: The register number where the result of the operation will be written.
  - `o_result`: Contains the data read from the memory.

#### Behavior of the Module:
- **Control Logic**:
  - The `axiops` module contains a state machine that manages the various stages of memory transactions, including address acknowledgment and data readiness.
  - It uses flags like `M_AXI_AWVALID` and `M_AXI_WVALID` to track active memory requests and ensure that data is only written to the memory when the interface is ready to accept it.
  
- **Handling Address and Data Transfers**:
  - It generates AXI signals for both write (`M_AXI_AWADDR`, `M_AXI_WDATA`, etc.) and read operations (`M_AXI_ARADDR`, `M_AXI_RDATA`, etc.) in response to CPU commands.
  - The module also implements functionality to handle data that may need endian swapping and misalignment handling, essential for ensuring that the CPU operates correctly across different architectures.

- **Error Handling**:
  - It provides mechanisms to flag errors based on alignment requirements and transaction states, ensuring that the CPU is notified of any issues encountered during operations.

- **Pipelined Operations**:
  - The architecture supports pipelined operations, allowing the system to initiate new memory operations even while previous ones are still being processed, enhancing throughput and efficiency for CPU operations.

Overall, the `axiops` module encapsulates the logic required for interfacing with memory using the AXI4 protocol, ensuring synchronized operations while handling various configuration and alignment constraints determined by the CPU's architecture.

### File: axilops.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axilops.v
### Overall Purpose of the File

The Verilog file `axilops.v` implements an AXI-lite memory unit tailored for a CPU architecture known as Zip CPU, aimed at providing a lightweight and low-logic design for memory access. It serves as an interface between the CPU and the AXI-lite bus, enabling basic read and write operations while supporting various configurable options like endianness, alignment error handling, and low-power modes. The design is intended to facilitate straightforward memory operations in a way that is compatible with the CPU's operational patterns and requirements.

### Inter-module Relationships

The `axilops` module interacts with multiple components within the Zip CPU architecture:

1. **CPU Module**: It interfaces directly with the CPU, receiving instructions (like address, data, and operation type) and outputting results.
2. **AXI-Lite Bus**: It acts as the master interface for the AXI-lite bus, sending/read requests and handling responses for read and write operations.
3. **Control Logic Modules**: It interacts with control logic that governs when to perform read or write operations based on CPU requests.
4. **Peripheral Modules**: By providing memory access, it indirectly supports various peripheral devices that may interact with the CPU through the memory subsystem.

### Key Signals (Inputs/Outputs)

#### Inputs:
- `S_AXI_ACLK`: Clock signal for synchronous operation.
- `S_AXI_ARESETN`: Active-low reset signal for the AXI interface.
- `i_cpu_reset`: Reset signal for the CPU.
- `i_stb`: Strobe signal indicating a CPU operation request.
- `i_lock`: Lock signal for exclusive access.
- `i_op`: Operation code indicating the type of access (read/write).
- `i_addr`: Address from which data will be read or written.
- `i_data`: Data to be written to memory.
- `i_oreg`: Register number for the operation.

#### Outputs:
- `o_busy`: Indicates that an operation is currently underway (either reading or writing).
- `o_rdbusy`: Indicates that a read operation is in progress.
- `o_valid`: Indicates that a valid read result is available.
- `o_err`: Indicates that an error occurred during the operation.
- `o_wreg`: Register output number to which results will be written.
- `o_result`: Result data that is read from memory or computed from a write operation.

### Behavior of the Module

The `axilops` module includes several key functionalities and control mechanisms:

1. **Control Logic**: The module manages control signals such as `M_AXI_AWVALID`, `M_AXI_WVALID`, `M_AXI_ARVALID`, and corresponding `*_READY` signals to orchestrate read and write requests in a synchronous manner. It ensures that proper signals are asserted based on the current operation type and memory access state.

2. **Endianness Handling**: Configurable parameters such as `SWAP_ENDIANNESS` and `SWAP_WSTRB` allow for byte order adjustments, ensuring compatibility of data transferred over the AXI-lite bus with the expected format of the Zip CPU.

3. **Alignment Error Checking**: The module checks for alignment errors when reading or writing data to ensure that operations respect the address requirements (e.g., 4-byte boundaries for full word accesses). If an alignment error occurs, it can either report the error or handle it by automatically correcting the alignment issue based on set parameters.

4. **Low Power Operations**: When `OPT_LOWPOWER` is enabled, the module incorporates logic to minimize transitions and power consumption by setting unused registers and signals to low states until they are needed.

5. **State Management**: The module utilizes various internal states to track whether it is currently busy with an operation or empty, responding to requests appropriately. It internally manages states for misalignment requests and ongoing read or write operations, coordinating transactions with the AXI-lite bus.

6. **Result Handling**: The module prepares results for the CPU by handling data received from the memory and managing how results are returned based on the operation and conditions like signed extension.

In summary, the `axilops` module serves as a crucial interface between the Zip CPU and the AXI-lite bus, facilitating memory transactions and ensuring that operations adhere to various configurable parameters for system operation. The intricate control logic and state management ensure that these operations are performed reliably and efficiently.

### File: div.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/div.v
### Overall Purpose of the File

The `div.v` file implements an integer division unit for the Zip CPU, providing support for both signed and unsigned division operations. The module is designed to handle division requests, manage the necessary calculations, and communicate the results, including error signaling in the event of division by zero.

### Inter-module Relationships

The `div` module interacts with the broader architecture of the Zip CPU as follows:

- **Integration with the CPU Pipeline**: The division unit communicates with the instruction decode and execute stages, receiving instructions from the pipeline and emitting results and status signals as needed.
- **Signal Coordination**: It sends and receives control signals to/from other components, such as the processing units or the memory subsystem, ensuring proper sequencing and timing for division operations.
- **Error Reporting**: The `o_err` signal indicates division errors (specifically division by zero), which other modules must handle appropriately to maintain CPU integrity and proper operation.

### Key Signals (Inputs/Outputs)

#### Inputs:
- `i_clk`: The clock signal that synchronizes operations within the division module.
- `i_reset`: Resets the internal state of the division unit.
- `i_wr`: A write signal that indicates a division operation has been requested.
- `i_signed`: A control signal indicating whether the division should be treated as signed.
- `i_numerator`: The numerator (dividend) for the division operation.
- `i_denominator`: The denominator (divisor) for the division operation.

#### Outputs:
- `o_busy`: Indicates that the division operation is in progress.
- `o_valid`: Indicates that the division result is valid and can be used.
- `o_err`: An error flag that signals if a division by zero has occurred.
- `o_quotient`: The result of the division operation.
- `o_flags`: Additional flags related to the result, such as zero result (Z), negative result (N), carry (C), etc.

### Behavior of the Module

The division module operates through a structured sequence of steps and control logic, embodying a state machine approach for managing the various stages of division:

1. **Idle/Reset State**: On reset (`i_reset`), the module initializes, setting all outputs and internal registers to known starting values.

2. **Request Initiation**: When `i_wr` is asserted, the division process begins. The module sets the `o_busy` signal to high, indicating an active operation.

3. **Sign Management**: If the division is signed, an additional clock cycle is used to compute the absolute values of the numerator and the denominator. This is controlled by the `pre_sign` flag.

4. **Division Logic**: The division is executed through a process similar to long-division, where bits of the numerator are compared with the denominator. It employs a loop to determine the quotient, modifying internal registers (`r_dividend`, and `r_divisor`) based on the comparison results. 

5. **Error Handling**: The module checks for division by zero, setting the `zero_divisor` flag if applicable. If division by zero is detected, `o_err` is asserted, and `o_valid` will indicate the result of the operation once it's completed.

6. **Completion**: After processing all necessary cycles (up to 32 cycles for a 32-bit divide), the module determines if the final result should be negated based on the sign information. The `o_valid` signal is set to true when the result is ready for use, and the `o_busy` signal will be de-asserted.

7. **State Management**: The module uses various internal state registers (`r_busy`, `r_sign`, `last_bit`) to manage operation timing and ensure synchronization with input signals. These states help track whether a division is ongoing and the current bit's significance in the division process.

Through this structured approach, the `div` module reliably handles division operations, ensuring that valid results are generated and that error states are properly managed. The design is robust, featuring mechanisms to handle both signed and unsigned integers, making it a critical component of the CPU's arithmetic capabilities.

### File: pffifo.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/pffifo.v
### Overview of `pffifo.v`

**Purpose:**
The `pffifo.v` file implements a prefetch FIFO (First-In-First-Out) buffer for a CPU architecture, specifically designed to handle the continuous fetching of instructions with minimal stalls. This module aims to keep the CPU well fed with instruction data at a target rate of ideally one instruction per clock cycle, optimizing instruction throughput.

### Inter-module Relationships:
- **Connection to CPU Components:** The `pffifo` module interacts with a CPU's request and control mechanisms. It interfaces with:
  - The instruction-fetching logic (potentially another submodule that sends requests for new instructions).
  - A memory interface that fetches the instructions from the memory subsystem.
- **Control Signals with other Modules:** The module communicates through control signals that are crucial for instruction fetching, such as `i_new_pc` and `i_clear_cache` for managing instruction requests, and `i_ready` for signaling when the CPU is prepared to accept the next instruction.
- **Integration with Wishbone Protocol:** It uses the Wishbone interface to handle memory operations, consisting of signals for dealing with memory reads/writes, responses, and error handling.

### Key Signals:
- **Inputs:**
  - `i_clk`: Clock signal for synchronization.
  - `i_reset`: Asynchronous reset signal for the module.
  - `i_new_pc`: A signal indicating when a new program counter value needs to be fetched for instruction prefetch.
  - `i_clear_cache`: A signal that clears any cached instructions.
  - `i_ready`: Indicates readiness of the CPU to receive a new instruction.
  - `i_pc`: The current program counter value to fetch instructions from.
  
- **Outputs:**
  - `o_valid`: Indicates whether the fetched instruction is valid.
  - `o_illegal`: Signals an illegal instruction fetch (e.g., an error in fetching).
  - `o_insn`: The instruction fetched from the FIFO buffer.
  - `o_pc`: The program counter after the instruction has been fetched.
  
- **Wishbone Interface Outputs:**
  - `o_wb_cyc`, `o_wb_stb`: Control signals for the Wishbone bus indicating a cycle and a strobe for an on-going transfer.
  - `o_wb_addr`: The address to fetch from memory during a read operation.
  - `o_wb_data`: Data placeholder for writing to memory (though only reads are performed here).
  - `o_wb_sel`: Selects which bytes are being read from/written to on the bus.

### Behavior of the Module:
- **Control Logic:**
  - The `pffifo` module contains control logic that manages instruction requests and buffers responses. It builds a FIFO buffer that stores instructions fetched from the memory. 
  - The requests are managed according to the status of the FIFO (i.e., whether it's empty or full) and the results of memory requests (acknowledgments, errors).
  
- **State Management:**
  - The module employs state management to handle conditions like pending errors (`pending_err`), instruction fetching (`wb_pending`), and the number of instructions ready for the CPU (`pipe_fill`).
  - Control flows through several states, responding to clock cycles and input signals to coordinate fetching, storing, and delivering instructions.
  
- **Instruction Fetching Mechanism:**
  - Upon receiving a new program counter or a cache clear signal, the module retrieves the relevant instruction data via the Wishbone interface, buffers it, and prepares it for access by the CPU.
  - It also features mechanisms to identify and declare illegal instructions based on the fetched instruction data and its context in the FIFO.

- **Error Handling:**
  - The module detects errors during memory transactions and flags them appropriately, preventing the propagation of erroneous instruction data to the CPU.
  
In summary, `pffifo.v` plays a crucial role in the instruction fetching subsystem of a CPU, ensuring efficient data flow while providing mechanisms for control, error handling, and integration with other architecture components.

### File: axiicache.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axiicache.v
### Overview of the `axiicache.v` Module

#### Purpose
The `axiicache.v` module implements an instruction cache for a CPU designed with an AXI (Advanced eXtensible Interface) interface. Its primary purpose is to efficiently provide instruction fetching from memory, optimizing access times to improve CPU performance by caching previously accessed instructions. The design aims to return instructions within a single clock cycle, with mechanisms in place to handle cache misses, illegal instructions, and memory read requests.

#### Inter-module Relationships
- **FFetch Module**: The `axiicache.v` interacts with the instruction fetch logic (likely represented as `ffetch`). The fetch module supplies the program counter (`i_pc`) and receives the fetched instructions (`o_insn`), the program counter corresponding to the returned instruction (`o_pc`), and an illegal instruction signal (`o_illegal`).
- **AXI Memory Interface**: Connections with the AXI memory controller are established to issue read requests (`M_AXI_AR*`) and receive responses (`M_AXI_R*`). The AXI bus handles the memory transactions required to fill the cache when there is a cache miss.
- **CPU Interface**: The module responds to signals from the CPU, including reset (`i_cpu_reset`), new program counter (`i_new_pc`), and cache clear signals (`i_clear_cache`).

#### Key Signals
- **Inputs**:
  - `S_AXI_ACLK`: System clock signal.
  - `S_AXI_ARESETN`: Active-low reset signal.
  - `i_cpu_reset`: Resets the CPU.
  - `i_new_pc`: Indicates the CPU has provided a new program counter.
  - `i_clear_cache`: Clears the cache.
  - `i_ready`: Indicates readiness for the next operation.
  - `i_pc`: The current program counter from the CPU.
  
- **Outputs**:
  - `o_insn`: Fetched instruction output.
  - `o_pc`: Corresponding program counter for the fetched instruction.
  - `o_valid`: Indicates whether a valid instruction is being output.
  - `o_illegal`: Indicates if the fetched instruction address was illegal.

#### Behavior
The `axiicache` module operates with a clocked state machine to manage instruction fetching and cache management effectively. Here’s a breakdown of its main functionalities:

1. **Cache Management**:
   - The cache is maintained, checking if the requested instruction is present. If present (cache hit), the appropriate instruction is provided to the CPU.
   - On a cache miss, the module initiates a reading operation from the AXI bus to fetch the required instruction from memory.
   
2. **Request Handling**:
   - The module checks whether the request (from either the CPU or the AXI bus) is valid by examining tags, cache states, and any pending requests.
   - It implements logic to handle different types of accesses, including jumps and branches, which may require cache line changes.

3. **Control Logic and State Handling**:
   - The module features a control state machine that drives the read requests and manages responses from the AXI bus, updating the cache and internal state based on the results.
   - The module will track valid, last accessed addresses and the corresponding tags to optimize future requests, minimizing delays from illegal accesses or cache misses.

4. **Error Management**:
   - It monitors for illegal reads, triggering the `o_illegal` signal if a read response from memory indicates an error.
   - In case of a bus abort (error in reading), the corresponding cache line's validity is reset.

5. **Fetching Process**:
   - Instructions are fetched from the cache based on the current PC (`i_pc`). If the instruction is valid and present in the cache, it is output immediately.
   - In situations where the instruction is not present, it triggers the AXI read cycle, waits for the response, and populates the cache accordingly.

This comprehensive approach to managing the instruction cache is designed to enhance the efficiency of instruction access within the CPU, thereby improving overall performance.

### File: prefetch.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/prefetch.v
### Purpose of the File
The `prefetch.v` file implements a simple instruction prefetch mechanism for the Zip CPU architecture. This module is responsible for retrieving one instruction at a time from memory based on the program counter (PC) value provided by the CPU. The module features a basic structure that allows for the fetching, acknowledgement, and handling of instruction errors while adhering to the principles of a fetch stage in a RISC CPU pipeline. Future enhancements could involve pipelining the fetch requests and integrating caching mechanisms for improved performance.

### Inter-Module Relationships
The `prefetch` module interacts primarily with the CPU control unit and the Wishbone (WB) bus interface. It connects with the instruction decode module (referred to as `ffetch` in formal assertions) to provide valid instruction data as fetched from memory, while also managing the necessary handshake signals with the WB bus:

- **CPU Control**: The `prefetch` module receives signals from the CPU, such as the new program counter (`i_new_pc`), requests to clear the cache (`i_clear_cache`), and whether the CPU is ready to accept new instructions (`i_ready`).
- **Wishbone Bus**: The module communicates with the WB interface by generating control signals like `o_wb_cyc` (to indicate a bus cycle in progress) and `o_wb_stb` (to indicate that the current transaction is valid). It also processes signals from the WB bus, such as `i_wb_ack` (acknowledgement of instruction received) and `i_wb_err` (error flag).

### Key Signals
- **Inputs**:
  - `i_clk`: Clock signal for timing synchronization.
  - `i_reset`: Resets the module to its initial state.
  - `i_new_pc`: Indicates a request for a new program counter value.
  - `i_clear_cache`: Requests cache to be cleared.
  - `i_ready`: Signal from the CPU indicating readiness to receive new instruction data.
  - `i_pc`: Suggested program counter for the next instruction fetch.
  - `i_wb_stall`, `i_wb_ack`, `i_wb_err`: Feedback from the WB interface.
  - `i_wb_data`: Data returned from the WB bus.

- **Outputs**:
  - `o_valid`: Indicates if the output instruction data is valid.
  - `o_illegal`: Signals if an illegal instruction was fetched (due to a bus error).
  - `o_insn`: The instruction fetched from memory.
  - `o_pc`: Program counter aligned with the fetched instruction.
  - `o_wb_cyc`, `o_wb_stb`: Control signals for bus transactions.
  - `o_wb_addr`: The address from which data is being fetched.

### Behavior of the Module
The `prefetch` module implements control logic to manage the instruction fetching process:

1. **Initialization and Reset Handling**: It sets its outputs to invalid upon reset or when a new PC or clear cache request is received.

2. **Bus Transaction Management**: It controls the process of initiating and concluding WB transactions. A bus cycle begins when the CPU signals readiness (`i_ready`), the previous output was valid, and there’s either a request for a new PC or if the previous bus result was invalid.

3. **Invalidation Logic**: The module tracks whether an incoming request (e.g., a new PC) renders the current bus request invalid. If a new PC request occurs, the `invalid` flag is set, preventing the module from sending stale data to the CPU.

4. **Address Generation**: The calculation of the Wishbone request address occurs based on the incoming program counter. This address increments on successful fetches unless a new PC is signaled.

5. **Data Handling**: The fetched instruction can be shifted based on the configured endianness (little or big). The module manages the shifting process depending on the instruction and bus data widths.

6. **Output Control**: Upon positive acknowledgment from the WB bus, the output instruction is updated. The module raises the valid output (`o_valid`) once it has completed a fetch cycle successfully, while `o_illegal` indicates if the instruction fetch resulted in an error.

This design allows the `prefetch` module to reliably interface with both the CPU and memory subsystem through the Wishbone architecture, managing the intricacies of instruction fetching while providing the necessary feedback for subsequent processing stages in the CPU pipeline.

### File: dblfetch.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/dblfetch.v
### Overview of `dblfetch.v`

#### Purpose of the File
The `dblfetch.v` file implements a dual instruction fetch mechanism for a RISC CPU. Unlike a simple instruction fetch (as seen in `prefetch.v`), `dblfetch.v` allows the CPU to fetch two instruction words in a single bus cycle by utilizing memory pipelining. This feature aims to enhance the CPU's performance by keeping it busy while waiting for potentially slow memory operations to complete. The module manages its bus transactions intelligently to maximize instruction throughput and handle busy states elegantly.

#### Inter-module Relationships
The `dblfetch` module interacts with the following components in the CPU architecture:

- **CPU Control Logic**: It receives signals from the CPU for new program counter values (`i_new_pc`), cache clearing (`i_clear_cache`), and readiness (`i_ready`).
- **Wishbone Interface**: It connects to the memory subsystem via a Wishbone interface, generating bus cycle signals (`o_wb_cyc`, `o_wb_stb`, `o_wb_addr`, etc.) and receiving responses.
- **Fetching and Decoding Logic**: It coordinates with the `ffetch` module by providing instructions and status signals, including `o_valid`, `o_insn`, and `o_pc` for instruction execution.

#### Key Signals
- **Inputs**:
  - `i_clk`: System clock signal.
  - `i_reset`: Asynchronous reset signal.
  - `i_new_pc`: Signal indicating a new program counter value is available.
  - `i_clear_cache`: Signal to indicate the cache should be cleared.
  - `i_ready`: Signal to indicate the CPU is ready to receive a new instruction.
  - `i_pc`: Current program counter value.
  - `i_wb_stall`: Indicates whether the bus operation is stalled.
  - `i_wb_ack`: Acknowledgement signal from the memory subsystem.
  - `i_wb_err`: Indicates an error on the bus operation.
  - `i_wb_data`: Data received from memory.

- **Outputs**:
  - `o_valid`: Indicates that valid instructions are available.
  - `o_illegal`: Indicates whether the fetched instruction is illegal.
  - `o_insn`: The fetched instruction or instructions.
  - `o_pc`: The program counter associated with the fetched instruction.
  - `o_wb_cyc`: Indicates a Wishbone cycle is active.
  - `o_wb_stb`: Indicates a Wishbone request is being made.
  - `o_wb_addr`: Address for the Wishbone transaction.
  - `o_wb_data`: Data being sent on the Wishbone bus.

#### Behavior of the Module
The `dblfetch` module utilizes several control logic mechanisms to manage instruction fetching:

1. **Bus Cycle Management**:
   - The module starts new bus cycles under specific conditions (like a new program counter or an invalid cycle).
   - It maintains the state of bus cycles (`o_wb_cyc`, `o_wb_stb`) and manages the transition between them based on the acknowledgement (`i_wb_ack`), errors (`i_wb_err`), and stall conditions (`i_wb_stall`).

2. **Inflight Handling**:
   - It keeps track of the number of outstanding requests (`inflight`) to handle bus traffic efficiently and ensure that new requests are only issued when the previous ones are acknowledged.

3. **Instruction Caching**:
   - The module uses a cache mechanism to hold fetched instructions. If the CPU is ready and the cache is valid, it prioritizes fetching instructions from the cache over fetching from memory.
   - It also manages the legality of cached instructions, signaling any illegal fetches through `o_illegal`.

4. **Output Generation**:
   - Based on the current state, it drives the output signals such as `o_insn`, `o_pc`, and `o_valid` to inform the CPU about the fetched instructions and their corresponding addresses.

5. **Formal Verification**:
   - The module includes formal verification checks to ensure correctness in various states, ensuring the fetched instructions are valid, and that any illegal states are handled appropriately.

Overall, `dblfetch.v` facilitates robust instruction-fetching capabilities, improving CPU performance through effective bus management and dual instruction prefetching.

### File: axilfetch.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axilfetch.v
### Overall Purpose
The `axilfetch.v` file implements an instruction fetch module for the Zip CPU architecture, according to the AXI-lite protocol. It is responsible for fetching instructions from memory and providing them to the CPU. This module handles fetching, prefetching, and buffering of instructions, optimizing the instruction retrieval process to reduce latency and improve CPU performance.

### Inter-module Relationships
The `axilfetch` module interacts with several components within the CPU architecture:
- **Instruction Fetching**: It retrieves instructions from memory for execution in coordination with the `ffetch` module.
- **CPU Control Signals**: It interfaces with the CPU to react to control signals such as `i_cpu_reset`, `i_new_pc`, and `i_clear_cache` which dictate when to reset, fetch new instructions, or clear the instruction cache.
- **AXI-lite Bus**: As a master device, it communicates with an AXI-lite compliant memory bus, utilizing signals like `M_AXI_ARVALID`, `M_AXI_ARADDR`, `M_AXI_RVALID`, and `M_AXI_RDATA` for reading instructions from memory.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `S_AXI_ACLK`: Clock input for AXI interface.
  - `S_AXI_ARESETN`: Active low reset signal for the AXI interface.
  - `i_cpu_reset`: Resets the CPU and instruction fetching mechanism.
  - `i_new_pc`: Indicates a new program counter value for fetching instructions.
  - `i_clear_cache`: Clears the instruction cache.
  - `i_ready`: Signals readiness for the next instruction.
  - `i_pc`: Instruction address for fetching.
- **Outputs**:
  - `o_insn`: Instruction fetched from the memory.
  - `o_pc`: Program counter (address) of the fetched instruction.
  - `o_valid`: Indicates whether the fetched instruction is valid.
  - `o_illegal`: Indicates if an illegal operation or bus error occurred.
- **AXI Outputs**:
  - `M_AXI_ARVALID`: Signal to indicate a valid read address.
  - `M_AXI_ARADDR`: Address from which the instruction is to be fetched.

### Behavior of the Module
The `axilfetch` module exhibits the following behaviors:

1. **Instruction Fetching Logic**: It employs a FSM (Finite State Machine) to manage the state of instruction requests and responses over the AXI bus. It generates read requests and handles the incoming instruction data.

2. **Control Logic**: The module contains conditional logic that responds to various input conditions. For instance:
   - If `i_new_pc` is asserted, it triggers fetching the instruction from the new program counter address.
   - If `fifo_reset` is asserted, the fetching and buffering counters and states are reset.

3. **Request Throttling**: The module includes logic to prevent excessive read requests from overwhelming the AXI bus. It limits the number of outstanding requests through counters and status flags, ensuring efficient bandwidth usage on the AXI bus.

4. **Data Processing**: The module handles endian swapping based on the `SWAP_ENDIANNESS` parameter and processes multiple instructions fetched in a single bus transaction, allowing for efficient data handling across varying bus widths (e.g., 32-bit vs. 64-bit).

5. **Instruction Validity Management**: It tracks whether the fetched instructions are valid or if an error occurred during the fetch process, indicated by the `o_valid` and `o_illegal` signals.

Through these mechanisms, the `axilfetch` module effectively retrieves instructions for the CPU while managing the flow of data in accordance with the operational requirements of the Zip CPU architecture.

### File: iscachable.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/iscachable.v
### Overall Purpose of the File

The `iscachable.v` file implements combinatorial logic that determines whether a given address is cacheable in the context of a memory hierarchy in the Zip CPU architecture. It assists both the data cache (dcache) and any formal properties that check whether specific addresses can be cached, ensuring efficient memory access and performance.

### Inter-module Relationships

The `iscachable` module interacts primarily with the data cache subsystem (dcache) within the CPU architecture. Its output, `o_cachable`, is used by the dcache to decide if a memory operation can utilize caching mechanisms for improved performance. This interaction is crucial for maintaining a streamlined memory access pattern, particularly in systems that require high bandwidth and lower latency.

### Key Signals (Inputs/Outputs)

- **Input:**
  - `i_addr` (width: `AW`, which is 32 by default): A bus representing the address that is being checked for cachability.

- **Output:**
  - `o_cachable` (1 bit): A flag that indicates whether the provided address is cacheable (1) or not (0).

### Behavior of the Module

The behavior of the `iscachable` module follows a simple combinatorial logic structure encapsulated in an `always @(*)` block, which means it reacts to changes in any of its inputs immediately.

1. **Initial Condition:**
   - The output `o_cachable` is initialized to `1'b0` (not cacheable).

2. **Cachability Check:**
   - The module checks specific address ranges based on predefined parameters (including the `SDRAM_ADDR`, `FLASH_ADDR`, and `BKRAM_ADDR`). If a non-zero address is defined for any of these categories, the module performs a bitwise AND operation between the input address (`i_addr`) and the corresponding address mask:
     - If `i_addr` matches the `SDRAM_ADDR` based on the `SDRAM_MASK`, `o_cachable` is set to `1`.
     - Similarly, it checks for `FLASH_ADDR` and `BKRAM_ADDR` using their respective masks.
   - The module only sets `o_cachable` to `1` if the specific addresses match specified parameters, indicating that those memory locations can benefit from caching.

### Summary

In essence, the `iscachable` module provides critical combinatorial logic to assess the cachability of memory addresses in the Zip CPU architecture, facilitating efficient caching decisions in the data cache subsystem. This leads to improved performance by optimizing the memory access patterns of the CPU while adhering to the address specifications required for each memory type.

### File: idecode.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/idecode.v
### Overall Purpose of the File
The `idecode.v` file implements the instruction decoding logic for the Zip CPU, a small RISC CPU soft core. Its primary purpose is to decode instructions fetched from memory, determining operational codes, operand types, and the conditions under which instructions should execute. It manages the translation of raw instruction data into control signals that can guide subsequent stages of instruction execution in the CPU pipeline.

### Inter-module Relationships
The `idecode` module interacts with various components within the CPU architecture:

1. **Instruction Fetch Logic**: It receives instructions from the fetch stage and determines their meaning. This interaction is crucial for managing instruction flow into the decoding stage.

2. **Execution Stage**: The outputs of `idecode` provide control signals that correspond to operations that need to be performed in the execution stage. It communicates information on what operation to perform, which registers to access, and under what conditions.

3. **Memory Control**: It interacts with the memory management subsystem to determine if certain instructions involve read/write operations, thereby coordinating with external memory devices.

Moreover, the module may have formal verification properties (`FORMAL` section) that ensure the correctness of its behavior and that it meets architectural expectations.

### Key Signals (Inputs/Outputs)
**Inputs**:
- `i_clk`: The clock signal for synchronous operations.
- `i_reset`: A signal to reset the module to a known state.
- `i_ce`: Clock enable signal, indicating when the module should be active.
- `i_stalled`: Indicates whether the fetching process is stalled.
- `i_instruction`: The instruction word fetched from memory to decode.
- `i_gie`: Global interrupt enable signal.
- `i_pc`: The program counter representing the current instruction address.
- `i_pf_valid`: Indicates if the prefetched instruction is valid.
- `i_illegal`: Signals if an illegal operation was attempted.

**Outputs**:
- `o_valid`: Asserts when the output from the decoder is valid.
- `o_phase`: Indicates the phase of instruction processing (e.g., first or second half for CIS instructions).
- `o_illegal`: Signals if the instruction being processed is illegal.
- `o_pc`: The program counter output for the instruction being processed.
- `o_dcdR`, `o_dcdA`, `o_dcdB`: Outputs to indicate destination and source registers for the instruction.
- `o_I`: The immediate value extracted from the instruction.
- `o_zI`: Indicates if the immediate value is zero.
- `o_cond`: The condition under which the instruction operates.
- Control signals such as `o_ALU`, `o_M`, `o_DV`, `o_FP`, `o_break`, `o_lock`, `o_wR`, `o_rA`, and `o_rB` indicate the operation modes and register accesses.

### Behavior of the Module
The behavior of the `idecode` module can be summarized into the following aspects:

1. **Instruction Decoding Logic**: 
   - The module interprets the `i_instruction` signal and determines the type of operations to perform (e.g., MOV, ALU operations, branch instructions, etc.) based on pre-defined opcodes. 
   - The opcodes are analyzed using various conditions to categorize the instruction type, which determines how the CPU responds to the instruction.

2. **Control Logic and Conditions**: 
   - The output conditions (`o_cond`, `o_wF`, etc.) are set based on the various calculated paths. For example, the `o_cond` output indicates under what conditions the instruction should execute, supporting features like conditional execution.

3. **Instruction Validity and Control Signals**: 
   - The module maintains status signals like `o_valid` and `o_illegal` to control downstream logic that depends on valid instruction processing.
   - It incorporates checks to ensure that illegal instructions do not propagate to later pipeline stages, offering robustness in instruction handling.

4. **State Machine Behavior**: 
   - Some state management occurs through conditional logic to ascertain if the instruction is a long jump, which affects how the instruction is processed and what values are sent down to subsequent stages.

5. **Pipelining Support**: 
   - The module supports pipelining functionality, so it can process instructions in an overlapped manner, using the `o_phase` signal for managing instruction halves in compressed instruction sets (CIS).

6. **Immediate Value Extraction**: 
   - It manages immediate value generation (`w_fullI`, `w_I`) based on the specific instruction logic, allowing for operand evaluations critical for operations like LOAD immediate (LDI).

In conclusion, the `idecode` module plays a crucial role in decoding instructions for the Zip CPU, ensuring that each step in instruction processing is performed correctly, thereby facilitating efficient execution of the CPU architecture.

### File: mpyop.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/mpyop.v
### Overall Purpose of the File
The `mpyop.v` file implements a flexible multiplier operation for the Zip CPU architecture. Its main objective is to encapsulate various multiplication algorithms, allowing for performance optimization in terms of timing and resource utilization. This separation from other components enhances abstraction and maintainability of the CPU's design, facilitating easier testing and potential future modifications.

### Inter-module Relationships
The `mpyop.v` module interacts primarily with:
- **CPU Control Logic**: It receives various control signals (e.g., `i_stb`, `i_op`) that dictate the operation type and initiation of multiplication.
- **Other Arithmetic/Logic Units**: Depending on the defined multiplication strategy, it may interact with different representations of operands (signed/unsigned) and other arithmetic functions.
- **Result Latch**: The output signals from this module (like `o_valid` and `o_result`) are likely used by subsequent modules in the execution stage of the CPU to complete arithmetic operations.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_clk`: The clock signal for synchronous operation.
  - `i_reset`: Reset signal to initialize the module.
  - `i_stb`: Indicates a valid multiplication operation request.
  - `i_op`: A 2-bit signal to select the type of multiplication operation. 
    - `00`: 32x32 multiply, returning low order bits,
    - `10`: 32x32 unsigned multiply, returning upper bits,
    - `11`: 32x32 signed multiply, returning upper bits.
  - `i_a`, `i_b`: The operands for multiplication, each 32 bits wide.

- **Outputs**:
  - `o_valid`: Signal indicating the result of the multiplication is valid and ready for use.
  - `o_busy`: Signal indicating that the multiplier is currently processing a multiplication operation.
  - `o_result`: A 64-bit output that contains the result of the multiplication.
  - `o_hi`: Indicates whether to return the high half of the multiplication result as dictated by the input operation type.

### Behavior of the Module
The `mpyop.v` module implements several multiplication strategies based on the `OPT_MPY` parameter. 

- **No Multiply (OPT_MPY == 0)**: The module outputs zero and sets the `o_valid` signal based on `i_stb`, essentially bypassing multiplication.

- **Single Clock Multiply (OPT_MPY == 1)**: A straightforward multiply operation is performed in one clock cycle. The result is produced immediately, and control signals are set accordingly.

- **Two Clock Multiply (OPT_MPY == 2)**: The inputs are registered on the first clock edge, and multiplication occurs on the second so it introduces a delay allowing better control.

- **Three Clock Multiply (OPT_MPY == 3)**: A more complex operation that registers inputs and incorporates state management through the `mpypipe` register. After pipelining the input through stages, the actual multiply results are managed over three clock cycles.

- **Four Clock Multiply (OPT_MPY == 4)**: This strategy implements polynomial multiplication, requiring multiple stages to compute partial products. Each clock iterates through states that correspond with further calculations of partial products before producing the final result.

- **Slow Multiply (OPT_MPY > 4)**: For situations where faster hardware multipliers are not available, the module leverages an external slow multiplier module, maintaining compatibility with the architecture.

### Control Logic and State Machines
- The behavior of the module is heavily dependent on pipelined registers (`mpypipe`) that track the state of incoming operations and the timing of results.
  
- Always blocks handle synchronization with the clock and reset signals, managing when to reset internal states and when to hold specific values based on active operations.

Overall, this module's design allows for a scalable approach to multiplication operations within the CPU, accommodating various algorithms suited for different hardware capabilities and operational optimizations.

### File: pipemem.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/pipemem.v
### Overall Purpose

The `pipemem.v` file implements a memory unit designed to support pipelined Wishbone memory accesses for a small, lightweight RISC CPU known as the Zip CPU. The module is engineered to enable issuing one pipelined Wishbone access per clock cycle, allowing for efficient single-cycle retrieval of data, assuming the memory subsystem is fast enough. This design is aimed at facilitating pipelined CPUs' performance by handling memory requests and responses in a streamlined manner.

### Inter-module Relationships

The `pipemem` module interacts predominantly with other components in the Zip CPU architecture via the Wishbone interface. It communicates with the CPU's control signals and registers to manage memory operations effectively. The primary interactions include:

- **CPU Interface:** Inputs such as instruction addresses, data to write, and control signals from the CPU (e.g., `i_pipe_stb`, `i_op`, `i_addr`, etc.) trigger memory read/write operations based on CPU commands.
- **Wishbone Interface:** Outputs control signals to the Wishbone bus (`o_wb_stb`, `o_wb_cyc_lcl`, `o_wb_cyc_gbl`, etc.) to manage local and global memory accesses and relay data back to the CPU (`i_wb_data`, etc.).

The module also orchestrates the necessary flow control through signals that indicate whether the memory is busy or whether requests can be accepted.

### Key Signals (Inputs/Outputs)

#### Inputs:
- **Clock and Reset:**
  - `i_clk`: Clock signal that synchronizes operations.
  - `i_reset`: Resets module state upon activation.

- **CPU Command Signals:**
  - `i_pipe_stb`: Indicates that the CPU is producing a new request.
  - `i_lock`: Signal to enable a lock on memory operations.
  - `i_op`: Operation code indicating type of memory transaction.
  - `i_addr`: Address for memory access.
  - `i_data`: Data input for write operations.
  - `i_oreg`: Register output index for the operation.

- **Wishbone Signals:**
  - `i_wb_stall`: Suggests the current cycle cannot process operations.
  - `i_wb_ack`: Acknowledgement of a valid memory operation.
  - `i_wb_err`: Error indication from the memory subsystem.
  - `i_wb_data`: Data retrieved from the Wishbone bus after read operations.

#### Outputs:
- **CPU Response Signals:**
  - `o_busy`: Indicates the memory is currently processing a request.
  - `o_rdbusy`: Indicates if the memory is dedicated to read operations.
  - `o_pipe_stalled`: Indicates that the pipeline is stalled due to memory constraints.
  - `o_valid`: Indicates successful completion of a memory operation.
  - `o_err`: Represents memory operation errors.

- **Memory Control Signals for Wishbone:**
  - `o_wb_cyc_gbl`, `o_wb_cyc_lcl`: Signals for global and local memory cycles.
  - `o_wb_stb_gbl`, `o_wb_stb_lcl`: Signals to assert the start of a Wishbone transaction.
  - `o_wb_we`: Write enable signal.
  - `o_wb_addr`: Output address for memory transactions.
  - `o_wb_data`: Data output signal for write operations.
  - `o_wb_sel`: Select signals for byte validity in memory transactions.

### Behavior of the Module

The `pipemem` module implements a comprehensive control logic mechanism to manage memory requests in a pipelined architecture. The key behaviors include:

1. **FIFO Mechanism:** Implements a first-in-first-out (FIFO) buffer structure to queue memory requests. Address pointers (`wraddr`, `rdaddr`) manage the writing and reading of requests, allowing multiple simultaneous access requests.

2. **Control Logic:** Implements combinational and sequential logic to manage the state transitions based on the current requests:
   - Memory operations can be issued on detecting the `i_pipe_stb` signal unless the pipeline is stalled due to errors or alignment issues.
   - Data is fetched or written based on operation type (read or write) and address alignment errors are flagged when applicable.
   - A locking mechanism is used to manage global and local bus accesses, ensuring no contention occurs between various memory requests.

3. **Pipelining Logic:** The module keeps track of the operational status using signals for busy states and access completion, allowing the CPU to proceed without stalling unnecessarily when the memory is busy.

4. **Parameterization:** It includes various parameters to customize its behavior, such as the address and bus widths and options for alignment error detection, enabling the integration of different configurations in the CPU's architecture.

Overall, the `pipemem` module operates as an efficient memory controller, ensuring that pipelined access to the memory subsystem is conducted effectively while handling potential errors and busy states gracefully.

### File: zipwb.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/zipwb.v
### Description of the Verilog File: `zipwb.v`

#### Overall Purpose:
The `zipwb.v` file implements the top-level module of the Zip CPU architecture, acting as the core component that unifies various parts of the CPU. This module orchestrates the interactions between the instruction fetching, execution, and memory operations in a pipelined fashion. It is designed to provide a lightweight, efficient RISC processing core capable of executing a limited set of instructions while facilitating bus operations over a Wishbone bus interface.

#### Inter-module Relationships:
- The `zipwb` module directly interfaces with several internal components:
  - **`zipcore`**: This is the central processing unit that handles the core operations of the CPU, managing instruction processing across different stages (fetch, decode, execute, and write-back).
  - **Data and Instruction Cache Modules** (`dcache`, `prefetch`, `dblfetch`, `pffifo`, and `pfcache`): These modules manage the memory access patterns for data and instruction caches. The `zipwb` module handles the control signals to fetch instructions from the instruction cache efficiently or to access data from the data cache as needed.
  - **Bus Arbiter** (`wbdblpriarb`): Provides arbitration logic between prefetch and execution requests on the Wishbone bus to ensure that only one operation accesses the bus at a time.

#### Key Signals:
- **Inputs:**
  - `i_clk`: Clock input for synchronous operations.
  - `i_reset`: Asynchronous reset signal for initializing the module.
  - `i_interrupt`: Interrupt signal for handling asynchronous events.
  - `i_cpu_clken`: Clock enable signal for the CPU.
  - Several debug-related inputs (`i_halt`, `i_dbg_wreg`, `i_dbg_we`, `i_dbg_data`, etc.) which allow monitoring and control during operation.

- **Outputs:**
  - `o_wb_gbl_cyc`, `o_wb_gbl_stb`, `o_wb_lcl_cyc`, `o_wb_lcl_stb`: Control signals for the Wishbone bus indicating global or local access cycles and strobe signals.
  - `o_dbg_stall`, `o_halted`: Debug outputs representing pipeline stall conditions and whether the CPU is halted.
  - `o_op_stall`, `o_pf_stall`: Outputs that convey the status of the operational stalls affecting instruction fetch and execution.

#### Behavior of the Module:
- The `zipwb` module operates in a pipelined fashion, allowing multiple instruction processing stages (fetch, decode, execute, write-back) to occur concurrently. It utilizes control signals (`_ce`, `_stall`, `_valid`) to manage the flow of instructions and data.
- Each stage of the pipeline generates a `valid` signal to indicate valid data at that stage. The `stall` signals indicate if the pipeline must pause due to hazards (e.g., waiting for data).
- The module integrates instruction and data fetch controls, handling requests to the memory. It may switch between different strategies for prefetching instructions based on the configuration (single cache, double cache, FIFO, or cache).
- Clock gating is employed to reduce power consumption when the CPU is idle or in a debug state by controlling the clock to the core.

In summary, `zipwb.v` is a vital component of the Zip CPU, managing instruction flow and memory access while coordinating with various subsystems to maintain efficient operation within a pipelined processing architecture.

### File: axipipe.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/axipipe.v
### Description of the `axipipe` Module in Verilog

#### Overall Purpose
The `axipipe.v` file implements a memory unit designed to support a CPU architecture based on the AXI-lite protocol. Its primary purpose is to facilitate memory transactions by allowing multiple requests to be outstanding concurrently, thus improving throughput and efficiency in accessing memory. This is crucial for a system aiming for high performance, especially in scenarios where latency needs to be minimized while servicing multiple requests.

#### Inter-module Relationships
The `axipipe` module interacts with several other components within the CPU architecture:
- **CPU Interface:** It communicates directly with the CPU, receiving instructions related to memory operations (such as read and write requests) and sending back results or error statuses.
- **AXI Bus Interface:** The module serves as an intermediary between the CPU and the AXI bus, translating CPU-level requests into AXI transactions and managing the timing and sequencing of these transactions.
- **FIFO Buffers:** It utilizes internal FIFO structures to manage read and write operations efficiently, keeping track of outstanding transactions and ensuring proper order and alignment.
- **Control Logic:** The module's behavior is contingent upon various control signals, which determine how it responds to requests and what transactions are in progress.

#### Key Signals
**Inputs:**
- `S_AXI_ACLK` and `S_AXI_ARESETN`: Clock and reset signals for synchronizing AXI transactions.
- `i_cpu_reset`: A CPU reset signal that initializes the module's state.
- `i_stb`: A signal indicating that a valid request is being sent from the CPU.
- `i_lock`, `i_op`, `i_addr`, `i_data`, `i_oreg`: Various control signals that provide the operation type, address, data, and register information for memory transactions.

**Outputs:**
- `o_busy`: Indicates whether the AXI bus is currently processing a transaction.
- `o_pipe_stalled`: Shows if the internal pipeline is stalled, often due to waiting for a response from the AXI bus.
- `o_valid`: Signals that a valid response is available for the CPU.
- `o_err`: Indicates any error conditions that occurred during transaction processing.
- `o_wreg`: The register address to which data is written if applicable.
- `o_result`: Contains the result of a read operation.

#### Behavior of the Module
The `axipipe` module employs a complex control structure and state machine logic to manage its function:
1. **Transaction Management:** It evaluates input signals to determine when to initiate a transaction on the AXI bus, transitioning through states for address and data phases, and handling both read and write operations.
2. **Lock Management**: The module can support acquiring locks on transactions, which is essential for ensuring consistent access to resources in a multi-threaded environment.
3. **Alignment Checks**: The module checks for data alignment issues based on the defined AXI protocol specifications, generating errors for misaligned requests according to configuration options. 
4. **Response Handling**: It manages the response from the AXI bus, determining whether the operation was successful or if an error has occurred, and then propagating this information back to the CPU.
5. **Pipelining**: Through use of FIFOs and flags for operation control, the `axipipe` module can handle multiple outstanding transactions, thus optimizing memory access patterns and improving overall system efficiency.

The `axipipe` module exemplifies a critical component of a well-structured CPU design, ensuring rapid and efficient communication between the processing core and memory resources while adhering to established bus protocols.

### File: pipefetch.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/pipefetch.v
### Overall Purpose of the File

The `pipefetch.v` file implements an instruction fetch module for the Zip CPU architecture, designed to efficiently supply the CPU with instructions without stalling. The module utilizes pipelining to access the memory bus and caches instructions to improve performance by mitigating latency associated with memory reads. This allows the CPU to continue executing instructions while fetching the next instruction in the background.

### Inter-Module Relationships

The `pipefetch` module interacts with several components of the CPU architecture:

1. **Memory Interface (Wishbone Bus)**: The `pipefetch` module communicates with the memory subsystem using the Wishbone bus protocol, issuing read requests and handling acknowledgments, stalls, and errors.
   
2. **`ffetch` Module**: It works together with the `ffetch` module (mentioned at the end of the provided code). The latter serves as a higher-level instruction fetch controller, taking in inputs from the `pipefetch` module (valid instruction output, computed program counter, etc.) and exposing a CPU-friendly interface for instruction execution.

3. **Control Logic**: The `pipefetch` relies on various input signals to modify its state and behavior, including reset signals, boundaries for cache use, and signals indicating when it should clear the cache.

### Key Signals (Inputs/Outputs)

#### Inputs:

- `i_clk`: Clock signal.
- `i_reset`: Reset signal, initializing the module.
- `i_new_pc`: Signal indicating that a new program counter is available.
- `i_clear_cache`: Signal to clear the instruction cache.
- `i_stall_n`: Indicates if the CPU is ready (not stalled).
- `i_pc`: Current program counter value (input for instruction fetch).
- `i_wb_stall`, `i_wb_ack`, `i_wb_err`, `i_wb_data`, `i_wb_request`: Signals from the memory interface (Wishbone) for bus control and status.

#### Outputs:

- `o_i`: Output instruction fetched from the cache.
- `o_pc`: Output program counter corresponding to the fetched instruction.
- `o_v`: Indicates if the fetched instruction is valid.
- `o_wb_cyc`, `o_wb_stb`, `o_wb_we`, `o_wb_addr`, `o_wb_data`: Control signals for the Wishbone bus.
- `o_illegal`: Signal indicating if the retrieved instruction was illegal.

### Behavior of the Module

The behavior of the `pipefetch` module can be described through the following components:

1. **Caching Mechanism**: 
    - Uses a cache to hold recently fetched instructions, enabling quicker access without waiting for slower memory reads.
    - It maintains a count (`r_nvalid`) of valid cache entries, which dictates when new requests to the memory are necessary.

2. **State Management**:
    - The module maintains states regarding instruction fetching and cache management, with a primary state of whether it is currently engaged in a memory transaction (`o_wb_cyc`).
    - The cache’s base address and the valid entries are updated as new instructions are fetched from the memory.

3. **Bus Transaction Logic**:
    - Implements control logic to manage bus requests based on whether the instruction cache is valid, if new instructions need to be fetched (due to program counter changes), or if there is a stall on the Wishbone bus.
    - Incorporates checks for out-of-bounds access or errors from the bus and resets the cache state as necessary.

4. **Read and Write Logic**:
    - When valid instructions are available, it outputs them via `o_i` and keeps track of the current program counter through `o_pc`. 
    - The cached instruction can be updated based on bus acknowledgment signals (`i_wb_ack`) once an instruction fetch completes.

5. **Error Handling**:
    - Monitors for illegal instructions with an internal mechanism to flag invalid instruction reads based on responses from the memory (e.g., if a bus error occurs).

The combination of these functions promotes efficient instruction fetching for the CPU, allowing it to keep processing without delays associated with memory access.

### File: pfcache.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/pfcache.v
### Overall Purpose of the File
The `pfcache.v` file implements the instruction prefetch cache logic for the Zip CPU, a lightweight RISC CPU architecture. Its primary purpose is to maintain an efficient flow of instructions to the CPU pipeline by caching instructions fetched from memory, ensuring that the CPU receives one instruction per clock cycle while minimizing stalls. The logic also allows for the invalidation and clearing of cache entries when necessary, thus supporting effective instruction fetching under various conditions.

### Inter-module Relationships
The `pfcache` module interacts closely with various components of the Zip CPU architecture:

- **Instruction Fetch Unit**: It works in conjunction with the instruction fetch logic to retrieve instructions based on the current program counter (PC). It uses its output to indicate the validity of the fetched instruction.
- **Memory Subsystem**: The module interfaces with a memory bus (wishbone bus) to read from external memory when cache misses occur. It sends requests for instructions and receives data through this bus.
- **Control Logic**: The signals `i_new_pc` and `i_clear_cache` can modify fetching behaviors, indicating when a new PC is available or when the cache should be cleared.

Overall, the `pfcache` serves as an intermediary between the CPU's instruction pipeline and the memory subsystem, ensuring that instruction fetching is optimized.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_clk`: The clock signal for synchronization.
  - `i_reset`: Resets the state of the module.
  - `i_new_pc`: Indicates a new program counter has been provided to the cache.
  - `i_clear_cache`: Command to clear the contents of the cache.
  - `i_ready`: A signal indicating that the CPU is ready for the fetched instruction.
  - `i_pc`: The current program counter that indicates the address of the instruction to fetch.
  - `i_wb_stall`, `i_wb_ack`, `i_wb_err`, `i_wb_data`: Signals from the wishbone bus interface indicating the state of memory operations.

- **Outputs**:
  - `o_valid`: Indicates whether the fetched instruction is valid.
  - `o_illegal`: Signals if an illegal memory access occurred during fetching.
  - `o_insn`: The fetched instruction.
  - `o_pc`: The associated program counter.
  - `o_wb_cyc`: Control signal for the wishbone bus cycle.
  - `o_wb_stb`: Strobe signal for initiating transfers on the wishbone bus.
  - `o_wb_addr`: Address bus for the wishbone interface.
  - `o_wb_data`: Data to be written to the bus (not used in this module; always zero).

### Behavior of the Module
The `pfcache` module implements a state machine to manage fetching behaviors, including cache hits and misses, fetching from memory, and invalidating the cache when necessary. Key operational details include:

- **Fetching Logic**: The module tracks two potential addresses for fetching: the current `i_pc` and the stored `lastpc`. This allows it to handle branches and ensure valid instructions are delivered.
- **Control Flows**: A series of control signals dictate whether to read from the cache or initiate a fetch from memory. The cache is checked for validity using tag checks on the inputs.
- **State Management**: It utilizes state variables to keep track of cache line readiness and memory communication statuses (e.g., waiting for bus acknowledgments, cache loading).
- **Invalidation Logic**: The module can invalidate cache entries based on bus errors or reset commands.
- **Delay Cycles**: The logic includes mechanisms for handling delays when the CPU is stalled or when waiting for bus acknowledgments, ensuring seamless operation despite varying latencies.

The combination of these behaviors enables the `pfcache` module to fulfill its role in the CPU architecture effectively, striving for high performance and low latency in instruction fetching.

### File: dcache.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/dcache.v
### Overview of `dcache.v`

#### Purpose
The `dcache.v` file implements a simple data cache for the ZipCPU architecture. This module is designed to enhance the efficiency of data access by enabling single-cycle read access from the last cached memory line and two-cycle access for data that is currently in the cache. The primary goal is to serve as a drop-in replacement for the existing `pipemem` memory unit within the ZipCPU, providing faster access times for cached data and managing cache coherence through reads and writes to the bus.

#### Inter-module Relationships
- **CPU Interface**: `dcache` receives inputs from the CPU (such as request signals, operation codes, addresses, and data) and provides outputs back to the CPU, including read data, busy status, and error flags.
- **Wishbone Bus Interface**: It interacts with the Wishbone bus as a master device, driving read/write cycles and acknowledging operations through signals like `o_wb_stb`, `o_wb_we`, `o_wb_addr`, etc.
- **Other Cache Management Modules**: It collaborates with additional modules like `iscachable` to determine whether a memory address is cacheable. It retrieves and stores cache line tags and data, managing cache entry validity through various internal registers.

#### Key Signals
- **Inputs**:
  - `i_clk`: Clock signal.
  - `i_reset`: Reset signal to initialize the state.
  - `i_clear`: Signal to clear the cache.
  - `i_pipe_stb`: Valid signal indicating a new instruction.
  - `i_lock`: Lock signal for memory operations.
  - `i_op[2:0]`: Operation code (read/write).
  - `i_addr`: Address to read from or write to.
  - `i_data`: Data to be written to memory.
  - `i_oreg`: Auxiliary register data (such as destination register).

- **Outputs**:
  - `o_busy`: Indicates whether the cache is currently processing a request.
  - `o_rdbusy`: Indicates read operation status.
  - `o_pipe_stalled`: Indicates if the pipeline is stalled.
  - `o_valid`: Shows if the output data is valid.
  - `o_err`: Error flag indicating a problem with a transaction.
  - `o_wreg`: Indicates the register to write to on a successful operation.
  - `o_data`: The data read from the memory.

#### Behavior of the Module
The `dcache` module operates based on a state machine that manages various states such as idle, read, and write operations:

1. **State Machine**: The module has a primary control state machine that handles transitions between states based on inputs and internal conditions.
   - **DC_IDLE**: The default state, waiting for requests.
   - **DC_WRITE**: Processes write operations, asserting write enables and updating cache entries as necessary. It checks cachability and manages data consistency with the global state.
   - **DC_READC**: Handles reading cache lines and manages data bus transactions, ensuring proper tracking of cache lines.
   - **DC_READS**: Deals with non-cacheable reads, issuing appropriate bus transactions, and setting signals to alert the CPU.

2. **Control Logic**: The module utilizes several internal flags and registers to keep track of cache state, pending operations, validity of addresses, and the status of transactions on the memory bus. It checks whether a requested address is cacheable and if it is present in the cache, directing valid cache hits to quick paths for data retrieval.

3. **Error Handling**: It incorporates mechanisms for handling errors that arise during read/write operations, updating internal error signals for the CPU to monitor.

4. **Behavior During Clock Cycles**: The cache operates on a clock cycle basis, where procedural blocks update the state and outputs based on the clock's rising edge, maintaining synchronous behavior in response to CPU requests and bus signals.

In summary, the `dcache.v` file effectively implements a data cache for the ZipCPU architecture, describing control logic that interacts with both the CPU and Wishbone bus, enabling efficient read/write operations while managing state and data integrity effectively.

### File: memops.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/core/memops.v
### Description of `memops.v`

#### Overall Purpose
The `memops.v` file implements a memory operator for a lightweight RISC CPU, providing support for memory read and write operations. It handles both global and local memory transactions, as well as managing alignment and bus locking features within the CPU architecture. The design emphasizes simplicity and potentially undefined behavior if successive memory commands are issued before completion of prior transactions.

#### Inter-module Relationships
The `memops` module interacts primarily with two other critical components in the CPU architecture:
1. **CPU Interface:** It communicates with the CPU components through input signals (like `i_stb`, `i_op`, `i_addr`, etc.) and outputs signals to the CPU (`o_busy`, `o_valid`, `o_err`, `o_result`, etc.). It essentially acts as the medium for data passing between the CPU and memory subsystem.
2. **Wishbone Interface:** The module interfaces with Wishbone bus signals, issuing control commands for memory operations (defined in output signals such as `o_wb_stb_gbl`, `o_wb_stb_lcl`, etc.) and handling incoming responses (like `i_wb_ack`, `i_wb_err`, `i_wb_data`). 

#### Key Signals
- **Inputs:**
  - `i_clk`: Clock signal.
  - `i_reset`: Reset signal.
  - `i_stb`: Indicates a valid memory access request from the CPU.
  - `i_lock`: Lock signal for transaction control.
  - `i_op`: Operation type (read/write).
  - `i_addr`: Memory address for the operation.
  - `i_data`: Data to be written for write operations.
  - `i_oreg`: Register index for the CPU's register file.

- **Outputs:**
  - `o_busy`: Indicates if the memory operator is currently busy with a transaction.
  - `o_valid`: Indicates a valid read result back to the CPU.
  - `o_err`: Error signal to indicate any issues during the operation.
  - `o_wreg`: Register index to be written with the result.
  - `o_result`: Data result being sent back to the CPU.
  - `o_wb_cyc_gbl`, `o_wb_cyc_lcl`: Control signals indicating ongoing transactions on global or local Wishbone buses.
  - `o_wb_stb_gbl`, `o_wb_stb_lcl`: Strobe signals for initiating a transaction on the respective Wishbone buses.

#### Behavior of the Module
The `memops` module has a combination of combinatorial and sequential logic to handle memory operations:

1. **Instruction Handling and Address Alignment:** It checks the alignment of addresses in accordance with operation types (e.g., word, halfword) using generated logic to prevent misaligned accesses if the corresponding feature is enabled (controlled by `OPT_ALIGNMENT_ERR`).

2. **State Management for Transactions:** The module uses registers to track ongoing transactions. When a memory request (`i_stb`) is valid, it enables the appropriate Wishbone signals (like `o_wb_stb_gbl` or `o_wb_stb_lcl`) for memory access.

3. **Response Handling:** It awaits acknowledgment from the memory subsystem (through `i_wb_ack`), updating output signals accordingly to indicate successful transactions or errors.

4. **Control Logic for Read and Write Operations:** The module encapsulates the control logic to set up write data (`o_wb_data`), select lines (`o_wb_sel`), and drive the operation types (read/write) based on the incoming CPU request.

5. **Locking Mechanism:** If enabled, the module manages locking between transactions, ensuring coherent access to shared memory resources.

6. **Error Management and Validity Signals:** It generates error signals on misalignment or transaction errors, ensuring that the CPU receives accurate feedback and status indication of memory operations.

The `memops` module is inherently designed to ensure that the CPU interacts with memory efficiently while maintaining consistency and correctness in operations, leveraging robust control mechanisms for state management and error checking.

### File: wbpriarbiter.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/wbpriarbiter.v
### Overall Purpose of `wbpriarbiter.v`

The `wbpriarbiter.v` file implements a priority bus arbiter for the Zip CPU architecture. This module enables two separate Wishbone masters (designated as Bus A and Bus B) to access a shared bus. Its primary goal is to ensure that one master can have immediate access to the bus without delay when the other master is not using it. This priority arbitration reduces the need for complex combinatorial logic while ensuring deterministic access times for the higher-priority master.

### Inter-module Relationships

The `wbpriarbiter` module has strong inter-module relationships within the Zip CPU architecture:

1. **Bus Masters**: It interfaces with two master modules (referred to as Bus A and Bus B). Each of these masters can request access to the bus through their respective signals. The arbiter grants access based on predefined logic.
  
2. **Outgoing Bus Interface**: The arbiter's outputs (`o_cyc`, `o_stb`, `o_we`, etc.) are directly connected to the bus that communicates with downstream slave devices or modules in the CPU system. The arbiter thus acts as a mediator between the bus masters and the shared bus.

3. **Slave Modules**: The arbiter interacts with slave modules (not fully specified in this file) via the signals (`i_ack`, `i_stall`, `i_err`) that handle acknowledgments and handshakes required for bus transactions.

4. **Formal Verification Modules**: There are built-in formal verification assertions within the module that reference and interact with theoretical bus master and slave models, ensuring that the arbiter behaves correctly under various conditions.

### Key Signals (Inputs/Outputs)

**Inputs:**
- `i_clk`: The system clock input.
- Bus A control signals: 
  - `i_a_cyc`: Indicates if Bus A wants to access the bus.
  - `i_a_stb`: Strobe signal for Bus A.
  - `i_a_we`: Write enable signal for Bus A.
  - `i_a_adr`: Address bus for Bus A.
  - `i_a_dat`: Data bus for Bus A.
  - `i_a_sel`: Byte select signals for Bus A.
- Bus B control signals:
  - `i_b_cyc`: Represents access request status for Bus B.
  - `i_b_stb`: Strobe signal for Bus B.
  - `i_b_we`: Write enable signal for Bus B.
  - `i_b_adr`, `i_b_dat`, `i_b_sel`: Same functions as their A counterparts.

**Outputs:**
- Bus control signals:
  - `o_cyc`, `o_stb`, `o_we`: Combined cyc, strobe, and write enable signals indicating ownership of the bus.
  - `o_adr`, `o_dat`, `o_sel`: Multiplexer outputs for the address, data, and select lines based on bus ownership.
- Acknowledgement and stall signals for both buses:
  - `o_a_ack`, `o_a_stall`, `o_a_err`: Acknowledgment, stall, and error signals for Bus A.
  - `o_b_ack`, `o_b_stall`, `o_b_err`: Acknowledgment, stall, and error signals for Bus B.

### Behavior of the Module

The behavior of the `wbpriarbiter` module includes:

1. **Ownership Management**: A state (`r_a_owner`) determines which of the two masters currently owns the bus. If neither master is requesting access, ownership defaults to Bus A.

2. **Bus Access Control Logic**:
   - If Bus A asserts its control signals, it is immediately granted bus access.
   - If both buses request access, and Bus B asserts its `cyc` signal while Bus A does not, Bus B is allowed access.
   - Bus ownership is dynamically changed based on the status of the control signals.

3. **Signal Routing**: During bus ownership:
   - The output signals (address, data, and select) are derived either from Bus A or Bus B, based on which master currently owns the bus.
   
4. **Acknowledgement and Stall Logic**: 
   - Acknowledgment and errors are routed back to the respective bus based on the current owner of the bus.
   - Stall signals are used to control the flow when the bus is busy, ensuring that the requesting bus is informed about the status of the operation.

5. **Low Power Logic Option**: An option (`OPT_ZERO_ON_IDLE`) allows the design to drive bus lines to zero state when idle, potentially reducing power consumption at the cost of additional logic.

6. **Formal Verification Logic**: The module contains formal properties that check the correctness of the arbitration logic, ensuring that requests and acknowledgments behave as expected throughout its operation.

Overall, the `wbpriarbiter` module is crucial for managing bus access efficiently and ensuring predictable behavior in the context of the Zip CPU architecture.

### File: busdelay.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/busdelay.v
### Purpose of the File

The `busdelay.v` file implements a module designed to manage access to a Wishbone bus with a delay mechanism. This is particularly relevant in high-speed CPU designs where timing issues may arise. The module can delay access to the bus by a clock cycle, which helps ensure that data conflicts and timing violations do not occur during the bus interaction process. It is intended to alleviate timing problems that can be encountered when operating at higher frequencies by temporarily holding bus requests.

### Inter-Module Relationships

The `busdelay.v` module interacts with other parts of the CPU architecture as follows:

1. **Wishbone Bus Interface:** It serves as a bridge between a Wishbone master (e.g., CPU, device) and a Wishbone slave (e.g., memory or peripheral device). The input signals from the master and output signals toward the slave indicate control and data signals that are passed through the bus.

2. **Stalling Mechanism:** The module incorporates a stalling mechanism to ensure the Wishbone master is informed correctly when the bus is busy. It takes care of signals involving bus cycles, acknowledge signals, error flags, and data paths, ensuring the correct handling of these states as they propagate through the system.

3. **Flexible Delay Options:** There are parameters like `DELAY_STALL` that enable the designer to choose whether or not to include the stall delay logic, thus providing options for optimizing the design based on specific use cases.

### Key Signals (Inputs/Outputs)

- **Inputs:**
  - `i_clk`: Clock signal to synchronize the operation of the module.
  - `i_reset`: Asynchronous reset to reset the module's state.
  - `i_wb_cyc`: Signal indicating that a Wishbone cycle is in progress.
  - `i_wb_stb`: Strobe signal to indicate valid bus transactions.
  - `i_wb_we`: Write enable signal indicating the direction of data transfer (read/write).
  - `i_wb_addr`: The address for the transaction.
  - `i_wb_data`: Data input from the master for write operations.
  - `i_wb_sel`: Select signal for byte lanes.
  - `i_dly_stall`: Input signal indicating the delayed stall condition.
  - `i_dly_ack`: Acknowledge signal from the delayed bus target.
  - `i_dly_data`: Data input from the delayed bus target.
  - `i_dly_err`: Error signal from the delayed bus target.

- **Outputs:**
  - `o_wb_stall`: Stall signal indicating the master bus should wait.
  - `o_wb_ack`: Acknowledge signal for the master.
  - `o_wb_data`: Data output to the master.
  - `o_wb_err`: Error status output.
  - `o_dly_cyc`: Indicates that the delayed bus is in a cycle.
  - `o_dly_stb`: Strobe signal for the delayed bus transaction.
  - `o_dly_we`: Write enable signal for the delayed bus.
  - `o_dly_addr`: The address for transactions on the delayed bus.
  - `o_dly_data`: Data output to the delayed bus target.
  - `o_dly_sel`: Select signal for the delayed bus byte lanes.

### Behavioral Description

The behavior of the `busdelay` module can be broken down into several key characteristics:

1. **Delayed Operation:** The primary behavior is to introduce a delay in processing bus transactions. When input conditions are met, it triggers delayed outputs for the bus cycle (e.g., `o_dly_cyc`, `o_dly_stb`, etc.), meaning that it holds the signals for one clock cycle before they are sent to the downstream slave module.

2. **Control Logic:** The module maintains state through control logic that determines when to process requests and how to respond to various conditions:
   - If a reset occurs (`i_reset`), all internal states are reset.
   - If a bus error occurs (`o_wb_err`), the output signals are modified accordingly.
   - The logic uses `always` blocks sensitive to clock edges and the reset state to synchronize operations correctly.

3. **Handling Stall Conditions:** The module accurately tracks conditions under which the bus should stall or continue, determined by signals like `o_wb_stall` and the delayed bus's state. 

4. **Flexibility with Parameters:** Parameters such as `DELAY_STALL` and `OPT_LOWPOWER` allow designers to tweak the behavior of the module based on specific needs such as performance versus resource efficiency.

5. **Formality Assertions:** Formal verification blocks are included to ensure that the operation of the bus delay meets certain correctness properties, which allow for confirming the expected behavior through simulation or other formal methods.

In summary, the `busdelay.v` module is crucial for managing bus interactions in a CPU/system design, particularly under conditions that require tight timing control or when optimizing for specific resource constraints.

### File: fwb_master.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/fwb_master.v
### Purpose of the File
The Verilog file `fwb_master.v` implements a formal verification model for a Wishbone master interface within the Zip CPU architecture. Its primary purpose is to define the rules governing the interactions of a Wishbone master with the bus, ensuring that the master complies with protocol specifications during transactions. Notably, this file contains no functional logic; it serves as a basis for proving through formal verification that the master correctly handles outgoing requests and incoming responses, specifically focusing on request handling, acknowledgment receipt, and error management.

### Inter-module Relationships
The `fwb_master` module interacts directly with Wishbone slave modules and the broader CPU architecture through the Wishbone bus protocol. It does not control any functional operations or data transfers but instead focuses on ensuring compliance with the bus protocol requirements. The module's design allows it to be used in conjunction with a corresponding `formal_slave.v` module, establishing a framework for comparative formal verification. The usage of macros (`SLAVE_ASSUME`, `SLAVE_ASSERT`) allows for a defined interface for validating assumptions and assertions concerning bus interactions, facilitating a systematic method for verifying correct functionality across the entire Wishbone bus interface.

### Key Signals
**Inputs:**
- `i_clk`: The clock signal driving the module.
- `i_reset`: A reset signal to initialize the module state.
- `i_wb_cyc`: Indicates the cycle (CYC) status of the Wishbone bus.
- `i_wb_stb`: Indicates the strobe (STB) status of the Wishbone bus.
- `i_wb_we`: Indicates write (WE) operation status.
- `i_wb_addr`: The address signal for the Wishbone transaction.
- `i_wb_data`: The data signal for the Wishbone transaction.
- `i_wb_sel`: The byte selection signal.
- `i_wb_ack`: Acknowledge signal from the slave.
- `i_wb_stall`: Stall signal indicating whether the slave can accept transactions.
- `i_wb_idata`: Data signal returning from the slave.
- `i_wb_err`: Error signal from the slave.

**Outputs:**
- `f_nreqs`: A counter for the number of requests initiated by the master.
- `f_nacks`: A counter for the number of acknowledgments received.
- `f_outstanding`: A signal indicating the number of outstanding requests that have not yet been acknowledged.

### Behavior of the Module
The `fwb_master` module operates under several key behavioral constructs that enforce the rules for proper Wishbone master functioning:

1. **Reset and Initial State Management**: The module ensures that upon reset, both `CYC` and `STB` are low, and that no acknowledgments or errors are active.

2. **Request and Acknowledgment Management**: The module tracks request counts (`f_nreqs`) and acknowledgment counts (`f_nacks`), managing the state of outstanding requests. It ensures that requests can only be made when the `CYC` signal is active and that the behavior when `CYC` is low follows appropriate protocol rules.

3. **Bus Transaction Rules**: It asserts that the `STB` signal can only be high when `CYC` is high and verifies the directionality of requests (read/write) remains consistent throughout the transaction.

4. **Error Handling**: In the event of an error, the module ensures that the `CYC` line is dropped, consistent with the expected behavior of Wishbone masters following a transaction failure.

5. **Stalling Management**: The module manages stall counts, ensuring that the slave’s response does not exceed specified thresholds through defined parameters.

6. **Formal Assertions**: Throughout the module, formal verification assertions are embedded using macros to validate the state and behavior of signals and parameters dynamically, allowing a proving tool to check for compliance with the expected Wishbone protocol behavior.

This module establishes a framework for ensuring that Wishbone master interfaces adhere to specified operational behaviors in a formal verification context, enriching the robustness and reliability of the underlying CPU architecture.

### File: fwb_slave.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/fwb_slave.v
### Overview of `fwb_slave.v`

#### Purpose
The `fwb_slave.v` file is part of the Zip CPU architecture and defines a formal verification model for a Wishbone (WB) slave interface. This module outlines the expected behavior of a slave device interacting with a Wishbone master, ensuring that the slave adheres to proper communication protocols and handle requests and responses correctly. The primary intent of this module is to facilitate formal verification through assertions and assumptions about the various state transitions and signal behaviors, ensuring that the implemented logic behaves as expected.

#### Inter-Module Relationships
The `fwb_slave` module interacts with the following components:
- **Wishbone Master Module:** As a slave, it receives requests from a Wishbone master. The assumptions specified in this module describe how it should handle inputs, which are generated by the master.
- **Formal Verification Tooling (e.g., Yosys-SMTBMC):** The module includes assertions for formal verification tools that check compliance with the Wishbone protocol. This enables the validation of the slave's responses to requests without implementing functional logic.

This `fwb_slave` module does not directly implement any functional logic. Instead, it serves to formally verify that any master interacting with it behaves according to the design specifications.

#### Key Signals
**Inputs:**
- `i_clk`: Clock signal for synchronous behavior.
- `i_reset`: Active high reset signal for initialization.
- `i_wb_cyc`: Indicates if a transaction is currently active (valid bus cycle).
- `i_wb_stb`: Indicates if a data request is valid (strobe signal).
- `i_wb_we`: Indicates whether the current operation is a write (1) or read (0).
- `i_wb_addr`: The address of the data that is being read or written.
- `i_wb_data`: The data that is being written (only valid for write operations).
- `i_wb_sel`: The byte enable signal indicating which bytes are being accessed.

**Outputs:**
- `f_nreqs`: A register counting the number of requests received.
- `f_nacks`: A register counting the acknowledgments received.
- `f_outstanding`: Indicates the number of requests that are currently outstanding (not yet acknowledged).
- `i_wb_ack`: Acknowledgment signal from the slave, indicating successful reception of a request.
- `i_wb_stall`: Indicates that the slave is not currently ready to process requests.
- `i_wb_idata`: Data returned to the master in response to a read request.
- `i_wb_err`: Error signal indicating a fault in transmission.

The outputs are primarily monitoring variables meant for asserting the correctness of the operations performed within the slave interface under formal verification conditions.

#### Behavior
The `fwb_slave` does not perform any actual data processing; rather, it focuses on:
- **State Validation:** The module uses several assertion statements to ensure that the signals adhere to the expected behavior based on various states of the Wishbone protocol. For instance, it ensures that an acknowledgement (`o_wb_ack`) cannot occur without a corresponding request, and it maintains consistency in input signals across clock cycles.
- **Stall and Delay Management:** It keeps track of how long requests can be stalled and ensures that there are limits to how long the slave can delay responses after receiving requests. This is implemented with parameters such as `F_MAX_STALL` and `F_MAX_ACK_DELAY`, which dictate how many cycles are permissible for stalling in response to a request.
- **Request and Acknowledge Counting:** The module maintains counters (`f_nreqs` for requests and `f_nacks` for acknowledgments) to precisely track the flow of communication, thus enabling the validation of the number of outstanding operations.

By employing these assertions and checks, the `fwb_slave` module provides a foundation for formally verifying behavior in the rest of the Zip CPU implementation, ensuring that all interactions comply with the expected protocol while seamlessly integrating into the broader architecture of the CPU.

### File: skidbuffer.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/skidbuffer.v
### Purpose of the File
The `skidbuffer.v` file implements a skid buffer, which is essential for creating high-throughput AXI (Advanced eXtensible Interface) compliant components in digital circuits. The skid buffer helps manage data flow when there are stall conditions—when output needs to wait for input due to timing mismatches. It averts data loss by temporarily storing incoming data until it can be processed, which is important in robust, high-speed designs like the Zip CPU.

### Inter-module Relationships
The skid buffer interacts with bus interfaces by controlling the data flow through the AXI interface. It connects the input signals (`i_valid`, `i_data`, and `i_ready`) representing incoming data validity, the actual data, and readiness to receive new data, respectively, to the corresponding outputs (`o_valid`, `o_data`, and `o_ready`) for the bus interface. It operates as a bridge that can either allow data to pass directly through (in passthrough mode) or buffer it (in normal operation mode). This behavior is critical for ensuring the AXI protocol's requirements are met, especially the registration of outputs.

### Key Signals
- **Inputs:**
  - `i_clk`: Clock signal, synchronizing operations.
  - `i_reset`: Asynchronous reset signal to initialize the buffer.
  - `i_valid`: Indicates valid incoming data is available.
  - `i_data`: The actual data payload being transferred.
  - `i_ready`: Signal indicating that the downstream module is ready to accept data.

- **Outputs:**
  - `o_ready`: Indicates readiness to accept new valid data.
  - `o_valid`: Indicates that the output data is valid.
  - `o_data`: The buffered output data, delivering either the incoming data or data from the skid buffer.

### Behavior of the Module
1. **Control Logic**: The skid buffer includes logic to handle data based on the `i_valid`, `i_ready`, `o_valid`, and `o_ready` signals:
   - When the incoming side indicates valid data (`i_valid`) and the output is ready (`o_ready`), the buffer can pass `i_data` to the output directly.
   - If the output is not ready (i.e., the module downstream cannot accept the new data), the skid buffer temporarily holds the data in an internal register (`r_data`), and the `r_valid` flag is set to indicate there is valid data stored.

2. **State Management**: The module features state-based behavior using different registers (`r_valid`, `r_data`, etc.):
   - The `r_valid` flag shows whether there is valid data present in the skid buffer.
   - The internal data register (`r_data`) temporarily holds data as long as the output is not ready to consume it.
   - The output signals (`o_valid` and `o_data`) are driven based on the current state of valid data and ready signals, ensuring correct communication to the downstream interface.

3. **Configurable Parameters**: The skid buffer is designed to be highly configurable through parameters:
   - `DW`: Data width, allowing customization for different word sizes.
   - `OPT_LOWPOWER`: Controls low-power operation by avoiding unnecessary toggling of output signals when valid signals are low.
   - `OPT_OUTREG`: Defines whether the output should be registered or combinatorial.
   - `OPT_PASSTHROUGH`: When enabled, the module simulates a direct path for data, useful for formal verification.

Overall, the behavior of the skid buffer effectively manages data flow and buffering in the presence of stall conditions, maintaining compliance with the AXI specification and ensuring reliable data transfer within high-speed CPU designs like the Zip CPU.

### File: fwb_counter.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/fwb_counter.v
### Overall Purpose
The `fwb_counter.v` file implements a counter specifically designed for managing the transactions on the Wishbone bus within the Zip CPU architecture. Its primary role is to handle the counting of outstanding requests and acknowledgments. This module ensures that the bus protocol adheres to the expected behavior in terms of request handling and acknowledgment signaling.

### Inter-module Relationships
The `fwb_counter` module interacts with several other modules in the Zip CPU architecture, primarily through the Wishbone bus interface. It serves as a foundational component for any module that requires transaction management on the bus, and it is likely to be a part of a larger bus interface or memory controller. Other modules in the CPU, such as memory devices, peripheral controllers, or the main CPU core, would depend on `fwb_counter` to correctly track the number of outstanding requests and manage data flow over the bus. 

### Key Signals (Inputs/Outputs)
1. **Inputs:**
   - `i_clk`: The clock signal for synchronizing operations.
   - `i_reset`: Active signal to reset the counter values.
   - `i_wb_cyc`: Indicates whether a bus cycle is active.
   - `i_wb_stb`: Indicates that a request is valid.
   - `i_wb_we`: Indicates whether the operation is a write (1) or read (0).
   - `i_wb_addr`: Address for the bus transaction.
   - `i_wb_data`: Data to be written (if `i_wb_we` is active).
   - `i_wb_sel`: Indicates which bytes of the data are valid.
   - `i_wb_ack`: Acknowledgment signal from the Wishbone slave indicating the request was processed.
   - `i_wb_stall`: Indicates that the bus is stalled and not ready to process requests.
   - `i_wb_idata`: Data read from the Wishbone slave.
   - `i_wb_err`: Error flag indicating that the request encountered an error.

2. **Outputs:**
   - `f_nreqs`: Counts the number of requests sent by the master.
   - `f_nacks`: Counts the number of acknowledgments received.
   - `f_outstanding`: Represents the current number of outstanding requests, calculated as the difference between requests and acknowledgments.

### Behavior of the Module
The `fwb_counter` module functions primarily through the use of sequential logic based on the clock signal (`i_clk`). Key behaviors include:

- **Request Counting**: The module initializes the count of requests (`f_nreqs`) to zero and increments this count whenever a valid request is made (`i_wb_stb` is high and `i_wb_stall` is low). If a reset occurs or if the bus cycle is inactive (`!i_wb_cyc`), the request count resets to zero.

- **Acknowledgment Counting**: Similarly, the module counts the number of acknowledgments (`f_nacks`). If a reset occurs, this count is also reset. The count increments when either an acknowledgment (`i_wb_ack`) or an error (`i_wb_err`) is received.

- **Outstanding Requests Calculation**: The number of outstanding requests (`f_outstanding`) is calculated as the difference between the number of requests and acknowledgments, active only during an active bus cycle (`i_wb_cyc`). If not active, `f_outstanding` resets to zero.

Overall, this module provides critical tracking of bus transactions, ensuring that the connection between the CPU and peripheral devices maintains a coherent state regarding request processing. Furthermore, the inclusion of parameters allows for configuration of maximum requests and stalls, thereby enabling flexibility and adaptation to different system designs or requirements.

### File: sfifo.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/sfifo.v
### Overall Purpose of the File
The file `sfifo.v` implements a synchronous data FIFO (First-In, First-Out) buffer. It's designed for efficient and orderly storage and retrieval of data, making it particularly useful in CPU architectures where temporary storage of data is required between different processing stages, such as during instruction execution or data handling.

### Inter-Module Relationships
The `sfifo` module interacts with various other modules in the CPU architecture by serving as a data buffering component. It can be integrated with:
- **Core Logic**: Providing data storage for instructions or data that need to be processed sequentially.
- **Execution Units**: Serving as an interface between data producers (such as ALUs or other processing units) and consumers (like memory or other pipeline stages).
- **Memory Interfaces**: It could manage data from memory reads/writes, buffering the data in situations where data throughput must be maintained in the event of slow memory accesses.

The FIFO's outputs can be used as inputs for other modules, taking advantage of its capacity to store data temporarily, thus helping smooth data flow in the overall architecture.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_clk`: The clock signal used to synchronize operations within the module.
  - `i_reset`: Used for resetting the FIFO state.
  - `i_wr`: Signal that indicates a write operation is requested.
  - `i_data`: The data input to be stored in the FIFO.
  - `i_rd`: Signal indicating a read operation is requested.

- **Outputs**:
  - `o_full`: Indicates if the FIFO is full and cannot accept more data.
  - `o_fill`: A register output (local) indicating how many items are currently stored in the FIFO.
  - `o_data`: The data output that provides the next item to be read from the FIFO.
  - `o_empty`: Indicates if the FIFO is empty and has no data to read.

### Behavior of the Module
The `sfifo` module employs control logic that manages the state of the FIFO through various stages:

1. **Write Logic**:
   - When `i_wr` is asserted and the FIFO is not full (`o_full` is low), data from `i_data` is written into the memory at the current write address (`wr_addr`), which increments with each successful write.
   - The module keeps track of how many items are in the FIFO using `o_fill`. It increases on a successful write and decreases when items are read.

2. **Read Logic**:
   - Similarly, when `i_rd` is asserted, and the FIFO is not empty (`o_empty` is low), it retrieves data from the memory at `rd_addr` and increments the read address for the next operation.
   - The `o_data` output provides the data read from FIFO. If the FIFO is empty and configured (`OPT_READ_ON_EMPTY`), it may output previously written data (`i_data`).

3. **Full/Empty Mechanics**: 
   - The module determines if it is full or empty based on the values of `wr_addr` and `rd_addr`. If the written addresses exceed the configured limits (`FLEN`), `o_full` is set. Conversely, it tracks when no data is left in FIFO using `o_empty`.

4. **Asynchronous Reads**:
   - The module can be configured to allow asynchronous reads in different ways (depending on the parameters). If enabled, the outputs can be driven directly from the memory content, allowing for greater flexibility in how data can be accessed.

5. **Formal Verification**:
   - The module incorporates assertions for formal verification that checks the integrity of its behavior and conditions, ensuring that its states hold true under various conditions and transitions.

Overall, `sfifo.v` provides a robust mechanism for buffered data flow within the CPU, supporting both write and read operations supplemented by control flags and conditions that prevent overflows or underflows in data handling.

### File: wbarbiter.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/wbarbiter.v
### Overview of `wbarbiter.v`

#### Purpose
The `wbarbiter.v` file implements a priority bus arbiter designed for the Zip CPU architecture. Its primary purpose is to manage access to a shared bus by two separate Wishbone masters (designated as A and B). The arbiter ensures that one master can gain exclusive access to the bus while minimizing the complexity and delay associated with bus access.

#### Inter-Module Relationships
The `wbarbiter` module interacts with other components of the CPU that require shared access to the bus. It connects two Wishbone interfaces (masters) to a single downstream bus, managing the arbitration between them. The following modules interact with `wbarbiter`:
- **Master A**: Provides control signals and data to `wbarbiter` which it uses to request bus access.
- **Master B**: Similar to Master A, but may contend with Master A for bus access.
- **Downstream Bus**: Represents the bus interface toward the memory or peripheral devices, receiving outputs from `wbarbiter`.

It also interacts with auxiliary components like `fwb_master` and `fwb_slave`, which manage the acknowledgment signals and request counts for formal verification.

#### Key Signals
- **Inputs:**
  - `i_clk`: Clock signal for synchronization.
  - `i_reset`: Reset signal to initialize the module.
  - `i_a_cyc`, `i_a_stb`, `i_a_we`, `i_a_adr`, `i_a_dat`, `i_a_sel`: Control signals and data from Master A.
  - `i_b_cyc`, `i_b_stb`, `i_b_we`, `i_b_adr`, `i_b_dat`, `i_b_sel`: Control signals and data from Master B.
  
- **Outputs:**
  - `o_cyc`: Signals the start of a bus cycle.
  - `o_stb`: Strobe signal indicating that data is valid on the bus.
  - `o_we`: Write enable signal, indicating that a write operation is occurring.
  - `o_adr`, `o_dat`, `o_sel`: Address, data, and select lines output to the bus.
  - `o_a_stall`, `o_a_ack`, `o_a_err`: Stall, acknowledgment, and error signals for Master A.
  - `o_b_stall`, `o_b_ack`, `o_b_err`: Stall, acknowledgment, and error signals for Master B.

#### Behavior
The `wbarbiter` operates by implementing state-driven arbitration that can follow different schemes: "ALTERNATING", "PRIORITY", or "LAST". The arbitration scheme determines which master receives bus access when both request access simultaneously. 

1. **Ownership Management**: 
   - The arbiter maintains a state (`r_a_owner`) that tracks which master currently owns the bus. If one master asserts its cycle signal (`i_a_cyc` or `i_b_cyc`), it can request access.
   - In the "ALTERNATING" scheme, priority alternates between the two masters; if one master was last granted the bus and it does not de-assert its cycle signal, the other master must wait.

2. **Bus Granting Logic**:
   - If both masters assert their cycle signals simultaneously, the arbiter grants the bus based on the configured arbitration scheme. For example, in the "PRIORITY" scheme, Master A always takes precedence.
   - The bus remains owned by the granted master until they release the bus (deassert `o_cyc`).

3. **Control Outputs**:
   - The module generates the necessary control signals for the bus based on the ownership state. If neither master holds the bus, the outputs are effectively irrelevant (don't care conditions).
   - The acknowledgment, stall, and error signals for each master are routed based on the active ownership of the bus to ensure correct communication back to the respective masters.

4. **Formal Verification Support**:
   - Included in the file are sections of formal verification code to ensure that the arbiter behaves correctly according to specified properties, including assertions about request counts and acknowledgment signals.

Overall, `wbarbiter.v` is crucial for enabling efficient and orderly access to a shared resource (the bus) in a multi-master CPU environment, maintaining fairness and performance.

### File: wbdblpriarb.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/ex/wbdblpriarb.v
### Purpose of the File

The file `wbdblpriarb.v` implements a double priority arbiter for two separate Wishbone (WB) buses. The purpose of this module is to facilitate arbitration between two masters attempting to access the Wishbone bus while maintaining the timing requirements of the Zip CPU architecture. By allowing simultaneous cyclic access requests from two bus masters (A and B), the arbiter determines which master has control over the bus in a manner that satisfies the local and external bus access needs and minimizes performance delays caused by bus contention.

### Inter-module Relationships

The `wbdblpriarb` module interacts with several other modules in the CPU architecture including:

- **fwb_master:** It is instantiated twice in the file for the two masters (A and B). These modules represent the Wishbone master interfaces that handle the outgoing bus signals and connection to the bus arbiter, enabling requests and handling responses.
  
- **fwb_slave:** It is also instantiated multiple times for the two slave devices corresponding to both A and B buses. This gives the arbiter the capacity to evaluate requests, acknowledgments, and errors from the slave interfaces.
  
The associated control signals from `i_a_*` and `i_b_*` inputs and `o_*` outputs are structured to relay necessary information regarding read/write requests, addresses, and data, thus forming connections with both internal and external bus pathways of the system.

### Key Signals (Inputs/Outputs)

**Inputs:**
- `i_clk`: Clock input for synchronization.
- `i_reset`: Asynchronous reset signal.
- Bus A Signals:
  - `i_a_cyc_a`, `i_a_cyc_b`: Cycle signals indicating active bus cycles.
  - `i_a_stb_a`, `i_a_stb_b`: Strobe signals indicating valid data transfers.
  - `i_a_we`: Write enable signal.
  - `i_a_adr`, `i_a_dat`, `i_a_sel`: Address, data, and select signals for bus A.
  
- Bus B Signals:
  - Same as bus A signals but prefixed with `i_b_*`.

**Outputs:**
- Bus Control Signals:
  - `o_cyc_a`, `o_cyc_b`: Output cycle signals for the respective buses.
  - `o_stb_a`, `o_stb_b`: Strobe outputs.
  - `o_we`: Write enable signal indicating write operations.
  - `o_adr`, `o_dat`, `o_sel`: Outputs for address, data, and select signals.
  
- Acknowledgment and Error Signals:
  - `o_a_stall`, `o_a_ack`, `o_a_err`: Stall, acknowledgment, and error signals for bus A.
  - `o_b_stall`, `o_b_ack`, `o_b_err`: Stall, acknowledgment, and error signals for bus B.

### Behavior of the Module

The arbiter's primary logic involves determining which bus master (A or B) has the right to utilize the shared bus based on their request signals. This is managed using the `r_a_owner` register, which keeps track of current ownership (whether A or B is allowed access). The arbitration occurs as follows:

- **Ownership Logic:** 
  - If neither master is active (`CYC` signals are low), the ownership remains with the last requester until the other master requests access. 
  - The module aims to yield control to a requesting master if its `STB` signal is asserted, and if the opposite master does not also have an active request.
  
- **Output Signal Generation:** 
  - The outputs for the cycle, strobe, and data control signals are driven based upon which master currently "owns" the bus. 
  - If `A` owns the bus, its respective signals are passed out; if `B` owns it, `B`'s signals are routed instead.

- **Handling Acknowledgments and Errors:** 
  - The arbiter monitors responses from the slave devices (`ACK` and `ERR` signals); it will only acknowledge a signal from the master that currently owns the bus. 
  - Inactive masters (those not owning the bus) will always have their acknowledgment outputs de-asserted, providing a clean signal to the slaves.

This approach assures minimum bus contention and maximizes system performance, following timing constraints effectively. The module thus enhances the overall efficiency of bus transactions within the Zip CPU architecture.

### File: wbdmac.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/wbdmac.v
### Overview of the wbdmac.v File

#### Purpose
The `wbdmac.v` file implements a Wishbone DMA (Direct Memory Access) controller for the Zip CPU -- a small, lightweight, RISC CPU soft core. This DMA controller facilitates the transfer of data between different memory locations within the Wishbone address space without CPU intervention, allowing hardware to manage memory transfers efficiently. The DMA can transfer up to 4kB (1k words) at a time and is controlled via dedicated registers for configuration such as control/status, length, source address, and destination address.

#### Inter-module Relationships
The wbdmac module interacts with various components of the CPU architecture, specifically:
- **Wishbone Bus Interface**: It uses Wishbone signals (`i_swb_*` for slave port and `o_mwb_*` for master port) to receive commands and manage memory transfers.
- **Interrupt Controller**: It connects to an interrupt device (`i_dev_ints`) to assert an interrupt signal (`o_interrupt`) upon DMA completion.
- **Memory Interface**: It manages memory access by reading from and writing to internal memory (`dma_mem`) during the DMA operations.
- **Other Pipeline Components**: It might interact with other CPU modules, as it is often part of the execution and memory hierarchy, handling data movement that is critical to overall system performance.

#### Key Signals
**Inputs:**
- `i_clk`: System clock signal.
- `i_reset`: Reset signal to initialize the module.
- `i_swb_cyc`, `i_swb_stb`, `i_swb_we`: Signals for the slave Wishbone interface (cycle, strobe, write enable).
- `i_swb_addr`: Address input for the control/status and configuration.
- `i_swb_data`: Data input for configuration.
- `i_mwb_cky`, `i_mwb_stb`, `i_mwb_we`, `i_mwb_data`: Inputs from the master Wishbone interface, indicating when data transfers occur, along with data received.
- `i_dev_ints`: Interrupt signals from devices.

**Outputs:**
- `o_swb_ack`: Acknowledge output for the slave.
- `o_swb_data`: Data output for the slave interface.
- `o_mwb_cyc`, `o_mwb_stb`, `o_mwb_we`: Outputs to drive the master portion of the Wishbone interface, initiating transactions.
- `o_mwb_addr`, `o_mwb_data`: Address and data outputs during DMA operations.
- `o_interrupt`: Interrupt output indicating DMA transfer completion.

#### Behavior
1. **Control Logic**: The module implements a state machine composed of several states (DMA_IDLE, DMA_WAIT, DMA_READ_REQ, etc.) to manage its operations. It transitions between these states based on the status of the input signals, reflecting whether it is idle, waiting for controller commands, reading data, or writing data.

2. **State Machine**: 
   - **DMA_IDLE**: The controller is inactive. Upon receiving valid commands, it transitions to the `DMA_WAIT` state.
   - **DMA_WAIT**: The module is waiting for an external trigger or interrupt to start the transfer.
   - **DMA_READ_REQ**: The module requests data to be read from the source address.
   - **DMA_READ_ACK**: Acknowledgment of read data.
   - **DMA_PRE_WRITE**: Prepares to write data to the destination address.
   - **DMA_WRITE_REQ**: Initiates the write command.
   - **DMA_WRITE_ACK**: Acknowledgment of the written data.

3. **Data Transfer**: The controller handles movement of data by managing and updating internal registers that hold the source and destination addresses, transfer lengths, and more. It supports incremental address updates during the transfer based on configurations provided in the control/status register.

4. **Error Handling**: The module includes mechanisms to handle errors or bus errors during transfers, allowing it to abort operations or indicate failure statuses.

This comprehensive design allows the `wbdmac` module to seamlessly integrate into the larger CPU architecture, enabling efficient data management and operations that enhance the overall functionality of the Zip CPU.

### File: ziptimer.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/ziptimer.v
Certainly! Here's a comprehensive analysis of the `ziptimer.v` file based on the provided content:

### Overall Purpose
The `ziptimer.v` file implements a lightweight timer module for the Zip CPU architecture. Its primary purpose is to provide timing capabilities for the CPU, offering functionality that can be used for generating interrupts based on a countdown mechanism. The timer can operate in a mode that allows for automatic reloading, making it suitable for both one-time and periodic interruption applications.

### Inter-module Relationships
The `ziptimer` module interfaces with several other components within the CPU architecture:
- **Wishbone Interface**: The timer uses the Wishbone protocol for communication, allowing it to interact seamlessly with other Wishbone-compatible modules, such as the CPU and memory.
- **Interrupt Controller**: The module generates an interrupt signal which can be connected to the CPU's interrupt controller. This feature allows the CPU to reset when the timer expires, enabling the timer to function as a watchdog timer.
- **Associated Control Logic**: The timer is influenced by control signals from the CPU, particularly around its reset and enable states, allowing it to receive commands for starting, stopping, or resetting the timer.

### Key Signals (Inputs/Outputs)
#### Inputs:
- `i_clk`: The clock signal for timing the operations within the timer.
- `i_reset`: Asynchronous reset signal to initialize the timer state.
- `i_ce`: Clock enable signal that allows the timer to operate.
- **Wishbone Inputs**:
  - `i_wb_cyc`: Wishbone cycle signal indicating that a transaction is in progress.
  - `i_wb_stb`: Wishbone strobe signal that indicates the current wishbone transaction is being initiated.
  - `i_wb_we`: Write enable signal that differentiates between read and write operations.
  - `i_wb_data`: Data signal containing the value to be written/read.
  - `i_wb_sel`: Byte select signals for determining which bytes of the data are valid.

#### Outputs:
- `o_wb_stall`: Indicates if the Wishbone bus is stalled (always 0 in this implementation).
- `o_wb_ack`: Acknowledge signal for Wishbone, indicating a successful transaction.
- `o_wb_data`: Data output from the timer, which includes the current timer value and the auto-reload state.
- `o_int`: Interrupt output that signals when the timer has expired.

### Behavior of the Module
The `ziptimer` module operates using a combination of registers and control logic:

- **State Management**: Registers are maintained for tracking the running state of the timer (`r_running`), the timer value (`r_value`), and whether the timer has reached zero (`r_zero`).
- **Control Logic**:
  - When the timer is written to (triggered by `wb_write`), different states can be set, such as starting the timer or configuring it for auto-reload.
  - The timer counts down when enabled and when the `i_ce` (clock enable) signal is active. When it reaches zero, the interrupt signal `o_int` is set, and if auto-reload is enabled, it resets to the specified interval value.
  
- **Initialization & Resetting**: Upon reset, the timer values are initialized, and the module enters a stable state where it does not generate interrupts or acknowledge transactions until it is explicitly started.

- **Interrupt Generation**: An interrupt is generated precisely when the timer value transitions from 1 to 0, making it reliable for real-time applications.

- **Formal Verification Properties**: The module includes several assertions for formal verification purposes to ensure its operation adheres to expected behaviors, particularly concerning its state transitions and interface integrity with the Wishbone protocol.

Overall, the `ziptimer.v` serves as a critical component in the Zip CPU, providing essential timing functionalities needed for system control and operation.

### File: zipjiffies.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/zipjiffies.v
### Overall Purpose of the File

The `zipjiffies.v` file implements a peripheral for the Zip CPU architecture, specifically designed to handle 'jiffies', which are time units used in operating systems, such as Linux, for scheduling sleep intervals for processes. This module allows the CPU to read a counter representing the current number of jiffies and set interrupts based on future jiffie values. The jiffies mechanism is essential for implementing time-based functionality in the CPU, enabling processes to manage timing and potentially sleep until certain time intervals have passed.

### Inter-module Relationships

The `zipjiffies` module interacts directly with the Wishbone bus protocol, allowing the CPU or other peripherals to communicate with it. Its input signals are generated by other CPU components, such as the control unit or other peripherals wishing to set or read the jiffies counter. The output signals of `zipjiffies` also provide necessary information back to the CPU, including the current counter value and interrupt signals. More specifically, it interfaces with modules responsible for timer management, interrupt handling, and memory management through the Wishbone protocol, allowing for coherent timing operations across the system.

### Key Signals (Inputs/Outputs)

**Inputs:**
- `i_clk`: The clock signal to synchronize operations.
- `i_reset`: A signal to reset the internal states of the module.
- `i_ce`: Clock enable line to control the incrementing behavior of the counter.
- `i_wb_cyc`: Indicates that the Wishbone cycle is active.
- `i_wb_stb`: Signals that a Wishbone transaction has started.
- `i_wb_we`: Write enable signal for Wishbone operations.
- `i_wb_data`: The data sent during a Wishbone write operation.
- `i_wb_sel`: Enables selection of the wishbone data byte to write.

**Outputs:**
- `o_wb_stall`: A signal that indicates if the module is stalling the Wishbone bus (always low in this implementation).
- `o_wb_ack`: Acknowledge signal for Wishbone transactions; indicates the module has valid data to respond with.
- `o_wb_data`: The current value of the jiffies counter, accessible to other modules.
- `o_int`: The interrupt signal that indicates an interrupt condition based on the jiffies timing.

### Behavior of the Module

The `zipjiffies` module contains several key functionalities:

1. **Counter Logic**:
   - The module maintains a jiffies counter (`r_counter`) that continuously increments on each clock cycle, controlled by the `i_ce` signal. The counter can be reset by the `i_reset` signal.

2. **Interrupt Management**:
   - The module sets an interrupt (`o_int`) based on the jiffies counter reaching a specific value, which can be written to by the CPU or external devices through the Wishbone interface.
   - When a value is written to the jiffies counter, it is only accepted if it represents a future time compared to the current counter value. This comparison is managed using signed arithmetic to determine if the new interrupt time is valid.

3. **Wishbone Acknowledgment**:
   - The design acknowledges Wishbone transactions within the clock cycle they are issued. Every time a valid Write transaction occurs, the corresponding data can be either written to set a new interrupt or read back to retrieve the current jiffies count.

4. **Control Logic**:
   - The module includes control logic that detects when a write operation is intended to set a new interrupt and manages the state of that interrupt (whether it is active or not).
   - The interrupt becomes self-clearing once it triggers, meaning it will automatically reset, requiring a new write command to set a future interrupt.

5. **Formal Verification Section**:
   - The module includes formal properties to verify its behavior under various assumptions about input signals. This aspect helps in ensuring that the implementation is correct and can be validated formally.

In summary, the `zipjiffies.v` module is a critical component of the Zip CPU, responsible for managing time-based interrupts and providing an interface for scheduling processes based on elapsed time while ensuring interaction with the overall CPU architecture through the Wishbone bus structure.

### File: zipmmu.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/zipmmu.v
### Overall Purpose of the File
The `zipmmu.v` file implements a Memory Management Unit (MMU) designed for the Zip CPU architecture. The MMU acts as an intermediary between the CPU and memory, facilitating address translation and memory protection. It allows the CPU to configure and access its memory space in a controlled manner, providing features such as page-based memory management, context switching, and control over read/write permissions. The MMU is particularly tailored for operation in a system where it translates virtual addresses to physical addresses while ensuring efficient memory access.

### Inter-module Relationships
The `zipmmu` module interacts with multiple other modules within the CPU architecture:
- **Wishbone Bus Interfaces**: It employs two Wishbone bus interfaces (master and slave) to manage access to memory. The MMU acts on instructions and data passing through these buses while servicing the requests from the CPU.
- **Control Logic**: The MMU integrates into the ZIP CPU architecture's control logic, handling requests from the execution pipeline concerning virtual memory access, page table lookups, and context management.
- **Data/Instruction Memory**: It serves data and instruction fetches from memory, potentially translating virtual addresses to physical addresses as required.
- **Prefetching Logic**: The MMU allows for integration with prefetch logic, enabling it to snoop on memory requests and cache address translations.

This architecture enables efficient management and control over memory access, especially considering the potential overlap between memory configuration and normal operational accesses.

### Key Signals (Inputs/Outputs)
1. **Inputs**:
   - `i_clk`: Main clock signal for synchronization.
   - `i_reset`: Reset signal to initialize the MMU.
   - `i_wbs_cyc_stb`, `i_wbs_we`, `i_wbs_addr`, `i_wbs_data`: Signals related to the Wishbone slave interface for communication with the CPU.
   - `i_wbm_cyc`, `i_wbm_stb`, `i_wbm_we`, `i_wbm_exe`, `i_wbm_addr`, `i_wbm_data`, `i_wbm_sel`: Signals related to the Wishbone master interface for accessing memory and performing read/write operations.
   - `i_gie`: General interrupt enable signal to control MMU operations based on the CPU's execution context.
   - `i_stall`, `i_ack`, `i_err`: Signals from the slave/controlled memory indicating the state of read/write operations.

2. **Outputs**:
   - `o_wbs_stall`: Indicates whether the Wishbone slave is to stall.
   - `o_wbs_ack`: Acknowledgment signal for Wishbone slave transactions.
   - `o_wbs_data`: Data output to the CPU via the Wishbone slave.
   - `o_cyc`, `o_stb`, `o_we`, `o_addr`, `o_data`, `o_sel`: Control signals for the Wishbone master interface to initiate memory transactions.
   - `o_rtn_stall`, `o_rtn_ack`, `o_rtn_err`, `o_rtn_miss`, `o_rtn_data`: Outputs indicating the status of return transactions from the memory bus.
   - Prefetch signals: For enabling snooping by prefetch logic.

### Behavior of the Module
The `zipmmu` module contains complex control logic and may include state machines that manage various operations:

1. **Memory Access and TLB Handling**: 
   - The MMU maintains translation entries in a Translation Lookaside Buffer (TLB), allowing fast address translation from virtual to physical addresses. It supports read-only and executable flags for memory pages, providing protection against unauthorized access.
   
2. **Page Lookup Control**: 
   - A sequence of checks and actions occurs when a memory access is requested, determining whether the corresponding page is in the TLB or has to be fetched from the page table. The module handles hits, misses, and different error conditions like read-write violations.

3. **Context Management**:
   - The MMU supports multiple contexts, handling switches between kernel and user modes, ensuring appropriate access rights based on the current execution context.

4. **Latency Control**:
   - The MMU introduces mechanisms to control memory access latencies, limiting stalls to ensure efficient operation within the memory access pipeline.

5. **Prefetch Handling**:
   - It has logic to manage prefetch signaling, thus providing data about memory accesses to other systems like cache systems or instruction prefetchers.

In summary, the `zipmmu.v` plays a crucial role in managing complex memory access patterns in a CPU, supporting virtual memory architecture while interacting cooperatively with other components in the system to facilitate efficient and safe memory operations.

### File: zipcounter.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/zipcounter.v
### Overall Purpose of the File
The `zipcounter.v` file implements a simple counter module intended for use within a CPU design, specifically in the context of measuring time or certain events by counting clock cycles. This counter can trigger interrupts upon rollover and is designed to support process accounting by enabling the user to reset the counter for tracking resource usage for various tasks in an operating environment. With a 32-bit wide counter, it allows for counting up to 2^32 clock cycles before rolling over.

### Inter-module Relationships
The `zipcounter` module interacts closely with other components in the CPU architecture:
- **Wishbone Interface**: It communicates with other modules via the Wishbone interface, handling inputs such as `i_wb_cyc`, `i_wb_stb`, `i_wb_we`, and `i_wb_data`. It signals acknowledgment (`o_wb_ack`) and presents data (`o_wb_data`) in response to reads.
- **Interrupt Controller**: The module outputs an interrupt signal (`o_int`) to notify other parts of the CPU when it rolls over (i.e., the counter exceeds its maximum value). This interaction is crucial for processes in the CPU that need to handle interrupts.
- **Event Input (`i_event`)**: The counter can increment its value based on an external event signal, allowing it to be integrated into different control flows or mechanisms where event counting is necessary.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_clk`: The clock signal to synchronize operations.
  - `i_reset`: Active high reset signal to clear the counter and interrupt state.
  - `i_event`: A signal indicating when to increment the counter.
  - `i_wb_cyc`, `i_wb_stb`, `i_wb_we`: Control signals for the Wishbone bus interface denoting cycle status, strobe, and write operation respectively.
  - `i_wb_data`: Data input during write operations on the Wishbone bus.

- **Outputs**:
  - `o_wb_stall`: Always outputs 0, indicating no stalling on the Wishbone interface.
  - `o_wb_ack`: Acknowledge signal for Wishbone read/write transactions.
  - `o_wb_data`: Output data representing the current count value of the counter.
  - `o_int`: Interrupt signal indicating that the counter has rolled over.

### Behavior of the Module
The `zipcounter` module operates based on clock edges and defined conditions:

1. **Initialization**: On reset (`i_reset`), the counter and interrupt signal are set to zero.

2. **Writing Data**: If a write enable (`i_wb_we`) and strobe (`i_wb_stb`) signal are active, the counter value is set to the incoming data (`i_wb_data`), and the interrupt signal is cleared.

3. **Counting on Event**: If the `i_event` signal is asserted when the module is not in reset, the counter increments by 1 on each clock cycle. If the counter rolls over (i.e., reaches its maximum value of 2^32), the interrupt signal (`o_int`) is asserted.

4. **Acknowledgment on Bus Transactions**: The module acknowledges any valid Wishbone bus transactions by setting `o_wb_ack` based on the strobe signal.

5. **Control Logic**: Throughout the counting process, control logic maintains the behavior of the output signals:
    - It ensures that the `o_wb_stall` is always set to zero, indicating that the counter does not hinder bus operations.
    - The interrupt signal is controlled such that it will not assert two cycles consecutively after a rollover condition.

In summary, `zipcounter.v` serves as a simple yet effective means to count clock cycles, allowing the CPU to track time or events correspondingly while integrating seamlessly with the overall system architecture.

### File: icontrol.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/icontrol.v
### Overall Purpose of `icontrol.v`

The `icontrol.v` file implements an interrupt controller for a RISC CPU soft core named Zip CPU. Its primary purpose is to manage multiple interrupt sources effectively, enabling or disabling interrupts based on written values and propagating triggered interrupts appropriately. This controller is designed to be compliant with the Wishbone bus protocol and operates on a 32-bit data bus, allowing it to handle various interrupt scenarios with minimal clock cycle overhead.

### Inter-Module Relationships

The `icontrol` module interacts with several other parts of the CPU architecture, particularly those related to interrupt handling and communication via the Wishbone interface. Key relationships include:

1. **Wishbone Bus Interfaces**: The module communicates with other subsystems over the Wishbone bus, responding to control signals that determine whether interrupts are to be enabled, disabled, or acknowledged. It reads the interrupt status from the `i_brd_ints` input, which is expected to represent external interrupt requests.

2. **Interrupt Logic**: The controller works closely with CPU components that generate interrupts. It signals the CPU when an interrupt occurs by asserting the `o_interrupt` output. 

3. **Memory and Control Units**: It integrates with the memory and control units that may use the interrupt signals. The controller ensures that when an interrupt is asserted, the CPU can appropriately handle the event based on its architecture.

### Key Signals (Inputs/Outputs)

- **Inputs**:
  - `i_clk`: Clock signal for synchronizing operations.
  - `i_reset`: Reset signal to initialize the module.
  - `i_wb_cyc`, `i_wb_stb`, `i_wb_we`: Wishbone control signals to manage bus transactions.
  - `i_wb_data`: Data input for writing configurations and states.
  - `i_wb_sel`: Byte enable signal for the Wishbone data bus.
  - `i_brd_ints`: A vector of interrupt request signals from various sources.

- **Outputs**:
  - `o_wb_stall`: Indication of any stalling conditions on the Wishbone bus.
  - `o_wb_ack`: Acknowledgment signal for successful bus transactions.
  - `o_wb_data`: Output data containing the status of interrupts and other control signals.
  - `o_interrupt`: Asserts when an interrupt should be handled by the CPU.

### Behavior of the Module

The behavior of the `icontrol` module can be described in the following key parts:

1. **Interrupt State Management**:
   - The module maintains a state of interrupts via `r_int_state`, which indicates pending interrupts from the various sources connected via the `i_brd_ints` input.
   - This state is updated based on incoming interrupts and bus write operations, allowing the controller to respond to changes from the system.

2. **Interrupt Enable Logic**:
   - A second register, `r_int_enable`, tracks which interrupts are enabled, based on write operations to the Wishbone data bus. Writes to the bus can enable or disable specific interrupts.

3. **Master Interrupt Enable**:
   - The global interrupt enable bit, tracked in `r_mie`, determines whether any interrupts will be acknowledged. If this bit is cleared, all pending interrupts will be effectively ignored even if they are enabled.

4. **Signal Generation**:
   - The output signal `o_interrupt` is asserted if a pending interrupt exists and the global interrupt enable is set. This logic integrates the states of multiple interrupts to inform the CPU about active interrupts needing service.

5. **Output Data Handling**:
   - The module creates a structured output data word, `o_wb_data`, which includes the state of all interrupts, their enable status, and the global interrupt enable status, providing comprehensive information back to the CPU or other bus masters.

6. **Reset Handling**:
   - Upon reset, all internal registers are initialized, ensuring a clean start for the module to avoid any unintended active states when the system powers up.

This structured control logic, along with its integration into the Wishbone bus architecture, allows for efficient management of interrupts within the CPU design, enhancing performance and responsiveness to external events.

### File: axilperiphs.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/axilperiphs.v
### Purpose of the File
The `axilperiphs.v` file implements a peripheral module for an AXI Lite bus interface in a CPU architecture. Its primary role is to facilitate communication between the CPU and peripheral devices by managing read and write transactions, including control for devices like an interrupt controller, watchdog timer, and timers. It defines addressable registers for various functionality including interrupts and timer operations, enabling the CPU to manage and monitor these peripherals efficiently.

### Inter-module Relationships
The `axilperiphs` module interacts with several other modules within the CPU architecture:

1. **Interrupt Controller (`icontrol`)**: This module handles external interrupts and connects to the `axilperiphs` module to maintain interrupt status and vectoring. The `o_interrupt` output of `axilperiphs` indicates when an interrupt is asserted.

2. **Watchdog Timer (`ziptimer`)**: This module is instantiated to provide a watchdog function, and it connects to the peripheral module's bus interface for writing and reading its control registers.

3. **Timer Modules (`ziptimer`)**: Similar to the watchdog, multiple instances of timer modules are included for maintaining time-based operations that can be accessed via the AXI interface.

4. **Performance Counters**: The module can optionally interface with performance metrics, which can also be managed via AXI-lite transactions if the `OPT_COUNTERS` parameter is enabled.

### Key Signals (Inputs/Outputs)
**Inputs:**
- `S_AXI_ACLK`, `S_AXI_ARESETN`: Clock and reset signals for standard AXI-lite operation.
- `S_AXI_AWVALID`, `S_AXI_WVALID`, `S_AXI_ARVALID`: Transaction request signals for various types of AXI operations (write and read).
- `S_AXI_AWADDR`, `S_AXI_WDATA`, `S_AXI_ARADDR`: Data paths for address and data corresponding to AXI transactions.
- Peripheral Control Inputs: `i_cpu_reset`, `i_cpu_halted`, `i_cpu_gie`, etc., for controlling the peripheral state based on CPU conditions.
  
**Outputs:**
- `S_AXI_AWREADY`, `S_AXI_BVALID`, `S_AXI_RVALID`: Response signals indicating the readiness of the AXI interface to proceed with transactions.
- Peripheral outputs: `o_interrupt`, `o_watchdog_reset`, which relay the status of the interrupt controller and watchdog functionalities back to the core CPU architecture.

### Behavior of the Module
The module's behavior consists of several key functionalities:

1. **AXI Transaction Handling**: It incorporates both simple read/write mechanisms and skid buffers to manage asynchronous operations effectively. The use of skid buffers helps to mitigate timing issues by allowing one operation to queue while another is still processing. 

2. **Control Logic**: 
   - **Write Handling**: When a write transaction is detected (via `S_AXI_AWVALID` and `S_AXI_WVALID`), the appropriate addressing and data handling occurs to register the values in the internal peripheral registers. The ready and valid signals are managed to ensure correct handshaking.
   - **Read Handling**: Read requests are queued and processed similarly, taking care to respond appropriately to the read requests based on the current state of the peripherals.

3. **Interrupt Vector Generation**: The interrupt vector is constructed based on the status of various peripheral devices. This allows external interrupt sources to be properly managed and propagated to the CPU.

4. **Timer Management**: The timer instances handle periodic events through interrupts, and state-based control is implemented for these timers, including read/write operations to their respective registers.

5. **Accounting Counters**: If enabled, the module incorporates counters to track different CPU states and performance metrics. This information can be accessed via AXI but is effectively isolated from the operational logic unless specifically requested through the bus.

### Conclusion
In summary, the `axilperiphs.v` file encapsulates a critical part of the CPU peripheral management system, providing an AXI-lite interface for effective integration with various hardware peripherals and control logic. Its interactions with other modules such as interrupt controllers and timers allow for comprehensive management of hardware events and CPU operations.

### File: wbwatchdog.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/rtl/peripherals/wbwatchdog.v
### Description of `wbwatchdog.v`

#### Overall Purpose
The `wbwatchdog.v` file implements a bus watchdog timer for the Zip CPU architecture. This module serves as a countdown timer that monitors system activity and issues interrupts when certain conditions are met—specifically, when a predefined timeout expires. Its main responsibility is to enhance the reliability of system operations by detecting when the bus has not been accessed for a sufficiently long period, triggering an interrupt to signal potential issues or the need for corrective action.

#### Inter-module Relationships
The `wbwatchdog` module is interconnected with several other components within the CPU architecture:
- It relies on a signal input (`i_timeout`) to determine the countdown period for the watchdog timer.
- The output signal (`o_int`) serves as an interrupt line, which may interface with the CPU's interrupt management system, allowing the CPU to respond when the timer expires.
- While the detailed interactions with other modules are not explicitly provided in the file, it can be inferred that the watchdog would typically be integrated in conjunction with modules related to bus operations, interrupt servicing, and possibly other peripherals that operate over the Wishbone bus interface.

#### Key Signals
**Inputs:**
- `i_clk`: The clock signal, which synchronizes updates to the internal state of the watchdog.
- `i_reset`: An active-high reset signal that initializes the timer state.
- `i_timeout`: A parameter input that defines the duration before an interrupt occurs, and this input can be assumed to be constant during operation.

**Outputs:**
- `o_int`: A register output that signals an interrupt condition to other system components when the timer countdown reaches zero.

#### Behavior of the Module
1. **Initialization and Reset**: Upon reset (`i_reset` being high), the internal counter (`r_value`) is initialized to the value provided by `i_timeout`. The interrupt output (`o_int`) is cleared (`0`).

2. **Count Down Logic**:
   - The primary counter decreases over time when the reset is not active and the interrupt is not already asserted (`!o_int`). The counter value increments by one on each clock cycle (`r_value + 1`). Notably, the counter effectively counts down towards zero, which is implied in the commented section, but actually seems to count upwards towards a limit due to the behavior in the counter logic (`r_value <= r_value + {(BW){1'b1}};`).
   - Once `r_value` reaches zero, the week's interrupt flag, `o_int`, will be set to `1` if `r_value` is zero.

3. **Interrupt Logic**: The interrupt output (`o_int`) remains asserted (`1`) whenever the counter is at zero unless a reset occurs, which subsequently clears the output. The interrupt condition is established on the clock edge, allowing the system to respond in real time.

4. **Formal Verification Aspects**: For formal verification, the module includes assertions to ensure the expected behavior of the counter and interrupt outputs relative to the input conditions. This includes validating that if the interrupt occurs while the system is not resetting, the `o_int` signal reflects the state of the counter accurately.

### Conclusion
In summary, the `wbwatchdog` module plays a crucial role in maintaining system integrity by monitoring activity on the bus and providing timely interrupts when a specified timeout has elapsed. It does so while being designed to easily integrate with the Zip CPU architecture and accommodate formal verification to assure correctness in operation.

### File: wbdown.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/wbdown.v
### Overall Purpose of the File

The `wbdown.v` file implements a downconverter module for the Wishbone bus framework in a CPU architecture known as Zip CPU. The primary purpose of this module is to convert a wider data bus (e.g., 64 bits) to a smaller one (e.g., 32 bits). This conversion is particularly useful in scenarios where the CPU supports multiple data widths and needs to efficiently handle data reads and writes across different widths without introducing complexity in upstream components.

### Inter-Module Relationships

The `wbdown` module interacts with several other modules within the Zip CPU architecture:
- **Wishbone Bus Components**: It interfaces directly with the Wishbone bus protocol, receiving wide bus requests and transmitting smaller bus requests. Key modules involved in this interaction include slave and master entities which manage memory accesses and responses.
- **FIFO Buffers**: The module uses a FIFO (First-In-First-Out) buffer for managing data transfers, helping it to synchronize data flow between the wide and small bus widths while accommodating burst transfers.
- **Formal Verification Modules**: The code includes formal verification constructs to ensure the correct operation of the bus downconversion logic using additional modules like `fwb_slave` and `fwb_master` for checking the invariants and properties of the data handling logic during simulation.

### Key Signals (Inputs/Outputs)

**Inputs:**
- `i_clk`: The clock signal for synchronizing the behavior of the module.
- `i_reset`: A signal to reset the module state.
- `i_wcyc`: Indicates a valid cycle on the incoming wide bus.
- `i_wstb`: Signals a valid data write to the wide bus.
- `i_wwe`: Determines if the operation is a write (`1`) or read (`0`).
- `i_waddr`: Address for the incoming wide bus operation.
- `i_wdata`: Data input from the wide bus.
- `i_wsel`: Strobe selects which bytes in the wide data should be written.
- `i_stall`: Indicates if the wide bus is stalled, preventing further processing.
- `i_ack`: Acknowledgment signal from the downstream module.
- `i_data`: Data read from the downstream module.
- `i_err`: Error flag from the downstream module.

**Outputs:**
- `o_cyc`: Indicates a valid cycle on the outgoing small bus.
- `o_stb`: Signals a valid data request on the outgoing small bus.
- `o_we`: Indicates whether the operation on the small bus is a write.
- `o_addr`: Address for the outgoing small bus operation.
- `o_data`: Data output to the small bus.
- `o_sel`: Byte select for the outgoing small bus.
- `o_wstall`: Indicates if the module is stalled.
- `o_wack`: Acknowledgment signal for the wide bus write.
- `o_wdata`: Data that is acknowledged on the wide bus.
- `o_werr`: Error flag for the wide bus operation.

### Behavior of the Module

The `wbdown` module orchestrates its behavior through various states, mainly managing the write operations from a wider bus to a narrower bus:

1. **State Management**: The module uses state registers (`r_cyc`, `r_stb`, `r_we`, etc.) to keep track of the current cycle, status of the write request, and data address. The state is updated based on clock edges and control signals, particularly managing synchronization with the incoming and outgoing buses.

2. **Data Handling**: When a write request occurs, the module calculates the required number of small bus transactions based on the wide bus data width and processes through the FIFO structure. It keeps track of data alignment using little-endian or big-endian formats, ensuring proper data is sent out on the smaller bus.

3. **FIFO Management**: The use of a FIFO allows the module to manage data bursts effectively. It stores outgoing addresses and keeps track of how many transactions are yet to be acknowledged by the receiving end.

4. **Formal Verification Logic**: The module includes assertions and formal properties to validate that the operations conform to expected behaviors, such as ensuring that data is correctly aligned and that the status of requests is correctly managed.

In summary, the `wbdown` module is a critical component for efficiently managing data transfer across different bus widths in the Zip CPU design, ensuring seamless integration and operation within the larger system.

### File: addrdecode.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/addrdecode.v
### Overall Purpose of the File
The `addrdecode.v` file implements an address decoding module for the Zip CPU, which is a small RISC CPU soft core. The module's primary purpose is to decode incoming address requests from CPU masters and determine which slave device, if any, should respond to these requests based on predefined address ranges and access permissions.

### Inter-module Relationships
The `addrdecode` module interacts with several other components in the CPU architecture:
- **Slaves**: It routes address and data through to the correct slave device based on the incoming address. The range of addresses that each slave responds to is defined by the `SLAVE_ADDR` parameter.
- **CPU Master**: The module checks if the master has valid accesses, allowing the CPU to communicate effectively with different peripherals or memory blocks.
- **Bus Systems**: The address decoder may interact with AXI or similar bus systems, enabling proper routing of requests based on the specified parameters.
- **Formality and Verification**: The module includes formal verification assertions, ensuring that the behavior conforms to expected results during simulation and testing.

### Key Signals (Inputs/Outputs)
- **Inputs**:
  - `i_clk`: The clock signal used for synchronous operations within the module.
  - `i_reset`: A signal indicating when to reset the module; initializes outputs to a known state.
  - `i_valid`: Indicates that a valid address and data pair has been provided to the decoder.
  - `i_addr`: The address input that needs decoding; this address will determine which slave device responds.
  - `i_data`: The data input relevant to the address request.

- **Outputs**:
  - `o_stall`: A signal indicating whether the operation is stalled, controlling data flow based on whether the output can proceed.
  - `o_valid`: Indicates whether the output data is valid and ready to be read.
  - `o_decode`: A decoded output indicating which slave has been selected based on the decoded address.
  - `o_addr`: The output address that will be sent to the slave.
  - `o_data`: The data corresponding to the output address, ready to be driven towards a slave.

### Behavior of the Module
The behavior of the `addrdecode` module can be delineated as follows:

- **Address Matching**: The logic examines incoming requests by comparing the address against predefined slave address ranges (`SLAVE_ADDR`) while considering the relevant bits for each slave through `SLAVE_MASK`. If a match is found and access is allowed (as defined by `ACCESS_ALLOWED`), the corresponding decoded output for that slave is asserted.

- **Output Control Logic**:
  - Predetermined decoded requests are registered through the signal `prerequest`, which is derived through combinational comparison between the input address and slave addresses.
  - Depending on the `OPT_REGISTERED` parameter, the output values can either be registered synchronously with the clock or combinationally driven.
  
- **Stall Logic**: The module incorporates `o_stall` to manage flow control. If the output is valid and there is a stall signal asserted from downstream, the operation is held up.

- **Formal Verification**: The module includes extensive formal properties checking to ensure the correctness of address decoding logic during simulation. Properties like ensuring at least one decoded output is high when `o_valid` is asserted and ensuring proper formal checks for unused inputs are included.

Overall, the `addrdecode` module aims to efficiently manage address decoding and selection of slave devices in a structured and reliable manner, contributing to the robust communication infrastructure of the Zip CPU architecture.

### File: axilxbar.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axilxbar.v
### Purpose of the File
The `axilxbar.v` file implements a full crossbar switch for AXI-lite interfaces within a CPU architecture. It facilitates communication between multiple AXI-lite master devices and multiple AXI-lite slave devices, allowing for efficient transactions where any master can send requests to any slave. The design is aimed at achieving high throughput by allowing one transaction to occur per clock cycle while managing the complexity of potential contention from multiple masters.

### Inter-module Relationships
- **Master Interface Modules:** This module connects to multiple AXI-lite masters, each potentially issuing read and write requests to the slaves.
- **Slave Interface Modules:** It processes requests directed to multiple AXI-lite slaves, accepting and delivering data between slaves and the appropriate masters.
- **SubModules (e.g., `addrdecode`, `skidbuffer`):** The module uses instances of address decoder (`addrdecode`) to determine which slave a request is targeting based on the address signals. `skidbuffer` modules may be employed to handle potential misalignment of request and response signals, effectively implementing a buffer mechanism to alleviate timing issues.
  
Overall, `axilxbar.v` manages the arbitration and routing of signals between multiple master and slave interface modules in a CPU architecture, ensuring coherent transaction management across the system.

### Key Signals
- **Inputs:**
  - `S_AXI_ACLK`: Clock signal for the AXI-lite interface.
  - `S_AXI_ARESETN`: Active-low reset signal for the AXI-lite interface.
  - `S_AXI_*`: Signals pertaining to write and read transactions from multiple AXI-lite masters (address, control, data, and response).
  
- **Outputs:**
  - `M_AXI_*`: Signals pertaining to write and read transactions to multiple AXI-lite slaves (address, control, data, and response).

### Behavior of the Module
The crossbar switch orchestrates its operations as follows:

1. **Transaction Arbitration:** It employs a round-robin or priority-based approach for request handling from different AXI-lite masters to decide which master's request to service. This involves checking validity signals and potential backpressure from slaves.

2. **Control Logic:** Control logic is implemented for managing incoming and outgoing transaction signals. The module contains registers to track valid requests and their corresponding grants. It determines which master’s request is currently being processed based on request validity and readiness signals from slaves.

3. **Buffering Mechanism:** The module implements buffering logic using "skid buffers" to handle the possible timing discrepancy between address and data signals, preventing data corruption or undefined states.

4. **Transaction Flow:** It coordinates the state of each transaction by maintaining the state of outstanding requests (pending reads/writes) and ensuring responses are correctly directed back to the appropriate master once they are fulfilled by the slave interface.

5. **Latency Management:** The implementation also tracks the minimum latency required for read and write operations, which includes ensuring that writes properly acknowledge and complete before new requests are made.

6. **Error Handling:** Error signals and responses, such as the interconnect error, are encapsulated in the control logic to gracefully handle transaction failures.

Overall, this module provides a cohesive and efficient transaction engine for handling requests between masters and slaves, ensuring that the architecture operates smoothly even under potential contention scenarios.

### File: zipdma_check.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/zipdma_check.v
### Overall Purpose of `zipdma_check.v`

The `zipdma_check.v` file implements a verification module for testing a Direct Memory Access (DMA) interface within the Zip CPU architecture. This module performs functions related to data reading and writing operations facilitated by the Wishbone bus through a pseudo-random number generator implemented as a Linear Feedback Shift Register (LFSR). The goal of this module is to verify proper DMA operations by checking that data being passed through the buses match expected values and tracking the number of operations performed.

### Inter-module Relationships

The `zipdma_check` module communicates with various other components in the CPU architecture, primarily through the Wishbone bus interface. It accepts inputs for control and status signals typical of Wishbone-compliant devices, including:

- **Control Signals:** It can respond to control inputs that dictate memory operations—like read and write commands (indicated by `i_wb_we`, `i_wb_stb`, etc.).
- **Data Interfaces:** The module reads from and writes data to the Wishbone bus and other modules that might be connected, serving as a validation point for DMA transfers.
- **Status Reporting:** Outputs like `o_wb_ack` and `o_st_data` provide status information back to the bus masters, indicating whether operations were successful, erroneous, or if stalls are required.

### Key Signals (Inputs/Outputs)

#### Inputs:
- `i_clk`: The clock signal for synchronized operation.
- `i_reset`: Resets the module to an initial state.
- **Wishbone Control Signals**: 
  - `i_wb_cyc`: Indicates a Wishbone cycle is active.
  - `i_wb_stb`: Indicates that a Wishbone transaction is being requested.
  - `i_wb_we`: A write enable signal.
  - `i_wb_addr`: The address for the transaction.
  - `i_wb_data`: The data to write (for write transactions).
  - `i_wb_sel`: Byte select signals, determining which data bytes are valid for a transaction.
- **Status Port Signals**: 
  - `i_st_cyc`, `i_st_stb`, `i_st_we`, `i_st_addr`, `i_st_data`, `i_st_sel`: Manage the DMA status operations and control.

#### Outputs:
- `o_wb_stall`: A stall signal indicating the readiness of the output.
- `o_wb_ack`: Acknowledge signal for Wishbone transactions.
- `o_wb_data`: The data output for the Wishbone master.
- `o_wb_err`: Error signal indicating issues with the Wishbone operation.
- **Status Outputs**: 
  - `o_st_stall`, `o_st_ack`, `o_st_data`, `o_st_err`: Feedback for current status and results of operations.

### Behavior of the Module

The behavior of `zipdma_check` can be broken down into several functions:

1. **Data Enable Signals**: The `rd_data_en` and `wr_data_en` signals determine when read and write operations are valid based on the control signals. These signals are used to validate that transactions are occurring correctly based on the status of the `i_wb_stb` and `i_wb_we`.

2. **Data Handling with LFSR**: The LFSR generates pseudo-random data that simulates real data transactions. When there are valid write operations, the LFSR state is initialized based on the incoming data. It also shifts its state based on previous data for each read operation.

3. **Acknowledge Logic**: There are mechanisms to ensure that when a Wishbone transaction is active, an acknowledgment is generated. The condition `o_wb_ack <= i_wb_stb && !o_wb_stall` ensures that the acknowledgment is sent back to the initiator, signifying that the transaction was processed.

4. **Counting Operations**: The module keeps track of the number of read and write operations using `rd_count` and `wr_count`. It resets these counters during initialization but otherwise increments them based on the valid operations detected.

5. **Error Detection**: The module includes a basic error detection mechanism that checks if written data matches expected values. If there is a mismatch during a write operation, an error flag in the status data (`o_st_data[0]`) is set.

6. **Condition Monitoring**: The count of data read and written operations is reflected in the output data, providing visibility into the module's activity.

This design serves as a testing framework for the DMA capabilities of the Zip CPU architecture, ensuring that data transfers are occurring as expected and providing a mechanism for error detection and statistics monitoring.

### File: wbxbar.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/wbxbar.v
### Overall Purpose of the File

The `wbxbar.v` file implements a configurable Wishbone cross-bar interconnect that adheres to the Wishbone B4 pipeline specification. This module facilitates communication between multiple master and slave devices within a system, allowing them to share resources effectively while maintaining orderly and efficient transactions. Its primary aim is to manage the arbitration and routing of data between various bus masters and slaves, ensuring that data transfer adheres to specified protocols.

### Inter-module Relationships

The `wbxbar` module interacts with a variety of other components in the CPU architecture, specifically:

- **Master Modules**: It interfaces with NM number of master modules, receiving requests (read/write), addresses, and data from them. It manages these requests by directing them to the appropriate slave based on the addresses given.
- **Slave Modules**: The cross-bar connects to NS number of slave devices. For every transaction routed to a slave, it ensures appropriate signals are sent and monitored to handle the acknowledge (ACK) and error (ERR) responses.
- **Skid buffers** and **address decoders**: The design employs skid buffers to manage signals while preventing stalls from propagating back to the masters; an address decoder is used for decoding requests and directing them to the correct slave.

Through these interactions, `wbxbar` provides efficient arbitration and data management allowing multiple masters to communicate with several slaves without conflicts.

### Key Signals (Inputs/Outputs)

**Inputs**:
- `i_clk`: The clock signal that synchronizes the operations of the module.
- `i_reset`: The reset signal to initialize all internal states to a safe state.
- `i_mcyc`, `i_mstb`, `i_mwe`: Control signals from the bus masters indicating cycles, strobe, and write operations.
- `i_maddr`: Address signals from the master to specify where to read or write data.
- `i_mdata`: Data to write from the master to a given address.
- `i_msel`: Byte-enable signals for indicating which part of the data is relevant.

**Outputs**:
- `o_mstall`: Master stall signals, indicating whether the masters should pause their operations.
- `o_mack`: Acknowledgment signals that indicate whether a request was successfully processed.
- `o_mdata`: Data provided to the masters from the slaves.
- `o_merr`: Error signals indicating if a transaction encountered a problem.
- `o_scyc`, `o_sstb`, `o_swe`: Control signals to the slaves indicating cycle activity, strobe, and write enables for transactions.
- `o_saddr`, `o_sdata`, `o_ssel`: Address, data, and select signals sent to the slaves.

### Behavior of the Module

The `wbxbar.v` module's behavior can be divided into several functional parts:

1. **Request Handling**: It decodes incoming requests from the masters and determines which slave each request pertains to. The requests are combined in an arbiter structure to manage concurrent requests.

2. **Arbitration Logic**: The module employs a round-robin or priority-based arbitration strategy to decide which master gets access to which slave. This logic ensures that if multiple masters request data at the same time, they will be served in a fair manner.

3. **Timing and Stalling Management**: The module includes mechanisms to track the number of pending transactions for each master and slave. It carefully manages stalls and acknowledge signals to prevent data loss and ensure reliable communication. If the slave fails to respond within the expected timeframe (based on timeout settings), it generates error signals.

4. **Output Control**: Once a master has been granted access to a slave, the necessary signals (like addresses and data) are transferred appropriately. The module also may register outputs to reduce the combinatorial logic delays and help to meet timing requirements.

5. **Error Handling**: The `wbxbar` module detects various error conditions (e.g., timeouts, incorrect responses) and generates appropriate signals back to the masters to inform them of these situations, executing bus error reporting as necessary.

In summary, the `wbxbar.v` module plays a critical role in ensuring that the various components communicate correctly and efficiently in a CPU architecture using the Wishbone specification, actively managing resources and facilitating productive interactions among multiple masters and slaves.

### File: axilite2axi.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axilite2axi.v
### Description of `axilite2axi.v`

#### Overall Purpose:
The Verilog file `axilite2axi.v` is designed to serve as a bridge between an AXI Lite interface and a full AXI interface within the Zip CPU architecture. It facilitates the conversion of AXI Lite transactions into full AXI transactions, allowing the CPU to interact with peripherals and other external devices that utilize the AXI protocol.

#### Inter-Module Relationships:
The `axilite2axi` module interacts primarily with two different AXI interfaces (an AXI Lite interface and a full AXI interface):
- **Slave AXI interface**: The module receives commands and data from the AXI Lite interface to execute read and write transactions.
- **Master AXI interface**: The module communicates with the full AXI interface for equivalent read and write operations, effectively translating the simpler AXI Lite signals into the more comprehensive set expected by full AXI.

The file also includes sections that integrate with other formal verification modules, confirming the correct behavior between different AXI interfaces. These verification aspects help ensure that the conversion of signals between these interfaces maintains proper transaction logic.

#### Key Signals (Inputs/Outputs):
- **Inputs**:
  - `ACLK`: Clock signal for synchronous operations.
  - `ARESETN`: Active-low reset signal for the module.
  - **Slave AXI Input Signals** (AXI Lite):
    - Signals like `S_AXI_AWVALID`, `S_AXI_AWADDR`, `S_AXI_WVALID`, `S_AXI_WDATA`, etc. are used to receive write commands from the AXI Lite interface.
    - Signals for read operations, such as `S_AXI_ARVALID`, `S_AXI_ARADDR`, along with the response signals `S_AXI_RVALID`, `S_AXI_RDATA`.
  
- **Outputs**: 
  - **Master AXI Output Signals** (Full AXI):
    - Signals like `M_AXI_AWVALID`, `M_AXI_AWADDR`, `M_AXI_WVALID`, `M_AXI_WDATA` are output to represent the corresponding write commands to the full AXI interface.
    - Similarly, signals for read operations like `M_AXI_ARVALID`, `M_AXI_ARADDR`, and response signals including `M_AXI_RVALID`, `M_AXI_RDATA`.

#### Behavior of the Module:
The `axilite2axi` module contains combinational logic that maps the signals from the AXI Lite interface to appropriate signals that conform to the full AXI protocol. 

1. **Address and Data Handling**: The module translates incoming AXI Lite addresses and data into formats suitable for AXI transactions. It manages burst settings, and fixed burst lengths suitable for the AXI Lite signals, as specified by the module parameters.

2. **Control Logic for Write Transactions**:
   - When a write transaction is initiated on the AXI Lite port (`S_AXI_AWVALID`), the corresponding signals (`M_AXI_AWVALID`, etc.) are activated to facilitate the write request to the AXI Master interface.
   - The signal `M_AXI_WLAST` is set to `1`, indicating this is the last word in a burst.

3. **Control Logic for Read Transactions**:
   - Similar control processes occur for read transactions where the read commands and addresses are forwarded from the AXI Lite interface to the full AXI interface. 

4. **Synchronization and Validation**:
   - The module uses ready-valid mechanisms where `READY` signals indicate when the corresponding `VALID` signals can be accepted, ensuring proper synchronization between master and slave interfaces.

5. **Formal Verification**:
   - The module includes assertions and assumptions for verifying its proper functioning using formal methods. These checks ensure that the number of outstanding transactions adheres to the expected AXI protocol behavior, as well as validation of signals under specific conditions to prevent errors.

In summary, the `axilite2axi.v` file implements essential logic to convert and interconnect AXI Lite and full AXI transactions effectively while also providing a framework for testing its correctness through formal verification methodologies.

### File: memdev.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/memdev.v
### Overview of the `memdev.v` File:

#### Purpose:
The `memdev.v` file implements an on-chip memory module for the Zip CPU architecture. This module interfaces with the Wishbone bus, facilitating memory operations such as read and write. It is designed for high-speed access with pipelined transactions that can achieve single-cycle latency for successive memory accesses. It offers flexibility in terms of memory size and behavior, allowing configuration to behave as ROM or RAM depending on parameters.

---

#### Inter-module Relationships:
- **Interaction with the Wishbone Bus**: The memory device communicates with other components of the CPU via the Wishbone protocol, which standardizes data transfer. 
- **Dependency on CPU Signals**: It relies on control signals from the CPU (or other master devices) such as `i_wb_cyc` (wishbone cycle), `i_wb_stb` (strobe signal), `i_wb_we` (write enable), and `i_wb_addr` (address).
- **Connection to Other Modules**: The memory module interacts with various CPU modules that require memory access such as the instruction fetch unit, data fetch unit, and potentially execution units, depending on data and instruction storage.

---

#### Key Signals:
- **Inputs**:
  - `i_clk`: Clock signal for synchronous operation.
  - `i_reset`: Signal to reset the module to a known state.
  - `i_wb_cyc`: Wishbone cycle signal indicating a transaction is ongoing.
  - `i_wb_stb`: Strobe signal to indicate the memory is being accessed.
  - `i_wb_we`: Write enable signal to specify if the operation is a write.
  - `i_wb_addr`: Address where the memory operation is targeted.
  - `i_wb_data`: Data input for write operations.
  - `i_wb_sel`: Byte select input to indicate which parts of the memory should be affected.

- **Outputs**:
  - `o_wb_stall`: Output stall signal indicating whether the device is able to respond immediately.
  - `o_wb_ack`: Acknowledgment signal that indicates when a memory transaction has been completed.
  - `o_wb_data`: Data output for read operations.

---

#### Behavior of the Module:
- **Memory Preloading**: The memory can be preloaded with data from a hex file specified by the parameter `HEXFILE`. This is done during initialization using the `$readmemh` system task.
  
- **Read and Write Operations**: The module supports both read and write operations:
  - For reads, it simply captures the data from the appropriate memory location, indexed by the `i_wb_addr` signal.
  - For writes, conditional on `i_wb_we` and `w_wstb` being active, it uses a loop to write data to the memory array `mem` based on the `i_wb_sel` signal that defines which bytes within the address are valid for writing. 

- **Pipelining**: The design supports pipelined transactions, allowing for a new memory access to be initiated before the previous one has completed (though it should be noted that memory may still experience latency due to the predefined cycle cost of address operations).

- **State Management**: It incorporates simple state management in the form of acknowledgment control. It raises `o_wb_ack` based on the combination of the strobe, cycle, and other conditions, ensuring that it responds appropriately to the Wishbone protocol.

- **Formal Properties Testing**: The module includes blocks for formal verification, ensuring that the assumptions around memory state and response behavior are adhered to, which is critical for maintaining correctness in hardware design.

This `memdev.v` file showcases a well-structured representation of memory in a CPU architecture, emphasizing modularity and compliance with established protocols, which is vital for effective hardware description and design.

### File: axi_tb.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axi_tb.v
### Purpose of the `axi_tb.v` File
The `axi_tb.v` file serves as a comprehensive test bench for evaluating the Zip CPU within various AXI and AXI-Lite configurations. Specifically, it facilitates testing by instantiating necessary peripheral components, such as memory, a console port, an external debug port, and monitoring interfaces, thereby enabling rigorous validation of the CPU's functionality and performance.

### Inter-module Relationships
The test bench interacts extensively with different components of the CPU architecture:

1. **Zip CPU (`zipaxil` / `zipaxi`)**: The test bench utilizes either the AXI or AXI-Lite interfaces to communicate with the CPU. This allows the CPU to perform read and write operations to memory and other peripherals.
   - The CPU's instruction and data buses are connected via AXI interfaces, allowing for dual porting capabilities.
   
2. **Memory (`demofull`)**: The memory module is set up to model memory behavior in response to AXI transactions initiated by the CPU.
   - The memory block handles both read and write operations, interfacing directly with the CPU to support its instruction fetch and data manipulations.
   
3. **Console and Scope Interfaces**: These are added for observing outputs and debugging.
   - The console interacts with the CPU to output simulated data directly to a specified console file.
   - The scope can monitor signals from the CPU for debugging hardware performance and states.

4. **SMP Support**: The file supports optional multiprocessor operations (SMP) by instantiating additional CPUs. Each additional CPU connects to a shared memory interface and maintains AXI connectivity like the primary CPU.

5. **Watchdog Timer**: This is present in the test bench to prevent hanging during simulations, ensuring proper CPU activity and terminating execution if the CPU does not utilize the bus for an extended time.

### Key Signals (Inputs/Outputs)
- **Inputs**:  
    - `i_aclk`: The clock signal.
    - `i_aresetn`: Active-low reset signal.
    - `sim_awvalid`, `sim_wvalid`, `sim_arvalid`: Host signals indicating transaction origins.
    - `i_sim_int`: A signal indicating simulation interrupts.
  
- **Outputs**:  
    - `sim_awready`, `sim_wready`, `sim_arready`: Acknowledgment signals for transactions.
    - `sim_rvalid`, `sim_bvalid`: Responses indicating the validity of read and write operations.
    - `o_prof_stb`, `o_prof_addr`, `o_prof_ticks`: Profiling outputs to monitor the CPU's operational status.

#### Control Logic
The test bench employs various control signals to manage data flow between components and synchronize transactions. A significant characteristic of this module is the use of combinatorial logic to manage and validate the read and write transactions across AXI interfaces.

### Behavior of the Module
1. **Reset and Clock Generation**: The test bench contains instantiate clocks and resets to ensure that all components start in a known state. The generation is done to toggle clock states every 5 ns.

2. **Simulation Flow**: 
   - The CPU initiates read or write transactions through the AXI protocol. The outputs such as `sim_awready` or `sim_wready` allow the bus to acknowledge valid operations.
   - Peripheral data is fetched from a predetermined memory map (using `MEM_FILE`) upon a read request from the CPU.
   - The watchdog timer ensures the CPU is active, automatically terminating the simulation if it hangs in idle.
   
3. **Partitioned Logic**: The AXI control for different peripherals and the core CPU itself is modularized, allowing easy debugging and compartmentalized testing of various segments within the CPU architecture.

4. **State Monitoring**: The interconnections between the console, memory, and the CPU allow for dynamic monitoring of operations in a way that's straightforward to observe via console outputs or debug interfaces.

In conclusion, the `axi_tb.v` file is crucial for validating the functionality of the Zip CPU by emulating a realistic operating environment. It integrates various components, ensuring their correct interaction and allowing thorough testing of both instruction fetching and execution paths.

### File: wb_tb.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/wb_tb.v
The `wb_tb.v` file is a comprehensive testbench designed for the Zip CPU, which is a small, lightweight RISC CPU core. The testbench facilitates the verification of various Wishbone configurations of the CPU, allowing for debugging, performance profiling, and interaction with peripheral devices. Here’s a detailed breakdown of the file's structure and functionality:

### Overall Purpose
The main purpose of `wb_tb.v` is to serve as a top-level test infrastructure for the Zip CPU. It enables simulation of the CPU's behavior by providing essential components such as memory, console ports for displaying output, and external debugging access. This testbench is crucial for executing test programs across different CPU configurations to identify and rectify potential bugs prior to any release.

### Inter-module Relationships
- **CPU Module**: The testbench instantiates either the `zipbones` or `zipsystem` module, both of which define the core structure and behavior of the CPU.
- **Memory Module**: The testbench includes a memory device (`memdev`) that allows the CPU to read from and write to simulated memory.
- **Console Interface**: It has a console module that captures outputs from the CPU to log data into a text file or display it directly in the simulation console.
- **Hardware Peripherals**: Various peripherals like timers and interrupt controllers are instantiated within the testbench to facilitate complete system functionality during testing.
- **Wishbone Interface**: The testbench interacts with a Wishbone bus, enabling communication between the CPU and memory/IO devices. It ensures compliance with the Wishbone protocol, facilitating standard operations such as read/write and acknowledgment signaling.

### Key Signals (Inputs/Outputs)
**Inputs:**
- `i_clk`: The input clock signal to sync operations.
- `i_reset`: Reset signal to initialize the system state.
- Other control signals such as `i_sim_cyc`, `i_sim_stb`, `i_sim_we`, and bus data signals for simulation control, which facilitate external input control during testing.

**Outputs**:
- `o_sim_ack`, `o_sim_data`, `o_sim_err`: Acknowledgment, data output, and error indicators that are returned from the testbench to the simulator.
- Various status signals for peripherals (timers, console, etc.) that indicate their operational state and data readiness.

### Behavior of the Module
The behavior of the testbench includes:
- **Initialization and Simulation Control**: The testbench initializes signals, manages clock toggling, and handles system reset.
- **State Management**: It includes control logic to handle various operational states of the CPU and peripherals. For instance, input signals are monitored to signal the CPU for actions during its operational cycle.
- **Watchdog Timer**: An implementation for a watchdog timer checks for the CPU’s operation state, alerting for timeouts to ensure that the system does not get stuck indefinitely.
- **Data Logging**: The testbench logs outputs to a console and traces CPU activity through various components, which can be useful for debugging and performance assessment.
- **Control Logic for Peripherals**: Various control paths are established to handle reading from and writing to peripheral devices effectively, responding to CPU requests according to the Wishbone bus protocol.

Overall, `wb_tb.v` is effectively designed to facilitate robust testing of the Zip CPU across various configurations and operational scenarios, ensuring that the CPU can function correctly within a fully simulated environment.

### File: axilempty.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axilempty.v
### Purpose of the File

The `axilempty.v` file defines a Verilog module that implements a simplified AXI-lite interface tailored to act as an "empty shell." This shell is designed to be used in bus architectures with masters but without any slaves connected. By implementing this module, the interconnect system can handle requests properly and generate valid responses (such as error returns) without needing a functional slave module, thus simulating a slave's presence on the bus.

### Inter-module Relationships

This module interacts with:
- **AXI-compatible Master Modules:** It connects to master devices on the AXI bus, handling read and write requests sent by these masters.
- **Interconnect Logic:** It plays a role in the interconnect architecture facilitating communication between the masters and other components in the system.

By ensuring  proper response signaling for incomplete or erroneous transactions, it provides a way to maintain system integrity even when slaves are absent. 

### Key Signals (Inputs/Outputs)

**Inputs:**
- `S_AXI_ACLK`: Clock signal for the AXI interface.
- `S_AXI_ARESETN`: Active-low reset signal.
- Various AXI signals including:
  - `S_AXI_AWVALID`: Indicates that a write address is valid.
  - `S_AXI_WVALID`: Indicates that write data is valid.
  - `S_AXI_BREADY`: Indicates the master is ready to accept a response.
  - `S_AXI_ARVALID`: Indicates that a read address is valid.
  - `S_AXI_RREADY`: Indicates the master is ready to accept read data.

**Outputs:**
- `S_AXI_AWREADY`: Indicates that the slave is ready to accept a write address.
- `S_AXI_WREADY`: Indicates that the slave is ready to accept write data.
- `S_AXI_BVALID`: Indicates that the slave has a valid response for the master.
- `S_AXI_BRESP`: Response status for the write transaction.
- `S_AXI_ARREADY`: Indicates that the slave is ready to accept a read address.
- `S_AXI_RVALID`: Indicates that the slave has valid read data for the master.
- `S_AXI_RDATA`: The data being returned for read operations.
- `S_AXI_RRESP`: Response status for the read transaction.

### Behavior of the Module

The module has no actual data processing logic but implements control logic for handling AXI-lite signaling:

1. **Write Signaling:**
   - The module generates signals indicating readiness for write operations. If the write address and data are valid, `S_AXI_AWREADY` and `S_AXI_WREADY` are asserted. 
   - After a successful write, it sets the `S_AXI_BVALID` to indicate that a response is available, which the master can acknowledge via `S_AXI_BREADY`.

2. **Read Signaling:**
   - Similarly, for read operations, it creates a readiness signal for address requests. If a read address is valid, `S_AXI_ARREADY` is asserted. 
   - The read responsiveness is indicated through `S_AXI_RVALID` and the data is always returned as zero since it's an empty shell. It also responds with an error status (`S_AXI_RRESP` set to a specific error code).

3. **State Management:**
   - The control logic uses registers to manage states for write and read operations. It ensures that the responses are consistent and provides logical behavior in the absence of actual data handling capabilities.

Overall, `axilempty.v` acts primarily as a placeholder that can maintain proper AXI signaling protocols, generating accurate responses to bus transactions, aiding in the simulation and design verification processes within a larger CPU architecture.

### File: axi2axilsub.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axi2axilsub.v
### Overview of `axi2axilsub.v`

#### Purpose of the File
The `axi2axilsub.v` file implements a conversion module that translates the AXI (Advanced eXtensible Interface) protocol to the AXI-lite protocol within the Zip CPU architecture. The primary goal of this converter is to maintain performance when transferring data between the AXI and AXI-lite interfaces while possibly reducing the data bus width, depending on the configuration parameters. This module is tailored to support both read and write transactions, facilitating seamless integration between AXI and AXI-lite subsystems.

#### Inter-module Relationships
The `axi2axilsub` module interacts with various components of the CPU architecture:
- It interfaces with AXI4 slave elements and acts as a bridge to AXI-lite master interfaces. 
- It utilizes sub-modules such as `axi2axilite`, which encapsulates the logic necessary to handle read and write transactions.
- Through signals and handshaking, it integrates with FIFOs (First In, First Out) for managing data buffering, ensuring that data rates and flow remain efficient.
- The formal verification portion of the module enables it to work within a formal proof framework, guaranteeing correctness in its operation.

#### Key Signals
- **Inputs:**
  - `S_AXI_ACLK`: Clock signal for the slave AXI interface.
  - `S_AXI_ARESETN`: Active-low reset input for the slave AXI interface.
  - `S_AXI_*`: Various inputs for the AXI4 protocol, including:
    - Address, data, and control signals for both write and read transactions (`S_AXI_AWVALID`, `S_AXI_WVALID`, `S_AXI_ARVALID`, etc.)
  
- **Outputs:**
  - `M_AXI_*`: Corresponding outputs for the AXI-lite protocol:
    - Address and control signals for the AXI-lite master (`M_AXI_AWVALID`, `M_AXI_WVALID`, `M_AXI_ARVALID`, etc.).
  - Transaction response signals like `S_AXI_BVALID`, `S_AXI_RVALID`, indicating the validity of responses from the AXI-lite master.

#### Behavior of the Module
The behavior of the module is defined through several control logic segments implemented via combinational and sequential logic:
- **Write Logic:**
  - It handles incoming write requests on the AXI interface and translates them into compatible AXI-lite write requests, managing the state through local registers and FIFOs.
  - Includes mechanisms for handshaking, FIFO management for write data, and response handling as it tracks the completion of writes.

- **Read Logic:**
  - Manages read requests by converting AXI read transactions into AXI-lite format. It serves incoming read commands and outputs the data requested.
  - It incorporates robust state tracking for read transactions including counters for remaining transfer beats and addressing for sequential data retrieval.
  - Handles the synchronization between AXI read requests and corresponding AXI-lite responses to ensure continuity and avoid data underruns or overruns.

- **Control Flow and State Machines:**
  - The module exhibits control flow through various state machines that dictate the current status of transactions (e.g., reading, writing, idle). Each component responds to FIFO statuses and AXI signals to ensure conformance to protocol timing requirements.
  - The use of skid buffers enables the smoothing out of data transfer by allowing the module to hold data in a buffer until it is ready to send or receive, thereby preventing bottlenecks.

#### Conclusion
In summary, the `axi2axilsub.v` module plays a critical role in enabling effective communication and data handling between AXI and AXI-lite interfaces in the Zip CPU architecture. Through rigorous handling of input/output signals and robust control mechanisms, it ensures high performance and minimal latency while conforming to various protocol specifications.

### File: wbscope.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/wbscope.v
### Description of `wbscope.v`

#### Overall Purpose
The `wbscope.v` file implements a bus-accessed logic analyzer (or scope) for a CPU architecture, specifically designed to capture and analyze 32-bit data values as they traverse through the system. It records values on clock ticks when enabled and provides a mechanism to read the recorded data after a trigger condition is met. This module facilitates debugging by allowing observations of internal bus activity during simulation or operation.

#### Inter-module Relationships
Within the CPU architecture, `wbscope.v` interacts primarily with other components via the WISHBONE bus interface:
- It acts as a peripheral that collects data from the main CPU logic during operation.
- It receives control signals and data inputs from the CPU through the WISHBONE bus, enabling it to start recording, reset, and configure parameters.
- The recorded data can be read back by other modules (like a CPU or testbench) using the same WISHBONE interface.

#### Key Signals (Inputs/Outputs)
**Inputs:**
1. **`i_data_clk`**: Main signal used for data input clock.
2. **`i_ce`**: Chip enable signal, determining if the scope should be active and responding to data.
3. **`i_trigger`**: Trigger signal that, when asserted, indicates that recording should stop after a specific hold-off period.
4. **`i_data`**: The data input line from which the scope records values.
5. **WISHBONE bus control signals**:
   - **`i_wb_clk`**: Clock signal for the WISHBONE bus.
   - **`i_wb_cyc`, `i_wb_stb`, `i_wb_we`**: Control signals indicating a bus cycle, a valid strobe, and a write operation, respectively.
   - **`i_wb_addr`**: Address line for WISHBONE (1-bit).
   - **`i_wb_data`**: Data input for configuration/commands over the WISHBONE bus.
   - **`i_wb_sel`**: Select lines for byte-enable (for 32-bit data).

**Outputs:**
1. **`o_wb_stall`**: Signal to indicate that the WISHBONE bus is stalled.
2. **`o_wb_ack`**: Acknowledge signal for WISHBONE operations.
3. **`o_wb_data`**: Data output from the scope to the WISHBONE bus for read operations.
4. **`o_interrupt`**: An interrupt signal for the CPU, indicating that recording has stopped, contingent on whether triggers are disabled.

#### Behavior of the Module
The `wbscope` module consists of several key state-based behaviors and processes:
1. **Configuration Handling**: The module can be initialized and configured through the WISHBONE bus. Control registers manage settings like hold-off times and trigger conditions.
2. **Recording Mechanism**:
   - Uses `i_data_clk` to capture data when enabled; records values to a circular buffer until the trigger is asserted.
   - Implements a hold-off timer that counts down after a trigger has been received.
3. **Data Management**:
   - A counter keeps track of how many values have been recorded.
   - Memory is organized as a circular buffer that allows data values to be overwritten when full. The write address is managed to accommodate sequential data storage.
4. **State Logic**:
   - States like **stopped**, **triggered**, and **primed** are defined to manage the recording states. If a trigger occurs, recording continues for a few cycles as defined by the hold-off before stopping.
   - The output flags related to these states (like `o_interrupt`) notify the CPU regarding the status of recording, allowing the system to respond appropriately.

Overall, the `wbscope.v` module provides a valuable tool for debugging and performance monitoring within the CPU architecture, helping developers visualize the internal workings and data flows of their designs.

### File: iscachable.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/iscachable.v
### Overall Purpose of the File

The `iscachable.v` file implements a combinatorial logic module that determines whether a specific address is cacheable in the Zip CPU architecture. It uses a combination of a memory address and a mask to assess if the given input address (`i_addr`) satisfies the condition required to be categorized as cacheable. The output is a single signal, `o_cachable`, which indicates whether caching can occur for the provided address.

### Inter-module Relationships

The `iscachable` module is designed specifically to support the functionality of data cache (dcache) operations and could also have implications for formal verification properties. It serves as a utility in the CPU architecture, offering a clean interface for other modules—primarily the data cache controller or any module that requires a decision on address cacheability.

Other modules in the architecture, particularly those handling memory requests and data caching, would interact with `iscachable` to determine whether they should cache the data being accessed at a given address. The integration of this module helps ensure that only valid cacheable addresses are processed, streamlining data retrieval and potentially improving performance through efficient memory access.

### Key Signals (Inputs/Outputs)

1. **Inputs:**
   - `i_addr [AW-1:0]`: This represents the address input to the module where caching is being evaluated. The address width is parameterized, allowing flexibility in the design to accommodate different address sizes.

2. **Outputs:**
   - `o_cachable`: This is a one-bit output that indicates whether the address provided via `i_addr` is cacheable (`1`) or not (`0`). It is a registered output, meaning it holds its state until it is updated.

### Behavior of the Module

The module utilizes an `always @(*)` block, which is triggered any time there is a change to its inputs. The logic within this block works as follows:

- The output signal `o_cachable` is initially set to `0`.
- It then checks two conditions:
  - If `MEM_ADDR` (the memory address defined for cacheability) is not zero.
  - If the bitwise AND operation between the incoming address `i_addr` and `MEM_MASK` results in `MEM_ADDR`.
  
If both conditions are satisfied, it sets `o_cachable` to `1`. This logic ensures that the output reflects the cacheability of the input address according to the defined memory address and mask.

The nature of the logic is combinational, which means there are no state machines or sequential elements involved in the operation of this module. It simply evaluates the conditions provided in real-time as the inputs change, leading to an immediate response regarding address cacheability. This design choice is vital for maintaining high performance and minimal latency within the CPU architecture, especially in memory transactions that involve caches. 

### Summary

In summary, the `iscachable.v` file functions as a crucial decision-making module in the Zip CPU architecture, determining if addresses are eligible for caching based on specific criteria. Its combinatorial logic ensures quick evaluations, and its output directly influences memory subsystem interactions, contributing to the overall efficiency of the CPU's operation concerning memory access and data caching strategies.

### File: axilcon.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axilcon.v
### Purpose of the File
The `axilcon.v` file implements a basic AXI-Lite console port controller. It serves as an interface for communication between the CPU and the external environment. Specifically, it has a similar functionality to the WBUART core within the same project directory, allowing data transmission and reception through an AXI-Lite interface, which is typically used for low-bandwidth control register operations.

### Inter-module Relationships
The `axilcon` module interacts with other components in the CPU architecture, primarily via the AXI-Lite protocol. Its primary role is to facilitate communication with peripheral devices or external systems that require control and status registers, such as UART devices. 

- **AXI Master/Slave Interaction**: The `axilcon` module acts as an AXI-Lite slave that responds to read and write operations initiated by an AXI master (which could be part of the CPU core). 
- **Console Interaction**: The module has a console file option (`CONSOLE_FILE`) that it can utilize for logging, enabling it to write data to an external file for debugging or monitoring purposes.
  
### Key Signals
The key signals for the `axilcon` module include:

#### Inputs:
- `S_AXI_ACLK`: Clock signal for the AXI interface.
- `S_AXI_ARESETN`: Active-low reset signal for the AXI interface.
- `S_AXI_AWVALID`: Indicates that a write address is valid.
- `S_AXI_AWADDR`: Write address for the AXI-Lite transaction.
- `S_AXI_WVALID`: Indicates that write data is valid.
- `S_AXI_WDATA`: Data to be written.
- `S_AXI_WSTRB`: Write strobe for byte selection.
- `S_AXI_ARVALID`: Indicates that an address for read is valid.
- `S_AXI_ARADDR`: Read address for AXI-Lite transaction.
- `S_AXI_RREADY`: Indicates that the master is ready to receive data.

#### Outputs:
- `S_AXI_AWREADY`: Indicates that the slave is ready to accept a write address.
- `S_AXI_WREADY`: Indicates that the slave is ready to accept write data.
- `S_AXI_BVALID`: Indicates that a write response is valid.
- `S_AXI_BRESP`: Write response from the slave.
- `S_AXI_ARREADY`: Indicates that the slave is ready to accept a read address.
- `S_AXI_RVALID`: Indicates that read data is valid.
- `S_AXI_RDATA`: Data being read from the slave.
- `S_AXI_RRESP`: Read response from the slave.

### Behavior of the Module
The `axilcon` module has several behavior components and control logic:

1. **Reset Handling**: The module is driven by the `S_AXI_ARESETN` signal. When the reset condition is active (reset low), certain state variables are initialized accordingly.

2. **AXI-Lite Write Process**:
   - The module implements write logic that processes incoming write requests from the AXI master. If the `S_AXI_AWVALID` and `S_AXI_WVALID` signals are both valid at the same time, the module asserts `S_AXI_AWREADY` and `S_AXI_WREADY` after checking internal conditions.
   - If the address corresponds to the `UART_TXREG`, the module writes the data to the UART console or writes it back to the console file if specified.

3. **AXI-Lite Read Process**:
   - For read requests, the module supports whether to use a skid buffer. If the address is valid (`S_AXI_ARVALID`), the module sets `S_AXI_ARREADY` accordingly. It then prepares for read replies based on which internal register was accessed.
   - The read data is set according to the address requested (`UART_RXREG`, `UART_TXREG`, etc.).

4. **Response Handling**:
   - The response signals (`S_AXI_BVALID` and `S_AXI_RVALID`) are managed through logic that ensures they correctly indicate the readiness of data to be read or acknowledged after a write.

5. **Logging and Communication**:
   - The module integrates file I/O functionality via `sim_console`, allowing transmission of characters through the AXI-Lite bus, including handling of LF (line feed) to flush the console output.

### Conclusion
Overall, the `axilcon` module serves as a critical interface for interaction with external systems through the AXI-Lite protocol. It handles both read and write requests efficiently while providing optional logging mechanisms, crucial for monitoring and debugging within the CPU system.

### File: demofull.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/demofull.v
### Description of demofull.v

**Overall Purpose:**
The `demofull.v` file implements a functionality for a formally verified AXI4 core that serves as a basic interface for integrated circuits in the Zip CPU project. It has been designed for high throughput, allowing one beat of data transfer per clock cycle for both read and write transactions. The module manages data transfers between a master device and a slave device according to the AXI4 protocol, providing necessary address and control signal handling.

**Inter-Module Relationships:**
The `demofull` module interacts with various other components within the CPU architecture, including:
- **AXI Address Module** (`axi_addr`): This module computes the next addresses for read and write operations based on current configurations such as burst size and length.
- **Skid Buffer Module** (`skidbuffer`): This component helps manage and buffer write and read requests, ensuring proper timing and synchronization in the data transfer.
- **Faxi Slave**: A dedicated formal verification module that checks compliance with the AXI protocol. It ensures that the transactions meet the protocol's specifications and behaves correctly with regard to signals.

The interaction between these modules allows the `demofull` to efficiently handle ongoing transactions while maintaining protocol integrity and performance.

**Key Signals (Inputs/Outputs):**
- **Inputs:**
  - `S_AXI_ACLK`: Clock signal for the AXI interface.
  - `S_AXI_ARESETN`: Active low reset signal.
  - Transaction signals such as `S_AXI_AWVALID`, `S_AXI_WVALID`, and `S_AXI_ARVALID` indicate the presence of valid address and data ready for write or read operations.

- **Outputs:**
  - `S_AXI_AWREADY`, `S_AXI_WREADY`, and `S_AXI_ARREADY`: Indicate the readiness of the slave device to accept write addresses, write data, and read addresses, respectively.
  - `S_AXI_BVALID`, `S_AXI_RVALID`: Signals that indicate valid responses for write and read transactions.
  - Other signals such as `S_AXI_BRESP`, `S_AXI_RDATA`, `S_AXI_RRESP` convey the status of transactions and the actual data read from the slave.

The major user-facing outputs include `o_we`, `o_raddr`, `o_wdata`, and `o_wstrb`, which provide necessary data to be used by the rest of the CPU architecture.

**Behavior of the Module:**
The `demofull` module incorporates control logic and state management to handle the AXI transactions:
- **Write Processing**: The module manages write requests by first confirming that write addresses are valid. It buffers the write data and generates the corresponding write signals while taking into account the conditions such as burst length and exclusive access (if enabled).
- **Read Processing**: Similar to write, read requests are handled by accepting read addresses and generating the read responses. The module utilizes a skid buffer to manage timing between requests and responses, ensuring that read data is available in line with AXI timing requirements.
- **Exclusive Access Handling**: If enabled, the module has mechanisms to manage exclusive access to certain addresses, indicating when other operations might need to back off or yield access.
- **Latency Management**: The module accounts for different latencies introduced by both the read and write paths and manages the transition between states such that the protocol is followed without conflicts.

In summary, the `demofull.v` module is a sophisticated interface designed to handle AXI transactions efficiently while ensuring compliance with the AXI4 protocol, supported by extensive signal management, state control, and integration with other modules in the CPU architecture.

### File: axilscope.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axilscope.v
### Overall Purpose of `axilscope.v`

The `axilscope.v` file implements a generic logic analyzer (or bus-accessed "scope") for an FPGA design. Its primary function is to monitor and record the transit of 32-bit data values across the bus. The module provides facilities to start recording data when specific conditions are met (e.g., a trigger signal) and enables the user to subsequently read back the recorded values. It is a debugging tool that helps in analyzing bus transactions or signals during simulation and hardware prototyping.

### Inter-Module Relationships

The `axilscope` module interacts with various components within a CPU architecture, particularly those that communicate over an AXI bus. It acts as an AXI slave, meaning it responds to requests from a master device (usually a CPU or other control unit). The connections to AXI signals allow it to receive commands for starting and stopping data recording and to provide read-back capabilities for the recorded data. Here's how it integrates with other system components:

- **AXI Interface**: The signals prefixed with `S_AXI_` are tied to the AXI protocol, which enables communication with the CPU or other master devices.
- **Clock and Reset Signals**: It uses external clocks (`S_AXI_ACLK`, `i_data_clk`) and reset signals (`S_AXI_ARESETN`) for timing and control. The module must synchronize data recording with these clocks.
- **Trigger Inputs**: The module's behavior is influenced by other system components through trigger and enable signals (`i_trigger`, `i_ce`), allowing external control to dictate when data should be recorded.

### Key Signals (Inputs/Outputs)

- **Inputs**:
  - `i_data_clk`: The clock for timing data recording.
  - `i_ce`: Indicates when valid data is present for recording.
  - `i_trigger`: Active high signal for triggering data capture.
  - `i_data`: The 32-bit data input to be recorded.
  - AXI interface signals (`S_AXI_*`) for address, data, and control operations.

- **Outputs**:
  - `o_interrupt`: Indicates when the scope has stopped recording data.
  - AXI responses (`S_AXI_*`) for read/write operations indicate data transactions and responses sent back to the master.

### Behavior of the Module

The module behavior can be broken down into several key functionalities:

1. **Trigger and Recording Logic**: When `i_trigger` is asserted, and `i_ce` is true, the module begins recording data into a circular buffer. It continues to record until it detects a stop condition, which typically occurs once the data from a certain number of cycles (defined by `br_holdoff`) is captured after the trigger signal.

2. **Buffer Management**: The data is stored in memory (implemented as an array of registers). The writing to this memory is controlled by the `i_data_clk`, and addresses (`waddr`, `raddr`) are tracked for reading historical data or writing new data.

3. **Reset and Control Signals**: The module has mechanisms to handle resets (`S_AXI_ARESETN`) gracefully, clearing out any state and stopping recordings. Control signals allow configurations related to triggering and hold-off timers.

4. **Read Operation**: The module interfaces through the AXI protocol to allow external devices to read back recorded data from the buffer. It uses dedicated AXI read signals to respond with the data to be returned.

5. **State Signals**: The module maintains several flags and registers to track the state of recording (e.g., whether it is actively recording, stopped, or triggered). It uses these to correctly respond to external requests and manage data flow.

Overall, the `axilscope` module serves as a crucial diagnostic tool that integrates various elements within the architecture, facilitating a deeper understanding of how data flows through the CPU and assisting in the debugging process.

### File: axiempty.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axiempty.v
### Overview of the Verilog File: `axiempty.v`

#### Purpose
The `axiempty.v` file implements a basic AXI (Advanced eXtensible Interface) core that serves as a placeholder in a system where no other slaves are connected to the AXI bus. This core responds to incoming requests from an AXI master by generating bus errors for all operations, effectively indicating that there are no available slaves to handle the transactions.

#### Inter-module Relationships
The `axiempty` module interacts with other components of the CPU architecture that utilize the AXI bus for communication, such as peripherals or memory controllers. It is designed to fit into systems where AXI masters may attempt to perform read and write operations, but in the absence of functioning slave devices, the `axiempty` module allows for proper transaction handling by sending error responses. 

This module typically interacts with AXI master modules, which generate the AXI transactions, and expects those transactions on its interface. The outputs from `axiempty` feed back into the AXI master, helping it to handle or report errors appropriately.

#### Key Signals

1. **Inputs:**
   - `S_AXI_ACLK`: The input clock signal for the AXI interface.
   - `S_AXI_ARESETN`: The active-low reset signal to initialize the module.
   - `S_AXI_AWVALID`: Indicates that the write address is valid.
   - `S_AXI_WVALID`: Indicates that write data is valid.
   - `S_AXI_BREADY`: Indicates that the master can accept a response.
   - `S_AXI_ARVALID`: Indicates that a read address is valid.
   - Other control signals related to AXI transactions (AWID, WLAST, ARID, ARLEN).

2. **Outputs:**
   - `S_AXI_AWREADY`: Indicates readiness to accept a write address.
   - `S_AXI_WREADY`: Indicates readiness to accept write data.
   - `S_AXI_BVALID`: Indicates that a response to a write operation is valid. 
   - `S_AXI_BID`: Provides the ID for the response sent back to the master (Error response ID).
   - `S_AXI_BRESP`: Provides the response status, which is set to indicate a bus error.
   - `S_AXI_ARREADY`: Indicates readiness to accept a read address.
   - `S_AXI_RVALID`: Indicates that the read data is valid.
   - `S_AXI_RDATA`: Provides read data (always zero as there is no actual data to send).
   - `S_AXI_RRESP`: Indicates a response status for read transactions (also set to indicate a bus error).
   - `S_AXI_RLAST`: Indicates the last read transfer.

#### Behavior
The module implements control logic to handle write and read operations from the AXI master. In essence:

- **Write Logic**: 
  - Utilizes double buffering to accept the incoming write address and data through a skid buffer mechanism. Whenever a valid write operation is detected, it sets the `S_AXI_BVALID` and indicates that a bus error (`S_AXI_BRESP` is `2'b11`) occurred.
  
- **Read Logic**: 
  - Reads are processed similarly, where the read address requests are watched, and a corresponding response is generated. When a read address is received, the module sets `S_AXI_RVALID` and responds with a zero data value (`S_AXI_RDATA`) and a read error status (`S_AXI_RRESP`); `S_AXI_RLAST` indicates the last read transfer, which is trivially determined.
  
- **Control Signals**: 
  - The module relies on internal state machines to track valid signals and readiness for both read and write operations. These internal registers help manage buffering and maintaining correct handshake signals between AXI master and the empty slave.

This structure ensures that the AXI requests are handled gracefully, even in the absence of actual slave devices, thus helping to simulate a complete AXI system during modeling or testing.

### File: axi_addr.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axi_addr.v
### Overview of `axi_addr.v`

**Overall Purpose:**
The `axi_addr.v` file implements the address calculation logic for AXI (Advanced eXtensible Interface) compliant systems. It handles the complexities of address generation in different AXI addressing modes, including FIXED, INCREMENTing, and WRAP addressing. The module calculates the next address to be accessed during a data transfer, ensuring that addresses are correctly aligned according to AXI protocol requirements.

**Inter-module Relationships:**
This module interacts primarily with other components of the AXI interface within the CPU architecture, potentially including modules responsible for AXI signals such as `axilpipe`, `axidcache`, or `zipaxi`. It is part of the broader memory management and data transfer logic that aligns with AXI's requirements for address handling. It may receive signals from modules that generate control signals regarding burst types and sizes, and it subsequently outputs the calculated address to downstream AXI components involved in data transactions.

**Key Signals (Inputs/Outputs):**
- **Inputs:**
  - `i_last_addr`: The address of the last beat in the current burst.
  - `i_size`: A 3-bit input that specifies the data transfer size (1 byte, 2 bytes, 4 bytes, etc.).
  - `i_burst`: A 2-bit code that indicates the type of burst (fixed, incrementing, wrap).
  - `i_len`: The length of the burst, defining how many beats will occur in this transaction.

- **Output:**
  - `o_next_addr`: The calculated next address to be used for the subsequent data transfer, which reflects the adjustments based on the input parameters.

**Behavior of the Module:**
The behavior of the `axi_addr` module is primarily combinatorial. It does not contain state machines but instead uses combinational logic to compute values based on its inputs:

1. **Address Increment Logic:**
   - The module calculates how much to increment the address (`increment`) based on the size and type of the data transfer. The logic accommodates different data widths depending on the target architecture.

2. **Wrap Mask Calculation:**
   - For wrap burst mode, it constructs a `wrap_mask`, which helps determine which bits of the address will remain fixed and which bits will change. This ensures the wrap-around addressing follows correct boundaries as per the AXI specification.

3. **Next Address Calculation:**
   - The output address (`o_next_addr`) is computed by adding the `increment` to the last address (`i_last_addr`). Additional logic ensures that the address is aligned according to the transaction size and burst type:
     - Increments are adjusted based on alignment requirements (e.g., ensuring that a 4-byte transfer aligns to a 4-byte boundary).
     - If the burst type is WRAP, the address wraps around to an appropriate value based on the `wrap_mask`.
     - The module finalizes the `o_next_addr` by ensuring that any bits above a specific boundary (often 4kB) remain unchanged.

4. **Unused Logic Warning:**
   - The module also includes provisions to suppress warnings from synthesis tools regarding unused signals, signaling good design practices by addressing potential lint or synthesis issues.

Overall, the `axi_addr` module serves a critical role in ensuring that address computations comply with AXI protocol constraints and contribute effectively to the data transaction processes within AXI-compliant CPU architectures.

### File: axixbar.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axixbar.v
### Description of `axixbar.v`

#### Overall Purpose of the File:
The `axixbar.v` file implements a crossbar switch for AXI (Advanced eXtensible Interface) interconnects. This module facilitates communication between multiple AXI masters (sources) and AXI slaves (destinations), allowing any master to send data to any slave as long as the latter is not busy. It is designed to handle read and write transactions with specific accounts of latency and bus control mechanisms, ensuring efficient data flow across the interconnected components while managing bus contention scenarios.

#### Inter-module Relationships:
The `axixbar` module interacts with several external components:
- **AXI Masters:** It receives address and data signals from multiple AXI master devices, managing write and read requests.
- **AXI Slaves:** It forwards these requests to the appropriate AXI slave devices based on the address decoding, then receives responses from the slaves.
- **Arbiters:** The design incorporates arbiter logic that manages which master gets access to a given slave when multiple masters attempt concurrent transactions.
- **Subsystem Modules:** It includes references to various helper modules like `addrdecode` for address decoding and `skidbuffer` for handling request steady-state conditions.

#### Key Signals:
- **Inputs:**
  - `S_AXI_ACLK`: Clock signal for synchronous operation.
  - `S_AXI_ARESETN`: Active-low reset signal.
  - `S_AXI_AW*`: Signals related to write address transactions (e.g., `S_AXI_AWVALID`, `S_AXI_AWADDR`).
  - `S_AXI_W*`: Signals related to write data transactions (e.g., `S_AXI_WVALID`, `S_AXI_WDATA`).
  - `S_AXI_AR*`: Signals related to read address transactions (e.g., `S_AXI_ARVALID`, `S_AXI_ARADDR`).

- **Outputs:**
  - `M_AXI_AW*`: Signals forwarded to AXI slaves about write address transactions.
  - `M_AXI_W*`: Signals forwarded to AXI slaves about write data transactions.
  - `M_AXI_B*`: Response signals from AXI slaves regarding write transactions (e.g., `M_AXI_BVALID`, `M_AXI_BRESP`).
  - `M_AXI_AR*`: Signals forwarded to AXI slaves regarding read address transactions.
  - `M_AXI_R*`: Response signals from AXI slaves regarding read transactions (e.g., `M_AXI_RDATA`, `M_AXI_RRESP`).

#### Behavior of the Module:
The `axixbar` operates using a combination of combinatorial logic and clocked (sequential) logic to:
1. **Handle Write Transactions:** It uses skid buffers to manage incoming write requests and decodes addresses to determine the target slave. It employs an arbiter for managing simultaneous requests from different masters to the same slave.
2. **Handle Read Transactions:** Similar to write requests, it captures read requests, performs address decoding, and uses an arbiter to resolve conflicts among multiple masters requesting access to the same slave.
3. **Arbitrate Access:** The module includes complex arbiter logic to ensure that requests are handled fairly based on priority. The conditions for granting access to a master include checking if another master is using the channel, if responses have been received, and if the slave is ready.
4. **Manage Latency:** It accounts for latencies inherent in the AXI protocol, introducing state machines to manage request acknowledgment and response transmission states and managing buffers to maintain correct transaction order.
5. **Error Handling:** The module includes provisions for responding to potential errors during address mapping or transaction processing, generating error responses as needed.

The crossbar effectively provides a versatile and manageable interconnect network for AXI-based CPUs, enabling a scalable architecture while maximizing data throughput and minimizing latency.

### File: axi2axilite.v
- **Path**: /Users/frankliu/Desktop/fa24/Takehome/bronco-zipcpu/sim/rtl/axi2axilite.v
### Purpose of the File

The `axi2axilite.v` file implements a bridge module that converts signals from the AXI interface to the AXI-Lite interface. The design aims to achieve a seamless conversion while maintaining a one-clock-per-transaction performance and providing compatibility for AXI-Lite communications. This module is useful for interfacing components within the Zip CPU architecture that require AXI-Lite connections while also ensuring compatibility with the broader AXI protocol.

### Inter-module Relationships

The `axi2axilite` module interacts with both the AXI and AXI-Lite interfaces, functioning as a translator between them. It interfaces specifically with AXI agents under the following categories:

- **AXI Slave Interfaces:** This module listens to incoming AXI commands from a master device and translates them into AXI-Lite commands for downstream components.
- **AXI-Lite Master Interfaces:** It generates appropriate signals for AXI-Lite transaction responses, enabling communication with AXI-Lite downstream devices.

Moreover, the module connects to FIFO buffers for managing read and write operations, assisting in the flow of data between different clock domains and ensuring reliable data transfer.

### Key Signals (Inputs/Outputs)

#### Inputs:
- **Clock and Reset Signals:**
  - `S_AXI_ACLK`: The clock signal for AXI transactions.
  - `S_AXI_ARESETN`: Active low reset signal.

- **AXI Write Address Channel Signals:**
  - `S_AXI_AWVALID`, `S_AXI_AWID`, `S_AXI_AWADDR`, `S_AXI_AWLEN`, `S_AXI_AWSIZE`, `S_AXI_AWBURST`, etc.

- **AXI Write Data Channel Signals:**
  - `S_AXI_WVALID`, `S_AXI_WDATA`, `S_AXI_WSTRB`, etc.

- **AXI Read Address Channel Signals:**
  - `S_AXI_ARVALID`, `S_AXI_ARID`, `S_AXI_ARADDR`, `S_AXI_ARLEN`, `S_AXI_ARSIZE`, etc.

- **AXI Read Data Channel Signals:**
  - `M_AXI_RVALID`, `M_AXI_RREADY`, `M_AXI_RDATA`, etc.

#### Outputs:
- **AXI-Lite Write Address Channel Signals:**
  - `M_AXI_AWVALID`, `M_AXI_AWADDR`, `M_AXI_AWPROT`, etc.

- **AXI-Lite Write Data Channel Signals:**
  - `M_AXI_WVALID`, `M_AXI_WDATA`, `M_AXI_WSTRB`, etc.

- **AXI-Lite Read Address Channel Signals:**
  - `M_AXI_ARVALID`, `M_AXI_ARADDR`, `M_AXI_ARPROT`, etc.

- **AXI-Lite Read Data Channel Signals:**
  - `S_AXI_RVALID`, `S_AXI_RDATA`, `S_AXI_RRESP`, etc.

### Behavior of the Module

The behavior of the `axi2axilite` module can be broken down into several key areas:

1. **Transaction Handling:**
   - The module processes incoming AXI transactions by using skid buffers to handle valid and ready signals while accommodating different clock domains and ensuring proper data flow.

2. **State Machines:**
   - The design includes state management logic for controlling the transitions between different states of read and write operations, essentially acting as a controller that assigns signals based on the readiness of AXI and AXI-Lite interfaces.

3. **FIFO Management:**
   - The module incorporates FIFO buffers to store IDs and count transactions of messages waiting to be processed. This enables the efficient handling of multiple outstanding transactions, enhancing throughput and reducing latency.

4. **Error and Response Handling:**
   - The design manages both AXI and AXI-Lite responses, providing error handling such as SLVERR for error cases, and it updates response signals depending on transaction states.

5. **Timing and Control Logic:**
   - Timing control is crucial, as the module carefully sequences signal activations based on clock cycles and acknowledges signals for writes and reads, ensuring data integrity during transactions.

This complex interplay of operations allows the `axi2axilite` module to effectively bridge AXI transactions into a compatible form for AXI-Lite usage, accommodating the needs of various components within the CPU architecture.

