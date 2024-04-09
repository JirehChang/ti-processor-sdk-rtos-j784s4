#!/usr/bin/env python3
#
# Copyright (c) 2018 Texas Instruments Incorporated
#
# All rights reserved not granted herein.
#
# Limited License.
#
# Texas Instruments Incorporated grants a world-wide, royalty-free, non-exclusive
# license under copyrights and patents it now or hereafter owns or controls to make,
# have made, use, import, offer to sell and sell ("Utilize") this software subject to the
# terms herein.  With respect to the foregoing patent license, such license is granted
# solely to the extent that any such patent is necessary to Utilize the software alone.
# The patent license shall not apply to any combinations which include this software,
# other than combinations with devices manufactured by or for TI ("TI Devices").
# No hardware patent is licensed hereunder.
#
# Redistributions must preserve existing copyright notices and reproduce this license
# (including the above copyright notice and the disclaimer and (if applicable) source
# code license limitations below) in the documentation and/or other materials provided
# with the distribution
#
# Redistribution and use in binary form, without modification, are permitted provided
# that the following conditions are met:
#
#       No reverse engineering, decompilation, or disassembly of this software is
# permitted with respect to any software provided in binary form.
#
#       any redistribution and use are licensed by TI for use only with TI Devices.
#
#       Nothing shall obligate TI to provide you with source code for the software
# licensed and provided to you in object code.
#
# If software source code is provided to you, modification and redistribution of the
# source code are permitted provided that the following conditions are met:
#
#       any redistribution and use of the source code, including any resulting derivative
# works, are licensed by TI for use only with TI Devices.
#
#       any redistribution and use of any object code compiled from the source code
# and any resulting derivative works, are licensed by TI for use only with TI Devices.
#
# Neither the name of Texas Instruments Incorporated nor the names of its suppliers
#
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# DISCLAIMER.
#
# THIS SOFTWARE IS PROVIDED BY TI AND TI'S LICENSORS "AS IS" AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL TI AND TI'S LICENSORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
#
#

#
# This script is used to generate 'MEMORY' section for multiple CPUs
# in different CPU specific linker command files.
#
# This helps to define the memory map in one file vs having to manually
# keep the system memory map consistant across multiple CPUs
# in different linker commnd files.
#
# Make sure PyTI_PSDK_RTOS module is installed before running this script.
# See vision_apps/tools/PyTI_PSDK_RTOS/README.txt to install PyTI_PSDK_RTOS module.
#
# Edit this file to change the memory map
#
# Run this script by doing below,
# ./gen_linker_mem_map.py
#
# This will generate linker command file at below folders
# ./<cpu name>/linker_mem_map.cmd
#
# Here CPU name is mpu1, c7x_1, c7x_2, mcu1_0, mcu2_0, mcu3_0
#
#
from ti_psdk_rtos_tools import *

KB = 1024;
MB = KB*KB;
GB = KB*MB;

#
# Notes,
# - recommend to keep all memory segment sizes in units of KB at least
#

#
# On J721E/J7ES/TDA4VM, there are 2 DDR chipsets
#
# lower DDR address starts at 0x0000_8000_0000
# higher DDR address starts at 0x0008_8000_0000
#
# As the address is non-contiguous it requires MMU to remap the address
# Currently the upper 2GB is accessed by either ARM (user space)
# C7x DSP heap/scratch space, as 32-bit cores like R5F cannot access it
#
# The upper DDR address is mapped contiguously from lower DDR address
# but remapped to actual physical address using MMU
#
# physical lower DDR address range 0x0000_8000_0000
# virtual lower DDR address range 0x0000_8000_0000
#
# physical lower DDR address range 0x0008_8000_0000
# virtual lower DDR address range 0x0001_0000_0000
#

ddr_mem_addr  = 0xa0000000;
ddr_mem_size  = 1*GB + 448*MB; # Last 64MB is used by Linux

ddr_mem_addr_hi_phy = 0x880000000;
ddr_mem_addr_hi = 0x100000000;
ddr_mem_size_hi = 736*MB;

msmc_mem_addr = 0x70000000;
main_ocram_mem_addr = 0x60000000; # Note: uses RAT to translate to proper address
main_ocram_mem_addr_phys = 0x4F02000000;

#
# Other constant sizes
#
linux_ddr_ipc_size = 1*MB;
linux_ddr_resource_table_size = 1*KB;

#
# MSMC memory allocation for various CPUs
#
dmsc_msmc_size   = 64*KB;
mpu1_msmc_addr   = msmc_mem_addr;
mpu1_msmc_size   = 128*KB;
c7x_1_msmc_addr  = mpu1_msmc_addr + mpu1_msmc_size;
misc_msmc_stack_size = 32*KB;
c7x_1_msmc_size  = 4*MB - mpu1_msmc_size - dmsc_msmc_size - misc_msmc_stack_size;
dmsc_msmc_addr   = c7x_1_msmc_addr + c7x_1_msmc_size + misc_msmc_stack_size;

#
# C7x L1, L2 memory allocation
# L1 - 32KB $, 16KB SRAM
# L2 - 64KB $, 448KB SRAM
c7x_1_l2_addr  = 0x64800000;
c7x_1_l2_size  = (512 - 64)*KB;
c7x_1_l1_addr  = 0x64E00000;
c7x_1_l1_size  = 16*KB;

#
# C7x L1, L2 memory allocation
# L1 - 32KB $, 16KB SRAM
# L2 - 64KB $, 448KB SRAM
c7x_2_l2_addr  = 0x65800000;
c7x_2_l2_size  = (512 - 64)*KB;
c7x_2_l1_addr  = 0x65E00000;
c7x_2_l1_size  = 16*KB;

#
# Main OCRAM memory allocation
#
mcu2_0_main_ocram_addr       = main_ocram_mem_addr;
mcu2_0_main_ocram_addr_phys  = main_ocram_mem_addr_phys;
mcu2_0_main_ocram_size       = 512*KB;

mcu2_1_main_ocram_addr       = mcu2_0_main_ocram_addr + mcu2_0_main_ocram_size;
mcu2_1_main_ocram_addr_phys  = mcu2_0_main_ocram_addr_phys + mcu2_0_main_ocram_size;
mcu2_1_main_ocram_size       = 512*KB;

#
# DDR memory allocation for various CPUs
#
mcu1_0_ddr_ipc_addr = ddr_mem_addr;
mcu1_0_ddr_resource_table_addr = mcu1_0_ddr_ipc_addr + linux_ddr_ipc_size;
mcu1_0_ddr_addr = mcu1_0_ddr_resource_table_addr + linux_ddr_resource_table_size;
mcu1_0_ddr_size = 16*MB - (mcu1_0_ddr_addr-mcu1_0_ddr_ipc_addr);

mcu1_1_ddr_ipc_addr = mcu1_0_ddr_addr + mcu1_0_ddr_size;
mcu1_1_ddr_resource_table_addr = mcu1_1_ddr_ipc_addr + linux_ddr_ipc_size;
mcu1_1_ddr_addr = mcu1_1_ddr_resource_table_addr + linux_ddr_resource_table_size;
mcu1_1_ddr_size = 16*MB - (mcu1_1_ddr_addr-mcu1_1_ddr_ipc_addr);

