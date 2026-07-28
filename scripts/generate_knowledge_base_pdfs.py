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
        heading = section["heading"]
        paragraphs = section["paragraphs"]
        story.append(Paragraph(heading, heading_style))
        for paragraph in paragraphs:
            story.append(Paragraph(paragraph, body_style))
            story.append(Spacer(1, 4))
        if index < len(sections) - 1:
            story.append(PageBreak())

    doc.build(story)


def main() -> None:
    KNOWLEDGE_BASE.mkdir(parents=True, exist_ok=True)

    documents = [
        (
            "Water_Resources.pdf",
            "Water Resources: Planning, Use, and Sustainability",
            [
                {
                    "heading": "Introduction",
                    "paragraphs": [
                        "Water resources include rivers, lakes, wetlands, reservoirs, groundwater, and precipitation that replenish the hydrologic system. They support agriculture, domestic supply, industrial production, ecosystem resilience, and public health. Because the same water bodies serve multiple users and functions, planning must balance human demand with ecological protection and climate variability.",
                        "A strong water resources strategy begins with reliable data collection and transparent governance. Hydrologists, engineers, planners, and communities all contribute to basin-level decisions. These decisions often involve seasonal forecasting, infrastructure upgrades, conservation programs, and participatory water allocation arrangements that are adapted to local conditions.",
                    ],
                },
                {
                    "heading": "Integrated Management",
                    "paragraphs": [
                        "Integrated water resources management emphasizes coordinated development and use of land, water, and related resources to maximize economic and social welfare without undermining ecosystem sustainability. This means aligning flood control, irrigation, wastewater treatment, public water supply, and habitat restoration in a shared planning framework.",
                        "Modern planning tools combine remote sensing, hydrologic modelling, citizen reporting, and geographic information systems. These tools help identify pressure points such as over-allocation, low-flow conditions, saline intrusion, and loss of wetland connectivity. When used well, they allow agencies to evaluate trade-offs and select interventions that improve long-term reliability.",
                        "The most effective strategies also include demand management. Efficient irrigation, leak detection, water reuse, and pricing reform can reduce waste while preserving service quality. In many regions, non-structural measures such as conservation education and drought preparedness planning yield high benefits at lower cost than building new infrastructure.",
                    ],
                },
                {
                    "heading": "Climate and Resilience",
                    "paragraphs": [
                        "A changing climate is increasing the variability of rainfall, snowmelt, and streamflow. Water managers now need to plan for both extreme floods and prolonged droughts. Seasonal forecasting, flexible operating rules, and contingency plans improve resilience when conditions change quickly.",
                        "Resilient systems are designed around redundancy, diversity, and adaptive management. Storage reservoirs, groundwater recharge projects, wetlands, and distributed treatment systems can all contribute to reliability. By combining multiple options, a region can better absorb shocks while maintaining essential services to farmers, households, and ecosystems.",
                    ],
                },
            ],
        ),
        (
            "Groundwater_Management.pdf",
            "Groundwater Management: Protection, Recharge, and Governance",
            [
                {
                    "heading": "Groundwater as a Strategic Resource",
                    "paragraphs": [
                        "Groundwater is one of the most important freshwater reserves on Earth, especially where surface water is seasonal or unreliable. It supports irrigation, municipal supply, industry, and baseflow to rivers and wetlands. Because groundwater moves slowly and accumulates over long periods, it is especially vulnerable to overuse, contamination, and poor governance.",
                        "Managing groundwater requires understanding aquifer geometry, recharge rates, water quality, and extraction trends. Hydrogeologists use well logs, pumping tests, isotope tracing, and monitoring networks to estimate how much water can be safely used. These datasets are essential for preventing permanent declines in storage and protecting dependent ecosystems.",
                    ],
                },
                {
                    "heading": "Recharge and Conservation",
                    "paragraphs": [
                        "Artificial recharge systems improve the replenishment of aquifers through infiltration basins, recharge trenches, managed aquifer storage, and stormwater capture. These approaches are especially useful in urban areas where impervious surfaces reduce natural infiltration. Recharge projects can also be combined with water harvesting to reduce flood risk and improve drought resilience.",
                        "Conservation measures are equally important. Drip irrigation, crop selection, and improved irrigation scheduling can greatly reduce pumping demand. In many basins, regulatory frameworks limit new withdrawals during critical periods and require meter installation so that use can be monitored and enforced.",
                        "Governance also needs to address equity. Groundwater use often crosses property boundaries and administrative jurisdictions, making coordination challenging. Effective management frameworks encourage transparency, basin-level planning, and local participation while preventing unregulated extraction by large users.",
                    ],
                },
                {
                    "heading": "Quality and Risk",
                    "paragraphs": [
                        "Groundwater contamination can result from industrial spills, untreated sewage, nitrate leaching, arsenic mobilization, and poor well construction. Once polluted, aquifers are difficult and expensive to remediate. Prevention is therefore more cost-effective than treatment, and monitoring should be designed to detect emerging risks early.",
                        "Integrated groundwater management also considers land use planning. Protecting recharge zones, restricting hazardous activities near wells, and enforcing septic standards can significantly reduce contamination risk. These measures safeguard both water quality and public health over the long term.",
                    ],
                },
            ],
        ),
        (
            "Water_Quality.pdf",
            "Water Quality: Monitoring, Treatment, and Protection",
            [
                {
                    "heading": "Why Water Quality Matters",
                    "paragraphs": [
                        "Water quality determines whether water is safe for drinking, agricultural use, industrial production, recreation, and ecosystem support. Even water that is plentiful can become unusable if it contains excessive nutrients, pathogens, chemicals, sediments, or harmful temperatures. Protecting water quality is therefore as important as maintaining water quantity.",
                        "Monitoring programs track physical, chemical, and biological indicators such as turbidity, pH, dissolved oxygen, conductivity, pathogens, heavy metals, and nutrient concentrations. By comparing measurements over time and across locations, agencies can identify pollution sources and respond before risks expand.",
                    ],
                },
                {
                    "heading": "Sources of Pollution",
                    "paragraphs": [
                        "Pollution enters water bodies through point sources such as wastewater discharge pipes and industrial outfalls, and through diffuse sources such as agricultural runoff, urban stormwater, and erosion. Nutrient pollution can cause algal blooms, depletion of oxygen, and fish kills. Sediment runoff can reduce visibility, damage habitats, and interfere with drinking water treatment.",
                        "Emerging contaminants, including pharmaceuticals, personal care products, and microplastics, are also changing the way regulators approach monitoring. These substances often appear in low concentrations but may have long-term ecological and human health effects. Their detection requires advanced analytical methods and careful interpretation.",
                    ],
                },
                {
                    "heading": "Treatment and Protection",
                    "paragraphs": [
                        "Water treatment systems vary by use case. Drinking water systems often rely on coagulation, filtration, disinfection, and pH adjustment, while wastewater plants use biological treatment, clarification, and nutrient removal processes. Green infrastructure such as constructed wetlands and vegetated swales can complement engineered treatment systems by capturing runoff before it reaches rivers or lakes.",
                        "Effective water quality management requires coordination across sectors. Farmers, utilities, industries, construction firms, and local governments all shape the quality of the receiving water. Strong regulations, public education, and incentives for pollution prevention can reduce the burden on treatment systems and improve environmental outcomes.",
                    ],
                },
            ],
        ),
        (
            "Flood_Control.pdf",
            "Flood Control: Infrastructure, Planning, and Community Safety",
            [
                {
                    "heading": "Flood Risk and Exposure",
                    "paragraphs": [
                        "Floods are among the most damaging natural hazards because they can destroy homes, disrupt transport, contaminate water supplies, and interrupt economic activity. Flood risk arises from intense rainfall, river overflow, coastal storm surge, rapid snowmelt, and land use changes that reduce infiltration. The consequences are often magnified when settlements grow in flood-prone areas.",
                        "A modern flood management approach combines structural and non-structural measures. Structural options include levees, detention basins, floodwalls, channel improvements, and elevated roads. Non-structural options include zoning, floodplain mapping, early warning systems, insurance policies, and emergency preparedness.",
                    ],
                },
                {
                    "heading": "Designing Resilient Systems",
                    "paragraphs": [
                        "Resilient flood systems are designed to withstand events beyond historical averages. This often means planning for extreme precipitation, sea level rise, and infrastructure failure. Climate adaptation strategies can include wetland restoration, green roofs, permeable pavements, and managed storage that slows runoff before it reaches rivers.",
                        "Good flood control planning also considers community behavior. Evacuation routes, public communication, and household preparedness all influence whether a hazard becomes a disaster. When communities understand their risk and know how to respond, damage can be reduced even when water levels exceed expectations.",
                    ],
                },
                {
                    "heading": "Integrated Flood Management",
                    "paragraphs": [
                        "Integrated flood management focuses on protecting people, property, and ecosystems at the basin scale. It recognizes that upstream land use affects downstream flow, and that floodplains can provide valuable storage and habitat if managed carefully. Restoring wetlands and reconnecting rivers to floodplains can reduce peak flows while improving biodiversity.",
                        "The most successful programs combine engineering with local knowledge and long-term maintenance. Levees require inspections, pumping stations need upkeep, and warning systems require regular testing. By investing in maintenance and community engagement, agencies can ensure that flood control infrastructure remains effective for decades.",
                    ],
                },
            ],
        ),
        (
            "Drought_Management.pdf",
            "Drought Management: Preparedness, Response, and Recovery",
            [
                {
                    "heading": "Understanding Drought",
                    "paragraphs": [
                        "Drought is a slow-onset hazard that can persist for months or years, causing water shortages, crop failure, ecosystem stress, and economic losses. Unlike floods, droughts are often difficult to recognize early because their impacts accumulate gradually. Effective monitoring relies on precipitation records, soil moisture estimates, reservoir storage, groundwater levels, and vegetation indicators.",
                        "Because drought affects different sectors in different ways, management strategies must be flexible. Agriculture may need irrigation restrictions and crop switching, while municipalities may focus on conservation targets and emergency supply arrangements. A well-designed drought plan can reduce the severity of impacts by promoting early action rather than reactive emergency measures.",
                    ],
                },
                {
                    "heading": "Preparedness and Response",
                    "paragraphs": [
                        "Preparedness measures include water conservation campaigns, drought contingency plans, water banking, and reserve storage. Communities can also reduce risk through demand management, leakage control, and use of alternative sources such as recycled water. These measures become more effective when triggers are clear and communications are timely.",
                        "During drought conditions, agencies often implement staged restrictions, prioritize critical uses, and coordinate with utilities, farmers, and businesses. Transparency is essential because public trust is stronger when people understand the reasons behind restrictions and the expected duration of shortages. Recovery planning should begin before the drought ends so that communities can restore systems quickly and avoid future vulnerability.",
                    ],
                },
                {
                    "heading": "Building Long-Term Resilience",
                    "paragraphs": [
                        "Long-term drought resilience depends on both infrastructure and governance. Investments in storage, recharge, water reuse, efficient irrigation, and ecosystem restoration can reduce the impact of dry periods. At the same time, institutions need clear legal frameworks, robust data systems, and regular updates to drought plans.",
                        "The most sustainable strategies recognize that drought is not only a hydrologic event but also a social and economic challenge. By combining technical planning, community participation, and transparent decision-making, water managers can protect livelihoods and ecosystems even under increasing climatic stress.",
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
