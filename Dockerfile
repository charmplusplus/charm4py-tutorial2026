# Charm4py tutorial image
#
# Clones Charm4py (and the bundled Charm++ runtime, MPI layer) from upstream
# and builds it, giving tutorial attendees a ready-to-run environment on their
# laptop.
#
# Build:
#   docker build -t charm4py-tutorial .
#   (override the repo/ref with --build-arg CHARM4PY_REPO=... CHARM4PY_REF=...)
#
# Run an example (4 PEs on one node, via MPI):
#   docker run --rm -it charm4py-tutorial \
#       mpirun -n 4 python3 /home/tutorial/examples/hello/array_hello.py
#
# Open an interactive shell with the examples available:
#   docker run --rm -it charm4py-tutorial bash

FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Build-time dependencies for Charm++ and the Cython extensions, plus MPI
# (MPICH) which Charm++ will build against, and a few quality-of-life tools.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gfortran \
        autoconf \
        automake \
        libtool \
        make \
        cmake \
        git \
        openssh-client \
        ca-certificates \
        procps \
        nano \
        vim \
        emacs-nox \
        mpich \
        libmpich-dev \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt

# Clone Charm4py and the Charm++ runtime from upstream. Charm4py's setup.py
# looks for the Charm++ sources at ./charm_src/charm relative to the project
# root, so we drop the clone there.
ARG CHARM4PY_REPO=https://github.com/charmplusplus/charm4py.git
ARG CHARM4PY_REF=main
ARG CHARM_REPO=https://github.com/charmplusplus/charm.git
ARG CHARM_REF=main
RUN git clone --branch "${CHARM4PY_REF}" "${CHARM4PY_REPO}" /opt/charm4py && \
    git clone --branch "${CHARM_REF}" "${CHARM_REPO}" /opt/charm4py/charm_src/charm

WORKDIR /opt/charm4py

# Install Python build-time dependencies.
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# `git describe` inside setup.py may not produce a clean version on a shallow or
# tag-less checkout. Supply the version explicitly via a build arg and write
# charm4py/_version.py before building.
ARG CHARM4PY_VERSION=1.1
RUN echo "version='${CHARM4PY_VERSION}'" > charm4py/_version.py

# Build Charm++ (MPI layer) + Charm4py. CHARM_BUILD_PROCESSES bounds parallelism
# so the build works on low-RAM laptops; override with `--build-arg` if desired.
ARG CHARM_BUILD_PROCESSES=2
ENV CHARM_BUILD_PROCESSES=${CHARM_BUILD_PROCESSES}
RUN python setup.py install --mpi

# ---- Second build: Charm4py with Charm++ tracing enabled (Projections) ----
# Installed into its own venv so the default install above stays lean.
# Attendees invoke it as `python3-prj` instead of `python3`; add
# `+tracemode projections` on the command line to write trace logs.
RUN git clone --branch "${CHARM4PY_REF}" "${CHARM4PY_REPO}" /opt/charm4py-prj && \
    git clone --branch "${CHARM_REF}" "${CHARM_REPO}" /opt/charm4py-prj/charm_src/charm && \
    echo "version='${CHARM4PY_VERSION}'" > /opt/charm4py-prj/charm4py/_version.py

RUN python3 -m venv /opt/venv-prj && \
    /opt/venv-prj/bin/pip install --upgrade pip setuptools wheel && \
    /opt/venv-prj/bin/pip install -r /opt/charm4py-prj/requirements.txt

WORKDIR /opt/charm4py-prj
RUN /opt/venv-prj/bin/python setup.py install --mpi --enable-tracing && \
    rm -rf /opt/charm4py-prj

# Convenience launcher: `python3-prj` runs the projections-enabled interpreter.
# Must be a shell wrapper, not a symlink — a symlink resolves to the system
# python3 binary, which makes Python lose the venv context and fall back to the
# default (non-tracing) charm4py install.
RUN printf '#!/bin/sh\nexec /opt/venv-prj/bin/python "$@"\n' > /usr/local/bin/python3-prj && \
    chmod +x /usr/local/bin/python3-prj

# Create an unprivileged user for the tutorial session.
RUN useradd --create-home --shell /bin/bash tutorial && \
    cp -r /opt/charm4py/examples /home/tutorial/examples

# Copy the tutorial materials (exercises, slides, README) from the build
# context into the attendee's home directory.
COPY --chown=tutorial:tutorial exercises /home/tutorial/exercises
COPY --chown=tutorial:tutorial slides /home/tutorial/slides
COPY --chown=tutorial:tutorial README.md /home/tutorial/README.md

RUN chown -R tutorial:tutorial /home/tutorial

USER tutorial
WORKDIR /home/tutorial

CMD ["bash"]
