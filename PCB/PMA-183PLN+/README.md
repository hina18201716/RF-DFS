# Changelog

## Revision B - 7/5/2023

### Added

- More PTH vias around and directly under RF components.
- Another layer of via picketing around transmission line.
- Silkscreen revision indicator.

### Changed

- Removed Hammond 1554B compatibility due to difficulties in assembly and weatherproofing SMA connectors.

### Fixed

- C9 footprint now correctly matches schematic (0402 --> 1206).
- Moved SMA footprints closer to board edge to reduce filing prior to assembly.

## Revision A - 6/12/2023

### First revision 🎉🎉🎉

- Board is built to 4-layer OSHPark specifications
- Testing shows amplifier oscillates strongly at ~18.5 GHz. This occurs both when the amplifier is biased through the regulator or directly from a DC power supply. SMA landings were also copied from test coupons so that can likely be ruled out. This is possibly due to the lack of PTH vias directly under the IC or the tuning/spacing of picketing around the transmission line.
