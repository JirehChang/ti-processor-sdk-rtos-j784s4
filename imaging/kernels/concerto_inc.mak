# This file contains a list of extension kernel specific static libraries
# to be included in the PC executables.  It is put in this separate file
# to make it easier to add/extend kernels without needing to modify
# several concerto.mak files which depend on kernel libraries.

ifeq ($(TARGET_CPU),x86_64)

ifeq ($(BUILD_HWA_KERNELS),yes)
ifneq ($(SOC),am62a)

STATIC_LIBS += vx_kernels_hwa_tests vx_kernels_hwa vx_vxu

ifeq ($(BUILD_DMPAC_SDE), yes)
STATIC_LIBS += vx_target_kernels_dmpac_sde
STATIC_LIBS += sde_hw
endif

ifeq ($(BUILD_VPAC_LDC), yes)
STATIC_LIBS += vx_target_kernels_vpac_ldc
STATIC_LIBS += ldc
endif

ifeq ($(BUILD_DMPAC_DOF),yes)
    STATIC_LIBS += vx_target_kernels_dmpac_dof
    STATIC_LIBS += vx_kernels_hwa_tests
endif

ifeq ($(BUILD_VPAC_MSC),yes)
STATIC_LIBS += vx_target_kernels_vpac_msc
STATIC_LIBS += scalar
endif

ifeq ($(BUILD_VPAC_NF),yes)
STATIC_LIBS += vx_target_kernels_vpac_nf
STATIC_LIBS += bl_filter_lib
endif

ifeq ($(BUILD_VPAC_VISS),yes)
STATIC_LIBS += vx_target_kernels_vpac_viss
STATIC_LIBS += rawfe nsf4 flexcc h3a ee utils glbce
SYS_SHARED_LIBS += glbce
endif

ifeq ($(VPAC_VERSION), VPAC3)
    STATIC_LIBS += cac RawHistogram nsf4_wb flexcfa_vpac3
else ifeq ($(VPAC_VERSION), VPAC3L)
    STATIC_LIBS += cac RawHistogram nsf4_wb flexcfa_vpac3 pcid
else ifeq ($(VPAC_VERSION), VPAC1)
    STATIC_LIBS += flexcfa
endif

STATIC_LIBS += vx_target_kernels_j7_arm

endif #ifneq ($(SOC),am62a)
endif #ifeq ($(BUILD_HWA_KERNELS),yes)

LDIRS+=$(J7_C_MODELS_PATH)/lib/PC/x86_64/LINUX/release

LDIRS       += $(IMAGING_PATH)/lib/PC/$(TARGET_CPU)/$(TARGET_OS)/$(TARGET_BUILD)
STATIC_LIBS += ti_imaging_dcc

STATIC_LIBS += app_utils_iss

endif #ifeq ($(TARGET_CPU),x86_64)