mcu2_0_ddr_ipc_addr = mcu1_1_ddr_addr + mcu1_1_ddr_size;
mcu2_0_ddr_resource_table_addr = mcu2_0_ddr_ipc_addr + linux_ddr_ipc_size;
mcu2_0_ddr_addr = mcu2_0_ddr_resource_table_addr + linux_ddr_resource_table_size;
mcu2_0_ddr_size = 32*MB - (mcu2_0_ddr_addr-mcu2_0_ddr_ipc_addr);

mcu2_1_ddr_ipc_addr = mcu2_0_ddr_addr + mcu2_0_ddr_size;
mcu2_1_ddr_resource_table_addr = mcu2_1_ddr_ipc_addr + linux_ddr_ipc_size;
mcu2_1_ddr_addr = mcu2_1_ddr_resource_table_addr + linux_ddr_resource_table_size;
mcu2_1_ddr_size = 32*MB - (mcu2_1_ddr_addr-mcu2_1_ddr_ipc_addr);

mcu3_0_ddr_ipc_addr = mcu2_1_ddr_addr + mcu2_1_ddr_size;
mcu3_0_ddr_resource_table_addr = mcu3_0_ddr_ipc_addr + linux_ddr_ipc_size;
mcu3_0_ddr_addr = mcu3_0_ddr_resource_table_addr + linux_ddr_resource_table_size;
mcu3_0_ddr_size = 16*MB - (mcu3_0_ddr_addr-mcu3_0_ddr_ipc_addr);

mcu3_1_ddr_ipc_addr = mcu3_0_ddr_addr + mcu3_0_ddr_size;
mcu3_1_ddr_resource_table_addr = mcu3_1_ddr_ipc_addr + linux_ddr_ipc_size;
mcu3_1_ddr_addr = mcu3_1_ddr_resource_table_addr + linux_ddr_resource_table_size;
mcu3_1_ddr_size = 16*MB - (mcu3_1_ddr_addr-mcu3_1_ddr_ipc_addr);

#
# DDR memory allocation for various shared memories
#

# Hardcoding this value, as this cannot be different from IPC echo test value
ipc_vring_mem_addr      = 0xA8000000;
ipc_vring_mem_size      = 32*MB;

app_log_mem_addr        = ipc_vring_mem_addr + ipc_vring_mem_size;
app_log_mem_size        = 256*KB;
tiovx_obj_desc_mem_addr = app_log_mem_addr + app_log_mem_size;
tiovx_obj_desc_mem_size = 64*MB - app_log_mem_size;

app_fileio_mem_addr     =  tiovx_obj_desc_mem_addr + tiovx_obj_desc_mem_size;
app_fileio_mem_size     = 4*MB;
tiovx_log_rt_mem_addr   = app_fileio_mem_addr + app_fileio_mem_size;
tiovx_log_rt_mem_size   = 32*MB - app_fileio_mem_size;

c7x_1_ddr_ipc_addr =tiovx_log_rt_mem_addr + tiovx_log_rt_mem_size;
c7x_1_ddr_resource_table_addr = c7x_1_ddr_ipc_addr + linux_ddr_ipc_size;
c7x_1_ddr_boot_addr = c7x_1_ddr_resource_table_addr + 1*MB;
c7x_1_ddr_boot_size = 1*KB;
c7x_1_ddr_vecs_addr = c7x_1_ddr_resource_table_addr + 3*MB;
c7x_1_ddr_vecs_size = 16*KB;
c7x_1_ddr_secure_vecs_addr = c7x_1_ddr_resource_table_addr + 5*MB;
c7x_1_ddr_secure_vecs_size = 16*KB;
c7x_1_ddr_addr = c7x_1_ddr_secure_vecs_addr + c7x_1_ddr_secure_vecs_size;
c7x_1_ddr_size = 96*MB - (c7x_1_ddr_addr-c7x_1_ddr_ipc_addr);

c7x_2_ddr_ipc_addr = c7x_1_ddr_addr  + c7x_1_ddr_size;
c7x_2_ddr_resource_table_addr = c7x_2_ddr_ipc_addr + linux_ddr_ipc_size;
c7x_2_ddr_boot_addr = c7x_2_ddr_resource_table_addr + 1*MB;
c7x_2_ddr_boot_size = 1*KB;
c7x_2_ddr_vecs_addr = c7x_2_ddr_resource_table_addr + 3*MB;
c7x_2_ddr_vecs_size = 16*KB;
c7x_2_ddr_secure_vecs_addr = c7x_2_ddr_resource_table_addr + 5*MB;
c7x_2_ddr_secure_vecs_size = 16*KB;
c7x_2_ddr_addr = c7x_2_ddr_secure_vecs_addr + c7x_2_ddr_secure_vecs_size;
c7x_2_ddr_size = 32*MB - (c7x_2_ddr_addr-c7x_2_ddr_ipc_addr);

mcu1_0_ddr_local_heap_addr  = c7x_2_ddr_addr + c7x_2_ddr_size;
mcu1_0_ddr_local_heap_size  = 8*MB;
mcu1_1_ddr_local_heap_addr  = mcu1_0_ddr_local_heap_addr + mcu1_0_ddr_local_heap_size;
mcu1_1_ddr_local_heap_size  = 8*MB;
mcu2_0_ddr_local_heap_addr  = mcu1_1_ddr_local_heap_addr + mcu1_1_ddr_local_heap_size;
mcu2_0_ddr_local_heap_size  = 16*MB;
mcu2_1_ddr_local_heap_addr  = mcu2_0_ddr_local_heap_addr + mcu2_0_ddr_local_heap_size;
mcu2_1_ddr_local_heap_size  = 16*MB;
mcu3_0_ddr_local_heap_addr  = mcu2_1_ddr_local_heap_addr + mcu2_1_ddr_local_heap_size;
mcu3_0_ddr_local_heap_size  = 8*MB;
mcu3_1_ddr_local_heap_addr  = mcu3_0_ddr_local_heap_addr + mcu3_0_ddr_local_heap_size;
mcu3_1_ddr_local_heap_size  = 8*MB;

# Shared memory for DMA Buf FD carveout
ddr_shared_mem_addr     = 0xC0000000; # This will be the virtual address used for R5F's / C7X's
ddr_shared_mem_size     = 512*MB;

c7x_1_ddr_scratch_addr     = ddr_mem_addr_hi;
c7x_1_ddr_scratch_size     = 368*MB;

c7x_1_ddr_local_heap_addr  = c7x_1_ddr_scratch_addr + c7x_1_ddr_scratch_size;
c7x_1_ddr_local_heap_size  = 256*MB;

