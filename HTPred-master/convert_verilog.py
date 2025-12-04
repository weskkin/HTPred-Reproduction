# convert_verilog.py
# Usage: adjust the input_file / cell_dir / top_module variables below and run:
#    python convert_verilog.py

import time
import os
import sys

# import the Creator wrapper from HTPredBenchCreator
# the repo sometimes exposes Creator as HTPredBenchCreator.Creator
# so both import styles may work. Adjust if your repo exposes differently.
try:
    # preferred
    from HTPredBenchCreator import Creator
except Exception:
    import HTPredBenchCreator as HBC
    Creator = getattr(HBC, "Creator")

# -------- CONFIG -----
# Change these paths to match your environment
cell_dir    = r'tsmc_cells/'   # mapping / cells folder (if needed)
input_file  = r'AES_T200_TjIn.v'  # Verilog to convert
top_module  = 'top'   # set to the top module name (or None to let Creator decide)
out_path    = r'AES_T200_TjOu.bench'  # where to save bench output
# ---------------------

def convert_one(verilog_path, cell_dir, top_module=None, out_path=None):
    start = time.time()
    print(f"[INFO] Converting: {verilog_path}  (top_module={top_module})")
    try:
        c = Creator(verilog_path, cell_dir, top_module)
        bench_text = c.convert()

        # default output filename if not provided
        if out_path is None:
            base = os.path.splitext(os.path.basename(verilog_path))[0]
            out_path = os.path.join(os.path.dirname(verilog_path), base + ".bench")

        with open(out_path, "w", newline="\n") as fh:
            fh.write(bench_text)

        elapsed_ms = int((time.time() - start) * 1000)
        print(f"[OK] Saved bench to: {out_path}  (time: {elapsed_ms} ms)")
        return True, out_path

    except Exception as e:
        elapsed_ms = int((time.time() - start) * 1000)
        print(f"[ERROR] conversion failed for {verilog_path} after {elapsed_ms} ms. Exception:\n{e}")
        return False, str(e)

if __name__ == "__main__":
    # Basic sanity checks
    if not os.path.isfile(input_file):
        print(f"[ERROR] input_file not found: {input_file}")
        sys.exit(1)

    if not os.path.isdir(cell_dir):
        print(f"[WARN] cell_dir not found: {cell_dir} (converter may still work without it)")

    ok, info = convert_one(input_file, cell_dir, top_module=top_module, out_path=out_path)

    # --- Optional: batch convert a directory of .v files (uncomment to use) ----
    # srcdir = r'D:/dsci/Integration/verilog_samples/'
    # if os.path.isdir(srcdir):
    #     vfiles = [f for f in os.listdir(srcdir) if f.endswith('.v')]
    #     for vf in sorted(vfiles):
    #         full = os.path.join(srcdir, vf)
    #         convert_one(full, cell_dir, top_module=None,
    #                     out_path=os.path.join(srcdir, os.path.splitext(vf)[0] + '.bench'))

    # end