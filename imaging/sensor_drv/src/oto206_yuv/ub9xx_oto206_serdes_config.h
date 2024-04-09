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
#ifndef _UB96X_OTO206_SERDES_H_
#define _UB96X_OTO206_SERDES_H_

#define OTO206_OUT_WIDTH           (1280U)
#define OTO206_OUT_HEIGHT          (800U)

#define OTO206_DES_CFG_SIZE    (40U)
I2cParams ub9xxDesCfg_OTO206[OTO206_DES_CFG_SIZE] = {

    /*TI960 4 input port,one output port*/
    {0x01, 0x02, 0x1},  /*digital reset include registers*/
    {0x1f, 0x02, 0x1},  /*0x02 800Mhz, 0x03 400Mhz,00 1.6GHz,01 1.2GHz*/
    {0xbc, 0x00, 0x1},
		
	/*RX0 VC=0*/
    {0x4C, 0x01, 0x1},
	{0x58, 0x58, 0x1},   /*enable pass throu,Enable Back channel, set to 2.5Mbs for TI913*/
	{0x6d, 0x7f, 0x1},   /*RAW10 mode for TI913,TI933*/
	{0x7c, 0xc0, 0x1},   /*8-bit processing using lower 8 bits*/
    /*{0x5b, 0xba, 0x1},    //this field is normally loaded automatically from remote Serializer*/
    {0x5c, SER_0_I2C_ALIAS, 0x1},
    {0x5d, 0x20, 0x1},    /* sensor physical IIC address*/
    {0x65, SENSOR_0_I2C_ALIAS, 0x1},
    {0x70, 0x1e, 0x1},
	
	/*RX1 VC=1*/
    {0x4c, 0x12, 0x1},
	{0x58, 0x58, 0x1},
	{0x6d, 0x7f, 0x1},  /*RAW10 mode for TI913,TI933*/
	{0x7c, 0xc0, 0x1},
    /*{0x5b, 0xb0, 0x1},   //this field is normally loaded automatically from remote Serializer*/
    {0x5c, SER_1_I2C_ALIAS, 0x1},
    {0x5d, 0x20, 0x1},    /*sensor physical IIC address*/
    {0x65, SENSOR_1_I2C_ALIAS, 0x1},
    {0x70, 0x5e, 0x1},
	
	/*RX2 VC=2*/
    {0x4c, 0x24, 0x1},
	{0x58, 0x58, 0x1},
	{0x6d, 0x7f, 0x1},    /*RAW10 mode for TI913,TI933*/
	{0x7c, 0xc0, 0x1},
    /*{0x5b, 0xb0, 0x1},    //this field is normally loaded automatically from remote Serializer*/
    {0x5c, SER_2_I2C_ALIAS, 0x1},
    {0x5d, 0x20, 0x1},   /*sensor physical IIC address*/
    {0x65, SENSOR_2_I2C_ALIAS, 0x1},
    {0x70, 0x9e, 0x1},
	
	/*RX3 VC=3*/
    {0x4c, 0x38, 0x1},
	{0x58, 0x58, 0x1},
	{0x6d, 0x7f, 0x1},    /*RAW10 mode for TI913,TI933*/
	{0x7c, 0xc0, 0x1},
    /*{0x5b, 0xb0, 0x1},    //this field is normally loaded automatically from remote Serializer*/
    {0x5c, SER_3_I2C_ALIAS, 0x1},
    {0x5d, 0x20, 0x1},    /*sensor physical IIC address*/
    {0x65, SENSOR_3_I2C_ALIAS},
    {0x70, 0xde, 0x1},

    {0x0c, 0x0f, 0x1},  /*RX_PORT_CTL:Enable All ports*/
	{0x32, 0x1, 0x1},   /*CSI0 select */
    {0x33, 0x2, 0x1},   /* CSI_EN & CSI0 4L,Enable Continuous clock mode and CSI output*/
    {0x20, 0x0, 0x1},   /*forwarding of all RX to CSI0*/
    {0xFFFF, 0x00, 0x0} /*End of script */
};

#if 1	// MD modify, workaround & bypass
#define OTO206_SER_CFG_SIZE    (1U)
I2cParams ub9xxSerCfg_OTO206[OTO206_SER_CFG_SIZE] = {
    {0xFFFF, 0x00, 0x0} /*End of script */
};
#else   // original config, but it can't wirte.
#define OTO206_SER_CFG_SIZE    (5U)
I2cParams ub9xxSerCfg_OTO206[OTO206_SER_CFG_SIZE] = {
    {0x0E, 0xF0, 0xF0},
    {0x0D, 0xF0, 0x60},
    {0x0D, 0xB0, 0x60},
    {0x0D, 0xB4, 0x60},
    {0xFFFF, 0x00, 0x0} /*End of script */
};
#endif

I2cParams ub9xxOTO206DesCSI2Enable[10u] = {
    {0x33, 0x03, 0x1},
    {0xFFFF, 0x00, 0x0} //End of script
};

I2cParams ub9xxOTO206DesCSI2Disable[2u] = {
    {0x33, 0x02, 0x10},
    {0xFFFF, 0x00, 0x0} /*End of script */
};

#endif /* _UB96X_OTO206_SERDES_H_ */

