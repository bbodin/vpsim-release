# Thank you for trying out VPSim: Virtual Prototyping Simulator!
VPSim environment to test or validate the generated binaries and other files in a release-like environment.

**NOTE:** This repo is a submodule of VPSim main repository.
To set-up the full VPSim environment, please refer to the parent repository: [VPSim main repo](https://github.com/CEA-LIST/VPSim.git)

## VPSim features:

- The running Linux kernel on top of the simulated architecture allows for up to 256 simulated cores.
- Detailed memory hierarchy counters: NoC performance counters: number of packets and contention delay per router, Read/Write counters per memory controller, details of each cache level L1, L2 & L3, ...
- The cache hierarchy is endowed with an MSI directory-based coherence protocol and the NoC model accounts for network contention at a router basis.
- Memory address N-way interleaving: default enabled when the memory hierarchy is simulated and can be disabled in the 'off-chip-memory' section using the 'with-interleave' entry.
- Qemu Devices integration in order to account for the impact of I/O transfers on NoC performance and memory accesses. A device can be declared in the 'IODevs' entry of the configuration file.
- Automatic dump to the host machine of the result of a sesam benchmark command performed on the guest Linux. Result files will appear as `sesamBench_<name_of_application>_0.log`, `sesamBench_<name_of_application>_1.log`, `sesamBench_<name_of_application>_...` in the associated `./bin/` directory.

## Demo Package Contents
- **bin (/bin):** Contains vpsim binary. After each simulation run, a specific folder is created here with files & results of the simulated architecture.
- **lib (/lib):** holds the modified qemu library (`./qemu/vpsim-qemu.so`)
- **GPP (/GPP):** Contains configuration python scripts as well as linux kernel and disk image. Configure and simulate a multi-core ARMv8 system running a minimal operating system.
- **Python (/Python):** 
    - `Platforms/armv8_platform.py`: gives a versatile, generic ARMv8 System script that generates and configures its components based on a higher-level description. In order to abstract away for the user the whole work of composition.
    - `Libs/dt.py`: generates the Device Tree to automate the process of configuring hardware components for the simulated architecture.
    - `Libs/vpsim.py`: generates the final `xml` of the simulated architecture.
- **SESAM userspace (/SESAM_userspace)**: source code for a user space software tool used to control over the simulator for monitoring purposes and collect statistics following the execution of a specific user application and makes it possible to perform an entire exploration task.

## Installation

If not already done, please follow the steps in the parent repo README to install the VPSIM binaries.
If the installation runs properly, you should have the main compilation targets:

- `vpsim-release/bin/vpsim` the main application binary.
- `vpsim-release/lib/qemu/vpsim-qemu.so` shared library of the modified QEMU compatible with VPSim.


### Requirements
- You will need to install `dtc` device tree compiler and `zip`:

    ```sh
    apt install device-tree-compiler zip
    ```
Once the package has been properly installed, be sure to have it available and if not, add the path of the dtc executables (something like `.../dtb/usr/bin`) to your `PATH` environment variable.

### Configure
Once you verified the existence of these two main compilation targets, you need to configure your environment variables. This is done, depending on your own shell, by sourcing from the `vpsim-release` folder either the (`setup.sh`) bash script or the (`setup.csh`) csh script.


1. Configure environment variables by sourcing the (`setup.sh`) script:

    ```sh
    source setup.sh
    ```

    - **NOTE**: This command must be run in the root directory of VPSim release.
    - **NOTE**: The disk image `busybox.qcow2` will be unzipped if not already done in the convenient path.
    - **NOTE**: An environment variable named `$VPSIM_HOME` will be set to point to the root directory of VPSim.
    - **NOTE**: `setup.sh` will not modify your `~/.bashrc`. You need to re-source `setup.sh` each time you change the terminal.

## Getting Started

VPSim provides a user-friendly interface to compose and build virtual platforms using an in-house DomainSpecific Language (DSL) based on Python. The tool takes as input a high-level platform description (Python script) together with
the software binaries to be executed on the virtual platform.

1. Move to ([vpsim-release/GPP](./GPP)) directory and run your first simulation:

    ```sh
    python3 gpp.py
    ```

    - This should boot the Busybox Linux on an ARMv8 system with internet connectivity.
    - Login as `root` (no password).
    - To end the simulation, enter the following command in your simulated userspace:

    ```sh
    sesam quit
    ```

    - Dive in `gpp.py` to see how to customize your own architecture

## Getting to know more about VPSim
For further examples and to know more about VPSim, please check the `README.md` file in the [vpsim-release/GPP](./GPP) folder.