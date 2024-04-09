ifeq ($(TARGET_CPU),$(filter $(TARGET_CPU), x86_64 A72 A53))

include $(PRELUDE)

TARGET      := vx_app_conformance_video_io
TARGETTYPE  := exe
CSOURCES    := $(call all-c-files)

ifeq ($(TARGET_CPU),$(filter $(TARGET_CPU), A72 A53))
include $(VISION_APPS_PATH)/apps/concerto_mpu_inc.mak
endif

ifeq ($(TARGET_CPU),x86_64)
include $(VISION_APPS_PATH)/apps/concerto_x86_64_inc.mak
endif

#IDIRS += ${TIOVX_PATH}
IDIRS += ${VIDEO_IO_PATH}
IDIRS += ${TIOVX_PATH}/conformance_tests

STATIC_LIBS += $(IMAGING_LIBS)
STATIC_LIBS += $(TEST_LIBS)

CFLAGS      += -DBUILD_CT_TIOVX_VIDEO_IO
CFLAGS      += -DBUILD_CT_TIOVX_VIDEO_IO_CAPTURE_TESTS
CFLAGS      += -DBUILD_CT_TIOVX_VIDEO_IO_DISPLAY_TESTS

include $(FINALE)

endif

