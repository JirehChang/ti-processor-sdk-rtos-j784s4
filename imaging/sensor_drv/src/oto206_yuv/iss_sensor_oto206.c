/*
 *
 * Copyright (c) 2020 Texas Instruments Incorporated
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
#include "iss_sensor_oto206.h"
#include "ub9xx_oto206_serdes_config.h"

static IssSensor_CreateParams  oto206CreatePrms = {
    OTO206_UYVY,     /*sensor name*/
    0x6,                             /*i2cInstId*/
    {SENSOR_0_I2C_ALIAS, SENSOR_1_I2C_ALIAS, SENSOR_2_I2C_ALIAS, SENSOR_3_I2C_ALIAS, 0, 0, 0, 0},   /*i2cAddrSensor*/
    {SER_0_I2C_ALIAS, SER_1_I2C_ALIAS, SER_2_I2C_ALIAS, SER_3_I2C_ALIAS, 0, 0, 0, 0},      /*i2cAddrSer*/
    /*IssSensor_Info*/
    {
        {
            OTO206_OUT_WIDTH,               /*width*/
            OTO206_OUT_HEIGHT,              /*height*/
            1,                              /*num_exposures*/
            vx_false_e,                     /*line_interleaved*/
            {
                {VX_DF_IMAGE_UYVY, 7},    /*dataFormat and MSB [0]*/
            },
            0,                              /*meta_height_before*/
            0,                              /*meta_height_after*/
        },
        ISS_SENSOR_OTO206_FEATURES,     /*features*/
        ALGORITHMS_ISS_AEWB_MODE_NONE,  /*aewbMode*/
        30,                             /*fps*/
        4,                              /*numDataLanes*/
        {1, 2, 3, 4},                   /*dataLanesMap*/
        {0, 0, 0, 0},                   /*dataLanesPolarity*/
        800,                            /*CSI Clock*/
    },
    8,                                  /*numChan*/
    206,                                /*dccId*/
};

static IssSensorFxns           oto206SensorFxns = {
    oto206_Probe,
    oto206_Config,
    oto206_StreamOn,
    oto206_StreamOff,
    oto206_PowerOn,
    oto206_PowerOff,
    NULL,
    NULL,
    oto206_GetDccParams,
    oto206_InitAewbConfig,
    NULL,
    NULL,
    NULL,
    oto206_deinit,
    NULL,
    NULL
};

static IssSensorIntfParams     oto206SensorIntfPrms = {
    0,                                /*isMultiChannel*/
    4,                              /*numCSI2Lanes*/
    1,                              /*inCsi2VirtualChanNum*/
    1,                /* isCplxCfgValid */
     {
        {0, 1}, /* Clock Lane */
        {0, 2}, /* data1Lane */
        {0, 3}, /* data2Lane */
        {0, 4}, /* data3Lane*/
        {0, 5}, /* data4Lane */
    },
    800,                 /* csi2PhyClk */ 
    0,             /*sensorBroadcast*/
    0,             /*enableFsin*/
};

IssSensorConfig     oto206SensorRegConfig = {
    ub9xxDesCfg_OTO206,     /*desCfgPreScript*/
    ub9xxSerCfg_OTO206,      /*serCfgPreScript*/
    NULL,      /*sensorCfgPreScript*/
    ub9xxOTO206DesCSI2Enable,        /*desCfgPostScript*/
    NULL,                    /*serCfgPostScript*/
    NULL,                    /*sensorCfgPostScript*/
};


IssSensors_Handle oto206SensorHandle = {
    1,                                 /*isUsed*/
    &oto206CreatePrms,                /*CreatePrms*/
    &oto206SensorFxns,                /*SensorFxns*/
    &oto206SensorIntfPrms,            /*SensorIntfPrms*/
};

/*
 * \brief DCC Parameters of oto206
 */
IssCapture_CmplxIoLaneCfg           oto206Csi2CmplxIoLaneCfg;

