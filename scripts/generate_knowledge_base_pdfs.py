from __future__ import annotations

from pathlib import Path

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_BASE = ROOT / "knowledge_base"


def build_pdf(path: Path, title: str, sections: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        "BodyText",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )
    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        spaceBefore=10,
        spaceAfter=6,
    )

    story = [Paragraph(title, styles["Title"]), Spacer(1, 12)]
    for index, section in enumerate(sections):
        heading = str(section["heading"])
        paragraphs = list(section["paragraphs"])
        story.append(Paragraph(heading, heading_style))
        for paragraph in paragraphs:
            story.append(Paragraph(str(paragraph), body_style))
            story.append(Spacer(1, 4))
        if index < len(sections) - 1:
            story.append(PageBreak())

    doc.build(story)


def main() -> None:
    KNOWLEDGE_BASE.mkdir(parents=True, exist_ok=True)

    documents = [
        (
            "Water_Resources.pdf",
            "Water Resources: Planning, Hydrology, and Sustainability",
            [
                {
                    "heading": "Hydrological Cycle and Global Water Distribution",
                    "paragraphs": [
                        "Water resources encompass all natural supplies of water in liquid, solid, or vapor states. Freshwater accounts for only approximately 2.5 percent of the Earth's total water volume, with the remaining 97.5 percent residing in ocean saltwater. Of the total freshwater, over 68 percent is trapped in ice caps and glaciers, approximately 30 percent exists as groundwater, and less than 1 percent is readily accessible in rivers, lakes, reservoirs, and soil moisture.",
                        "The global hydrological cycle drives the continuous movement of water through evaporation, transpiration, condensation, precipitation, infiltration, and runoff. Human activities such as deforestation, urban development, land conversion, and climate variability significantly alter precipitation patterns, river streamflow regimes, and basin evaporation rates, impacting overall water availability.",
                    ],
                },
                {
                    "heading": "Integrated Water Resources Management (IWRM)",
                    "paragraphs": [
                        "Integrated Water Resources Management (IWRM) is an internationally accepted operational framework designed to coordinate the development, management, and allocation of land, water, and related ecological resources. The principal objective of IWRM is to maximize economic prosperity and social welfare without compromising the sustainability of vital ecosystems.",
                        "IWRM incorporates cross-sectoral decision-making across agricultural, industrial, domestic, and environmental water sectors. Key principles include basin-level river planning, economic valuation of water services, stakeholder participation, gender equality in governance, and transparent regulatory mechanisms to handle competing allocation demands during periods of peak scarcity.",
                    ],
                },
                {
                    "heading": "River Basin Hydrology and Reservoir Operations",
                    "paragraphs": [
                        "A river basin or watershed represents the fundamental geographic unit for hydrologic analysis and water management. Modern basin management utilizes remote sensing, satellite radar altimetry, GIS mapping, and rainfall-runoff hydraulic modeling to track streamflow, sediment transport, and river channel dynamics.",
                        "Multipurpose reservoirs provide storage capacity for flood mitigation, hydroelectric power generation, agricultural irrigation, and municipal drinking water supply. Reservoir rule curves dictate seasonal drawdown and filling cycles based on hydrologic forecasts, ensuring multi-year carryover storage while preserving environmental flow requirements for downstream aquatic habitats.",
                    ],
                },
                {
                    "heading": "Climate Change Adaptation and Water Security",
                    "paragraphs": [
                        "Climate change accelerates hydrologic extreme events, shifting seasonal snowpack melt timelines, expanding arid climate zones, and increasing the frequency of heavy precipitation downpours. Water security requires adaptive planning capable of absorbing hydrological shocks without systemic failure.",
                        "Resilience measures combine structural interventions (such as expanding storage, inter-basin transfers, and flood detention basins) with non-structural strategies (including demand management, water metering, rainwater harvesting, watershed reforestation, and water trading markets).",
                    ],
                },
            ],
        ),
        (
            "Groundwater_Management.pdf",
            "Groundwater Management: Hydrogeology, Protection, and Governance",
            [
                {
                    "heading": "Hydrogeology and Aquifer Dynamics",
                    "paragraphs": [
                        "Groundwater represents the primary freshwater storage on Earth, supplying drinking water to over 50 percent of the global human population and over 40 percent of agricultural irrigation. Aquifers are underground layers of water-bearing permeable rock, gravel, sand, or silt. Unconfined aquifers are replenished directly by surface infiltration, while confined aquifers are sandwiched between low-permeability aquitards.",
                        "Hydrogeological characterization relies on hydraulic conductivity, storativity, transmissivity, well pumping tests, piezometric monitoring networks, and isotopic tracer analysis to calculate safe yield extraction rates and model groundwater flow fields.",
                    ],
                },
                {
                    "heading": "Over-Exploitation, Subsidence, and Saline Intrusion",
                    "paragraphs": [
                        "Unregulated abstraction exceeding natural recharge causes severe water table declines, drying shallow wells, reducing river baseflows, and degrading groundwater-dependent wetlands. Excessive drawdown in coastal areas causes saltwater intrusion, pulling dense ocean saltwater into freshwater aquifers.",
                        "Land subsidence occurs when prolonged groundwater pumping reduces pore pressure, causing clay and silt beds within aquifers to consolidate irreversibly. Subsidence damages surface buildings, pipelines, roads, and flood protection levees in major agricultural basins and coastal megacities.",
                    ],
                },
                {
                    "heading": "Managed Aquifer Recharge (MAR) and Artificial Replenishment",
                    "paragraphs": [
                        "Managed Aquifer Recharge (MAR) encompasses engineered techniques designed to intentionally augment groundwater storage. Methods include surface infiltration basins, percolation ponds, aquifer storage and recovery (ASR) injection wells, and check dam structures built across ephemeral streams.",
                        "MAR projects capture surplus monsoon runoff, treated stormwater, or reclaimed municipal effluent, filtering water naturally through the vadose zone into underlying aquifers. MAR improves drought resilience, prevents seawater intrusion, and restores depleted groundwater storage.",
                    ],
                },
                {
                    "heading": "Groundwater Quality Protection and Contaminant Mitigation",
                    "paragraphs": [
                        "Groundwater contamination arises from point sources (leaking underground fuel tanks, industrial solvent spills, landfill leachate) and non-point sources (nitrate fertilizer leaching, pesticide runoff, municipal septic systems). Geogenic contaminants like geogenic arsenic and fluoride pose severe widespread health risks.",
                        "Protection strategies enforce wellhead protection zones (WHPZs), restrict chemical storage near recharge areas, mandate impermeable liners for landfills, and implement permeable reactive barriers (PRBs) or pump-and-treat remediation systems for contaminated plumes.",
                    ],
                },
            ],
        ),
        (
            "Water_Quality.pdf",
            "Water Quality: Standards, Contaminants, and Treatment Technologies",
            [
                {
                    "heading": "Why Water Quality Matters and Regulatory Standards",
                    "paragraphs": [
                        "Water quality defines the chemical, physical, and biological characteristics of water relative to its designated use. World Health Organization (WHO) Guidelines and national Environmental Protection Agency (EPA) regulations specify Maximum Contaminant Levels (MCLs) for physical parameters (pH, turbidity, total dissolved solids), chemical pollutants (nitrates, heavy metals, synthetic organics), and biological pathogens.",
                        "Water quality monitoring networks utilize continuous automated sensors, turbidity meters, pH probes, electrical conductivity (EC) sensors, dissolved oxygen (DO) meters, and gas chromatography-mass spectrometry (GC-MS) laboratory analysis to detect contamination early.",
                    ],
                },
                {
                    "heading": "Sources of Pollution: Point and Non-Point Source Pollution",
                    "paragraphs": [
                        "Point source pollution originates from identifiable single locations, such as municipal wastewater treatment plant outfalls, factory effluent pipes, and industrial facilities. Point sources are regulated via discharge permits and effluent limitations.",
                        "Non-point source (diffuse) pollution occurs when rainfall runoff washes land contaminants into waterways. Key non-point sources include agricultural fertilizers (nitrogen and phosphorus causing severe eutrophication and toxic microcystin algal blooms), urban stormwater runoff carrying heavy metals and microplastics, and sediment erosion.",
                    ],
                },
                {
                    "heading": "Chemical Contaminants: Heavy Metals, Nitrates, and PFAS",
                    "paragraphs": [
                        "Heavy metals such as lead, cadmium, mercury, and hexavalent chromium enter water through mining, industrial discharge, and corroding lead plumbing pipes. Chronic exposure leads to severe neurological damage, kidney failure, and developmental disorders.",
                        "Per- and polyfluoroalkyl substances (PFAS), known as 'forever chemicals', are persistent industrial compounds that accumulate in water systems and human blood. Nitrate contamination from intensive agriculture causes methemoglobinemia (blue baby syndrome) and requires advanced ion exchange or reverse osmosis treatment.",
                    ],
                },
                {
                    "heading": "Water and Wastewater Treatment Processes",
                    "paragraphs": [
                        "Conventional drinking water treatment follows a multi-stage process: coagulation/flocculation (adding alum to bind suspended solids), sedimentation (settling flocs), sand filtration, and chemical disinfection (chlorination, ozonation, or ultraviolet UV irradiation).",
                        "Wastewater treatment plants utilize primary physical settling, secondary biological activated sludge aeration tanks to decompose organic matter, tertiary nutrient removal (denitrification and phosphorus precipitation), and membrane bioreactors (MBR) or reverse osmosis (RO) for indirect potable reuse.",
                    ],
                },
            ],
        ),
        (
            "Flood_Control.pdf",
            "Flood Control: Risk Assessment, Infrastructure, and Resilience",
            [
                {
                    "heading": "Flood Risk, Drivers, and Exposure",
                    "paragraphs": [
                        "Floods occur when water inundates normally dry land, driven by prolonged heavy rainfall, flash downpours, river overflows, storm surges, rapid snowmelt, or structural dam breaches. Flood risk is determined by hazard frequency, hydrologic exposure, and socioeconomic vulnerability.",
                        "Unplanned urban growth in low-lying floodplains drastically increases flood exposure. Impervious urban surfaces (concrete, asphalt) impair natural infiltration, dramatically accelerating peak stormwater discharge and increasing urban flash flooding.",
                    ],
                },
                {
                    "heading": "Structural Flood Mitigation Engineering",
                    "paragraphs": [
                        "Structural engineering defenses modify flood pathways to protect high-density populations and critical infrastructure. Primary structural interventions include levees, floodwalls, river channel widening/dredging, flood diversion canals, and upstream detention reservoirs.",
                        "Coastal flood engineering employs seawalls, storm surge barriers, breakwaters, elevated coastal dikes, and large-scale pumping stations capable of removing thousands of cubic meters of floodwater per minute during extreme storm events.",
                    ],
                },
                {
                    "heading": "Non-Structural Flood Management and Early Warning Systems",
                    "paragraphs": [
                        "Non-structural strategies reduce vulnerability without altering physical waterways. Key measures include floodplain land-use zoning regulations, building codes requiring elevated foundations, flood risk insurance schemes, and wetland conservation.",
                        "Early Warning Systems (EWS) integrate weather radar, river gauge telemetering, hydrologic runoff forecasts, and real-time mobile cell-broadcast emergency notifications to allow timely evacuation of vulnerable populations prior to peak river crests.",
                    ],
                },
                {
                    "heading": "Nature-Based Solutions and Urban Sponge Cities",
                    "paragraphs": [
                        "Nature-based solutions (NbS) restore natural ecosystem hydrology to mitigate flood energy. Methods include restoring river meanders, reconnecting floodplain wetlands, and establishing coastal mangrove belts to attenuate wave energy.",
                        "The Sponge City concept transforms urban landscapes by integrating permeable pavements, bioswales, rain gardens, green roofs, and urban retention ponds to capture, slow, and filter up to 80 percent of stormwater runoff locally.",
                    ],
                },
            ],
        ),
        (
            "Drought_Management.pdf",
            "Drought Management: Monitoring, Mitigation, and Resilience",
            [
                {
                    "heading": "Understanding Drought Categories and Indices",
                    "paragraphs": [
                        "Drought is a prolonged, insidious moisture deficit that propagates through the hydrological cycle. It is categorized into four main phases: Meteorological Drought (precipitation deficit), Agricultural Drought (soil moisture deficit impairing crop yields), Hydrological Drought (declining streamflow, lake levels, and groundwater tables), and Socioeconomic Drought (water supply shortages disrupting economic goods and services).",
                        "Drought monitoring relies on key indices including the Standardized Precipitation Index (SPI), Standardized Precipitation Evapotranspiration Index (SPEI), Palmer Drought Severity Index (PDSI), and satellite-derived Normalized Difference Vegetation Index (NDVI).",
                    ],
                },
                {
                    "heading": "Drought Preparedness and Municipal Contingency Planning",
                    "paragraphs": [
                        "Proactive drought management replaces reactive crisis response with multi-staged drought contingency plans. Municipal plans define operational trigger levels based on reservoir storage thresholds, initiating staged conservation targets (Stage 1 voluntary conservation, Stage 2 mandatory outdoor watering bans, Stage 3 emergency rationing).",
                        "Municipal resilience is enhanced through water loss reduction (detecting network pipe leaks), dual-pipe graywater recycling networks, brackish water desalination, and inter-utility emergency interconnections.",
                    ],
                },
                {
                    "heading": "Agricultural Resilience, Micro-Irrigation, and Crop Adaptation",
                    "paragraphs": [
                        "Agriculture accounts for over 70 percent of global freshwater consumption. Enhancing agricultural drought resilience requires transitioning from flood/furrow irrigation to precision micro-irrigation systems such as drip lines and micro-sprinklers.",
                        "Soil moisture conservation techniques—including conservation tillage, cover cropping, and mulching—reduce evaporative water loss. Agronomic adaptation incorporates drought-tolerant crop varieties, deficit irrigation scheduling, and crop rotation strategies tailored to reduced water allocations.",
                    ],
                },
                {
                    "heading": "Long-Term Aridity Adaptation and Water Reuse Technologies",
                    "paragraphs": [
                        "Arid regions adapt through large-scale water reuse and advanced desalination. Seawater Reverse Osmosis (SWRO) removes dissolved salts using high-pressure semi-permeable membranes, providing drought-proof drinking water supplies for arid coastal regions.",
                        "Direct and Indirect Potable Reuse (DPR/IPR) purify municipal wastewater through advanced oxidation, microfiltration, and reverse osmosis, returning high-purity water to reservoirs or aquifers, establishing a closed-loop sustainable water cycle.",
                    ],
                },
            ],
        ),
        (
            "Water_Policy_and_Governance.pdf",
            "Water Policy, Laws, and Global Resource Governance",
            [
                {
                    "heading": "UN Sustainable Development Goal 6 (SDG 6) and Human Rights",
                    "paragraphs": [
                        "United Nations Sustainable Development Goal 6 (SDG 6) commits the global community to ensuring access to safe water and sanitation for all by 2030. SDG 6 targets encompass universal drinking water access, adequate sanitation, improved ambient water quality, increased water-use efficiency, integrated water management, and water ecosystem protection.",
                        "In 2010, the UN General Assembly explicitly recognized access to clean, safe, acceptable, and affordable drinking water and sanitation as a fundamental human right essential for the full enjoyment of life and human dignity.",
                    ],
                },
                {
                    "heading": "Transboundary Water Treaties and International Water Law",
                    "paragraphs": [
                        "Over 260 international river basins cross political boundaries, serving 40 percent of the world's population. Transboundary water governance requires international legal treaties and river basin commissions to prevent hydropolitical conflict.",
                        "International water law principles—codified in the 1997 UN Watercourses Convention—rely on two foundational pillars: Equitable and Reasonable Utilization of shared waters, and the Obligation Not to Cause Significant Harm to downstream riparian states.",
                    ],
                },
                {
                    "heading": "Economic Instruments: Water Pricing, Water Rights, and Subsidies",
                    "paragraphs": [
                        "Economic instruments incentivize water conservation while funding utility infrastructure maintenance. Block-rate tariffs charge higher volumetric rates for high-volume consumption, protecting basic lifeline water affordability for low-income households while discouraging wasteful use.",
                        "Tradable water rights allocation markets allow agricultural and industrial water users to trade volumetric water entitlements, encouraging water-efficient technology adoption and transferring water to high-value uses during extreme scarcity.",
                    ],
                },
                {
                    "heading": "Community-Based Watershed Management and Water Governance",
                    "paragraphs": [
                        "Effective water governance requires decentralization and direct community participation. Water User Associations (WUAs) empower local farming communities to manage canal distribution, maintain infrastructure, and resolve local allocation disputes equity.",
                        "Integrating traditional ecological knowledge—such as ancient qanat underground channels, stepwells, and traditional rainwater harvesting bunds—with modern hydrologic science yields culturally robust, climate-resilient water stewardship.",
                    ],
                },
            ],
        ),
    ]

    for filename, title, sections in documents:
        build_pdf(KNOWLEDGE_BASE / filename, title, sections)
        print(f"Created {filename}")


if __name__ == "__main__":
    main()