c7x_2_ddr_local_heap_addr = c7x_1_ddr_local_heap_addr + c7x_1_ddr_local_heap_size;
c7x_2_ddr_local_heap_size = 16*MB;
c7x_2_ddr_scratch_addr    = c7x_2_ddr_local_heap_addr + c7x_2_ddr_local_heap_size;
c7x_2_ddr_scratch_size    = 64*MB;

# Shared memory for DMA Buf FD carveout (located in high mem)
ddr_shared_mem_addr_phys  = 0x900000000; # TODO: Clean this up
ddr_shared_mem_size       = 512*MB;

#
# Create memory section based on addr and size defined above, including
# any CPU specific internal memories
#

# r5f local memory sections
mcu_r5f_tcma_vecs  = MemSection("R5F_TCMA_VECS" , "X"   , 0x00000000, (KB >> 4));
mcu_r5f_tcma       = MemSection("R5F_TCMA" , "X"   , 0x00000040, (32*KB) - (KB >> 4));

r5f_tcmb0      = MemSection("R5F_TCMB0", "RWIX", 0x41010000, 32*KB);

mcu_r5f_tcmb0_vecs   = MemSection("R5F_TCMB0_VECS", "RWIX", 0x41010000, (KB >> 4));
mcu_r5f_tcmb0        = MemSection("R5F_TCMB0", "RWIX", 0x41010040, (32*KB) - (KB >> 4));

# MSMC memory sections
mpu1_msmc   = MemSection("MSMC_MPU1", "RWIX", mpu1_msmc_addr  , mpu1_msmc_size  , "MSMC reserved for MPU1 for ATF");
c7x_1_msmc  = MemSection("MSMC_C7x_1", "RWIX", c7x_1_msmc_addr  , c7x_1_msmc_size  , "MSMC for C7x_1");
dmsc_msmc  = MemSection("MSMC_DMSC", "RWIX", dmsc_msmc_addr  , dmsc_msmc_size  , "MSMC reserved for DMSC IPC");

# C7x L1/L2 memory sections
c7x_1_l2   = MemSection("L2RAM_C7x_1", "RWIX", c7x_1_l2_addr  , c7x_1_l2_size  , "L2 for C7x_1");
c7x_1_l1   = MemSection("L1RAM_C7x_1", "RWIX", c7x_1_l1_addr  , c7x_1_l1_size  , "L1 for C7x_1");

c7x_2_l2   = MemSection("L2RAM_C7x_2", "RWIX", c7x_2_l2_addr  , c7x_2_l2_size  , "L2 for C7x_2");
c7x_2_l1   = MemSection("L1RAM_C7x_2", "RWIX", c7x_2_l1_addr  , c7x_2_l1_size  , "L1 for C7x_2");

# Main OCRAM memory sections
mcu2_0_main_ocram   = MemSection("MAIN_OCRAM_MCU2_0", "RWIX", mcu2_0_main_ocram_addr  , mcu2_0_main_ocram_size  , "Main OCRAM for MCU2_0");
mcu2_1_main_ocram   = MemSection("MAIN_OCRAM_MCU2_1", "RWIX", mcu2_1_main_ocram_addr  , mcu2_1_main_ocram_size  , "Main OCRAM for MCU2_1");

mcu2_0_main_ocram_phys   = MemSection("MAIN_OCRAM_MCU2_0_PHYS", "RWIX", mcu2_0_main_ocram_addr_phys  , mcu2_0_main_ocram_size  , "Main OCRAM Physical Address for MCU2_0");
mcu2_1_main_ocram_phys   = MemSection("MAIN_OCRAM_MCU2_1_PHYS", "RWIX", mcu2_1_main_ocram_addr_phys  , mcu2_1_main_ocram_size  , "Main OCRAM Physical Address for MCU2_1");

# CPU code/data memory sections in DDR
mcu1_0_ddr_ipc             = MemSection("DDR_MCU1_0_IPC", "RWIX", mcu1_0_ddr_ipc_addr, linux_ddr_ipc_size, "DDR for MCU1_0 for Linux IPC");
mcu1_0_ddr_ipc.setDtsName("vision_apps_mcu_r5fss0_core0_dma_memory_region", "vision-apps-r5f-dma-memory");
mcu1_0_ddr_resource_table  = MemSection("DDR_MCU1_0_RESOURCE_TABLE", "RWIX", mcu1_0_ddr_resource_table_addr, linux_ddr_resource_table_size, "DDR for MCU1_0 for Linux resource table");
mcu1_0_ddr                 = MemSection("DDR_MCU1_0", "RWIX", mcu1_0_ddr_addr, mcu1_0_ddr_size, "DDR for MCU1_0 for code/data");
mcu1_0_ddr_local_heap      = MemSection("DDR_MCU1_0_LOCAL_HEAP", "RWIX", mcu1_0_ddr_local_heap_addr, mcu1_0_ddr_local_heap_size, "DDR for MCU1_0 for local heap");
mcu1_0_ddr_total           = MemSection("DDR_MCU1_0_DTS", "", 0, 0, "DDR for MCU1_0 for all sections, used for reserving memory in DTS file");
mcu1_0_ddr_total.concat(mcu1_0_ddr_resource_table);
mcu1_0_ddr_total.concat(mcu1_0_ddr);
mcu1_0_ddr_total.setDtsName("vision_apps_mcu_r5fss0_core0_memory_region", "vision-apps-r5f-memory");

mcu1_1_ddr_ipc             = MemSection("DDR_MCU1_1_IPC", "RWIX", mcu1_1_ddr_ipc_addr, linux_ddr_ipc_size, "DDR for MCU1_1 for Linux IPC");
mcu1_1_ddr_ipc.setDtsName("vision_apps_mcu_r5fss0_core1_dma_memory_region", "vision-apps-r5f-dma-memory");
mcu1_1_ddr_resource_table  = MemSection("DDR_MCU1_1_RESOURCE_TABLE", "RWIX", mcu1_1_ddr_resource_table_addr, linux_ddr_resource_table_size, "DDR for MCU1_1 for Linux resource table");
mcu1_1_ddr                 = MemSection("DDR_MCU1_1", "RWIX", mcu1_1_ddr_addr, mcu1_1_ddr_size, "DDR for MCU1_1 for code/data");
mcu1_1_ddr_local_heap      = MemSection("DDR_MCU1_1_LOCAL_HEAP", "RWIX", mcu1_1_ddr_local_heap_addr, mcu1_1_ddr_local_heap_size, "DDR for MCU1_1 for local heap");
mcu1_1_ddr_total           = MemSection("DDR_MCU1_1_DTS", "", 0, 0, "DDR for MCU1_1 for all sections, used for reserving memory in DTS file");
mcu1_1_ddr_total.concat(mcu1_1_ddr_resource_table);
mcu1_1_ddr_total.concat(mcu1_1_ddr);
mcu1_1_ddr_total.setDtsName("vision_apps_mcu_r5fss0_core1_memory_region", "vision-apps-r5f-memory");

