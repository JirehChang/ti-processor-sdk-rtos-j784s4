
ifeq ($(TARGET_CPU), $(filter $(TARGET_CPU), X86 x86_64 A15 M4 A72 A53 R5F))

include $(PRELUDE)
TARGET      := vx_kernels_stereo_tests
TARGETTYPE  := library
CSOURCES    := $(call all-c-files)
IDIRS       += $(HOST_ROOT)/conformance_tests
IDIRS       += $(HOST_ROOT)/source/include
IDIRS       += $(VISION_APP_PATH)/kernels/stereo/include
IDIRS       += $(VISION_APP_PATH)
CFLAGS      += -DHAVE_VERSION_INC

ifeq ($(HOST_COMPILER),TIARMCGT)
CFLAGS += --display_error_number
CFLAGS += --diag_suppress=179
CFLAGS += --diag_suppress=112
CFLAGS += --diag_suppress=552
endif

ifeq ($(HOST_COMPILER),$(filter $(HOST_COMPILER),GCC GCC_WINDOWS GCC_LINUX GCC_SYSBIOS_ARM GCC_LINUX_ARM))
CFLAGS += -Wno-unused-function
CFLAGS += -Wno-unused-variable
CFLAGS += -Wno-format-security
endif

ifeq ($(TARGET_CPU),x86_64)
CFLAGS      += -DTARGET_X86_64
endif

include $(FINALE)
endif

