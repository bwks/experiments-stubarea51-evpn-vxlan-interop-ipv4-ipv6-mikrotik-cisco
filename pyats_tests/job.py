"""pyATS job file — runs all EVPN/VXLAN interop test sections.

Usage:
    # Run all tests (including convergence)
    pyats run job pyats_tests/job.py

    # Skip convergence/resilience tests (section 9)
    pyats run job pyats_tests/job.py --skip-convergence

    # Run from project root with the venv
    PATH="$PWD/.venv/bin:$PATH" .venv/bin/pyats run job pyats_tests/job.py
"""

import os
import sys
import logging
from pyats.easypy import run

# Add pyats_tests to path so libs can be imported
sys.path.insert(0, os.path.dirname(__file__))

logger = logging.getLogger(__name__)

TEST_SCRIPTS = [
    "test_01_physical.py",
    "test_02_addressing.py",
    "test_03_isis.py",
    "test_04_bgp.py",
    "test_05_evpn.py",
    "test_06_vxlan.py",
    "test_07_overlay.py",
    "test_08_mac.py",
    # Section 9 added conditionally below
    "test_10_interop.py",
]

CONVERGENCE_SCRIPT = "test_09_convergence.py"


def main(runtime):
    skip_convergence = runtime.args.skip_convergence if hasattr(runtime.args, "skip_convergence") else False

    test_dir = os.path.dirname(__file__)

    scripts = list(TEST_SCRIPTS)
    if not skip_convergence:
        scripts.append(CONVERGENCE_SCRIPT)
    else:
        logger.info("Skipping Section 9 (convergence tests) per --skip-convergence flag")

    for script in scripts:
        run(
            testscript=os.path.join(test_dir, script),
            runtime=runtime,
        )
