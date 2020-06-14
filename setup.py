# Copyright (c) 2020, Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

from setuptools import find_packages, setup

setup(
    name="license-text-normalizer",
    author="Jesse Porter",
    author_email="quic_jporter@quicinc.com",
    url="https://github.com/quic/license-text-normalizer",
    package_dir={"": "src"},
    packages=find_packages("src"),
    setup_requires="setuptools_scm",
    use_scm_version=True,
)
