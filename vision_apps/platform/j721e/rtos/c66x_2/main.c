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
 * *       No reverse engineering, decompilation, or disassembly of this software is
 * permitted with respect to any software provided in binary form.
 *
 * *       any redistribution and use are licensed by TI for use only with TI Devices.
 *
 * *       Nothing shall obligate TI to provide you with source code for the software
 * licensed and provided to you in object code.
 *
 * If software source code is provided to you, modification and redistribution of the
 * source code are permitted provided that the following conditions are met:
 *
 * *       any redistribution and use of the source code, including any resulting derivative
 * works, are licensed by TI for use only with TI Devices.
 *
 * *       any redistribution and use of any object code compiled from the source code
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

#include <app.h>
#include <utils/console_io/include/app_log.h>
#include <utils/misc/include/app_misc.h>
#include <utils/rtos/include/app_rtos.h>
#include <stdio.h>
#include <string.h>
#include <ti/osal/osal.h>
#include <ti/osal/CacheP.h>
#include <ti/drv/sciclient/sciclient.h>
#include <app_ipc_rsctable.h>
#ifdef SYSBIOS
#include <ti/sysbios/family/c66/Cache.h>
#endif
#include <utils/perf_stats/include/app_perf_stats.h>

void appCacheMarInit(void);

static void appMain(void* arg0, void* arg1)
{
    appUtilsTaskInit();
    appInit();
    appRun();
    #if 1
    while(1)
    {
        appLogWaitMsecs(100u);
    }
    #else
    appDeInit();
    #endif
}

void StartupEmulatorWaitFxn (void)
{
    volatile uint32_t enableDebug = 0;
    do
    {
    }while (enableDebug);
}

static uint8_t gTskStackMain[8*1024]
__attribute__ ((section(".bss:taskStackSection")))
__attribute__ ((aligned(8192)))
    ;

int main(void)
{
    app_rtos_task_params_t tskParams;
    app_rtos_task_handle_t task;

    /* This is for debug purpose - see the description of function header */
    StartupEmulatorWaitFxn();

    /* set cache, non-cache sections for C6x */
    appCacheMarInit();

    OS_init();

    appPerfStatsInit();

    appRtosTaskParamsInit(&tskParams);
    tskParams.priority = 8u;
    tskParams.stack = gTskStackMain;
    tskParams.stacksize = sizeof (gTskStackMain);
    tskParams.taskfxn = &appMain;
    task = appRtosTaskCreate(&tskParams);
    if(NULL == task)
    {
        OS_stop();
    }
    OS_start();

    return 0;
}

void appCacheMarInit(void)
{
#ifdef SYSBIOS
    /* enable cache for cached sections */
    Cache_setMar((Ptr)DDR_C66x_2_DTS_ADDR, DDR_C66x_2_DTS_SIZE, Cache_Mar_ENABLE);
    Cache_setMar((Ptr)DDR_C66X_2_LOCAL_HEAP_ADDR, DDR_C66X_2_LOCAL_HEAP_SIZE, Cache_Mar_ENABLE);
    Cache_setMar((Ptr)DDR_C66X_2_SCRATCH_ADDR, DDR_C66X_2_SCRATCH_SIZE, Cache_Mar_ENABLE);
    Cache_setMar((Ptr)DDR_SHARED_MEM_ADDR, DDR_SHARED_MEM_SIZE, Cache_Mar_ENABLE);

    /* disable cache for non-cached sections */
    Cache_setMar((Ptr)DDR_C66x_2_IPC_ADDR, DDR_C66x_2_IPC_SIZE, Cache_Mar_DISABLE);
    Cache_setMar((Ptr)APP_LOG_MEM_ADDR, APP_LOG_MEM_SIZE, Cache_Mar_DISABLE);
    Cache_setMar((Ptr)TIOVX_OBJ_DESC_MEM_ADDR, TIOVX_OBJ_DESC_MEM_SIZE, Cache_Mar_DISABLE);
    Cache_setMar((Ptr)IPC_VRING_MEM_ADDR, IPC_VRING_MEM_SIZE, Cache_Mar_DISABLE);
    Cache_setMar((Ptr)TIOVX_LOG_RT_MEM_ADDR, TIOVX_LOG_RT_MEM_SIZE, Cache_Mar_DISABLE);
#else
    /* enable cache for cached sections */
    CacheP_setMar((void *)DDR_C66x_2_DTS_ADDR, DDR_C66x_2_DTS_SIZE, CacheP_Mar_ENABLE);
    CacheP_setMar((void *)DDR_C66X_2_LOCAL_HEAP_ADDR, DDR_C66X_2_LOCAL_HEAP_SIZE, CacheP_Mar_ENABLE);
    CacheP_setMar((void *)DDR_C66X_2_SCRATCH_ADDR, DDR_C66X_2_SCRATCH_SIZE, CacheP_Mar_ENABLE);
    CacheP_setMar((void *)DDR_SHARED_MEM_ADDR, DDR_SHARED_MEM_SIZE, CacheP_Mar_ENABLE);

    /* disable cache for non-cached sections */
    CacheP_setMar((void *)DDR_C66x_2_IPC_ADDR, DDR_C66x_2_IPC_SIZE, CacheP_Mar_DISABLE);
    CacheP_setMar((void *)APP_LOG_MEM_ADDR, APP_LOG_MEM_SIZE, CacheP_Mar_DISABLE);
    CacheP_setMar((void *)TIOVX_OBJ_DESC_MEM_ADDR, TIOVX_OBJ_DESC_MEM_SIZE, CacheP_Mar_DISABLE);
    CacheP_setMar((void *)IPC_VRING_MEM_ADDR, IPC_VRING_MEM_SIZE, CacheP_Mar_DISABLE);
    CacheP_setMar((void *)TIOVX_LOG_RT_MEM_ADDR, TIOVX_LOG_RT_MEM_SIZE, CacheP_Mar_DISABLE);
#endif
}

uint64_t appUdmaVirtToPhyAddrConversion(const void *virtAddr,
                                      uint32_t chNum,
                                      void *appData)
{

  return (uint64_t)virtAddr;
}
