/*
 * Copyright (c) 2017-2018, Texas Instruments Incorporated
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * *  Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * *  Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * *  Neither the name of Texas Instruments Incorporated nor the names of
 *    its contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/*
 *  \file ipc_rsctable.h
 *
 *  \brief Define the resource table entries for all R5F cores. This will be
 *  incorporated into corresponding base images, and used by the remoteproc
 *  on the host-side to allocated/reserve resources.
 *
 */

#ifndef IPC_RSCTABLE_H_
#define IPC_RSCTABLE_H_

#ifdef __cplusplus
extern "C" {
#endif

#if defined(CPU_c7x_1)
#define BUILD_C7X_1
#define BUILD_C7X
#endif

#if !defined(MCU_PLUS_SDK)
#include <ti/drv/ipc/include/ipc_rsctypes.h>
#include <stddef.h>
#else
#include <drivers/ipc_rpmsg/include/ipc_rpmsg_linux_resource_table.h>
#define NUM_ENTRIES      2
#define TYPE_VDEV        RPMESSAGE_RSC_TYPE_VDEV
#define VIRTIO_ID_RPMSG  RPMESSAGE_RSC_VIRTIO_ID_RPMSG
#define TRACE_INTS_VER0  RPMESSAGE_RSC_TRACE_INTS_VER0
#define TRACE_INTS_VER1  RPMESSAGE_RSC_TRACE_INTS_VER0
#define TYPE_TRACE       RPMESSAGE_RSC_TYPE_TRACE

typedef RPMessage_ResourceTable Ipc_ResourceTable;

#define rpmsg_vdev  vdev
#if defined(BUILD_C7X_1)
#pragma diag_suppress 70
#endif
#endif
#include <app_mem_map.h>

#ifdef SYSBIOS
  #include <xdc/runtime/SysMin.h>
#else
  #include "ipc_trace.h"
#endif

/* Linux kernel defines this as (-1), below define avoids compile warnings */
/** \brief Macro to specify memory needs to be dynamically allocated */
#define RPMSG_VRING_ADDR_ANY (~0)

/*
 * Sizes of the virtqueues (expressed in number of buffers supported,
 * and must be power of 2)
 */
#define R5F_RPMSG_VQ0_SIZE      256
#define R5F_RPMSG_VQ1_SIZE      256
#define C7X_RPMSG_VQ0_SIZE      256
#define C7X_RPMSG_VQ1_SIZE      256

/* flip up bits whose indices represent features we support */
#define RPMSG_R5F_C0_FEATURES   1
#define RPMSG_C7X_DSP_FEATURES  1

#ifdef SYSBIOS
  extern __T1_xdc_runtime_SysMin_Module_State__outbuf xdc_runtime_SysMin_Module_State_0_outbuf__A[];
  #define TRACEBUFADDR ((uintptr_t)&xdc_runtime_SysMin_Module_State_0_outbuf__A)
#else
  #define TRACEBUFADDR ((uintptr_t)&Ipc_traceBuffer)
#endif

const Ipc_ResourceTable ti_ipc_remoteproc_ResourceTable __attribute__ ((section (".resource_table"), aligned (4096))) =
{
    1,                   /* we're the first version that implements this */
    NUM_ENTRIES,         /* number of entries in the table */
    0, 0,                /* reserved, must be zero */

    /* offsets to entries */
    {
        offsetof(Ipc_ResourceTable, rpmsg_vdev),
        offsetof(Ipc_ResourceTable, trace),
    },

    /* rpmsg vdev entry */
    {
        TYPE_VDEV, VIRTIO_ID_RPMSG, 0,
#if defined (CPU_c7x_1)
        RPMSG_C7X_DSP_FEATURES, 0, 0, 0, 2, { 0, 0 },
#else
        RPMSG_R5F_C0_FEATURES, 0, 0, 0, 2, { 0, 0 },
#endif
        /* no config data */
    },
    /* the two vrings */
#if defined (CPU_mcu1_0)
    { RPMSG_VRING_ADDR_ANY, 4096, R5F_RPMSG_VQ0_SIZE, 1, 0 },
    { RPMSG_VRING_ADDR_ANY, 4096, R5F_RPMSG_VQ1_SIZE, 2, 0 },
#elif defined (CPU_c7x_1)
    { RPMSG_VRING_ADDR_ANY, 4096, C7X_RPMSG_VQ0_SIZE, 1, 0 },
    { RPMSG_VRING_ADDR_ANY, 4096, C7X_RPMSG_VQ1_SIZE, 2, 0 },
#else
    #error CPU_<cpu name> not defined
#endif

    {
#ifdef CPU_c7x_1
        (TRACE_INTS_VER1 | TYPE_TRACE), TRACEBUFADDR, 0x80000, 0, "trace:r5f0",
#else
        (TRACE_INTS_VER0 | TYPE_TRACE), TRACEBUFADDR, 0x80000, 0, "trace:r5f0",
#endif
    },
};

void *appGetIpcResourceTable()
{
    return (void*)&ti_ipc_remoteproc_ResourceTable;
}


#ifdef __cplusplus
}
#endif

#endif /* IPC_RSCTABLE_H_ */