mcu2_0_ddr_ipc             = MemSection("DDR_MCU2_0_IPC", "RWIX", mcu2_0_ddr_ipc_addr, linux_ddr_ipc_size, "DDR for MCU2_0 for Linux IPC");
mcu2_0_ddr_ipc.setDtsName("vision_apps_main_r5fss0_core0_dma_memory_region", "vision-apps-r5f-dma-memory");
mcu2_0_ddr_resource_table  = MemSection("DDR_MCU2_0_RESOURCE_TABLE", "RWIX", mcu2_0_ddr_resource_table_addr, linux_ddr_resource_table_size, "DDR for MCU2_0 for Linux resource table");
mcu2_0_ddr                 = MemSection("DDR_MCU2_0", "RWIX", mcu2_0_ddr_addr, mcu2_0_ddr_size, "DDR for MCU2_0 for code/data");
mcu2_0_ddr_total           = MemSection("DDR_MCU2_0_DTS", "", 0, 0, "DDR for MCU2_0 for all sections, used for reserving memory in DTS file");
mcu2_0_ddr_local_heap      = MemSection("DDR_MCU2_0_LOCAL_HEAP", "RWIX", mcu2_0_ddr_local_heap_addr, mcu2_0_ddr_local_heap_size, "DDR for MCU2_0 for local heap");
mcu2_0_ddr_total.concat(mcu2_0_ddr_resource_table);
mcu2_0_ddr_total.concat(mcu2_0_ddr);
mcu2_0_ddr_total.setDtsName("vision_apps_main_r5fss0_core0_memory_region", "vision-apps-r5f-memory");

mcu2_1_ddr_ipc             = MemSection("DDR_MCU2_1_IPC", "RWIX", mcu2_1_ddr_ipc_addr, linux_ddr_ipc_size, "DDR for MCU2_1 for Linux IPC");
mcu2_1_ddr_ipc.setDtsName("vision_apps_main_r5fss0_core1_dma_memory_region", "vision-apps-r5f-dma-memory");
mcu2_1_ddr_resource_table  = MemSection("DDR_MCU2_1_RESOURCE_TABLE", "RWIX", mcu2_1_ddr_resource_table_addr, linux_ddr_resource_table_size, "DDR for MCU2_1 for Linux resource table");
mcu2_1_ddr                 = MemSection("DDR_MCU2_1", "RWIX", mcu2_1_ddr_addr, mcu2_1_ddr_size, "DDR for MCU2_1 for code/data");
mcu2_1_ddr_total           = MemSection("DDR_MCU2_1_DTS", "", 0, 0, "DDR for MCU2_1 for all sections, used for reserving memory in DTS file");
mcu2_1_ddr_local_heap      = MemSection("DDR_MCU2_1_LOCAL_HEAP", "RWIX", mcu2_1_ddr_local_heap_addr, mcu2_1_ddr_local_heap_size, "DDR for MCU2_1 for local heap");
mcu2_1_ddr_total.concat(mcu2_1_ddr_resource_table);
mcu2_1_ddr_total.concat(mcu2_1_ddr);
mcu2_1_ddr_total.setDtsName("vision_apps_main_r5fss0_core1_memory_region", "vision-apps-r5f-memory");

mcu3_0_ddr_ipc             = MemSection("DDR_MCU3_0_IPC", "RWIX", mcu3_0_ddr_ipc_addr, linux_ddr_ipc_size, "DDR for MCU3_0 for Linux IPC");
mcu3_0_ddr_ipc.setDtsName("vision_apps_main_r5fss1_core0_dma_memory_region", "vision-apps-r5f-dma-memory");
mcu3_0_ddr_resource_table  = MemSection("DDR_MCU3_0_RESOURCE_TABLE", "RWIX", mcu3_0_ddr_resource_table_addr, linux_ddr_resource_table_size, "DDR for MCU3_0 for Linux resource table");
mcu3_0_ddr                 = MemSection("DDR_MCU3_0", "RWIX", mcu3_0_ddr_addr, mcu3_0_ddr_size, "DDR for MCU3_0 for code/data");
mcu3_0_ddr_local_heap      = MemSection("DDR_MCU3_0_LOCAL_HEAP", "RWIX", mcu3_0_ddr_local_heap_addr, mcu3_0_ddr_local_heap_size, "DDR for MCU3_0 for local heap");
mcu3_0_ddr_total           = MemSection("DDR_MCU3_0_DTS", "", 0, 0, "DDR for MCU3_0 for all sections, used for reserving memory in DTS file");
mcu3_0_ddr_total.concat(mcu3_0_ddr_resource_table);
mcu3_0_ddr_total.concat(mcu3_0_ddr);
mcu3_0_ddr_total.setDtsName("vision_apps_main_r5fss1_core0_memory_region", "vision-apps-r5f-memory");

mcu3_1_ddr_ipc             = MemSection("DDR_MCU3_1_IPC", "RWIX", mcu3_1_ddr_ipc_addr, linux_ddr_ipc_size, "DDR for MCU3_1 for Linux IPC");
mcu3_1_ddr_ipc.setDtsName("vision_apps_main_r5fss1_core1_dma_memory_region", "vision-apps-r5f-dma-memory");
mcu3_1_ddr_resource_table  = MemSection("DDR_MCU3_1_RESOURCE_TABLE", "RWIX", mcu3_1_ddr_resource_table_addr, linux_ddr_resource_table_size, "DDR for MCU3_1 for Linux resource table");
mcu3_1_ddr                 = MemSection("DDR_MCU3_1", "RWIX", mcu3_1_ddr_addr, mcu3_1_ddr_size, "DDR for MCU3_1 for code/data");
mcu3_1_ddr_local_heap      = MemSection("DDR_MCU3_1_LOCAL_HEAP", "RWIX", mcu3_1_ddr_local_heap_addr, mcu3_1_ddr_local_heap_size, "DDR for MCU3_1 for local heap");
mcu3_1_ddr_total           = MemSection("DDR_MCU3_1_DTS", "", 0, 0, "DDR for MCU3_1 for all sections, used for reserving memory in DTS file");
mcu3_1_ddr_total.concat(mcu3_1_ddr_resource_table);
mcu3_1_ddr_total.concat(mcu3_1_ddr);
mcu3_1_ddr_total.setDtsName("vision_apps_main_r5fss1_core1_memory_region", "vision-apps-r5f-memory");

