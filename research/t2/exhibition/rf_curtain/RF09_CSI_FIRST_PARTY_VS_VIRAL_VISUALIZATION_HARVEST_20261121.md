# RF09 — Wi-Fi 'camera' claim versus measured first-party CSI: method harvest

Date 2026-11-21. Web documentation and primary public repository source review; **no local RF device measurement** or authenticated source build.

## Source distinctions (links verified in web access)
1. Espressif official esp-csi repository: https://github.com/espressif/esp-csi
   - Documentation explicitly lists ESP32/ESP32-S2/C3/S3/C5/C6/C61 series CSI support and sender/receiver examples. Not all listed boards/versions are interchangeable: firmware/toolchain compatibility must be checked on the exact owned SoC.
2. Official get-started: https://github.com/espressif/esp-csi/blob/master/examples/get-started/README.md
   - Describes CSI data communicated between Espressif devices and graphical real-time subcarrier visualization. This is the *lowest credible physical milestone*: measured subcarrier trace, not a camera image.
3. Official csi_recv: https://github.com/espressif/esp-csi/blob/master/examples/get-started/csi_recv/main/app_main.c
   - Different target families use different CSI configuration structures and buffer handling; copying a generic configuration across board variants is not safe evidence of functionality. It may show MAC fields in the stock output; the school research export must prevent storing third-party device identifiers or collecting unrelated traffic.
4. WiFi DensePose community implementation: https://github.com/syntax-syndicate/wifi-densepose
   - The project's own README distinguishes ambitious rendered poses from limited camera-free empirical validation (one documented proxy-labelled PCK@20 figure approximately 2.5%). A beautiful 3D avatar is not evidence of reconstructing spatial scenes with camera precision.

## Scientific transfer to exhibition
- First milestone: **measured RF traces** that are accurately labelled as CSI, not signal strength RSSI.
- Next: compare fixed known-empty and labelled model movement in controlled owned lab paths with a holdout session.
- Next: independent stationary occupancy and moved-placement evaluation. Do not implicitly claim a pixel grid, tomography, person imaging or lane resolution.
- Comparison: cheap optical break-beam/marker occupancy control. If it outperforms CSI for the stated source-diagnosis task, preserve the negative finding.
- Separate model failure from environment: mounting, packet losses, sample sizes, band/channel, reflective surfaces, toy material, training leakage.

## 'Wow' exhibition verdict
The strongest claim is *camera-free, physically measured channel changes that help distinguish specific tabletop obstruction scenarios*, and displaying failure/uncertainty honestly. Rendering a fabricated traffic-image heatmap would undermine rather than improve scientific value.

## Next gate
Before purchase or firmware decisions, inventory school-owned compatible boards and supervisor permission. Freeze an independent label protocol and time×placement split before measurement. No public-road installations, controller connections, bystander monitoring or unrelated Wi-Fi interception. CIM dataset.zip remains HOLD.