extern IssSensors_Handle * gIssSensorTable[ISS_SENSORS_MAX_SUPPORTED_SENSOR];

int32_t IssSensor_oto206_Init()
{
    int32_t status;
    status = IssSensor_Register(&oto206SensorHandle);
    if(0 != status)
    {
        printf("IssSensor_oto206_Init failed \n");
    }

    return status;
}

/*******************************************************************************
 *  Local Functions Definition
 *******************************************************************************
 */

static int32_t oto206_Probe(uint32_t chId, void *pSensorHdl)
{
    int32_t status = -1;
    return (status);
}

static int32_t oto206_Config(uint32_t chId, void *pSensorHdl, uint32_t sensor_features_requested)
{
    int32_t status = 0;
    I2cParams *deserCfg = NULL;
    I2cParams *serCfg = NULL;
    int8_t ub9xxInstanceId = getUB960InstIdFromChId(chId);
    uint32_t i2cInstId;
    IssSensors_Handle * pSenHandle = (IssSensors_Handle*)pSensorHdl;
    IssSensor_CreateParams * pCreatePrms;
	uint8_t chNum = 0, i2cAddr = 0;
    assert(NULL != pSenHandle);
    pCreatePrms = pSenHandle->createPrms;
    assert(NULL != pCreatePrms);

    deserCfg =oto206SensorRegConfig.desCfgPreScript;
    serCfg = oto206SensorRegConfig.serCfgPreScript;
	if(ub9xxInstanceId < 0)
    {
        printf("oto206_Config Invalid ub960InstanceId \n");
        return -1;
    }
	Board_fpdU960GetI2CAddr(&chNum, &i2cAddr, ub9xxInstanceId);
printf("Jireh: func:%s(), line:%d, chNum:%d, i2cAddr:%d\n", __FUNCTION__, __LINE__, chNum, i2cAddr);
    i2cInstId = (uint32_t)chNum;

    if(NULL != deserCfg)
    {
        status = ub960_cfgScript(deserCfg, ub9xxInstanceId);
    }

    if(0 == status)
    {
        if(NULL != serCfg)
        {
            status = ub953_cfgScript(i2cInstId, pCreatePrms->i2cAddrSer[chId], serCfg);
        }
    }

    return (status);
}

static int32_t oto206_StreamOn(uint32_t chId, void *pSensorHdl)
{
    int32_t status = 0;
    int8_t ub9xxInstanceId = getUB960InstIdFromChId(chId);

    if(ub9xxInstanceId < 0)
    {
        printf("Invalid ub9xxInstanceId \n");
        return 0xFF;
    }

    /*Start Streaming*/
    status |= ub960_cfgScript(ub9xxOTO206DesCSI2Enable, ub9xxInstanceId);
    return (status);
}

static int32_t oto206_StreamOff(uint32_t chId, void *pSensorHdl)
{
    int32_t status = 0;
    int8_t ub9xxInstanceId = getUB960InstIdFromChId(chId);

    if(ub9xxInstanceId < 0)
    {
        printf("Invalid ub9xxInstanceId \n");
        return 0xFF;
    }

    /*Stop Streaming*/
    status |= ub960_cfgScript(ub9xxOTO206DesCSI2Disable, ub9xxInstanceId);
    return (status);
}

static int32_t oto206_PowerOn(uint32_t chId, void *pSensorHdl)
{
    int32_t status = 0;
    return status;
}

static int32_t oto206_PowerOff(uint32_t chId, void *pSensorHdl)
{
    int32_t status = 0;
    return (status);
}

static int32_t oto206_GetDccParams(uint32_t chId, void *pSensorHdl, IssSensor_DccParams *pDccPrms)
{
    int32_t status = 0;
    return (status);
}

static void oto206_InitAewbConfig(uint32_t chId, void *pSensorHdl)
{
    return;
}

static void oto206_deinit (uint32_t chId, void *pSensorHdl)
{
    return;
}