c7x_2_ddr_ipc             = MemSection("DDR_C7x_2_IPC", "RWIX", c7x_2_ddr_ipc_addr, linux_ddr_ipc_size, "DDR for C7x_2 for Linux IPC");
c7x_2_ddr_ipc.setDtsName("vision_apps_c71_1_dma_memory_region", "vision-apps-c71_1-dma-memory");
c7x_2_ddr_resource_table  = MemSection("DDR_C7x_2_RESOURCE_TABLE", "RWIX", c7x_2_ddr_resource_table_addr, linux_ddr_resource_table_size, "DDR for C7x_2 for Linux resource table");
c7x_2_ddr_boot            = MemSection("DDR_C7x_2_BOOT", "RWIX", c7x_2_ddr_boot_addr, c7x_2_ddr_boot_size, "DDR for C7x_2 for boot section");
c7x_2_ddr_vecs            = MemSection("DDR_C7x_2_VECS", "RWIX", c7x_2_ddr_vecs_addr, c7x_2_ddr_vecs_size, "DDR for C7x_2 for vecs section");
c7x_2_ddr_secure_vecs     = MemSection("DDR_C7x_2_SECURE_VECS", "RWIX", c7x_2_ddr_secure_vecs_addr, c7x_2_ddr_secure_vecs_size, "DDR for C7x_2 for secure vecs section");
c7x_2_ddr                 = MemSection("DDR_C7x_2", "RWIX", c7x_2_ddr_addr, c7x_2_ddr_size, "DDR for C7x_2 for code/data");
c7x_2_ddr_local_heap      = MemSection("DDR_C7X_2_LOCAL_HEAP", "RWIX", c7x_2_ddr_local_heap_addr, c7x_2_ddr_local_heap_size, "DDR for c7x_2 for local heap");
c7x_2_ddr_scratch         = MemSection("DDR_C7X_2_SCRATCH", "RWIX", c7x_2_ddr_scratch_addr, c7x_2_ddr_scratch_size, "DDR for c7x_2 for Scratch Memory");
c7x_2_ddr_total           = MemSection("DDR_C7x_2_DTS", "", 0, 0, "DDR for C7x_2 for all sections, used for reserving memory in DTS file");
c7x_2_ddr_total.concat(c7x_2_ddr_resource_table);
c7x_2_ddr_total.concat(c7x_2_ddr_boot);
c7x_2_ddr_total.concat(c7x_2_ddr_vecs);
c7x_2_ddr_total.concat(c7x_2_ddr_secure_vecs);
c7x_2_ddr_total.concat(c7x_2_ddr);
c7x_2_ddr_total.setDtsName("vision_apps_c71_1_memory_region", "vision-apps-c71_1-memory");

c7x_1_ddr_ipc             = MemSection("DDR_C7x_1_IPC", "RWIX", c7x_1_ddr_ipc_addr, linux_ddr_ipc_size, "DDR for C7x_1 for Linux IPC");
c7x_1_ddr_ipc.setDtsName("vision_apps_c71_0_dma_memory_region", "vision-apps-c71-dma-memory");
c7x_1_ddr_resource_table  = MemSection("DDR_C7x_1_RESOURCE_TABLE", "RWIX", c7x_1_ddr_resource_table_addr, linux_ddr_resource_table_size, "DDR for C7x_1 for Linux resource table");
c7x_1_ddr_boot            = MemSection("DDR_C7x_1_BOOT", "RWIX", c7x_1_ddr_boot_addr, c7x_1_ddr_boot_size, "DDR for C7x_1 for boot section");
c7x_1_ddr_vecs            = MemSection("DDR_C7x_1_VECS", "RWIX", c7x_1_ddr_vecs_addr, c7x_1_ddr_vecs_size, "DDR for C7x_1 for vecs section");
c7x_1_ddr_secure_vecs     = MemSection("DDR_C7x_1_SECURE_VECS", "RWIX", c7x_1_ddr_secure_vecs_addr, c7x_1_ddr_secure_vecs_size, "DDR for C7x_1 for secure vecs section");
c7x_1_ddr                 = MemSection("DDR_C7x_1", "RWIX", c7x_1_ddr_addr, c7x_1_ddr_size, "DDR for C7x_1 for code/data");
c7x_1_ddr_local_heap      = MemSection("DDR_C7X_1_LOCAL_HEAP", "RWIX", c7x_1_ddr_local_heap_addr, c7x_1_ddr_local_heap_size, "DDR for c7x_1 for local heap");
c7x_1_ddr_scratch         = MemSection("DDR_C7X_1_SCRATCH", "RWIX", c7x_1_ddr_scratch_addr, c7x_1_ddr_scratch_size, "DDR for c7x_1 for Scratch Memory");
c7x_1_ddr_total           = MemSection("DDR_C7x_1_DTS", "", 0, 0, "DDR for C7x_1 for all sections, used for reserving memory in DTS file");
c7x_1_ddr_total.concat(c7x_1_ddr_resource_table);
c7x_1_ddr_total.concat(c7x_1_ddr_boot);
c7x_1_ddr_total.concat(c7x_1_ddr_vecs);
c7x_1_ddr_total.concat(c7x_1_ddr_secure_vecs);
c7x_1_ddr_total.concat(c7x_1_ddr);
c7x_1_ddr_total.setDtsName("vision_apps_c71_0_memory_region", "vision-apps-c71_0-memory");

# Shared memory memory sections in DDR
app_log_mem            = MemSection("APP_LOG_MEM"        , "", app_log_mem_addr       , app_log_mem_size       , "Memory for remote core logging");
tiovx_obj_desc_mem     = MemSection("TIOVX_OBJ_DESC_MEM" , "", tiovx_obj_desc_mem_addr, tiovx_obj_desc_mem_size, "Memory for TI OpenVX shared memory. MUST be non-cached or cache-coherent");
app_fileio_mem        = MemSection("APP_FILEIO_MEM"        , "", app_fileio_mem_addr       , app_fileio_mem_size       , "Memory for remote core file operations");
tiovx_log_rt_mem     = MemSection("TIOVX_LOG_RT_MEM" , "", tiovx_log_rt_mem_addr, tiovx_log_rt_mem_size, "Memory for TI OpenVX shared memory for Run-time logging. MUST be non-cached or cache-coherent");

ipc_vring_mem      = MemSection("IPC_VRING_MEM"     , "", ipc_vring_mem_addr     , ipc_vring_mem_size     , "Memory for IPC Vring's. MUST be non-cached or cache-coherent");
ipc_vring_mem.setDtsName("vision_apps_rtos_ipc_memory_region", "vision-apps-rtos-ipc-memory-region");

vision_apps_ddr_total  = MemSection("DDR_VISION_APPS_DTS", "", 0                      , 0                      , "DDR for Vision Apps for all sections, used for reserving memory in DTS file");
vision_apps_ddr_total.concat(app_log_mem);
vision_apps_ddr_total.concat(tiovx_obj_desc_mem);
vision_apps_ddr_total.concat(app_fileio_mem);
vision_apps_ddr_total.concat(tiovx_log_rt_mem);
vision_apps_ddr_total.setDtsName("vision_apps_memory_region", "vision-apps-dma-memory");

vision_apps_core_heaps_lo = MemSection("DDR_VISION_APPS_CORE_HEAPS_LO_DTS", "", 0, 0, "Vision Apps Core Heaps in 32bit address range of DDR");
vision_apps_core_heaps_lo.concat(mcu1_0_ddr_local_heap);
vision_apps_core_heaps_lo.concat(mcu2_0_ddr_local_heap);
vision_apps_core_heaps_lo.concat(mcu2_1_ddr_local_heap);
vision_apps_core_heaps_lo.concat(mcu3_0_ddr_local_heap);
vision_apps_core_heaps_lo.concat(mcu3_1_ddr_local_heap);
vision_apps_core_heaps_lo.setDtsName("vision_apps_core_heaps_lo", "vision-apps-core-heap-memory-lo");

