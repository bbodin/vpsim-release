"""
Copyright (C) 2024 Commissariat à l'énergie atomique et aux énergies alternatives (CEA)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0 

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from armv8_platform import FullSystem
import os

gpp_home = os.path.join(os.environ['VPSIM_HOME'], 'GPP')

conf = {
    'platform_name': 'GPP_VP',
    'device_tree_template': os.path.join(gpp_home, 'dt', 'gpp.dts.template'),

    'cpu': {
        'cores': 4,
        'cores_per_cluster': 1,
        'gic': {
            'version': 3,
            'distributor_base': 0x1010000,
            'distributor_size': 0x10000,
            'redistributor_base': 0x1080000,
            'redistributor_size': 0x1000000,
        },
        'cpu_clusters': [
            # CPUs in cluster, NoC position (X,Y)
            ([0], (0,0)),
            ([1], (1,0)),
            ([2], (0,1)),
            ([3], (1,1)),
        ],
    },

    'ram': [
        {
            'base': 0x40000000,
            'size': 0x100000000
        }
    ],

    'uarts': [
        {
            'type': 'pl011',
            'name': 'uart0',
            'base': 0x08000000,
            'irq': 11
        }
    ],

    'block': [
        {
           'name': 'block0',
           'base': 0xa100000,
           'size': 0x1000,
           'irq': 40,
           'image': os.path.join(gpp_home, 'disk_images', "disk_image.link"),
        },
    ],

    'net': [
        {
            'name': 'net0',
            'base': 0xa200000,
            'size': 0x1000,
            'irq': 42,
            'ip': '192.168.0.0/24',
            #'hostfwd_ssh_port': 2222, # Decomment this to Host-forward Port to access VM via SSH.
        },
    ],

    'rtc': {
        'base': 0xb000000,
        'size': 0x1000,
        'irq': 44
    },

    'sesam_monitor_addr': 0x17000000,

    'software': {
       'mode': 'minimal', # minimal

       'elf': [
            # List of ELF files (absolute paths) to load into memory before simulation starts.
       ],

       'bin': [
            # List of binaries
       ],

       'dtb': {
           'path': os.path.join(gpp_home, 'dt', 'gpp.dtb'),
       },

       'kernel': {
           'path': os.path.join(gpp_home, 'linux', 'linux.link'),
           'bootargs': 'console=ttyAMA0 earlycon root=/dev/vda uio_pdrv_genirq.of_id=generic-uio ip=dhcp',
       },

       'entry': None # Set this to entry PC when in custom mode.
    },

    'memory_subsystem': {
        'simulate': True,
        'focus_on_roi': True,
        'enable_coherence': True,
        'cache': {
            'l1-data': {
                'size': 64*1024, # Bytes
                'line-size': 64, # Bytes
                'associativity': 4,
                'latency-ns': 0,
            },
            'l1-instructions': {
                'size': 64*1024, # Bytes
                'line-size': 64, # Bytes
                'associativity': 4,
                'latency-ns': 0,
            },
            'l2': {
                'size': 1024*1024, # Bytes
                'line-size': 64, # Bytes
                'associativity': 8,
                'latency-ns': 1,
                'inclusion-l1': 'NINE', # Can be Exclusive, Inclusive, or NINE
            },
            'l3': {
                'line-size': 64, # Bytes
                'associativity': 16, # Bytes
                'latency-ns': 2,
                'home-node-size': 2048*1024,
                'inclusion-l2': 'Exclusive', # Can be Exclusive, Inclusive, or NINE
                'home-nodes': [
                    # Base address, size, NoC position (X,Y)
                    (0x40000000, 0x40000000, (0,0)),
                    (0x80000000, 0x40000000, (1,0)),
                    (0xc0000000, 0x40000000, (0,1)),
                    (0x100000000,0x40000000, (1,1)),
                ],
            },
        },
        'noc': {
            'x-nodes': 2,
            'y-nodes': 2,
            'diagnosis' : False,
            'with-contention' : True,
            'contention-interval-ns' : 10,
            'buffer-size-flits' : 1,
            'flit-size': 8,
            'router-latency-ns': 0.34,
            'link-latency-ns': 0.34,
            'virtual-channels' : 1,
        },
        'off-chip-memory': {
            'read-latency-ns': 20,
            'write-latency-ns': 1,

            # For now we only support the same width for all memories
            'channel-width': 16, # bytes
            'channels': 8,
            'memory-controllers': [
                # base address, size, noc position
                (0x40000000, 0x80000000, (0,0)),
                (0xC0000000, 0x80000000, (1,0)),
            ],
        },
    },

    # Provide a port to start in Debug mode
    # (You then need to connect a cross-gdb to start the simulation !)
    'gdb_port': None,
    'log_execution': False,
    'log_file': os.path.join(os.environ['VPSIM_HOME'],'bin','log.txt'),
}

if __name__ == '__main__':
    # Build the config
    sys = FullSystem(conf)
    # Run simulation
    stats = sys.build(simulate=True,wait=True,silent=False,)

    # Print global stats at the end since the boot
    if not stats:
        print("No statistics were available !")
    else:
        instr=0
        for component in stats:
            print("\n==== Statistics for %s ====" % component)
            for stat in stats[component]:
                value, unit = stats[component][stat]
                print("%s = %s %s" % (stat, value, unit))
                if stat == 'executed_instructions':
                    instr += int(stats[component][stat][0])
        print("Total executed instructions: %s" % instr)

