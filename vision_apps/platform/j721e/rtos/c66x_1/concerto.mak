ifeq ($(BUILD_APP_RTOS_LINUX),yes)
ifeq ($(BUILD_CPU_C6x_1),yes)
ifeq ($(TARGET_CPU),C66)

# OS_ID must be set before include $(PRELUDE)
OS_ID=linux

_MODULE=$(OS_ID)
include $(PRELUDE)

DEFS+=CPU_c6x_1

TARGET      := vx_app_rtos_linux_c6x_1
TARGETTYPE  := exe
CSOURCES    := $(call all-c-files)

include $($(_MODULE)_SDIR)/concerto_c6x_1_inc.mak

IDIRS+=$(VISION_APPS_PATH)/platform/$(SOC)/rtos/common_linux

STATIC_LIBS += app_rtos_linux

include $(FINALE)

endif
endif
endif

ifeq ($(BUILD_APP_RTOS_QNX),yes)
ifeq ($(BUILD_CPU_C6x_1),yes)
ifeq ($(TARGET_CPU),C66)

# OS_ID must be set before include $(PRELUDE)
OS_ID=qnx

_MODULE=$(OS_ID)
include $(PRELUDE)

DEFS+=CPU_c6x_1

TARGET      := vx_app_rtos_qnx_c6x_1
TARGETTYPE  := exe
CSOURCES    := $(call all-c-files)

include $($(_MODULE)_SDIR)/concerto_c6x_1_inc.mak

IDIRS+=$(VISION_APPS_PATH)/platform/$(SOC)/rtos/common_qnx

STATIC_LIBS += app_rtos_qnx

include $(FINALE)

endif
endif
endif