c7x_1_ddr_local_heap_phy  = MemSection("DDR_C7X_1_LOCAL_HEAP", "RWIX", ddr_mem_addr_hi_phy, (c7x_1_ddr_scratch_size + c7x_1_ddr_local_heap_size + c7x_2_ddr_scratch_size + c7x_2_ddr_local_heap_size), "DDR for c7x_1, c7x_2 for scratch memory and local heap");

c7x_ddr_heaps_hi = MemSection("DDR_VISION_APPS_CORE_HEAPS_HI_DTS", "", 0, 0, "Vision Apps Core Heaps in 40bit address range of DDR");
c7x_ddr_heaps_hi.concat(c7x_1_ddr_local_heap_phy);
c7x_ddr_heaps_hi.setDtsName("c7x_ddr_heaps_hi", "c7x_ddr_heaps_hi-apps-core-heap-memory-hi");
c7x_ddr_heaps_hi.splitOrigin(True)

# this region should NOT have the "no-map" flag since we want ION to map this memory and do cache ops on it as needed
ddr_shared_mem     = MemSection("DDR_SHARED_MEM"    , "", ddr_shared_mem_addr    , ddr_shared_mem_size    , "Memory for shared memory buffers in DDR");
ddr_shared_mem_phys  = MemSection("DDR_SHARED_MEM_PHYS"    , "", ddr_shared_mem_addr_phys  , ddr_shared_mem_size    , "Physical address of memory for shared memory buffers in DDR");
ddr_shared_mem_phys.setDtsName("vision_apps_shared_region", "vision_apps_shared-memories");
ddr_shared_mem_phys.setCompatibility("dma-heap-carveout");
ddr_shared_mem_phys.setNoMap(False);
ddr_shared_mem_phys.setOriginTag(False);
ddr_shared_mem_phys.splitOrigin(True)

#
# Create CPU specific memory maps using memory sections created above
#

mcu1_0_mmap = MemoryMap("mcu1_0");
mcu1_0_mmap.addMemSection( mcu_r5f_tcma_vecs );
mcu1_0_mmap.addMemSection( mcu_r5f_tcma      );
mcu1_0_mmap.addMemSection( mcu_r5f_tcmb0_vecs   );
mcu1_0_mmap.addMemSection( mcu_r5f_tcmb0        );
mcu1_0_mmap.addMemSection( mcu1_0_ddr_ipc       );
mcu1_0_mmap.addMemSection( mcu1_0_ddr_resource_table  );
mcu1_0_mmap.addMemSection( mcu1_0_ddr           );
mcu1_0_mmap.addMemSection( app_log_mem          );
mcu1_0_mmap.addMemSection( tiovx_obj_desc_mem   );
mcu1_0_mmap.addMemSection( app_fileio_mem          );
mcu1_0_mmap.addMemSection( ipc_vring_mem        );
mcu1_0_mmap.addMemSection( mcu1_0_ddr_local_heap  );
mcu1_0_mmap.addMemSection( ddr_shared_mem       );
mcu1_0_mmap.checkOverlap();

mcu1_1_mmap = MemoryMap("mcu1_1");
mcu1_1_mmap.addMemSection( mcu_r5f_tcma_vecs );
mcu1_1_mmap.addMemSection( mcu_r5f_tcma      );
mcu1_1_mmap.addMemSection( mcu_r5f_tcmb0_vecs );
mcu1_1_mmap.addMemSection( mcu_r5f_tcmb0      );
mcu1_1_mmap.addMemSection( mcu1_1_ddr_ipc     );
mcu1_1_mmap.addMemSection( mcu1_1_ddr_resource_table  );
mcu1_1_mmap.addMemSection( mcu1_1_ddr         );
mcu1_1_mmap.addMemSection( app_log_mem        );
mcu1_1_mmap.addMemSection( tiovx_obj_desc_mem );
mcu1_1_mmap.addMemSection( app_fileio_mem        );
mcu1_1_mmap.addMemSection( ipc_vring_mem      );
mcu1_1_mmap.addMemSection( mcu1_1_ddr_local_heap  );
mcu1_1_mmap.addMemSection( ddr_shared_mem     );
mcu1_1_mmap.checkOverlap();


mcu2_0_mmap = MemoryMap("mcu2_0");
mcu2_0_mmap.addMemSection( mcu_r5f_tcma_vecs );
mcu2_0_mmap.addMemSection( mcu_r5f_tcma      );
mcu2_0_mmap.addMemSection( r5f_tcmb0          );
mcu2_0_mmap.addMemSection( mcu2_0_ddr_ipc     );
mcu2_0_mmap.addMemSection( mcu2_0_ddr_resource_table  );
mcu2_0_mmap.addMemSection( mcu2_0_ddr         );
mcu2_0_mmap.addMemSection( app_log_mem        );
mcu2_0_mmap.addMemSection( tiovx_obj_desc_mem );
mcu2_0_mmap.addMemSection( app_fileio_mem        );
mcu2_0_mmap.addMemSection( ipc_vring_mem      );
mcu2_0_mmap.addMemSection( mcu2_0_ddr_local_heap  );
mcu2_0_mmap.addMemSection( ddr_shared_mem     );
mcu2_0_mmap.addMemSection( mcu2_0_main_ocram );
mcu2_0_mmap.checkOverlap();

mcu2_1_mmap = MemoryMap("mcu2_1");
mcu2_1_mmap.addMemSection( mcu_r5f_tcma_vecs );
mcu2_1_mmap.addMemSection( mcu_r5f_tcma      );
mcu2_1_mmap.addMemSection( r5f_tcmb0          );
mcu2_1_mmap.addMemSection( mcu2_1_ddr_ipc     );
mcu2_1_mmap.addMemSection( mcu2_1_ddr_resource_table  );
mcu2_1_mmap.addMemSection( mcu2_1_ddr         );
mcu2_1_mmap.addMemSection( app_log_mem        );
mcu2_1_mmap.addMemSection( tiovx_obj_desc_mem );
mcu2_1_mmap.addMemSection( app_fileio_mem        );
mcu2_1_mmap.addMemSection( ipc_vring_mem      );
mcu2_1_mmap.addMemSection( mcu2_1_ddr_local_heap  );
mcu2_1_mmap.addMemSection( ddr_shared_mem     );
mcu2_1_mmap.addMemSection( mcu2_1_main_ocram );
mcu2_1_mmap.checkOverlap();

