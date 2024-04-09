/* 
 * This file is AUTO GENERATED by PyTI_PSDK_RTOS tool. 
 * It is NOT recommended to manually edit this file 
 */ 
/* 
 * 
 * Copyright (c) 2018 Texas Instruments Incorporated 
 * 
 * All rights reserved not granted herein. 
 * 
 * Limited License. 
 * 
 * Texas Instruments Incorporated grants a world-wide, royalty-free, non-exclusive 
 * license under copyrights and patents it now or hereafter owns or controls to make, 
 * have made, use, import, offer to sell and sell ("Utilize") this software subject to the 
 * terms herein.  With respect to the foregoing patent license, such license is granted 
 * solely to the extent that any such patent is necessary to Utilize the software alone. 
 * The patent license shall not apply to any combinations which include this software, 
 * other than combinations with devices manufactured by or for TI ("TI Devices"). 
 * No hardware patent is licensed hereunder. 
 * 
 * Redistributions must preserve existing copyright notices and reproduce this license 
 * (including the above copyright notice and the disclaimer and (if applicable) source 
 * code license limitations below) in the documentation and/or other materials provided 
 * with the distribution 
 * 
 * Redistribution and use in binary form, without modification, are permitted provided 
 * that the following conditions are met: 
 * 
 *        No reverse engineering, decompilation, or disassembly of this software is 
 * permitted with respect to any software provided in binary form. 
 * 
 *        any redistribution and use are licensed by TI for use only with TI Devices. 
 * 
 *        Nothing shall obligate TI to provide you with source code for the software 
 * licensed and provided to you in object code. 
 * 
 * If software source code is provided to you, modification and redistribution of the 
 * source code are permitted provided that the following conditions are met: 
 * 
 *        any redistribution and use of the source code, including any resulting derivative 
 * works, are licensed by TI for use only with TI Devices. 
 * 
 *        any redistribution and use of any object code compiled from the source code 
 * and any resulting derivative works, are licensed by TI for use only with TI Devices. 
 * 
 * Neither the name of Texas Instruments Incorporated nor the names of its suppliers 
 * 
 * may be used to endorse or promote products derived from this software without 
 * specific prior written permission. 
 * 
 * DISCLAIMER. 
 * 
 * THIS SOFTWARE IS PROVIDED BY TI AND TI'S LICENSORS "AS IS" AND ANY EXPRESS 
 * OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
 * IN NO EVENT SHALL TI AND TI'S LICENSORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY 
 * OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
 * OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED 
 * OF THE POSSIBILITY OF SUCH DAMAGE. 
 * 
 */ 

