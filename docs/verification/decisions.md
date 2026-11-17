# Decision register — proposed vs verified

Updated 2026-11-17 JST. This is a summary of prior project design documents, **not an engineering release approval**.

| ID | Subject | Current state | Rationale / evidence | Reopen condition |
|---|---|---|---|---|
| D-001 | Main MCU: Pico 2 | **PROPOSED baseline** | `docs/reva-integrated-net-spec.md` | Unacceptable size, current, pin count or startup behavior |
| D-002 | Separate TPS63031 3V3 supply | **NOT in Rev.A baseline** | Pico 3V3(OUT) may supply OLED + RTC; `docs/ctrl-power-domains.md` | External load/standby/noise tests fail |
| D-003 | MAX668 single boost 5 V → 205 V | **REJECTED** | Required ideal D≈97.56%, device max duty lower; `docs/hv-architecture-decision.md` | Fundamentally different topology |
| D-004 | HV solution: 5V flyback | **PROPOSED, unproven** | Candidate topology, but no certified transformer efficiency/power match; `docs/hv-transformer-screen.md` | Demonstrated alternative better on specs, cost, thermals |
| D-005 | HV max output 16 mA continuous | **TARGET, NOT VERIFIED** | 205V×16mA=3.28W, high loss and current requirements; `docs/pwr-reva-power-thermal-review.md` | Lamp-current measurements or power/heat evidence |
| D-006 | “200–205V” interpretation | **UNDECIDED** | Nominal-target vs guaranteed-window conflict; `docs/hv-voltage-window.md` | User decision + full tolerance/OVP analysis |
| D-007 | Independent HV OVP, fault stop, bleeder | **MANDATORY SAFETY REQUIREMENTS, NOT DESIGNED** | `docs/reva-integrated-prototype-review.md` | Only marked complete after schematic, faults, tolerances and safe bench test |
| D-008 | Charging /CE tied GND | **PROPOSED** | Automatic charging when valid USB/NTC; `docs/pwr-reva-v3-review.md` | Cell requirements or charging thermal tests disallow |
| D-009 | ADC: MOS-switched 100k/47k | **PROPOSED** | Lower cost than TMUX1101 approach; reverse feed needs validation; `docs/pwr-reva-v3-review.md` | Leak/injection or thermal results fail |
| D-010 | USB supply from dedicated 5V ≥500mA charger | **PROPOSED operating constraint** | USB source advertisement/host behavior not automatically handled; `docs/pwr-reva-v3-review.md` | Need broader host compatibility |
| D-011 | HV outputs rely on HV5524 BL=LOW/POL=HIGH for display OFF | **LOGIC-STATE ONLY; NOT SAFETY ISOLATION** | `docs/ctrl-driver-rtc-schematic.md`; HV logic supply must be valid | HV stop/discharge is separately verified |

## Editing rules

A new result may supersede a prior decision, but it must include original ID, old state, new state, date, supporting calculation/tests, link to dated report and a concise explicit reason. Never silently erase rejected alternatives. The user must approve product requirements changes (e.g. reducing maximum neon current or relaxing nominal target); the engineer/supervisor must verify high-voltage bench safety.

## 2026-11-17 — WORK-INT-001 integration supplement

| ID | Previous state | New state | Adoption conditions / evidence | Reopen trigger |
|---|---|---|---|---|
| D-012 | No mode-specific integrated adoption gate | **PROPOSED / PENDING REVIEW:** define HV–PWR–CTRL power contract before final HV selection | [Work integration](2026-11-17-work-integration-001.md); lamp-current evidence, qualified topology, supply/startup/thermal bounds, independent OVP and power-loss/discharge behavior; explicit approval for requirements changes | Chat C reviewed package or new power/current/protection evidence |

D-003 remains limited to ordinary non-coupled boost. D-004 is unproven; D-005 remains the unmodified 16mA target; D-006 remains undecided. Latest Chat A report has no located Chat C review package at examined SHA. No final topology, component rating or firmware threshold is adopted.