mcu3_0_mmap = MemoryMap("mcu3_0");
mcu3_0_mmap.addMemSection( mcu_r5f_tcma_vecs );
mcu3_0_mmap.addMemSection( mcu_r5f_tcma      );
mcu3_0_mmap.addMemSection( r5f_tcmb0          );
mcu3_0_mmap.addMemSection( mcu3_0_ddr_ipc     );
mcu3_0_mmap.addMemSection( mcu3_0_ddr_resource_table  );
mcu3_0_mmap.addMemSection( mcu3_0_ddr         );
mcu3_0_mmap.addMemSection( app_log_mem        );
mcu3_0_mmap.addMemSection( tiovx_obj_desc_mem );
mcu3_0_mmap.addMemSection( app_fileio_mem        );
mcu3_0_mmap.addMemSection( ipc_vring_mem      );
mcu3_0_mmap.addMemSection( mcu3_0_ddr_local_heap  );
mcu3_0_mmap.addMemSection( ddr_shared_mem     );
mcu3_0_mmap.checkOverlap();

mcu3_1_mmap = MemoryMap("mcu3_1");
mcu3_1_mmap.addMemSection( mcu_r5f_tcma_vecs );
mcu3_1_mmap.addMemSection( mcu_r5f_tcma      );
mcu3_1_mmap.addMemSection( r5f_tcmb0          );
mcu3_1_mmap.addMemSection( mcu3_1_ddr_ipc     );
mcu3_1_mmap.addMemSection( mcu3_1_ddr_resource_table  );
mcu3_1_mmap.addMemSection( mcu3_1_ddr         );
mcu3_1_mmap.addMemSection( app_log_mem        );
mcu3_1_mmap.addMemSection( tiovx_obj_desc_mem );
mcu3_1_mmap.addMemSection( app_fileio_mem        );
mcu3_1_mmap.addMemSection( ipc_vring_mem      );
mcu3_1_mmap.addMemSection( mcu3_1_ddr_local_heap  );
mcu3_1_mmap.addMemSection( ddr_shared_mem     );
mcu3_1_mmap.checkOverlap();

c7x_1_mmap = MemoryMap("c7x_1");
c7x_1_mmap.addMemSection( c7x_1_l2           );
c7x_1_mmap.addMemSection( c7x_1_l1           );
c7x_1_mmap.addMemSection( c7x_1_msmc         );
c7x_1_mmap.addMemSection( c7x_1_ddr_ipc      );
c7x_1_mmap.addMemSection( c7x_1_ddr_resource_table      );
c7x_1_mmap.addMemSection( c7x_1_ddr_boot     );
c7x_1_mmap.addMemSection( c7x_1_ddr_vecs     );
c7x_1_mmap.addMemSection( c7x_1_ddr_secure_vecs     );
c7x_1_mmap.addMemSection( c7x_1_ddr          );
c7x_1_mmap.addMemSection( app_log_mem        );
c7x_1_mmap.addMemSection( tiovx_obj_desc_mem );
c7x_1_mmap.addMemSection( app_fileio_mem        );
c7x_1_mmap.addMemSection( ipc_vring_mem      );
c7x_1_mmap.addMemSection( c7x_1_ddr_local_heap  );
c7x_1_mmap.addMemSection( c7x_1_ddr_scratch  );
c7x_1_mmap.addMemSection( ddr_shared_mem     );
c7x_1_mmap.checkOverlap();

c7x_2_mmap = MemoryMap("c7x_2");
c7x_2_mmap.addMemSection( c7x_2_l2           );
c7x_2_mmap.addMemSection( c7x_2_l1           );
c7x_2_mmap.addMemSection( c7x_2_ddr_ipc      );
c7x_2_mmap.addMemSection( c7x_2_ddr_resource_table      );
c7x_2_mmap.addMemSection( c7x_2_ddr_boot     );
c7x_2_mmap.addMemSection( c7x_2_ddr_vecs     );
c7x_2_mmap.addMemSection( c7x_2_ddr_secure_vecs     );
c7x_2_mmap.addMemSection( c7x_2_ddr          );
c7x_2_mmap.addMemSection( app_log_mem        );
c7x_2_mmap.addMemSection( tiovx_obj_desc_mem );
c7x_2_mmap.addMemSection( app_fileio_mem        );
c7x_2_mmap.addMemSection( ipc_vring_mem      );
c7x_2_mmap.addMemSection( c7x_2_ddr_local_heap  );
c7x_2_mmap.addMemSection( c7x_2_ddr_scratch  );
c7x_2_mmap.addMemSection( ddr_shared_mem     );
c7x_2_mmap.checkOverlap();

html_mmap = MemoryMap("System Memory Map for Linux+RTOS mode");
html_mmap.addMemSection( c7x_1_l2           );
html_mmap.addMemSection( c7x_1_l1           );
html_mmap.addMemSection( c7x_2_l2           );
html_mmap.addMemSection( c7x_2_l1           );
html_mmap.addMemSection( mpu1_msmc          );
html_mmap.addMemSection( c7x_1_msmc         );
html_mmap.addMemSection( dmsc_msmc          );
html_mmap.addMemSection( mcu1_0_ddr_ipc     );
html_mmap.addMemSection( mcu1_0_ddr_resource_table      );
html_mmap.addMemSection( mcu1_0_ddr         );
html_mmap.addMemSection( mcu1_0_ddr_local_heap );
html_mmap.addMemSection( mcu1_1_ddr_ipc     );
html_mmap.addMemSection( mcu1_1_ddr_resource_table      );
html_mmap.addMemSection( mcu1_1_ddr         );
html_mmap.addMemSection( mcu1_1_ddr_local_heap );
html_mmap.addMemSection( mcu2_0_ddr_ipc     );
html_mmap.addMemSection( mcu2_0_ddr_resource_table      );
html_mmap.addMemSection( mcu2_0_ddr         );
html_mmap.addMemSection( mcu2_0_ddr_local_heap );
html_mmap.addMemSection( mcu2_1_ddr_ipc     );
html_mmap.addMemSection( mcu2_1_ddr_resource_table      );
html_mmap.addMemSection( mcu2_1_ddr         );
html_mmap.addMemSection( mcu2_1_ddr_local_heap );
html_mmap.addMemSection( mcu3_0_ddr_ipc     );
html_mmap.addMemSection( mcu3_0_ddr_resource_table      );
html_mmap.addMemSection( mcu3_0_ddr         );
html_mmap.addMemSection( mcu3_0_ddr_local_heap );
html_mmap.addMemSection( mcu3_1_ddr_ipc     );
html_mmap.addMemSection( mcu3_1_ddr_resource_table      );
html_mmap.addMemSection( mcu3_1_ddr         );
html_mmap.addMemSection( mcu3_1_ddr_local_heap );
html_mmap.addMemSection( c7x_1_ddr_ipc     );
html_mmap.addMemSection( c7x_1_ddr_resource_table     );
html_mmap.addMemSection( c7x_1_ddr_boot    );
html_mmap.addMemSection( c7x_1_ddr_vecs    );
html_mmap.addMemSection( c7x_1_ddr_secure_vecs    );
html_mmap.addMemSection( c7x_1_ddr_local_heap         );
html_mmap.addMemSection( c7x_1_ddr_scratch );
html_mmap.addMemSection( c7x_1_ddr         );
html_mmap.addMemSection( c7x_2_ddr_ipc     );
html_mmap.addMemSection( c7x_2_ddr_resource_table     );
html_mmap.addMemSection( c7x_2_ddr_boot    );
html_mmap.addMemSection( c7x_2_ddr_vecs    );
html_mmap.addMemSection( c7x_2_ddr_secure_vecs    );
html_mmap.addMemSection( c7x_2_ddr_local_heap         );
html_mmap.addMemSection( c7x_2_ddr_scratch );
html_mmap.addMemSection( c7x_2_ddr         );
html_mmap.addMemSection( app_log_mem        );
html_mmap.addMemSection( tiovx_obj_desc_mem );
html_mmap.addMemSection( app_fileio_mem        );
html_mmap.addMemSection( ipc_vring_mem      );
html_mmap.addMemSection( ddr_shared_mem     );
html_mmap.addMemSection( tiovx_log_rt_mem );
html_mmap.addMemSection( mcu2_0_main_ocram );
html_mmap.addMemSection( mcu2_1_main_ocram );
html_mmap.checkOverlap();

