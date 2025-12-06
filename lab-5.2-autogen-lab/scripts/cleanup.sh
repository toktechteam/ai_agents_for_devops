#!/bin/bash
docker rm -f autogen-free 2>/dev/null || true
rm -f output.log
echo "Cleanup complete."
