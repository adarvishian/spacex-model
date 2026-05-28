"""OpEx layer — R&D by module + SG&A by function per Architecture §12 / PRD §5.2."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import (
    assumption_scalar,
    assumption_year_vector,
    bounded_cagr_pct_vector,
)
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class OpExRevenueBases:
    """Revenue bases extracted from module Allocator OUT rows."""

    starlink_total_revenue: YearVector
    starlink_subscription_revenue: YearVector
    customer_launch_total_revenue: YearVector
    customer_launch_external_revenue: YearVector
    odc_revenue: YearVector
    ai_stack_revenue: YearVector
    group_revenue_net_of_elims: YearVector


@dataclass(frozen=True, slots=True)
class OpExInputs:
    """Inputs for OpEx — Assumptions plus module Allocator OUT dict."""

    assumptions: Assumptions
    module_outputs: dict[str, AllocatorOut]
    revenue_bases: OpExRevenueBases | None = None
    customer_launch_external_revenue: YearVector | None = None
    starlink_subscription_revenue: YearVector | None = None


@dataclass(frozen=True, slots=True)
class S1SegmentMemo:
    """S-1 segment reconciliation memo — MDA §4.1 / §4.2 (P1-6)."""

    rd_space: YearVector
    rd_connectivity: YearVector
    rd_ai: YearVector
    sga_space: YearVector
    sga_connectivity: YearVector
    sga_ai: YearVector


@dataclass(frozen=True, slots=True)
class OpExResult:
    """OpEx tab outputs."""

    starlink_rd: YearVector
    customer_launch_rd: YearVector
    starship_precommercial_rd: YearVector
    odc_rd: YearVector
    ai_stack_rd: YearVector
    moon_mars_rd: YearVector
    total_rd: YearVector
    sales_marketing: YearVector
    general_administrative: YearVector
    customer_service: YearVector
    other_corporate_operating: YearVector
    total_sga: YearVector
    total_opex: YearVector
    s1_segment_memo: S1SegmentMemo | None = None


def _module_out(outputs: dict[str, AllocatorOut], key: str) -> AllocatorOut:
    if key in outputs:
        return outputs[key]
    return AllocatorOut.zeros()


def build_revenue_bases(
    module_outputs: dict[str, AllocatorOut],
    *,
    customer_launch_external_revenue: YearVector | None = None,
    starlink_subscription_revenue: YearVector | None = None,
    eliminations: YearVector | None = None,
) -> OpExRevenueBases:
    """Derive OpEx revenue bases from module Allocator OUT dict.

    Excel cell:        OpEx!— (revenue base wiring)
    Excel label:       "OpEx revenue bases"
    Architecture ref:  §12 OpEx tab
    Principle:         3 (canonical cross-tab labels)

    """
    starlink = _module_out(module_outputs, "starlink").total_revenue
    customer_launch = _module_out(module_outputs, "customer_launch").total_revenue
    odc = _module_out(module_outputs, "odc").total_revenue
    ai_stack = _module_out(module_outputs, "ai_stack").total_revenue
    lunar_mars = _module_out(module_outputs, "lunar_mars").total_revenue

    cl_external = customer_launch_external_revenue or customer_launch
    subscription = starlink_subscription_revenue or starlink

    gross = (
        starlink.values
        + customer_launch.values
        + odc.values
        + ai_stack.values
        + lunar_mars.values
    )
    elim = eliminations.values if eliminations is not None else np.zeros(HORIZON_YEARS)
    group_net = YearVector(gross - elim)

    return OpExRevenueBases(
        starlink_total_revenue=starlink,
        starlink_subscription_revenue=subscription,
        customer_launch_total_revenue=customer_launch,
        customer_launch_external_revenue=cl_external,
        odc_revenue=odc,
        ai_stack_revenue=ai_stack,
        group_revenue_net_of_elims=group_net,
    )


def switching_rd(
    dollar_profile: YearVector,
    pct_rate: YearVector,
    revenue: YearVector,
) -> YearVector:
    """Pre-revenue R&D switch: MAX($-profile, % × revenue) per Architecture §12.1.

    Excel cell:        OpEx!D26 / D32
    Excel label:       "ODC R&D ($mm) — MAX($-profile, % × rev)"
    Architecture ref:  §12.1 (pre-revenue R&D switch)
    Principle:         12 (anchor-and-offset year rows)

    """
    pct_amount = pct_rate.values * revenue.values
    return YearVector(np.maximum(dollar_profile.values, pct_amount))


def _pct_rd(
    assumptions: Assumptions,
    *,
    start_label: str,
    end_label: str,
    cagr_label: str,
    revenue: YearVector,
    start_default: float,
    end_default: float,
    cagr_default: float,
) -> YearVector:
    start = assumption_scalar(assumptions, start_label, default=start_default)
    end = assumption_scalar(assumptions, end_label, default=end_default)
    cagr = assumption_scalar(assumptions, cagr_label, default=cagr_default)
    pct = bounded_cagr_pct_vector(start, end, cagr)
    return YearVector(pct * revenue.values)


def compute_starlink_rd(inputs: OpExInputs, bases: OpExRevenueBases) -> YearVector:
    """Starlink R&D = bounded-CAGR % × (Starlink + Starshield) revenue.

    Excel cell:        OpEx!D13
    Excel label:       "Starlink R&D ($mm)"
    Architecture ref:  §12.1 R&D by module
    Principle:         12 (anchor-and-offset bounded CAGR)

    """
    return _pct_rd(
        inputs.assumptions,
        start_label=cl.STARLINK_R_D_START_OF_STARLINK_STARSHIELD_REV,
        end_label=cl.STARLINK_R_D_END_STATE_FLOOR,
        cagr_label=cl.STARLINK_R_D_CAGR_TAPER,
        revenue=bases.starlink_total_revenue,
        start_default=0.08,
        end_default=0.03,
        cagr_default=-0.10,
    )


def compute_customer_launch_rd(inputs: OpExInputs, bases: OpExRevenueBases) -> YearVector:
    """Customer Launch R&D = bounded-CAGR % × external revenue.

    Excel cell:        OpEx!D19
    Excel label:       "Customer Launch R&D ($mm)"
    Architecture ref:  §12.1 R&D by module
    Principle:         12 (anchor-and-offset bounded CAGR)

    """
    return _pct_rd(
        inputs.assumptions,
        start_label=cl.CUSTOMER_LAUNCH_R_D_START_OF_EXTERNAL_REV,
        end_label=cl.CUSTOMER_LAUNCH_R_D_END_STATE_FLOOR,
        cagr_label=cl.CUSTOMER_LAUNCH_R_D_CAGR_TAPER,
        revenue=bases.customer_launch_external_revenue,
        start_default=0.25,
        end_default=0.04,
        cagr_default=-0.20,
    )


def compute_odc_rd(inputs: OpExInputs, bases: OpExRevenueBases) -> YearVector:
    """ODC R&D = MAX($-profile, bounded-CAGR % × ODC revenue).

    Excel cell:        OpEx!D26
    Excel label:       "ODC R&D ($mm) — MAX($-profile, % × rev)"
    Architecture ref:  §12.1 (pre-revenue R&D switch)
    Principle:         12 (anchor-and-offset bounded CAGR)

    """
    a = inputs.assumptions
    start = assumption_scalar(a, cl.ODC_R_D_START_OF_ODC_REV, default=0.30)
    end = assumption_scalar(a, cl.ODC_R_D_END_STATE_FLOOR, default=0.08)
    cagr = assumption_scalar(a, cl.ODC_R_D_CAGR_TAPER, default=-0.15)
    pct = YearVector(bounded_cagr_pct_vector(start, end, cagr))
    profile = assumption_year_vector(a, cl.ODC_R_D_PROFILE_MM_YR_YEAR_ROW, default=0.0)
    if profile.at(FIRST_YEAR) == 0.0:
        profile = assumption_year_vector(a, cl.ODC_R_D_PROFILE_MM_PRE_REVENUE_FLOOR, default=200.0)
    return switching_rd(profile, pct, bases.odc_revenue)


def compute_ai_stack_rd(inputs: OpExInputs, bases: OpExRevenueBases) -> YearVector:
    """AI Stack R&D = MAX($-profile, bounded-CAGR % × AI Stack revenue).

    Excel cell:        OpEx!D32
    Excel label:       "AI Stack R&D ($mm) — MAX($-profile, % × rev)"
    Architecture ref:  §12.1 (pre-revenue R&D switch)
    Principle:         12 (anchor-and-offset bounded CAGR)

    """
    a = inputs.assumptions
    start = assumption_scalar(a, cl.AI_STACK_R_D_START_OF_AI_STACK_REV, default=0.15)
    end = assumption_scalar(a, cl.AI_STACK_R_D_END_STATE_FLOOR, default=0.05)
    cagr = assumption_scalar(a, cl.AI_STACK_R_D_CAGR_TAPER, default=-0.10)
    pct = YearVector(bounded_cagr_pct_vector(start, end, cagr))
    profile = assumption_year_vector(a, cl.AI_STACK_R_D_PROFILE_MM_YR_YEAR_ROW, default=0.0)
    if profile.at(FIRST_YEAR) == 0.0:
        profile = assumption_year_vector(a, cl.AI_STACK_R_D_PROFILE_MM_PRE_REVENUE_FLOOR, default=50.0)
    return switching_rd(profile, pct, bases.ai_stack_revenue)


def compute_starship_precommercial_rd(inputs: OpExInputs) -> YearVector:
    """Starship pre-commercialization R&D $-profile — MDA §9 / §11.6 (P1-4).

    Excel cell:        OpEx!— (S-1 segment memo)
    Excel label:       "Starship pre-commercialization R&D ($mm/yr) — memo"
    Architecture ref:  §12.1 S-1 segment reconciliation
    Principle:         8 (memo-only; port capitalizes Starship via vehicle build)

    """
    return assumption_year_vector(
        inputs.assumptions,
        cl.STARSHIP_PRECOMMERCIAL_RD_MM_YEAR_ROW,
        default=0.0,
    )


def compute_moon_mars_rd(inputs: OpExInputs) -> YearVector:
    """Moon/Mars R&D = Assumptions $-profile year-row (pre-revenue).

    Excel cell:        OpEx!D35
    Excel label:       "Mars/Moon R&D ($mm/yr) — year-row"
    Architecture ref:  §12.1 R&D — Moon/Mars
    Principle:         12 (anchor-and-offset year rows)

    """
    profile = assumption_year_vector(
        inputs.assumptions,
        cl.R_D_MOON_MARS_MM_YR_YEAR_ROW,
        default=700.0,
    )
    if profile.at(FIRST_YEAR) == 0.0:
        profile = assumption_year_vector(
            inputs.assumptions,
            cl.MARS_MOON_R_D_MM_YR_YEAR_ROW,
            default=700.0,
        )
    return profile


def _allocate_sga_by_revenue(
    total_sga: YearVector,
    space_rev: YearVector,
    conn_rev: YearVector,
    ai_rev: YearVector,
) -> tuple[YearVector, YearVector, YearVector]:
    """Allocate group SG&A to S-1 segments by revenue share."""
    denom = space_rev.values + conn_rev.values + ai_rev.values
    safe = np.where(denom > 0, denom, 1.0)
    space_share = np.where(denom > 0, space_rev.values / safe, 0.0)
    conn_share = np.where(denom > 0, conn_rev.values / safe, 0.0)
    ai_share = np.where(denom > 0, ai_rev.values / safe, 0.0)
    return (
        YearVector(total_sga.values * space_share),
        YearVector(total_sga.values * conn_share),
        YearVector(total_sga.values * ai_share),
    )


def compute_s1_segment_memo(
    opex_rd: OpExResult,
    bases: OpExRevenueBases,
    module_outputs: dict[str, AllocatorOut],
) -> S1SegmentMemo:
    """Roll port module R&D/SG&A into S-1 Space / Connectivity / AI segments (P1-6).

    Excel cell:        OpEx!— (S-1 reconciliation memo block)
    Excel label:       "S-1 segment R&D / SG&A rollup"
    Architecture ref:  §12.1 + MDA §4.1 / §4.2
    Principle:         3 (reconciliation memo; not a second P&L)

    """
    cl_rev = bases.customer_launch_external_revenue
    conn_rev = _module_out(module_outputs, "starlink").total_revenue
    ai_rev = YearVector(
        bases.odc_revenue.values + bases.ai_stack_revenue.values
    )
    rd_space = YearVector(
        opex_rd.customer_launch_rd.values
        + opex_rd.moon_mars_rd.values
        + opex_rd.starship_precommercial_rd.values
    )
    rd_connectivity = opex_rd.starlink_rd
    rd_ai = YearVector(opex_rd.odc_rd.values + opex_rd.ai_stack_rd.values)
    sga_space, sga_conn, sga_ai = _allocate_sga_by_revenue(
        opex_rd.total_sga, cl_rev, conn_rev, ai_rev
    )
    return S1SegmentMemo(
        rd_space=rd_space,
        rd_connectivity=rd_connectivity,
        rd_ai=rd_ai,
        sga_space=sga_space,
        sga_connectivity=sga_conn,
        sga_ai=sga_ai,
    )


def compute_sales_marketing(inputs: OpExInputs, bases: OpExRevenueBases) -> YearVector:
    """Sales & Marketing = bounded-CAGR % × expanded revenue base.

    Excel cell:        OpEx!D44
    Excel label:       "S&M ($mm)"
    Architecture ref:  §12.2 SG&A by function
    Principle:         12 (anchor-and-offset bounded CAGR)

    """
    a = inputs.assumptions
    start = assumption_scalar(
        a,
        cl.SALES_MARKETING_START_OF_STARLINK_STARSHIELD_CUSTOMER_LAUNCH_EXT_REV,
        default=0.04,
    )
    end = assumption_scalar(a, cl.SALES_MARKETING_END_STATE_FLOOR, default=0.02)
    cagr = assumption_scalar(a, cl.SALES_MARKETING_CAGR_TAPER, default=-0.08)
    pct = bounded_cagr_pct_vector(start, end, cagr)
    sm_base = YearVector(
        bases.starlink_total_revenue.values
        + bases.customer_launch_external_revenue.values
        + bases.ai_stack_revenue.values
    )
    return YearVector(pct * sm_base.values)


def compute_general_administrative(inputs: OpExInputs, bases: OpExRevenueBases) -> YearVector:
    """General & Administrative = bounded-CAGR % × group revenue net of eliminations.

    Excel cell:        OpEx!D47
    Excel label:       "G&A ($mm)"
    Architecture ref:  §12.2 SG&A by function
    Principle:         12 (anchor-and-offset bounded CAGR)

    """
    a = inputs.assumptions
    start = assumption_scalar(a, cl.GENERAL_ADMINISTRATIVE_START_OF_GROUP_REV, default=0.05)
    end = assumption_scalar(
        a,
        "General & Administrative — end-state % (ceiling)",
        default=0.06,
    )
    cagr = assumption_scalar(
        a,
        "General & Administrative — CAGR (taper)",
        default=0.01,
    )
    pct = bounded_cagr_pct_vector(start, end, cagr)
    return YearVector(pct * bases.group_revenue_net_of_elims.values)


def compute_customer_service(inputs: OpExInputs, bases: OpExRevenueBases) -> YearVector:
    """Customer Service = flat % × Starlink subscription revenue (BB + DTC).

    Excel cell:        OpEx!D48
    Excel label:       "Customer Service ($mm) — 2% × Starlink subscription rev"
    Architecture ref:  §12.2 SG&A by function
    Principle:         12 (flat rate on subscription base)

    """
    flat_pct = assumption_scalar(
        inputs.assumptions,
        "Customer Service — flat % of Starlink subscription rev",
        default=0.02,
    )
    return YearVector(flat_pct * bases.starlink_subscription_revenue.values)


def compute_other_corporate_operating(inputs: OpExInputs, bases: OpExRevenueBases) -> YearVector:
    """Other corporate operating = flat % × group revenue net of eliminations.

    Excel cell:        OpEx!D49
    Excel label:       "Other corporate operating ($mm) — 1% × group rev"
    Architecture ref:  §12.2 SG&A by function
    Principle:         12 (flat rate on group revenue)

    """
    flat_pct = assumption_scalar(
        inputs.assumptions,
        cl.OTHER_CORPORATE_OPERATING_FLAT_OF_GROUP_REV,
        default=0.01,
    )
    return YearVector(flat_pct * bases.group_revenue_net_of_elims.values)


def compute_opex(inputs: OpExInputs) -> OpExResult:
    """Total OpEx = Σ R&D + Σ SG&A per Architecture §12.

    Excel cell:        OpEx!D53
    Excel label:       "Total OpEx ($mm)"
    Architecture ref:  §12 OpEx tab
    Principle:         8 (corporate OpEx excluded from module tabs)

    """
    bases = inputs.revenue_bases
    if bases is None:
        bases = build_revenue_bases(
            inputs.module_outputs,
            customer_launch_external_revenue=inputs.customer_launch_external_revenue,
            starlink_subscription_revenue=inputs.starlink_subscription_revenue,
        )

    starlink_rd = compute_starlink_rd(inputs, bases)
    customer_launch_rd = compute_customer_launch_rd(inputs, bases)
    starship_precommercial_rd = compute_starship_precommercial_rd(inputs)
    odc_rd = compute_odc_rd(inputs, bases)
    ai_stack_rd = compute_ai_stack_rd(inputs, bases)
    moon_mars_rd = compute_moon_mars_rd(inputs)

    total_rd = YearVector(
        starlink_rd.values
        + customer_launch_rd.values
        + odc_rd.values
        + ai_stack_rd.values
        + moon_mars_rd.values
    )

    sm = compute_sales_marketing(inputs, bases)
    ga = compute_general_administrative(inputs, bases)
    cs = compute_customer_service(inputs, bases)
    other = compute_other_corporate_operating(inputs, bases)
    total_sga = YearVector(sm.values + ga.values + cs.values + other.values)

    total_opex = YearVector(total_rd.values + total_sga.values)

    partial = OpExResult(
        starlink_rd=starlink_rd,
        customer_launch_rd=customer_launch_rd,
        starship_precommercial_rd=starship_precommercial_rd,
        odc_rd=odc_rd,
        ai_stack_rd=ai_stack_rd,
        moon_mars_rd=moon_mars_rd,
        total_rd=total_rd,
        sales_marketing=sm,
        general_administrative=ga,
        customer_service=cs,
        other_corporate_operating=other,
        total_sga=total_sga,
        total_opex=total_opex,
    )
    segment_memo = compute_s1_segment_memo(partial, bases, inputs.module_outputs)

    return OpExResult(
        starlink_rd=starlink_rd,
        customer_launch_rd=customer_launch_rd,
        starship_precommercial_rd=starship_precommercial_rd,
        odc_rd=odc_rd,
        ai_stack_rd=ai_stack_rd,
        moon_mars_rd=moon_mars_rd,
        total_rd=total_rd,
        sales_marketing=sm,
        general_administrative=ga,
        customer_service=cs,
        other_corporate_operating=other,
        total_sga=total_sga,
        total_opex=total_opex,
        s1_segment_memo=segment_memo,
    )
