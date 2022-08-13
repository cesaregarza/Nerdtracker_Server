FROM python:3.10-slim

LABEL maintainer="Cesar E. Garza <cesar@cegarza.com>"

WORKDIR /opt/build

ENV OPENCV_VERSION="4.6.0"

# Install open-cv and tesseract
RUN apt-get -qq update \
    && apt-get -qq install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        tesseract-ocr \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libopenjp2-7-dev \
        libavformat-dev \
        libpq-dev \
    && wget -q https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip -O opencv.zip \
    && unzip -qq opencv.zip -d /opt \
    && rm -rf opencv.zip \
    && cmake \
        -D BUILD_TIFF=ON \
        -D BUILD_opencv_java=OFF \
        -D WITH_CUDA=OFF \
        -D WITH_OPENGL=ON \
        -D WITH_OPENCL=ON \
        -D WITH_IPP=ON \
        -D WITH_TBB=ON \
        -D WITH_EIGEN=ON \
        -D WITH_V4L=ON \
        -D BUILD_TESTS=OFF \
        -D BUILD_PERF_TESTS=OFF \
        -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=$(python3.10 -c "import sys; print(sys.prefix)") \
        -D PYTHON_EXECUTABLE=$(which python3.10) \
        -D PYTHON_INCLUDE_DIR=$(python3.10 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
        -D PYTHON_PACKAGES_PATH=$(python3.10 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
        /opt/opencv-${OPENCV_VERSION} \
    && make -j$(nproc) \
    && make install \
    && rm -rf /opt/build/* \
    && rm -rf /opt/opencv-${OPENCV_VERSION} \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq autoremove \
    && apt-get -qq clean

# Install pipenv and dependencies
RUN pip install pipenv \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcc

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install

CMD tail -f /dev/null