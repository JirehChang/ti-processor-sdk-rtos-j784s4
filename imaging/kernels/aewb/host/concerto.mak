ifeq ($(TARGET_CPU), $(filter $(TARGET_CPU), X86 x86_64 A72 A53 R5F))

include $(PRELUDE)
TARGET      := vx_kernels_imaging
TARGETTYPE  := library
CSOURCES    := $(call all-c-files)
IDIRS       += $(HOST_ROOT)/kernels/include

ifeq ($(SOC), am62a)
ifneq ($(TARGET_OS), QNX)
SKIPBUILD=1
endif
endif

include $(FINALE)

endif
