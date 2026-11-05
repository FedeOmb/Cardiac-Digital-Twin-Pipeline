FROM kitware/trame:uv-glvnd

ENV TRAME_PYTHON=3.12
# paraview installation path
ENV TRAME_PARAVIEW=/opt/paraview
ENV PATH="/opt/paraview/bin:${PATH}"
# trame config variables
ENV TRAME_CLIENT_TYPE=vue3
ENV VTK_DEFAULT_OPENGL_WINDOW=vtkEGLRenderWindow
# mesh default data path
ENV MESH_ROOT=/data/meshes
# paraview 6.1.0
ARG PV_URL="https://www.paraview.org/files/v6.1/ParaView-6.1.0-MPI-Linux-Python3.12-x86_64.tar.gz"

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    libpciaccess-dev \
    libxcursor-dev \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# download and install paraview
RUN set -eux; \
    mkdir -p "${TRAME_PARAVIEW}"; \
    wget -qO /tmp/paraview.tar.gz "${PV_URL}"; \
    tar -xzf /tmp/paraview.tar.gz --strip-components=1 -C "${TRAME_PARAVIEW}"; \
    rm -f /tmp/paraview.tar.gz; \
    test -x "${TRAME_PARAVIEW}/bin/pvpython"

# setup application and data directories
RUN install -d -o trame-user -g trame-user \
    /deploy \
    /data/meshes

# copy app and config files
COPY --chown=trame-user:trame-user . /deploy

# build trame and verify
RUN set -eux; \
    test -f /deploy/setup/apps.yml; \
    test -f /deploy/setup/requirements.txt; \
    /opt/trame/entrypoint.sh build; \
    test -s /deploy/server/launcher.json; \
    python3 -m json.tool /deploy/server/launcher.json > /dev/null