MEMORY
{
    /* L2 for C7x_1 [ size 448.00 KB ] */
    L2RAM_C7x_1              ( RWIX ) : ORIGIN = 0x64800000 , LENGTH = 0x00070000
    /* L1 for C7x_1 [ size 16.00 KB ] */
    L1RAM_C7x_1              ( RWIX ) : ORIGIN = 0x64E00000 , LENGTH = 0x00004000
    /* MSMC for C7x_1 [ size  3.00 MB ] */
    MSMC_C7x_1               ( RWIX ) : ORIGIN = 0x68000000 , LENGTH = 0x00300000
    /* Memory for IPC Vring's. MUST be non-cached or cache-coherent [ size 48.00 MB ] */
    IPC_VRING_MEM                     : ORIGIN = 0xAC000000 , LENGTH = 0x03000000
    /* Memory for remote core logging [ size 256.00 KB ] */
    APP_LOG_MEM                       : ORIGIN = 0xAF000000 , LENGTH = 0x00040000
    /* Memory for TI OpenVX shared memory. MUST be non-cached or cache-coherent [ size 63.75 MB ] */
    TIOVX_OBJ_DESC_MEM                : ORIGIN = 0xAF040000 , LENGTH = 0x03FC0000
    /* Memory for remote core file operations [ size  4.00 MB ] */
    APP_FILEIO_MEM                    : ORIGIN = 0xB3000000 , LENGTH = 0x00400000
    /* DDR for C7x_1 for Linux IPC [ size 1024.00 KB ] */
    DDR_C7x_1_IPC            ( RWIX ) : ORIGIN = 0xB4000000 , LENGTH = 0x00100000
    /* DDR for C7x_1 for Linux resource table [ size 1024 B ] */
    DDR_C7x_1_RESOURCE_TABLE ( RWIX ) : ORIGIN = 0xB4100000 , LENGTH = 0x00000400
    /* DDR for C7x_1 for boot section [ size 1024 B ] */
    DDR_C7x_1_BOOT           ( RWIX ) : ORIGIN = 0xB4200000 , LENGTH = 0x00000400
    /* DDR for C7x_1 for vecs section [ size 16.00 KB ] */
    DDR_C7x_1_VECS           ( RWIX ) : ORIGIN = 0xB4400000 , LENGTH = 0x00004000
    /* DDR for C7x_1 for secure vecs section [ size 16.00 KB ] */
    DDR_C7x_1_SECURE_VECS    ( RWIX ) : ORIGIN = 0xB4600000 , LENGTH = 0x00004000
    /* DDR for C7x_1 for code/data [ size 41.98 MB ] */
    DDR_C7x_1                ( RWIX ) : ORIGIN = 0xB4604000 , LENGTH = 0x029FC000
    /* Memory for shared memory buffers in DDR [ size 512.00 MB ] */
    DDR_SHARED_MEM                    : ORIGIN = 0xC0000000 , LENGTH = 0x20000000
    /* Virtual address of non-cacheable DDR for c7x_1 for local heap [ size 128.00 MB ] */
    DDR_C7X_1_LOCAL_HEAP_NON_CACHEABLE ( RWIX ) : ORIGIN = 0x100000000 , LENGTH = 0x08000000
    /* Virtual address of cacheable DDR for c7x_1 for local heap [ size 128.00 MB ] */
    DDR_C7X_1_LOCAL_HEAP     ( RWIX ) : ORIGIN = 0x108000000 , LENGTH = 0x08000000
    /* Virtual address of non-cacheable DDR for c7x_1 for Scratch Memory [ size 128.00 MB ] */
    DDR_C7X_1_SCRATCH_NON_CACHEABLE ( RWIX ) : ORIGIN = 0x110000000 , LENGTH = 0x08000000
    /* Virtual address of cacheable DDR for c7x_1 for Scratch Memory [ size 128.00 MB ] */
    DDR_C7X_1_SCRATCH        ( RWIX ) : ORIGIN = 0x118000000 , LENGTH = 0x08000000
    /* Virtual address of non-cacheable DDR for c7x_2 for local heap wrt c7x_1 [ size 128.00 MB ] */
    DDR_C7X_1_2_LOCAL_HEAP_NON_CACHEABLE ( RWIX ) : ORIGIN = 0x120000000 , LENGTH = 0x08000000
    /* Virtual address of non-cacheable DDR for c7x_3 for local heap wrt c7x_1 [ size 128.00 MB ] */
    DDR_C7X_1_3_LOCAL_HEAP_NON_CACHEABLE ( RWIX ) : ORIGIN = 0x128000000 , LENGTH = 0x08000000
    /* Virtual address of non-cacheable DDR for c7x_4 for local heap wrt c7x_1 [ size 128.00 MB ] */
    DDR_C7X_1_4_LOCAL_HEAP_NON_CACHEABLE ( RWIX ) : ORIGIN = 0x130000000 , LENGTH = 0x08000000
    /* Virtual address of cacheable DDR for c7x_2 for local heap wrt c7x_1 [ size 128.00 MB ] */
    DDR_C7X_1_2_LOCAL_HEAP   ( RWIX ) : ORIGIN = 0x138000000 , LENGTH = 0x08000000
    /* Virtual address of cacheable DDR for c7x_3 for local heap wrt c7x_1 [ size 128.00 MB ] */
    DDR_C7X_1_3_LOCAL_HEAP   ( RWIX ) : ORIGIN = 0x140000000 , LENGTH = 0x08000000
    /* Virtual address of cacheable DDR for c7x_4 for local heap wrt c7x_1 [ size 128.00 MB ] */
    DDR_C7X_1_4_LOCAL_HEAP   ( RWIX ) : ORIGIN = 0x148000000 , LENGTH = 0x08000000
    /* Virtual address of non-cacheable DDR for c7x_2 for Scratch Memory wrt c7x_1 [ size 128.00 MB ] */
    DDR_C7X_1_2_SCRATCH_NON_CACHEABLE ( RWIX ) : ORIGIN = 0x150000000 , LENGTH = 0x08000000
    /* Virtual address of non-cacheable DDR for c7x_3 for Scratch Memory wrt c7x_1 [ size 128.00 MB ] */
    DDR_C7X_1_3_SCRATCH_NON_CACHEABLE ( RWIX ) : ORIGIN = 0x158000000 , LENGTH = 0x08000000
    /* Virtual address of non-cacheable DDR for c7x_4 for Scratch Memory wrt c7x_1 [ size 128.00 MB ] */
    DDR_C7X_1_4_SCRATCH_NON_CACHEABLE ( RWIX ) : ORIGIN = 0x160000000 , LENGTH = 0x08000000
    /* Virtual address of cacheable DDR for c7x_2 for Scratch Memory wrt c7x_1 [ size 128.00 MB ] */
    DDR_C7X_1_2_SCRATCH      ( RWIX ) : ORIGIN = 0x168000000 , LENGTH = 0x08000000
    /* Virtual address of cacheable DDR for c7x_3 for Scratch Memory wrt c7x_1 [ size 128.00 MB ] */
    DDR_C7X_1_3_SCRATCH      ( RWIX ) : ORIGIN = 0x170000000 , LENGTH = 0x08000000
    /* Virtual address of cacheable DDR for c7x_4 for Scratch Memory wrt c7x_1 [ size 128.00 MB ] */
    DDR_C7X_1_4_SCRATCH      ( RWIX ) : ORIGIN = 0x178000000 , LENGTH = 0x08000000
}