c_header_mmap = MemoryMap("Memory Map for C header file");
c_header_mmap.addMemSection( c7x_1_l2           );
c_header_mmap.addMemSection( c7x_1_l1           );
c_header_mmap.addMemSection( c7x_1_msmc         );
c_header_mmap.addMemSection( c7x_2_l2           );
c_header_mmap.addMemSection( c7x_2_l1           );
c_header_mmap.addMemSection( mcu1_0_ddr_ipc     );
c_header_mmap.addMemSection( mcu1_1_ddr_ipc     );
c_header_mmap.addMemSection( mcu2_0_ddr_ipc     );
c_header_mmap.addMemSection( mcu2_1_ddr_ipc     );
c_header_mmap.addMemSection( mcu3_0_ddr_ipc     );
c_header_mmap.addMemSection( mcu3_1_ddr_ipc     );
c_header_mmap.addMemSection( c7x_1_ddr_ipc     );
c_header_mmap.addMemSection( c7x_2_ddr_ipc     );
c_header_mmap.addMemSection( mcu1_0_ddr_total     );
c_header_mmap.addMemSection( mcu1_1_ddr_total     );
c_header_mmap.addMemSection( mcu2_0_ddr_total     );
c_header_mmap.addMemSection( mcu2_1_ddr_total     );
c_header_mmap.addMemSection( mcu3_0_ddr_total     );
c_header_mmap.addMemSection( mcu3_1_ddr_total     );
c_header_mmap.addMemSection( c7x_1_ddr_total     );
c_header_mmap.addMemSection( c7x_2_ddr_total     );

c_header_mmap.addMemSection( mcu1_0_ddr_local_heap);
c_header_mmap.addMemSection( mcu1_1_ddr_local_heap);
c_header_mmap.addMemSection( mcu2_0_ddr_local_heap);
c_header_mmap.addMemSection( mcu2_1_ddr_local_heap);
c_header_mmap.addMemSection( mcu3_0_ddr_local_heap);
c_header_mmap.addMemSection( mcu3_1_ddr_local_heap);
c_header_mmap.addMemSection( c7x_1_ddr_local_heap);
c_header_mmap.addMemSection( c7x_1_ddr_scratch);
c_header_mmap.addMemSection( c7x_2_ddr_local_heap);
c_header_mmap.addMemSection( c7x_2_ddr_scratch);
c_header_mmap.addMemSection( tiovx_log_rt_mem );
c_header_mmap.addMemSection( app_log_mem        );
c_header_mmap.addMemSection( tiovx_obj_desc_mem );
c_header_mmap.addMemSection( app_fileio_mem        );
c_header_mmap.addMemSection( ipc_vring_mem      );
c_header_mmap.addMemSection( ddr_shared_mem     );
c_header_mmap.addMemSection( ddr_shared_mem_phys     );
c_header_mmap.addMemSection( c7x_1_msmc         );
c_header_mmap.addMemSection( mcu2_0_main_ocram  );
c_header_mmap.addMemSection( mcu2_1_main_ocram  );
c_header_mmap.addMemSection( mcu2_0_main_ocram_phys  );
c_header_mmap.addMemSection( mcu2_1_main_ocram_phys  );
c_header_mmap.checkOverlap();

dts_mmap = MemoryMap("Memory Map for Linux kernel dts/dtsi file");
dts_mmap.addMemSection( mcu1_0_ddr_ipc     );
dts_mmap.addMemSection( mcu1_0_ddr_total   );
dts_mmap.addMemSection( mcu1_1_ddr_ipc     );
dts_mmap.addMemSection( mcu1_1_ddr_total   );
dts_mmap.addMemSection( mcu2_0_ddr_ipc     );
dts_mmap.addMemSection( mcu2_0_ddr_total   );
dts_mmap.addMemSection( mcu2_1_ddr_ipc     );
dts_mmap.addMemSection( mcu2_1_ddr_total   );
dts_mmap.addMemSection( mcu3_0_ddr_ipc     );
dts_mmap.addMemSection( mcu3_0_ddr_total   );
dts_mmap.addMemSection( mcu3_1_ddr_ipc     );
dts_mmap.addMemSection( mcu3_1_ddr_total   );
dts_mmap.addMemSection( c7x_1_ddr_ipc      );
dts_mmap.addMemSection( c7x_1_ddr_total    );
dts_mmap.addMemSection( c7x_2_ddr_ipc      );
dts_mmap.addMemSection( c7x_2_ddr_total    );
dts_mmap.addMemSection( vision_apps_ddr_total );
dts_mmap.addMemSection( ipc_vring_mem      );
dts_mmap.addMemSection( vision_apps_core_heaps_lo );
dts_mmap.addMemSection( c7x_ddr_heaps_hi );
dts_mmap.addMemSection( ddr_shared_mem_phys );
dts_mmap.checkOverlap();

#
# Generate linker command files containing "MEMORY" definitions
#
LinkerCmdFile(c7x_1_mmap , "./c7x_1/linker_mem_map.cmd" ).export();
LinkerCmdFile(c7x_2_mmap , "./c7x_2/linker_mem_map.cmd" ).export();
LinkerCmdFile(mcu1_0_mmap, "./mcu1_0/linker_mem_map.cmd").export();
LinkerCmdFile(mcu1_1_mmap, "./mcu1_1/linker_mem_map.cmd").export();
LinkerCmdFile(mcu2_0_mmap, "./mcu2_0/linker_mem_map.cmd").export();
LinkerCmdFile(mcu2_1_mmap, "./mcu2_1/linker_mem_map.cmd").export();
LinkerCmdFile(mcu3_0_mmap, "./mcu3_0/linker_mem_map.cmd").export();
LinkerCmdFile(mcu3_1_mmap, "./mcu3_1/linker_mem_map.cmd").export();

HtmlMmapTable(html_mmap, "./system_memory_map.html").export();

CHeaderFile(c_header_mmap, 0x880000000, 0x100000000, "./app_mem_map.h").export();

DtsFile(dts_mmap, "./k3-j721s2-rtos-memory-map.dtsi").export();
